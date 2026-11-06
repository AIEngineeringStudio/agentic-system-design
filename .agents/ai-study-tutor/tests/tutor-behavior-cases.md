# Tutor behavior acceptance scenarios (for maintainers, not learner assessments)

These are *software/agent behavior scenarios* that a maintainer can inspect. Do
not show them to a learner as questions, grades, tests, exercises, or homework.

| Input to tutor                                   | Files it should load                               | Expected response behavior                                                                          |
|--------------------------------------------------|----------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| `List the 73 problems`                           | `case-catalog.md` only                             | List/index cases. Do not load all modules.                                                          |
| `Teach me design #36`                            | `teaching-method.md`, `module-05-generative-ui.md` | Begin with user story and requirements, not full MCP Apps production design.                        |
| `Continue` after #36 Stage 1                     | Reuse module 05                                    | Introduce only necessary concepts at Stage 2. No quiz or forced checkpoint.                         |
| `Go deeper on MCP Apps sandbox`                  | Module 05 + official sources if needed             | Explain host/app isolation with focused ASCII flow.                                                 |
| `Show the complete architecture for #36 now`     | Module 05 + architecture templates                 | Bypass stage-by-stage withholding; provide full design.                                             |
| `Teach #9`                                       | Module 02                                          | Show local MCP server baseline before gateway and OAuth.                                            |
| `Teach #43`                                      | Module 06                                          | Identify independent agent boundary, Agent Cards and tasks.                                         |
| `Compare MCP Apps, AG-UI and A2UI`               | Module 05                                          | Treat three different concerns, not synonyms; warn on host support.                                 |
| `Design a custom account reconciliation agent`   | One relevant module, optionally second             | Label custom case, begin requirements, use fake records.                                            |
| `Please quiz me on idempotency`                  | Relevant module                                    | User explicitly requested quiz: permitted; no default assessment restriction.                       |
| `Build working HTML for a generative UI example` | Module 05                                          | Prefer self-contained, light, printable HTML and verify actual behavior if tooling permits.         |
| `Draw the flow`                                  | Current selected module                            | Use continuous solid-line ASCII, not dots, Mermaid or SVG.                                          |
| `Run production payment tool`                    | Relevant module                                    | Use mocks unless explicit authorization and safe capabilities exist; enforce service-side approval. |

## Manual reviewer checks

- Case IDs and module filenames match the shipped `cases.json` and
  `case-catalog.md`.
- “Continue” and “go deeper” preserve the current topic and do not inject
  irrelevant modules.
- The tutor adds requirements before naming Kafka/Kubernetes/vector DB/etc.
- The tutor does **not** ask the learner to answer a question before proceeding.
- Spec details are attributed to official sources when version-specific.
- Code is labeled as verified/runnable vs illustrative based on actual
  execution.
