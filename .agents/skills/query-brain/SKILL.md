---
name: query-brain
description: Use to answer from the Brain with progressive loading and claim-level citations.
---

# Query Brain

## Goal

Answer from durable workspace knowledge with minimal context loading and transparent provenance.

## Loading Order

1. Read `CONTEXT-MAP.md` to choose the relevant domain.
2. Read `Brain/INDEX.md` to locate candidate pages.
3. Read the relevant current context, canonical pages, decisions, and derived source records.
4. Read raw captures, source artifacts or manifests, and raw health evidence only when exact wording, disputed provenance, or verification is necessary.

Do not recursively scan the Brain by default. If the map or index is missing or stale, state that limitation and use the narrowest available search.

## Answer Method

1. Identify the claim type before resolving conflicts: user preference, decision, external fact, health record, or interpretation.
2. Apply claim-specific authority, date, provenance, and scope. Do not use a single global hierarchy.
3. Cite material claims with standard Markdown links to the actual workspace pages. Cite the evidence page when a derived summary is insufficient.
4. Clearly separate:

   * **Durable state:** approved current context, preferences, and decisions recorded in the Brain;
   * **Source claims:** what an external source asserts and what evidence it provides;
   * **User interpretation:** the user's attributed view, acceptance, rejection, or application;
   * **Agent inference:** reasoning produced for this answer that is not already durable knowledge.
5. Surface relevant contradictions, dates, uncertainty, and open questions.
6. Keep the response proportional. Omit empty categories, but never blur categories to make the answer smoother.

## Citations

Use resolvable links to actual decision or evidence pages and include a section anchor when useful and reliable. Never cite `Brain/INDEX.md`, `CONTEXT-MAP.md`, or `Brain/LOG.md` as substantive evidence merely because they mention a page.

Do not invent citations or claim access to missing raw material.

## Durable Synthesis

Query is read-only. Do not update files, maintenance metadata, Git state, or logs merely because a question was asked. If the answer produces a novel synthesis likely to remain useful, propose `sync-brain` once at a natural boundary and identify the candidate canonical page. Do not propose a Git checkpoint after Query.
