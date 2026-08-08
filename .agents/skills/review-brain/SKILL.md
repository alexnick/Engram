---
name: review-brain
description: Use to review unprocessed captures and propose actions in small batches.
---

# Review Brain

## Goal

Help the user process accumulated captures without turning Review into an automatic whole-Brain rewrite.

## Default Scope

Unless the user requests another scope, inspect:

1. unprocessed ordinary captures;
2. unprocessed health captures;
3. active Explore sessions directly related to those captures;
4. canonical pages linked from those items.

Remain Inbox-oriented. Do not recursively audit all contexts, links, and schema rules; use `lint-brain` for that.

## Procedure

1. Run `python Tools/brain.py status` and capture its exact exit status and output. If unavailable or failing, report the limitation and continue with the targeted checks; do not invent status data.
2. Target-scan `Brain/Inbox/` and `Brain/Health/Inbox/` metadata for review candidates, then cross-check them against `Brain/INDEX.md`. Never rely only on status encoded in the index.
3. Read the relevant candidate items and nearby linked context.
4. Group by topic, project, possible context, or likely action.
5. Identify obvious duplicates, extensions to canonical pages, possible decisions, reusable knowledge, conflicts, forgotten ideas, and material with no durable value.
6. Read `Brain/.review-state.md` and diff the current candidates against its last-surfaced list: mark items seen in a prior run and still unresolved as "still open" instead of presenting them as new, so unresolved items do not get re-flagged fresh on every run.
7. Present no more than ten items per batch.
8. Recommend one action per item or cluster: promote, update canonical, attach to project, record decision, leave unprocessed, archive, or delete.
9. Cite the reviewed files with standard Markdown links and explain each recommendation briefly.
10. Wait for approval before semantic changes, merge, archive, delete, context changes, or health interpretation.
11. Apply approved actions through `sync-brain` semantics. Preserve every Raw Capture payload; processing may change metadata and add links only.
12. After presenting the batch, update `Brain/.review-state.md` with today's date and the current surfaced-item list. This is non-semantic bookkeeping and does not require separate approval.

## Safety

* Never delete automatically.
* Never rewrite or combine raw payloads in a way that loses wording, dates, values, or provenance.
* Never treat age as proof of irrelevance.
* Never interpret health chronology as diagnosis.
* A read-only review report requires no material approval; proposed fixes do.

## Output

Use Review Summary, Suggested Actions, Conflicts, Forgotten Material, and Approval Needed. After approved Sync changes, report resulting files. A completed high-impact review batch may justify proposing a checkpoint, but Review never commits directly.
