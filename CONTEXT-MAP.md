# Context Map

This is the small routing map for the Life Workspace. Keep it short; use `Brain/INDEX.md` for the full generated catalog.

## Start Here

- [Home Dashboard](Dashboards/HOME.md)
- [User Guide](USER-GUIDE.md)
- [Brain Context](Brain/CONTEXT.md)
- [Generated Brain Index](Brain/INDEX.md)
- [Operations Log](Brain/LOG.md)

## Main Areas

- [Inbox](Brain/Inbox/) — ordinary raw captures waiting for review.
- [Health Inbox](Brain/Health/Inbox/) — explicitly health-related raw captures.
- [Knowledge](Brain/Knowledge/) — reusable derived knowledge.
- [Decisions](Brain/Decisions/) — consequential approved decisions.
- [Entities](Brain/Entities/) — people, organizations, places, products, concepts, and other durable objects.
- [Events](Brain/Events/) — dated things that happened.
- [Sources](Brain/Sources/) — raw source provenance and derived source records.
- [Projects](Projects/) — project-specific contexts, maps, decisions, and status.
- [Learning](Learning/) — optional learning workspaces.

## Maintenance

- Do not turn this file into a full catalog.
- After substantive file changes, run `python Tools/brain.py index` to refresh `Brain/INDEX.md`.
- Use `python Tools/brain.py lint` to check structure and links.
