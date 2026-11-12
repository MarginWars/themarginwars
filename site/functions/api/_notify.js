// Shared notifier for every site form. Storage happens before this is called (always on).
//  1. Primary: the signed alert route (MW_ALERT_URL, HMAC-SHA256 with MW_ALERT_SECRET over `${ts}.${body}`,
//     headers X-MW-Timestamp / X-MW-Signature, 25 s timeout). It posts the summary to private #margin-wars and
//     emails the full record to the team. Same id is deduped on the receiving side.
//  2. Email fallback (only when the primary did not report mail delivered):
//     MAILER service binding -> Worker themarginwars-contact-mailer -> Email Routing send_email.
//     Recipients from the NOTIFY_EMAILS secret. Full details go to the team only. Never to the visitor.
//     There is no Slack fallback: the old SLACK_WEBHOOK_URL path was retired on 10 Nov 2026.
// SITE_ENV="dev" prefixes [DEV]; test submissions are prefixed [TEST].
export const envTag = env => (String(env.SITE_ENV || "").toLowerCase() === "dev" ? "DEV" : "");
export const isQa = (env, request) => !!env.QA_TOKEN && request.headers.get("x-tmw-qa") === env.QA_TOKEN;

const UA = "themarginwars-site/1.0";
const TIMEOUT_MS = 25000; // the alert route answers in ~7-10 s (it sends Slack + email before replying); notify runs in waitUntil (30 s budget), so visitors never wait. Aborting early makes the route drop its dedupe record.
const short = (x, n = 120) => String((x && x.message) || x).slice(0, n);

// Site attribution touch {source, medium, campaign, content, term, referrer, landing, at} -> alert-route touch.
function touchOut(t) {
  if (!t || typeof t !== "object") return null;
  const o = {};
  const map = { source: "utm_source", medium: "utm_medium", campaign: "utm_campaign", content: "utm_content", term: "utm_term", referrer: "referrer", landing: "landing_path", at: "ts" };
  for (const [k, v] of Object.entries(map)) if (t[k]) o[v] = String(t[k]).slice(0, 200);
  return Object.keys(o).length ? o : null;
}
export function attrOut(a) {
  if (!a || typeof a !== "object") return null;
  const first = touchOut(a.first), last = touchOut(a.last);
  if (!first && !last) return null;
  const o = {}; if (first) o.first = first; if (last) o.last = last; // omit empty touches rather than send null
  return o;
}

async function hmacHex(secret, msg) {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(msg));
  return [...new Uint8Array(mac)].map(b => b.toString(16).padStart(2, "0")).join("");
}

// Returns {ok, slack, mail} from the alert route, or {ok:false, error} on any failure.
async function viaHarness(env, payload) {
  if (!env.MW_ALERT_URL || !env.MW_ALERT_SECRET) return { ok: false, slack: false, mail: false, error: "not-configured" };
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort("timeout"), TIMEOUT_MS);
  try {
    const body = JSON.stringify(payload); // sign these exact bytes, send these exact bytes
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const signature = await hmacHex(env.MW_ALERT_SECRET, `${timestamp}.${body}`);
    const r = await fetch(env.MW_ALERT_URL, {
      method: "POST", signal: ctl.signal, body,
      headers: { "content-type": "application/json", "user-agent": UA, "X-MW-Timestamp": timestamp, "X-MW-Signature": signature },
    });
    const d = await r.json().catch(() => null);
    if (!r.ok) return { ok: false, slack: false, mail: false, error: "http " + r.status };
    if (!d || typeof d !== "object") return { ok: false, slack: false, mail: false, error: "bad-json" };
    return { ok: d.ok === true, slack: d.slack === true, mail: d.mail === true, error: d.ok === true ? "" : "ok:false" };
  } catch (x) {
    return { ok: false, slack: false, mail: false, error: ctl.signal.aborted ? "timeout" : short(x) };
  } finally { clearTimeout(timer); }
}

// s: the record the form already builds; extra: {form, page, attribution} (attribution in site shape, first + last touch).
export async function notify(env, s, extra = {}) {
  const tag = envTag(env), res = [];

  const payload = { ...s, tag, env: tag === "DEV" ? "dev" : "prod" };
  if (extra.form) payload.form = extra.form;
  if (extra.page) payload.page = String(extra.page).slice(0, 300);
  const attribution = attrOut(extra.attribution);
  if (attribution) payload.attribution = attribution;

  const h = await viaHarness(env, payload);
  if (h.ok) return ["harness:ok"]; // delivered to Slack and email: skip the old path so nothing posts twice
  // Failure is recorded (notify_error) and logged; the "harness-fail" entry does not count against delivery.
  res.push(`harness-fail:${h.error || "unknown"} slack=${h.slack} mail=${h.mail}`);
  console.error("[notify] alert route failed, falling back", s.id, h.error, "slack=" + h.slack, "mail=" + h.mail);

  if (h.mail) res.push("mail:ok(harness)");
  else if (env.MAILER) {
    try {
      const to = String(env.NOTIFY_EMAILS || "").split(",").map(x => x.trim()).filter(Boolean);
      const r = await env.MAILER.fetch("https://mailer/notify", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ ...s, tag, to }) });
      const d = await r.json().catch(() => ({})); res.push(d.ok ? "mail:ok" : "mail:" + String(d.summary || d.error || r.status).slice(0, 240));
    } catch (x) { res.push("mail:" + short(x)); }
  }
  // Slack has no fallback since 10 Nov 2026 (old "Margin Wars Alerts" webhook retired per Avi 5:27 PM PT).
  // A Slack failure on the route is recorded (and the email fallback still carries the full record).
  res.push(h.slack ? "slack:ok(harness)" : "slack-fail:no-fallback");
  return res;
}

// Delivered when the email reached the team (route or fallback); a Slack-only miss is recorded in notify_error.
export const delivered = res => res.includes("harness:ok") || res.some(x => x.startsWith("mail:ok"));
