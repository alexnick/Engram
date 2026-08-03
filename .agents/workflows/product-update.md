# Product Update Workflow

Use this workflow when the user asks to update Brain workflows, skills, protocols, templates, tools, or documentation across the personal Brain, Brain-Product, and user Brain repositories.

## Rule

Brain-Product is the clean source of truth for product/core. User Brain repositories consume it as upstream. Never use a user Brain as the source for product/core without explicit approval.

## Steps

1. Read `PRODUCT-UPDATE-WORKFLOW.md`.
2. Inspect Git status in every repo in scope.
3. Refuse to overwrite protected user-data paths unless the user approved a specific migration.
4. Sync only allowlisted product/core paths.
5. Run privacy grep and validation.
6. Present diff summary and validation results.
7. Commit/push only after explicit approval.
