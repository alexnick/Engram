# Query Brain

Use this workflow when the user invokes `/query`.

1. Load and follow `.agents/skills/query-brain/SKILL.md`.
2. Determine the question from command text or the current request.
3. Load `CONTEXT-MAP.md`, then `Brain/INDEX.md`, then relevant canonical pages.
4. Read raw evidence only when exact wording, verification, or disputed provenance requires it.
5. Answer with claim-level standard Markdown citations.
6. Clearly separate durable state, source claims, user interpretation, and agent inference.
7. Surface conflicts, uncertainty, dates, and open questions.
8. Keep Query read-only. Propose Sync once at a natural boundary only for a novel durable synthesis.
9. Do not propose or create a checkpoint merely because Query completed.
