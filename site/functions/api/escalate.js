import { limited, ipOf } from "./_rl.js";
const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store", "x-robots-tag": "noindex" } });
const cut = (v, n) => String(v == null ? "" : v).trim().slice(0, n);
const EMAIL = /^[^\s@<>()]{1,64}@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$/;
export async function onRequestPost({ request, env }) {
  const lim = await limited(env, ipOf(request));
  if (lim) return J({ a: lim === "day" ? "Hold fire, ammo spent for today. Try again tomorrow." : "Hold fire, too many shots. Try again in a minute.", limit: lim }, 429);
  let b; try { b = await request.json(); } catch { return J({ a: "Bad request." }, 400); }
  if (cut(b.website, 200)) return J({ ok: true, a: "Message received. Avi or Anitha will reply by email within two business days." }); // honeypot: silently drop
  const name = cut(b.name, 120), email = cut(b.email, 200), company = cut(b.company, 160), question = cut(b.question, 2000);
  if (!name || !question) return J({ a: "Name and question are required." }, 400);
  if (!EMAIL.test(email)) return J({ a: "That email address doesn't look right." }, 400);
  if (!env.ESC_KV) return J({ a: "Comms down. Try again later." }, 503);
  const turns = (Array.isArray(b.history) ? b.history : []).slice(-10).map(t => ({ q: cut(t && t.q, 500), a: cut(t && t.a, 1000) }));
  const ts = new Date().toISOString(), id = crypto.randomUUID();
  const rec = { id, ts, name, email, company, question, history: turns, page: cut(b.page, 300) };
  await env.ESC_KV.put(`esc:${ts}:${id}`, JSON.stringify(rec));
  return J({ ok: true, id, a: "Message received. Avi or Anitha will reply by email within two business days." });
}
