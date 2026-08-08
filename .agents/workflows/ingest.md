# Ingest Source

Use this workflow when the user invokes `/ingest`.

1. Load and follow `.agents/skills/ingest-source/SKILL.md`.
2. Identify the source from command text, URL, attachment, selected local file, or current document.
3. Verify access and establish the ingestion goal.
4. Preserve an immutable locator manifest and available artifact under `Engram/Sources/Raw/<domain>/`.
5. Prepare the derived-record proposal under `Engram/Sources/Records/<domain>/`; every derived claim requires approval before writing.
6. Determine whether approved reusable standalone knowledge or a project change warrants canonical pages; otherwise record `Canonical pages: none needed`.
7. Present the complete derived semantic proposal and obtain approval.
8. Apply only approved source-record and canonical changes, keeping claim categories distinct.
9. Link one-way from the derived record to the immutable raw manifest; never add a raw-manifest backlink. Add reciprocal backlinks only among editable derived pages.
10. Maintain the complete corpus `Engram/INDEX.md`, append a policy-conforming `Engram/LOG.md` entry, and record contradictions and open questions.
11. Route project-semantic updates through Sync.
12. Report the ingestion Definition of Done and any incomplete items.
13. A completed significant ingest may lead to a checkpoint proposal, never an implicit commit.
