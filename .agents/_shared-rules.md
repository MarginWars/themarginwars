# Shared rules (pasted into every Margin Wars agent brief)

Public-safe version. The full rules, including the private denylist and personal details, live only in each
agent's private profile and in 1Password. Never copy them into this repo.

- Avi and Anitha run The Margin Wars (themarginwars.com), Pacific Time. This repo is the single source of truth:
  every outbound item is a file with front-matter (channel, schedule in PT, status, sources, approvals), and you
  change things only by pull request, authored as the bot account.
- **A merge Avi approves (CODEOWNERS) is the approval of record.** Without it, or a standing permission recorded in
  `ops/standing-permissions.md`, you never publish, post, deploy, send or submit.
- Avi's explicit OK (a merge counts) is required for any LinkedIn change, post or deploy.
- Every outgoing email is a draft card; you never send it yourself.
- Approval-gated company names need an `approvals:` entry pointing at an approved row in `ops/approvals.md`.
- Never write anything on the private denylist (the compliance gate blocks it by hash). If the gate fires, remove
  the text; never reword around it, and never print the term in a PR, issue or log.
- Use the approved bio wording only (`speaking/kit/`, `brand/docs/bios.md`); speaker forms use 19 years of
  experience and the verified past stages in `facts/approved.yml`.
- First names only on site material. No metalworking motifs (the `motif:*` rules in `qa/compliance/banned.yml`).
- Never invent facts, stats, quotes or war stories. Every number cites `sources:` or is labelled `[Assumption]`.
- Anitha is co-speaker, in line with The Margin Wars.
- Bots fill and submit forms themselves after the pack merges; ask Avi only for real decisions. Personal form
  values come from `{{profile.*}}` placeholders resolved from your private profile and are never committed.
- Never ask anyone for a password. Logins come from 1Password through Passwords & Vaults (open a `login-needed` issue).
- No personal data in git: no lead records, subscriber lists, submissions, phone numbers or addresses.
- Soft-launch rules hold until Avi's launch go (SP-0).
- One consolidated status list (filed / waiting on Avi / blocked) instead of many pings.
- Times in PT, with explicit offsets.
