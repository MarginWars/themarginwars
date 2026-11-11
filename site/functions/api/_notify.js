// Shared notifier for every site form. Storage happens before this is called (always on).
//  - Email: MAILER service binding -> Worker themarginwars-contact-mailer -> Email Routing send_email.
//    Recipients from the NOTIFY_EMAILS secret (each must be a verified Email Routing destination and on the
//    Worker allow-list). Full details go to the team only. Never to the visitor.
//  - Slack: SLACK_WEBHOOK_URL (private #margin-wars). Summary only: kind, topic, name, company, record id.
//    Never the visitor's email address or message body.
// SITE_ENV="dev" prefixes [DEV]; test submissions are prefixed [TEST].
export const envTag = env => (String(env.SITE_ENV || "").toLowerCase() === "dev" ? "DEV" : "");
export const isQa = (env, request) => !!env.QA_TOKEN && request.headers.get("x-tmw-qa") === env.QA_TOKEN;
export async function notify(env, s) {
  const tag = envTag(env), res = [];
  const pre = `${tag ? "[" + tag + "] " : ""}${s.test ? "[TEST] " : ""}`;
  if (env.MAILER) {
    try {
      const to = String(env.NOTIFY_EMAILS || "").split(",").map(x => x.trim()).filter(Boolean);
      const r = await env.MAILER.fetch("https://mailer/notify", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ ...s, tag, to }) });
      const d = await r.json().catch(() => ({})); res.push(d.ok ? "mail:ok" : "mail:" + String(d.summary || d.error || r.status).slice(0, 240));
    } catch (x) { res.push("mail:" + String(x && x.message || x).slice(0, 120)); }
  }
  if (env.SLACK_WEBHOOK_URL) {
    try {
      const text = `${pre}${s.kind}: ${s.topic}\nName: ${s.name}\nCompany: ${s.company || "(not given)"}\nRecord: ${s.id} (${s.store}, ${s.host})`;
      const r = await fetch(env.SLACK_WEBHOOK_URL, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ text }) });
      res.push(r.ok ? "slack:ok" : "slack:" + r.status);
    } catch (x) { res.push("slack:" + String(x && x.message || x).slice(0, 120)); }
  }
  return res;
}
