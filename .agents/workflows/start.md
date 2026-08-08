# Start Engram

Use this workflow when the user invokes `/start`.

1. Read `.agents/AGENTS.md`.
2. Read `Protocols/Engram-Protocol.md`.
3. Read `CONTEXT-MAP.md` as the small router.
4. Read `Engram/CONTEXT.md` for root current state.
5. Read `Engram/INDEX.md` as the complete catalog of navigable corpus pages, including sessions and raw-source manifests, to locate active material without scanning the workspace.
6. Read only the relevant recently modified Markdown pages and active project context.
7. If a required navigation file is missing or stale, report the schema gap; do not silently replace it during startup.
8. Default to English and briefly report current priorities, active Explore sessions, unprocessed capture count, active project contexts, and obvious unresolved items.
9. Mention the available commands when useful: `/capture`, `/project-map`, `/explore`, `/ingest`, `/query`, `/sync`, `/review`, `/lint`, and `/checkpoint`.
10. Do not modify files, logs, metadata, indexes, or Git state during startup.
