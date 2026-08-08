---
name: sync-brain
description: Use to propose and apply approved durable changes, then maintain links, index, and log.
---

# Sync Brain

## Goal

Update the durable knowledge model without saving the full conversation or changing raw evidence.

## Inputs

Use the current conversation, named session notes, captures, source records, canonical pages, decisions, and relevant context. Load `CONTEXT-MAP.md`, use `Brain/INDEX.md` to locate candidates, and read raw evidence only when exact wording or provenance matters.

## Phase 1: Detect and Classify Changes

Identify durable changes only: ideas, corrected understanding, decisions, constraints, terminology, reusable knowledge, source relationships, preferences, open questions, factual health records, interpretations, and supersession.

For each claim, classify it as user preference, decision, external fact, health record, user interpretation, or agent inference. Apply the claim-specific authority rules. Ignore filler, repeated background, abandoned suggestions, and unaccepted model speculation.

## Phase 2: Locate Canonical Knowledge

Search relevant existing pages before creating files. Update a canonical page unless the concept or entity can stand alone, has an independent lifecycle, and deserves links from multiple contexts. Do not create duplicates because wording differs.

Raw Capture payloads, raw source artifacts and manifests, dated raw health evidence, and prior `Brain/LOG.md` entries are immutable.

## Phase 3: Propose Semantic Writes

Before semantic writes, show a compact diff-like proposal containing:

* files to create or update;
* claim types and provenance;
* semantic text to add, revise, or mark superseded;
* captures or sessions whose metadata will change;
* links that assert new semantic relationships;
* merge, archive, or delete actions;
* unresolved conflicts and open questions.

Separate semantic changes requiring approval from safe follow-up maintenance. The user may approve all, reject all, or select a subset. Do not treat a general discussion as approval.

## Phase 4: Apply Approved Scope

After approval:

1. Apply only approved semantic writes.
2. Preserve raw payloads and evidence unchanged.
3. Add processing status and links around captures without editing their raw sections.
4. Update `CONTEXT.md` only when current approved state changed.
5. Append consequential approved choices to the relevant decision record.
6. Preserve important supersession history rather than silently erasing it.
7. Keep source claims, user interpretation, and agent inference visibly separate.
8. For health data, preserve exact facts and provenance; never infer diagnosis or alter dosage.
9. Close related session notes when approved, recording status, sync date, and resulting files.

## Phase 5: Service Maintenance

After approved semantic writes, without requesting another material approval:

1. add or repair real standard Markdown links, with reciprocal backlinks only between editable derived pages; never edit an immutable raw source manifest to add a backlink;
2. keep `Brain/INDEX.md` complete for navigable corpus pages, including sessions and raw-source manifests;
3. append a `Brain/LOG.md` entry containing only date, operation, a short non-sensitive title, affected workspace-relative paths, and an optional bounded non-sensitive note; never include raw payloads or external absolute paths;
4. update non-semantic timestamps and metadata.

If a proposed maintenance edit would introduce new meaning, stop and add it to a semantic proposal.

## Completion

Report created and updated files, processed captures or sessions, maintenance performed, unresolved conflicts, and remaining questions.

After an approved high-impact Sync, a schema migration, or a substantial completed batch, you may propose `checkpoint-brain`. Never commit implicitly and do not propose a checkpoint for every small Sync.
