# ADR-0002: Reuse the group's repository standards

- Status: accepted

## Decision

Adopt the conventions already used in the owner's other repositories: CODEOWNERS with a single required owner,
PR and issue templates per workstream, a `standards.lock.json` that pins the governance files by hash
(`qa/check_standards_lock.py`), a claims check against a facts file, Conventional Commits, and squash merges with
linear history.

## Consequences

Changes to the gates or governance files show up as a lock diff and need the same review as content.
Run `python3 qa/check_standards_lock.py --write` in the same PR that changes a locked file.
