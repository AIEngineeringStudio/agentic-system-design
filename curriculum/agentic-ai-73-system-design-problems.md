# Agentic AI Solution Architecture — 73 Real-World System Design Problems

**Updated:** November 6, 2026  
**Goal:** Breadth-first knowledge of production Agentic AI architectures,
learned through worked system-design cases and practical builds.  
**Style:** Case-first, visual, hands-on, concept-at-point-of-need. No isolated
theory chapters, quizzes, or fixed weekly schedule.

## 1. What this curriculum is

This adapts the structure of the supplied 73-problem system design plan. The
original is a systems / payments curriculum; this new one is a **separate
Agentic AI curriculum**. The 73 problems below are **design briefs with hands-on
scope and production constraints**, not 73 already solved implementations. We
can subsequently work each one into a complete guided design. Sixteen anchors
warrant full-depth treatment; the other 57 are pattern variations.

### Learning rules

1. **Start from a user requirement.** Do not start by naming a framework or
   protocol.
2. **Draw a minimal baseline first.** Add a framework, queue, protocol or store
   only when a constraint justifies it.
3. **Teach concepts at first use.** Define the term in one or two lines, show it
   on the diagram, then use it.
4. **Build something observable.** Every case includes a mock/local lab, request
   flow and expected behavior.
5. **Make it production-grade on paper.** Design authorization, failure states,
   quality, scaling, cost, monitoring and migration, even if the lab remains
   small.
6. **Compare credible options.** Identify the constraint, choose an architecture
   and state what would change the choice.
7. **Cover breadth, then depth.** The 16 anchors get full walkthroughs; lighter
   cases emphasize new decisions.
8. **Use safe practice systems.** Mock external business systems and sensitive
   data. Require explicit approval for high-impact actions.

### Coverage and scope

| Module                                                     |  Cases | Scope                                                                                                            |
|------------------------------------------------------------|-------:|------------------------------------------------------------------------------------------------------------------|
| 01 · Agentic AI fundamentals and application patterns      |      8 | Understand when a model, tool-using agent, or deterministic workflow is the right system boundary.               |
| 02 · MCP tools, data access and remote integrations        |      9 | Treat MCP as a protocol boundary; distinguish tools, resources, prompts, clients, hosts and extensions.          |
| 03 · RAG, context engineering and memory                   |      8 | Design information flow, source provenance and the boundary between conversation context and durable data.       |
| 04 · Agent orchestration, workflows and durable state      |      8 | Progress from single-agent execution to explicit workflows, state machines and failure recovery.                 |
| 05 · Generative UI, MCP Apps, AG-UI and A2UI               |      8 | Separate three concerns: what UI to render, how embedded views execute, and how frontends exchange agent events. |
| 06 · Multi-agent systems and A2A interoperability          |      8 | Use collaboration only where independent capabilities, ownership or task decomposition justify it.               |
| 07 · Security, identity and enterprise architecture        |      8 | Put trust boundaries and permission checks around data, tools, UI and external agents.                           |
| 08 · Evaluation, observability, reliability and operations |      8 | Make nondeterministic systems measurable, recoverable and supportable.                                           |
| 09 · Emerging and advanced agentic systems                 |      8 | Extend the standard architecture with multimodal, computer-use, skills, code execution and a platform capstone.  |
| **Total**                                                  | **73** | **16 recommended anchor deep dives**                                                                             |

### Standards vs implementations

| Layer                               | Learn and compare                                 | Practical boundary                                                                  |
|-------------------------------------|---------------------------------------------------|-------------------------------------------------------------------------------------|
| Agent execution                     | Agent loops, OpenAI Agents SDK, LangGraph         | Runtime and workflow control; **not** an interop protocol                           |
| Tool and data interoperability      | **MCP**                                           | Standardizes client/server access to tools, resources and prompts                   |
| Inline conversational UI            | **MCP Apps**                                      | Optional MCP extension delivering sandboxed app views in compatible hosts           |
| Agent ↔ first-party frontend        | **AG-UI**                                         | Standardized event stream / state updates, not a substitute for MCP tools           |
| Declarative generated UI            | **A2UI**                                          | UI as structured component data rendered by the host, not generated executable code |
| Independent agent ↔ agent           | **A2A**                                           | Remote agent capability discovery and task/artifact exchange                        |
| Reusable capability instructions    | **Agent Skills**                                  | SKILL.md packaging; a different concern from tool execution                         |
| Evaluation, security and operations | OWASP, OpenTelemetry, cloud architecture guidance | Cross-cutting practices, not alternatives to the above                              |

**Version warning:** MCP core and extensions evolve. The July 28, 2026
specification updates the core model; MCP Apps is an optional extension and
requires compatible host support. Likewise, A2A, AG-UI and A2UI have different
adoption and interoperability constraints. Treat a published specification as a
design target, **not** proof that your chosen product implements every
capability. Refer to official links in section 10.

## 2. The case-study method (apply to every problem)

| Step                          | Guided design / work product                                                                |
|-------------------------------|---------------------------------------------------------------------------------------------|
| 1. User journey               | Actors, task, outcome and explicit out-of-scope boundary                                    |
| 2. Requirements               | Correctness, security, latency, availability, quality, cost, throughput (in priority order) |
| 3. Basics just-in-time        | One-minute definition + why this case needs each new concept                                |
| 4. Trust and data flow        | What is source of truth? Who can see/act? Which data is untrusted?                          |
| 5. Interface contract         | API/tool schema, authorization, events, idempotency, cancellation and errors                |
| 6. Simplest acceptable design | ASCII component diagram and sequence of the happy path                                      |
| 7. Hands-on lab               | Small working mock with fixture data, visible requests/results                              |
| 8. Design choices             | Compare at least two valid options; choose by constraints and state drawbacks               |
| 9. Production evolution       | Prompt injection, tenant security, retries, checkpoints, telemetry, evals and budgets       |
| 10. Critical failures         | Duplicate calls, partial results, interrupted workflow, revoked access, stale data          |
| 11. Final design              | Updated ASCII architecture, owner boundaries, operational risks and cost drivers            |
| 12. Variants                  | How architecture changes with scale, compliance, latency or host capability                 |

**Visual package for each deep dive:** (a) baseline ASCII diagram, (b)production
ASCII diagram, (c) success/failure sequence, (d) state lifecycle, (e)decision
comparison. Optional static HTML visualizations are supplemental; the diagram
must remain readable in plain text.

**Working-lab standard:** Python agent service, TypeScript only where MCP UI SDK
requirements benefit from it, self-contained plain HTML/CSS/JS frontend,
SQLite/PostgreSQL for examples, mock external services, tests and Docker where
useful. All dependencies are replaceable; first explain the protocol before the
library.

## 3. Foundation concepts (introduced inside problems, not as lectures)

| Concept             | Meaning in one sentence                                                            | First case |
|---------------------|------------------------------------------------------------------------------------|------------|
| Model call vs agent | One model response differs from a controlled loop that may select tools and steps. | #1, #3     |
| Structured output   | A model output is checked against a data schema before code uses it.               | #2         |
| Tool calling        | The model proposes an action; application code decides whether/how it executes.    | #3         |
| Grounding and RAG   | Retrieve evidence from owned sources instead of assuming model recall is current.  | #1, #18    |
| Prompt injection    | Untrusted content attempts to act as trusted instructions.                         | #3, #50    |
| Idempotency         | Repeating a logical command does not create an extra business effect.              | #7         |
| Workflow state      | Durable facts about which steps ran and what may run next.                         | #8, #29    |
| MCP                 | A standardized contract between AI clients and external tool/data servers.         | #9         |
| OAuth delegation    | Limit calls to the signed-in user's approved scopes and resources.                 | #14        |
| Context engineering | Select, compress and order useful information inside model context limits.         | #18, #22   |
| Memory              | Persist relevant information beyond one request with lifecycle rules.              | #22        |
| Human-in-the-loop   | Explicit human approval or correction at defined trust boundaries.                 | #7, #28    |
| MCP Apps            | Sandboxed interactive HTML UI associated with MCP tools, in compatible hosts.      | #36        |
| AG-UI               | Structured streaming of agent lifecycle, content, tool and state events.           | #38        |
| A2UI                | Structured, declarative UI components rendered by a trusted host.                  | #39        |
| A2A                 | Remote agent-to-agent communication for tasks and artifacts.                       | #43        |
| Agent Skills        | SKILL.md-based reusable instruction and supporting-resource packages.              | #70        |
| Evaluation          | Measure task success, safety, grounding and regression with repeatable cases.      | #59        |
| Tracing             | Correlate model, tool, workflow and user interactions into one operation.          | #58        |
| Reliability         | Recover safely from timeout, crash, cancellation and duplicate delivery.           | #33, #62   |

## 4. Architecture map (orienting diagram)

```text
 User / Operator
      |
      v
 Web UI / chat / native host
      |      |             |
      |      | A2UI data   +-- MCP App (sandboxed HTML view)
      |      +-- rendered by host       [requires MCP Apps-capable host]
      |
  AG-UI events / other app transport
      |
      v
 Agent runtime + deterministic workflow
  planner, state, approvals, tool policy
      |                     |
      | MCP                 | A2A
      v                     v
 MCP client -> MCP server    Remote independent agent
      |                     |
  SaaS / APIs / search       tasks, artifacts
  records / business logic

 Cross-cutting: IAM, authorization, data policy, evaluations,
 traces, rate limits, audit, cost and disaster recovery.
```

This diagram shows **logical boundaries**, not a mandatory stack: for example,
an MCP App's UI communicates through its host bridge; AG-UI is not a required
part of MCP Apps. A2UI is a representation of UI, not the transport. Many cases
need only some of these layers.

## 5. The 73 system-design problems

Each case states the **problem**, the **basics to introduce when needed**, a *
*working lab**, a **production-level extension**, and the **architectural
judgment to practice**. `★` marks a recommended full-depth anchor.

### Module 01 — Agentic AI fundamentals and application patterns

*Goal: Understand when a model, tool-using agent, or deterministic workflow is
the right system boundary.*

#### 01. FAQ support assistant ★

**Problem:** Customers ask policy questions in plain English; responses should
stay inside approved information.

- **Basics at point of use:** Model request/response, system instructions,
  grounding, structured answers; an agent is not required for every AI task.
- **Build:** Build a chat endpoint against a small curated FAQ and return answer
  plus source IDs.
- **Production architecture:** Add refusal for missing evidence, content
  filtering, token budgets, trace IDs, and quality checks.
- **Key decision:** Retrieval-grounded answer vs free-form generation; simplest
  useful architecture.

#### 02. Support-ticket triage and routing

**Problem:** Classify a new ticket and route it to the correct queue without
taking arbitrary actions.

- **Basics at point of use:** Prompt vs classifier, schema-constrained output,
  confidence, deterministic routing, fallback.
- **Build:** Accept a ticket, emit category/priority JSON, and route to a mock
  queue.
- **Production architecture:** Validate schema, reject unknown queues, add human
  review for ambiguous cases, monitor misroutes.
- **Key decision:** Classification with rules vs a model; fail-safe fallbacks.

#### 03. Order-status tool agent ★

**Problem:** A user asks where an order is; data must come from the order
system, not model memory.

- **Basics at point of use:** Tool/function calling, typed inputs, model vs
  service responsibility, external data as untrusted input.
- **Build:** Implement `get_order_status(order_id)` and a single-agent tool
  loop.
- **Production architecture:** Bind order IDs to the authenticated user, limit
  tool scope, retry boundedly and audit access.
- **Key decision:** Direct API integration vs exposing an agent-callable tool.

#### 04. Document intake and extraction

**Problem:** Convert uploaded invoices into validated structured records.

- **Basics at point of use:** Multimodal input, extraction, JSON schema,
  validation, deterministic post-processing.
- **Build:** Extract supplier/date/total from sample PDFs or images into a local
  database.
- **Production architecture:** Duplicate detection, malware screening, PII
  retention controls, manual correction and batch retries.
- **Key decision:** One LLM call vs extract-validate-correct pipeline.

#### 05. Read-only analytics copilot

**Problem:** Business users ask natural language questions about a governed
dataset.

- **Basics at point of use:** Text-to-SQL, semantic layer, read-only access,
  query plans, execution limits.
- **Build:** Generate SQL against a small analytics DB and chart the result.
- **Production architecture:** Restrict tables/columns, enforce tenant filters
  server-side, set time/row limits, log SQL.
- **Key decision:** LLM-generated SQL vs fixed metrics API.

#### 06. Research report generator

**Problem:** An analyst wants a short brief grounded in multiple external or
supplied documents.

- **Basics at point of use:** Retrieval, citations, source ranking, synthesis,
  uncertainty.
- **Build:** Search a local document set, collect passages, and produce a cited
  report.
- **Production architecture:** Enforce source provenance, freshness checks,
  source isolation and reproducibility.
- **Key decision:** Single-shot summarization vs evidence-first pipeline.

#### 07. Email draft-and-send assistant

**Problem:** An assistant drafts a customer reply and sends only after explicit
user approval.

- **Basics at point of use:** Action vs suggestion, side effects, confirmation
  gates, idempotency.
- **Build:** Build draft, preview, approve and a simulated `send_email` action.
- **Production architecture:** Persist approval subject/body hash, protect
  recipient scope, deduplicate sends, audit.
- **Key decision:** Fully autonomous execution vs approval-gated action.

#### 08. Goal-to-task planning assistant

**Problem:** Turn a goal into steps, execute safe parts, and request permission
for risky steps.

- **Basics at point of use:** Planner/executor, bounded iterations, tool
  budgets, agent loop termination.
- **Build:** Plan a 3-step workflow and run with mock calendar/task tools.
- **Production architecture:** Detect infinite loops, enforce budgets, log
  decisions and escalate stalled runs.
- **Key decision:** Static workflow vs dynamic planning; when autonomy adds
  value.

### Module 02 — MCP tools, data access and remote integrations

*Goal: Treat MCP as a protocol boundary; distinguish tools, resources, prompts,
clients, hosts and extensions.*

#### 09. Local ticket-lookup MCP server ★

**Problem:** An AI host needs reusable access to ticket records from a local
service.

- **Basics at point of use:** MCP host/client/server roles, tools, schemas,
  JSON-RPC and local connectivity.
- **Build:** Implement a local MCP server with `list_tickets` and `get_ticket`
  tools; connect a client.
- **Production architecture:** Validate tool arguments, narrow data returned,
  add contract tests and host compatibility checks.
- **Key decision:** MCP server vs one application's private function tools.

#### 10. Remote CRM MCP server

**Problem:** Multiple assistant clients need access to a remote mock CRM.

- **Basics at point of use:** Remote MCP communication, authentication, tool
  discovery, error semantics, version compatibility.
- **Build:** Deploy a mock CRM MCP endpoint using the current official SDK.
- **Production architecture:** HTTPS, OAuth authorization, credential isolation,
  timeouts, quotas and rollout strategy.
- **Key decision:** Local vs remote MCP; session/state expectations by protocol
  version.

#### 11. MCP tool gateway

**Problem:** An enterprise has several MCP servers, duplicate tool names and
different security policies.

- **Basics at point of use:** Gateway, tool catalog, naming, policy enforcement,
  discovery and routing.
- **Build:** Aggregate three mock MCP services behind a gateway adapter.
- **Production architecture:** Avoid confused-deputy access, centrally authorize
  per tool, log provenance, handle server outages.
- **Key decision:** Direct client-to-server access vs governed gateway.

#### 12. Internal knowledge exposed as MCP resources

**Problem:** An assistant needs documents without treating every read as an
action.

- **Basics at point of use:** MCP tools vs resources vs prompts, resource
  addressing, context selection and access control.
- **Build:** Expose a versioned policy document as an MCP resource and fetch it
  in a host.
- **Production architecture:** Per-document ACL enforcement, cache invalidation,
  data classification and audit.
- **Key decision:** Resource vs tool vs retrieval API; least-context principle.

#### 13. Reusable MCP prompt catalog

**Problem:** Teams want repeatable workflow prompts distributed to compatible
clients.

- **Basics at point of use:** MCP prompt primitives, prompt parameterization,
  versioning and injection boundaries.
- **Build:** Publish two parameterized prompts for support and incident review.
- **Production architecture:** Curate ownership, tests, documentation, safe
  defaults and deprecation policy.
- **Key decision:** Protocol prompt vs application-owned prompt template.

#### 14. Enterprise MCP authorization broker ★

**Problem:** A user-approved agent must call SaaS APIs without obtaining broad
administrator rights.

- **Basics at point of use:** OAuth concepts, scopes, audience, delegated
  identity, consent and token exchange.
- **Build:** Protect a mock CRM MCP tool with scoped access and per-user grants.
- **Production architecture:** Block token passthrough, tenant leakage, scope
  escalation and confused-deputy abuse; record grants.
- **Key decision:** Service credentials vs user delegation vs brokered access.

#### 15. Multi-tenant MCP service

**Problem:** One tool endpoint serves multiple companies with strict data
separation.

- **Basics at point of use:** Tenant identity, authorization context, row-level
  controls and isolated storage.
- **Build:** Add tenant-scoped ticket data to an MCP server and negative
  cross-tenant tests.
- **Production architecture:** Separate tenant budgets, secrets, metrics,
  retention and admin operations.
- **Key decision:** Shared MCP endpoint vs per-tenant deployment.

#### 16. Scalable MCP catalog and lookup

**Problem:** Hundreds of tools are available; clients cannot discover and send
all descriptions every turn.

- **Basics at point of use:** Tool discovery, schema design, tool catalog
  caching, filtering and latency budgeting.
- **Build:** Build relevance-based tool selection on a catalog of mock tools.
- **Production architecture:** Define catalog TTL, schema-version pinning,
  stale-tool fallback and gateway observability.
- **Key decision:** Broad tool exposure vs prefiltered/curated tool sets.

#### 17. Long-running report via MCP Tasks

**Problem:** A report tool takes several minutes and must survive client
interruption.

- **Basics at point of use:** MCP Tasks extension, long-running operation
  lifecycle, polling and cancellation; host support varies.
- **Build:** Prototype an async report job with durable status, result retrieval
  and cancellation.
- **Production architecture:** Retry-safe creation, expiry, authorization on
  follow-up calls, worker recovery and compatibility fallback.
- **Key decision:** Immediate tool response vs task-based async execution.

### Module 03 — RAG, context engineering and memory

*Goal: Design information flow, source provenance and the boundary between
conversation context and durable data.*

#### 18. Document Q&A with RAG ★

**Problem:** Answer employee questions using a folder of approved documents.

- **Basics at point of use:** Ingestion, chunking, embeddings, vector search,
  retrieval and grounding.
- **Build:** Index 30 sample documents and return an answer with exact source
  links.
- **Production architecture:** Measure retrieval failures, enforce access,
  support document deletion and rebuild indexes.
- **Key decision:** Long-context prompting vs retrieval-augmented generation.

#### 19. Permission-aware enterprise search

**Problem:** Two users querying the same document set must see different
results.

- **Basics at point of use:** ACL filtering, prefilter vs postfilter, source
  metadata, security trimming.
- **Build:** Index a fake HR/engineering corpus and apply user-specific
  retrieval filters.
- **Production architecture:** Keep ACL changes synchronized, block cross-tenant
  snippets and test adversarial queries.
- **Key decision:** Filter before search vs after search; leakage and relevance
  trade-offs.

#### 20. Hybrid search and reranking

**Problem:** A product catalog contains exact identifiers and semantically
similar descriptions.

- **Basics at point of use:** BM25/keyword search, vector similarity, rank
  fusion, rerankers.
- **Build:** Compare keyword-only, vector-only and hybrid results on sample
  queries.
- **Production architecture:** Track ranking quality, freshness, p95 retrieval
  latency and index cost.
- **Key decision:** Semantic vs lexical vs hybrid retrieval.

#### 21. Customer 360 evidence assistant ★

**Problem:** A support agent needs CRM fields, orders and policy documents in
one answer.

- **Basics at point of use:** Structured + unstructured federation, source of
  truth, joins, evidence and citations.
- **Build:** Query mock SQL order data and a document index in one agent answer.
- **Production architecture:** Enforce cross-source permissions, reconcile
  conflicting timestamps and avoid hallucinated joins.
- **Key decision:** Tool federation vs central ETL/knowledge graph.

#### 22. Long-term assistant memory

**Problem:** An assistant remembers durable preferences without storing every
chat forever.

- **Basics at point of use:** Conversation window, summaries, episodic/semantic
  memory, lifecycle and consent.
- **Build:** Save only explicitly approved preferences; retrieve by relevance
  across sessions.
- **Production architecture:** Provide inspect/edit/delete, retention rules,
  prompt-injection defenses and stale-memory tests.
- **Key decision:** Session state vs long-term store; explicit vs inferred
  memory.

#### 23. Multilingual policy assistant

**Problem:** Employees ask in multiple languages about policies written in
different languages.

- **Basics at point of use:** Cross-lingual retrieval, translation boundaries,
  locale metadata and answer grounding.
- **Build:** Build a bilingual FAQ with source-language citations.
- **Production architecture:** Verify semantic equivalence, localize legal
  caveats and evaluate each language separately.
- **Key decision:** Translate-first vs multilingual embeddings.

#### 24. Near-real-time knowledge indexing

**Problem:** A customer updates a record and the AI answer must reflect it
quickly.

- **Basics at point of use:** CDC/events, indexing pipeline, tombstones,
  freshness contracts and eventual consistency.
- **Build:** Sync a mock source DB to a search index via change events.
- **Production architecture:** Handle reorder/replay, permission changes,
  deletion propagation and rebuilds.
- **Key decision:** Scheduled ingestion vs event-driven sync.

#### 25. Evidence verification agent

**Problem:** Analysts need reports that distinguish source-backed facts from
inferences.

- **Basics at point of use:** Claim extraction, evidence mapping, confidence
  calibration and abstention.
- **Build:** Extract claims from a draft and attach passages or flag unsupported
  claims.
- **Production architecture:** Evaluate false citations, provenance tampering,
  source contradictions and model changes.
- **Key decision:** Single-model self-check vs independent evidence retrieval.

### Module 04 — Agent orchestration, workflows and durable state

*Goal: Progress from single-agent execution to explicit workflows, state
machines and failure recovery.*

#### 26. IT incident investigator ★

**Problem:** An operator asks an assistant to diagnose an outage using logs and
metrics.

- **Basics at point of use:** ReAct-style tool loop, observation/action
  separation, tool budgets and bounded exploration.
- **Build:** Integrate mock metrics and log tools; produce an investigation
  timeline.
- **Production architecture:** Read-only by default, handle missing tools, rank
  evidence and constrain expensive queries.
- **Key decision:** Autonomous investigation vs scripted diagnostic tree.

#### 27. Plan-execute research workflow

**Problem:** A research task requires multiple questions, retrieval steps and
final synthesis.

- **Basics at point of use:** Task decomposition, explicit state,
  planner/executor, checkpointed partial results.
- **Build:** Build a graph of plan → retrieve → synthesize → cite.
- **Production architecture:** Revise plans after failure, preserve evidence
  IDs, cap recursion and resume safely.
- **Key decision:** Fixed graph vs dynamic planner.

#### 28. Refund approval agent ★

**Problem:** Support wants refunds proposed automatically but money must move
only with approval.

- **Basics at point of use:** Human-in-the-loop, separation of duties, action
  contracts and state transitions.
- **Build:** Implement proposal → approval → mock refund with persisted state.
- **Production architecture:** Expiring approval, amount caps, idempotency keys,
  audit and unknown provider status.
- **Key decision:** Model-selected action vs deterministic approval workflow.

#### 29. Supplier onboarding agent

**Problem:** Completing an onboarding request requires days, documents and
multiple departments.

- **Basics at point of use:** Durable execution, checkpoints, timers, external
  callbacks and compensation.
- **Build:** Orchestrate mock document checks and wait for human review.
- **Production architecture:** Resume across restarts, keep SLA timers, handle
  partial completion and operator intervention.
- **Key decision:** Agent loop vs durable workflow engine.

#### 30. Parallel contract comparison

**Problem:** Compare many documents independently, then combine findings.

- **Basics at point of use:** Fan-out/fan-in, concurrent tasks, result
  aggregation and provenance.
- **Build:** Analyze six sample contracts concurrently and produce a differences
  table.
- **Production architecture:** Bound parallelism, preserve per-document errors
  and avoid summary contamination.
- **Key decision:** Sequential tool calls vs concurrent workers.

#### 31. Event-triggered operations assistant

**Problem:** A monitoring event should launch a supervised investigation without
a user message.

- **Basics at point of use:** Event-driven agent invocation, queue semantics,
  deduplication and correlation IDs.
- **Build:** Trigger an agent from a mock alert stream and post a case note.
- **Production architecture:** Debounce alert storms, restrict authority, retry
  consumers and prevent duplicate actions.
- **Key decision:** Interactive request/response vs autonomous event processing.

#### 32. Large batch classification agent

**Problem:** Process 100,000 incoming records with mixed complexity.

- **Basics at point of use:** Work queues, batching, model routing, concurrency
  and backpressure.
- **Build:** Run a batch of sample tickets through cheap and fallback
  classifiers.
- **Production architecture:** Rate limits, dead-letter handling, cost caps and
  replay-safe writes.
- **Key decision:** Online agent vs offline batch processing.

#### 33. Crash-recoverable agent runtime

**Problem:** An agent stops halfway through an external operation and is
restarted.

- **Basics at point of use:** State machines, checkpointing, retries,
  at-least-once semantics and idempotency.
- **Build:** Kill a running workflow and resume from durable state.
- **Production architecture:** Detect in-flight ambiguous outcomes, use action
  ledger, prevent repeat side effects.
- **Key decision:** Re-run entire agent vs resume from committed steps.

### Module 05 — Generative UI, MCP Apps, AG-UI and A2UI

*Goal: Separate three concerns: what UI to render, how embedded views execute,
and how frontends exchange agent events.*

#### 34. AI sales dashboard from structured answers ★

**Problem:** A user asks for revenue comparisons and needs an interactive chart
rather than prose.

- **Basics at point of use:** Structured UI data, component catalogs, schema
  validation, derived state.
- **Build:** Return validated chart/table data to a self-contained HTML
  dashboard.
- **Production architecture:** Prevent arbitrary script injection, support empty
  states and export/print, log UI schema versions.
- **Key decision:** Server-rendered fixed dashboard vs model-selected approved
  components.

#### 35. Conversational configuration wizard

**Problem:** An assistant collects several settings with forms and updates them
after user edits.

- **Basics at point of use:** Form state, two-way interaction, validation, UI
  state vs agent state.
- **Build:** Build a plain HTML wizard with model-suggested fields from a fixed
  registry.
- **Production architecture:** Validate again on server, handle stale
  suggestions, accessibility and approval before save.
- **Key decision:** Model-generated HTML vs trusted component rendering.

#### 36. Expense-analysis MCP App ★

**Problem:** A user asks an AI host to analyze expenses and interact with charts
inline.

- **Basics at point of use:** MCP Apps `ui://` resources, tool-to-view metadata,
  host bridge and sandboxed iframe.
- **Build:** Build a tool returning budget data and a linked HTML MCP App view.
- **Production architecture:** Require compatible host, isolate credentials,
  enforce app permissions and text fallback.
- **Key decision:** MCP Apps embedded view vs conventional web app or plain tool
  response.

#### 37. Ticket-approval MCP App

**Problem:** Inside an AI chat, a reviewer approves or rejects a proposed
support action.

- **Basics at point of use:** MCP App bidirectional messaging, app-only tool
  visibility, approval and server authority.
- **Build:** Display a ticket view and send an approval decision to a mock
  backend tool.
- **Production architecture:** Ignore client-trusted claims, validate approver
  identity, prevent cross-server calls and duplicate approval.
- **Key decision:** App-view action via host vs model-issued action.

#### 38. Live incident console with AG-UI ★

**Problem:** Users need to watch agent steps and change the investigation while
it runs.

- **Basics at point of use:** AG-UI run lifecycle, text/tool events,
  snapshots/deltas and interruptions.
- **Build:** Stream mock agent events to an HTML timeline with a stop button.
- **Production architecture:** Reconnect with event cursor, validate state
  versions, redact tool payloads and show failed runs.
- **Key decision:** AG-UI event protocol vs custom SSE event format.

#### 39. Declarative A2UI request form

**Problem:** A remote agent suggests a form that must fit the host's own design
system.

- **Basics at point of use:** A2UI component descriptions, client-owned catalog,
  data binding and actions.
- **Build:** Render a small allowlisted A2UI form with native HTML components.
- **Production architecture:** Reject unknown components, enforce action
  authorization and version the renderer.
- **Key decision:** A2UI declarative native components vs MCP Apps embedded
  HTML.

#### 40. Portable UI comparison lab

**Problem:** A financial data result must appear inside both an MCP host and a
first-party web app.

- **Basics at point of use:** Transport vs rendering, MCP Apps vs A2UI vs static
  GenUI, compatibility.
- **Build:** Implement the same data workflow using two presentation adapters.
- **Production architecture:** Test fallback, host capabilities, accessibility
  and mismatched schema versions.
- **Key decision:** Embedded app portability vs native-style declarative UI.

#### 41. Enterprise agent cockpit

**Problem:** Analysts want chat, a shared workspace, tool progress and human
overrides.

- **Basics at point of use:** Shared state, AG-UI, generative components,
  frontend tools and state ownership.
- **Build:** Combine a chat pane, artifact pane and AG-UI progress timeline in
  plain HTML.
- **Production architecture:** Add authorization by action, reconnection,
  concurrent edits, redaction and event auditing.
- **Key decision:** Single conversational view vs coordinated multi-panel
  workspace.

### Module 06 — Multi-agent systems and A2A interoperability

*Goal: Use collaboration only where independent capabilities, ownership or task
decomposition justify it.*

#### 42. Supervisor and specialist investigators ★

**Problem:** A coordinator delegates incident subtasks to log, metrics and
change-history specialists.

- **Basics at point of use:** Supervisor-worker pattern, agents-as-tools,
  delegation contracts, shared evidence.
- **Build:** Make three isolated specialists return typed findings to one
  coordinator.
- **Production architecture:** Limit recursion, prevent untrusted specialist
  instructions, consolidate conflicting findings.
- **Key decision:** Multiple tools on one agent vs specialist agents.

#### 43. Remote fraud specialist via A2A ★

**Problem:** An investigation agent must ask a separately deployed fraud agent
for a risk report.

- **Basics at point of use:** A2A Agent Card, task-oriented interaction,
  artifacts and remote trust boundaries.
- **Build:** Publish a mock specialist and call it from an independent A2A
  client.
- **Production architecture:** Authenticate both parties, pin capabilities,
  track task IDs and validate artifacts.
- **Key decision:** In-process handoff vs cross-service A2A.

#### 44. Multi-vendor agent broker

**Problem:** Different vendors offer specialized agents with different
reliability and cost.

- **Basics at point of use:** Agent discovery, capability matching, routing,
  fallback and contract normalization.
- **Build:** Route a document query to one of two mock agents by declared
  capabilities.
- **Production architecture:** Health checks, vendor isolation, quotas, error
  normalization and sensitive-data routing.
- **Key decision:** Static integration vs agent registry/broker.

#### 45. Long-running A2A research task

**Problem:** A remote specialist takes minutes to produce an artifact while the
caller continues other work.

- **Basics at point of use:** A2A task lifecycle, status updates, push/poll
  variants and cancellation.
- **Build:** Start a remote job, observe status and retrieve result artifact.
- **Production architecture:** Durable task store, expiry, authorization on
  status reads, late results and retry rules.
- **Key decision:** Sync request vs long-lived task coordination.

#### 46. Customer-service handoff network

**Problem:** Triage routes a conversation to billing, returns or technical
support specialists.

- **Basics at point of use:** Handoffs, agent-as-tool, conversation ownership
  and context filtering.
- **Build:** Implement a triage agent and two specialists with explicit handoff
  behavior.
- **Production architecture:** Prevent oversharing chat history, handle
  unsupported intents and track ownership.
- **Key decision:** Manager retains control vs specialist takes control.

#### 47. Multi-agent peer review

**Problem:** One agent drafts a risk analysis and another independently
challenges missing evidence.

- **Basics at point of use:** Independent review, evidence comparison,
  disagreement resolution and self-critique limits.
- **Build:** Produce two independent analyses and a deterministic evidence-based
  merge.
- **Production architecture:** Avoid correlated errors, set review budgets and
  keep human final accountability.
- **Key decision:** One larger model vs structured specialist review.

#### 48. Cross-organization procurement assistants

**Problem:** Buyer and supplier agents exchange quotes without leaking internal
policies.

- **Basics at point of use:** Cross-org delegation, scoped intent, bounded
  negotiation and independent identity.
- **Build:** Simulate quote exchange between separately hosted agents.
- **Production architecture:** Validate prices deterministically, cap
  authorization and preserve signed/audited agreement state.
- **Key decision:** Free-form agent negotiation vs constrained business
  protocol.

#### 49. Enterprise agent directory

**Problem:** A platform team needs an inventory of agent owners, interfaces and
allowed capabilities.

- **Basics at point of use:** Capability metadata, agent registry, ownership,
  versioning and governance.
- **Build:** Create a searchable registry of mock Agent Cards and approved
  endpoints.
- **Production architecture:** Review untrusted cards, revoke capabilities,
  audit changes and deprecate versions.
- **Key decision:** Discovery convenience vs attack surface and control.

### Module 07 — Security, identity and enterprise architecture

*Goal: Put trust boundaries and permission checks around data, tools, UI and
external agents.*

#### 50. Injection-resistant knowledge assistant ★

**Problem:** A retrieved document tells the assistant to ignore policy and call
a privileged tool.

- **Basics at point of use:** Prompt injection, instruction/data separation,
  least authority and tool validation.
- **Build:** Insert hostile text into a mock knowledge base and prove the tool
  call is rejected.
- **Production architecture:** Red-team datasets, sandbox tool outputs, enforce
  policy outside the model and monitor drift.
- **Key decision:** Prompt-based warnings vs enforceable policy controls.

#### 51. Central policy engine for agent actions

**Problem:** Many agents want to perform the same risky business actions under
different conditions.

- **Basics at point of use:** RBAC/ABAC, policy decision/enforcement points,
  least privilege, audit.
- **Build:** Put one authorization service before write-capable mock tools.
- **Production architecture:** Fail closed on policy outage for high-risk
  actions; review policies and cache safely.
- **Key decision:** Embedded per-agent checks vs shared authorization service.

#### 52. Delegated identity across MCP

**Problem:** A signed-in user wants an agent to call their own CRM and
documents, not everyone else's.

- **Basics at point of use:** OAuth delegated access, token audience, scope,
  consent and session binding.
- **Build:** Implement mock per-user tool calls with scoped tokens and
  revocation.
- **Production architecture:** Verify scope and audience at each server, avoid
  token passthrough, test revoked sessions.
- **Key decision:** User delegation vs shared service principal.

#### 53. Computer-use assistant sandbox

**Problem:** An agent must inspect a web UI and fill a form safely.

- **Basics at point of use:** Computer-use environment, browser isolation, input
  injection and action confirmation.
- **Build:** Automate a local fake admin interface with safe read/preview-only
  steps.
- **Production architecture:** Ephemeral sandbox, domain allowlist, secret
  masking, file/download controls and approval.
- **Key decision:** Browser automation vs supported business API.

#### 54. Sensitive-document AI workspace

**Problem:** Employees query internal contracts containing personal and
confidential data.

- **Basics at point of use:** Data classification, retention, redaction, DLP and
  audit trails.
- **Build:** Classify mock documents and restrict retrieval/answers by
  sensitivity.
- **Production architecture:** Encrypt storage, minimize prompt payloads, handle
  legal retention and deletion proofs.
- **Key decision:** Central indexing vs isolated datasets.

#### 55. Multi-tenant agent platform

**Problem:** Enterprise customers share infrastructure but need separate state,
tools and billing.

- **Basics at point of use:** Control plane/data plane, tenant isolation,
  per-tenant keys and quotas.
- **Build:** Run two simulated tenants with isolated thread state and tool
  credentials.
- **Production architecture:** Prevent cross-tenant cache hits, enforce fair use
  and produce tenant-level audit/cost.
- **Key decision:** Shared runtime vs isolated tenant workloads.

#### 56. Auditable payment-operations copilot

**Problem:** An agent investigates failed payments but must not move money
without separate controls.

- **Basics at point of use:** Financial invariants, immutable audit, approval,
  idempotency and reconciliation.
- **Build:** Use mock payment records to draft a reversible remediation
  recommendation.
- **Production architecture:** Strict separation of duties, transaction
  confirmation, unknown outcomes and audit evidence.
- **Key decision:** AI recommendation vs deterministic financial execution.

#### 57. Agent supply-chain security

**Problem:** An agent pulls tools, skills and model configurations from external
repositories.

- **Basics at point of use:** Software supply chain, manifests, signatures,
  provenance, dependency review.
- **Build:** Validate a small approved registry of tool manifests and SKILL.md
  packages.
- **Production architecture:** Pin versions, audit permissions, quarantine
  untrusted packages and monitor changes.
- **Key decision:** Dynamic discovery vs curated trusted catalog.

### Module 08 — Evaluation, observability, reliability and operations

*Goal: Make nondeterministic systems measurable, recoverable and supportable.*

#### 58. Agent tracing and evaluation dashboard ★

**Problem:** Engineers need to know why a tool-using agent failed and what it
cost.

- **Basics at point of use:** Traces/spans, OpenTelemetry GenAI conventions,
  events, token/cost metrics.
- **Build:** Instrument model and tool spans and visualize run outcomes in a
  local dashboard.
- **Production architecture:** Redact sensitive data, correlate across MCP/A2A,
  define retention and sampling.
- **Key decision:** Vendor-specific telemetry vs portable instrumentation.

#### 59. Grounded-answer regression suite

**Problem:** A release improves one prompt but may break citation accuracy
elsewhere.

- **Basics at point of use:** Golden datasets, offline evals, grading rubrics,
  retrieval vs generation metrics.
- **Build:** Build a 30-case dataset and compare two assistant versions.
- **Production architecture:** Stratify edge cases, human adjudication, repeat
  runs and deployment gates.
- **Key decision:** Exact-match tests vs rubric/model-judged evaluation.

#### 60. Model gateway and fallback

**Problem:** Different requests need different quality, latency and cost.

- **Basics at point of use:** Model routing, timeout budgets, fallback, caching
  and model abstraction.
- **Build:** Route small tasks to one mock model profile and hard tasks to
  another.
- **Production architecture:** Measure quality regression, bound retries,
  protect data residency and control costs.
- **Key decision:** One model for everything vs task-based routing.

#### 61. High-load agent admission control

**Problem:** A spike in AI requests overwhelms model quotas and downstream
tools.

- **Basics at point of use:** Rate limiting, concurrency limits, queues, token
  budgets and backpressure.
- **Build:** Simulate overload and prioritize interactive requests over batch
  jobs.
- **Production architecture:** Tenant fairness, cancellation, queue expiry,
  graceful degradation and spend caps.
- **Key decision:** Unlimited queued work vs admission-controlled execution.

#### 62. Replay-safe external actions

**Problem:** A retry occurs after an agent submitted a downstream operation and
lost the response.

- **Basics at point of use:** Idempotency ledger, unknown outcomes, event replay
  and reconciliation.
- **Build:** Execute a fake refund or email send with crashes and repeated
  requests.
- **Production architecture:** Use stable operation IDs, status reconciliation,
  bounded retries and audit.
- **Key decision:** Blind retry vs deduplicate-and-reconcile.

#### 63. Safe prompt and agent rollout

**Problem:** Teams change prompts, models and tool contracts while users are
active.

- **Basics at point of use:** Versioning, canary, shadow runs, rollback and
  compatibility.
- **Build:** Compare current and candidate agent on replayed mock requests.
- **Production architecture:** Define rollback signals, keep stable tool schemas
  and prevent incompatible checkpoint resumes.
- **Key decision:** Big-bang deployment vs controlled release.

#### 64. Agent service SLO and on-call

**Problem:** A production agent sometimes takes many steps, fails or gives wrong
answers.

- **Basics at point of use:** Task success vs availability, latency percentiles,
  error budgets, incident runbooks.
- **Build:** Define metrics and a simulated alert dashboard for a mock support
  assistant.
- **Production architecture:** Separate model quality from infra health, triage
  bad actions, manage incident ownership.
- **Key decision:** HTTP uptime alone vs task-level service objectives.

#### 65. Multi-region agent disaster recovery

**Problem:** A regional failure interrupts agent runs and tool calls.

- **Basics at point of use:** RPO/RTO, durable checkpoints, failover, location
  of data and external effects.
- **Build:** Recover a mock active run in a second simulated region.
- **Production architecture:** Restore credentials safely, reconcile external
  side effects and test recovery drills.
- **Key decision:** Active-passive vs active-active agent processing.

### Module 09 — Emerging and advanced agentic systems

*Goal: Extend the standard architecture with multimodal, computer-use, skills,
code execution and a platform capstone.*

#### 66. Browser-based travel-admin agent

**Problem:** A user wants help filling travel expense forms in systems without
good APIs.

- **Basics at point of use:** Computer use, DOM/visual feedback, action
  grounding, confirmation and task boundaries.
- **Build:** Run a safe local travel-form mock that previews but does not
  purchase or submit.
- **Production architecture:** Handle changed layouts, credential isolation,
  stop conditions and intervention.
- **Key decision:** API/MCP integration vs computer use as last resort.

#### 67. Realtime voice support assistant

**Problem:** A spoken customer conversation needs quick responses and reliable
handoff to a human.

- **Basics at point of use:** Audio streaming, VAD/turn-taking, transcripts,
  real-time tool use and interruption.
- **Build:** Build a mock voice transcript stream driving a simple support
  workflow.
- **Production architecture:** Redaction, consent, audio retention, latency,
  call transfer and accessibility.
- **Key decision:** Speech pipeline vs integrated real-time multimodal model.

#### 68. Visual claims-inspection assistant

**Problem:** A user uploads product-damage images and asks for a claim
recommendation.

- **Basics at point of use:** Vision input, OCR where needed, multimodal
  grounding, uncertainty and evidence storage.
- **Build:** Return a structured damage report with referenced image regions and
  human review.
- **Production architecture:** Never treat model assessment as proof, retain
  originals, protect privacy and test visual edge cases.
- **Key decision:** Vision model vs deterministic CV + rules + human review.

#### 69. Code-editing agent in sandbox

**Problem:** An agent fixes a failing test in a small repository and proposes a
patch.

- **Basics at point of use:** Agent harness, filesystem tools, isolated
  execution, feedback loops and diffs.
- **Build:** Run a local repo agent on a toy failing test and produce a reviewed
  patch.
- **Production architecture:** Restrict network/secrets, cap resource use,
  require tests, review and rollback.
- **Key decision:** LLM-generated patch vs bounded edit/test harness.

#### 70. Agent Skills registry and discovery

**Problem:** Teams package repeatable workflows that agents may selectively
load.

- **Basics at point of use:** Agent Skills `SKILL.md`, metadata, progressive
  context loading and versioning.
- **Build:** Create three local skills with references and scripts; load by
  task.
- **Production architecture:** Vet code, pin skill versions, approve allowed
  tools, audit updates and use sandboxing.
- **Key decision:** Skills as reusable instructions vs tools as executable
  capabilities.

#### 71. AI workflow builder with visual steps

**Problem:** A non-developer describes a business process and receives an
editable workflow diagram.

- **Basics at point of use:** Declarative workflow schema, UI component grammar,
  static validation and human edits.
- **Build:** Generate a JSON workflow and render it with a self-contained HTML
  editor.
- **Production architecture:** Validate cycles, permissions, deployments and
  rollback before activating the workflow.
- **Key decision:** Free-form code generation vs constrained visual DSL.

#### 72. Code-and-data analysis workspace

**Problem:** An analyst asks a model to explore data and generate reproducible
charts.

- **Basics at point of use:** Code execution, sandbox, artifacts, notebook
  lineage and provenance.
- **Build:** Run generated analysis only on mock data in an isolated process.
- **Production architecture:** Restrict file/network access, capture
  dependencies, test results and retain audit artifacts.
- **Key decision:** Direct reasoning vs controlled computation.

#### 73. Unified enterprise agentic platform ★

**Problem:** A company needs governed assistants, MCP integrations, UI,
multi-agent tasks and operations.

- **Basics at point of use:** Control/data planes, identity, registries, MCP,
  A2A, AG-UI, MCP Apps, evaluation and cost.
- **Build:** Integrate one small end-to-end assistant with a UI, two tools and
  one remote specialist.
- **Production architecture:** Design policy enforcement, tenancy, DR,
  observability, deployment and upgrade governance.
- **Key decision:** Platform reuse vs per-team autonomy; which abstractions
  should remain optional.

## 6. The 16 full-depth anchor designs

Do not force the same depth onto all 73. Fully work these 16 in a
dependency-driven order; cover other cases as focused variations. The order
below is a recommendation, not a timed schedule.

| Order | Case                                           | Deep pattern                                        | What becomes easier afterward            |
|------:|------------------------------------------------|-----------------------------------------------------|------------------------------------------|
|     1 | #1 FAQ support assistant                       | Structured answer, grounding and non-agent baseline | Classification, summarization, research  |
|     2 | #3 Order-status tool agent                     | Tool schemas, ownership checks, error semantics     | MCP tools, analytics and action safety   |
|     3 | #9 Local ticket-lookup MCP server              | Host/client/server, resource/tool contract          | All MCP servers and gateways             |
|     4 | #14 Enterprise MCP authorization broker        | OAuth scopes, delegation and token flow             | Multi-tenant and secure MCP              |
|     5 | #18 Document Q&A with RAG                      | Ingestion, retrieval and citation                   | Enterprise search and memory             |
|     6 | #21 Customer 360 evidence assistant            | Data ownership and multi-source evidence            | Customer 360 and analyst assistants      |
|     7 | #26 IT incident investigator                   | Tool loops, state and evidentiary reasoning         | Planners, monitoring and automation      |
|     8 | #28 Refund approval agent                      | Approvals, idempotency and side-effect safety       | Payments, IT ops and autonomous actions  |
|     9 | #34 AI sales dashboard from structured answers | Typed UI contracts and safe component rendering     | MCP Apps, A2UI                           |
|    10 | #36 Expense-analysis MCP App                   | UI resources, iframe bridge, host compatibility     | Embedded AI apps and approvals           |
|    11 | #38 Live incident console with AG-UI           | Streaming lifecycle, state deltas and reconnection  | Agent cockpits and live workflows        |
|    12 | #42 Supervisor and specialist investigators    | Delegation and coordination trade-offs              | Multi-agent systems                      |
|    13 | #43 Remote fraud specialist via A2A            | Capability discovery, tasks, artifacts              | Cross-org agent networks                 |
|    14 | #50 Injection-resistant knowledge assistant    | Model trust vs enforceable controls                 | All enterprise agents                    |
|    15 | #58 Agent tracing and evaluation dashboard     | Runs, spans, objective outcomes and test suites     | Production diagnostics and release gates |
|    16 | #73 Unified enterprise agentic platform        | End-to-end governance and operating model           | Architecture review and reference design |

## 7. Fully worked sample — #36 Expense-analysis MCP App

This is a compact **worked-design example**, not a claim of an already executed
code project. It demonstrates how the remaining anchors should be taught.

### 7.1 Define the problem before the technology

**User story:** An expense analyst asks an AI assistant: “Show spending by
category for Q3; let me adjust the threshold and inspect anomalies.” A prose
answer is inadequate because the analyst needs an interactive chart within the
conversation.

**Functional requirements:** Retrieve mock expense data, show summary/charts,
adjust a filter locally, optionally request a new tool query, and fall back to
text if the host does not support embedded UI. The example uses *fake* data; it
does not initiate payments.

**Quality priorities:** Correct tenant access > trusted actions > readable UI >
interactive latency > deployment simplicity. Example dataset size is small; no
large-scale infrastructure is needed yet.

### 7.2 Introduce exactly the concepts the requirement creates

- **Tool:** A typed callable capability, such as
  `get_expense_summary(period, department)`. The model/host requests it, but the
  server performs authorization and queries the actual source of truth.
- **MCP:** The shared contract that lets a compatible host access the tool
  without rewriting the same tool integration for each client.
- **MCP App:** An *optional* MCP extension where a tool points to a `ui://` HTML
  resource. A compatible host displays it in a sandboxed iframe and mediates
  messages through its bridge.
- **UI state:** The selected chart filter should live in the view; authoritative
  permissions and any persisted business change must remain server-side.
- **Host fallback:** An ordinary MCP tool result must remain useful if the
  target host cannot render MCP Apps.

### 7.3 Minimum viable architecture

```text
Analyst
   |
   v
AI host / chat UI (supports MCP Apps)
   |    (MCP client)
   v
MCP expense server
   |-- tool: get_expense_summary(period, department)
   |-- resource: ui://expense-dashboard  [HTML view]
   +-- mock expense database

AI host reads UI resource --> sandboxed HTML view
                                 | 
                                 +-- chart filter (local only)
                                 +-- host bridge for allowed tool calls
```

**Happy path:** User asks → host chooses tool → server validates request and
returns data → host fetches the linked UI resource → host displays the HTML
view → user adjusts a filter → view updates locally or asks the host to call an
app-permitted tool.

### 7.4 Data and interface contracts

Example **logical** tool request (not SDK-specific wire syntax):

```json
{
  "tool": "get_expense_summary",
  "arguments": {
    "period": "2026-Q3",
    "department": "sales"
  }
}
```

Example tool response shape:

```json
{
  "period": "2026-Q3",
  "currency": "USD",
  "categories": [
    {
      "name": "Travel",
      "amount": 1800
    },
    {
      "name": "Software",
      "amount": 650
    }
  ],
  "as_of": "2026-10-01T00:00:00Z"
}
```

An implementation should link the tool to a `ui://` resource using the MCP Apps
specification for the actual SDK version. The payload above is intentionally *
*application-level JSON**, not an invented MCP envelope. For practice, implement
one tool with summary data and one linked HTML view; test it in a host that
explicitly supports MCP Apps.

### 7.5 Evolve the architecture because of named requirements

1. **Requirement — no cross-tenant access.** The server derives tenant/user from
   verified credentials; do not accept tenant choice from the model or iframe as
   authority.
2. **Requirement — unsafe instructions in expense memos.** Treat tool/data
   content as untrusted, not as policy or instructions.
3. **Requirement — expensive date-range queries.** Use bounded query windows,
   paging/aggregation and a cache with a visible freshness timestamp.
4. **Requirement — host incompatibility.** Return human-readable text/structured
   data; do not assume all MCP clients support MCP Apps.
5. **Requirement — operational diagnosis.** Trace host request, MCP tool,
   database query and UI error separately; keep sensitive query values out of
   logs.
6. **Requirement — reproducibility.** Version tool input/output schema, UI
   bundle and SDK/runtime versions.

### 7.6 Production architecture and failure flow

```text
                   Signed-in analyst
                          |
                          v
             MCP Apps-capable AI host
           (auth, capability negotiation)
                          |
                 MCP client / bridge
                          |
                          v
           HTTPS MCP expense service
             |     |        |
           AuthZ  Tool    UI resource
             |     |        |
             |     v        +--> Sandboxed HTML iframe
             |  Query layer              |
             |     |                     +-- local filters
             |     +--> mock DB          +-- host-mediated calls
             |     +--> cache
             |
             +--> audit + traces + quotas

     No host UI support --> useful text/structured fallback
     Revoked permission --> deny tool call; do not show old data
     Tool timeout       --> error UI + bounded retry, no fake totals
```

**Failure sequence:** User's permission is revoked after viewing the dashboard.
When they request refreshed values, server authorization must reject the call
even if the iframe still contains stale local data. The UI should show the
failed refresh; it must not invent a successful result.

### 7.7 The choice that matters

| Option                      | When it fits                                                                  | Trade-off                                                              |
|-----------------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------|
| Plain MCP tool result       | User only needs text or structured data                                       | No rich in-chat control surface                                        |
| MCP Apps                    | A compatible conversational host should render an inline tool-owned HTML view | Optional host support; iframe and bridge security requirements         |
| AG-UI + first-party web app | You own the application's frontend and need live agent progress/state         | You build and operate the web app; a separate concern from MCP tool UI |
| A2UI                        | A host should render agent-declared components from its own approved catalog  | Requires compatible renderer and approved component set                |

**Production acceptance criteria:** (1) authorized user sees only their own
department's sample data, (2) a disallowed tool action is rejected by the
server, (3) incompatible host receives usable fallback text, (4) interrupted
queries show explicit error, (5) request/trace IDs correlate across the
server, (6) UI works without external JavaScript dependencies if building the
standalone lab.

## 8. Recommended breadth-first study order

Not a weekly schedule. Start with five anchors to establish the minimum model,
tool and state vocabulary. Continue through integration and UI, then multi-agent
and production.

```text
Pass A — First AI architecture decisions:
  #1 -> #3 -> #9 -> #18 -> #26

Pass B — Actions, identity and information quality:
  #14 -> #21 -> #28 -> #50

Pass C — Human-facing architecture:
  #34 -> #36 -> #38 -> #39 (A2UI variation)

Pass D — Inter-agent architecture:
  #42 -> #43 -> #45 (long-running task variation)

Pass E — Operate and integrate:
  #58 -> #62 (retry variation) -> #73

Pass F — Complete the remaining 57 cases as pattern variants.
```

**No framework lock-in:** A recommended first lab stack is Python + a small
agent SDK or direct model API, TypeScript for MCP Apps SDK examples where
useful, HTML/CSS/JS for the UI and SQLite for mock business records. When a
particular feature is SDK-specific, label it. Do not confuse *protocol-level
compatibility* with SDK support.

## 9. Reusable prompt to begin any design

> Work through Agentic AI case **#N** as a guided Solution Architect lesson.
> Start from the business requirement and simplest valid solution. Explain each
> newly needed concept in basic English at first use, then draw ASCII
> component/sequence/state diagrams. Give me a small working mock build with
> inputs and expected outputs. Derive production changes from specific
> constraints: authorization, untrusted input, safety, latency, scale, failure
> recovery, evaluation, observability and cost. Compare credible architectural
> options; clearly distinguish standards, extensions, frameworks and vendor
> features. Do not quiz or time-box me.

## 10. Official references and version boundaries

Verified from primary project, standards-body and vendor documentation as of *
*November 6, 2026**. These resources are starting points; inspect actual SDK and
client capability before implementation.

-
    *
*[MCP current specification / release notes](https://blog.modelcontextprotocol.io/posts/2026-07-28/):
** Check the specific negotiated spec and SDK version. July 2026 release added
stateless core and extensions.
-
    *
*[MCP main specification](https://modelcontextprotocol.io/specification/2026-07-28):
** Core protocol; verify implementation-specific capabilities.
-
    *
*[MCP Apps official spec / SDK](https://github.com/modelcontextprotocol/ext-apps):
** Optional host extension: UI resources, iframe sandbox and host bridge.
- **[AG-UI official docs and events](https://github.com/ag-ui-protocol/ag-ui):**
  Event stream between agent runtime and first-party user-facing frontend.
- **[A2A 1.0 specification](https://a2a-protocol.org/v1.0.0/specification):**
  Interoperability across independently deployed agent systems.
- **[A2UI official project](https://a2ui.org/):** Declarative UI representation
  rendered by a host-owned component library.
- **[Agent Skills specification](https://agentskills.io/specification):**
  SKILL.md package format and optional scripts/references.
- **[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/):**
  Agents, tools, handoffs, guardrails and tracing.
-
    *
*[LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence):
** Checkpoints and durable state in explicit workflows.
-
    *
*[OWASP Agentic Top 10 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/):
** Agent-specific security risks and mitigations.
-
    *
*[OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai):
** Open instrumentation vocabulary, subject to change.
-
    *
*[AWS Agentic AI Well-Architected Lens](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/):
** Production architecture and operations review.

## 11. Scope notes and maintenance

- The catalog is a **proposed learning architecture**, not an official
  industry-certified problem bank. Its order and anchor selection are teaching
  recommendations.
- Terms such as *agent harness*, *GenUI* and *multi-agent* can refer to broad
  patterns; no single standard governs everything.
- **MCP** is a core protocol; **MCP Apps** is an optional extension, not
  guaranteed in every host. **AG-UI** transports events between an agent and an
  app; **A2UI** is a declarative representation of UI; **A2A** concerns agents
  communicating with other agents.
- A user-facing approval button is not enough to authorize an action:
  authorization must be enforced at the service where the business effect
  occurs.
- Side-effecting actions cannot be made safe by asking the model to be careful.
  Use deterministic state transitions, idempotency, access checks and
  reconciliation.
- Official specs and framework capabilities change. Before building a case,
  check release notes, host support and SDK versions. Avoid turning fast-moving
  API details into permanent design assumptions.
