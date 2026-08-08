# Hermes Agent integration

Hermes can expose one Engram across Desktop, CLI, Telegram, and IDE sessions. Markdown remains the durable store. Hermes memory should hold only small routing facts and stable preferences.

The Hermes documentation changes faster than this guide. Check the [official docs](https://hermes-agent.nousresearch.com/docs) when a command differs from your installed version.

## Create a Hermes Project

Windows:

```bash
hermes project create "Engram" C:/workspace/Brain --use
```

Linux or macOS:

```bash
hermes project create "Engram" /path/to/Brain --use
```

To select an existing project, include its slug or ID:

```bash
hermes project use <project-slug>
```

Do not run bare `hermes project use`; current Hermes versions use that form to clear the active project.

## Expose the skills

Add the repository skill directory to the active Hermes profile:

```bash
hermes config set skills.external_dirs 'C:/workspace/Engram/.agents/skills'
```

This setting is profile-scoped. If you already use other external skill directories, inspect the current value before replacing it.

Verify discovery:

```bash
hermes prompt-size --platform cli
hermes prompt-size --platform telegram
```

Start a new session after changing startup configuration.

## Choose a working directory

A dedicated Engram profile can start inside the Engram:

```bash
hermes config set terminal.cwd 'C:/workspace/Brain'
```

A general coding profile may keep a project-specific working directory instead. Store the canonical Brain path as a small Hermes memory fact so Engram skills can resolve it when another repository is active.

## Keep the memory layers separate

Hermes memory is appropriate for:

- the canonical Brain path;
- stable environment conventions;
- communication preferences;
- small routing facts needed in every session.

The Engram is appropriate for:

- evidence and sources;
- decisions and rationale;
- project context;
- reusable knowledge;
- captures and session outcomes;
- contradictions and supersession history.

Do not copy the Engram into Hermes memory or `SOUL.md`. Both are startup context and should stay small.

## Telegram

Run the gateway setup and select Telegram:

```bash
hermes gateway setup
```

Keep the bot token in the Hermes secret store or environment file. The user allowlist is behavioral configuration and belongs in `config.yaml`, not in the secret store.

Optional local voice transcription:

```bash
hermes config set stt.enabled true
hermes config set stt.provider local
hermes config set stt.local.model base
```

Restart the gateway from a terminal outside the running gateway process:

```bash
hermes gateway restart
```

Telegram command names use underscores:

```text
/capture ...
/project_map ...
/query_brain ...
/sync_brain ...
```

Natural-language requests work without command names. Telegram topics can keep long-running projects in separate sessions.

## Avoid competing wiki rules

If another installed skill defines a different knowledge schema and triggers on the same requests, disable it in the active profile:

```bash
hermes config set skills.disabled 'llm-wiki' --force
```

Use this only when the skills actually conflict.

## Safe automation

Cron jobs and webhooks may run read-only checks, monitor sources, or prepare proposals. They should not approve their own semantic changes.

```text
automation -> report or proposal -> user approval -> Sync
```

Set the scheduled job's working directory to the Engram so Hermes loads `AGENTS.md`.

## Verify

```bash
hermes doctor
hermes tools --summary
python Tools/engram.py status
python Tools/engram.py lint
python Tools/test_engram.py
```
