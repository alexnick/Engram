#!/usr/bin/env python3
"""Mirror safe Hermes self-improvement state into an Engram checkout.

The live Hermes profile remains the runtime source. This tool snapshots only
agent-created skills recorded by ``hermes journey --json`` plus the bounded
built-in memory files. It never copies configuration, credentials, sessions,
logs, caches, or databases.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

FORMAT_VERSION = 1
STATE_RELATIVE_ROOT = Path("Agent-State") / "Hermes"
MEMORY_FILES = ("MEMORY.md", "USER.md")
IGNORED_NAMES = {"__pycache__", ".DS_Store"}
IGNORED_SUFFIXES = {".pyc", ".pyo", ".tmp"}
RECOVERY_TEXT = """# Restore Hermes self-improvement state

This directory is a Git-backed mirror. Hermes continues to run from its normal
profile directory, so a missing or unavailable Engram checkout does not stop
Hermes.

The mirror contains only:

- agent-created skills listed by `hermes journey --json`;
- `memories/MEMORY.md`;
- `memories/USER.md`.

It intentionally excludes configuration, secrets, OAuth tokens, session
transcripts, databases, logs, caches, and Skills Hub metadata.

## Check the live profile against this mirror

From the Engram root:

```bash
python Tools/hermes_state.py status
```

## Recreate automatic snapshots

Copy the durable cron wrapper into the active Hermes profile:

```bash
cp Tools/hermes_state_cron.py "$HERMES_HOME/scripts/hermes_state_cron.py"
```

Then create a script-only Hermes cron job that runs `hermes_state_cron.py`
every 30 minutes with the Engram root as its workdir. The wrapper depends only
on the tracked `Tools/hermes_state.py`; it prints nothing when the snapshot is
already current. Cron configuration itself is Hermes runtime state and is not
part of this mirror.

## Restore after reinstalling Hermes

First restore into a temporary directory and inspect it:

```bash
python Tools/hermes_state.py restore --target-hermes-home ./restored-hermes
```

Then restore into the active profile. Set `HERMES_HOME` to that profile and use
`--force` only after reviewing conflicts:

```bash
python Tools/hermes_state.py restore --target-hermes-home "$HERMES_HOME" --force
```

Start a new Hermes session after restoring skills or memory. API keys, OAuth
tokens, provider configuration, MCP credentials, and conversation history must
be restored separately because they are deliberately absent from this mirror.
"""


@dataclass(frozen=True)
class SnapshotResult:
    changed_files: int
    skill_count: int


@dataclass(frozen=True)
class StatusResult:
    changed: tuple[str, ...]
    missing: tuple[str, ...]
    extra: tuple[str, ...]

    @property
    def in_sync(self) -> bool:
        return not (self.changed or self.missing or self.extra)


@dataclass(frozen=True)
class RestoreResult:
    changed_files: int


def default_hermes_home() -> Path:
    configured = os.environ.get("HERMES_HOME")
    if configured:
        return Path(configured).expanduser()
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "hermes"
    return Path.home() / ".hermes"


def load_journey() -> dict[str, Any]:
    completed = subprocess.run(
        ["hermes", "journey", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise ValueError("hermes journey returned a non-object JSON value")
    return value


def learned_skill_names(journey: dict[str, Any]) -> list[str]:
    names = {
        node.get("id")
        for node in journey.get("nodes", [])
        if isinstance(node, dict)
        and node.get("kind") == "skill"
        and node.get("state") == "active"
        and node.get("createdBy") == "agent"
        and isinstance(node.get("id"), str)
    }
    return sorted(names)


def frontmatter_name(skill_md: Path) -> str | None:
    lines = skill_md.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, separator, value = line.partition(":")
        if separator and key.strip() == "name":
            return value.strip().strip("\"'")
    return None


def discover_learned_skills(skills_root: Path, names: Iterable[str]) -> dict[str, Path]:
    requested = set(names)
    found: dict[str, Path] = {}
    if skills_root.is_dir():
        for skill_md in skills_root.rglob("SKILL.md"):
            name = frontmatter_name(skill_md)
            if name not in requested:
                continue
            if name in found:
                raise ValueError(f"duplicate learned skill name in Hermes profile: {name}")
            found[name] = skill_md.parent
    missing = sorted(requested - found.keys())
    if missing:
        raise ValueError("learned skills missing from Hermes profile: " + ", ".join(missing))
    return found


def included_files(root: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file()
            and not any(part in IGNORED_NAMES for part in path.relative_to(root).parts)
            and path.suffix not in IGNORED_SUFFIXES
        ),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in included_files(root):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def state_root(workspace: Path, profile: str) -> Path:
    if not profile or profile in {".", ".."} or any(character in profile for character in "/\\"):
        raise ValueError("profile must be a single non-empty path component")
    return workspace.resolve() / STATE_RELATIVE_ROOT / profile


def build_manifest(hermes_home: Path, journey: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Path]]:
    names = learned_skill_names(journey)
    skills = discover_learned_skills(hermes_home / "skills", names)
    memory_entries: list[dict[str, str]] = []
    for filename in MEMORY_FILES:
        path = hermes_home / "memories" / filename
        if not path.is_file():
            raise ValueError(f"Hermes memory file missing: {filename}")
        memory_entries.append({"name": filename, "sha256": sha256_bytes(path.read_bytes())})

    skill_entries = []
    for name in names:
        relative = skills[name].relative_to(hermes_home / "skills").as_posix()
        skill_entries.append(
            {"name": name, "relative_path": relative, "sha256": tree_sha256(skills[name])}
        )
    manifest = {
        "format_version": FORMAT_VERSION,
        "memories": memory_entries,
        "skills": skill_entries,
    }
    return manifest, skills


def copy_file_if_changed(source: Path, destination: Path) -> int:
    content = source.read_bytes()
    if destination.is_file() and destination.read_bytes() == content:
        return 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return 1


def write_text_if_changed(destination: Path, content: str) -> int:
    encoded = content.encode("utf-8")
    if destination.is_file() and destination.read_bytes() == encoded:
        return 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(encoded)
    return 1


def mirror_directory(source: Path, destination: Path) -> int:
    changed = 0
    source_relatives = {path.relative_to(source) for path in included_files(source)}
    for relative in sorted(source_relatives, key=lambda path: path.as_posix().casefold()):
        changed += copy_file_if_changed(source / relative, destination / relative)
    if destination.is_dir():
        destination_files = included_files(destination)
        for path in destination_files:
            if path.relative_to(destination) not in source_relatives:
                path.unlink()
                changed += 1
        for directory in sorted(
            (path for path in destination.rglob("*") if path.is_dir()),
            key=lambda path: len(path.parts),
            reverse=True,
        ):
            if not any(directory.iterdir()):
                directory.rmdir()
    return changed


def snapshot(
    workspace: Path,
    hermes_home: Path,
    profile: str = "default",
    journey: dict[str, Any] | None = None,
) -> SnapshotResult:
    workspace = workspace.resolve()
    hermes_home = hermes_home.resolve()
    journey = journey if journey is not None else load_journey()
    manifest, skills = build_manifest(hermes_home, journey)
    destination = state_root(workspace, profile)
    changed = 0

    for filename in MEMORY_FILES:
        changed += copy_file_if_changed(
            hermes_home / "memories" / filename,
            destination / "memories" / filename,
        )
    for entry in manifest["skills"]:
        changed += mirror_directory(
            skills[entry["name"]],
            destination / "skills" / Path(entry["relative_path"]),
        )

    serialized_manifest = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    changed += write_text_if_changed(destination / "manifest.json", serialized_manifest)
    changed += write_text_if_changed(destination / "RECOVERY.md", RECOVERY_TEXT)
    return SnapshotResult(changed_files=changed, skill_count=len(manifest["skills"]))


def manifest_entries(manifest: dict[str, Any]) -> dict[str, str]:
    entries = {
        f"memories/{item['name']}": item["sha256"]
        for item in manifest.get("memories", [])
    }
    entries.update(
        {
            f"skills/{item['relative_path']}": item["sha256"]
            for item in manifest.get("skills", [])
        }
    )
    return entries


def status(
    workspace: Path,
    hermes_home: Path,
    profile: str = "default",
    journey: dict[str, Any] | None = None,
) -> StatusResult:
    destination = state_root(workspace, profile)
    manifest_path = destination / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"snapshot manifest missing: {manifest_path}")
    stored = json.loads(manifest_path.read_text(encoding="utf-8"))
    live, _ = build_manifest(
        hermes_home.resolve(), journey if journey is not None else load_journey()
    )
    stored_entries = manifest_entries(stored)
    live_entries = manifest_entries(live)
    shared = stored_entries.keys() & live_entries.keys()
    return StatusResult(
        changed=tuple(sorted(key for key in shared if stored_entries[key] != live_entries[key])),
        missing=tuple(sorted(stored_entries.keys() - live_entries.keys())),
        extra=tuple(sorted(live_entries.keys() - stored_entries.keys())),
    )


def restore(
    workspace: Path,
    target_hermes_home: Path,
    profile: str = "default",
    force: bool = False,
) -> RestoreResult:
    source = state_root(workspace, profile)
    target = target_hermes_home.resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError("snapshot and restore target must not overlap")
    manifest_path = source / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"snapshot manifest missing: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    copies: list[tuple[Path, Path]] = []
    for item in manifest.get("memories", []):
        copies.append((source / "memories" / item["name"], target / "memories" / item["name"]))
    for item in manifest.get("skills", []):
        skill_source = source / "skills" / Path(item["relative_path"])
        skill_target = target / "skills" / Path(item["relative_path"])
        copies.extend(
            (path, skill_target / path.relative_to(skill_source))
            for path in included_files(skill_source)
        )

    missing_sources = [str(source_path) for source_path, _ in copies if not source_path.is_file()]
    if missing_sources:
        raise ValueError("snapshot files missing: " + ", ".join(missing_sources))
    conflicts = [
        destination
        for source_path, destination in copies
        if destination.is_file() and destination.read_bytes() != source_path.read_bytes()
    ]
    if conflicts and not force:
        names = ", ".join(str(path) for path in conflicts)
        raise ValueError(f"restore would overwrite different files; inspect them or use --force: {names}")

    changed = sum(copy_file_if_changed(source_path, destination) for source_path, destination in copies)
    return RestoreResult(changed_files=changed)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mirror safe Hermes self-improvement state into an Engram checkout."
    )
    subparsers = parser.add_subparsers(dest="command")

    def common(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--workspace", type=Path, default=Path.cwd())
        subparser.add_argument("--hermes-home", type=Path, default=default_hermes_home())
        subparser.add_argument("--profile", default="default")

    snapshot_parser = subparsers.add_parser("snapshot")
    common(snapshot_parser)
    snapshot_parser.add_argument("--quiet", action="store_true")

    status_parser = subparsers.add_parser("status")
    common(status_parser)

    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument("--workspace", type=Path, default=Path.cwd())
    restore_parser.add_argument("--profile", default="default")
    restore_parser.add_argument("--target-hermes-home", type=Path, required=True)
    restore_parser.add_argument("--force", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments:
        arguments = ["snapshot", "--quiet"]
    parser = build_parser()
    args = parser.parse_args(arguments)
    try:
        if args.command == "snapshot":
            result = snapshot(args.workspace, args.hermes_home, args.profile)
            if not args.quiet and result.changed_files:
                print(
                    f"Updated Hermes snapshot: {result.changed_files} file(s), "
                    f"{result.skill_count} learned skill(s)."
                )
            return 0
        if args.command == "status":
            result = status(args.workspace, args.hermes_home, args.profile)
            if result.in_sync:
                print("Hermes self-improvement snapshot is in sync.")
                return 0
            for label, values in (
                ("changed", result.changed),
                ("missing from live profile", result.missing),
                ("new in live profile", result.extra),
            ):
                for value in values:
                    print(f"{label}: {value}")
            return 1
        if args.command == "restore":
            result = restore(
                args.workspace,
                args.target_hermes_home,
                args.profile,
                force=args.force,
            )
            print(f"Restored {result.changed_files} file(s).")
            return 0
    except (OSError, subprocess.SubprocessError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    parser.error("a command is required")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
