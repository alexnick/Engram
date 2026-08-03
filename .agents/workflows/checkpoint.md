# Checkpoint Brain

Use this workflow when the user invokes `/checkpoint`.

1. Load and follow `.agents/skills/checkpoint-brain/SKILL.md`.
2. Default to propose mode.
3. Inspect Git status and relevant staged and unstaged diffs without changing the worktree.
4. Present the reason, intended paths, exclusions, risks, and proposed commit message.
5. Do not stage or commit unless the user directly requested execution or gives current explicit approval.
6. Before any staging or commit, enumerate every already-staged path. If any path is outside the current approved scope, stop, report it, and do not unstage, stage, or commit anything.
7. Otherwise stage only explicit intended paths and inspect the complete staged diff, because a normal commit includes all staged state.
8. Never include unrelated or sensitive files by implication.
9. Create one normal commit and report its identifier and paths only after success.
10. Never amend, reset, discard work, clean, force push, or create hidden commits.
