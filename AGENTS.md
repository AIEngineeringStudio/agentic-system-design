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
- Additionally, load **`ai-study-tutor`**
  (`.agents/ai-study-tutor/SKILL.md`) for practical AI solution-architecture
  learning: Agentic AI, agents and tools, MCP/MCP Apps, Generative
  UI/AG-UI/A2UI,
  A2A, RAG/context/memory, AI workflow orchestration, agent security,
  evaluation, observability, or the **AI 73-problem system-design curriculum**.
  This skill owns the AI case-study teaching method and module routing:
    1. Read its `SKILL.md` first. For a numbered AI case or catalog lookup,
       consult `references/case-catalog.md` for the case-to-module mapping.
    2. For an actual lesson, use `references/teaching-method.md` and load
       **only the selected** `references/module-NN-*.md`. Load another module
       only when the current design truly requires its concepts or the user
       explicitly asks for cross-module coverage.
    3. Load architecture templates, worked examples, and standards references
       only when that stage or request needs them. Never preload all nine
       modules.
    4. Teach **progressively**: real problem and requirements -> just-in-time
       basics -> simplest working architecture -> hands-on mock -> production
       evolution -> reusable patterns and trade-offs. Explain the rationale
       before adding complexity. Prefer continuous-line ASCII diagrams.
    5. **Never introduce quizzes, grades, homework, forced comprehension checks,
       or mock interviews** unless explicitly requested. Software tests for
       working examples are allowed; they do not assess the learner. Honor
       `continue`, `go deeper`, `build it`, `skip ahead`, and
       `show full design`.
    6. Keep existing learning context and the current stage when the user asks
       to continue. Do not claim persistent progress across conversations.
- Additionally, load **`system-design-tutor`** for **non-AI** system-design
  teaching, worked architectures, case comparisons, distributed-systems
  patterns, and solution-architect reviews. Use `first-principles-learning`
  alongside it for learning requests, and load only the relevant case module.
  For an AI-focused design, prefer `ai-study-tutor` instead of loading both
  full curricula; load a general system-design reference only if needed to
  explain a specific cross-domain decision.
- **Case-number disambiguation:** Both system-design curricula contain 73
  cases. Route `#N` to `ai-study-tutor` when the user explicitly mentions AI or
  the ongoing context is the AI curriculum; route to `system-design-tutor`
  when they name the general system-design curriculum. If neither is clear,
  ask which curriculum they mean rather than guessing.

When the user asks for documentation, a guide, or learning material in HTML
format, load **`html-documentation`**. It requires a single self-contained,
light-themed, PDF-friendly HTML file and a complete-source verification before
delivery. Apply it together with any relevant learning or technology-stack
skills above.

When creating or reorganizing technical documentation, tutorials, reference
guides, or engineering explanations in Markdown, load **`technical-docs-styling`
**
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

- Use the modes defined in `first-principles-learning` for general learning:
  interactive lessons pause after one concept; requested guides cover the
  complete requested scope; quick clarifications receive a focused answer. A
  guide request takes precedence over interactive pacing, while retaining the
  learner's preferred language, examples, and visuals.
- **AI architecture teaching precedence:** For requests routed to
  `ai-study-tutor`, its problem-first, six-stage progression takes precedence
  over generic per-concept pacing and any `first-principles-learning`
  comprehension-check routine. Continue using the general skill's clear
  language, accessible visuals and hands-on teaching principles, but do not
  require learner answers, quizzes or assessments. If the user explicitly asks
  for a complete design, deliver it in one response rather than stage-gating.
- **Stack curriculum boundary:** When an AI design uses Python, `uv`, FastAPI,
  FastMCP, Docker or PostgreSQL, also use relevant `tech-stack-curriculum`
  implementation and environment rules. Do not let its topic order replace the
  AI tutor's case-first teaching sequence; production-only setup should not be
  forced into a minimal mock build.
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
