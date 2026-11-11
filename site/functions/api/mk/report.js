// GET /api/mk/report  — auth-protected JSON report for routines. Never public.
// Auth: header "authorization: Bearer <MK_REPORT_TOKEN>". Params: from, to (YYYY-MM-DD, UTC; default last 30 days), include_qa=1.
import { ensureMk, FORM_EVENTS } from "../_mk.js";
const J = (o, s = 200) => new Response(JSON.stringify(o, null, 1), { status: s, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" } });
async function same(a, b) { const e = new TextEncoder(); const [x, y] = await Promise.all([crypto.subtle.digest("SHA-256", e.encode(a)), crypto.subtle.digest("SHA-256", e.encode(b))]); const u = new Uint8Array(x), v = new Uint8Array(y); let d = 0; for (let i = 0; i < u.length; i++) d |= u[i] ^ v[i]; return d === 0; }
const DAY = /^\d{4}-\d{2}-\d{2}$/;
function roll(rows, keyf) {
  const m = new Map();
  for (const r of rows) {
    const k = keyf(r); let o = m.get(k.id); if (!o) { o = { ...k.cols, visits: 0, conversions: 0, by_form: {}, cta: {} }; m.set(k.id, o); }
    if (r.event === "visit") o.visits += r.n; else if (FORM_EVENTS.has(r.event)) { o.conversions += r.n; o.by_form[r.event] = (o.by_form[r.event] || 0) + r.n; } else o.cta[r.event] = (o.cta[r.event] || 0) + r.n;
  }
  return [...m.values()].map(o => ({ ...o, conversion_rate: o.visits ? +(o.conversions / o.visits).toFixed(4) : null }));
}
export async function onRequestGet({ request, env }) {
  const h = request.headers.get("authorization") || "";
  if (!env.MK_REPORT_TOKEN || !h.startsWith("Bearer ") || !(await same(h.slice(7), env.MK_REPORT_TOKEN))) return J({ ok: false, error: "unauthorized" }, 401);
  if (!env.CONTACT_DB) return J({ ok: false, error: "no database" }, 503);
  const u = new URL(request.url), today = new Date().toISOString().slice(0, 10);
  const to = DAY.test(u.searchParams.get("to") || "") ? u.searchParams.get("to") : today;
  const from = DAY.test(u.searchParams.get("from") || "") ? u.searchParams.get("from") : new Date(Date.now() - 29 * 864e5).toISOString().slice(0, 10);
  const qa = u.searchParams.get("include_qa") === "1";
  await ensureMk(env.CONTACT_DB);
  const { results } = await env.CONTACT_DB.prepare("SELECT day, page, campaign, source, medium, event, n FROM mk_daily WHERE day BETWEEN ?1 AND ?2" + (qa ? "" : " AND campaign NOT LIKE 'qa-%'") + " ORDER BY day").bind(from, to).all();
  const rows = results || [];
  const by_day_campaign = roll(rows, r => ({ id: r.day + "|" + r.campaign, cols: { day: r.day, campaign: r.campaign } }));
  return J({
    ok: true, env: String(env.SITE_ENV || "production"), generated_at: new Date().toISOString(), from, to, timezone: "UTC", include_qa: qa,
    definitions: { visits: "first page view per browser session (sessionStorage), last-touch attributed", conversions: "stored form submissions: " + [...FORM_EVENTS].join(", "), conversion_rate: "conversions / visits" },
    by_day_campaign,
    by_campaign: roll(rows, r => ({ id: r.campaign, cols: { campaign: r.campaign } })),
    by_page: roll(rows, r => ({ id: r.page, cols: { page: r.page } })),
    by_source: roll(rows, r => ({ id: r.source + "|" + r.medium, cols: { source: r.source, medium: r.medium } })),
    totals: roll(rows, () => ({ id: "all", cols: {} }))[0] || { visits: 0, conversions: 0, by_form: {}, cta: {}, conversion_rate: null }
  });
}
const no = () => J({ ok: false, error: "Method not allowed" }, 405);
export const onRequestPost = no, onRequestPut = no, onRequestDelete = no, onRequestPatch = no;
