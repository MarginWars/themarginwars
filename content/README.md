# content/

One file per outbound item, with front-matter per `schemas/content-item.schema.json`:
`channel`, `schedule` (Pacific Time with an explicit offset), `status`, `owner`, `sources` (fact ids or URLs) and
`approvals` (only for gated names; see `ops/approvals.md`). Templates are in `_templates/`.

- `linkedin/personal`, `linkedin/company`, `x`, `substack`: posts, threads, issues and profile copy.
- `calendar/YYYY-Www.yml`: the weekly calendar, the approval unit for scheduled posts.

Status on `main` never goes past `approved` (or `live` for standing profile copy); publish results live on the
`ledger` branch.
