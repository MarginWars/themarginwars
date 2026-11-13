# What this public repository never contains

- Secrets: API tokens, webhook URLs, passwords, private keys, `.env` files, Cloudflare resource ids. They live in
  Passwords & Vaults, GitHub environment secrets or Cloudflare Pages secrets.
- Personal data: lead, CRM or contact-form records, phone numbers, home addresses, private email addresses.
  `pipeline/` holds a schema and a placeholder example only.
- Internal notes: approvals about people, employment matters, partner or third-party matters not yet public.
- QA screenshots and raw browser artefacts (they stay in CI artefacts with 14-day retention).

The `compliance` check enforces this on every PR (hashed term lists, PII patterns, secret patterns) and `secrets`
runs gitleaks over the full history. GitHub secret scanning and push protection are on.

If something private lands in a PR: close the PR, delete the branch, tell Avi, and rotate any credential. If it
reached `main`, rewriting history needs Avi's explicit approval and a force-push window; rotate first.
