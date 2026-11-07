# Agentic AI Solution Architecture — Fundamentals Primer

**Start here | Foundation module | Version: 2026-11-06**  
**Scope:** agent fundamentals, tool calling, bounded workflows, architecture decisions, and a first look at MCP, Generative UI, and A2A.  
**Estimated reading:** 35–45 minutes. **Optional local mock:** 10 minutes.  
**Audience:** software engineers, architects, and technical leads new to agentic AI.

> **Core rule:** Design around a business problem and a trusted source of truth. Do not add an agent, protocol, vector database, or multiple services unless a requirement justifies it.

This primer follows the project's `SKILL.md`, `sdt-module-01-agent-fundamentals.md`, and the optional FAQ anchor. Cross-protocol and production-control references are only used to preview later topics. Current protocol descriptions were checked against their official documentation on the version date. Examples and policies below are **synthetic**, not real company rules or production-ready code.

---

## 1. Begin with a real problem

**Scenario:** A customer-support assistant must answer return-policy questions from approved company information. Later, customers also want to know the status of their own support tickets.

- **Actors:** customer, support application, approved policy owner, ticket service, human support agent.
- **Business result:** return an accurate answer with evidence; never expose another customer's ticket.
- **Sources of truth:** the approved policy repository for return rules; the ticket service for live ticket status. The LLM is **not** a source of truth.
- **Initial scope:** read-only questions. No refunds, account changes, email sending, or ticket closing.
- **Ranked constraints:** (1) factual correctness, (2) access control, (3) source freshness, (4) clear failure behavior, (5) latency and cost.

**Representative requests:**

> “Can I return an unopened item after 14 days?”  
> “What is the status of ticket T-100?”

Start with the first request. It may need no autonomous agent at all.

## 2. The building blocks, in plain English

| Term | Simple definition | In the support example |
|---|---|---|
| **Model / LLM** | Software that predicts and generates language or structured content from input. | Writes a clear answer from a policy passage. |
| **Prompt and context** | Instructions plus the information supplied for the current model call. | “Only answer from policy POL-01,” followed by the approved text. |
| **Structured output** | A response constrained to a known data shape. | `{ "answer": "...", "source_ids": ["POL-01"] }` |
| **Tool / function call** | A named operation with defined inputs and outputs. | `get_ticket(ticket_id)` reads a ticket service. |
| **Agent** | A model-driven application that can choose and use tools across steps under runtime controls. | Decides whether to search policy or call the ticket tool. |
| **Workflow** | A predefined sequence of steps and decisions. | Retrieve policy → verify evidence → format answer. |
| **Orchestration** | The code/runtime that schedules steps, stores state and handles failure. | Limits tool calls and stops after a timeout. |
| **Grounding** | Making the answer depend on retrieved or verified evidence. | Cites the policy passage rather than inventing a return rule. |
| **Authorization (AuthZ)** | Checking whether this authenticated actor may access this specific resource or perform this action. | Alice may read T-100 but not Bob's T-200. |

**Important:** A model producing the words “I called the ticket system” does not prove a tool was called. Only the application runtime can execute tools and record verified results.

## 3. Pick the simplest valid pattern

| Design | Choose it when | Example | Main weakness |
|---|---|---|---|
| **Deterministic application code** | Inputs and business rules are predictable. | Exact lookup of an existing policy ID. | Does not handle flexible language well. |
| **Single model call** | Language understanding or formatting is needed, but no dynamic tools. | Rewrite an approved rule in simple English. | May misstate information without validation. |
| **Fixed workflow** | Every request has the same ordered steps. | Retrieve → validate → answer. | Less flexible when tasks vary. |
| **Bounded tool-using agent** | The next tool really depends on the user's question or intermediate results. | Choose policy search or ticket lookup, at most three tool calls. | More variable latency, cost and failure paths. |

**Decision principle:** Prefer deterministic code for rules, permissions, and side effects. Use a model for interpretation and language. Use an agent when dynamic tool selection provides clear value.

## 4. Minimal architecture: FAQ assistant

For twelve approved FAQ items, an exact or keyword lookup may be enough. A vector database and MCP are not prerequisites.

```text
+-------------------------+
| Customer / web client   |
+-------------------------+
             |
             v
+-------------------------+
| Support API             |
| Input + identity checks |
+-------------------------+
             |
             v
+-------------------------+
| Approved FAQ lookup     |
| Returns source IDs      |
+-------------------------+
             |
             v
+-------------------------+
| Answer or abstain       |
| Optional LLM phrasing   |
+-------------------------+
```

**Ownership:** the support API owns request validation; the policy system owns the rule; the answer layer owns how to present the result. The model does not approve policy changes.

**Happy path:** (1) customer asks, (2) API retrieves an approved matching passage, (3) the service returns a grounded answer with its ID, (4) the UI displays it.

**Failure path:** if no approved policy matches, return `insufficient_evidence` and offer escalation. Do not guess.

### Worked contract (application JSON, not a protocol wire format)

Request:

```json
{"question":"Can I return an unopened item after 14 days?"}
```

Synthetic approved record:

```json
{"source_id":"POL-01","status":"approved","text":"Unopened items may be returned within 30 days of delivery."}
```

Example response:

```json
{
  "status":"grounded",
  "answer":"Yes. The example policy allows unopened-item returns within 30 days of delivery.",
  "source_ids":["POL-01"]
}
```

The example uses a fake return policy. A real implementation must use the current rule owned by the business.

## 5. Add one read-only tool: ticket lookup

Now the customer asks, “What is the status of T-100?” The model cannot know the live status. We need a trusted tool.

```text
+-------------------------+
| Authenticated customer  |
+-------------------------+
             |
             v
+-------------------------+
| Support API / agent     |
| Chooses allowed tool    |
+-------------------------+
             |
             v
+-------------------------+
| get_ticket(ticket_id)   |
| Server-side AuthZ       |
+-------------------------+
             |
             v
+-------------------------+
| Ticket system           |
| Business source of truth|
+-------------------------+
```

**Tool signature (conceptual):**

```text
get_ticket(ticket_id: string) ->
  {ticket_id: string, status: string, updated_at: string}
  OR {error: "not_found" | "forbidden" | "unavailable"}
```

Example tool request proposed by the model:

```json
{"tool":"get_ticket","arguments":{"ticket_id":"T-100"}}
```

Example verified tool result:

```json
{"ticket_id":"T-100","status":"in_progress","updated_at":"2026-11-05T16:30:00Z"}
```

**Trust boundary:** the model may suggest a `ticket_id`. The backend gets the authenticated user from trusted session or token context and checks ticket ownership itself. The model cannot pass `"user_id":"alice"` and gain Alice's rights.

If T-200 belongs to a different user, the tool must return `forbidden` **before** the model sees that ticket's content.

## 6. What an agent loop actually does

An agent is more than one prompt. A runtime repeatedly asks the model what to do next, validates a proposed tool call, executes it, and supplies the verified result back to the model.

```text
+------------------------+
| User request           |
+------------------------+
            |
            v
+------------------------+
| Model proposes         |
| answer or tool call    |
+------------------------+
            |
            v
+------------------------+
| Runtime checks budget, |
| schema and permissions |
+------------------------+
            |
            v
+------------------------+
| Tool runs and returns  |
| verified result        |
+------------------------+
            |
            v
+------------------------+
| Model answers or asks  |
| for another tool call  |
+------------------------+
```

An illustrative runtime:

```python
for step in range(MAX_STEPS):
    decision = model.propose_next_step(context)  # conceptual model API
    if decision.kind == "final":
        return validate_answer(decision.answer)
    call = validate_allowed_tool_and_schema(decision.tool_call)
    result = execute_with_server_authorization(call, identity)
    context.append(result)
return {"status": "stopped", "reason": "step_limit"}
```

This is **architecture pseudocode**, not executable SDK code. The runtime must also enforce time limits, error handling and limits on sensitive data passed into context.

A good agent has a clear **finish condition**. Unlimited tool loops are not a feature.

## 7. Retrieval, context and memory are different

- **Retrieval:** find relevant source material, such as the approved return policy.
- **RAG (retrieval-augmented generation):** retrieve passages and then ask the model to answer using them.
- **Context:** the information placed in a particular model request; it has a finite capacity and cost.
- **Memory:** retained information about a user/session across requests, subject to retention and permission rules.

For the small FAQ assistant, keyword matching may be sufficient. If policies grow to thousands of documents, add appropriate retrieval, source IDs, access filters, freshness tracking, and possibly semantic/hybrid search.

**The search index is derived data, not the policy source of truth.** If a policy changes, the index needs an update process. If the source is restricted, retrieval must enforce that restriction before its text reaches the model.

## 8. MCP: a standard boundary for tools and context

**Model Context Protocol (MCP)** standardizes communication between an AI host and external capability providers. It does not tell the model how to reason and does not grant business permission.

```text
+-------------------------+
| AI host                 |
| Conversation + runtime  |
+-------------------------+
             |
             v
+-------------------------+
| MCP client              |
| Protocol connection     |
+-------------------------+
             |
             v
+-------------------------+
| MCP server              |
| Tools / resources /     |
| prompts                 |
+-------------------------+
             |
             v
+-------------------------+
| Owner system / API      |
| Identity + AuthZ        |
+-------------------------+
```

**Three common MCP primitives:**

- **Tools:** callable operations, such as `get_ticket`.
- **Resources:** retrievable context, such as a policy document.
- **Prompts:** reusable prompt templates exposed to the host.

**Direct function or MCP?** If one application owns a single tool, a direct typed API call is often simpler. If multiple compatible AI hosts need the same integration, MCP can give you a reusable boundary. An MCP tool's input schema is not a permission check.

MCP uses a defined protocol and versioned capabilities. Check the exact specification/SDK supported by your host before copying tutorials.

## 9. Generative UI, MCP Apps, AG-UI, A2UI, and A2A

These technologies solve **different boundaries**. They are not five versions of the same architecture.

| Technology | Boundary | Example | Key caution |
|---|---|---|---|
| **Structured Generative UI** | Model data → application-owned approved UI components | Return ticket status as a validated card schema. | Never render arbitrary model HTML without control. |
| **MCP Apps** | MCP host ↔ sandboxed embedded UI associated with server tools | Interactive ticket dashboard inside an AI chat host. | Optional extension; requires compatible host. |
| **AG-UI** | Agent runtime ↔ first-party frontend event/state stream | Show live “fetching ticket → summarizing” progress. | Not a replacement for MCP tools. |
| **A2UI** | Declarative UI description ↔ trusted component renderer | Agent proposes a form using approved controls. | Needs a compatible renderer and allowed components. |
| **A2A** | One independently deployed agent ↔ another agent service | Delegate fraud review to a remote specialist. | Adds remote trust, task and failure handling. |
| **Agent Skills** | Reusable agent instructions and references | A documented support-triage procedure. | Instructions do not execute tools or grant access. |

For your first FAQ/ticket system, none of these extensions is required. Introduce a protocol **only after** its integration or UI requirement appears.

### A concrete UI progression

1. **Plain answer:** text says “T-100 is in progress.”
2. **Structured UI:** app renders an approved ticket card from validated JSON.
3. **AG-UI (if needed):** first-party app shows live agent run and tool events.
4. **MCP Apps (if needed):** compatible AI host embeds a sandboxed ticket view linked to MCP tools.
5. **A2A (if needed):** an independently operated specialist handles a delegated task.

Do not describe a plain HTML preview as an MCP App unless it actually uses the extension's host/server/view contract.

## 10. Production concerns: derive the control from the failure

| Failure you must prevent | Required architectural idea | How you would demonstrate it |
|---|---|---|
| Model invents a return policy | Approved evidence + abstention | Unknown question returns `insufficient_evidence`. |
| Alice reads Bob's ticket | Server-side per-ticket authorization | T-200 is denied to Alice. |
| Tool result contains hostile instructions | Treat retrieved/tool text as untrusted | No privileged action is executed from ticket text. |
| Agent repeatedly calls tools | Step, time and cost limits | Run terminates at its configured limit. |
| UI button says “Approved” but backend did not approve | Server checks user, resource, action and current state | Unauthorized click is rejected. |
| Write call times out after succeeding | Stable operation ID + reconcile before retry | Only one logical effect is recorded. |
| System is “up” but answers are wrong | Task-level evaluations and traces | Grounding regressions and tool failures are visible. |

**Read-only tools are best for the first project.** When you eventually add refund, email or ticket-close actions, separate proposal from execution:

```text
+-------------------------+
| Agent proposes action   |
+-------------------------+
             |
             v
+-------------------------+
| Application stores      |
| pending action + ID     |
+-------------------------+
             |
             v
+-------------------------+
| Human reviews action    |
+-------------------------+
             |
             v
+-------------------------+
| Business service checks |
| identity + policy +     |
| current state           |
+-------------------------+
             |
             v
+-------------------------+
| Execute once, audit and |
| reconcile result        |
+-------------------------+
```

**Approval screens and model text do not enforce authorization.** The business service is the final enforcement point.

## 11. A small local mock you can run

The companion script `agent_fundamentals_mock.py` is intentionally **not** an LLM agent or an MCP server. It demonstrates the mechanics you must understand first: routing requests, looking up trusted data, checking ownership, citing source IDs, and returning honest failures.

**Requirements:** Python 3.9+; no third-party packages; no network calls. Use synthetic data only.

```bash
python agent_fundamentals_mock.py --user alice --question "Can I return an unopened item after 14 days?"
python agent_fundamentals_mock.py --user alice --question "What is the status of ticket T-100?"
python agent_fundamentals_mock.py --user alice --question "What is the status of ticket T-200?"
python agent_fundamentals_mock.py --smoke
```

**Illustrative outcomes:**

| Input | Expected behavior |
|---|---|
| Return-policy question | Returns approved synthetic policy `POL-01`. |
| Alice asks about T-100 | Returns Alice's ticket status. |
| Alice asks about T-200 | Returns `forbidden`, never the private ticket fields. |
| Unknown policy question | Returns `insufficient_evidence`, not an invented answer. |

The mock uses deterministic selection to make the trust and data flow easy to see. An actual model/tool loop can be introduced later without changing the authorization boundary.

## 12. Architecture checklist and next reading

Before choosing a framework, write down the answers to these:

- **Outcome:** What business task must succeed?
- **Truth:** Which service/document owns the facts?
- **Trust:** Who is the user, and where is authorization enforced?
- **Tools:** Which operations are necessary, read-only, or side-effecting?
- **State:** What must survive retries, crashes, or a resumed session?
- **Failure:** What happens when evidence is missing or a tool times out?
- **Evidence:** How will you measure correct answers and trace errors?
- **Complexity:** Why is an agent, MCP, AG-UI, or A2A better than a simpler design?

**Suggested progression through this project's AI catalog:**

1. **AI design #01 — FAQ support assistant:** grounding and abstention.
2. **AI design #03 — Order-status tool agent:** tools, runtime and access checks.
3. **AI design #09 — Local ticket-lookup MCP server:** protocol boundary.
4. **AI design #34 — AI sales dashboard:** structured Generative UI.
5. **AI design #36 — Expense-analysis MCP App:** interactive host-embedded UI.
6. **AI design #38 — Live incident console:** AG-UI events and state.
7. **AI design #43 — Remote fraud specialist:** A2A delegation.

### Six principles to retain

1. **Begin with the source of truth, not the model.**
2. **Use the simplest architecture that satisfies the task.**
3. **A tool schema is not a permission policy.**
4. **A model may propose; trusted application code must validate and execute.**
5. **Keep UI, protocol, runtime and business authorization as separate boundaries.**
6. **Test failure behavior and task correctness, not just a successful demo.**

---

## References and verification

### Project reference sources

- `SKILL.md` — problem-first, six-stage teaching method.
- `sdt-module-01-agent-fundamentals.md` — primary source for this primer, cases #01–#08.
- `sdt-anchor-01-faq-support-assistant.md` — FAQ source-of-truth and grounding example.
- `concept-protocol-boundaries.md` — short, boundary-oriented comparison of MCP Apps, AG-UI, A2UI, A2A and Skills.
- `concept-production-controls.md` — authorization, idempotency, security and evaluation controls.
- `sdt-catalog.md` — exact next-case titles and routing.

### Official documentation (checked 2026-11-06)

- [Model Context Protocol architecture](https://modelcontextprotocol.io/docs/learn/architecture) and [specification](https://modelcontextprotocol.io/specification)
- [MCP Apps overview and specification](https://github.com/modelcontextprotocol/ext-apps/blob/main/docs/overview.md)
- [AG-UI protocol overview](https://github.com/ag-ui-protocol/ag-ui/blob/main/docs/introduction.mdx)
- [A2A protocol specification](https://a2a-protocol.org/latest/specification/)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Agents SDK — agents](https://openai.github.io/openai-agents-python/agents/)
- [OpenTelemetry Generative AI conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)

**Version warning:** protocol features and host support can change. This is a conceptual primer, not a claim that every host supports every optional extension.
