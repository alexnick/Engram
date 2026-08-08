# User Guide

Life Workspace is a Markdown knowledge base maintained with an AI agent. It stores evidence, current understanding, decisions, and project state without treating chat history as permanent memory.

## The three layers

### Raw evidence

Raw evidence preserves what arrived:

- exact user wording;
- source files and retrieval manifests;
- dated observations and records.

Raw payloads are append-only. A correction becomes an addendum or a derived page; it does not replace the original.

### Derived knowledge

Derived pages hold the current model:

- knowledge;
- decisions;
- context;
- entities and events;
- source records;
- project documents.

These pages may change when understanding changes. Important claims should point back to their evidence.

### Operations

Operations define how an agent reads or changes the workspace. Raw preservation can happen on request. Changes to durable meaning require a proposal and approval.

## Choose an operation

| If you want to... | Use |
|---|---|
| Preserve exact wording | Capture |
| Work through a large project | Project Map |
| Develop an unclear idea | Explore |
| Pressure-test a plan | Grilling |
| Add an external source | Ingest |
| Ask from existing knowledge | Query |
| Update durable knowledge | Sync |
| Process the Inbox | Review |
| Audit the workspace | Lint |
| Create a Git restore point | Checkpoint |

Plain English is enough. Slash commands are optional and depend on the harness.

## Capture

Use Capture when losing the original wording would matter.

```text
Save this exactly: not every efficiency improvement makes a game better.
```

Capture writes the raw payload immediately because the request itself grants permission to preserve it. It may add light metadata and a search hint. It must not rewrite, translate, or promote the statement into accepted knowledge.

Ordinary captures go to `Brain/Inbox/`. Explicit health captures go to `Brain/Health/Inbox/`.

## Project Map

Use Project Map for work that spans many decisions or sessions.

```text
Create a project map for the combat redesign. The destination is an approved design spec and an implementation plan.
```

A map tracks:

- the destination;
- inputs and constraints;
- decisions already made;
- the current unblocked frontier;
- blocked questions;
- areas that are still too vague;
- work intentionally left out.

The map is a navigation layer. It does not replace approved project context, decisions, specs, or implementation plans. Changes to those canonical documents go through Sync.

## Explore

Use Explore when the question is still fuzzy.

```text
Help me understand when optimization reduces meaningful player choice. Ask one question at a time.
```

Explore loads only relevant context and may maintain a temporary note in `Brain/Sessions/`. The note records the working model, not a transcript. Conclusions remain provisional until Sync.

## Grilling

Use Grilling when a plan is ready for a hard review.

```text
Grill me on this architecture until every unresolved dependency is visible.
```

The agent works through a dependency tree in rounds, recommends answers, and asks the user to make the actual decisions. Grilling is conversation-only. Nothing enters the Brain until the user confirms shared understanding and approves a Sync proposal.

## Ingest

Use Ingest for articles, papers, books, PDFs, videos, transcripts, or other external sources.

```text
Ingest this article. Preserve the source, then separate the author's claims from evidence, limitations, and my interpretation: https://example.com/article
```

A requested ingest may preserve a raw artifact or an immutable locator manifest immediately. If the source is unavailable, the agent must say so rather than inventing its contents.

The derived source record requires a proposal and approval. It should separate:

- direct source claims;
- supporting evidence or quotations;
- author opinion;
- user interpretation;
- agent inference;
- limitations and unresolved contradictions.

Ingest does not have to create a Knowledge page. It should do so only when the source supports a reusable, standalone model.

## Query

Query reads the Brain without changing it.

```text
What has the Brain decided about Git checkpoints? Cite the decision and current context.
```

The agent starts with `CONTEXT-MAP.md`, uses `Brain/INDEX.md` to locate relevant pages, and reads raw evidence only when exact wording or provenance matters.

A good answer distinguishes:

- approved durable state;
- external source claims;
- user interpretation;
- new agent inference.

The Index and Log help discovery, but they are not evidence for a substantive claim.

## Sync

Sync is the boundary between discussion and durable meaning.

```text
Propose the Brain changes from this conversation. Show the files and claims first.
```

The agent should:

1. find existing canonical pages before creating new ones;
2. show a compact proposal with exact files and intended changes;
3. wait for approval;
4. apply only the approved items;
5. repair links and refresh the Index;
6. append a short, non-sensitive operation entry to `Brain/LOG.md`.

Agreement with an idea is not approval to write. Approval applies to the current proposal.

## Review

Review processes unhandled captures in small batches.

```text
Show up to ten unprocessed captures and recommend one action for each. Do not change anything yet.
```

The report is read-only. Promotion, merging, archiving, deletion, or project updates require approval and follow the Sync rules. Raw payloads remain unchanged.

## Lint

Lint checks the workspace without repairing it.

```text
Audit the Brain for broken links, stale claims, missing provenance, and raw/derived mixing.
```

Run the deterministic check first:

```bash
python Tools/brain.py lint
```

Semantic findings should be reported separately. Fixes that change meaning go through Sync.

## Checkpoint

Checkpoint creates a deliberate Git restore point after meaningful approved work.

```text
Propose a checkpoint for the approved architecture update. Exclude unrelated files and do not commit until I confirm.
```

The default is proposal-only. Before a commit, the agent must inspect every staged path and stop if any staged work falls outside the approved scope. It must not reset, clean, amend, or hide unrelated work.

Use `Brain/LOG.md` to find an operation and Git to inspect the actual file history.

## Project files

A project usually contains:

- `CONTEXT.md` for current approved state;
- `DECISIONS.md` for consequential choices and rationale;
- `PROJECT-MAP.md` for navigation across unresolved work;
- optional specs, research, and implementation plans.

Keep large source-code repositories outside the Brain. Connect them through the agent harness or IDE instead.

## Language

The product, system files, generated examples, and default agent responses are English. Raw user material stays in the language received. An agent may use another conversation language when the user explicitly asks for it, but it should not silently translate stored evidence.

## Common mistakes

- Saving a whole transcript instead of the durable conclusion.
- Treating a Capture as proof that a claim is true.
- Expecting Explore or Grilling to write durable state.
- Creating a new page when an existing canonical page should be updated.
- Editing raw payloads or source manifests after creation.
- Mixing source claims, user interpretation, and agent inference.
- Editing `Brain/INDEX.md` by hand.
- Expecting Lint to repair semantic problems automatically.
- Committing every small capture instead of checkpointing at useful boundaries.

For storage rules and edge cases, read the [Life Workspace Protocol](Protocols/Life-Workspace-Protocol.md).
