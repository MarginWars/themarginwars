# ADR-0003: Publish routes per channel

- Status: accepted for launch; revisit after 30 days

## Decision

At launch, LinkedIn (personal and company), X and Substack publish by computer-use in the signed-in browser profile
for that account, using each platform's native scheduler where it has one, and only from text merged on `main`.
The site publishes by GitHub Actions and wrangler. API routes (LinkedIn Share, X API, a webhook for ops digests)
come later as separate ADRs. See `ops/publish/channels.md`.

## Consequences

Publishing depends on browser sessions that can hit login checkpoints; the agent asserts the account before
every post and stops on mismatch. Every attempt is written to the ledger.
