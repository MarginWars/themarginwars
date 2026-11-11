// POST /api/contact — The Margin Wars contact form.
// Stores every valid submission in D1 (CONTACT_DB), then notifies the site owner through the
// internal mailer Worker (MAILER service binding -> Email Routing send_email to the verified
// owner address). Never sends anything to the visitor.
import { limited, ipOf } from "./_rl.js";
import { notify, envTag, isQa, delivered } from "./_notify.js";
import { turnstile } from "./_ts.js";
import { cleanAttr, dims, count, countable } from "./_mk.js";

const TOPICS = ["Margin Teardown", "Campaign Sprint", "Board sessions and workshops", "Retained advisory", "Briefing invitation", "Something else"];
const LIM = { name: 120, email: 200, company: 160, message: 5000 };
const EMAIL = /^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[^\s@<>()",;:]{2,}$/;
const PROD = new Set(["themarginwars.com", "www.themarginwars.com"]);

const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" } });
const hex = b => [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join("");
async function sha(s) { return hex(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s))).slice(0, 32); }

export function validate(f) {
  const v = {
    name: String(f.name || "").trim(), email: String(f.email || "").trim(), company: String(f.company || "").trim(),
    topic: String(f.topic || "").trim(), message: String(f.message || "").trim()
  };
  const e = {};
  if (!v.name) e.name = "Please enter your name."; else if (v.name.length > LIM.name) e.name = `Please keep your name under ${LIM.name} characters.`;
  if (!v.email) e.email = "Please enter your email address."; else if (v.email.length > LIM.email || !EMAIL.test(v.email)) e.email = "Please enter a valid email address, like name@company.com.";
  if (v.company.length > LIM.company) e.company = `Please keep this under ${LIM.company} characters.`;
  if (!TOPICS.includes(v.topic)) e.topic = "Please choose a topic.";
  if (v.message.length < 10) e.message = "Please add a few words about what you need (at least 10 characters)."; else if (v.message.length > LIM.message) e.message = `Please keep your message under ${LIM.message} characters.`;
  return { v, e };
}

const SCHEMA = "CREATE TABLE IF NOT EXISTS submissions (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, host TEXT, name TEXT NOT NULL, email TEXT NOT NULL, company TEXT, topic TEXT NOT NULL, message TEXT NOT NULL, ip_hash TEXT, user_agent TEXT, is_test INTEGER NOT NULL DEFAULT 0, notified INTEGER NOT NULL DEFAULT 0, notify_error TEXT)";
let schemaReady = false;
async function ensureSchema(db) { if (schemaReady) return; await db.prepare(SCHEMA).run(); try { await db.prepare("ALTER TABLE submissions ADD COLUMN attribution TEXT").run(); } catch {} schemaReady = true; }


export async function onRequestPost(ctx) {
  const { request, env } = ctx;
  const ct = request.headers.get("content-type") || "";
  const wantsJson = ct.includes("application/json") || (request.headers.get("accept") || "").includes("application/json");
  const back = (q) => new Response(null, { status: 303, headers: { location: `/contact?form=${q}#contact-form`, "cache-control": "no-store" } });
  const fail = (o, s, q) => wantsJson ? json(o, s) : back(q);

  let f = {};
  try {
    if (ct.includes("application/json")) f = await request.json();
    else { const fd = await request.formData(); for (const [k, x] of fd.entries()) if (typeof x === "string") f[k] = x; }
  } catch { return fail({ ok: false, error: "We could not read the form. Please try again." }, 400, "error"); }

  // Honeypot: real visitors never see or fill "website". Pretend success, store nothing.
  if (String(f.website || "").trim()) return wantsJson ? json({ ok: true }) : back("sent");

  const { v, e } = validate(f);
  if (Object.keys(e).length) return fail({ ok: false, error: "Please check the highlighted fields.", errors: e }, 422, "error");

  if (!env.CONTACT_DB) return fail({ ok: false, error: "The form is not available right now. Please email us directly." }, 503, "error");

  try { await ensureSchema(env.CONTACT_DB); } catch {}
  const rawIp = request.headers.get("cf-connecting-ip") || "";
  const ip = ipOf(request);
  const ipHash = await sha(ip + "|" + (env.RL_SECRET || "tmw"));

  const qa = isQa(env, request); // owner QA hook: skips the human check, always stored as a test
  const ts = qa ? { ok: true } : await turnstile(env, f["cf-turnstile-response"], rawIp);
  if (!ts.ok) return fail({ ok: false, error: "We could not confirm you are human. Please complete the check and try again.", code: "verify" }, 403, "verify");

  const rl = await limited(env, "contact:" + ip);
  if (rl) return fail({ ok: false, error: "Too many messages in a short time. Please wait a few minutes, or email us directly.", code: "rate" }, 429, "rate");
  try {
    const since = new Date(Date.now() - 3600_000).toISOString();
    const c = await env.CONTACT_DB.prepare("SELECT COUNT(*) AS n FROM submissions WHERE ip_hash = ?1 AND created_at > ?2").bind(ipHash, since).first();
    if (c && c.n >= 5) return fail({ ok: false, error: "Too many messages in a short time. Please wait a few minutes, or email us directly.", code: "rate" }, 429, "rate");
  } catch {}

  const id = crypto.randomUUID();
  const created_at = new Date().toISOString();
  const host = new URL(request.url).hostname;
  const isTest = qa || /^\[TEST\]/.test(v.message) || (!PROD.has(host) && /^TEST\b/.test(v.name)) ? 1 : 0;
  let attr = null; try { attr = cleanAttr(typeof f.attribution === "string" ? JSON.parse(f.attribution) : f.attribution); } catch {}
  try {
    await env.CONTACT_DB.prepare("INSERT INTO submissions (id, created_at, host, name, email, company, topic, message, ip_hash, user_agent, is_test, attribution) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12)")
      .bind(id, created_at, host, v.name, v.email, v.company || null, v.topic, v.message, ipHash, (request.headers.get("user-agent") || "").slice(0, 300), isTest, attr ? JSON.stringify(attr) : null).run();
  } catch { return fail({ ok: false, error: "We could not save your message. Please try again, or email us directly." }, 500, "error"); }

  const md = dims(attr, request.headers.get("referer") || "/contact");
  if (countable(isTest, md)) ctx.waitUntil(count(env, v.topic === "Briefing invitation" ? "form_briefing" : "form_contact", md));
  ctx.waitUntil((async () => {
    const res = await notify(env, { kind: v.topic === "Briefing invitation" ? "Briefing request" : "Contact request", store: "D1 themarginwars" + (envTag(env) ? "-dev" : "") + "-contact", id, created_at, host, test: !!isTest, ...v }, { form: v.topic === "Briefing invitation" ? "briefing" : "contact", page: md.page, attribution: attr });
    const ok = delivered(res) ? 1 : 0;
    try { await env.CONTACT_DB.prepare("UPDATE submissions SET notified = ?1, notify_error = ?2 WHERE id = ?3").bind(ok, res.length ? res.join(" ") : "no-notifier", id).run(); } catch {}
  })());
  return wantsJson ? json({ ok: true, id }) : back("sent");
}

const no = () => json({ ok: false, error: "Method not allowed" }, 405);
export const onRequestGet = no, onRequestPut = no, onRequestDelete = no, onRequestPatch = no;
