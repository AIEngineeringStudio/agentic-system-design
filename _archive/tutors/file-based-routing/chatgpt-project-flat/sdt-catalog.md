# AI Study Tutor — 73-problem case catalog

**Purpose:** Filename-based router for a flat ChatGPT Project Source collection.
This is an index, not the teaching method. Use exact names/IDs. A ★ means one of
the 16 recommended deep dives. An `anchor-file` entry is optional, and only
eight anchors have standalone deep-dive reference files in this compact package.

**Routing:** Find the case, use the `module-file` named here, and optionally
retrieve its `anchor-file`. Never assume a directory path is available; all
source files are siblings. Do not load all modules to answer one design. Project
retrieval is best-effort, not guaranteed strict lazy loading.

|  # | Design problem                               | module-file                           | anchor-file                                            |
|---:|----------------------------------------------|---------------------------------------|--------------------------------------------------------|
| 01 | ★ FAQ support assistant                      | `sdt-module-01-agent-fundamentals.md` | `sdt-anchor-01-faq-support-assistant.md`               |
| 02 | Support-ticket triage and routing            | `sdt-module-01-agent-fundamentals.md` | —                                                      |
| 03 | ★ Order-status tool agent                    | `sdt-module-01-agent-fundamentals.md` | —                                                      |
| 04 | Document intake and extraction               | `sdt-module-01-agent-fundamentals.md` | —                                                      |
| 05 | Read-only analytics copilot                  | `sdt-module-01-agent-fundamentals.md` | —                                                      |
| 06 | Research report generator                    | `sdt-module-01-agent-fundamentals.md` | —                                                      |
| 07 | Email draft-and-send assistant               | `sdt-module-01-agent-fundamentals.md` | —                                                      |
| 08 | Goal-to-task planning assistant              | `sdt-module-01-agent-fundamentals.md` | —                                                      |
| 09 | ★ Local ticket-lookup MCP server             | `sdt-module-02-mcp.md`                | `sdt-anchor-09-local-ticket-lookup-mcp-server.md`      |
| 10 | Remote CRM MCP server                        | `sdt-module-02-mcp.md`                | —                                                      |
| 11 | MCP tool gateway                             | `sdt-module-02-mcp.md`                | —                                                      |
| 12 | Internal knowledge exposed as MCP resources  | `sdt-module-02-mcp.md`                | —                                                      |
| 13 | Reusable MCP prompt catalog                  | `sdt-module-02-mcp.md`                | —                                                      |
| 14 | ★ Enterprise MCP authorization broker        | `sdt-module-02-mcp.md`                | —                                                      |
| 15 | Multi-tenant MCP service                     | `sdt-module-02-mcp.md`                | —                                                      |
| 16 | Scalable MCP catalog and lookup              | `sdt-module-02-mcp.md`                | —                                                      |
| 17 | Long-running report via MCP Tasks            | `sdt-module-02-mcp.md`                | —                                                      |
| 18 | ★ Document Q&A with RAG                      | `sdt-module-03-rag-memory.md`         | `sdt-anchor-18-document-q-a-with-rag.md`               |
| 19 | Permission-aware enterprise search           | `sdt-module-03-rag-memory.md`         | —                                                      |
| 20 | Hybrid search and reranking                  | `sdt-module-03-rag-memory.md`         | —                                                      |
| 21 | ★ Customer 360 evidence assistant            | `sdt-module-03-rag-memory.md`         | —                                                      |
| 22 | Long-term assistant memory                   | `sdt-module-03-rag-memory.md`         | —                                                      |
| 23 | Multilingual policy assistant                | `sdt-module-03-rag-memory.md`         | —                                                      |
| 24 | Near-real-time knowledge indexing            | `sdt-module-03-rag-memory.md`         | —                                                      |
| 25 | Evidence verification agent                  | `sdt-module-03-rag-memory.md`         | —                                                      |
| 26 | ★ IT incident investigator                   | `sdt-module-04-orchestration.md`      | —                                                      |
| 27 | Plan-execute research workflow               | `sdt-module-04-orchestration.md`      | —                                                      |
| 28 | ★ Refund approval agent                      | `sdt-module-04-orchestration.md`      | `sdt-anchor-28-refund-approval-agent.md`               |
| 29 | Supplier onboarding agent                    | `sdt-module-04-orchestration.md`      | —                                                      |
| 30 | Parallel contract comparison                 | `sdt-module-04-orchestration.md`      | —                                                      |
| 31 | Event-triggered operations assistant         | `sdt-module-04-orchestration.md`      | —                                                      |
| 32 | Large batch classification agent             | `sdt-module-04-orchestration.md`      | —                                                      |
| 33 | Crash-recoverable agent runtime              | `sdt-module-04-orchestration.md`      | —                                                      |
| 34 | ★ AI sales dashboard from structured answers | `sdt-module-05-generative-ui.md`      | —                                                      |
| 35 | Conversational configuration wizard          | `sdt-module-05-generative-ui.md`      | —                                                      |
| 36 | ★ Expense-analysis MCP App                   | `sdt-module-05-generative-ui.md`      | `sdt-anchor-36-expense-analysis-mcp-app.md`            |
| 37 | Ticket-approval MCP App                      | `sdt-module-05-generative-ui.md`      | —                                                      |
| 38 | ★ Live incident console with AG-UI           | `sdt-module-05-generative-ui.md`      | `sdt-anchor-38-live-incident-console-with-ag-ui.md`    |
| 39 | Declarative A2UI request form                | `sdt-module-05-generative-ui.md`      | —                                                      |
| 40 | Portable UI comparison lab                   | `sdt-module-05-generative-ui.md`      | —                                                      |
| 41 | Enterprise agent cockpit                     | `sdt-module-05-generative-ui.md`      | —                                                      |
| 42 | ★ Supervisor and specialist investigators    | `sdt-module-06-multi-agent-a2a.md`    | —                                                      |
| 43 | ★ Remote fraud specialist via A2A            | `sdt-module-06-multi-agent-a2a.md`    | `sdt-anchor-43-remote-fraud-specialist-via-a2a.md`     |
| 44 | Multi-vendor agent broker                    | `sdt-module-06-multi-agent-a2a.md`    | —                                                      |
| 45 | Long-running A2A research task               | `sdt-module-06-multi-agent-a2a.md`    | —                                                      |
| 46 | Customer-service handoff network             | `sdt-module-06-multi-agent-a2a.md`    | —                                                      |
| 47 | Multi-agent peer review                      | `sdt-module-06-multi-agent-a2a.md`    | —                                                      |
| 48 | Cross-organization procurement assistants    | `sdt-module-06-multi-agent-a2a.md`    | —                                                      |
| 49 | Enterprise agent directory                   | `sdt-module-06-multi-agent-a2a.md`    | —                                                      |
| 50 | ★ Injection-resistant knowledge assistant    | `sdt-module-07-security.md`           | —                                                      |
| 51 | Central policy engine for agent actions      | `sdt-module-07-security.md`           | —                                                      |
| 52 | Delegated identity across MCP                | `sdt-module-07-security.md`           | —                                                      |
| 53 | Computer-use assistant sandbox               | `sdt-module-07-security.md`           | —                                                      |
| 54 | Sensitive-document AI workspace              | `sdt-module-07-security.md`           | —                                                      |
| 55 | Multi-tenant agent platform                  | `sdt-module-07-security.md`           | —                                                      |
| 56 | Auditable payment-operations copilot         | `sdt-module-07-security.md`           | —                                                      |
| 57 | Agent supply-chain security                  | `sdt-module-07-security.md`           | —                                                      |
| 58 | ★ Agent tracing and evaluation dashboard     | `sdt-module-08-operations.md`         | —                                                      |
| 59 | Grounded-answer regression suite             | `sdt-module-08-operations.md`         | —                                                      |
| 60 | Model gateway and fallback                   | `sdt-module-08-operations.md`         | —                                                      |
| 61 | High-load agent admission control            | `sdt-module-08-operations.md`         | —                                                      |
| 62 | Replay-safe external actions                 | `sdt-module-08-operations.md`         | —                                                      |
| 63 | Safe prompt and agent rollout                | `sdt-module-08-operations.md`         | —                                                      |
| 64 | Agent service SLO and on-call                | `sdt-module-08-operations.md`         | —                                                      |
| 65 | Multi-region agent disaster recovery         | `sdt-module-08-operations.md`         | —                                                      |
| 66 | Browser-based travel-admin agent             | `sdt-module-09-advanced-ai.md`        | —                                                      |
| 67 | Realtime voice support assistant             | `sdt-module-09-advanced-ai.md`        | —                                                      |
| 68 | Visual claims-inspection assistant           | `sdt-module-09-advanced-ai.md`        | —                                                      |
| 69 | Code-editing agent in sandbox                | `sdt-module-09-advanced-ai.md`        | —                                                      |
| 70 | Agent Skills registry and discovery          | `sdt-module-09-advanced-ai.md`        | —                                                      |
| 71 | AI workflow builder with visual steps        | `sdt-module-09-advanced-ai.md`        | —                                                      |
| 72 | Code-and-data analysis workspace             | `sdt-module-09-advanced-ai.md`        | —                                                      |
| 73 | ★ Unified enterprise agentic platform        | `sdt-module-09-advanced-ai.md`        | `sdt-anchor-73-unified-enterprise-agentic-platform.md` |

## Module names

| Module | Focus                                                 | Case range |
|--------|-------------------------------------------------------|------------|
| 01     | Agent fundamentals and application patterns           | #1–#8      |
| 02     | MCP tools, data access and remote integrations        | #9–#17     |
| 03     | RAG, context engineering and memory                   | #18–#25    |
| 04     | Agent orchestration, workflows and durable state      | #26–#33    |
| 05     | Generative UI, MCP Apps, AG-UI and A2UI               | #34–#41    |
| 06     | Multi-agent systems and A2A interoperability          | #42–#49    |
| 07     | Security, identity and enterprise architecture        | #50–#57    |
| 08     | Evaluation, observability, reliability and operations | #58–#65    |
| 09     | Emerging and advanced agentic systems                 | #66–#73    |

## Routing precedence

1. An explicit **AI design #N** maps to this catalog.
2. A named case maps to its title here, regardless of incidental terminology
   from another module.
3. General system design is distinct from this **AI** 73-case collection. For an
   ambiguous `#N`, establish which curriculum is intended from conversation
   context; if still unclear, ask one brief question.
4. For an unlisted design: identify the main architecture concern, route to the
   nearest module by its title, and label the problem **custom case**.
5. Cross-module concepts can be explained briefly; retrieve another module only
   when the current requested depth needs it.
6. `concept-protocol-boundaries.md` is optional for comparisons across MCP / MCP
   Apps / AG-UI / A2UI / A2A / Skills. `concept-production-controls.md` is
   optional for production or security deep dives.
7. If the exact module source is not available, say it cannot be retrieved; do
   not invent its content or silently substitute unrelated modules.
