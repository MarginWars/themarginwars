# Publish

The detailed contract is `ops/publish/scheduler-spec.md`; routes per channel are in `ops/publish/channels.md`.

1. Content Studio, Publications or Speaking opens a PR with the item under `content/`, `publications/` or
   `speaking/` (front-matter: channel, schedule in PT, status, sources, approvals).
2. Checks: compliance (names, personal data, secrets), frontmatter-limits (schema + character limits), claims
   (every number cites `facts/`), links.
3. Avi reviews and merges (CODEOWNERS). The merge is the approval; status on `main` stays `approved`.
4. Channels publishes at the scheduled time via the route for that channel, then writes the ledger entry and live URL.
5. Failures go to a `channel-incident` issue; nothing is retried on a different account or route.
