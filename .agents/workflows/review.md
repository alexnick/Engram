# Review Brain

Use this workflow when the user invokes `/review`.

1. Load and follow `.agents/skills/review-engram/SKILL.md`.
2. Default to Inbox review unless the user names another scope.
3. Run `python Tools/engram.py status` and report an exact failure if it is unavailable.
4. Target-scan Inbox metadata, cross-check candidates against `Engram/INDEX.md`, and read only nearby relevant context. Never rely on index status alone.
5. Present no more than ten cited review items at once.
6. Wait for decisions before semantic changes, merge, archive, delete, context changes, or health interpretation.
7. Apply approved actions through Sync semantics while preserving all raw payloads.
8. Use `/lint` instead when the requested task is a broad schema or link audit.
9. Never delete or commit automatically.
