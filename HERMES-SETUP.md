# Hermes Agent Setup

Hermes can use the same Life Workspace from Desktop, CLI, Telegram, and IDE sessions. The Brain remains the durable store; Hermes memory only keeps small routing facts and user preferences.

## 1. Register the workspace

Create a Hermes Project with the Life Workspace as its primary folder:

```bash
hermes project create "Life Workspace" /path/to/life-workspace --use
```

If the project already exists, select it in Hermes Desktop or with `hermes project use`.

## 2. Expose the skills globally

Point Hermes at the repository's skill directory:

```bash
hermes config set skills.external_dirs '/path/to/life-workspace/.agents/skills'
```

Use a plain path value. Do not pass a JSON array to `hermes config set`; the CLI stores command-line values as scalars, and Hermes accepts a single external directory as a scalar.

The skills will then be available in CLI, Desktop, Telegram, and other gateway platforms after a new session or gateway restart.

Verify:

```bash
hermes prompt-size --platform cli
hermes prompt-size --platform telegram
```

## 3. Choose the default working directory

For a dedicated Life Workspace profile:

```bash
hermes config set terminal.cwd '/path/to/life-workspace'
```

For a general coding profile, keep the project-specific working directory and store the canonical Life Workspace path as a small Hermes memory entry instead. Life Workspace skills should resolve Brain-relative paths against that root when the active repository is elsewhere.

## 4. Keep the memory layers separate

Use Hermes built-in memory for bounded information that belongs in every session:

- preferred communication style;
- the canonical Life Workspace path;
- stable workflow preferences;
- environment conventions.

Use the Brain for durable knowledge:

- source evidence;
- decisions and rationale;
- project context;
- reusable knowledge;
- captures and session outcomes;
- contradictions and supersession history.

Do not copy the Brain into `SOUL.md` or Hermes memory. Both are injected into every session and are intentionally small.

## 5. Avoid competing wiki rules

If another installed skill defines a different wiki schema, disable it so the Life Workspace skills remain authoritative:

```bash
hermes config set skills.disabled 'llm-wiki' --force
```

This is optional. Use it only when the other skill would trigger on the same requests.

## 6. Telegram

Run the gateway setup and select Telegram:

```bash
hermes gateway setup
```

Keep the bot token and user allowlist in the Hermes secret store or `.env`; keep behavioral settings in `config.yaml`.

For local voice transcription:

```bash
hermes config set stt.enabled true
hermes config set stt.provider local
hermes config set stt.local.model base
```

Then restart the gateway from a terminal outside the running gateway process:

```bash
hermes gateway restart
```

Useful Telegram commands:

```text
/commands
/capture ...
/project_map ...
/query_brain ...
/sync_brain ...
```

Telegram command names use underscores; Hermes skill names use hyphens. Natural-language requests work in either case.

Telegram topics can keep long-running projects in isolated sessions. A topic may preload a Life Workspace skill, while cron reports can be delivered to a dedicated topic.

## 7. Safe automation

Cron jobs may run read-only operations such as Lint, status reports, source monitoring, or proposal preparation. They should not approve their own semantic changes.

Recommended flow:

```text
cron or webhook -> report/proposal -> user approval -> Sync
```

Use `workdir` on scheduled jobs so the repository's `AGENTS.md` is loaded.

## 8. Validate

```bash
hermes doctor
hermes tools --summary
python Tools/brain.py status
python Tools/brain.py lint
python Tools/test_brain.py
```

Start a new Hermes session after changing `SOUL.md`, memory, toolsets, or global skill configuration. Existing sessions keep a frozen startup snapshot to preserve prompt caching.