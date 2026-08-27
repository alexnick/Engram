#!/usr/bin/env python3
"""Cron-safe entry point for the Engram Hermes state snapshot."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    workspace = Path.cwd()
    snapshot_tool = workspace / "Tools" / "hermes_state.py"
    if not snapshot_tool.is_file():
        print(
            f"error: Hermes state tool not found under cron workdir: {snapshot_tool}",
            file=sys.stderr,
        )
        return 2
    return subprocess.run([sys.executable, str(snapshot_tool)], cwd=workspace).returncode


if __name__ == "__main__":
    raise SystemExit(main())
