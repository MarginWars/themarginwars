const RATE = 10, WINDOW = 60_000; const hits = new Map();
export const ipOf = r => { const raw = r.headers.get("cf-connecting-ip") || "anon"; return raw.includes(":") ? raw.split(":").slice(0, 3).join(":") + "::/48" : raw; };
export async function limited(env, ip) {
  // Strongly consistent per-IP Durable Object (themarginwars-soldier-rl): 10/min, 100/day.
  if (env.RL_SECRET) {
    try {
      const r = await fetch(`https://themarginwars-soldier-rl.avinesh-reddy.workers.dev/?ip=${encodeURIComponent(ip)}`, { method: "POST", headers: { "x-rl-key": env.RL_SECRET } });
      if (r.ok) { const v = (await r.json()).r; return v === "ok" ? false : v; }
    } catch {}
  }
  const now = Date.now(); const h = (hits.get(ip) || []).filter(t => now - t < WINDOW); if (h.length >= RATE) { hits.set(ip, h); return "minute"; }
  h.push(now); hits.set(ip, h); if (hits.size > 5000) hits.clear(); return false;
}
