// Shared Cloudflare Turnstile server-side check (contact form and assistant escalation).
export async function turnstile(env, token, ip) {
  if (!env.TURNSTILE_SECRET) return { ok: false, reason: "not-configured" };
  if (!token) return { ok: false, reason: "missing" };
  const body = new FormData(); body.append("secret", env.TURNSTILE_SECRET); body.append("response", token); if (ip) body.append("remoteip", ip);
  try { const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body }); const d = await r.json(); return { ok: !!d.success, reason: (d["error-codes"] || []).join(",") }; }
  catch { return { ok: false, reason: "unreachable" }; }
}
