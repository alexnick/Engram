# Projects

This directory contains workspace projects.

## Project Structure

Each project directory should normally contain:

* `CONTEXT.md` — The project's purpose, current state, constraints, and open questions.
* `STATUS.md` — Current milestone, completed items, and immediate next steps.
* `DECISIONS.md` — A log of consequential technical and design decisions.
* `Design/` *(optional)* — Design notes, mockups, and assets.
* `Research/` *(optional)* — Research notes, comparisons, and investigations.
* Links or references to external source-code folders.

## Source Code Policy

Large application source trees and repository directories (e.g., Unity project directories, large codebases) should **not** be copied directly into the Life Workspace. Keeping source trees separate prevents clutter, reduces search latency, and keeps the Brain highly portable.

Instead, the agent workspace can connect to the external source folder alongside the project's folder in the Life Workspace using the appropriate shell or IDE settings.
