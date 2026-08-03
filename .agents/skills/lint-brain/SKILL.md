---
name: lint-brain
description: Audits Life Workspace structure and semantics without modifying files. Use when the user asks to lint, validate, audit, check links or schema, find drift, or invokes /lint; run the deterministic Brain linter first, then report semantic findings and route fixes through Sync.
---

# Lint Brain

## Goal

Produce a reproducible, read-only quality report that separates deterministic failures from semantic review findings.

## Procedure

1. Run exactly:

   `python Tools/brain.py lint`
2. Capture its exit status and output. If the command or script is unavailable, report that failure exactly; do not invent a passing result or mutate files to compensate.
3. After the deterministic pass, perform targeted read-only semantic checks. Broad reading is allowed for the requested lint scope, but avoid unrelated binaries, caches, and external projects.
4. Report findings in the current conversation only. Do not create, edit, move, archive, delete, stage, or commit files.

## Semantic Checks

Check for:

* raw evidence stored outside append-only locations or raw payloads apparently rewritten;
* derived source records mixed with `Brain/Sources/Raw/` artifacts;
* duplicate canonical pages or pages that do not represent standalone entities or concepts;
* claims whose authority is inferred from a global hierarchy rather than claim type, provenance, date, and scope;
* source claims, user interpretation, and agent inference blended together;
* health facts with missing date, unit, range, or attribution, or interpretation presented as diagnosis;
* missing, broken, pseudo, or misleading Markdown links, reciprocal backlinks outside editable derived pages, or backlinks added to immutable raw manifests;
* navigable corpus pages—including captures, sessions, derived source records, and raw-source manifests—missing from `Brain/INDEX.md`;
* catalog detail leaking into the small `CONTEXT-MAP.md` router;
* non-append-only behavior or `Brain/LOG.md` fields outside date, operation, short non-sensitive title, workspace-relative affected paths, and optional bounded non-sensitive note, including raw payloads or external absolute paths;
* unrecorded contradictions, supersession, or open questions;
* semantic changes that appear to lack an approval boundary;
* orphan pages—navigable corpus pages with neither an inbound nor an outbound Markdown link to any other navigable page;
* stale claims—Knowledge, Decision, Context, or Entity pages whose `updated`/`last_verified` metadata (or absence of it) suggests the content has not been revisited in a long time relative to its own stated temporal bounds;
* contradictions noted in prose without the standard `[!contradiction]` Markdown callout marker, which should flag them consistently and make them greppable.

## Report Format

Use:

* Deterministic Lint — command, exit status, and concise output;
* Semantic Findings — severity, file citation, evidence, and why it matters;
* Clean Checks — important checks that passed;
* Proposed Fix Plan — grouped into safe maintenance and approval-required semantic changes.

Use real standard Markdown citations. Mark uncertainty explicitly and do not claim to prove immutability from a current snapshot when history is unavailable.

## Fixes

Lint is always read-only. Offer or invoke `sync-brain` for fixes. Sync may apply genuinely non-semantic maintenance under the maintenance policy, but semantic fixes, merge, archive, delete, context changes, and health interpretation require approval.
