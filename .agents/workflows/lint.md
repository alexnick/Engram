# Lint Brain

Use this workflow when the user invokes `/lint`.

1. Load and follow `.agents/skills/lint-engram/SKILL.md`.
2. Run `python Tools/engram.py lint` first and record its exact exit status and output.
3. Perform the targeted semantic checks after the deterministic pass, even if the command reports failures.
4. Return a read-only report with deterministic results, semantic findings, clean checks, and a proposed fix plan.
5. Do not modify, stage, or commit files.
6. Route requested fixes through `/sync`, where approval boundaries still apply.
