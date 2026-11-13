// Contract tests for site/workers/contact_mailer/worker.js with a stubbed cloudflare:email module.
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
const src = readFileSync(new URL("../../site/workers/contact_mailer/worker.js", import.meta.url), "utf8")
  .replace('import { EmailMessage } from "cloudflare:email";', "class EmailMessage { constructor(f, t, r) { this.from = f; this.to = t; this.raw = r; } }");
const w = (await import("data:text/javascript;base64," + Buffer.from(src).toString("base64"))).default;
const sent = []; const env = (extra = {}) => ({ NOTIFY: { send: async m => { sent.push(m.to); } }, ...extra });
const req = b => new Request("https://mailer.internal/", { method: "POST", body: JSON.stringify(b) });
const base = { name: "Test", email: "visitor@example.com", topic: "advisory", id: "00000000", host: "example.com", message: "hi" };
let n = 0; const t = async (name, fn) => { await fn(); n++; };
await t("no destination and no MAIL_TO fails closed", async () => { const r = await w.fetch(req(base), env()); assert.equal(r.status, 503); });
await t("MAIL_TO is the default destination", async () => { sent.length = 0; const r = await w.fetch(req(base), env({ MAIL_TO: "owner@example.com" })); assert.equal(r.status, 200); assert.deepEqual(sent, ["owner@example.com"]); });
await t("explicit to list wins over MAIL_TO", async () => { sent.length = 0; await w.fetch(req({ ...base, to: ["a@example.com", "b@example.com"] }), env({ MAIL_TO: "owner@example.com" })); assert.deepEqual(sent, ["a@example.com", "b@example.com"]); });
await t("GET is refused", async () => { const r = await w.fetch(new Request("https://mailer.internal/"), env()); assert.equal(r.status, 405); });
console.log(`mailer: ${n} local mock tests passed`);
