# Agent Instructions

This is a learning workspace. Its purpose is to teach the user concepts, tools,
and technologies — not just to write production code for them.

## Skill routing

Workspace skills live directly under `.agents/<skill-name>/SKILL.md`.

When the user asks to learn, understand, study, or be taught something, use the
skills in `.agents/`:

- Always load **`first-principles-learning`** for any learning request. It
  defines the learner profile (non-native English speaker, visual/bulleted
  learner, hands-on learner, Intel + Apple Silicon Macs), the teaching
  principles (one concept at a time, checks for understanding, professional
  articulation), and the per-concept session flow.
- Additionally, load **`tech-stack-curriculum`** when the topic is part of the
  workspace technology stack: Python, `uv`, `.env`/`python-dotenv`,
  `pydantic-settings`, Agentic AI, MCP, FastMCP, FastAPI, Docker, or PostgreSQL.
  It defines the topic list, teaching sequence, and
  versioning/containerization/configuration standards for that stack.
- If the user asks about a technology outside this stack, still apply
  `first-principles-learning` with any relevant domain skill; do not force-fit
  `tech-stack-curriculum` rules onto unrelated technologies.
- Additionally, load **`pycharm-workflow`** whenever a hands-on task must be
  run, debugged, or configured in the PyCharm IDE. It defines the required
  plugins, Python/`uv` interpreter setup, and Run/Debug configurations for both
  PyCharm Professional (Apple Silicon Mac) and PyCharm Community (Intel Mac).
- Additionally, load **`design-pattern-tutor`** for learning, comparing, or
  practicing software design patterns, pattern selection, and learning-focused
  design reviews. It covers object-oriented, architectural, data, messaging,
  distributed, and concurrency topics through changing requirements,
  refactoring, tests, and trade-offs. Use `first-principles-learning` alongside
  it, and load `tech-stack-curriculum` when implementing examples in Python or
  another workspace-stack technology. Load only the topic references needed
  for the current lesson.
- Additionally, load **`system-design-tutor`** when the user requests system
  design teaching, a worked architecture, a case comparison, a distributed-
  systems pattern, or a solution-architect review. Use
  `first-principles-learning` alongside it for learning requests, and load only
  the relevant module and references for the requested case.

When the user asks for documentation, a guide, or learning material in HTML
format, load **`html-documentation`**. It requires a single self-contained,
light-themed, PDF-friendly HTML file and a complete-source verification before
delivery. Apply it together with any relevant learning or technology-stack
skills above.

When creating or reorganizing technical documentation, tutorials, reference
guides, or engineering explanations in Markdown, load **`technical-docs-styling`**
(`.agents/technical-docs-styling/SKILL.md`) for content structure,
learning design, accessibility, and scannability. Apply it together with
**`markdown-authoring`** (`.agents/markdown-authoring/SKILL.md`) for
general Markdown conventions and print-friendly source formatting.

Load **`markdown-authoring`** whenever creating or revising Markdown documents
in this workspace, including when a specialized skill is also required.

When asked to create, regenerate, export, render, or convert a Markdown document
to PDF, load **`pdf-skill`**
(`.agents/pdf-skill/SKILL.md`) and follow the shared PDF theme and
validation workflow. Also load **`markdown-authoring`** for the source Markdown
and **`technical-docs-styling`** when the document is technical documentation,
a tutorial, reference guide, or learning material.

### Learning mode and implementation stage

- Use the modes defined in `first-principles-learning`: interactive lessons
  pause after one concept; requested guides cover the complete requested scope;
  quick clarifications receive a focused answer. A guide request takes
  precedence over interactive pacing, while retaining the learner's preferred
  language, examples, and visuals.
- Use the stages defined in `tech-stack-curriculum`: begin with a minimal
  concept exercise; apply production requirements in a production extension once
  its prerequisites are understood. Docker and typed configuration must not
  become prerequisites for unrelated beginner exercises. PyCharm setup must
  follow the selected stage.

## When adding new skills

- Keep skills single-purpose: one skill for teaching style/pedagogy, separate
  skills for domain-specific curricula.
- Update this routing section whenever a new skill is added, so it stays the
  single place that explains which skill(s) apply to which request.

## Workspace boundary

- Always create, read, and edit files inside this project directory only. Never
  read or write files outside this workspace.
- If a task requires a change outside the workspace (e.g., global config,
  another repository, system-level setup), do not attempt it directly. Instead:
    1. Create the required file(s) inside this workspace (e.g., under a clearly
       named folder such as `external-changes/`).
    2. Document, in a comment or an accompanying note, the exact purpose of each
       file and precisely where and how it should be applied outside the
       workspace.
    3. Explicitly call out this requirement in the response to the user — do not
       bury it — so it is not missed.
