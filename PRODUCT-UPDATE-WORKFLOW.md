# Product Update Workflow

This workflow keeps Life Workspace product/core changes synchronized between the personal development Brain, the clean product repository, and user Brain repositories without copying private content.

## Repositories

- **Personal development Brain** — where product ideas may be prototyped alongside private content.
- **Brain-Product** — clean source of truth for product/core files.
- **User Brain repositories** — personal instances that consume Brain-Product as upstream.

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

## Standard agent command

When the user says something like:

```text
Обнови Brain product во всех репах
```

the agent should run this sequence:

1. Inspect Git status in every involved repository.
2. Stop if any repo has unrelated dirty changes that would be overwritten.
3. Identify intended product/core changes in the personal development Brain.
4. Copy only allowlisted product/core paths into Brain-Product.
5. Run privacy grep in Brain-Product for known private project names, health payloads, secrets, absolute local paths, and accidental raw/session content.
6. Run:

   ```bash
   python Tools/brain.py index
   python Tools/brain.py lint
   python Tools/test_brain.py
   ```

7. Show a concise diff summary for Brain-Product.
8. Commit/push Brain-Product only after explicit approval.
9. In each user Brain repo, merge or pull Brain-Product through its configured upstream remote.
10. Resolve conflicts only in product/core files unless a user-data migration was explicitly approved.
11. Run status/lint/tests in each updated user repo.
12. Report changed paths, validation results, and any conflicts or manual follow-ups.

## Local sync helper

`Tools/product_sync.py` provides a conservative local path helper for steps 4 and 9. It is not a replacement for Git review. Always inspect diffs before committing.
