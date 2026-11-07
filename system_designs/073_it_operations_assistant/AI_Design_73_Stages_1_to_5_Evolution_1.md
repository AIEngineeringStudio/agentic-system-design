# AI Design #73 — Unified Enterprise Agentic Platform

## Enterprise IT Operations Assistant — Stages 1–4 and Stage 5, Evolution 1

**Case:** Fictional Checkout API incident `INC-42`  
**Learning approach:** Problem → Concepts → Minimal architecture → Local mock →
One production evolution  
**Coverage:** Stage 1, Stage 2, Stage 3, Stage 4, and **Stage 5 Evolution 1 (
bounded model-driven tool calling)**. Stage 5 Evolution 2 and Stage 6 are **not
covered**.  
**Data:** All incident records, identities, metrics, and deployment records in
this guide are **synthetic**.

> **Safety rule:** AI-generated explanations and tool requests are not
> authorization. The application and business systems enforce permissions. No
> part
> of the implemented baseline can modify production systems.

### Contents

1. [Stage 1 — Problem Definition and Requirements](#stage-1--problem-definition-and-requirements)
2. [Stage 2 — Essential Concepts](#stage-2--essential-concepts)
3. [Stage 3 — Minimal Working Architecture](#stage-3--minimal-working-architecture)
4. [Stage 4 — Working Local Mock](#stage-4--working-local-mock)
5. [Stage 5, Evolution 1 — Bounded Model-Driven Tool Calling](#stage-5-evolution-1--bounded-model-driven-tool-calling)
6. [Consolidated Architecture Decisions and Next Step](#consolidated-architecture-decisions-and-next-step)
7. [Curriculum and Documentation Sources](#curriculum-and-documentation-sources)

---

# Stage 1 — Problem Definition and Requirements

## 1.1 Business problem

An enterprise runs an e-commerce platform. Customers use its **Checkout API** to
complete purchases. The API becomes slow, and the IT Operations team receives a
severity-2 alert.

### Fictional incident: INC-42 [SEV-2]

| Signal                   | Normal |   During incident |
|--------------------------|-------:|------------------:|
| Checkout API p95 latency | 240 ms |          1,800 ms |
| Error rate               |   0.4% |              3.1% |
| Deployment               |      — | `v2.7.4` at 09:55 |

Illustrative observations:

- Latency is near normal around 09:45.
- Deployment `v2.7.4` occurs at 09:55.
- Latency increases sharply afterward, reaching 1,800 ms around 10:10.
- **Temporal correlation does not prove the deployment caused the slowdown.**

The on-call engineer needs to answer:
- What changed?
- What evidence explains the slowdown?
- What is the most likely cause?
- What should we investigate or do next?
- Can we safely recover the service?

The on-call engineer currently checks monitoring dashboards, logs, deployments,
incident records, and runbooks separately. 

The process is slow, repetitive and vulnerable to human error under pressure.

**Business objective:** Help IT Operations engineers **investigate incidents
faster**, **understand evidence, and recommend safe next steps**, while
retaining human responsibility for remediation.

Desired outcomes include:
- lower investigation effort, 
- potentially shorter mean time to resolution (MTTR),
- fewer unsafe operational decisions. 

These are **goals, not measured improvements**.

## 1.2 Representative user request

> Investigate incident INC-42. Checkout API latency increased. Find possible
> causes and recommend the safest next step.

Expected assistant behavior:

1. Confirm which incident and service are being investigated.
2. Confirm that the engineer may access the incident.
3. Read permitted metrics and deployment history.
4. Separate `observed facts from hypotheses and unknowns`.
5. Attach evidence references to findings.
6. Identify missing or contradictory information.
7. Recommend a next diagnostic step without changing production.

### Business-level sequence

```
+-------------------------------+
|       On-call engineer        |
|                               |
| Investigate INC-42:           |
| "Why is Checkout API slow?"v  |
+-------------------------------+
               |
               v
+-------------------------------+
|   IT Operations Assistant     |
|                               |
| Collect and evaluate evidence |
+-------------------------------+               
               |
               v
+-------------------------------+
|   Approved source systems     |
|                               |
|  Metrics, changes, logs       |
|  and operational records      |
+-------------------------------+
               |
               v
+-------------------------------+
|  Evidence-backed report       |
|                               |
|  Facts, hypotheses,           |
|  and recommended next step    |
+-------------------------------+
               |
               v
+-------------------------------+
|  Engineer reviews and decides |
+-------------------------------+

```

This is a **business flow**, not yet a deployment architecture.

## 1.3 Actors

| Actor                      | Main responsibility                               | Authority boundary                              |
|----------------------------|---------------------------------------------------|-------------------------------------------------|
| On-call engineer           | Starts investigations and reviews findings        | May read only permitted operational evidence    |
| Incident commander         | Coordinates response and incident status          | Manages incident within assigned role           |
| SRE / service owner        | Checks technical findings and remediation options | Can operate owned services under policy         |
| Change approver            | Reviews proposed production changes               | Approves only eligible actions                  |
| Security / compliance team | Defines identity, policy, and audit rules         | Governs security controls                       |
| Shared platform team       | Owns reusable AI platform capabilities later      | Does not own every service's business semantics |

**Primary first-version user:** The on-call engineer.

## 1.4 Functional requirements

Priority definitions: **P0 = mandatory for the safe baseline**, **P1 = important
next**, **P2 = deferred until justified**.

| ID | Requirement                                             | Priority | Architectural consequence                   |
|----|---------------------------------------------------------|----------|---------------------------------------------|
| F1 | Accept an incident ID, service, and question            | P0       | Requires an investigation entry point       |
| F2 | Retrieve authorized metrics and deployment data         | P0       | Requires approved read-only integrations    |
| F3 | Explain observations and possible causes using evidence | P0       | Requires provenance and report structure    |
| F4 | Recommend next steps without executing remediation      | P0       | Separates recommendation from action        |
| F5 | Enforce user-specific data access                       | P0       | Requires server-side authorization          |
| F6 | Handle missing, stale, or conflicting evidence          | P1       | Requires incomplete/uncertain result states |
| F7 | Show an incident timeline and readable report           | P1       | Requires useful presentation and event data |
| F8 | Reuse tools across teams and applications               | P2       | May later justify a shared protocol/catalog |
| F9 | Support human-approved remediation                      | P2       | May later require durable workflow state    |

## 1.5 Ranked non-functional requirements

| Rank | Constraint                     | First-version rule                                | Why                                              |
|-----:|--------------------------------|---------------------------------------------------|--------------------------------------------------|
|    1 | Security and authorization     | No unauthorized incident access                   | Operational data may be sensitive                |
|    2 | Action safety                  | Zero production writes                            | A wrong action can worsen an outage              |
|    3 | Evidence integrity             | Material findings cite available evidence         | Plausible language is not proof                  |
|    4 | Reliability and responsiveness | Explicit tool failures and usable partial results | Engineers need honest responses during incidents |
|    5 | Auditability and cost          | Track investigation steps and bound work          | Supports review and predictable usage            |

**Illustrative future latency target:** An initial investigation summary within
30 seconds for 95% of requests. This was a proposed design target, **not an
agreed or measured SLO**.

A faster response does not justify skipping authorization or inventing
unavailable facts.

## 1.6 Sources of truth

| Information                    | Authoritative owner                             | Assistant's permitted role              |
|--------------------------------|-------------------------------------------------|-----------------------------------------|
| Latency and error measurements | Monitoring system                               | Read authorized values                  |
| Application logs               | Logging system                                  | Read permitted records when later added |
| Deployments                    | Deployment/change system                        | Read versions and timestamps            |
| Incident metadata              | Incident management system                      | Read permitted incident state           |
| Runbooks                       | Approved runbook repository                     | Retrieve guidance when later added      |
| Identity and permissions       | Enterprise identity and business policy systems | Use independently verified decisions    |

The model's answer is **not** a source of operational truth.

## 1.7 Trust boundaries

1. A chat request does not grant access to all services.
2. The API must derive identity and permissions from verified server-side
   context.
3. Each data source must enforce its own authorization rules.
4. Tool responses, logs, documents, and model-generated text are **untrusted
   data**, not executable instructions.
5. A suggested rollback or an approval button is **not** authorization to
   perform a rollback.

## 1.8 First-version scope

**Included:**

- One fictional enterprise and IT Operations team.
- One incident: `INC-42`, Checkout API.
- One authorized on-call engineer.
- Two read-only capabilities: retrieve metrics and deployment history.
- Evidence-backed findings, uncertainty, and recommendations.
- Synthetic source data only.

**Excluded initially:**

- Automatic restart, rollback, or infrastructure writes.
- Real credentials or production integrations.
- Multi-agent delegation, MCP, A2A, RAG, and advanced UI protocols.
- Global multi-region platform infrastructure.

**Working assumptions:** The incident has a known tenant and service; the
authorized operator may read its records; two sources are enough for the first
demonstration; the application has no write permission.

### Stage 1 result

We defined an **investigation copilot**, not an autonomous operations
controller. Safety, provenance, and ownership take priority over sophistication.

---

# Stage 2 — Essential Concepts

## 2.1 LLM versus agent

A **large language model (LLM)** generates a response from supplied input. It
can explain metrics or summarize a deployment record, but it does not
automatically know the current state of Checkout API.

An **AI agent** is an application that lets a model participate in deciding
which tools or steps to request while pursuing a task. The application still
executes and authorizes those steps.

```text
+-----------------------------+
| Engineer asks a question    |
+-----------------------------+
               |
               v
+-----------------------------+
| Model proposes next step    |
+-----------------------------+
               |
               v
+-----------------------------+
| App validates tool request  |
+-----------------------------+
               |
               v
+-----------------------------+
| Approved tool returns data  |
+-----------------------------+
               |
               v
+-----------------------------+
| Model analyzes evidence     |
+-----------------------------+
               |
               v
+-----------------------------+
| Human-readable report       |
+-----------------------------+
```

| Pattern                    | Use when                                 | Main trade-off                          |
|----------------------------|------------------------------------------|-----------------------------------------|
| Single LLM call            | All evidence is already present          | Simplest, but cannot retrieve new facts |
| Fixed workflow plus LLM    | Known evidence sources and steps         | Predictable, but less flexible          |
| Bounded tool-calling agent | Next diagnostic tool depends on findings | Flexible, but requires stricter limits  |

**Stage 2 choice:** Start with a **fixed read-only workflow** because the two
required sources are known. Introduce model-selected tools only when the
requirement emerges in Stage 5.

## 2.2 Tool calling

A **tool** is an approved operation that application code can execute. Our tools
are:

- `get_metrics`: read current and baseline latency/error measurements.
- `get_deployments`: read recent deployment history.

Conceptual request:

```json
{
  "tool": "get_metrics",
  "arguments": {
    "service": "checkout-api",
    "incident_id": "INC-42"
  }
}
```

Synthetic response:

```json
{
  "evidence_id": "METRIC-07",
  "service": "checkout-api",
  "p95_latency_ms": 1800,
  "baseline_p95_ms": 240,
  "error_rate_percent": 3.1
}
```

The model may **request** a tool, but the application must check its name,
arguments, user authorization, and allowed scope before executing it.

## 2.3 Context engineering and grounding

**Context engineering** chooses the relevant information given to the model for
this specific task. **Grounding** ties material claims to retrieved evidence.

Example context:

```text
Incident: INC-42
Service: checkout-api

Evidence:
  METRIC-07: p95 latency = 1,800 ms
  CHANGE-03: version v2.7.4 deployed at 09:55

Rules:
  Distinguish facts from hypotheses.
  Cite evidence IDs.
  Never treat correlation as proof of root cause.
  Do not execute remediation.
```

A proper report separates:

| Classification | Example                                             |
|----------------|-----------------------------------------------------|
| Observation    | p95 latency increased to 1,800 ms (`METRIC-07`)     |
| Observation    | Deployment `v2.7.4` occurred at 09:55 (`CHANGE-03`) |
| Hypothesis     | The deployment might be related                     |
| Unknown        | Whether the deployment caused the slowdown          |

A fake citation can be rejected by checking that its ID exists. **However, a
valid citation ID alone does not prove that the claim is supported.** Semantic
verification is a later requirement.

### Do we need RAG?

Not for the baseline. **Retrieval-Augmented Generation (RAG)** becomes useful
when the assistant must search many approved runbooks, previous incidents, or
other unstructured documents. Two structured API calls do not require a vector
index.

## 2.4 Control plane versus runtime/data plane

The **control plane** governs configuration: which tools, versions, policies,
and owners are approved. The **runtime/data plane** handles live investigation
requests and performs approved reads.

```text
+------------------------------+
| Control plane                |
| Tool policy and configuration|
+------------------------------+
               |
               | Governs
               v
+------------------------------+
| Runtime / data plane         |
| INC-42 workflow and reads    |
+------------------------------+
```

These are **responsibilities**, not yet separate deployments. The source system
must still authorize every protected read.

## 2.5 Observability versus evaluation

| Concern       | Question                           | Example                                     |
|---------------|------------------------------------|---------------------------------------------|
| Observability | What happened during execution?    | Which tool failed and how long did it take? |
| Evaluation    | Was the result useful and correct? | Did the report invent a root cause?         |

Software success is not the same as investigation correctness. Useful later
measures include task success, tool errors, groundedness, latency, human
corrections, and cost.

## 2.6 Technologies explicitly deferred

| Technology              | Initial decision | Why                                                      |
|-------------------------|------------------|----------------------------------------------------------|
| Direct functions        | Use              | Small number of local integrations                       |
| Fixed workflow          | Use              | Predictable two-source investigation                     |
| MCP                     | Defer            | Tool interoperability across clients is not yet required |
| RAG                     | Defer            | No large document collection                             |
| Durable orchestration   | Defer            | No long-running approval or write action                 |
| MCP Apps / AG-UI / A2UI | Defer            | Basic incident report is sufficient                      |
| Multi-agent / A2A       | Defer            | No independently owned specialist delegation required    |

### Stage 2 result

A simple authorized application retrieves evidence; an LLM can interpret it; an
engineer reviews the recommendation. Model authority and execution authority
remain separate.

---

# Stage 3 — Minimal Working Architecture

## 3.1 Logical components

```text
+--------------------------------+
| On-call engineer               |
| Request: investigate INC-42    |
+--------------------------------+
                |
                v
+--------------------------------+
| Investigation API              |
| Identity, request validation   |
| Incident authorization         |
+--------------------------------+
                |
                v
+--------------------------------+
| Bounded investigation workflow |
| Fetch evidence and coordinate  |
+--------------------------------+
                |
                v
+--------------------------------+
| Two approved read-only tools   |
| get_metrics / get_deployments  |
+--------------------------------+
                |
                v
+--------------------------------+
| Monitoring and deployment data |
| Authoritative source records   |
+--------------------------------+
                |
                | Results return to workflow
                v
+--------------------------------+
| Evidence analysis              |
| Mock now; LLM can be added     |
+--------------------------------+
                |
                v
+--------------------------------+
| Report validator               |
| Structure and evidence IDs     |
+--------------------------------+
                |
                v
+--------------------------------+
| Engineer reviews findings      |
+--------------------------------+
```

**Deployment decision:** The API, workflow, tools, and validator can run in one
Python application. They are not required to be separate services.

## 3.2 Ownership by component

| Component          | Owns                                         | Does not own                                |
|--------------------|----------------------------------------------|---------------------------------------------|
| Investigation API  | Request validation and user-context handling | The original business records               |
| Workflow           | Execution order and result state             | User privileges                             |
| Read-only adapters | Calls into approved systems                  | Authorization grants generated by the model |
| Source systems     | Metrics and deployment truth                 | LLM interpretation                          |
| Analysis component | Observations, hypotheses, recommendations    | Operational authority                       |
| Report validator   | Output shape and citation existence          | Proof of semantic correctness               |

## 3.3 API and typed tool contracts

Request to the investigation API:

```json
{
  "incident_id": "INC-42",
  "service": "checkout-api",
  "question": "Why is Checkout API slow?"
}
```

**Important:** The client cannot supply a trusted `user_id`, role, or tenant.
The application derives these from the authenticated session in a real
deployment.

Illustrative typed Python contracts:

```python
from typing import TypedDict


class Principal(TypedDict):
    user_id: str
    tenant_id: str


class MetricsEvidence(TypedDict):
    evidence_id: str
    service: str
    p95_latency_ms: int
    baseline_p95_ms: int
    error_rate_percent: float


class DeploymentEvidence(TypedDict):
    evidence_id: str
    service: str
    version: str
    deployed_at: str


def get_metrics(
        service: str,
        principal: Principal,
) -> MetricsEvidence: ...


def get_deployments(
        service: str,
        principal: Principal,
) -> list[DeploymentEvidence]: ...
```

These describe **logical interfaces**, not a particular SDK or wire protocol.

Deployment evidence:

```json
{
  "evidence_id": "CHANGE-03",
  "service": "checkout-api",
  "version": "v2.7.4",
  "deployed_at": "09:55"
}
```

## 3.4 Successful investigation sequence

| Step | Owner             | Action                                       |
|-----:|-------------------|----------------------------------------------|
|    1 | Engineer          | Requests investigation of INC-42             |
|    2 | API               | Verifies identity and incident access        |
|    3 | Workflow          | Calls metrics tool                           |
|    4 | Monitoring source | Authorizes and returns `METRIC-07`           |
|    5 | Workflow          | Calls deployment tool                        |
|    6 | Deployment source | Authorizes and returns `CHANGE-03`           |
|    7 | Workflow          | Builds evidence context                      |
|    8 | Analysis          | Produces observations, hypothesis, next step |
|    9 | Validator         | Checks structure and evidence references     |
|   10 | Engineer          | Reviews report; no action is executed        |

Expected synthetic report:

```json
{
  "run_id": "RUN-42",
  "incident_id": "INC-42",
  "status": "needs_review",
  "observations": [
    {
      "text": "Checkout API p95 latency is 1800 ms.",
      "evidence_ids": [
        "METRIC-07"
      ]
    },
    {
      "text": "Version v2.7.4 deployed at 09:55.",
      "evidence_ids": [
        "CHANGE-03"
      ]
    }
  ],
  "hypothesis": {
    "text": "Recent deployment may be related.",
    "evidence_ids": [
      "METRIC-07",
      "CHANGE-03"
    ]
  },
  "next_step": "Investigate latency by deployment version.",
  "action_executed": false
}
```

`needs_review` means the findings await the engineer's review. It does **not**
mean the root cause is verified or a remediation action is approved.

## 3.5 Failure path: monitoring times out

```text
+---------------------------+
| Investigation starts      |
+---------------------------+
             |
             v
+---------------------------+
| get_metrics               |
| TIMEOUT                   |
+---------------------------+
             |
             v
+---------------------------+
| get_deployments           |
| CHANGE-03 available       |
+---------------------------+
             |
             v
+---------------------------+
| Partial evidence          |
| Root cause not confirmed  |
+---------------------------+
             |
             v
+---------------------------+
| Return incomplete result  |
+---------------------------+
```

```json
{
  "run_id": "RUN-42",
  "status": "insufficient_evidence",
  "available_evidence": [
    "CHANGE-03"
  ],
  "missing_evidence": [
    "metrics"
  ],
  "recommendation": "Retry metrics retrieval or investigate manually.",
  "action_executed": false
}
```

If **authorization** fails, the workflow must stop **before** protected data
reaches the model. A timeout and an access denial are different failure classes.

## 3.6 Baseline execution limits

| Control                       | Proposed first-version rule              |
|-------------------------------|------------------------------------------|
| Tool reads                    | One metrics read and one deployment read |
| Analysis                      | One bounded analysis step                |
| Production write capabilities | None                                     |
| Unavailable source            | Explicit partial-result state            |
| Invalid citation              | Reject invalid output                    |
| Remediation                   | Engineer review only                     |

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
