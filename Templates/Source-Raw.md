---
type: source-raw
status: immutable
source_type: unknown # article, book, paper, video, podcast, document, locator, etc.
title: ""
author: ""
url_or_path: ""
artifact_path: "" # workspace-relative immutable sidecar artifact path, when stored locally
published: unknown
retrieved: YYYY-MM-DD
snapshot_status: full # full, partial, locator-only
content_hash: "" # optional when a local snapshot exists
---

# Raw Source: Title

> [!IMPORTANT]
> The entire manifest—frontmatter and body—is immutable after initial creation. If the source or metadata changes, preserve a new dated artifact or manifest. Never add future derived-record backlinks to this raw file.

## Locator

*Canonical URL or local path and any stable source identifier.*

## Artifact Sidecar

*For a binary or local artifact, store the immutable artifact beside this Markdown manifest with the same dated slug and its original extension: `YYYY-MM-DD--slug.md` for the manifest and, for example, `YYYY-MM-DD--slug.pdf` for the artifact. Set `artifact_path` to the workspace-relative artifact path, such as `Brain/Sources/Raw/domain/YYYY-MM-DD--slug.pdf`. The manifest and artifact are one immutable raw-source unit. Leave `artifact_path` empty for `locator-only` records.*

*Derived records own the one-way links to this manifest or its artifact. Do not edit the raw manifest later to add backlinks.*

## Snapshot Scope

*State exactly what was preserved. For `locator-only`, explicitly say that the full source content was not saved.*

## Raw Material

*Insert unmodified textual content here only when it is stored inline. For binary or separate local content, use the immutable `artifact_path` sidecar instead. Never place derived summaries or interpretations here.*

## Retrieval Notes

*Access date, retrieval limitations, format, and integrity details. Do not claim access to unavailable content.*
