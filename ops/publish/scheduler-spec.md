# Publish scheduler spec (read by the Channels agent)

How agents turn the **merged queue on `main`** into posts. Nothing outside `main` is ever published.

## 1. What is due

Every 15 minutes, 7 AM–7 PM PT (`ops/schedules.json` → `channels/publish-due`):

1. `git fetch origin main ledger` and read `main` at its latest commit.
2. Candidates = files matching `qa/limits.yml` `item_globs` whose front-matter has
   `status: approved`, a `schedule` (PT, explicit offset) `<= now`, and `schedule >= now - 24h`.
3. An item is **authorised** only if one of these holds, checked at publish time:
   - it is listed in a merged `content/calendar/<week>.yml` whose `status: approved` **and** SP-1 is `granted`
     in `ops/standing-permissions.md`; or
   - the item itself was merged in a PR approved by the code owner (the merge commit's PR review is `APPROVED`
     by `@AviShip-Type0`), and the channel's rule allows publishing on merge (see `channels.md`).
   LinkedIn items additionally need that the approving merge is Avi's (always true under CODEOWNERS).
4. Skip anything already in `ledger/published.jsonl` with the same `id` and `status: published` or `scheduled`.
5. Skip anything whose current blob sha differs from the sha approved in the merge (edits need a new PR).

## 2. Publish

For each due, authorised item, in schedule order, using the route in `ops/publish/channels.md`:

1. Assert the account (X: the signed-in handle is `@marginwars`; LinkedIn: the actor is Avi or the company page;
   Substack: the publication is `themarginwars`). If the assertion fails, **stop**, write `failed`, open a
   `channel-incident` issue.
2. Paste the body exactly as merged (no edits, no improvisation). Threads post in order, one part per post.
3. Read back the live URL.

## 3. Write back (ledger branch)

Append one JSON line per item to `ledger/published.jsonl` on branch **`ledger`**, validating against
`schemas/ledger-entry.schema.json`:

```json
{"id":"li-company-2026-11-16-launch","channel":"linkedin-company","status":"published","at":"2026-11-16T08:31:12-08:00","url":"https://www.linkedin.com/feed/update/...","route":"computer-use","sha":"<blob sha>","merge_pr":12,"standing_permission":"SP-1","reason":null}
```

Then set the Projects item's Live URL and Status = Published, and comment the URL on the merge PR.
Failures write `status: failed` with `reason` and open a `channel-incident` issue (label `status:failed`).

## 4. Metrics

Daily 6 PM PT, Channels writes `ledger/metrics/YYYY-MM-DD.jsonl` (site `/api/mk/report` totals per campaign and
post; X metrics via API or connector once @marginwars is connected; LinkedIn and Substack via dashboard reads or CSV
exports). Totals only; no personal data. Launch Command opens a weekly `chore(metrics)` PR to `main` with
`reports/YYYY-WW.md`.

## 5. Never

- Never publish from a branch, a draft, a closed PR or an unmerged change.
- Never post from the wrong account; never send email (draft cards only).
- Never edit `status` past `approved` on `main`; post-approval states live only on the ledger branch.
