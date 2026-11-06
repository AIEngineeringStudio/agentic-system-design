---
name: pycharm-workflow
description: PyCharm IDE setup, required plugins, and Run/Debug configuration instructions for hands-on exercises, covering PyCharm Professional (Apple Silicon Mac) and PyCharm Community (Intel Mac).
---

# PyCharm Workflow

Use this skill whenever a hands-on task needs to be run or debugged inside
PyCharm, or when the learner asks how to configure the IDE. Apply it together
with `first-principles-learning` (and `tech-stack-curriculum` for stack topics).

## Match the learning stage

- For concept exercises, use the lesson's local Python interpreter or virtual
  environment. Use the `uv` setup below after `uv` has been introduced; IDE
  setup must not force Docker, `uv`, or typed configuration into an earlier
  lesson.
- For production extensions, follow the curriculum's containerized workflow once
  its prerequisites are covered. The local-debugging fallback below is an
  allowed development workflow; retain containerized run instructions for the
  extension.
- In complete guides, provide the relevant setup and run instructions without
  pausing for learner responses. For quick clarifications, include only the IDE
  details needed to answer the question.

## Environment

| Machine | Chip                  | PyCharm edition      |
|---------|-----------------------|----------------------|
| Mac A   | Apple Silicon (arm64) | PyCharm Professional |
| Mac B   | Intel (x86_64)        | PyCharm Community    |

Professional bundles the Docker and Database Tools plugins; Community does not.
Whenever a feature is Professional-only, give the Community terminal-based
fallback right after it, clearly labeled.

## Required plugins

- **Both editions:** Python support must be enabled.
    - **Professional:** bundled. Verify under Settings → Plugins → Installed.
    - **Community:** install the free "Python Community Edition" plugin via
      Settings → Plugins → Marketplace, if not already installed.
- **Professional only** (bundled, just verify enabled): Docker; Database Tools
  and SQL.
- **Community fallback:** no bundled Docker/Database plugins.
    - Use the Terminal tool window for `docker` and `psql` commands.
    - Optional: install a free Docker plugin from Marketplace for basic support,
      or use an external DB client (e.g., DataGrip, TablePlus, `psql`).
- **Optional, both editions:** an ".env files support" plugin (Settings →
  Plugins → Marketplace) so run configurations can read `.env` values.

## Python interpreter setup (`uv`)

1. In the Terminal tool window, from the project root: `uv venv` then `uv sync`.
2. PyCharm: Settings → Project: gen-ui → Python Interpreter → Add Interpreter →
   Add Local Interpreter → select the existing `.venv/bin/python` created by
   `uv`.
    - PyCharm 2024.2+ also offers a native `uv` interpreter type in the same
      dialog; use it if present.
3. Verify: the Terminal tool window shows a `(.venv)` prefix, and `python -V`
   matches the pinned version from `tech-stack-curriculum`.

## Run/Debug configurations

### Plain Python script

- Run → Edit Configurations → `+` → Python.
- Script path: the file to run (e.g., `main.py`).
- Working directory: project root.
- Python interpreter: the lesson's selected interpreter (the `uv` `.venv` once
  introduced).

### FastAPI (uvicorn)

- Run → Edit Configurations → `+` → Python.
- Use "Module name" (not script path): `uvicorn`.
- Parameters: `app.main:app --reload --host 0.0.0.0 --port 8000`.
- Working directory: project root.

### FastMCP server

- Same as "Plain Python script," pointing at the server entry file, or a "Module
  name" configuration if the server exposes a CLI entry point.

### PostgreSQL

**Professional:** Database tool window → `+` → Data Source → PostgreSQL → point
at the containerized instance (host `localhost`, mapped port).

**Community:** no Database tool window. Use the Terminal tool window:

- `psql "postgresql://<user>:<password>@localhost:<port>/<db>"`, or
- `docker exec -it <container> psql -U <user> -d <db>` to connect inside the
  running container.

## Debugging inside Docker

- **Professional:** use the Docker run configuration's Debug button, or Run →
  Attach to Process if the container exposes a debug port.
- **Community:** debug the app locally in PyCharm's debugger against a
  containerized dependency (e.g., PostgreSQL in Docker, app process running
  locally), instead of debugging inside the app container.

## When giving a hands-on task

- State the exact Run/Debug configuration name, type, and field values needed —
  not only the terminal command.
- If a feature is Professional-only, immediately give the labeled Community
  terminal-based equivalent.
- Keep instructions valid for both editions and both chip architectures without
  extra edits from the learner.
