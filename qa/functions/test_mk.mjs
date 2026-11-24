// Contract tests for cookieless marketing counters and the auth-protected report, including episode game events.
import assert from "node:assert/strict";
import { CLIENT_EVENTS, FORM_EVENTS, GAME_EVENTS, tok, pathOf, dims, count, countable } from "../../site/functions/api/_mk.js";
import { onRequestGet } from "../../site/functions/api/mk/report.js";

let n = 0;
const t = async (name, fn) => { await fn(); n++; };

await t("game events are accepted client events and not form events", () => {
  for (const ev of ["game_start", "game_complete", "game_rank"]) {
    assert.equal(GAME_EVENTS.has(ev), true, ev);
    assert.equal(CLIENT_EVENTS.has(ev), true, ev);
    assert.equal(FORM_EVENTS.has(ev), false, ev);
  }
});

await t("pathOf strips .html and keeps episode paths", () => {
  assert.equal(pathOf("/ep2.html"), "/ep2");
  assert.equal(pathOf("https://themarginwars.com/ep1"), "/ep1");
});

await t("dims keep last-touch source, campaign and content", () => {
  const d = dims({ last: { source: "linkedin", medium: "social", campaign: "2026-11-lessons", content: "personal-carousel-ep2", landing: "/ep2" } }, "/ep2.html");
  assert.deepEqual(d, { page: "/ep2", campaign: "2026-11-lessons", source: "linkedin", medium: "social", content: "personal-carousel-ep2" });
});

await t("tok sanitises and countable hides non-qa tests", () => {
  assert.equal(tok("Personal Carousel EP2"), "personal-carousel-ep2");
  assert.equal(countable(true, { campaign: "2026-11-lessons" }), false);
  assert.equal(countable(true, { campaign: "qa-game-complete" }), true);
});

function memoryDb() {
  const daily = new Map();
  const content = new Map();
  const key = (args, take) => args.slice(0, take).join("|");
  return {
    daily, content,
    prepare(sql) {
      let binds = [];
      const self = {
        bind(...a) { binds = a; return self; },
        async run() {
          if (/^CREATE TABLE/i.test(sql)) return { success: true };
          if (/INSERT INTO mk_daily /.test(sql)) {
            const k = key(binds, 6);
            const cur = daily.get(k);
            if (cur) cur.n += 1; else daily.set(k, { day: binds[0], page: binds[1], campaign: binds[2], source: binds[3], medium: binds[4], event: binds[5], n: 1 });
            return { success: true };
          }
          if (/INSERT INTO mk_daily_content/.test(sql)) {
            const k = key(binds, 7);
            const cur = content.get(k);
            if (cur) cur.n += 1; else content.set(k, { day: binds[0], page: binds[1], campaign: binds[2], source: binds[3], medium: binds[4], content: binds[5], event: binds[6], n: 1 });
            return { success: true };
          }
          return { success: true };
        },
        async all() {
          const from = binds[0], to = binds[1];
          const inRange = (row) => row.day >= from && row.day <= to;
          if (/FROM mk_daily_content/.test(sql)) return { results: [...content.values()].filter(inRange) };
          if (/FROM mk_daily /.test(sql)) return { results: [...daily.values()].filter(inRange) };
          return { results: [] };
        }
      };
      return self;
    }
  };
}

await t("count stores game_start and game_rank against the episode page and content slug", async () => {
  const db = memoryDb();
  const d = { page: "/ep2", campaign: "2026-11-lessons", source: "linkedin", medium: "social", content: "personal-carousel-ep2" };
  assert.equal(await count({ CONTACT_DB: db }, "game_start", d), true);
  assert.equal(await count({ CONTACT_DB: db }, "game_complete", d), true);
  assert.equal(await count({ CONTACT_DB: db }, "game_rank", d), true);
  assert.equal(await count({ CONTACT_DB: db }, "not_an_event", d), false);
  const events = [...db.daily.values()].map((r) => r.event).sort();
  assert.deepEqual(events, ["game_complete", "game_rank", "game_start"]);
  assert.equal([...db.daily.values()][0].page, "/ep2");
  assert.equal([...db.content.values()][0].content, "personal-carousel-ep2");
});

const TOKEN = "mk-report-test-token";
const reportOf = async (env, url) => {
  const res = await onRequestGet({ request: new Request(url, { headers: { authorization: "Bearer " + TOKEN } }), env });
  return { status: res.status, body: await res.json() };
};

await t("report is unauthorized without a matching token and lists game rates", async () => {
  const db = memoryDb();
  const d = { page: "/ep2", campaign: "2026-11-lessons", source: "linkedin", medium: "social", content: "personal-carousel-ep2" };
  await count({ CONTACT_DB: db }, "game_start", d);
  await count({ CONTACT_DB: db }, "game_start", d);
  await count({ CONTACT_DB: db }, "game_complete", d);
  await count({ CONTACT_DB: db }, "game_rank", d);
  const denied = await onRequestGet({ request: new Request("https://themarginwars.com/api/mk/report"), env: { CONTACT_DB: db, MK_REPORT_TOKEN: TOKEN } });
  assert.equal(denied.status, 401);
  const today = new Date().toISOString().slice(0, 10);
  const { status, body } = await reportOf({ CONTACT_DB: db, MK_REPORT_TOKEN: TOKEN, SITE_ENV: "production" }, `https://themarginwars.com/api/mk/report?from=${today}&to=${today}`);
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.totals.games.game_start, 2);
  assert.equal(body.totals.games.game_complete, 1);
  assert.equal(body.totals.games.game_rank, 1);
  assert.equal(body.totals.game_completion_rate, 0.5);
  assert.equal(body.totals.cta.game_start, undefined);
  const page = body.by_page.find((r) => r.page === "/ep2");
  assert.equal(page.games.game_rank, 1);
  const content = body.by_content.find((r) => r.content === "personal-carousel-ep2");
  assert.equal(content.games.game_start, 2);
});

console.log(`mk: ${n} local mock tests passed`);
