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

## Back up self-improvement into Git

Hermes keeps its live profile under `HERMES_HOME`; Engram should not replace
that runtime directory. Moving the whole profile into a repository would also
capture credentials, configuration, logs, caches, databases, and transcripts.

Use the bounded mirror instead:

```bash
python Tools/hermes_state.py snapshot
python Tools/hermes_state.py status
```

The snapshot is written under `Agent-State/Hermes/<profile>/` and contains only:

- active agent-created skills recorded by `hermes journey --json`, including
  their references, templates, scripts, and assets;
- `memories/MEMORY.md`;
- `memories/USER.md`;
- a deterministic manifest and recovery guide.

It excludes provider configuration, API keys, OAuth tokens, MCP credentials,
session databases, transcripts, logs, caches, and Skills Hub metadata. The live
profile remains the runtime source, so Hermes continues working if the Engram
checkout is unavailable. Run snapshots on a schedule if desired, but create Git
checkpoints through the normal Engram approval boundary; an uncommitted mirror
is not yet a remote backup.

For script-only scheduling, copy `Tools/hermes_state_cron.py` into the active
profile's `scripts/` directory and schedule that filename with the Engram root
as the job workdir. The wrapper runs the tracked snapshot tool from the workdir
and produces no output when nothing changed. Its setup is repeated in the
generated recovery guide because Hermes cron configuration remains runtime
state and is not mirrored.

To verify recovery without touching the live profile:

```bash
python Tools/hermes_state.py restore --target-hermes-home ./restored-hermes
```

Inspect that directory first. To restore into an existing profile, point
`--target-hermes-home` at the active `HERMES_HOME`; the command refuses to
overwrite different files unless `--force` is explicit. Start a new Hermes
session after restoring. The snapshot's `RECOVERY.md` preserves the same
instructions beside the backed-up state.

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
