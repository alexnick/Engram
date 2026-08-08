---
name: maintain-engram-product
description: Use when reusable Brain changes should ship to product.
---

# Maintain Engram Product

## Goal

Keep the clean Engram product and private Brain instances aligned without copying personal content into the product repository.

## Repository roles

- **The product repo** is the source of truth for reusable skills, workflows, protocols, templates, tools, starter files, and public documentation.
- **Private Brains** contain personal and project state. They consume product updates and may prototype reusable improvements.
- A private Engram becomes a product source only when the user explicitly asks to promote selected reusable changes.

Read `docs/MAINTAINING.md` before changing either side.

## Classification

For every changed path, classify it before syncing:

1. **Product/core** — reusable agent behavior, skills, workflow rules, templates, CLI code, tests, onboarding, README, changelog, or public docs.
2. **Private state** — captures, contexts, projects, sessions, health records, source artifacts, personal knowledge, local review state, generated index, or operation log.
3. **Migration** — a product schema change that requires an explicit proposal before touching established private state.

When uncertain, keep the file private and ask or propose a sanitized product version.

## Procedure

1. Inspect Git status, branch, remotes, and local rules in every repository.
2. Stop before overwriting unrelated dirty work.
3. Compare product/core paths; do not blindly copy whole directories when either side contains repository-specific files.
4. Make the reusable implementation in the product repo first, unless the user explicitly approved promotion from a private prototype.
5. Update public documentation and `CHANGELOG.md` for user-visible product changes.
6. Run privacy checks for private names, health content, raw/session payloads, credentials, and absolute local paths.
7. Run deterministic lint and tests.
8. Review the complete diff before staging.
9. Sync allowlisted product/core files into private Brains without overwriting protected state.
10. Commit and push only with current explicit approval; report each repository and validation result separately.

## Product quality bar

A product change is not complete until:

- behavior and approval boundaries are documented;
- README and onboarding remain accurate;
- changelog records the user-visible change;
- examples contain no personal data;
- tests and lint pass;
- private paths remain untouched;
- the Git diff contains only the intended scope.

## Safety

Never publish `Engram/`, `Projects/`, `Learning/`, `Feedback/`, private source artifacts, personal absolute paths, secrets, or project-specific knowledge merely because a nearby skill changed. Domain-specific skills require an explicit product decision and must be self-contained before promotion.