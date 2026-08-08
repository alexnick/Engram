# Maintaining Engram

This guide keeps the clean product repository and private Brain instances in sync without publishing personal content.

## Repository roles

- **The product repo** is the upstream for reusable skills, workflows, protocol, templates, tools, starter files, and public documentation.
- **Private Brains** contain captures, sources, project records, personal context, and other user state.
- A private prototype becomes product work only when its reusable part is selected, cleaned, documented, and reviewed.

The normal direction is product to private Brain. Promotion in the other direction is deliberate.

## Classify every changed path

### Product core

Product core includes agent instructions, skills, workflows, protocol, templates, CLI code, tests, starter files, and public docs.

The executable allowlist lives in `Tools/product_sync.py`. Keep this guide descriptive rather than duplicating the full list.

### Protected private state

Do not overwrite these from a product update without an approved migration:

```text
Engram/CONTEXT.md
Engram/INDEX.md
Engram/LOG.md
Engram/.review-state.md
Engram/Inbox/
Engram/Health/
Engram/Knowledge/
Engram/Decisions/
Engram/Entities/
Engram/Events/
Engram/Sessions/
Engram/Sources/
Projects/
Learning/
Feedback/
CONTEXT-MAP.md
```

`CONTEXT-MAP.md` begins as a starter file but becomes private routing state after setup.

### Migration

A schema change that touches established user state needs a separate proposal. State the files, transformation, rollback plan, and privacy risk before writing.

## Update sequence

When the user asks to ship reusable Brain changes:

1. Inspect status, branch, remotes, and local rules in every repository.
2. Stop before overwriting unrelated dirty work.
3. Classify the changes as product core, private state, or migration.
4. Implement the reusable version in the product repo. If it began in a private Engram, remove private names, paths, sources, and examples.
5. Update README, onboarding, and `CHANGELOG.md` when behavior changes.
6. Run privacy checks for secrets, personal paths, health material, private project names, raw payloads, and session content.
7. Run lint and tests.
8. Review the complete product diff and confirm that protected paths are absent.
9. Commit and push the product only after current approval.
10. Merge-copy the reviewed product allowlist into maintained private Brains.
11. Validate and checkpoint each private Brain separately.

## Local sync helper

Preview:

```bash
python Tools/product_sync.py --source <product-checkout> --target <private-engram> --dry-run
```

Apply:

```bash
python Tools/product_sync.py --source <product-checkout> --target <private-engram>
```

The helper merges allowlisted directories and preserves target-only files. It refuses identical or nested source/target roots. It does not commit, push, delete protected state, or resolve Git conflicts. Always inspect the diff afterward.

### Cleaning up removed product files

The sync helper only copies; it does not delete files that were removed from the product. When a product file is renamed or removed (for example, `QUICKSTART-RU.md` was replaced by `QUICKSTART.md`), existing private Brains keep the old file until you remove it explicitly.

After running the sync helper, check for stale top-level files:

```bash
git status --short
```

Remove obsolete product files from the private Brain manually or through an approved migration. The product changelog records what was removed so maintainers know what to clean up.

## Remote safety

A private Brain may configure the product repository as fetch-only:

```bash
git remote add product https://github.com/<owner>/<product-repo>.git
git remote set-url --push product DISABLED
git fetch product
```

Push product work only from the clean product checkout.

## Completion checklist

A product change is done when:

- behavior and approval boundaries are documented;
- README and onboarding match the real workflow;
- `CHANGELOG.md` records the user-visible change;
- examples contain no private data;
- privacy checks, lint, and tests pass;
- protected paths are absent from the product diff;
- maintained private Brains have received the reviewed product core.
