# Life Workspace

**A durable Markdown brain for AI agents.**

Chats disappear. Useful context should not.

Life Workspace is a small set of files, rules, and agent skills for maintaining knowledge across conversations. It preserves what was actually said or received, keeps current understanding editable, records why decisions were made, and gives every agent a predictable way to read and update the workspace.

It is inspired by the LLM Wiki pattern, but treats memory as a controlled knowledge-maintenance problem rather than a transcript archive.

## The model

Life Workspace separates three things that chat systems often blur together:

1. **Raw evidence** — exact captures, source artifacts, locator manifests, and dated records. Raw payloads are append-only.
2. **Derived knowledge** — contexts, knowledge pages, decisions, entities, events, source records, and project documents. These can change as understanding improves.
3. **Operations** — explicit workflows that preserve, develop, query, review, and update the workspace.

The central rule is simple:

> Conversation is temporary. Durable meaning enters the Brain through an explicit operation.

Raw input can be preserved immediately. Semantic changes to knowledge, decisions, or context are proposed first and written only after approval.

## What the skills do

| Skill | Purpose |
|---|---|
| `capture` | Preserve exact wording with almost no friction. |
| `project-map` | Navigate a large multi-session project through decisions, dependencies, fog, and open frontiers. |
| `explore` | Develop a fuzzy idea one question at a time, with a temporary session note. |
| `grilling` | Pressure-test a plan in dependency-ordered rounds without writing persistent state. |
| `ingest-source` | Preserve source provenance and derive source-grounded knowledge. |
| `query-brain` | Answer from durable pages with claim-level citations and explicit epistemic labels. |
| `sync-brain` | Preview and apply approved semantic changes. |
| `review-brain` | Process the Inbox in small, reviewable batches. |
| `lint-brain` | Audit structure and semantic drift without modifying files. |
| `checkpoint-brain` | Propose a scoped Git checkpoint for rollback and audit. |
| `maintain-life-workspace-product` | Keep reusable product changes synchronized without copying private content. |

You do not need to remember the skill names. Describe the outcome in normal language; the agent should route the request.

## Repository layout

```text
Life Workspace/
├── AGENTS.md               # portable agent entry point
├── .agents/
│   ├── AGENTS.md           # full agent contract
│   ├── skills/             # reusable workflows
│   └── workflows/          # slash-command adapters
├── Brain/                  # durable personal knowledge
│   ├── Inbox/              # raw captures
│   ├── Knowledge/          # maintained reusable knowledge
│   ├── Sources/            # immutable raw + editable records
│   ├── Sessions/           # temporary Explore state
│   ├── INDEX.md            # generated catalog
│   └── LOG.md              # append-only operation trail
├── Projects/               # project context, decisions, maps, and specs
├── Protocols/              # storage and approval rules
├── Templates/              # schemas for durable records
└── Tools/brain.py          # dependency-free index, status, lint, and log CLI
```

## Quick start

1. Clone the repository.
2. Open it in an agent harness that reads `AGENTS.md`.
3. Ask the agent to initialize or inspect the workspace.
4. Try the operating loop:

```text
/capture This is a thought I do not want to lose.
/query What does the Brain know about it?
/explore Help me develop the idea.
/sync
```

Useful local checks:

```bash
python Tools/brain.py status
python Tools/brain.py index
python Tools/brain.py lint
python Tools/test_brain.py
```

For a guided setup, see [Getting Started](GETTING-STARTED.md). Russian onboarding is available in [QUICKSTART-RU.md](QUICKSTART-RU.md) and [USER-GUIDE.md](USER-GUIDE.md).

## Agent and harness integration

The workspace is deliberately harness-agnostic:

- `AGENTS.md` provides the portable entry point;
- `.agents/skills/` contains reusable skill documents;
- Markdown remains the source of truth;
- Git provides history and rollback;
- application code can stay in separate repositories.

Hermes Agent can expose the same skills in Desktop, CLI, Telegram, and IDE sessions. See [Hermes Setup](HERMES-SETUP.md).

## Safe by design

- Raw payloads are never silently rewritten.
- A source claim is not automatically a fact.
- User interpretation and agent inference remain labeled.
- Indexes and logs help discovery but do not outrank evidence.
- Review and Lint report findings; they do not silently repair semantic state.
- Checkpoints are deliberate and scoped.
- Private Brain content is not part of the reusable product core.

## Product and private workspaces

The clean product repository contains reusable skills, protocols, templates, tools, and starter files. A private Brain may contain personal context, project records, health data, captures, and source material.

Reusable improvements can move from private experimentation into the product, but only through an allowlisted, reviewed sync. Product updates move back into private Brains without overwriting protected user data.

See [Product Update Workflow](PRODUCT-UPDATE-WORKFLOW.md) and [Changelog](CHANGELOG.md).

## Documentation

- [Getting Started](GETTING-STARTED.md)
- [User Guide](USER-GUIDE.md)
- [Life Workspace Protocol](Protocols/Life-Workspace-Protocol.md)
- [Hermes Setup](HERMES-SETUP.md)
- [Product Update Workflow](PRODUCT-UPDATE-WORKFLOW.md)
- [Changelog](CHANGELOG.md)

## Status

Life Workspace is usable and under active design. The current focus is real-world validation: whether the workflows stay understandable, safe, and lightweight as the Brain grows across years and projects.