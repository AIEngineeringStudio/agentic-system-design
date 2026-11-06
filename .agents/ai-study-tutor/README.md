# AI Study Tutor — Portable Agent Skill

A **case-first, hands-on, visual** solution-architecture tutor packaged
according to
the [Agent Skills specification](https://agentskills.io/specification).

The package separates **teaching behavior** from **case-specific knowledge**. It
contains a 73-case, nine-module Agentic AI system-design curriculum with 16
recommended deep dives. It is **not** a course with assessments, quizzes or a
fixed weekly timetable.

## What is included

```text
ai-study-tutor/
|
+-- SKILL.md                        # Activation, routing and default behavior
+-- README.md                       # Instructions for humans
+-- cases.json                      # Machine-readable 73-case catalog
+-- references/
|   +-- case-catalog.md            # Lightweight ID/name -> module index
|   +-- teaching-method.md         # Generic progressive teaching stages
|   +-- architecture-templates.md  # Solid-line ASCII diagrams and choices
|   +-- standards-and-sources.md   # Official protocol/spec links
|   +-- module-01-agent-fundamentals.md
|   +-- module-02-mcp.md
|   +-- module-03-rag-memory.md
|   +-- module-04-orchestration.md
|   +-- module-05-generative-ui.md
|   +-- module-06-multi-agent-a2a.md
|   +-- module-07-security.md
|   +-- module-08-operations.md
|   +-- module-09-advanced-ai.md
+-- assets/
|   +-- example-design.md          # Worked design #36 in six stages
|   +-- architecture-checklist.md  # Optional tutor-only production reference
+-- scripts/
|   +-- validate_skill.py          # Offline structural validator
+-- tests/
    +-- tutor-behavior-cases.md     # Acceptance scenarios, not learner quizzes
```

## Use

1. Unzip the package, preserving the `ai-study-tutor/` directory.
2. Copy the folder into the **Agent Skills location supported by your AI
   environment**. Different AI hosts have different skill installation and
   discovery workflows; this ZIP **does not auto-install** or enable the skill
   in this chat.
3. Have the AI environment discover `ai-study-tutor/SKILL.md` and allow it to
   read its local reference files.
4. Start with `Teach me system design #36` or
   `Design an AI support assistant from scratch`.
5. Say `continue`, `go deeper on authorization`, `show the ASCII sequence`,
   `build it`, or `show the entire production design` to control the level of
   detail.

Example requests:

- `Teach design #9. Start with the problem and basics. Use solid ASCII lines.`
- `Continue case #36 from requirements to the minimum architecture.`
- `Compare MCP Apps, AG-UI and A2UI using one real product example.`
- `Show the failure-recovery flow for #28. No quizzes.`
- `Design a custom customer support platform using tools, approvals and MCP.`
- `List all the 73 problems in the catalog.`

## Lazy-loading behavior

| User request              | Files expected                                                                             |
|---------------------------|--------------------------------------------------------------------------------------------|
| List cases                | `SKILL.md`, `references/case-catalog.md`                                                   |
| Teach #36                 | Above + `teaching-method.md` + `module-05-generative-ui.md`                                |
| Continue #36              | Reuse already loaded module and conversation state, if retained                            |
| Compare UI technologies   | `module-05-generative-ui.md`; `standards-and-sources.md` if up-to-date verification needed |
| Teach #43                 | `teaching-method.md` + `module-06-multi-agent-a2a.md`                                      |
| Ask for full architecture | Relevant module + `architecture-templates.md`                                              |
| Unlisted design           | Pick one primary module, read a second only as needed                                      |

Lazy loading means **the instructions direct the agent to read files on demand
**. It is not a cryptographic isolation feature and cannot force a host to
implement reading or persistent session state.

## Progressive explanations

**Default:** problem → just-in-time basics → minimal ASCII architecture →
working mock → production evolution → reusable patterns.

If you request the final design immediately, the tutor should provide it. No
forced checkpoints, quizzes, grades, homework or mock interviews. Program tests
in hands-on examples validate software only.

## Validation

```sh
python3 ai-study-tutor/scripts/validate_skill.py
```

Requires Python standard library only. This validator checks the package
structure, frontmatter shape, 73-case mapping, 16 anchors, 9 module coverage and
basic reference-path consistency. It **does not prove** an AI host will obey the
skill; manual behavior cases are listed in `tests/tutor-behavior-cases.md`.

## Maintenance

- To add or edit a case, update `cases.json`, the lightweight `case-catalog.md`
  entry, and its single module reference. Keep titles/IDs consistent.
- For protocol changes, update the relevant module and
  `standards-and-sources.md` after checking official specifications. Avoid
  coupling all modules to SDK-specific code.
- Preserve no-quizzes and requirement-first rules in the core `SKILL.md`. Any
  module-specific note must not override them.
- The curriculum and teaching content are an original synthesis guided by the
  user's attached system-design preparation document; it is not an industry
  certification or vendor standard.
