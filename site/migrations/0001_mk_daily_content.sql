-- D1 database: themarginwars-contact (and themarginwars-dev-contact). Per-post tracking: utm_content (the post slug).
-- Additive and idempotent. mk_daily is not touched: its rows, primary key and every existing query stay as they are.
-- /api/ev and /api/contact also create this table on first use (functions/api/_mk.js), so applying it by hand is safe in any order.
CREATE TABLE IF NOT EXISTS mk_daily_content (
  day TEXT NOT NULL, page TEXT NOT NULL, campaign TEXT NOT NULL, source TEXT NOT NULL, medium TEXT NOT NULL,
  content TEXT NOT NULL, event TEXT NOT NULL, n INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, page, campaign, source, medium, content, event)
);
-- Read it, for example: SELECT content, event, SUM(n) FROM mk_daily_content WHERE day >= '2026-11-19' GROUP BY content, event;
