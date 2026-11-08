
### Stage 3 result

The minimal design is:

**Engineer → Authorized API → Fixed workflow → Two read-only tools → Evidence →
Analysis → Validated report**.

The architecture deliberately excludes speculative distributed infrastructure.

---

# Stage 4 — Working Local Mock

## 4.1 Implementation goal

Stage 4 turned the Stage 3 design into a runnable **local Python simulator**
using synthetic files. The default path needs only Python's standard library.

**Important status:** The earlier Stage 4 work reported successful local tests.
The original ZIP/project files were not present in the working container when
this Markdown consolidation was created. Consequently, the earlier reported
outcomes are preserved below as lesson history, **not claimed as freshly re-run
in this export**.

## 4.2 Files and responsibilities

```text
it-ops-assistant-stage4/
|
+-- app.py
|   CLI request entry point
|
+-- auth.py
|   Synthetic principals and incident registry
|
+-- tools.py
|   Guarded reads over local JSON records
|
+-- investigator.py
|   Fixed workflow, mock analysis, validation
|
+-- specialist_server.py
|   Optional local HTTP specialist simulator
|
+-- timeline.html
|   Offline interactive viewer of recorded output
|
+-- data/
|   +-- metrics.json
|   +-- deployments.json
|
+-- tests/
    +-- test_investigation.py
```

No third-party package or API key is needed for the **default** CLI mock.

## 4.3 Synthetic identity and access

The fixture contains, among others:

| Identity     | Tenant      | Allowed service | Expected access to INC-42 |
|--------------|-------------|-----------------|---------------------------|
| `operator-5` | `company-A` | `checkout-api`  | Allowed                   |
| `operator-9` | `company-A` | `shipping-api`  | Denied                    |
| `external-1` | `company-B` | `checkout-api`  | Denied                    |

A trusted local incident registry maps `INC-42` to tenant `company-A` and
service `checkout-api`.

`--user` chooses a **synthetic fixture**, **not a real login**. The mock cannot
be deployed as a public service or connected to production credentials.

The application checks incident access first; read tools **repeat**
tenant/service checks at their own boundary.

## 4.4 Synthetic source records

Metrics fixture:

```json
[
  {
    "evidence_id": "METRIC-07",
    "source": "monitoring",
    "tenant_id": "company-A",
    "service": "checkout-api",
    "recorded_at": "2026-11-06T10:10:00Z",
    "p95_latency_ms": 1800,
    "baseline_p95_ms": 240,
    "error_rate_percent": 3.1
  }
]
```

Deployment fixture:

```json
[
  {
    "evidence_id": "CHANGE-03",
    "source": "deployment",
    "tenant_id": "company-A",
    "service": "checkout-api",
    "version": "v2.7.4",
    "deployed_at": "2026-11-06T09:55:00Z"
  }
]
```

All values are hypothetical. These records are the **simulated** sources of
truth for the exercise.

## 4.5 Deterministic mock analyst

The Stage 4 `MockAnalyst` is ordinary Python code, **not a real LLM**. It:

1. Finds monitoring evidence and deployment evidence.
2. Produces an observation for each available source.
3. Produces a tentative deployment-related hypothesis **only when both sources
   exist**.
4. Gives the engineer an investigation recommendation.

The validator checks that every cited `evidence_id` appears in the collected
data. It rejects nonexistent IDs, but **cannot prove semantic support or
causality**.

## 4.6 Execution event timeline

The workflow records simple events:

```json
[
  {
    "step": "incident_access",
    "status": "allowed"
  },
  {
    "step": "get_metrics",
    "status": "ok"
  },
  {
    "step": "get_deployments",
    "status": "ok"
  },
  {
    "step": "analyze_and_validate",
    "status": "ok"
  }
]
```

A self-contained `timeline.html` was produced in the earlier lab to **replay
recorded outputs** for success, missing metrics, denied access, and optional
specialist scenarios. The HTML preview does not execute the Python workflow.

## 4.7 CLI commands from the lab

Run from the extracted Stage 4 project directory:

```bash
python app.py
python app.py --fail-metrics
python app.py --user operator-9
python app.py --user external-1
python -m unittest discover -s tests -v
```

### Example successful result

```json
{
  "status": "needs_review",
  "evidence_ids": [
    "METRIC-07",
    "CHANGE-03"
  ],
  "missing_evidence": [],
  "action_executed": false
}
```

### Example missing-metrics result

```json
{
  "status": "insufficient_evidence",
  "evidence_ids": [
    "CHANGE-03"
  ],
  "missing_evidence": [
    "metrics"
  ],
  "hypothesis": null,
  "action_executed": false
}
```

### Example unauthorized result

```json
{
  "status": "error",
  "code": "ACCESS_DENIED"
}
```

## 4.8 Optional remote specialist

Stage 4 also included a **separate local HTTP/JSON process** that could suggest
checking database connection saturation. Its request shared only the service
name and evidence IDs.

Two terminals were used:

```bash
# Terminal 1
python specialist_server.py
```

```bash
# Terminal 2
python app.py --specialist-url http://127.0.0.1:8765/diagnose
```

This was a **mock boundary demonstration, not A2A**. The specialist's suggestion
is unverified and is not new source evidence. It cannot grant access or
authorize operations.

## 4.9 Reported Stage 4 software checks

The earlier lesson reported **8 of 8 automated software tests passing**. Covered
cases included:

- Successful investigation.
- Denial for another service.
- Denial for another tenant.
- Re-authorization inside the tool.
- Metrics timeout resulting in partial evidence.
- Rejection of a fabricated citation ID.
- Unknown incident handling.
- Empty question rejection.

**Limits:** No real authentication, no real LLM, no production API, no verified
root-cause classifier, no write operations, no MCP, and no A2A.

### Stage 4 result

The local mock established the **read-only evidence and safety workflow** before
introducing a real model.

---

# Stage 5 Evolution 1 — Bounded Model-Driven Tool Calling

## 5.1 New requirement

Stage 4 always reads the same two sources. A more flexible incident assistant
may need to decide which approved diagnostic tool to inspect first.

**New requirement:** Let a model **propose** approved diagnostic tool calls and
analyze their results, without letting it control service scope or perform
production writes.

### Why the baseline is insufficient

| Stage 4 baseline                  | New need                           |
|-----------------------------------|------------------------------------|
| Python always selects both tools  | Model can propose useful tools     |
| Deterministic mock interpretation | Optional real LLM reasoning        |
| Tool execution stays in Python    | Must remain in Python              |
| Two known sources                 | Preserve authorized incident scope |
| No write tools                    | Continue to prohibit remediation   |

This is the **first** Stage 5 increment only. It is not a completed enterprise
platform.

## 5.2 Revised architecture

```text
+----------------------------------+
| On-call engineer                 |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Investigation application        |
| Trusted incident authorization   |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Bounded agent controller         |
| Tool allowlist, schema, budget   |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Model proposes tool calls        |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Application validation gate      |
| Reject unknown tools/arguments   |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Approved read-only tools         |
| Metrics / deployments            |
+----------------------------------+
                 |
                 | Tool outputs returned to model
                 v
+----------------------------------+
| Model analysis                   |
| Structured evidence-based output |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Output validation                |
| Evidence IDs and required fields |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Engineer reviews report          |
| No production action             |
+----------------------------------+
```

The important change is **model-driven proposal**, not model-driven
authorization.

## 5.3 Tool request contract: no model-provided scope

Allowed tool names:

- `get_metrics`
- `get_deployments`

Their model-facing arguments are intentionally empty:

```json
{
  "name": "get_metrics",
  "arguments": {}
}
```

**Why empty arguments?** The controller gets the service and tenant from the
incident already authorized by application code. The model cannot override them
with `payroll-api`, a different tenant, or a guessed user identity.

Example rejected request:

```json
{
  "name": "get_metrics",
  "arguments": {
    "service": "payroll-api"
  }
}
```

The controller rejects this because unexpected arguments are not allowed.

## 5.4 Controller policy

| Guard                        | Stage 5 Evolution 1 behavior                      |
|------------------------------|---------------------------------------------------|
| Tool allowlist               | Only the two named read-only tools                |
| Arguments                    | Empty JSON object only                            |
| Call budget                  | At most two distinct tool calls per request       |
| Duplicate names / IDs        | Reject proposed batch                             |
| Authorization                | Incident-scoped at API and source-tool boundaries |
| Missing tool result          | Return incomplete-evidence status                 |
| Unknown tool                 | Reject before executing any tool                  |
| Model-generated evidence IDs | Validate against retrieved records                |
| Remediation tools            | None registered                                   |

The proposed batch is validated **before any tool executes**. This prevents
partially executing a batch that also contains a prohibited action.

Conceptual controller logic:

```python
ALLOWED_TOOLS = {"get_metrics", "get_deployments"}
MAX_TOOL_CALLS = 2


def validate_requests(requests):
    if len(requests) > MAX_TOOL_CALLS:
        raise RejectedToolRequest("TOOL_BUDGET_EXCEEDED")

    seen_names = set()
    seen_ids = set()
    for request in requests:
        if request.name not in ALLOWED_TOOLS:
            raise RejectedToolRequest("UNKNOWN_TOOL")
        if request.arguments != {}:
            raise RejectedToolRequest("UNEXPECTED_ARGUMENTS")
        if request.name in seen_names or request.call_id in seen_ids:
            raise RejectedToolRequest("DUPLICATE_TOOL_REQUEST")
        seen_names.add(request.name)
        seen_ids.add(request.call_id)
```

This excerpt illustrates the contract; the earlier Stage 5A project contained
the full implementation and additional input-type checks.

## 5.5 Model/tool request flow

The Stage 5A adapter uses **two model phases**:

1. Ask the model to propose up to two approved read-only tool calls.
2. After application-side validation and tool execution, supply matching tool
   outputs and request a structured investigation report.

An actual tool-call response includes a **call identifier**. The application
pairs the result with that identifier when returning the tool output to the
model.

Conceptual tool response handed back to the model:

```json
{
  "type": "function_call_output",
  "call_id": "call-01",
  "output": "{\"evidence_id\":\"METRIC-07\",\"p95_latency_ms\":1800}"
}
```

The model does **not** directly invoke Python functions. The controller executes
the authorized function and supplies its output.

**Important limitation:** The Stage 5A adapter demonstrated **one proposal phase
plus one analysis phase**, not an unlimited autonomous agent loop. A full
iterative tool-selection loop was explicitly deferred.

## 5.6 Failure scenario: model proposes a dangerous action

The model proposes:

```json
{
  "name": "restart_service",
  "arguments": {
    "service": "checkout-api"
  }
}
```

Safe behavior:

```text
+------------------------------+
| Model requests restart       |
+------------------------------+
               |
               v
+------------------------------+
| Controller checks allowlist  |
+------------------------------+
               |
               v
+------------------------------+
| Tool not registered          |
| Reject entire proposal       |
+------------------------------+
               |
               v
+------------------------------+
| No production action         |
+------------------------------+
```

Prompt instructions such as “do not restart services” are useful
defense-in-depth, but the **absence of a registered write capability** and
independent tool validation are the stronger controls.

## 5.7 Failure scenario: missing evidence

If the model skips `get_metrics` or monitoring times out:

1. The controller records metrics as missing.
2. Other authorized evidence can still be used.
3. The resulting status is `insufficient_evidence`.
4. A deployment-related hypothesis is not treated as confirmed root cause.
5. No production write is possible.

A denied user is handled earlier: no protected evidence should be retrieved and
no unnecessary model request should occur.

## 5.8 Stage 5A implementation structure

```text
it-ops-assistant-stage5a/
|
+-- app_agent.py
|   Entry point for scripted or optional model mode
|
+-- stage5_agent.py
|   Tool-request validation and guarded dispatcher
|
+-- openai_provider.py
|   Optional hosted model adapter
|
+-- auth.py
+-- tools.py
+-- investigator.py
+-- data/
|   +-- metrics.json
|   +-- deployments.json
|
+-- tests/
    +-- test_investigation.py
    +-- test_stage5_agent.py
    +-- test_openai_adapter_offline.py
```

The default provider, `ScriptedProvider`, simulates a model request but **is not
an LLM**.

`OpenAIProvider` was provided as an optional adapter for the OpenAI Responses
API using function calls and structured output. It uses an API key and a
configured supported model. The adapter's **transport behavior was tested with
offline fake responses**, but no real hosted model was called in the lesson.

### Local commands from the lab

```bash
python app_agent.py
python app_agent.py --fail-metrics
python app_agent.py --user operator-9
python -m unittest discover -s tests -v
```

Optional real-model path (requires separate API credentials and a compatible
model):

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL="your-supported-model"
python app_agent.py --real-model
```

**Do not put real secrets into study files or source control.** The real-model
path sends only synthetic incident data in this exercise, may incur API costs,
and was **not validated live**.

## 5.9 Reported Stage 5A verification

The earlier lesson reported **23 automated tests passing**, including Stage 4
regressions, Stage 5 controller checks, and offline provider-adapter tests. The
reported coverage included:

- Successful read-only investigation.
- Rejecting unknown write tool `restart_service`.
- Rejecting model-supplied service arguments.
- Rejecting excessive or duplicate tool calls.
- Handling no tool requests and monitoring timeouts.
- Denying unauthorized service or tenant access.
- Rejecting fabricated evidence IDs.
- Parsing structured model output in an offline stub.
- Pairing `function_call_output` with the correct `call_id`.

**Verification boundary:** These are previously reported software-test outcomes,
not a new test run for this Markdown export. The actual hosted-model request
path remains unverified.

## 5.10 Requirement → Change → Check → Trade-off

| New requirement / risk           | Change made                               | Check used                             | Trade-off                                            |
|----------------------------------|-------------------------------------------|----------------------------------------|------------------------------------------------------|
| Need flexible evidence selection | Model proposes tools                      | Scripted tool-proposal tests           | More flexibility; extra model complexity             |
| Model may request unsafe tool    | Application allowlist                     | `restart_service` rejection            | Cannot run arbitrary actions                         |
| Model may target another service | Scope fixed from authorized incident      | Unexpected service-argument rejection  | Less model autonomy                                  |
| Model may loop or over-call      | Two distinct tool-call limit              | Excess/duplicate tests                 | Investigation can stop early                         |
| Metrics may be unavailable       | Partial-result status                     | Timeout test                           | Not every investigation gets a conclusion            |
| Model may invent evidence IDs    | Citation-ID validator                     | Fabricated citation test               | Does not establish semantic truth                    |
| Model/API might be unavailable   | Error path rather than an invented answer | Offline adapter and application errors | No guaranteed useful response during provider outage |

### What is still missing for production?

- Real authentication, delegated identity, and service-level authorization
  tokens.
- Semantic verification that cited evidence actually supports each claim.
- Persistent, protected audit records and distributed tracing.
- Tool timeouts, retry policies, cancellation, and resource quotas for real
  infrastructure.
- Version-pinned models, evaluation datasets, rollout gates, and cost budgets.
- Data classification, retention, and privacy review before sending real
  operational evidence to a hosted model.
- Durable approval workflows if future phases add write actions.
- Shared MCP integration, RAG, AG-UI/A2UI/MCP Apps, or A2A **only when a
  concrete requirement warrants them**.

### Stage 5 Evolution 1 result

The model can **propose** approved evidence reads. The application still owns
execution and permissions. Reports are checked for structure and existing
evidence IDs. All available operational tools remain **read-only**.

---

# Consolidated Architecture Decisions and Next Step

## What changed across the completed work?

| Stage               | Main decision                                     | Proven or demonstrated                                      |
|---------------------|---------------------------------------------------|-------------------------------------------------------------|
| Stage 1             | Investigation copilot, not autonomous operator    | Requirements and scope defined                              |
| Stage 2             | Fixed workflow before adaptive agent              | Concepts and trade-offs explained                           |
| Stage 3             | One application with two guarded reads            | Contracts, sequence and failure path defined                |
| Stage 4             | Local deterministic Python mock                   | Synthetic workflow and negative tests reported              |
| Stage 5 Evolution 1 | Model proposes tools; app authorizes and executes | Guarded dispatcher and offline model-adapter tests reported |

## Reusable principles established

1. **Source of truth:** The monitoring and deployment systems own business
   facts.
2. **Trust boundary:** The model is not the authorizer and retrieved records are
   not instructions.
3. **Least privilege:** Initial tools read only the specific incident's
   authorized service.
4. **Evidence:** Separate observed measurements, hypotheses, and unknowns.
5. **Failure honesty:** Missing evidence must produce an incomplete response,
   not a confident diagnosis.
6. **Bounded execution:** Tool allowlists, argument schemas, and budgets are
   application controls.
7. **Incremental complexity:** Add protocols and distributed services only when
   justified by requirements.

## Next planned increment (not included)

**Stage 5 Evolution 2 — Shared tools and MCP.** The next problem is tool reuse
across several AI products. We would compare direct Python/API integrations with
an approved MCP server and catalog, then derive compatibility, ownership, and
authorization requirements before implementing the extra boundary.

No MCP server, agent-to-agent protocol, production approval workflow, or full
unified platform has been implemented in the stages covered by this file.

---

# Curriculum and Documentation Sources

This consolidated guide is based on the previous lesson's Stage 1–4 and Stage 5
Evolution 1 explanations, supplemented by the following **project reference
files**:

- `SKILL.md` — progressive teaching, mock implementation, and safety rules.
- `sdt-catalog.md` — maps AI design #73 to Module 09 and anchor #73.
- `sdt-module-09-advanced-ai.md` — #73 platform case brief.
- `sdt-anchor-73-unified-enterprise-agentic-platform.md` — focused capstone
  scope, staged evolution, and design trade-offs.
- `concept-production-controls.md` — authorization, grounding, audit, retries,
  and evaluation principles.
- `concept-protocol-boundaries.md` — distinctions between MCP, MCP Apps, AG-UI,
  A2UI, A2A, and Skills.

Official documentation links used as references in the earlier Stage 5 lesson:

- OpenAI function
  calling: <https://developers.openai.com/api/docs/guides/function-calling>
- OpenAI structured
  outputs: <https://developers.openai.com/api/docs/guides/structured-outputs>

These are **reference URLs**, not a claim that the optional live-model adapter
has been re-tested against a hosted service in this document-generation turn.

**Document scope ends at Stage 5, Evolution 1.**
