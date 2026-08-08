# Getting Started

This repository is a clean Life Workspace starter. It should contain product files and an empty personal Brain skeleton, not someone else's private content.

## First 5 minutes

1. Open this folder in your agent shell.
2. Ask the agent to read `AGENTS.md`, `.agents/AGENTS.md`, and `USER-GUIDE.md`.
3. Try a raw capture:

   ```text
   /capture Это мой первый тестовый capture.
   ```

4. Ask from the Brain:

   ```text
   /query Что Brain знает о первом тестовом capture?
   ```

5. Develop an idea:

   ```text
   /explore Как я хочу использовать Brain в ближайшую неделю?
   ```

6. If the result should become durable state, ask:

   ```text
   /sync
   ```

## Useful commands

```bash
python Tools/brain.py status
python Tools/brain.py index
python Tools/brain.py lint
python Tools/test_brain.py
```

## Rules of thumb

- Do not manually edit `Brain/INDEX.md`; regenerate it with the CLI.
- Do not rewrite raw captures or raw source manifests.
- Use Git checkpoints after meaningful approved changes, not after every capture.
- Keep application source code outside this Brain unless there is a deliberate reason to reference it.

## Harness setup

- Agent shells should start from [AGENTS.md](AGENTS.md).
- Hermes users can expose the repository skills across Desktop, CLI, Telegram, and IDE sessions with [HERMES-SETUP.md](HERMES-SETUP.md).
- Maintainers should use [PRODUCT-UPDATE-WORKFLOW.md](PRODUCT-UPDATE-WORKFLOW.md) and update [CHANGELOG.md](CHANGELOG.md) for reusable changes.
