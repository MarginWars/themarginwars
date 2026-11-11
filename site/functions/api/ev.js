// POST /api/ev  — cookieless aggregate event counter (visits and CTA clicks). Stores counts only.
import { limited, ipOf } from "./_rl.js";
import { CLIENT_EVENTS, cleanAttr, dims, count } from "./_mk.js";
const BOT = /bot|crawl|spider|slurp|preview|headless|lighthouse|facebookexternalhit|embedly|monitor/i;
const none = (s = 204) => new Response(null, { status: s, headers: { "cache-control": "no-store", "x-robots-tag": "noindex" } });
export async function onRequestPost({ request, env }) {
  let b; try { b = JSON.parse(await request.text()); } catch { return none(400); }
  const ev = String(b && b.e || "");
  if (!CLIENT_EVENTS.has(ev)) return none(400);
  if (BOT.test(request.headers.get("user-agent") || "")) return none();
  if (await limited(env, "ev:" + ipOf(request))) return none(429);
  await count(env, ev, dims(cleanAttr(b.a), b.p));
  return none();
}
const no = () => none(405);
export const onRequestGet = no, onRequestPut = no, onRequestDelete = no, onRequestPatch = no;
