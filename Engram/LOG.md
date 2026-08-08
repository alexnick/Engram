# Engram Operations Log

This append-only log records non-sensitive workspace operations for chronological search. Entries summarize what happened and link to affected durable paths; they do not replace substantive evidence or Git history. Existing entries must not be rewritten.

## Log Schema

Entries after this starter marker should use:

```text
## [YYYY-MM-DD] operation | Short non-sensitive title

Files:
- relative/path.md

Note: Optional bounded non-sensitive result, without raw payloads, source excerpts, health details, secrets, or absolute external paths.
```
