# Start Life Workspace

Use this workflow when the user invokes `/start`.

1. Read `.agents/AGENTS.md`.
2. Read `Protocols/Life-Workspace-Protocol.md`.
3. Read `CONTEXT-MAP.md` as the small router.
4. Read `Brain/CONTEXT.md` for root current state.
5. Read `Brain/INDEX.md` as the complete catalog of navigable corpus pages, including sessions and raw-source manifests, to locate active material without scanning the workspace.
6. Read `Projects/Life-Workspace/STATUS.md` and only the relevant recently modified Markdown pages.
7. If a required navigation file is missing or stale, report the schema gap; do not silently replace it during startup.
8. Respond in the user's language and briefly report current priorities, active Explore sessions, unprocessed capture count, active project contexts, and obvious unresolved items.
9. Mention the available commands when useful: `/capture`, `/explore`, `/ingest`, `/query`, `/sync`, `/review`, `/lint`, and `/checkpoint`.
10. Do not modify files, logs, metadata, indexes, or Git state during startup.
