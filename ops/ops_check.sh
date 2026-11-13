#!/usr/bin/env bash
# The Margin Wars ops check. Read-only: stores nothing, submits no form data.
# Usage: ops_check.sh [--slack]      (--slack posts the summary to $OPS_SLACK_WEBHOOK_URL, public #margin-wars-ops)
# Exit 0 = all green, 1 = at least one check failed. Safe to run from a daily routine.
# Optional env: OPS_SLACK_WEBHOOK_URL (incoming webhook for #margin-wars-ops), CLOUDFLARE_API_TOKEN/CLOUDFLARE_ACCOUNT_ID
# (or a logged-in wrangler) to report the live deployment ids. No visitor data is read or printed.
set -uo pipefail
PROD=https://themarginwars.com; DEV=https://themarginwars-dev.pages.dev
FAILS=0; OUT=()
ok(){ OUT+=("PASS  $1"); }; bad(){ OUT+=("FAIL  $1"); FAILS=$((FAILS+1)); }
code(){ curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$@"; }
check(){ local want=$1 label=$2; shift 2; local c; c=$(code "$@"); [ "$c" = "$want" ] && ok "$label ($c)" || bad "$label (got $c, want $want)"; }
for ENV in prod dev; do
  B=$PROD; [ $ENV = dev ] && B=$DEV
  t=$(curl -s -o /dev/null -w '%{http_code} %{time_total}' --max-time 20 "$B/"); [ "${t%% *}" = 200 ] && ok "$ENV up: home 200 in ${t#* }s" || bad "$ENV home: $t"
  # every public page in the production sitemap, mapped onto this host
  urls=$(curl -s --max-time 20 "$PROD/sitemap.xml" | grep -oE '<loc>[^<]+' | sed 's/<loc>//'); n=0; f=0; fl=""
  for u in $urls; do n=$((n+1)); c=$(code "${u/$PROD/$B}"); [ "$c" = 200 ] || { f=$((f+1)); fl="$fl ${u#$PROD}=$c"; }; done
  [ $n -gt 50 ] && [ $f -eq 0 ] && ok "$ENV pages: $n/$n return 200" || bad "$ENV pages: $((n-f))/$n 200;$fl"
  check 404 "$ENV unknown URL returns 404" "$B/ops-check-no-such-page"
  check 405 "$ENV form endpoint alive (GET /api/contact)" "$B/api/contact"
  check 422 "$ENV contact validation (empty POST, nothing stored)" -X POST -H 'content-type: application/json' -d '{}' "$B/api/contact"
  check 400 "$ENV assistant escalation validation (empty POST, nothing stored)" -X POST -H 'content-type: application/json' -d '{}' "$B/api/escalate"
  check 200 "$ENV sitemap.xml" "$B/sitemap.xml"
  for feed in feeds/wire.xml feeds/wire.atom feeds/route-briefs.xml feeds/dates.ics; do check 200 "$ENV $feed" "$B/$feed"; done
  rss=$(curl -s --max-time 20 "$B/feeds/wire.xml"); echo "$rss" | grep -q '<link>https://themarginwars.com' && ! echo "$rss" | grep -qiE "pending (avi|review)|preview ·|\\[preview\\]" && ok "$ENV RSS points at production, no preview labels" || bad "$ENV RSS links/labels"
  r=$(curl -s --max-time 20 "$B/robots.txt"); xr=$(curl -sI --max-time 20 "$B/" | tr -d '\r' | grep -i '^x-robots-tag' | head -1)
  if [ $ENV = prod ]; then echo "$r" | grep -q '^Allow: /' && [ -z "$xr" ] && ok "prod indexable (robots allow, no X-Robots-Tag)" || bad "prod indexing: robots/X-Robots-Tag wrong"
  else echo "$r" | grep -q '^Disallow: /$' && echo "$xr" | grep -qi noindex && ok "dev noindex (robots disallow + X-Robots-Tag)" || bad "dev indexing guard missing"; fi
done
loc=$(curl -sI --max-time 20 https://www.themarginwars.com/about | tr -d '\r' | awk 'tolower($1)=="location:"{print $2}'); c=$(code https://www.themarginwars.com/about)
[ "$c" = 301 ] && [ "$loc" = "https://themarginwars.com/about" ] && ok "www -> apex 301" || bad "www redirect ($c $loc)"
for h in themarginwars.com www.themarginwars.com; do
  end=$(echo | openssl s_client -servername $h -connect $h:443 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  if [ -n "$end" ]; then d=$(( ( $(date -d "$end" +%s) - $(date +%s) ) / 86400 )); [ $d -ge 14 ] && ok "SSL $h valid, $d days left" || bad "SSL $h expires in $d days"; else bad "SSL $h unreadable"; fi
done
if command -v npx >/dev/null && { [ -n "${CLOUDFLARE_API_TOKEN:-}" ] || [ -d "$HOME/.wrangler" ] || [ -d "$HOME/.config/.wrangler" ]; }; then
  for p in themarginwars themarginwars-dev; do
    id=$(cd /tmp && npx --yes wrangler pages deployment list --project-name $p --environment production --json 2>/dev/null | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d[0].get("Id") or d[0].get("id"),d[0].get("Created on") or "")' 2>/dev/null)
    [ -n "$id" ] && ok "$p live deploy: $id" || OUT+=("INFO  $p deploy id unavailable")
  done
fi
SUM="The Margin Wars ops check $(TZ=America/Los_Angeles date '+%Y-%m-%d %H:%M %Z'): $([ $FAILS = 0 ] && echo 'ALL GREEN' || echo "$FAILS FAILED")"
printf '%s\n' "$SUM" "${OUT[@]}"
if [ "${1:-}" = "--slack" ] && [ -n "${OPS_SLACK_WEBHOOK_URL:-}" ]; then
  body=$(printf '%s\n' "$SUM" "${OUT[@]}" | python3 -c 'import json,sys;print(json.dumps({"text":"```"+sys.stdin.read()+"```"}))')
  curl -s -o /dev/null -X POST -H 'content-type: application/json' -d "$body" "$OPS_SLACK_WEBHOOK_URL"
fi
[ $FAILS = 0 ]
