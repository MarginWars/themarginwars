#!/usr/bin/env bash
# The Margin Wars site build.
#   site/build.sh            dist mode: site/src -> site/dist (make_dist: self-hosted fonts, per-route purged CSS bundles)
#   site/build.sh full       run every layer (the old box build.sh order) on a staged copy of site/src, write the
#                            result back to site/src and site/functions, then build site/dist
#   site/build.sh check      run every layer on a staged copy and FAIL if site/src or site/functions would change
#                            (proves the committed source is a fixed point of the layered build)
# Output: site/dist (gitignored) + qa-out/dist.md5 (md5 manifest, sorted by path).
# The layers still use their original box layout; they are staged into site/.build with @MW_ROOT@ replaced.
set -euo pipefail
MODE="${1:-dist}"
SITE="$(cd "$(dirname "$0")" && pwd)"; REPO="$(dirname "$SITE")"; ST="$SITE/.build"
FONTS="$SITE/layers/brand_logo/fonts"
export PYTHONHASHSEED=0 MW_BANNED_YML="$REPO/qa/compliance/banned.yml"
LAYERS=(copy_weekend ui_weekend route_brief copy_tighten about_rethink_1108 feeds normalize_suite buildout marketing season_rebase)
stage() {
  rm -rf "$ST"; mkdir -p "$ST/review_deploy" "$ST/site_qa"
  cp -a "$SITE/src" "$ST/site_calm"
  cp -a "$SITE/functions" "$ST/review_deploy/functions"
  for l in "${LAYERS[@]}"; do cp -a "$SITE/layers/$l" "$ST/$l"; done
  cp -a "$SITE/layers/brand_logo" "$ST/linkedin_page_1110"
  cp "$SITE/layers/_mwguard.py" "$ST/_mwguard.py"
  cp -a "$REPO/qa/lib/." "$ST/site_qa/"
  grep -rlE '@MW_ROOT@|@MW_FONTS@' "$ST" --include='*.py' --include='*.sh' | while read -r f; do
    sed -i "s#@MW_ROOT@#$ST#g; s#@MW_FONTS@#$FONTS#g" "$f"; done
}
run_layers() {  # any layer error fails the build (&& chain: set -e is off inside "( ) || ...")
  ( cd "$ST" &&
    python3 copy_weekend/apply_copy_weekend.py &&
    python3 ui_weekend/apply_ui.py &&
    python3 route_brief/apply_rb.py &&
    python3 copy_tighten/apply_tighten.py &&
    python3 about_rethink_1108/apply_about.py &&
    python3 feeds/apply_feeds.py &&
    python3 normalize_suite/apply_normalize.py &&
    python3 buildout/apply_buildout.py &&
    python3 marketing/apply_marketing.py &&
    python3 buildout/apply_esc_ts.py &&
    python3 season_rebase/apply_season.py ) > "$REPO/qa-out/layers.log" 2>&1 || { tail -40 "$REPO/qa-out/layers.log"; exit 1; }
}
make_dist() {
  ( cd "$ST" && python3 buildout/make_dist.py )
  rm -rf "$SITE/dist"; mv "$ST/site_dist" "$SITE/dist"
  ( cd "$SITE/dist" && find . -type f -print0 | sort -z | xargs -0 md5sum ) > "$REPO/qa-out/dist.md5"
  echo "dist: $(wc -l < "$REPO/qa-out/dist.md5") files, manifest md5 $(md5sum < "$REPO/qa-out/dist.md5" | cut -c1-32)"
}
mkdir -p "$REPO/qa-out"
case "$MODE" in
  dist) stage; make_dist ;;
  full) stage; run_layers
        rm -rf "$SITE/src" && cp -a "$ST/site_calm" "$SITE/src"
        rm -rf "$SITE/functions" && cp -a "$ST/review_deploy/functions" "$SITE/functions"
        stage; make_dist ;;
  check) stage; run_layers
        if diff -rq "$SITE/src" "$ST/site_calm" > "$REPO/qa-out/layers.diff" && diff -rq "$SITE/functions" "$ST/review_deploy/functions" >> "$REPO/qa-out/layers.diff"; then
          echo "layers: committed site/src and site/functions are a fixed point of the layered build"
        else
          echo "layers: FAIL - running the layers changes committed source:"; cat "$REPO/qa-out/layers.diff"; exit 1
        fi ;;
  *) echo "usage: site/build.sh [dist|full|check]"; exit 2 ;;
esac
