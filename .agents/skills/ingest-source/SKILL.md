---
name: ingest-source
description: Use to preserve an external source and derive source-grounded knowledge with provenance.
---

# Ingest Source

## Goal

Preserve verifiable source provenance and produce approved reusable knowledge rather than a disposable summary.

## Storage Contract

Use two layers:

* `Brain/Sources/Raw/<domain>/...` for an immutable locator manifest and, when accessible and permitted, an immutable snapshot or artifact;
* `Brain/Sources/Records/<domain>/YYYY-MM-DD--short-source-title.md` for the editable derived source record.

A raw locator manifest records the original URL or path, retrieval timestamp, retrieval method, artifact filename and checksum when available, and access or licensing limitations. It must not claim inaccessible content was read. Never overwrite a raw artifact or manifest; create a dated version or addendum for a later retrieval. The derived source record references the manifest one-way. Never require or add a backlink to an immutable raw manifest after creation.

## Procedure

1. Determine whether the source is accessible. Never claim to have read content that was not accessed.
2. Establish the user's ingestion goal with at most one concise question when it is not obvious.
3. Choose the domain and inspect `Brain/INDEX.md` for an existing source record and relevant canonical pages.
4. Preserve the locator manifest and available artifact in `Brain/Sources/Raw/<domain>/`.
5. For long sources, inspect structure first and extract only the sections relevant to the goal.
6. Prepare a proposal for a derived source record under `Brain/Sources/Records/<domain>/` with title, author, source type, publication date, ingestion date, a one-way raw-manifest link, relevant sections, why it matters, and project relationships. Do not write derived claims yet.
7. Separate explicitly:

   * direct source claims;
   * evidence and method;
   * author opinion;
   * quotations with exact locations;
   * user interpretation;
   * agent inference.
8. Determine whether reusable standalone knowledge or a project change warrants a canonical page. If not, plan to report `Canonical pages: none needed`. If warranted, locate the existing canonical page before proposing a new standalone concept or entity.
9. Present a compact proposal covering every derived source-record claim, interpretation, and any canonical semantic change. Obtain approval before writing any derived claims.
10. Apply only the approved semantic scope. Add a standard Markdown link from the derived source record to the raw manifest, never the reverse. Add reciprocal backlinks only among editable derived pages.
11. Record contradictions and open questions explicitly. Use `None found` only after checking.
12. Keep `Brain/INDEX.md` complete for all navigable corpus pages created by the ingest. Append a `Brain/LOG.md` entry containing only date, operation, a short non-sensitive title, affected workspace-relative paths, and an optional bounded non-sensitive note. Never include raw payloads, excerpts, or external absolute paths.
13. Route every project-semantic or project-context update through `sync-brain`; source relevance alone is not approval to change a project.

## Extraction Rules

* Preserve quote text and page, chapter, section, paragraph, or timestamp when available.
* Never invent quotation text, bibliographic data, or locations.
* A canonical summary does not outrank its source evidence.
* Keep limitations, counterevidence, and unresolved contradictions visible.
* When approved reusable standalone knowledge exists, do not leave it trapped only in the source record. Do not manufacture a canonical page when none is warranted.

## Definition of Done

Do not report ingestion complete until all items are accounted for:

1. immutable raw locator manifest and artifact when accessible and permitted;
2. approved derived source record, including approval for all derived claims;
3. approved canonical pages when reusable standalone knowledge or a project change warrants them, otherwise explicit `Canonical pages: none needed`;
4. one-way derived-record link to the immutable raw manifest, plus real standard Markdown links and reciprocal backlinks only among editable derived pages;
5. complete `Brain/INDEX.md` entries for navigable corpus pages, including the raw manifest;
6. policy-conforming non-sensitive `Brain/LOG.md` operation entry;
7. explicit contradictions and open questions;
8. project semantic changes proposed through Sync rather than silently applied.

Report inaccessible artifacts or deferred source-record approval as incomplete items. A completed significant ingest may justify proposing `checkpoint-brain`, but never creates a commit implicitly.
