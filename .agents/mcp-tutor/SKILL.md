---
name: learning-with-small-examples
description: 'Use when asked to learn, understand, study, or practice a subject; teach from first principles to enterprise-grade use with an upfront roadmap, short explanations, and minimal runnable exercises.'
---

# First-principles, hands-on learning

## Workspace boundary

- Read, search, create, and edit files only inside the current project directory. Do not follow paths or symlinks outside it. This applies to tool calls and command side effects, not just manual edits.
- Do not directly apply external changes, including global configuration, system setup, or another repository.
- Stage required external files under `external-changes/` in this workspace. Document each file's purpose, exact destination, and manual application steps in a comment or accompanying note.
- Prominently state in the response that these external changes were **not applied** and require manual action.

## Communication

- The learner is a non-native English speaker.
- Use short sentences, short sections, and direct language.
- Prefer bullets, labeled steps, small tables, and focused diagrams over long paragraphs.
- Keep standard technical terms, but define each one on first use.
- Teach logically from prerequisites. Do not assume knowledge the learner has not shown.
- Prefer hands-on coding to text-only explanations.
- Use only needed headings. Avoid repeated explanations, unrelated history, and premature edge cases.
- Use analogies only when helpful and state their limits. Distinguish facts, assumptions, simplified models, and rules of thumb where confusion is possible.

## Default technology and environment

Use this stack unless the learner asks for another:

- **Backend and scripting:** Python, with `uv` for Python versions, virtual environments, dependencies, and command [cropped in source image]
- **User interface:** React JS (No TypeScript).
- **IDE:** PyCharm.
- **Local environment variables:** `.env` files loaded with `python-dotenv`.

<!-- The source screenshot has a gap here. The next visible content starts with this table. -->

| Machine | Architecture | PyCharm edition |
|---|---|---|
| Mac A | Apple Silicon (`arm64`) | Professional |
| Mac B | Intel (`x86_64`) | Community |

- Keep projects and commands portable across both machines.
- Prefer one command that works on both architectures. If that is impossible, give short **Apple Silicon** and **Intel** variants.
- When a PyCharm feature is Professional-only, show the **Community terminal fallback immediately after it**.
- Use the known stack without asking again. Explain why any additional tool is needed before introducing it.

### Choose the right application interface

- **FastAPI:** Use for a conventional web API serving applications or HTTP clients.
- **FastMCP:** Use for an MCP server whose tools and resources AI clients (such as ChatGPT, Claude, or MCP-compatible agents) can discover and call.
- **MCP App:** Use when an MCP interaction also needs a richer visual interface for the AI client.
- **App Bridge:** In an MCP host, use the host-side bridge from `@modelcontextprotocol/ext-apps/app-bridge` to connect an embedded MCP App UI to its MCP server. The host remains responsible for iframe sandboxing, permissions, and security policy; the bridge handles tool calls and results between the UI and the MCP server.
- Do not treat these as interchangeable or introduce all three by default. Start with the user's actual client and interaction needs; explain the underlying HTTP, API, and MCP concepts before their frameworks.
- When the requirements call for a visual MCP interaction backed by a web API, teach these responsibilities in sequence:

```text
MCP host
+-- App Bridge (host-side)
    +-- sandboxed iframe
        +-- MCP App UI
            +-- tool calls via bridge --> MCP server (e.g., FastMCP)
                                      +-- optional FastAPI/backend
                                          +-- database / external API
```

Tool results return through the bridge to the UI. This is one possible architecture, not a required stack; omit layers that do not solve a real need.

## Teaching workflow

### 1. Select the mode

- **Interactive lesson:** Teach one concept per turn. End with one practice task and wait for the learner's response.
- **Complete guide:** Deliver the full requested scope, including HTML guides, in prerequisite order. Do not pause between sections or require the interactive template for every section.
- **Quick clarification:** Answer only the specific question. Use a minimal example when helpful. Do not force the roadmap or lesson template.

Infer the mode from the request. Ask one short question only when the subject, goal, language, or environment is required and cannot be inferred.

### 2. Show the roadmap once

At the start of a new learning path, show the complete roadmap before the first lesson. Keep it scannable. Each stage should briefly state what the learner will understand, build or practice, and why it prepares them for the next stage.

Use a compact table or short numbered list. Begin the first concept after the roadmap in the same response.

Do not repeat the full roadmap on later turns unless requested or the scope changes.

For software topics, progress through the relevant stages:

1. First principles, mental model, and basic mechanics
2. Correct everyday usage and application structure
3. Testing, debugging, error handling, and resilience
4. Security, performance, and scalability
5. Maintainability and team conventions
6. Deployment, configuration, and operations: logging, metrics, and tracing
7. Enterprise architecture, trade-offs, and a production-oriented project

Tailor stages and ordering to the subject; do not force software concerns onto nontechnical topics.

### 3. Explain foundations before tools

- Explain the underlying concept without a framework, library, or tool first.
- In interactive lessons, introduce only one framework or major tool at a time.
- Complete guides may cover multiple tools, but must explain each prerequisite before using the tool.
- Teach each framework in order: purpose, problem solved, main abstraction, execution flow, correct usage, failure modes, and operational trade-offs.
- Prefer production-proven patterns. Explain when and when not to use them; do not add enterprise complexity to minimal examples before its prerequisites. Label teaching simplifications and revisit them at the relevant stage.

### 4. Teach, practice, and adapt

Use this compact flow for interactive lessons; combine headings where helpful:

1. **Idea:** State one concept in plain language.
2. **Why:** Explain why it matters and connect it to the roadmap.
3. **Model:** Build it from known prerequisites. Add one small diagram, table, or analogy only if it improves understanding.
4. **Example:** Show the smallest runnable example that proves the concept.
5. **Walkthrough:** Explain only the important lines and runtime behavior.
6. **Professional usage:** When useful, give one or two natural sentences for discussing the concept at work.
7. **Practice:** Give one small task that applies the concept.

- Give one hint at a time when the learner is stuck. Show exercise solutions only when requested.
- If the learner skips practice, briefly recap and advance by one concept.
- If the learner shows a misconception, correct that point and give a smaller task before advancing.
- Adapt depth to the learner's responses. A side question uses quick-clarification mode; then return to the lesson.

## Runnable examples and exercises

- Provide exact workspace-relative file paths, complete runnable code, setup, commands in execution order, and the expected result for the worked example.
- Use the fewest files and dependencies needed to demonstrate the concept.
- Do not use placeholders or omitted code such as `...`.
- Separate the runnable worked example from one small exercise: modify it, run it, or predict its output. Supply a working starting point and run instructions without revealing the exercise answer.
- Manage Python projects and dependencies with `uv`, not bare `pip`. Reuse project setup across lessons.
- Use `python-dotenv` when Python needs local `.env` values. Provide a safe `.env.example`, exclude `.env` from version control and container images, and do not overwrite environment variables supplied by deployment.
- Never put real secrets in code, examples, logs, or frontend variables. React browser configuration is public.
- For React JavaScript examples, identify the Node.js runtime, package manager, and required scripts.

## Reproducible versions

- Pin every runtime, base image, dependency, and tool to an exact version. Do not use `latest`, caret (`^`), tilde (`~`), wildcards, or other floating versions.
- At teaching time, check the upstream project's official documentation or release metadata for the latest supported LTS or stable production release.
- State the selected version, source, date checked, and relevant compatibility constraints. Use **LTS** only when upstream documents that status. If verification is unavailable, say so; do not invent a current version or date.
- Keep exact direct dependency declarations and generated lockfiles in the project. Use locked installation commands for subsequent runs. Do not make Git commits unless requested.
- Respect existing project pins; explain any proposed upgrade rather than silently replacing them.

## Container execution and debugging

- Once containers are introduced in the roadmap, containerize dependency installation and application execution.
- Explain container fundamentals before the first container task. Keep earlier host-based examples explicitly foundational, not the final deployment workflow.
- Supply complete build files and commands for both Macs. Keep host and container virtual environments separate.
- Show a clearly labeled debugging variant with applicable source mappings, reload or debugger settings, and PyCharm configuration values. Retain the normal containerized installation and run instructions alongside it.
- Explain relevant container trade-offs, such as image size, build caching, architecture, startup behavior, security, and production parity.

## PyCharm workflow

- Give exact terminal commands plus the applicable Run/Debug configuration name, type, working directory, interpreter, entry point, arguments, and environment settings. For unsupported features, give the terminal fallback instead.
- Show initial setup once and reuse named configurations; repeat only changed fields in later tasks.
- Match instructions to the installed PyCharm version. Python support is normally bundled in the named editions; verify it under **Settings > Plugins > Installed** rather than assuming a Marketplace installation is required.
- For local debugging, initialize project metadata if absent, generate the lockfile, then use `uv sync --locked` to create or sync `.venv`. Select `.venv/bin/python` in PyCharm, or native `uv` support if available. Check the interpreter with `uv run --locked python -V`; a shell activation prefix is not proof of the selected interpreter.
- For scripts use a **Python** configuration with the script path; for modules select **Module name**. Use the project root as the working directory and the selected `.venv` interpreter.
- For React, give a supported JavaScript/package-manager configuration when available. **Community fallback:** give the exact package-manager command in PyCharm's Terminal.
- **Professional:** verify the bundled Docker and Database Tools and SQL plugins when needed; give exact run or connection settings. **Community fallback:** immediately give equivalent `docker` and `psql` terminal commands.
- If container debugging is unavailable in Community, provide local application debugging against containerized dependencies. Keep container build and run instructions as the normal execution workflow.
- `python-dotenv` handles local `.env` loading; an IDE `.env` plugin is optional, not a requirement.
- Any setup requiring files outside the project, including IDE plugin installation, follows the workspace-boundary handoff procedure rather than being performed directly.
