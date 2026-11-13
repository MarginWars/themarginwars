# Security and data policy

This repository is **public**. Treat every byte as published.

## Never commit

- Secrets of any kind: API tokens, webhook URLs, Turnstile/rate-limit/alert secrets, account passwords, session cookies, private keys.
- Personal data: phone numbers, home addresses, personal or third-party email addresses, lead or CRM records,
  subscriber or invite lists, contact-form submissions, escalation logs, analytics rows tied to a person.
- Private or internal material: private notes, approval chatter about individuals, unpublished personal facts, screenshots of QA runs.

Form-fill packs use `{{profile.*}}` and `{{contact.*}}` placeholders. Agents resolve them at fill time from their
private profile and never write the values back.

## Where secrets live

| Secret | Where | Who manages it |
|---|---|---|
| `CLOUDFLARE_API_TOKEN` (Pages Edit, this account only), `CLOUDFLARE_ACCOUNT_ID` | GitHub environment secrets on `dev` and `production` | Passwords & Vaults |
| `QA_TOKEN`, `MK_REPORT_TOKEN` | GitHub environment secrets (`production` for the report token) | Passwords & Vaults |
| `MW_GUARD`, `MW_GUARD_TESTS`, `COMPLIANCE_EXTRA_TERMS` | GitHub Actions secrets (CI only) and, for `MW_GUARD`, Cloudflare Pages project secrets | Passwords & Vaults |
| `RL_SECRET`, `TURNSTILE_SECRET`, `MW_ALERT_SECRET`, `MW_ALERT_URL`, `ESCALATIONS_TOKEN`, `NOTIFY_EMAILS` | Cloudflare Pages project secrets only, never GitHub | Passwords & Vaults |

Only names appear in this repo, never values. Logins and tokens come from 1Password through Passwords & Vaults;
nobody is ever asked to paste a password into a chat or a PR.

## Gates that enforce this

- `secrets` job: gitleaks over the full history on every push and PR.
- `compliance` job: hashed private-term list, personal-data patterns (phones, addresses, non-allowlisted emails),
  webhook and key patterns, approval-gated names.
- Push protection and secret scanning are turned on in the repository settings.

## Reporting a problem

If something private or secret reaches this repo: do not open a public issue. Message Avi directly, rotate the
secret through Passwords & Vaults first, then remove it from history (`git filter-repo`) and force-push only with
Avi's explicit OK.
