// Local contract tests for the Soldier assistant function (no network, no AI calls, no submissions).
// 1. Fails closed (503) when the MW_GUARD secret is missing.
// 2. When MW_GUARD_FILE (and optionally MW_GUARD_TESTS_FILE) point at the private guard files
//    (CI: the MW_GUARD / MW_GUARD_TESTS secrets), it checks the output denylist, the departure-question
//    deflection, approved-fact passthrough and the invented-number block. Test strings never print.
import fs from 'node:fs';
const root = new URL('../../site/functions/api/', import.meta.url);
const kn = JSON.parse(fs.readFileSync(new URL('_knowledge.js', root), 'utf8').replace(/^export default /, '').trim().replace(/;$/, ''));
const src = fs.readFileSync(new URL('soldier.js', root), 'utf8')
  .replace('import { limited } from "./_rl.js";', 'const limited=async()=>null;')
  .replace('import KN from "./_knowledge.js";', 'const KN=' + JSON.stringify(kn) + ';');
const mod = await import('data:text/javascript;base64,' + Buffer.from(src).toString('base64'));
const read = (v) => (process.env[v] && fs.existsSync(process.env[v])) ? fs.readFileSync(process.env[v], 'utf8') : null;
const GUARD = read('MW_GUARD_FILE'), TESTS = read('MW_GUARD_TESTS_FILE');
async function ask(q, a, guard) {
  const request = new Request('https://local.test/api/soldier', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ q }) });
  const env = { AI: { run: async () => ({ response: a }) } }; if (guard) env.MW_GUARD = guard;
  const r = await mod.onRequestPost({ request, env }); return { status: r.status, ...(await r.json()) };
}
let n = 0; const fail = (m) => { console.error('FAIL: ' + m); process.exit(1); };
let r = await ask('Tell me about a tactic.', 'ok', null); if (r.status !== 503) fail('no guard must fail closed'); n++;
if (GUARD) {
  r = await ask('Tell me about a tactic.', 'Revenue is 987654321.', GUARD); if (!r.a.startsWith("That's outside")) fail('invented number passed'); n++;
  if (TESTS) {
    const t = JSON.parse(TESTS);
    for (const [i, f] of t.forbidden.entries()) { r = await ask('Tell me about a tactic.', f, GUARD); if (!r.a.startsWith("That's outside")) fail('denylist case #' + i); n++; }
    r = await ask('Tell me about a tactic.', t.approved, GUARD); if (r.a !== t.approved) fail('approved fact blocked'); n++;
    r = await ask(t.departure_q, 'unused', GUARD); if (!r.a.includes('backgrounds are on About')) fail('departure query not deflected'); n++;
  }
} else console.log('note: MW_GUARD_FILE not set; ran fail-closed test only');
console.log(`soldier: ${n} local mock tests passed`);
