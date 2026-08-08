# Life Workspace Protocol

Version: 0.2
Status: Active

## Purpose

Life Workspace is a persistent AI-assisted knowledge environment.

Its goal is not to preserve conversations. Its goal is to maintain an accurate, searchable, source-grounded, and continuously evolving model of the user's knowledge, projects, decisions, sources, health records, and ideas.

Markdown is the durable store. Chat history and model memory are temporary.

## Core Principles

### Knowledge over conversations

Do not preserve complete conversations by default. Extract only durable value: ideas, decisions, reusable knowledge, changed assumptions, project constraints, open questions, source-derived principles, and factual records.

### Raw evidence and derived models are different

Append-only raw evidence preserves input and provenance. The editable derived wiki preserves the current best model.

Raw evidence includes capture payloads, source artifacts and locator manifests, dated raw health evidence, and existing operational log entries. Never rewrite raw payloads. Correct them with append-only addenda, superseding records, or derived interpretation.

Derived contexts, Knowledge pages, source records, and summaries may be edited after approval. Early ideas use provisional Knowledge status rather than a separate entity type. A derived page must retain links to the evidence that supports it.

### Update canonical models, not diaries

When understanding changes, update the existing canonical page. Create a new page only when the entity or concept stands independently, has its own lifecycle, or deserves links from multiple contexts.

Use decision records for consequential choices, source records for source-specific analysis, project maps for large-project navigation, and `Brain/LOG.md` only for operational search.

### Preserve raw thoughts

A raw thought must be capturable with almost no friction. Preserve the original wording exactly and make it searchable immediately. Metadata may be enriched later, but the `Raw Capture` and `Additional Raw Capture` payloads are immutable after writing.

### Progressive context loading

Do not read the entire Brain at session start.

Use:

1. `CONTEXT-MAP.md` as the small domain router;
2. `Brain/INDEX.md` as the complete catalog of navigable corpus pages, including sessions and raw-source manifests;
3. root and local context;
4. only the relevant canonical and evidence pages.

Read raw evidence only when a claim must be verified, provenance is disputed, or a summary is insufficient.

### Human control with safe maintenance

Capture may write immediately because preservation was explicitly requested. A requested ingest may also preserve an immutable raw artifact or locator manifest.

An explicit Explore request narrowly authorizes creation and updates of that Explore's temporary structured session note. The note is non-authoritative working memory. This exception does not authorize promotion into canonical knowledge, decisions, context, project semantics, health interpretation, or any other durable semantic state.

An explicit Project Map request authorizes creation and updates of project-map and map-ticket working artifacts for the named effort. These artifacts are navigation and planning layers. They may organize frontier questions, fog, blocked items, and out-of-scope boundaries, but they do not promote project semantics into canonical specs, decisions, or context without Sync approval.

An explicit Teach request authorizes only the named `Learning/<Topic>/` working area for that teaching engagement. Curriculum and progress notes in that area are non-canonical. Changes to durable Knowledge, preferences, personal context, or project state still require Sync approval.

Semantic writes require a preview and approval. This includes changes to claims, interpretations, decisions, preferences, context, project meaning, or health interpretation, and all merge, archive, delete, replacement, and supersession operations.

Safe service maintenance may run without separate material approval when it does not change meaning: complete index entries, constrained non-sensitive operational log entries, real links, reciprocal backlinks between editable derived pages, non-semantic metadata, and lint reports.

## Claim-specific Authority

There is no universal authority ladder for all knowledge. Resolve each claim according to its type.

| Claim type | Primary authority test | Conflict behavior |
| --- | --- | --- |
| User preference | Latest explicit and attributable user statement in the relevant scope | Record the current preference without erasing dated historical preferences |
| Decision | Latest approved decision for the relevant person or project, including explicit supersession | Distinguish proposals from decisions and preserve rationale/history |
| External fact | Source quality, directness, method, publication date, retrieval date, and corroboration | Keep competing claims and cite their evidence; canonical text is not automatically stronger |
| Health record | Exact dated lab, clinician, document, or user-reported evidence with provenance | Preserve all records, units, ranges, and attribution; do not silently reconcile or diagnose |
| Interpretation | Explicitly attributed user interpretation or approved synthesis | Keep source claims separate; label agent inference and never promote it to fact by wording |

Indexes, backlinks, operational logs, current chat, and model memory are discovery aids, not substantive authority.

## Workspace Schema

### Navigation

* `CONTEXT-MAP.md` is a small, stable router to major contexts and domains.
* `Brain/INDEX.md` is the complete catalog of navigable corpus pages, including contexts, canonical pages, captures, sessions, derived source records, and raw-source manifests.
* `Brain/LOG.md` is an append-only operational log for search and maintenance history, not a knowledge model.

Operational log entries may contain only the date, operation type, a short non-sensitive title, affected workspace-relative paths, and at most one bounded non-sensitive note. They must not contain raw thoughts, health details, source excerpts, credentials, secrets, external absolute paths, or other sensitive content. A log-schema change is recorded by appending a migration marker; entries before that marker remain immutable legacy records governed by the schema active when they were written.

### Links and backlinks

Prefer standard Markdown links with real relative paths. Do not use unresolvable pseudo-links as the primary relationship mechanism. Add reciprocal backlinks only between editable derived pages when they improve navigation or provenance. A derived source record links one-way to its immutable raw manifest; never require or add a backlink to the manifest after creation.

A link is maintenance only when it records an already-established relationship. If adding the link asserts a new semantic relationship, include it in the approval proposal.

### Raw captures

Ordinary captures live under `Brain/Inbox/`. Explicit health captures live under `Brain/Health/Inbox/`.

The original payload is immutable. Metadata, processing status, and links to derived pages may be added. A near-duplicate may be appended as a separately dated `Additional Raw Capture`; neither payload may later be rewritten.

No Git checkpoint is required or implied after Capture.

### External sources

Use two layers:

* `Brain/Sources/Raw/<domain>/...` for immutable artifacts and locator manifests;
* `Brain/Sources/Records/<domain>/...` for editable, derived source records.

A locator manifest records the original locator, retrieval time, access method, artifact identity or checksum when available, and access limitations. It does not pretend inaccessible content was read. Raw artifacts and manifests are immutable; new retrievals create new versions or dated addenda. The derived source record references the manifest one-way, and the manifest is never edited later to add a backlink.

A source record separates source claims, evidence, quotations, author opinion, user interpretation, and agent inference. Every derived claim in the source record requires proposal and approval before it is written. Create or update canonical Knowledge pages only when reusable standalone knowledge or an approved project change warrants them; otherwise record `Canonical pages: none needed` in the ingestion result.

A completed ingestion must account for:

1. an immutable raw locator manifest and artifact when accessible and permitted;
2. an approved derived source record;
3. approved canonical pages when reusable standalone knowledge or a project change warrants them, otherwise an explicit `Canonical pages: none needed` result;
4. a one-way link from the derived source record to the raw manifest, plus real Markdown links and reciprocal backlinks only among editable derived pages;
5. `Brain/INDEX.md` maintenance for all navigable corpus pages created by the ingest;
6. a policy-conforming non-sensitive `Brain/LOG.md` entry;
7. explicit contradictions and open questions, including an explicit “none found” result when appropriate.

Project-semantic changes discovered during ingestion are proposed and applied through Sync.

## Core Behaviors

### Capture

Preserve a raw thought immediately without changing its wording. Enrich metadata only around the immutable payload. Do not checkpoint after every capture.

### Project Map

Use Project Map as the main user-facing workflow for large multi-session projects. First clarify the destination, then maintain a Markdown map of decisions so far, current frontier, blocked questions, fog, and out-of-scope boundaries. Route each frontier item internally to focused exploration, grilling, research, prototype, task, or Sync as needed. The map is a navigation layer and does not replace canonical project context, specs, decision records, or implementation plans.

### Explore

Use focused structured questioning to develop an idea, plan, design, or belief. The explicit Explore request authorizes its temporary non-authoritative session note and updates, but not durable semantic promotion. Keep facts, preferences, assumptions, interpretations, and decisions distinct. Durable conclusions go through Sync. For large projects, Explore is normally an internal mode within Project Map rather than a separate user-facing choice.

### Query

Load `CONTEXT-MAP.md`, then `Brain/INDEX.md`, then relevant canonical pages, and raw evidence only when needed. Cite durable pages and clearly separate durable state, source claims, user interpretation, and agent inference. Propose Sync for a novel durable synthesis.

### Sync

Preview semantic changes, obtain approval, and apply only the approved scope. After approved writes, maintain real links, reciprocal backlinks between editable derived pages, the complete corpus index, and the policy-conforming operational log without requesting another material approval. A high-impact Sync may propose a Git checkpoint; it never creates one implicitly.

### Review

Remain Inbox-oriented by default. Run `python Tools/brain.py status`, then verify candidates through a targeted scan of Inbox metadata and `Brain/INDEX.md`; never rely on index status alone. Surface manageable batches and route semantic actions through Sync. A broad quality audit belongs to Lint unless the user explicitly expands Review scope.

### Ingest

Preserve source provenance in the raw layer, obtain approval for all derived source-record claims, and connect approved reusable standalone knowledge to canonical pages only when warranted; otherwise report `Canonical pages: none needed`. Complete the ingestion definition of done before reporting success.

### Lint

Run `python Tools/brain.py lint` first, then perform read-only semantic checks. Report findings without changing files. Route fixes through Sync.

### Checkpoint

Use Git as rollback and audit history; use `Brain/LOG.md` for operational search. Default to proposing a checkpoint. Never make hidden commits, never checkpoint every Capture or Query, and never amend or reset history. Commit only after a current user request or explicit approval and only after inspecting status and diffs. If any already-staged path is outside the current approved checkpoint scope, stop, report it, and neither unstage nor commit anything.

## Save-Suggestion Policy

### Low impact

Casual conversation, repeated information, and temporary troubleshooting with no durable result: do not mention saving.

### Medium impact

A reusable insight, immature idea, useful preference, or open question: mention Capture once at a natural boundary.

### High impact

A project decision, changed design, corrected belief, reusable framework, approved Explore conclusion, important health record, or source-derived knowledge: present a concise Sync proposal at a natural boundary.

Do not ask after every response.

## Health Data Policy

Preserve exact dates, values, units, reference ranges, medication names, dosages, and stated medical advice. Distinguish user reports, laboratory data, clinician statements, source claims, user interpretation, and agent inference.

Do not silently diagnose, alter dosages, merge conflicting records, or include sensitive health content in `Brain/LOG.md`. Health interpretation and health-context changes require explicit approval.

## Language Policy

* Product files, protocols, skills, workflows, templates, generated headings, and examples: English
* Default conversation language: English
* Other conversation languages: only when the user requests one or the active profile configures one
* Raw user material: preserve the language received
* Derived pages: English by default; use another language only for an explicit workspace need
* Search: original terms and useful English equivalents

## Project Integration

Application source code need not live inside the Brain. A project workspace may connect external source folders, project context under `Projects/`, and relevant Brain knowledge.

Avoid broad scans of generated files, binaries, caches, and unrelated projects. Source-ingested project recommendations do not change project semantics until approved through Sync.

## Definition of Success

The system succeeds when the user can preserve raw evidence without loss, find it later, distinguish evidence from interpretation, develop ideas through discussion, maintain current canonical models, query them with citations, process the Inbox, ingest sources with provenance, detect schema drift, and create deliberate audit checkpoints without hidden automation.
