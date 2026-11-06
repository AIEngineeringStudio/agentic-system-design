# AI Study Tutor — Flat ChatGPT Project Sources edition

This folder contains **23 independent files in one flat directory**. It converts
the directory-based AI Study Tutor into a **Project Instructions + source-file
routing** package for ChatGPT web Projects, where a directory tree is not
available as an installed Agent Skill.

## Important setup distinction

- `PROJECT_INSTRUCTIONS.txt` contains the text to **copy and paste manually**
  into **ChatGPT Project settings → Project instructions**.
- `SKILL.md` is a **reference source** inside the Project, not an automatically
  installed executable skill.
- `sdt-catalog.md`, nine `sdt-module-*.md` files, eight `sdt-anchor-*.md` files,
  and two `concept-*.md` files are **Project Sources**.
- The ZIP is a transport package. **Unzip it before uploading the individual
  files.** Uploading the ZIP as one Project Source does not mean ChatGPT will
  discover and route the contents as individual sources.
- Routing is **best effort based on instructions and source retrieval**, not
  guaranteed selective filesystem loading or guaranteed retrieval of only the
  named file.

## Quick setup

1. Create or open the ChatGPT Project that will host this tutor.
2. Copy the complete text of `PROJECT_INSTRUCTIONS.txt` into the project's *
   *Project settings → Project instructions**.
3. Add the remaining `.md` sources individually to the Project Sources
   collection. You may omit the eight optional anchor files if you need a
   smaller upload, but keep the relevant module for every case you intend to
   teach.
4. Ask: **
   `Teach AI system design #36, starting with the real problem. Do not reveal the full architecture yet.`
   **
5. Continue naturally: `continue`, `show the minimal ASCII diagram`,
   `build a local mock`, `go deeper on authorization`, or
   `show full production design`.

ChatGPT Projects allow files and project-specific instructions to provide
context; availability and uploaded-file counts depend on the user's plan and
workspace configuration. Official
documentation: https://help.openai.com/en/articles/10169521-projects-in-chatgpt

## Flat file map

| File(s)                               | Purpose                                                          | Required for                             |
|---------------------------------------|------------------------------------------------------------------|------------------------------------------|
| `PROJECT_INSTRUCTIONS.txt`            | Copy-paste activation and routing instructions                   | Project setup (paste, not merely upload) |
| `SKILL.md`                            | Full progressive teaching and safe routing behavior              | All lessons                              |
| `sdt-catalog.md`                      | Maps all 73 cases to module / anchor filenames                   | Numbered or named case requests          |
| `sdt-module-01-agent-fundamentals.md` | Cases #1–#8                                                      | Foundational AI designs                  |
| `sdt-module-02-mcp.md`                | Cases #9–#17                                                     | MCP and remote tools                     |
| `sdt-module-03-rag-memory.md`         | Cases #18–#25                                                    | Retrieval, evidence, memory              |
| `sdt-module-04-orchestration.md`      | Cases #26–#33                                                    | State, approvals and workflows           |
| `sdt-module-05-generative-ui.md`      | Cases #34–#41                                                    | GenUI, MCP Apps, AG-UI and A2UI          |
| `sdt-module-06-multi-agent-a2a.md`    | Cases #42–#49                                                    | Multi-agent and A2A                      |
| `sdt-module-07-security.md`           | Cases #50–#57                                                    | Enterprise controls                      |
| `sdt-module-08-operations.md`         | Cases #58–#65                                                    | Evaluation, tracing and reliability      |
| `sdt-module-09-advanced-ai.md`        | Cases #66–#73                                                    | Advanced architectures and platform      |
| `sdt-anchor-*.md` (8 files)           | Detailed case references, progressively revealed                 | Optional deep dives                      |
| `concept-protocol-boundaries.md`      | Comparison of MCP / MCP Apps / AG-UI / A2UI / A2A / Skills       | Cross-protocol questions                 |
| `concept-production-controls.md`      | Side-effect safety, authorization, evaluations and observability | Production deep dives                    |
| `README.md`                           | Human installation and usage guide                               | Setup only                               |

## Eight standalone anchor references

- `sdt-anchor-01-faq-support-assistant.md`
- `sdt-anchor-09-local-ticket-lookup-mcp-server.md`
- `sdt-anchor-18-document-q-a-with-rag.md`
- `sdt-anchor-28-refund-approval-agent.md`
- `sdt-anchor-36-expense-analysis-mcp-app.md`
- `sdt-anchor-38-live-incident-console-with-ag-ui.md`
- `sdt-anchor-43-remote-fraud-specialist-via-a2a.md`
- `sdt-anchor-73-unified-enterprise-agentic-platform.md`

The catalog preserves **16 recommended full-depth anchor designs**. Eight have
separate anchor source files in the compact flat package; the other eight can
still be taught in full from their module briefs. An anchor file is a tutor
reference, not an implemented or tested software system.

## Examples of instruction-based routing

| Request                          | Main source(s)                                                     | Tutor behavior                           |
|----------------------------------|--------------------------------------------------------------------|------------------------------------------|
| List all AI cases                | `sdt-catalog.md`                                                   | Show catalog only                        |
| Teach AI #9                      | `sdt-module-02-mcp.md`, optional #9 anchor                         | Requirements first; local MCP server     |
| Continue #9                      | Previous module and conversation                                   | Advance one meaningful stage, no quizzes |
| Teach AI #36                     | `sdt-module-05-generative-ui.md`, optional #36 anchor              | Expense analyst journey first            |
| Compare MCP Apps, AG-UI and A2UI | `concept-protocol-boundaries.md`                                   | Explain distinct architecture boundaries |
| Production controls for refunds  | `sdt-module-04-orchestration.md`, `concept-production-controls.md` | Server-side approval and idempotency     |
| Full AI #73 production design    | `sdt-module-09-advanced-ai.md`, optional #73 anchor                | Full end-to-end architecture on request  |

## Teaching behavior

This is **problem-first**, **progressive**, **hands-on**, **visual**, *
*architecture-focused**, and **no unrequested quizzes or assessments**. Use
basic English and ASCII diagrams with continuous `+ - |` box lines. Show
requirements, minimal design, local mock, production changes and architecture
trade-offs. If the user asks to jump to an implementation or final design,
comply rather than insisting on a staged lesson.

## Source maintenance

- Change a title/ID: update `sdt-catalog.md` and its single module file; rename
  an anchor file and catalog entry together if needed.
- Change teaching behavior: update `SKILL.md` and the pasted Project
  Instructions.
- Update version-sensitive protocol examples using official specifications. Do
  not claim that an optional MCP extension is universally supported.
- Each module source is independently readable; do not create nested folders or
  relative links when uploading to ChatGPT Projects.
- The flat edition is an original adaptation of the AI 73-problem curriculum
  developed earlier in this chat. The attached non-AI 73-problem interview plan
  is a **separate** curriculum and does not share case-number meanings.
