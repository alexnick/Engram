# Product Update Workflow

Use this workflow when the user asks to update Engram workflows, skills, protocols, templates, tools, or documentation across the personal Engram, product, and user Engram repositories.

## Rule

The product repo is the clean source of truth for product/core. User Engram repositories consume it as upstream. Never use a user Engram as the source for product/core without explicit approval.

## Steps

1. Read `docs/MAINTAINING.md`.
2. Inspect Git status in every repo in scope.
3. Refuse to overwrite protected user-data paths unless the user approved a specific migration.
4. Sync only allowlisted product/core paths.
5. Run privacy grep and validation.
6. Present diff summary and validation results.
7. Update README, onboarding, and `CHANGELOG.md` for user-visible changes.
8. Commit/push only after explicit approval.
9. Propagate the reviewed product allowlist into maintained private Brains and validate each repository separately.
