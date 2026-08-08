# Changelog

All notable product changes to Life Workspace are recorded here.

The project is still pre-release. Earlier work is summarized from the product history without assigning unsupported release dates.

## Unreleased

### Added

- Harness-agnostic product maintenance skill for synchronizing reusable changes without copying private Brain content.
- Hermes Agent setup guide for Desktop, CLI, Telegram, global skills, and bounded memory.
- Explicit two-repository maintenance model: clean product core and protected private workspaces.
- Fetch-only product remote guidance for private Brains to prevent accidental publication.
- English-only product documentation, defaults, templates, and examples.
- A Project Map command adapter.

### Changed

- Replaced the long-form README with a concise English product overview.
- Strengthened the product update workflow with documentation, changelog, privacy, and validation gates.
- Made directory synchronization merge-safe so private repository-specific files are preserved.
- Consolidated onboarding into `QUICKSTART.md` and a shorter task-oriented `USER-GUIDE.md`.
- Moved integration and maintainer material under `docs/`.
- Removed stale Idea-entity references and aligned Teach and Project Map with the Sync approval boundary.
- Added a guard against synchronizing a checkout onto itself or into a nested subdirectory.

### Removed

- Russian-only onboarding and mixed-language examples from the product repository.
- Duplicate setup and maintainer documents from the repository root.

## Previous product work

### Added

- Project Map as the primary workflow for large multi-session projects.
- Decision-map templates with destination, frontier, blocked work, fog, and out-of-scope boundaries.
- Grilling workflow for dependency-ordered design interviews.
- Trial teaching workspace and skill-authoring guidance.
- Review state tracking and additional semantic lint checks.
- Markdown-first Brain structure.
- Raw and derived knowledge separation.
- Capture, Explore, Sync, Ingest, Query, Review, Lint, and Checkpoint workflows.
- Generated index, append-only operation log, dependency-free CLI, and Git checkpoint policy.

### Changed

- Folded early ideas into the Knowledge lifecycle instead of maintaining a separate Idea type.