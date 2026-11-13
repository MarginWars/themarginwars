// Internal mailer for The Margin Wars contact form. Reached only through a Pages service binding
// (no public route). It sends a notification to the site owner's verified address; it never
// emails visitors. The default destination comes from the MAIL_TO secret (a verified Email Routing
// destination, also listed in the send_email binding's allowed_destination_addresses); no address is
// kept in source. Set it with: wrangler secret put MAIL_TO (in the directory holding wrangler.toml).
import { EmailMessage } from "cloudflare:email";

const FROM = "contact-form@themarginwars.com";
const clean = (s, n) => String(s || "").replace(/[\r\n]+/g, " ").slice(0, n);
const b64 = s => { const b = new TextEncoder().encode(s); let o = ""; for (const x of b) o += String.fromCharCode(x); return btoa(o).replace(/.{1,76}/g, "$&\r\n"); };
const encH = s => "=?UTF-8?B?" + btoa(String.fromCharCode(...new TextEncoder().encode(s))) + "?=";
const emailOk = e => /^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[^\s@<>()",;:]+$/.test(e);

export default {
  async fetch(request, env) {
    if (request.method !== "POST") return new Response("no", { status: 405 });
    let s; try { s = await request.json(); } catch { return new Response("bad", { status: 400 }); }
    const subject = clean(`${s.tag ? "[" + clean(s.tag, 8) + "] " : ""}${s.test ? "[TEST] " : ""}Site enquiry: ${s.topic} from ${s.name}`, 180);
    const body = [
      `New enquiry from the contact form on ${clean(s.host, 80)}.`, "",
      `Name: ${clean(s.name, 120)}`, `Email: ${clean(s.email, 200)}`, `Company: ${clean(s.company, 160) || "(not given)"}`,
      `Topic: ${clean(s.topic, 80)}`, `Reference: ${clean(s.id, 64)}`, `Received: ${clean(s.created_at, 40)} (UTC)`, "",
      "Message:", String(s.message || "").slice(0, 5000), "",
      "Reply to this email to answer the sender directly. Nothing was sent to the sender automatically."
    ].join("\r\n");
    const fallback = clean(env.MAIL_TO, 200);
    const list = (Array.isArray(s.to) && s.to.length ? s.to : (fallback ? [fallback] : [])).map(x => clean(x, 200)).filter(emailOk).slice(0, 5);
    if (!list.length) return Response.json({ ok: false, sent: 0, total: 0, error: "MAIL_TO is not configured" }, { status: 503 });
    const failed = [];
    let sent = 0;
    for (const TO of list) { const r = await sendOne(env, TO, subject, body, s); if (r === true) sent++; else failed.push(TO.split("@")[0] + ": " + r); }
    const summary = `${sent}/${list.length} sent` + (failed.length ? "; " + failed.join("; ") : "");
    return Response.json({ ok: failed.length === 0, sent, total: list.length, error: failed.length ? summary.slice(0, 300) : undefined, summary }, { status: failed.length && !sent ? 502 : 200 });
  }
};

async function sendOne(env, TO, subject, body, s) {
    const headers = [
      `From: The Margin Wars site <${FROM}>`, `To: <${TO}>`, `Subject: ${encH(subject)}`,
      `Message-ID: <${clean(s.id, 64)}.${crypto.randomUUID().slice(0,8)}@themarginwars.com>`, `Date: ${new Date().toUTCString()}`,
      "MIME-Version: 1.0", "Content-Type: text/plain; charset=UTF-8", "Content-Transfer-Encoding: base64"
    ];
    if (emailOk(s.email)) headers.splice(2, 0, `Reply-To: <${clean(s.email, 200)}>`);
    const raw = headers.join("\r\n") + "\r\n\r\n" + b64(body);
    try { await env.NOTIFY.send(new EmailMessage(FROM, TO, raw)); return true; }
    catch (e) { return String(e && e.message || e).slice(0, 200); }
}
