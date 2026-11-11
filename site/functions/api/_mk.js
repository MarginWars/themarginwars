// First-party, cookieless marketing measurement. Aggregates only: no IP, no user agent, no visitor id is stored.
// Table mk_daily in CONTACT_DB: one counter per (day, page, campaign, source, medium, event).
export const CLIENT_EVENTS = new Set(["visit", "cta_contact", "cta_briefing", "out_substack", "out_linkedin"]);
export const FORM_EVENTS = new Set(["form_contact", "form_briefing", "form_escalation"]);
const SCHEMA = "CREATE TABLE IF NOT EXISTS mk_daily (day TEXT NOT NULL, page TEXT NOT NULL, campaign TEXT NOT NULL, source TEXT NOT NULL, medium TEXT NOT NULL, event TEXT NOT NULL, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (day, page, campaign, source, medium, event))";
let ready = false;
export async function ensureMk(db) { if (!ready) { await db.prepare(SCHEMA).run(); ready = true; } }
export const tok = (v, n = 64) => { const s = String(v || "").toLowerCase().trim().replace(/[^a-z0-9._~-]+/g, "-").replace(/^-+|-+$/g, "").slice(0, n); return s || "(none)"; };
export const pathOf = v => { try { let p = new URL(String(v || "/"), "https://themarginwars.com").pathname; p = p.replace(/\.html$/, "").replace(/\/index$/, "/"); return p.slice(0, 120) || "/"; } catch { return "/"; } };
const hostOf = v => { try { return new URL(String(v)).hostname.replace(/^www\./, "").slice(0, 80); } catch { return ""; } };
function touch(t) {
  if (!t || typeof t !== "object") return null;
  const o = {}; for (const k of ["source", "medium", "campaign", "content", "term"]) if (t[k]) o[k] = String(t[k]).slice(0, 100);
  const r = hostOf(t.referrer); if (r) o.referrer = r;   // host only, never the full referring URL
  if (t.landing) o.landing = pathOf(t.landing); if (t.at) o.at = String(t.at).slice(0, 30);
  return o;
}
// Sanitised first/last touch attribution as sent by assets/mk.js (sessionStorage only).
export function cleanAttr(a) { if (!a || typeof a !== "object") return null; const first = touch(a.first), last = touch(a.last); return first || last ? { first, last } : null; }
export function dims(attr, page) {
  const l = (attr && attr.last) || {};
  const source = l.source ? tok(l.source) : l.referrer ? tok(l.referrer) : "direct";
  const medium = l.medium ? tok(l.medium) : l.referrer ? "referral" : "(none)";
  return { page: pathOf(page || (attr && attr.last && attr.last.landing)), campaign: tok(l.campaign), source, medium };
}
export async function count(env, event, d) {
  if (!env.CONTACT_DB || !(CLIENT_EVENTS.has(event) || FORM_EVENTS.has(event))) return false;
  try {
    await ensureMk(env.CONTACT_DB);
    const day = new Date().toISOString().slice(0, 10);
    await env.CONTACT_DB.prepare("INSERT INTO mk_daily (day, page, campaign, source, medium, event, n) VALUES (?1,?2,?3,?4,?5,?6,1) ON CONFLICT (day, page, campaign, source, medium, event) DO UPDATE SET n = n + 1")
      .bind(day, d.page, d.campaign, d.source, d.medium, event).run();
    return true;
  } catch { return false; }
}
// Test submissions only count when tagged with a qa-* campaign, so QA can prove counting without polluting real numbers.
export const countable = (isTest, d) => !isTest || d.campaign.startsWith("qa-");
