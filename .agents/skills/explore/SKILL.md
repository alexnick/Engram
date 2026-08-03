---
name: explore
description: Runs a structured deep discussion to clarify and stress-test an idea, plan, design, belief, project, or captured thought. Use when the user asks to explore, think through, develop, challenge, pressure-test, design, clarify, deeply discuss something, or invokes /explore.
---

# Explore

## Goal

Improve the quality of the user's thinking rather than rushing to a polished answer.

## Principles

* Seek shared understanding through focused questions.
* Challenge assumptions without becoming performatively adversarial.
* Resolve terminology and surface constraints, alternatives, trade-offs, and contradictions.
* Distinguish source claims, facts, user preferences, decisions, user interpretations, assumptions, and agent inferences.
* Do not implement project or durable semantic changes during questioning.

## Narrow Write Authorization

An explicit user request to Explore authorizes creation and updates of only that Explore's temporary structured session note. The note is non-authoritative working memory and may contain provisional conclusions. This narrow authorization is not approval to promote any content into canonical Ideas, Knowledge, Decisions, project or personal context, health interpretation, or other durable semantic state.

## Startup

1. Read `CONTEXT-MAP.md`, then use `Brain/INDEX.md` to locate relevant material.
2. Read root and local context plus clearly relevant captures, Ideas, Knowledge, decisions, projects, and source records.
3. Read raw evidence only when provenance or exact wording matters. Do not scan the entire Brain.
4. Briefly tell the user what relevant material was found, using real Markdown citations.
5. Under the narrow Explore authorization, create `Brain/Sessions/YYYY-MM-DD-HHmm--topic.md` as a structured temporary session note with `type`, `status`, `created`, `updated`, `topic`, `related_contexts`, and `source_captures` metadata.

The session note is non-authoritative and is not a transcript. Store only the objective, current understanding, assumptions, constraints, questions, provisional conclusions, and unresolved branches.

## Interview Method

1. Ask one main, high-value unresolved question at a time.
2. Adapt each question to the user's answer.
3. Record meaningful branches and decide whether they block progress.
4. Periodically summarize the model to verify shared understanding.
5. Ask for operational definitions and concrete examples when abstraction hides disagreement.
6. Explore alternatives before converging.
7. Update only the authorized temporary session note after major changes or several meaningful exchanges, not after every message.

## Completion

Present:

* Current Understanding
* Decisions or Strong Conclusions
* Remaining Open Questions
* Risks and Counterarguments
* Possible Brain Changes

Classify impact as low, medium, or high. For medium impact, offer Capture once. For high impact, propose Sync at a natural boundary.

Do not write derived Ideas, Knowledge, Decisions, project context, health interpretation, or other semantic state without Sync approval. Do not code unless the user explicitly ends Explore and requests implementation.
