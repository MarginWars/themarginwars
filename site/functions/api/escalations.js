const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store", "x-robots-tag": "noindex" } });
function okTok(h, t) { if (!t || !h || !h.startsWith("Bearer ")) return false; const a = h.slice(7); if (a.length !== t.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ t.charCodeAt(i); return d === 0; }
export async function onRequestGet({ request, env }) {
  if (!okTok(request.headers.get("authorization"), env.ESCALATIONS_TOKEN)) return J({ error: "unauthorized" }, 401);
  if (!env.ESC_KV) return J({ error: "not configured" }, 503);
  const since = new URL(request.url).searchParams.get("since") || "1970-01-01T00:00:00.000Z";
  if (isNaN(Date.parse(since))) return J({ error: "since must be ISO 8601" }, 400);
  const out = []; let cursor;
  do { const l = await env.ESC_KV.list({ prefix: "esc:", cursor }); cursor = l.list_complete ? null : l.cursor;
    for (const k of l.keys) { if (k.name.slice(4, 28) < new Date(since).toISOString()) continue; const v = await env.ESC_KV.get(k.name); if (v) out.push(JSON.parse(v)); } } while (cursor);
  return J({ count: out.length, escalations: out });
}
