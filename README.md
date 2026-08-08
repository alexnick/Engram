# Engram

**A durable Markdown brain for AI agents.**

Chats are useful for thinking. They are a poor place to keep decisions, evidence, and project context.

Engram gives an AI agent a small, explicit system for maintaining knowledge across conversations. Markdown holds the state. Git keeps the history. Skills define how information enters, changes, and leaves the workspace.

## The model

Engram keeps three things separate:

1. **Raw evidence** preserves what was actually said, received, or observed. Captures and source artifacts are append-only.
2. **Derived knowledge** holds the current working model: context, knowledge, decisions, entities, events, source records, and project documents.
3. **Operations** control the movement between them. An agent can preserve raw input immediately, but it must show a proposal before changing durable meaning.

> Conversation is temporary. Durable meaning enters the Engram through an explicit operation.

This is an implementation of the [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) idea, originally proposed by Andrej Karpathy: a maintained knowledge base that compounds over time instead of a pile of transcripts that must be re-read from scratch.

## Core operations

| Operation | Use it to |
|---|---|
| `capture` | Preserve exact wording before it gets lost. |
| `project-map` | Work through a large project across many sessions. |
| `explore` | Develop an unclear idea one question at a time. |
| `grilling` | Pressure-test a plan or decision. |
| `ingest-source` | Preserve a source and extract grounded claims from it. |
| `query-engram` | Answer from the Engram with links to the pages used. |
| `sync-engram` | Preview and apply approved changes to durable knowledge. |
| `review-engram` | Process unhandled captures in small batches. |
| `lint-engram` | Check structure and semantic drift without editing files. |
| `checkpoint-engram` | Create a deliberate Git checkpoint after approval. |

You do not need to memorize these names. Describe what you want in plain English and let the agent route the request.

## Try it

```bash
git clone https://github.com/alexnick/Engram.git engram
cd engram
python Tools/engram.py status
python Tools/engram.py lint
```

Open the folder in an agent harness that reads `AGENTS.md`, then say:

```text
Save this exact thought: a useful memory system should preserve evidence without turning every thought into a fact.
```

Next:

```text
What does the Engram know about memory systems?
```

When a discussion produces a decision or reusable insight:

```text
Show me what you would update in the Engram. Do not write it until I approve the proposal.
```

See [Quickstart](QUICKSTART.md) for the full first-use loop.

## Repository layout

```text
Engram/
├── AGENTS.md               portable entry point for agents
├── .agents/
│   ├── AGENTS.md           agent contract
│   ├── skills/             reusable operations
│   └── workflows/          command adapters
├── Engram/                  personal knowledge and evidence
├── Projects/               project context, maps, and decisions
├── Protocols/              storage and approval rules
├── Templates/              record schemas
└── Tools/engram.py          index, status, lint, and log CLI
```

The public repository contains an empty starter Brain. Your private Brain contains your actual captures, projects, sources, and personal context.

## Why the boundaries matter

- Raw text is never silently cleaned up or rewritten.
- A source claim does not become a fact because an agent summarized it.
- User interpretation and agent inference stay labeled.
- Indexes and logs help discovery; they are not evidence.
- Review and Lint report findings without silently repairing knowledge.
- Semantic writes require a concrete proposal and approval.
- Git checkpoints are scoped and deliberate.

## Agent integration

The format is harness-independent. Any agent that can read Markdown and follow `AGENTS.md` can use it. The same Brain can be opened from an IDE, a terminal agent, or a chat gateway without moving knowledge into that tool's private memory.

For Hermes Agent, see [docs/HERMES.md](docs/HERMES.md).

## Documentation

- [Quickstart](QUICKSTART.md)
- [User Guide](USER-GUIDE.md)
- [Protocol](Protocols/Engram-Protocol.md)
- [Project conventions](docs/PROJECTS.md)
- [Hermes integration](docs/HERMES.md)
- [Maintainer guide](docs/MAINTAINING.md)
- [Changelog](CHANGELOG.md)

## Acknowledgements

Engram stands on existing ideas we learned from and adapted:

- **[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)** by [Andrej Karpathy](https://karpathy.bearblog.dev/) — the core architecture of an LLM-maintained Markdown knowledge base with immutable raw sources, a derived wiki, and Ingest/Query/Lint operations. Engram is a direct implementation of this idea.
- **[mattpocock/skills](https://github.com/mattpocock/skills)** by [Matt Pocock](https://github.com/mattpocock) — the grilling pattern (interviewing in dependency-ordered rounds over a design tree) inspired the `grilling` skill, and the `teach` skill was adopted on trial from the same repository.

## Status

Engram is usable and still evolving. Current work focuses on keeping the system understandable and safe as a Brain grows across years, projects, and agent harnesses.
