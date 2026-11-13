# Agents

Agents prepare. People sign. Every agent works only through pull requests on this repo, authored as the bot
account; Avi (code owner) approves; the merge is the approval of record. No agent merges, approves, bypasses a
ruleset, or grants itself a permission.

| # | Agent | Status | Approval boundary |
|---|---|---|---|
| 1 | [Margin Wars Launch Command](.agents/launch-command.md) | New | Merges nothing. Raises decisions. Cannot grant permissions. |
| 2 | [Margin Wars Site & Release](.agents/site-release.md) | Re-scoped (was Margin Wars Web & LinkedIn) | Dev deploy: automatic on merge. Production: the GitHub `production` environment, Avi as required reviewer. |
| 3 | [Margin Wars Channels](.agents/channels.md) | New (LinkedIn ops move here from Site & Release) | Publishes only merged items, or items under a standing permission. Profile and page changes need a merged PR. |
| 4 | [Margin Wars Content Studio](.agents/content-studio.md) | New | Drafts only; everything goes through PR. |
| 5 | [Margin Wars Briefing & Publications](.agents/publications.md) | Re-scoped (was Margin Wars Briefing) | Publishes only merged issues. |
| 6 | [Margin Wars Speaking & Media](.agents/speaking.md) | Re-scoped (media/PR merged in) | Files forms after a merge (forms are self-filled). Emails go as draft cards. Any fee or spend needs Avi's explicit OK. |
| 7 | [Margin Wars Pipeline](.agents/pipeline.md) | New | No outreach without a merged batch. Every email is a draft card. No personal data in git. |
| 8 | [Margin Wars Research & Intel](.agents/research.md) | New | Read-only outward. Its facts feed every claims gate. |

Existing agents that coordinate with the suite: Passwords & Vaults (all logins and tokens), SEO & AEO Desk (briefs
for Content Studio), Projects Manager (superseded for Margin Wars by the GitHub Projects board), and the stablecoin
advisory desk (input only, never named outward).

Shared rules: [.agents/_shared-rules.md](.agents/_shared-rules.md). Schedules: [ops/schedules.json](ops/schedules.json).
Standing permissions: [ops/standing-permissions.md](ops/standing-permissions.md).
