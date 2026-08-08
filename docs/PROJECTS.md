# Projects

A project keeps current state, decisions, and unresolved work together without copying the application source tree into the Brain.

## Suggested structure

```text
Projects/<Project>/
├── CONTEXT.md       current approved state
├── DECISIONS.md     consequential choices and rationale
├── PROJECT-MAP.md   navigation across unresolved work
├── Design/          optional specs and design notes
└── Research/        optional source-grounded investigations
```

`CONTEXT.md` is a current-state page, not a diary or task dump. `DECISIONS.md` explains why important choices were made. `PROJECT-MAP.md` tracks the destination, current frontier, blocked questions, fog, and out-of-scope work.

The map can change while the project is being worked through. Changes to approved context, decisions, specs, or implementation plans go through Sync.

## Source code

Keep large source trees outside the Brain. Connect the code repository and the relevant Brain folder in the agent harness or IDE. This keeps search focused and lets the Brain stay portable.

## Starting a project

Say:

```text
Create a project map for <project>. The destination is <deliverable>. Use the existing notes and codebase as inputs.
```

The agent should read only the project context and evidence needed for the current frontier, not recursively scan every linked repository.
