---
name: checkpoint-engram
description: Use to propose or create a scoped Git checkpoint after meaningful approved changes.
---

# Checkpoint Brain

## Goal

Use Git for deliberate rollback and audit history while keeping `Engram/LOG.md` as the append-only operational search trail.

## Default Mode: Propose

Default to `propose`. Inspect repository status and relevant diffs read-only, then present:

* why a checkpoint is suitable now;
* intended files;
* excluded unrelated or sensitive files;
* a concise proposed commit message;
* any risks or mixed changes.

Do not stage or commit in propose mode. A current direct user request to commit or explicit approval of the current proposal is required before execution. Never rely on old or implied approval.

## Suitable Boundaries

A checkpoint may be suitable after:

* an approved high-impact Sync;
* a completed source ingestion;
* a schema migration;
* a completed approved Review batch.

Do not checkpoint after every Capture, Query, small maintenance edit, or ordinary conversation. Never create a hidden or automatic commit.

## Execute Mode

After current explicit approval:

1. Inspect `git status --short` and enumerate every already-staged path.
2. Compare all already-staged paths with the current explicitly approved checkpoint scope.
3. If even one already-staged path is outside that scope, stop and report it. Do not unstage anything, stage anything else, or commit.
4. Inspect unstaged and staged diffs for every intended file.
5. Separate user changes and unrelated changes from the checkpoint scope.
6. Include only intended files with explicit path-based staging; never use broad staging when the worktree contains other changes.
7. Inspect the complete staged diff again. Because a normal commit includes all staged state, verify every staged path and hunk belongs to the approved scope and contains no unintended or sensitive content.
8. Commit once with a short imperative message that accurately describes the checkpoint.
9. Report the commit identifier and included paths.

If a file mixes intended and unrelated edits and cannot be safely isolated, stop and ask rather than staging it wholesale. Never attempt to make an unrelated staged path safe by unstaging it; leave the index untouched and stop. Health data, secrets, raw captures, and source artifacts require deliberate inclusion; never infer consent from their presence.

## Prohibitions

* Never amend an existing commit.
* Never reset, discard, checkout over, clean, or otherwise rewrite user work or Git history.
* Never force push or push unless separately requested and approved.
* Never use a commit as a substitute for `Engram/LOG.md`, or put sensitive content in the operational log.
* Never claim a checkpoint exists until the commit command succeeds.
