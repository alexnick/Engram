---
name: project-map
description: Use for large multi-session projects. Maintain a decision map and route the current frontier to the right workflow.
---

# Project Map

## Goal

Use one simple workflow for projects that are too broad for a single conversation. The user may call it a Project Map or ask to work through a large effort from high-level design to implementation planning.

The map is a navigation and decision-planning layer. It does not replace canonical project specs, decision records, source records, or implementation plans. It points to them and keeps the route clear.

## When to use

Use this skill when the user wants to:

* start or continue a large multi-session project;
* process notes into a game design, product design, architecture, course, or implementation roadmap;
* redesign a project from high-level systems down to dependency-ordered implementation work;
* avoid choosing between `explore`, `grilling`, `research`, `prototype`, and `sync` manually.

Do not create a project map for a small isolated question. Answer directly, or use `explore`/`grilling` internally when a single-session discussion is enough.

## User-facing interface

Keep the interface simple. The user should not need to remember multiple workflows.

Accept natural language such as:

* "Create a project map for <project>."
* "Continue the <project> map."
* "Work through this project from high-level design to an implementation plan."
* "Resolve system <X> within the project map."

## Startup router

Before substantial work, load `CONTEXT-MAP.md`, `Brain/INDEX.md`, root context, and relevant project context. Then classify the incoming task:

1. **Small decision:** a single isolated decision; handle directly or with a short internal explore/grilling pass. Do not create a map.
2. **Medium system:** one coherent subsystem; create or update one focused decision ticket/session if useful.
3. **Large project:** create or continue a Project Map with decision tickets, dependencies, fog, and out-of-scope boundaries.

If classification is unclear, ask up to four intake questions:

1. What should exist at the end: a spec, locked decision, prototype backlog, implementation plan, or something else?
2. What inputs already exist: notes, old GDD, codebase, spreadsheets, references, prior decisions?
3. Are we discovering direction, redesigning, writing specs, or planning implementation?
4. Should this pass be soft/expansive or hard/adversarial? If the user does not choose, default to breadth-first mapping.

## Map location

For a named project, prefer:

`Projects/<Project>/PROJECT-MAP.md`

For a temporary or cross-project effort, use the narrowest suitable existing project folder. Create a new project folder only when the project has an independent lifecycle and the user has approved durable project creation.

## Map structure

A Project Map should use this shape:

```markdown
# <Project> — Project Map

## Destination

<What reaching the end of this map means.>

## Inputs

<Existing notes, specs, code, references, decisions, and artifacts to account for.>

## Notes

<Standing preferences, constraints, relevant skills, and workflow rules.>

## Decisions so far

- `<link to resolved decision, spec, or ticket>` — <one-line gist.>

## Current frontier

<Open, unblocked questions or gates that can be worked now.>

## Blocked

<Questions that are real but depend on unresolved prerequisites.>

## Fog

<In-scope areas that are too vague to ticket yet. Do not pre-slice fog.>

## Out of scope

<Work consciously ruled beyond this map's destination.>

## Operating rules

<How to continue, how to close a ticket, and where durable results go.>
```

Use `Templates/Project-Map/MAP.md` and `Templates/Project-Map/TICKET.md` when creating fresh artifacts.

## Decision tickets

A ticket is a decision or investigation sized for one agent session. It is not a slice of implementation unless that task is required to unblock a decision.

Ticket types:

* `grilling` — human-in-the-loop decision pressure-test; use dependency-ordered rounds.
* `explore` — softer one-question-at-a-time development of a fuzzy subsystem.
* `research` — agent-driven reading of sources, code, docs, or existing Brain material.
* `prototype` — rough artifact created to make a decision concrete.
* `task` — preparatory work required before a decision can be made.

Work at most one non-research ticket per session unless the user explicitly narrows multiple tiny tickets into a single pass. Research tickets may run in parallel when independent.

## Working through a map

1. Load the map as the low-resolution view. Do not open every linked document by default.
2. Load only the relevant project context, specs, prior decisions, and ticket/session notes.
3. Pick the next unblocked item from `Current frontier` unless the user named a different item.
4. Route internally to the appropriate mode: exploration, grilling, research, prototype, task, or sync.
5. Resolve the item into one of:
   * a durable decision/spec update proposed through `sync-brain`;
   * a proposed implementation-plan or backlog change routed through `sync-brain` when it updates canonical project state;
   * a blocked item with explicit prerequisites;
   * a fog item graduated into a sharper ticket;
   * an out-of-scope ruling.
6. Update the map after approved semantic changes so `Decisions so far`, `Current frontier`, `Blocked`, `Fog`, and `Out of scope` remain accurate.

## Relationship to other skills

`project-map` is the main user-facing workflow for large projects. `explore`, `grilling`, `research` via subagents/tools, `prototype`, and `sync-brain` are internal modes or follow-up operations. The user does not need to choose among them.

Do not promote provisional map content into canonical project specs, decisions, or context without `sync-brain` approval. The map can be created or updated when the user explicitly asks to work through the project map, but consequential project semantics still require Sync before they become canonical state.
