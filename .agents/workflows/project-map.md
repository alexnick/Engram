# Project Map Workflow

Use this adapter when the user invokes `/project-map`.

1. Load `.agents/skills/project-map/SKILL.md`.
2. Treat command arguments as the project name, destination, or current frontier request.
3. If no project is named, infer it only from clear active context; otherwise ask one short question.
4. Create or update map and ticket working artifacts only within the authorization granted by an explicit Project Map request.
5. Route changes to canonical context, decisions, specs, or implementation plans through `sync-brain`.
