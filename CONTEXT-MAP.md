# Context Map

This is the small routing map for the Engram. Keep it short; use `Engram/INDEX.md` for the full generated catalog.

## Start Here

- [Home Dashboard](Dashboards/HOME.md)
- [User Guide](USER-GUIDE.md)
- [Brain Context](Engram/CONTEXT.md)
- [Generated Engram Index](Engram/INDEX.md)
- [Operations Log](Engram/LOG.md)

## Main Areas

- [Inbox](Engram/Inbox/) — ordinary raw captures waiting for review.
- [Health Inbox](Engram/Health/Inbox/) — explicitly health-related raw captures.
- [Knowledge](Engram/Knowledge/) — reusable derived knowledge.
- [Decisions](Engram/Decisions/) — consequential approved decisions.
- [Entities](Engram/Entities/) — people, organizations, places, products, concepts, and other durable objects.
- [Events](Engram/Events/) — dated things that happened.
- [Sources](Engram/Sources/) — raw source provenance and derived source records.
- [Projects](docs/PROJECTS.md) — conventions for project contexts, maps, decisions, and external source trees.
- [Learning](Learning/) — optional learning workspaces.

## Maintenance

- Do not turn this file into a full catalog.
- After substantive file changes, run `python Tools/engram.py index` to refresh `Engram/INDEX.md`.
- Use `python Tools/engram.py lint` to check structure and links.
