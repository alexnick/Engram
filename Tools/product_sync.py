#!/usr/bin/env python3
"""Conservative local helper for syncing Life Workspace product/core files.

This script copies only allowlisted product/core paths between local checkouts.
It intentionally does not commit, push, delete protected user data, or resolve
Git conflicts. Always inspect diffs after running it.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ALLOWLIST = [
    '.agents/AGENTS.md',
    '.agents/rules',
    '.agents/workflows',
    '.agents/skills/capture',
    '.agents/skills/checkpoint-brain',
    '.agents/skills/explore',
    '.agents/skills/grilling',
    '.agents/skills/ingest-source',
    '.agents/skills/lint-brain',
    '.agents/skills/maintain-life-workspace-product',
    '.agents/skills/project-map',
    '.agents/skills/query-brain',
    '.agents/skills/review-brain',
    '.agents/skills/sync-brain',
    '.agents/skills/teach',
    '.agents/skills/writing-great-skills',
    'Protocols',
    'Templates',
    'Tools/brain.py',
    'Tools/test_brain.py',
    'Tools/product_sync.py',
    'Dashboards/HOME.md',
    'README.md',
    'USER-GUIDE.md',
    'QUICKSTART.md',
    'docs',
    'CHANGELOG.md',
    'AGENTS.md',
    '.gitignore',
]

PROTECTED_PREFIXES = [
    'Brain/CONTEXT.md',
    'Brain/INDEX.md',
    'Brain/LOG.md',
    'Brain/.review-state.md',
    'Brain/Inbox',
    'Brain/Health',
    'Brain/Knowledge',
    'Brain/Decisions',
    'Brain/Entities',
    'Brain/Events',
    'Brain/Sessions',
    'Brain/Sources',
    'Projects',
    'Learning',
    'Feedback',
    'CONTEXT-MAP.md',
]

IGNORE_NAMES = {'__pycache__', '.git', '.DS_Store'}


def is_protected(path: str) -> bool:
    normalized = path.replace('\\', '/').rstrip('/')
    return any(normalized == p or normalized.startswith(p.rstrip('/') + '/') for p in PROTECTED_PREFIXES)


def validate_roots(source_root: Path, target_root: Path) -> None:
    if source_root.resolve() == target_root.resolve():
        raise ValueError('source and target must be different checkouts')
    source_resolved = source_root.resolve()
    target_resolved = target_root.resolve()
    if source_resolved in target_resolved.parents or target_resolved in source_resolved.parents:
        raise ValueError('source and target must not be nested inside each other')


def copy_path(source_root: Path, target_root: Path, item: str, dry_run: bool) -> str:
    if is_protected(item):
        raise ValueError(f'allowlist contains protected path: {item}')

    source = source_root / item
    target = target_root / item
    if not source.exists():
        return f'skip missing: {item}'

    if dry_run:
        return f'would copy: {item}'

    if source.is_dir():
        shutil.copytree(
            source,
            target,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(*IGNORE_NAMES, '*.pyc', '*.pyo'),
        )
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return f'copied: {item}'


def main() -> int:
    parser = argparse.ArgumentParser(description='Sync allowlisted Life Workspace product/core paths between local checkouts.')
    parser.add_argument('--source', required=True, type=Path, help='Source checkout path')
    parser.add_argument('--target', required=True, type=Path, help='Target checkout path')
    parser.add_argument('--dry-run', action='store_true', help='Print planned copies without writing')
    args = parser.parse_args()

    source = args.source.resolve()
    target = args.target.resolve()
    if not source.exists():
        parser.error(f'source does not exist: {source}')
    if not target.exists():
        parser.error(f'target does not exist: {target}')

    try:
        validate_roots(source, target)
    except ValueError as error:
        parser.error(str(error))

    for item in ALLOWLIST:
        print(copy_path(source, target, item, args.dry_run))
    print('Done. Inspect git diff before committing.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
