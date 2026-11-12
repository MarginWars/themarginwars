// themarginwars-soldier-rl: per-IP limiter (review only). 10/min sliding, 100/day.
export class Limiter {
  constructor(state) { this.state = state; }
  async fetch() {
    const now = Date.now(), day = new Date(now).toISOString().slice(0, 10);
    let s = (await this.state.storage.get("s")) || { m: [], d: day, n: 0 };
    if (s.d !== day) { s.d = day; s.n = 0; }
    s.m = s.m.filter(t => now - t < 60_000);
    let r = "ok";
    if (s.n >= 100) r = "day"; else if (s.m.length >= 10) r = "minute";
    else { s.m.push(now); s.n++; }
    await this.state.storage.put("s", s);
    return Response.json({ r, minute: s.m.length, day: s.n });
  }
}
export default {
  async fetch(req, env) {
    const k = req.headers.get("x-rl-key") || "", t = env.RL_SECRET || "";
    let d = k.length === t.length && t ? 0 : 1; for (let i = 0; i < t.length && !d; i++) d |= k.charCodeAt(i) ^ t.charCodeAt(i);
    const ip = new URL(req.url).searchParams.get("ip");
    if (d || req.method !== "POST" || !ip) return new Response("no", { status: 404 });
    return env.LIMITER.get(env.LIMITER.idFromName(ip)).fetch("https://rl/");
  }
};
