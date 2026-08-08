# Product Update Workflow

This workflow keeps Life Workspace product/core changes synchronized between the clean product repository, private development Brains, and other user Brain repositories without copying private content.

## Repositories

- **Brain-Product** — clean source of truth for product/core files.
- **Personal development Brain** — where product ideas may be prototyped alongside private content.
- **User Brain repositories** — personal instances that consume Brain-Product as upstream.

The default sync direction is Brain-Product → private Brain. A selected change may move from a private Brain → Brain-Product only when the user explicitly asks to promote it and the product version is sanitized and reviewed.

## Product/core allowlist

Only these paths are product/core by default:

```text
.agents/AGENTS.md
.agents/rules/
.agents/workflows/
.agents/skills/capture/
.agents/skills/checkpoint-brain/
.agents/skills/explore/
.agents/skills/grilling/
.agents/skills/ingest-source/
.agents/skills/lint-brain/
.agents/skills/maintain-life-workspace-product/
.agents/skills/project-map/
.agents/skills/query-brain/
.agents/skills/review-brain/
.agents/skills/sync-brain/
.agents/skills/teach/
.agents/skills/writing-great-skills/
Protocols/
Templates/
Tools/
Dashboards/HOME.md
README.md
USER-GUIDE.md
GETTING-STARTED.md
QUICKSTART-RU.md
HERMES-SETUP.md
CHANGELOG.md
PRODUCT-UPDATE-WORKFLOW.md
AGENTS.md
.gitignore
```

## Protected user-data paths

Never overwrite these from a product update unless the user explicitly asks for a migration and approves the exact plan:

```text
Brain/CONTEXT.md
Brain/INDEX.md
Brain/LOG.md
Brain/.review-state.md
Brain/Inbox/
Brain/Health/
Brain/Knowledge/
Brain/Decisions/
Brain/Entities/
Brain/Events/
Brain/Sessions/
Brain/Sources/
Projects/
Learning/
Feedback/
CONTEXT-MAP.md
```

`CONTEXT-MAP.md` is protected in established user Brains because it becomes personalized routing state. Product changes may ship a starter version, but updating an existing user map requires a migration proposal.

## Recommended Git remote safety

In a private Brain, configure the clean product repository as fetch-only. This permits comparison and upstream inspection while preventing an accidental push of personal history:

```bash
git remote add product https://github.com/<owner>/<product-repo>.git
git remote set-url --push product DISABLED
git fetch product
```

Push product changes only from the clean Brain-Product checkout.

## Standard agent command

When the user says something like:

```text
Обнови Brain product во всех репах
```

the agent should run this sequence:

1. Inspect Git status in every involved repository.
2. Stop if any repo has unrelated dirty changes that would be overwritten.
3. Classify changed paths as product/core, private state, or migration.
4. Implement reusable behavior in Brain-Product first. Promote a private prototype only when the user explicitly approved that scope.
5. Update `README.md`, onboarding docs, and `CHANGELOG.md` when behavior or user-facing setup changes.
6. Copy only allowlisted product/core paths. Compare directories before replacement so repository-specific files are not deleted.
7. Run privacy checks in Brain-Product for known private project names, health payloads, secrets, personal absolute paths, and accidental raw/session content.
8. Run:

   ```bash
   python Tools/brain.py index
   python Tools/brain.py lint
   python Tools/test_brain.py
   ```

9. Show a concise diff summary for Brain-Product and verify that protected paths are absent.
10. Commit/push Brain-Product only after explicit approval.
11. Sync the reviewed allowlist into each private Brain without overwriting protected state.
12. Resolve conflicts only in product/core files unless a user-data migration was explicitly approved.
13. Run status/lint/tests in each updated private repo.
14. Commit/push each repository separately and report its changed paths, validation result, and remote state.

## Product completion checklist

A reusable change is complete only when:

- behavior and approval boundaries are documented;
- README and onboarding still describe the real workflow;
- `CHANGELOG.md` records user-visible changes;
- examples and fixtures contain no private data;
- lint and tests pass;
- the product diff contains no protected path;
- reviewed product/core changes have been propagated to maintained private Brains.

## Local sync helper

`Tools/product_sync.py` provides a conservative local path helper for steps 4 and 9. It is not a replacement for Git review. Always inspect diffs before committing.
