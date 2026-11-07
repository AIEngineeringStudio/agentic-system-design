# OpenAI Agents SDK — Solution Architecture Study Guide

**From fundamentals to advanced, production-grade agentic systems**  
**Edition:** 2026-11-06 · **Primary language:** Python · **Audience:** AI solution architects and engineers  
**Primary SDK:** `openai-agents` (Agents SDK for Python), not to be confused with the lower-level `openai` API client.

> **Scope and verification.** This handbook interprets “OpenAI SDK” as the **OpenAI Agents SDK** because the surrounding learning goal is agentic architecture. It explains where the lower-level OpenAI API SDK fits. Official SDK documents and public release notes were checked on 2026-11-06. The Python Agents SDK repository listed **v0.24.0 (2026-10-15)** as its latest stable release and a newer **v0.24.0-alpha.6** prerelease; this document teaches documented APIs, not prerelease-only behavior. SDK features, model compatibility, and service limits change. Verify the version and relevant official pages before deployment. Code needing an API key is **illustrative and not executed against OpenAI** for this handbook. References are in §31.

---

## How to use this guide

**Read in order for your first pass:** Chapters 1–11 → 13–15 → 20–23. **For an architecture review:** chapters 2, 6, 12, 16–29. **For hands-on work:** run the short snippets with synthetic records, then build the capstone in Chapter 30. Code snippets assume Python 3.10+ unless otherwise noted. Use an isolated virtual environment, a development API key, and a supported model in your account. Do not put secrets in source files.

**Project curriculum mapping:** This is a **custom case** closest to `sdt-module-01-agent-fundamentals.md`, extended as needed into orchestration, MCP, security, and operations. It follows the AI Study Tutor principles: real problem → needed concepts → minimum architecture → mock → production evolution → trade-offs. The accompanying Project source `concept-production-controls.md` informs the authorization, retry, and recovery guidance. Those Project sources are architectural study material, not the authoritative SDK API documentation.

### Learning path at a glance

| Level | Chapters | Outcome |
|---|---|---|
| Foundations | 1–7 | Explain the model/API/SDK boundary; run one bounded agent |
| Core | 8–15 | Build tools, typed outputs, local context, sessions, streams, guardrails |
| Intermediate | 16–20 | Choose multi-agent patterns, approvals, MCP, retrieval, orchestration |
| Advanced | 21–29 | Add tracing, evaluation, security, durability, performance, platform patterns |
| Applied | 30 | Complete a staged enterprise case with architecture deliverables |

# Part I — Problem, system boundary, and fundamentals

## 1. Begin with a real problem: ticket-status assistant

A support operator asks: **“What is the status of ticket T-100?”** The answer must come from a ticket database, not the model’s memory. In the first version, the system only reads data. It never closes, refunds, or modifies tickets.

| Aspect | First-version decision |
|---|---|
| Actor | Authenticated support operator |
| Business result | Correct ticket status with source ID and timestamp |
| Source of truth | Internal ticket service/database |
| Trust boundary | Backend authenticates operator; ticket service authorizes each read |
| Priority 1 | No cross-customer ticket disclosure |
| Priority 2 | Correct factual answer or explicit “not found/not permitted” |
| Priority 3 | Bounded tool calls and latency |
| Out of scope | Modifying a ticket, multiple agents, MCP, vector index, automatic approvals |

**Smallest credible solution:** An application API could call `GET /tickets/{id}` directly and format the result. No agent is required. An agent becomes useful when requests are varied (“find the ticket about checkout failures, inspect its last update, and explain it in plain English”) and tool selection/explanation requires language understanding.

### 1.1 Minimal architecture

```text
+------------------------+
| Operator / web client  |
+------------------------+
            |
            v
+------------------------+
| Backend API + identity |
+------------------------+
            |
            v
+------------------------+
| Agent + Runner         |
| bounded tool selection |
+------------------------+
            |
            v
+------------------------+
| Authorized ticket API  |
| system of record       |
+------------------------+
```

**Happy path:** backend validates identity → calls agent with task and local identity context → agent requests `get_ticket` → backend tool applies the ticket access policy → result reaches model → model returns a grounded explanation. **Failure path:** if operator lacks permission, tool returns a safe denial; the assistant must not guess ticket contents.

## 2. What exactly is the OpenAI Agents SDK?

The **OpenAI API client SDK** (`pip install openai`) wraps model/platform endpoints such as the Responses API. You, the developer, can orchestrate your own tool loop on top of it. The **OpenAI Agents SDK** (`pip install openai-agents`) adds application-level orchestration primitives: agents, a runner/agent loop, tools, handoffs, sessions, guardrails, approval interruptions and tracing. For OpenAI models, the Agents SDK uses the Responses API by default. These are related but separate layers. [Official: Agents](https://openai.github.io/openai-agents-python/agents/)

```text
+----------------------------------------+
| Your application / REST API / web UI   |
+----------------------------------------+
                    |
                    v
+----------------------------------------+
| OpenAI Agents SDK                       |
| Agent / Runner / Tools / State / Trace |
+----------------------------------------+
                    |
                    v
+----------------------------------------+
| Model provider / Responses API          |
+----------------------------------------+
```

### 2.1 Core vocabulary

| Term | Plain-English meaning | Architecture implication |
|---|---|---|
| `Agent` | Model with instructions and optional tools/handoffs/output type | Define one task boundary clearly |
| `Runner` | Executes the agent loop | Loop/stop rules matter |
| Tool | Callable capability exposed to model | Tool implementation needs validation and authorization |
| Handoff | Transfer active control to specialist | Receiver may see prior conversation; filter sensitive history |
| Agent as tool | Specialist called by manager | Manager retains responsibility for final response |
| `RunContextWrapper` | Context object available to your Python code | Keep identity/credentials out of model messages |
| Session | SDK-managed conversation history | Not an authoritative business database |
| Guardrail | SDK validation mechanism | Not a replacement for business policy checks |
| Run interruption | Execution paused for approval | Requires trusted identity, durable state, and resume |
| Trace / span | Recorded execution timeline | Must apply sensitive-data controls |

### 2.2 What the SDK does *not* give you automatically

It does not establish who may read a record, guarantee true business facts, make a tool idempotent, decide safe retry policy, secure every external MCP server, provide your tenancy model, or turn every step into a crash-proof distributed workflow. Your own backend still owns these responsibilities.

### 2.3 When *not* to use Agents SDK

- Fixed classification with a few labels: use a structured model call and deterministic routing.
- Fetch-and-display an exact known ID: direct API may be simpler and cheaper.
- A strict financial approval path: use a workflow/state machine for side effects; optionally use an agent for proposals.
- A long-running cross-service process requiring contractual retries: integrate a durable orchestrator; do not rely only on an in-memory agent loop.

## 3. Anatomy of an agent run

```text
+-------------+      +--------------+      +------------------+
| User input  | ---> | Runner       | ---> | Agent + model    |
+-------------+      +--------------+      +------------------+
                          ^                       |
                          |                       v
                          |                 +-------------+
                          +---------------- | Tool call?  |
                             tool result    +-------------+
                                                |
                                             final answer
                                                v
                                         +---------------+
                                         | RunResult     |
                                         +---------------+
```

The runtime commonly calls the model, executes a selected tool or handoff, returns relevant output to the model, and repeats until final output, approval interruption or error. **The model proposes which tool to call; application code enforces what the tool actually does.** A tool must reject unacceptable or unauthorized arguments even if the model selected it confidently.

**Key limits to define:** number of turns, tool timeouts, maximum records returned, input size, total cost budget, and “insufficient evidence” exit behavior. `Runner.run` supports a `max_turns` parameter; do not assume a vague prompt alone can enforce a hard limit. [Official: Running agents](https://openai.github.io/openai-agents-python/running_agents/)

## 4. Installation and project setup

### 4.1 Python setup

```bash
mkdir agents-sdk-lab
cd agents-sdk-lab
python -m venv .venv
source .venv/bin/activate         # macOS / Linux
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install 'openai-agents>=0.24.0,<0.25.0' pydantic
python -m pip show openai-agents
```

The pinned range is a **study reproducibility choice**, not a claim that future versions are incompatible. The official quickstart uses `pip install openai-agents`. For production, pin the **resolved exact version in a lock file** after testing. [Official: Quickstart](https://openai.github.io/openai-agents-python/quickstart/)

```bash
export OPENAI_API_KEY='YOUR_DEVELOPMENT_KEY'
# Windows PowerShell: $env:OPENAI_API_KEY='YOUR_DEVELOPMENT_KEY'
```

**Do not** commit keys, put them into HTML, pass them through a browser, or embed them inside agent prompt text. Backends should load secrets from a protected environment or secrets manager. Check your account’s supported model IDs in official model documentation; examples here omit explicit `model=` unless a specific capability requires one.

### 4.2 Folder layout

```text
agents-sdk-lab/
|-- app.py                    # first agent
|-- ticket_agent.py           # tools + authorization
|-- mock_business_service.py  # deterministic fake data
|-- test_business_service.py  # no API key needed
|-- requirements.txt          # pinned by your own lock process
`-- README.md
```

## 5. First working agent

Save this as `app.py`. It calls a live model, so it needs an API key and may incur charges.

```python
import asyncio
from agents import Agent, Runner

agent = Agent(
    name="Plain English Assistant",
    instructions=(
        "Explain concepts in simple English. "
        "If you lack facts, say what is missing."
    ),
)

async def main() -> None:
    result = await Runner.run(
        agent,
        "What is the difference between an API and an SDK?",
        max_turns=3,
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

**Observe:** `Agent(...)` defines behavior. `Runner.run(...)` executes it. `result.final_output` is the final answer. Nothing here is multi-agent, MCP, RAG, or durable workflow orchestration. Start simple. To test the script, run `python app.py` after selecting valid credentials/model configuration.

## 6. Prompt and agent configuration

Agents can have a `name`, `instructions`, `model`, `model_settings`, `tools`, `handoffs`, `output_type`, `mcp_servers`, `input_guardrails`, `output_guardrails`, and hooks. Avoid stuffing business permissions into instructions alone. [Official: Agents](https://openai.github.io/openai-agents-python/agents/)

**Better instructions are operational:**

```python
from agents import Agent

support_agent = Agent(
    name="Ticket Reader",
    instructions=(
        "Help operators understand ticket records. "
        "Use get_ticket for facts; never invent status or ownership. "
        "When the tool reports denied or missing, explain that plainly. "
        "Do not claim to close or update tickets."
    ),
)
```

**Prompt design rules:** define the job, allowed data, output form, unknown/error behavior and when to stop. Keep short-lived record values in tools rather than large static prompts. Treat retrieved documents, webpages, logs, and tool results as **untrusted data**: they may contain text that looks like instructions.

### 6.1 Model choice

Choose by **measured task quality, latency, compatibility and cost**, not by naming convention or parameter count. Some model/tool features vary by model and API. Run an evaluation before changing a model in production. For current model support, use [official OpenAI model documentation](https://developers.openai.com/api/docs/models).

## 7. Function tools: the first useful agent architecture

A tool is a named, typed function the model may ask the runtime to invoke. The SDK derives tool argument schemas from Python types/docstrings. [Official: Tools](https://openai.github.io/openai-agents-python/tools/)

```python
import asyncio
from agents import Agent, Runner
from agents.decorators import tool

TICKETS = {
    "T-100": {"status": "open", "summary": "Checkout errors"},
    "T-101": {"status": "resolved", "summary": "Password reset"},
}

@tool
def get_ticket(ticket_id: str) -> dict:
    """Read a synthetic support ticket by exact ID."""
    record = TICKETS.get(ticket_id)
    if record is None:
        return {"status": "not_found", "ticket_id": ticket_id}
    return {"ticket_id": ticket_id, **record}

agent = Agent(
    name="Ticket reader demo",
    instructions="Use get_ticket for ticket facts; do not invent records.",
    tools=[get_ticket],
)

async def main() -> None:
    result = await Runner.run(agent, "What happened in T-100?", max_turns=4)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

**Important:** This is a **single-user fake-data lab**. Do *not* copy its globally accessible `TICKETS` dictionary into a multi-tenant service. The production service must derive user/tenant identity from verified backend context and check record-level permission before reading or returning data.

### 7.1 Good tool contracts

Use a name that describes one capability, typed arguments, a bounded response shape, explicit error codes, and no hidden side effects. Prefer a structured business response:

```json
{
  "ticket_id": "T-100",
  "status": "open",
  "summary": "Checkout errors",
  "observed_at": "2026-11-06T12:00:00Z",
  "source": "ticket-service",
  "result": "ok"
}
```

This is an **illustrative business JSON contract**, not an SDK wire-protocol message. Errors should distinguish `not_found`, `forbidden`, `upstream_timeout` and `temporarily_unavailable` where safe; avoid leaking existence of restricted records if your policy forbids it.

### 7.2 Tool error and timeout behavior

The documented `@tool(timeout=...)` applies to async function-tool handlers; a timed-out tool can return model-visible error text or raise, depending on configuration. A timeout is not proof that a remote write failed. For writes, always reconcile provider state before retrying. [Official: Tools, timeouts](https://openai.github.io/openai-agents-python/tools/)

## 8. Separating model input from local execution context

**Local context** is app-owned data passed to tool code through `RunContextWrapper`. It is *not itself given to the LLM*. Model-visible context is different: prompts, messages, tool schemas and tool results. Never assume local context protects values if your tool subsequently returns them to the model. [Official: Context management](https://openai.github.io/openai-agents-python/context/)

```python
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper
from agents.decorators import tool

@dataclass
class RequestContext:
    user_id: str       # authenticated server-side
    tenant_id: str     # authenticated server-side

# Mock authorization table; a real system uses trusted service policy.
ALLOWED = {("tenant-A", "operator-7", "T-100")}

@tool
def get_secure_ticket(
    ctx: RunContextWrapper[RequestContext], ticket_id: str
) -> dict:
    """Read one ticket only when backend policy permits it."""
    key = (ctx.context.tenant_id, ctx.context.user_id, ticket_id)
    if key not in ALLOWED:
        return {"result": "denied"}
    return {"result": "ok", "ticket_id": ticket_id, "status": "open"}

secure_agent = Agent[RequestContext](
    name="Secure ticket reader",
    instructions="Look up ticket records. Report denied records as unavailable.",
    tools=[get_secure_ticket],
)

# Example use inside an authenticated server request:
# result = await Runner.run(
#     secure_agent, "Read T-100",
#     context=RequestContext(user_id="operator-7", tenant_id="tenant-A"),
# )
```

**Trust rule:** only the backend creates `RequestContext` after authentication. Do not create it from `user_id` or `tenant_id` proposed by an LLM or sent unverified by a browser. An authorization decision should also account for current policy and record ownership, not just a static allowlist.

# Part II — Reliable agent behavior and state

## 9. Structured outputs and typed contracts

Use a typed output when downstream code expects data, not prose. A Pydantic model with `Agent(output_type=...)` gives a typed final result that your code can validate and handle. [Official: Agents, output types](https://openai.github.io/openai-agents-python/agents/)

```python
from typing import Literal
from pydantic import BaseModel
from agents import Agent, Runner

class TriageResult(BaseModel):
    team: Literal["billing", "technical", "general"]
    priority: Literal["low", "medium", "high"]
    reason: str

triage = Agent(
    name="Ticket classifier",
    instructions="Classify synthetic support tickets into the given schema.",
    output_type=TriageResult,
)

# result = await Runner.run(triage, "Our checkout fails for everyone")
# classified: TriageResult = result.final_output
# assert classified.team in {"billing", "technical", "general"}
```

**Design boundary:** syntactically valid JSON is not a business decision. For instance, `priority='high'` must not automatically grant refund privileges. Apply deterministic rules and review before side effects.

## 10. Multi-turn conversations: session vs state vs memory

These three ideas are often confused:

| Concept | Stores | Does not prove |
|---|---|---|
| Session history | Conversation messages/tool context | Ticket truth or customer permissions |
| Workflow state | Current step, approvals, pending operations, operation IDs | Human identity unless verified |
| Long-term memory | Approved durable preferences/facts | Live status of an order |

The SDK supports manual history (`result.to_input_list()`), SDK sessions (`SQLiteSession`, Redis/SQLAlchemy and others), and server-managed continuation (`conversation_id` / `previous_response_id`). Choose **one** session/continuation strategy per run; a session cannot be combined with those run-level continuation options. [Official: Sessions](https://openai.github.io/openai-agents-python/sessions/)

```python
from agents import Agent, Runner, SQLiteSession

agent = Agent(name="Helper", instructions="Answer plainly.")
session = SQLiteSession("demo-thread-001")

# a = await Runner.run(agent, "My project is about tool safety", session=session)
# b = await Runner.run(agent, "Summarize my project topic", session=session)
```

**Production decisions:** who owns session IDs, retention period, encryption, deletion, tenant separation, summarization/compaction, and how resumed runs load the right session. Never treat conversation state as a high-integrity transaction log.

## 11. Streaming agent output and progress

`Runner.run_streamed()` yields a result with `stream_events()`. Raw response events include token-level model updates; run-item events describe completed tool/handoff/message items. Consume the iterator until it ends before assuming run bookkeeping is complete. [Official: Streaming](https://openai.github.io/openai-agents-python/streaming/)

```python
import asyncio
from agents import Agent, Runner

agent = Agent(name="Explainer", instructions="Explain in two short paragraphs.")

async def main():
    result = Runner.run_streamed(agent, "Why is authorization server-side?")
    async for event in result.stream_events():
        if event.type == "run_item_stream_event":
            print(f"event: {event.name}")
        elif event.type == "agent_updated_stream_event":
            print(f"active agent: {event.new_agent.name}")
    print("final:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

**UI design:** do not expose raw sensitive tool payloads to the browser. Provide user-facing statuses such as “searching tickets”, “waiting for approval”, “completed”, “needs review” and “unknown remote outcome”. Streaming is an interface/experience pattern, not a guarantee of durable execution.

## 12. Run results, failures, and stopping rules

A run may produce final output, tool items, handoffs, or approval interruptions. Understand `final_output`, `last_agent`, run items, and the run-state checkpoint APIs. Common failures include model/provider errors, tool timeouts, max turns, invalid tool args, blocked guardrails, and pending approvals. [Official: Results](https://openai.github.io/openai-agents-python/results/)

**Recommended policy:**

1. Cap model turns using `max_turns` and tool-specific time budgets.
2. Return safe machine-readable failures from deterministic tools.
3. Log an internal correlation ID without exposing secret payloads.
4. Never silently transform `forbidden` or `timeout` into invented results.
5. For operations with side effects, use a persisted operation ID and status reconciliation.

The difference between an **error** and an **unknown outcome** matters. A timed-out refund provider could have processed the refund; repeating it without reconciliation can duplicate the payment.

## 13. Input, output, and tool guardrails

The SDK provides guardrails around agent inputs and outputs, plus tool guardrails for eligible function tools. An agent-level input guardrail applies to the first agent in the chain; the output guardrail applies to the final output. Tool guardrails apply around configured tool calls, not automatically to every hosted or built-in tool type. [Official: Guardrails](https://openai.github.io/openai-agents-python/guardrails/)

```python
from agents import Agent, GuardrailFunctionOutput, input_guardrail

@input_guardrail(run_in_parallel=False)
def reject_empty_request(ctx, agent, user_input):
    blocked = isinstance(user_input, str) and not user_input.strip()
    return GuardrailFunctionOutput(
        output_info={"reason": "empty input" if blocked else "ok"},
        tripwire_triggered=blocked,
    )

agent = Agent(
    name="Validated reader",
    input_guardrails=[reject_empty_request],
)
```

This example illustrates input validation only. Blocking mode (`run_in_parallel=False`) is useful when a dangerous tool must not start before the input check finishes. **Neither guardrails nor prompt instructions replace authorization at the business API.** Never depend on an LLM guardrail as the only protection for payments, record access or destructive actions.

## 14. Human-in-the-loop (HITL) approvals

For a sensitive tool, the SDK can mark a call as requiring approval. The run exposes an interruption; your application presents a review screen, binds the decision to an authenticated approver and persists the pending request, then resumes the run. This is an application workflow, not an automatic business authorization guarantee. [Official: Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)

```python
from agents import Agent
from agents.decorators import tool

@tool(needs_approval=True)
async def propose_cancel_order(order_id: int) -> str:
    """Demonstration-only: simulate a cancellation after approval."""
    return f"Mock cancellation recorded for order {order_id}"

agent = Agent(
    name="Order change assistant",
    instructions="Request approval before order changes.",
    tools=[propose_cancel_order],
)
```

**Approval sequence** (logical, omitting SDK-specific serialization details):

```text
+-------------------------+
| Agent proposes action   |
+-------------------------+
             |
             v
+-------------------------+
| Persist pending request |
| operation ID + args     |
+-------------------------+
             |
             v
+-------------------------+
| Authenticated reviewer  |
| approves exact request  |
+-------------------------+
             |
             v
+-------------------------+
| Business policy check   |
| role + owner + limits   |
+-------------------------+
             |
             v
+-------------------------+
| Idempotent action       |
| audit + reconciliation  |
+-------------------------+
```

**Resumable SDK pattern:** use `result.interruptions`, obtain `state = result.to_state()`, apply `state.approve(interruption)` or reject, then resume via `Runner.run(agent, state, session=session)` (if using that session). The SDK supports pending approval serialization, but you must decide durable storage and trusted reviewer binding. Approval **screens** do not themselves authorize money movement.

## 15. Tracing and hooks

Tracing records model generations, function calls, handoffs and guardrails; a trace represents a workflow and spans are its steps. The Python SDK enables tracing by default, but privacy controls and export configuration must be reviewed. The official documentation states tracing is unavailable for organizations using the API under a Zero Data Retention policy. [Official: Tracing](https://openai.github.io/openai-agents-python/tracing/)

**Good trace fields:** request/run ID, tool name, elapsed time, outcome status, safe tenant hash, retry count, SDK/model version and token usage. **Avoid:** API keys, full access tokens, unnecessary PII, private retrieved documents and raw high-impact tool payloads.

```python
from agents import Agent, Runner, trace

agent = Agent(name="Triage", instructions="Classify briefly.")

# with trace("Ticket investigation", group_id="thread-001"):
#     result = await Runner.run(agent, "What should we inspect first?")
```

Do not assume adding a redaction trace processor before a separate exporter prevents leaks: the official tracing docs describe processor failure isolation. If export depends on successful redaction, make redaction and export one application-owned fail-closed step.

---
# Part III — Multi-agent, protocols, and orchestration

## 16. Multi-agent architecture: handoffs vs agents as tools

The fact that a system needs three skills does **not** prove it needs three agents. First try one agent with three bounded tools. Add a specialist when it has a genuinely different task, policy, tool set, model profile or ownership boundary. The SDK supports two important patterns. [Official: Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)

### 16.1 Handoff: specialist owns the next turn

```text
+------------------+
| User             |
+------------------+
         |
         v
+------------------+
| Triage agent     |
+------------------+
         |
   handoff chosen
         v
+------------------+
| Billing agent    |
| final responder  |
+------------------+
```

```python
from agents import Agent, Runner

billing = Agent(
    name="Billing Specialist",
    handoff_description="Handles billing questions",
    instructions="Answer billing questions; never authorize payments.",
)
technical = Agent(
    name="Technical Specialist",
    handoff_description="Handles technical incidents",
    instructions="Answer technical troubleshooting questions.",
)
triage = Agent(
    name="Triage",
    instructions="Transfer each case to the best specialist.",
    handoffs=[billing, technical],
)

# result = await Runner.run(triage, "My card was charged twice")
# print(result.last_agent.name, result.final_output)
```

**Trade-off:** specialists can have focused instructions, but the new agent may receive previous history. Filter or minimize handoff history when sensitive fields should not cross the boundary. A handoff inside the SDK is **not** the same as A2A delegation to another independently operated service. [Official: Handoffs](https://openai.github.io/openai-agents-python/handoffs/)

### 16.2 Manager pattern: specialist is a tool

```text
+-----------------------+
| Manager agent         |
+-----------------------+
       |         |
       v         v
+----------+  +----------+
| Billing  |  | Policy   |
| helper   |  | helper   |
+----------+  +----------+
       |         |
       +----+----+
            |
            v
+-----------------------+
| Manager combines      |
| grounded answer       |
+-----------------------+
```

```python
from agents import Agent

billing = Agent(name="Billing Analyst", instructions="Analyze mock charges.")
policy = Agent(name="Policy Analyst", instructions="Analyze cited mock policies.")
manager = Agent(
    name="Case Manager",
    instructions="Use specialists for evidence; produce the final answer yourself.",
    tools=[
        billing.as_tool(
            tool_name="analyze_billing",
            tool_description="Analyze a billing issue without changing records",
        ),
        policy.as_tool(
            tool_name="analyze_policy",
            tool_description="Explain policy evidence",
        ),
    ],
)
```

**Choose handoff** when the specialist should directly own the conversation. **Choose agent-as-tool** when one manager must integrate several findings. **Choose ordinary Python functions** for simple deterministic helpers; agents add model calls, latency and evaluation burden.

### 16.3 Parallelism and manager control

You can coordinate parallel independent queries with normal Python concurrency (`asyncio.gather`) where appropriate, rather than turning every branch into another agent. Bound concurrency to protect upstream systems. A model deciding “parallel” does not remove the need for dependency checks and failure handling.

## 17. MCP: integrating reusable external tools

**MCP (Model Context Protocol)** connects hosts/clients to tools, resources and prompts exposed by MCP servers. The Agents SDK can integrate hosted MCP tools and local/client-managed servers. MCP is a **tool/data interoperability** boundary, not a frontend UI protocol and not the same thing as an SDK handoff. [Official: MCP in Agents SDK](https://openai.github.io/openai-agents-python/mcp/)

```text
+------------------------+
| Python agent runtime   |
| MCP client             |
+------------------------+
             |
             | MCP request/response
             v
+------------------------+
| Ticket MCP server      |
| get_ticket, search     |
+------------------------+
             |
             v
+------------------------+
| Authorized ticket API  |
+------------------------+
```

### 17.1 Choose the MCP integration

| Requirement | SDK option | Important concern |
|---|---|---|
| Local tool server process | `MCPServerStdio` | Process limits, trust and tool filtering |
| Remote endpoint managed by your application | `MCPServerStreamableHttp` | Authentication, endpoint trust, timeouts |
| Existing HTTP + SSE server | `MCPServerSse` | Compatibility with server transport |
| OpenAI-managed hosted MCP calls | `HostedMCPTool` | Provider availability, approval/data flow |

**Illustrative connected-server code** (requires a *real compatible server* at the specified URL and a valid token):

```python
import asyncio, os
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

async def main():
    async with MCPServerStreamableHttp(
        name="Ticket MCP",
        params={
            "url": "http://localhost:8000/mcp",
            "headers": {"Authorization": f"Bearer {os.environ['MCP_SERVER_TOKEN']}"},
            "timeout": 10,
        },
        cache_tools_list=True,
    ) as server:
        agent = Agent(
            name="Ticket investigator",
            instructions="Use MCP ticket tools only for facts.",
            mcp_servers=[server],
        )
        result = await Runner.run(agent, "Inspect ticket T-100")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

**What to test:** connection refusal, invalid token, missing tool, incompatible schema, forbidden ticket, stale cached tool catalog, prompt injection returned by an MCP tool, and timeout/retry behavior. **Never** let an MCP tool trust `user_id` from model arguments as proof of identity; the MCP server should use verified credentials and record-level checks.

### 17.2 MCP vs MCP Apps vs AG-UI vs A2A

| Technology | Main purpose | Typical boundary |
|---|---|---|
| MCP | Reusable tools/resources/prompts | Agent host/client ↔ MCP server |
| MCP Apps | Embedded HTML UI inside compatible AI host | Host ↔ sandboxed app view associated with MCP tools |
| AG-UI | Agent events/state to owned frontend | Agent runtime ↔ web UI |
| A2A | Delegation between independently deployed agents | Remote agent ↔ remote agent |
| Agent Skills | Reusable procedural instructions | Skill package ↔ agent context/runtime |

The **Agents SDK does not automatically make a tool result into an MCP App**. MCP Apps requires a compatible host and the optional UI extension. Likewise, an SDK handoff is internal orchestration; cross-organization A2A requires a separately designed protocol/service integration. For UI rendering, the application/host still owns trusted component handling and permissions. [Official: MCP Apps](https://github.com/modelcontextprotocol/ext-apps), [AG-UI](https://github.com/ag-ui-protocol/ag-ui), [A2A](https://a2a-protocol.org/)

## 18. Retrieval (RAG), evidence, and source truth

An agent can answer from retrieved evidence, but **retrieval** and **memory** solve different problems. RAG finds approved source passages; a session maintains conversation turns; the business service owns authoritative current records.

```text
+-----------------------+
| Authorized question   |
+-----------------------+
            |
            v
+-----------------------+
| ACL-aware retrieval   |
+-----------------------+
            |
            v
+-----------------------+
| Cited passages        |
| source + version      |
+-----------------------+
            |
            v
+-----------------------+
| Agent synthesizes     |
| or abstains           |
+-----------------------+
```

**Retrieval options:** a local approved search tool, the Responses API `FileSearchTool` when its store/governance matches the requirement, or your enterprise retrieval service exposed as a Python function/MCP tool. Choosing a tool does not decide whether permissions, freshness and citations are valid. [Official: Tools](https://openai.github.io/openai-agents-python/tools/)

**Correct evidence contract:** `source_id`, passage ID, effective date, last indexed time, access scope and matched text. Validate final citations against the passages actually retrieved. If nothing is sufficient, answer “not supported by the available approved evidence.”

**Failure scenario:** Engineering user searches an index containing HR-only policy. Filter by verified ACL **before** the text reaches the model. Post-generation filtering is too late.

## 19. Deterministic orchestration vs adaptive agent loops

Many production workflows are **hybrid**: a deterministic controller chooses the approved sequence; one or more agents perform narrow extraction/analysis steps. For example, approval, eligibility and payment execution are deterministic; drafting a readable recommendation may be model-driven.

| Pattern | Best for | Main risk |
|---|---|---|
| One prompt | Explanation, format conversion | Grounding limits |
| One agent + tools | Flexible lookup and investigation | Loops, uncontrolled calls |
| Agent handoff | Focused specialist dialogue | Context disclosure and ownership |
| Manager + specialists | Evidence from distinct specialties | Cost and compounded errors |
| Deterministic state machine | Payments, approvals, onboarding | More explicit engineering |
| Durable workflow engine + agent tasks | Days-long or crash-recoverable operations | Platform complexity |

**Avoid confusing `Session` with a durable workflow engine.** A conversation log alone is not enough to prevent duplicate writes or resume a transaction after a lost network response. The SDK documentation discusses durable execution integrations (e.g., Temporal and others), but you still need explicit workflow and side-effect contracts. [Official: Running agents](https://openai.github.io/openai-agents-python/running_agents/)

### 19.1 Explicit state machine for high-impact changes

```text
+----------+     +----------+     +-----------+
| PROPOSED | --> | APPROVED | --> | EXECUTING |
+----------+     +----------+     +-----------+
                        |                |
                        v                v
                   +----------+    +-----------+
                   | REJECTED |    | COMPLETED |
                   +----------+    +-----------+
                                         ^
                                         |
                                    +---------+
                                    | UNKNOWN |
                                    +---------+
```

**Critical invariant:** `UNKNOWN` does not imply `FAILED`. A reconciliation operation should determine whether the external side effect happened. Do not automatically re-run a payment, refund, send or delete after an ambiguous timeout.

## 20. Agentic UI: model output is not a UI authorization decision

There are three common UI approaches for an Agents SDK backend:

1. **Plain HTML frontend:** your API returns approved JSON. The frontend renders known components. Simple, clear and easy to print.
2. **Streaming UI:** the backend translates approved agent events into app-specific SSE/WebSocket messages, or uses a compatible protocol such as AG-UI.
3. **Embedded AI-host UI:** if the host supports MCP Apps, an MCP tool can be associated with a sandboxed interactive view. This is not provided by `Agent` alone.

For all three, backend authority remains separate from display:

```text
+---------------------------+
| Agent proposes next step  |
+---------------------------+
              |
              v
+---------------------------+
| HTML button / app view    |
| user reviews             |
+---------------------------+
              |
              v
+---------------------------+
| Backend authenticates +   |
| authorizes exact action   |
+---------------------------+
              |
              v
+---------------------------+
| Business service commits  |
+---------------------------+
```

**Do not** consider a rendered “Approve” button, streamed `approved=true` field or text in a tool response to be proof of authorization. Require a trusted identity, exact action/resource/amount binding, expiry, state validation and idempotency. These rules remain true with MCP Apps, AG-UI, or a proprietary frontend.

# Part IV — Production architecture and advanced capabilities

## 21. Authentication and authorization architecture

A production app usually has several identities: the human operator, your application service, the model API credential, and any downstream SaaS/MCP credentials. Keep these separate. The **system of record** makes the final record-level authorization decision.

### 21.1 Read request sequence

```text
Operator -> Backend: GET /ask?question=... (session cookie / token)
Backend  -> Identity: verify subject, tenant, role
Backend  -> Runner: start run with local authenticated context
Runner   -> get_ticket: model-selected ticket_id
Tool     -> Ticket API: user/tenant-scoped authorized read
Ticket   -> Tool: permitted record or safe denial
Tool     -> Runner: validated result
Runner   -> Backend: grounded reply
Backend  -> Operator: final response
```

**What is never an authority source:** prompt text (“I am the admin”), a document’s instruction, a model-generated role, an iframe local variable, or a handoff agent’s own claim about permissions.

### 21.2 Essential negative tests

- User A requests User B’s record: denied.
- Model passes a different `tenant_id`: ignored or rejected.
- Session with prior access resumes after revocation: fresh service check denies.
- MCP server returns instruction to call delete tool: tool policy blocks it.
- Approval is changed after review: backend rejects modified action.

## 22. Prompt injection, tools, and supply-chain security

**Prompt injection** occurs when lower-trust text tries to alter agent behavior: ticket notes, retrieved PDFs, webpage text, tool responses or third-party skill files can contain hostile “instructions”. Labels in a prompt help the model, but **enforcement belongs in code and service policy**.

**Defense design:** minimize privileged tools → allowlist permitted tool types → check args/identity on every call → sandbox untrusted code/file tools → redact sensitive context → review third-party MCP servers/skills → log decisions → evaluate injected cases. For destructive actions, use human approval **plus** business-level validation.

| Threat | Agent-only mitigation (weak) | Enforced mitigation |
|---|---|---|
| Document says “ignore prior rules” | Prompt warns not to obey | Tool cannot take unauthorized action |
| Model guesses restricted ticket ID | Model says “check owner” | Backend checks identity+record ACL |
| Tool response includes credential | Ask model not to repeat it | Strip/redact sensitive fields before model/UI |
| Duplicate write after retry | Model told “only once” | Stable idempotency key + ledger + reconciliation |
| Malicious plugin/skill | Trust its description | Approved registry, review, isolation |

## 23. Testing and evaluation

Separate **software correctness** from **model quality**.

### 23.1 Tests by layer

| Layer | Test | Example expected result |
|---|---|---|
| Business tool (offline) | AuthZ logic | Cross-user read denied |
| Tool contract | Type/schema checks | Invalid ticket ID rejected |
| Run behavior | Tool failure injection | No fabricated success |
| Output | Typed schema validation | Known fields parsed |
| Retrieval | Grounding/citation test | Source IDs actually exist |
| Agent quality | Scenario-level evaluator | Answer backed by approved evidence |
| Recovery | Crash/retry simulation | At most one logical refund |
| Security | Prompt injection attempt | Forbidden tool effect blocked |
| UI | Approval/expiry checks | Stale approval denied |

The SDK has a [Testing guide](https://openai.github.io/openai-agents-python/testing/); keep deterministic unit tests in normal Python test runners, and add representative model evaluations before release.

### 23.2 A small **offline** mock with real software tests

`mock_business_service.py` (no model or key required):

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Principal:
    user_id: str
    tenant_id: str

# Synthetic records only.
RECORDS = {
    "T-100": {"tenant_id": "A", "owner_id": "u1", "status": "open"},
    "T-200": {"tenant_id": "B", "owner_id": "u2", "status": "closed"},
}

def read_ticket(principal: Principal, ticket_id: str) -> dict:
    record = RECORDS.get(ticket_id)
    if record is None:
        return {"result": "not_available"}
    if (record["tenant_id"], record["owner_id"]) != (
        principal.tenant_id, principal.user_id
    ):
        return {"result": "not_available"}
    return {"result": "ok", "ticket_id": ticket_id,
            "status": record["status"]}
```

`test_business_service.py` (Python standard library):

```python
import unittest
from mock_business_service import Principal, read_ticket

class TicketPolicyTests(unittest.TestCase):
    def test_authorized(self):
        self.assertEqual(
            read_ticket(Principal("u1", "A"), "T-100")["status"], "open"
        )

    def test_cross_tenant_denied(self):
        self.assertEqual(
            read_ticket(Principal("u1", "A"), "T-200")["result"],
            "not_available"
        )

    def test_unknown_not_invented(self):
        self.assertEqual(
            read_ticket(Principal("u1", "A"), "T-999")["result"],
            "not_available"
        )

if __name__ == "__main__":
    unittest.main()
```

Run `python -m unittest -v`. Notice that the critical authorization policy works and can be tested **without any language model**. The agent tool should delegate to such a service, not reimplement policy through instructions.

### 23.3 An evaluation dataset

For an incident assistant, create a versioned JSONL set with `input`, permitted evidence IDs, expected tool behavior, forbidden effect list and success rubric. Measure **task completion**, **grounding/citation precision**, **authorization violation rate**, **unnecessary tool calls**, **latency** and **cost**, instead of only checking if the answer sounds good. Include “no evidence”, “upstream unavailable” and “malicious retrieved text” cases.

## 24. Observability, cost and service health

The SDK has traces and token usage. Build operational monitoring around the **business journey**, not only model calls.

| Metric | Why it matters | Example alert/test |
|---|---|---|
| End-to-end task success | Actual user outcome | Fall in grounded completion rate |
| Tool error rate | Upstream service health | Ticket API 5xx spike |
| p50/p95 visible latency | Responsiveness | Approval UI pending too long |
| Tokens/requests per task | Cost | Unexpected extra agent loops |
| Guardrail/policy denials | Safety/false positives | New prompt injection attempts |
| Unsupported-claim rate | Quality | Citation regression |
| Human correction rate | Quality drift | Increase after model update |
| Duplicate operation count | Side-effect correctness | Any second refund for one operation ID |

**Trace correlation:** carry a request ID across web API, Runner, business tools and external services. Attach safe metadata; minimize or avoid raw prompts/results in exported traces when data sensitivity requires it. If no trace exporter can meet required data policy, disable or replace it deliberately rather than assuming defaults are safe. [Official: Tracing](https://openai.github.io/openai-agents-python/tracing/)

## 25. Latency, scale and cost

An agent may do multiple model and tool calls per request. A simple one-shot prompt often has lower latency and cost than a multi-agent workflow. Make architecture changes only when measured requirements demand them.

**Reduce cost/latency safely:** narrow prompts and tool schemas; return compact structured tool results; defer large tool catalogs when supported; use a suitable model per task; bound turns/concurrency; cache non-sensitive and non-user-specific read results with explicit freshness; batch independent work carefully; add retrieval only when needed. Cache scope must include tenant, identity/access policy and version where relevant. Never cache a user’s authorized response for a different user by mistake.

**Budget model** (illustrative, not an OpenAI price quote):

```text
Cost per successful task
  = model request/response costs
  + hosted tool costs (when applicable)
  + external API / infrastructure costs
  + retry & failed-run overhead
```

Collect actual usage and provider pricing before making a cost claim. For planning, calculate **cost per grounded successful task**, not just cost per request. [Official: Usage](https://openai.github.io/openai-agents-python/usage/)

## 26. Durability, retries and unknown outcomes

A reliable production service needs application-owned durable records for pending actions, approvals, external operation IDs and reconciliation. Session history and streamed messages do not prove what happened in the business service.

### 26.1 Failure/recovery sequence

```text
+--------------------------+
| User approved refund     |
+--------------------------+
             |
             v
+--------------------------+
| Save operation ID        |
| refund-ORD17-v1          |
+--------------------------+
             |
             v
+--------------------------+
| Send to mock provider    |
+--------------------------+
             |
          timeout
             v
+--------------------------+
| Mark outcome UNKNOWN     |
+--------------------------+
             |
             v
+--------------------------+
| Query provider by ID     |
+--------------------------+
       |             |
    found           absent
       |             |
       v             v
+----------+   +----------------+
| Record   |   | Policy decides |
| success  |   | retry / review |
+----------+   +----------------+
```

**Rules:** persist before side effect; use a stable idempotency key; reconcile after ambiguous failures; cap retries; do not let the model choose arbitrary operation IDs; keep an audit trail of proposal, approval, execution and provider evidence. For long-lived workflows, consider a durable orchestrator rather than keeping one Python process alive indefinitely.

## 27. Advanced SDK capabilities: choose only when needed

### 27.1 Sandbox agents and code editing

The documented **SandboxAgent** path adds workspace-oriented execution with manifests, filesystem/shell capabilities, sandbox clients and resumable workspace state. It is useful for coding assistants, research over files, patch/test loops and artifact generation. It creates **new security boundaries**: filesystem scope, network egress, code execution, secrets, dependency supply chain and review before merge. [Official: Sandbox agents](https://openai.github.io/openai-agents-python/sandbox_agents/)

**Use case:** inspect a toy repository, propose a patch, run unit tests inside an isolated workspace, show diff, require human review before merge. Do not let a sandbox with real credentials access production systems by default.

### 27.2 Voice pipelines vs realtime agents

**Voice pipeline:** speech-to-text → agent/workflow → text-to-speech. Useful for spoken interfaces when modest latency is acceptable. The SDK documents `VoicePipeline` and `SingleAgentVoiceWorkflow`. **Realtime agents:** persistent realtime session and incremental audio/text, supporting interruptions and tool calls. Python Realtime transport is server-side WebSocket/SIP, not browser WebRTC. [Official: Voice quickstart](https://openai.github.io/openai-agents-python/voice/quickstart/), [Realtime guide](https://openai.github.io/openai-agents-python/realtime/guide/)

Choose based on interaction latency, audio quality, interruptions, privacy/retention and integration needs; do not assume both have identical APIs.

### 27.3 Hosted tools and tool search

The Agents SDK documents OpenAI-hosted tools for supported models, including web/file search, code interpreter, hosted MCP and other provider-backed capabilities. Availability and exact arguments depend on model/SDK version. Tool search can reduce exposure of very large tool catalogs when supported. A hosted tool may execute outside your application process, so explicitly review **data flow, trust, approvals and observability**. [Official: Tools](https://openai.github.io/openai-agents-python/tools/)

### 27.4 Agent Skills and reusable procedures

Agent Skills package repeatable procedural guidance, often using a `SKILL.md` entry and supporting resources. This is different from an API: skills tell an agent **how** to work; tools let it access capabilities; business services decide **what is authorized**. For a coding sandbox, study the SDK’s Skills capability after basic agent/tool patterns. [Official: Sandbox concepts](https://openai.github.io/openai-agents-python/sandbox/guide/)

### 27.5 A2A interoperability

If another team runs its own remote agent with independent task lifecycle and ownership, consider a verified A2A adapter or service integration. In-process `Agent.as_tool()` and handoffs do not themselves create an A2A-compliant service. Verify the chosen A2A implementation against its official protocol version; authenticate the remote service, validate agent metadata and artifacts, and minimize disclosed case data. [Official: A2A](https://a2a-protocol.org/)

## 28. Deployment reference architecture

```text
+--------------------------+
| Browser / chat client    |
+--------------------------+
             |
             v
+--------------------------+
| API gateway + identity   |
+--------------------------+
             |
             v
+--------------------------+
| App service              |
| intent, run ID, policy   |
+--------------------------+
             |
             v
+--------------------------+
| Agent SDK Runner         |
| bounded tools / traces   |
+--------------------------+
        |            |
        v            v
+--------------+  +-------------------+
| Read tools   |  | Draft/approval    |
| / retrieval  |  | workflow service  |
+--------------+  +-------------------+
        |            |
        v            v
+--------------+  +-------------------+
| Governed     |  | Business write    |
| data APIs    |  | API + action log  |
+--------------+  +-------------------+

Cross-cutting: authZ, secret management, tracing,
rate control, evaluation, audit, cost budgets.
```

### 28.1 Component ownership

| Component | Owns | Must not assume |
|---|---|---|
| Browser | Display and local form state | “Approve” UI alone authorizes effect |
| API gateway | Identity verification / request admission | Model-generated user ID is trusted |
| Agent runtime | Language decisions, tool selection, run events | Business record is true without source |
| Read service | Actual data and per-record access | Tool schema grants permission |
| Approval service | Pending action, reviewer, expiry, binding | Session text is an audit log |
| Write service | Final policy, idempotency, effect | Timeout means no effect |
| Observability | Correlated operational evidence | Raw traces are privacy-safe by default |

### 28.2 Common production decisions

- **Availability:** fail safely if identity or policy service is unavailable.
- **Scaling:** keep stateless API workers where possible; put durable action state in a database/queue.
- **Tenancy:** scope sessions, caches, credentials, search and logs by verified tenant.
- **Versioning:** pin/test SDK, model, prompt, tool schemas and MCP compatibility together.
- **Deployment:** use staged rollout; compare candidate vs baseline on a fixed evaluation set and representative traffic.
- **Disaster recovery:** restore state and reconcile unknown remote effects before resuming writes.

## 29. Architecture decision handbook

Use the simplest option that meets the business requirement:

| If you need… | Usually start with… | Evolve to… only if… |
|---|---|---|
| One formatted answer | Direct Responses call | Agent if flexible tool loop is needed |
| Known record by ID | Direct authenticated API | Agent if dynamic lookup/explanation matters |
| Reusable tools across hosts | MCP | Governed MCP catalog as it scales |
| Multiple specialist tasks | One agent + tools | Handoff/agent-as-tool when ownership differs |
| Controlled business writes | State machine + approval | Durable orchestration for long workflows |
| Searchable documents | Permission-aware retrieval | Hybrid search/rerank after evaluation |
| Live frontend updates | SSE and known JSON | AG-UI for interoperable event semantics |
| App embedded in AI chat | Host-supported MCP Apps | Fallback when host lacks extension |
| Remote independently owned agent | Typed service API | A2A when task/agent interoperability matters |
| Workspace file/code work | Restricted sandbox | SandboxAgent for persistent tool-rich workflows |

**Architectural anti-patterns:** (1) using 5 agents when 1 agent and 2 APIs suffice; (2) treating prompts as authorization; (3) assuming every tool use requires MCP; (4) treating MCP Apps as a different name for AG-UI; (5) retrying side effects blindly; (6) ignoring version and model capability checks; (7) shipping without scenario evaluations.

---

# Part V — Detailed use cases and hands-on capstone

## 30. Use-case catalog and capstone

This chapter turns concepts into solution-architecture decisions. The records and business rules are intentionally **synthetic**. Each case states the source of truth, minimal design, production upgrades and where an SDK feature earns its place.

### Case A — FAQ support assistant (beginner)

**Problem:** Answer a customer’s return-policy question only from approved policy paragraphs. **Source of truth:** approved FAQ documents. **Start:** deterministic retrieval of one relevant answer and source ID. **Add SDK:** one grounded answer agent. **Production:** document version/freshness, ACL filtering, citation checks, abstention when no evidence. **Trade-off:** for a small exact FAQ, retrieval plus template formatting may be sufficient.

**Example request:** `Can I return an opened item?`  
**Expected contract:** `{"status":"grounded","source_ids":["faq-returns-01"],"answer":"..."}` or `{"status":"insufficient_evidence"}`.

### Case B — Ticket lookup agent (beginner → intermediate)

**Problem:** Operator asks about current ticket status. **Source of truth:** ticket service. **Start:** one `get_ticket` function tool with local fake data. **Add SDK:** type-aware tool selection, concise explanation, bounded turns. **Production:** backend identity, per-ticket access, tool timeout, structured error, full trace. **Trade-off:** a direct record API is cheaper when no flexible reasoning is needed.

### Case C — Ticket triage and routing (beginner)

**Problem:** New support text needs an assigned queue and priority. **Source of truth:** ticketing rules and approved queue taxonomy. **Start:** structured output model (`team`, `priority`, `reason`) and deterministic validation. **Production:** unknown category, confidence/abstention, monitoring misroutes and schema versioning. **Trade-off:** rules/classifiers are preferable for fixed phrases and contractual decision trees.

### Case D — Document Q&A with grounded retrieval (intermediate)

**Problem:** Employees search policies with citations. **Source of truth:** versioned, permission-controlled documents. **Start:** offline keyword retrieval + `source_id`; add an agent only to synthesize evidence. **Production:** hybrid retrieval, ACL prefilter, fresh index, citation validation and evidence evaluation. **Trade-off:** long context vs RAG depends on corpus size, updates and access controls.

### Case E — Refund proposal and human approval (intermediate → advanced)

**Problem:** Support agent proposes a refund; a reviewer authorizes a specific action. **Source of truth:** order and payments systems. **Start:** agent drafts `RefundProposal`, no write tool. **Add SDK:** approval interruption around a simulated tool. **Production:** persisted proposal, verified approver, eligible amount, expiry, idempotency key, reconciliation after timeout, immutable audit. **Trade-off:** never replace the deterministic payment workflow with an unconstrained agent loop.

**Illustrative business contracts:**

```json
{
  "proposal_id": "P-17",
  "order_id": "ORD-17",
  "amount_minor": 2500,
  "currency": "USD",
  "state": "pending_approval",
  "expires_at": "2026-11-06T20:00:00Z"
}
```

```json
{
  "operation_id": "refund-ORD-17-v1",
  "proposal_id": "P-17",
  "approver_subject": "reviewer-3",
  "decision": "approved",
  "approved_version": 1
}
```

**Failure to demonstrate:** processing succeeds at provider but response times out; application stores `unknown` then looks up the operation before retrying.

### Case F — IT incident investigator (advanced)

**Problem:** Operator asks “Why did checkout fail after deployment?” **Source of truth:** monitoring, change log, incident record and runbooks. **Start:** one bounded agent with read-only `get_metric` and `get_change` tools. **Add SDK:** streaming activity, possibly specialists for logs and changes. **Production:** query quotas, evidence timeline, source attribution, human approval before remediation, incident-linked traces. **Trade-off:** runbook-first deterministic steps vs model-led adaptive investigation.

**Request/response contract example:**

```json
{
  "incident_id": "INC-42",
  "time_range": {"start": "2026-11-06T10:00:00Z",
                 "end": "2026-11-06T11:00:00Z"},
  "requested_analysis": "suspected deployment regression"
}
```

```json
{
  "incident_id": "INC-42",
  "status": "needs_review",
  "hypotheses": [
    {"claim": "errors increased after release R7",
     "evidence_ids": ["metric-12", "change-R7"]}
  ],
  "authorized_action": "none"
}
```

### Case G — Analytics assistant and Generative UI (advanced)

**Problem:** Analyst asks for a quarter’s expenses and changes department filters. **Source of truth:** governed metric API. **Start:** one typed result: `period`, `department`, `categories`, `as_of`. **UI:** ordinary self-contained HTML renders a table/chart from trusted JSON. **MCP Apps alternative:** when a compatible AI host must embed the interactive view, add a separate MCP server linked to an approved UI resource. **Production:** per-department authorization and stale data handling. **Trade-off:** never generate unrestricted executable HTML and run it as authority.

### Case H — Code-editing / data analysis sandbox (advanced)

**Problem:** Investigate a test failure, propose a patch and generate a report. **Source of truth:** checked-out repository/tests or authorized input files. **Start:** isolated workspace with fake repo and no secrets. **Add SDK:** SandboxAgent and permissioned file/shell capabilities. **Production:** network allowlist, resource limits, dependency pinning, diff review, code scanning, human merge approval. **Trade-off:** model reasoning should recommend edits; test execution and merge authority remain deterministic.

### Case I — Realtime voice customer service (advanced)

**Problem:** Spoken ticket lookup with interruptions. **Source of truth:** customer/ticket APIs. **Start:** voice pipeline with typed read-only tools. **Move to realtime:** if incremental audio, latency and barge-in require a live connection. **Production:** identity verification, consent/retention, call handoff, cancellation behavior and transcript logging policy. **Trade-off:** simpler STT→agent→TTS pipeline vs more complex real-time media session.

### 30.1 Capstone — Enterprise ticket + incident assistant

**Business goal:** an operator asks about an incident, the assistant searches permitted ticket/metrics data, displays a factual summary, offers a remediation *proposal*, and requires approval before a mocked ticket update. Start with a single read-only agent. Add complexity only when specific requirements justify it.

**Phase 1 — Minimum:** one agent, `get_ticket`, `get_metric`, structured `InvestigationSummary`. Everything is synthetic. Build three failure fixtures: unknown ticket, unauthorized tenant and upstream timeout.

**Phase 2 — Evidence:** include `source_id`, `observed_at`, evidence list and abstention state. Reject citations not returned from authorized tools.

**Phase 3 — State:** introduce a session for chat history; keep workflow state separate in durable storage.

**Phase 4 — Proposal:** add a `propose_ticket_update` path that writes **only** a draft. A real backend validates the reviewer and commits the change with a stable operation ID.

**Phase 5 — Interoperability:** turn shared read tools into an MCP service only if a second compatible host needs them. For an embedded dashboard, evaluate MCP Apps host support; for a web-owned streaming frontend, compare plain SSE with AG-UI.

**Phase 6 — Operations:** add trace IDs, eval cases, safety tests, bounded retries, a release checklist and a recovery plan for unknown writes.

### 30.2 Capstone contract set

```python
# The following Pydantic types are application contracts, not an SDK API.
from typing import Literal
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    source_id: str
    observed_at: str
    claim: str

class InvestigationSummary(BaseModel):
    incident_id: str
    status: Literal["grounded", "insufficient_evidence", "needs_review"]
    findings: list[Evidence]
    recommended_action: str | None = None

class TicketUpdateDraft(BaseModel):
    ticket_id: str
    action: Literal["add_comment", "change_priority"]
    reason: str = Field(min_length=1, max_length=500)
    proposal_id: str
```

**Trust boundary note:** model-generated `proposal_id` is *not* trusted as an authoritative ID. The application creates its own ID after validating the suggestion. The same applies to ticket IDs, user IDs, and any model-generated approval status.

### 30.3 Deliverables for a solution-architecture portfolio

1. Context diagram with user, API, agent, business sources and trust boundaries.
2. One read-only request sequence and one approval/write sequence.
3. Typed JSON contracts and versioned API endpoints.
4. A simple offline tool and authorization test suite.
5. Screenshots or HTML views of grounded findings and denied/pending states.
6. Failure/recovery scenario for an ambiguous remote outcome.
7. Architecture decision records: direct API vs tool; single vs multi-agent; MCP vs direct; session vs workflow state; plain UI vs host-embedded UI.
8. Evaluation evidence, trace correlation design, cost/latency budget and deployment plan.

### 30.4 Example architecture decision record (ADR)

**Decision:** use one bounded ticket-investigation agent with two read-only function tools for the first release.  
**Reason:** flexible natural-language lookup is useful; shared multi-host tool interoperability is not yet required.  
**Rejected:** 3-agent supervisor and MCP gateway, because they add latency, failure modes and version maintenance without meeting a named requirement.  
**Risks:** hallucinated synthesis and tool timeouts.  
**Controls:** source IDs, explicit errors, authorization in tools, bounded turns and scenario evaluation.  
**Revisit when:** second AI host needs shared tools, or independently owned investigation specialist is introduced.

---

## 31. Troubleshooting and version-aware reference index

### 31.1 Typical setup and runtime problems

| Symptom | Most likely category | What to check first |
|---|---|---|
| `ModuleNotFoundError: agents` | Wrong virtual environment/package | Active interpreter, `pip show openai-agents` |
| Authentication failure | API key or project configuration | Environment key/permissions; never log key |
| Unsupported tool/model | Capability mismatch | Model docs and SDK guide for this feature |
| Model never calls tool | Instructions/tool discovery | Tool name/description, task relevance, trace |
| Model loops | Missing termination or ambiguous tool | `max_turns`, tool output clarity, tool-choice settings |
| Typed output rejected | Schema complexity/validation | Simplify schema, inspect model behavior |
| Forbidden record accidentally visible | Authorization missing | Verify server-side policy; block release |
| MCP connection refused | Transport/auth endpoint | Real endpoint, TLS/auth, server compatibility |
| UI says succeeded after timeout | Incorrect state model | Reconcile provider effect; show `unknown` |
| Too many tokens | Long history and tool output | Inspect usage, compact/context/retrieval strategy |
| Trace contains PII | Unsafe telemetry configuration | Stop export, redact, assess stored copies |

### 31.2 Version discipline

**Verified reference baseline:** OpenAI Agents SDK Python **v0.24.0 stable** was listed on its official public release page on November 6, 2026; API examples are drawn from official documentation checked the same day. A later prerelease exists. The lower-level `openai` Python SDK is a **different package** and has an independent release cadence. Do not copy code from mismatched versions without testing.

For a new project, record: SDK version and commit/release date; Python version; actual model ID; hosting environment; relevant MCP protocol/SDK version; agent prompt version; tool schema version; and evaluation dataset version. Re-check versions before upgrades or production rollout.

### 31.3 Official reading list

These are **official project/vendor sources**; prioritize them over unverified blog examples. URLs should be rechecked as SDK docs evolve.

| Subject | Official documentation |
|---|---|
| Python Agents SDK intro / quickstart | https://openai.github.io/openai-agents-python/quickstart/ |
| Agents/configuration/structured output | https://openai.github.io/openai-agents-python/agents/ |
| Runner and conversation management | https://openai.github.io/openai-agents-python/running_agents/ |
| Function, hosted and sandbox tools | https://openai.github.io/openai-agents-python/tools/ |
| SDK context | https://openai.github.io/openai-agents-python/context/ |
| Sessions and memory | https://openai.github.io/openai-agents-python/sessions/ |
| Streaming | https://openai.github.io/openai-agents-python/streaming/ |
| Agent orchestration | https://openai.github.io/openai-agents-python/multi_agent/ |
| Handoffs | https://openai.github.io/openai-agents-python/handoffs/ |
| Guardrails | https://openai.github.io/openai-agents-python/guardrails/ |
| Human-in-the-loop | https://openai.github.io/openai-agents-python/human_in_the_loop/ |
| MCP integration | https://openai.github.io/openai-agents-python/mcp/ |
| Tracing | https://openai.github.io/openai-agents-python/tracing/ |
| SDK Testing | https://openai.github.io/openai-agents-python/testing/ |
| Usage | https://openai.github.io/openai-agents-python/usage/ |
| Sandbox agents | https://openai.github.io/openai-agents-python/sandbox_agents/ |
| Voice agents | https://openai.github.io/openai-agents-python/voice/quickstart/ |
| Realtime agents | https://openai.github.io/openai-agents-python/realtime/guide/ |
| Python SDK releases | https://github.com/openai/openai-agents-python/releases |
| OpenAI Agents SDK TypeScript (optional) | https://openai.github.io/openai-agents-js/ |
| OpenAI API reference/models | https://developers.openai.com/api/docs/ |
| MCP protocol | https://modelcontextprotocol.io/specification |
| MCP Apps extension | https://github.com/modelcontextprotocol/ext-apps |
| AG-UI protocol | https://github.com/ag-ui-protocol/ag-ui |
| A2A protocol | https://a2a-protocol.org/ |
| OpenTelemetry GenAI conventions | https://opentelemetry.io/docs/specs/semconv/gen-ai/ |
| OWASP GenAI security | https://genai.owasp.org/ |

### 31.4 Glossary

**ACL:** access-control list. **ADR:** architecture decision record. **A2A:** inter-agent service interoperability protocol. **Agent loop:** repeated model/tool processing until exit. **Approval interruption:** runner pause requiring a decision. **Context:** information available to code or model; not always the same. **Guardrail:** a validation/check mechanism. **Handoff:** internal transfer to a specialist agent. **Hosted tool:** tool executed through a model/platform-provided capability. **Idempotency:** retries of one logical operation do not duplicate effects. **MCP:** standard tool/resource/prompt connection boundary. **MCP Apps:** optional in-chat interactive app extension. **RAG:** retrieval-augmented generation. **RunState:** SDK state used in interruption/resumption. **Session:** conversation-history store. **Span:** one trace operation. **System of record:** authoritative business source. **Tool contract:** typed arguments, outputs, errors and security requirements. **Unknown outcome:** external side effect may have succeeded despite lost response.

---

**Final design principle:** *Let models reason and draft; let tools fetch and validate; let business services authorize; let durable state protect effects; let evaluations and traces prove the system works.*
