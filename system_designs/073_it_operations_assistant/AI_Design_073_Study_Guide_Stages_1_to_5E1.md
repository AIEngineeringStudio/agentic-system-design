# Enterprise IT Operations Assistant

Unified Enterprise Agentic Platform — Study Guide

A consolidated reference for **Stage 1 through Stage 5, Evolution 1**. Follow
the fictional slow Checkout API incident from requirements to a tested local
workflow, then to bounded model-driven tool selection.

**Scenario: INC-42** · **Synthetic data only** · **No full source code** · *
*Current checkpoint: Stage 5A**

- Normal p95 latency: **240 ms**
- Incident p95 latency: **1,800 ms**
- Incident error rate: **3.1%**
- Recent deployment: **v2.7.4**

## What we have built so far

We are **not designing the entire enterprise platform in one step**. Each stage
adds only the capabilities justified by INC-42. The platform-wide concerns
remain future work.

- **Stage 1** — Problem, actors, priorities and trust boundaries
- **Stage 2** — LLMs, workflows, tool calling and grounding
- **Stage 3** — Two-tool read-only system and typed contracts
- **Stage 4** — Runnable synthetic Python workflow and tests
- **Stage 5A** — Bounded model tool selection and enforcement

> **Central lesson**  
> The LLM may explain evidence and propose what to inspect next. **Application
code and business systems** decide what data can be read and what actions can
> run. No production write action exists in our current design.

### Business outcome

Reduce investigation effort and help authorized engineers reach safer decisions
using verifiable evidence.

### Current architectural limit

One bounded incident investigator, two read-only tools, synthetic records, an
optional model adapter, and no enterprise-scale platform services.

## STAGE 1 — Problem definition and requirements

### 1.1 The incident

Customers experience slow checkouts. Monitoring reports a p95 latency rise from
**240 ms to 1,800 ms**, while error rate rises from **0.4% to 3.1%**. Deployment
`v2.7.4` occurred at 09:55, shortly before the degradation. All values and
identifiers are fictional.

> **Do not confuse correlation with cause**  
> A deployment near the incident is a lead for investigation, not proof that the
> deployment caused the slowdown.

### 1.2 Actors and authority

| Actor                     | Job                                              | Authority boundary                                       |
|---------------------------|--------------------------------------------------|----------------------------------------------------------|
| On-call engineer          | Investigate INC-42 and review results.           | May read only permitted service records.                 |
| Incident commander        | Coordinate incident response.                    | Controls incident process within assigned rights.        |
| Service owner / SRE       | Interpret technical state and evaluate changes.  | Can operate only owned/authorized services.              |
| Change approver           | Review production changes.                       | Approval requires business-side policy enforcement.      |
| Security / platform teams | Provide identity, policies and shared standards. | Govern controls; do not replace source-system ownership. |

### 1.3 Representative user journey

1. Engineer asks: **“Investigate INC-42. Why is Checkout API slow?”**
2. Application authenticates the engineer and checks incident access.
3. Approved tools retrieve metrics and deployment history.
4. Analysis separates observations, hypotheses and unknowns.
5. Engineer reviews the recommendation. No remediation is executed.

### 1.4 Prioritized functional requirements

| Priority | Requirements                                                                                                                          | Architectural significance                                                                       |
|----------|---------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| P0       | Identify incident; read approved metrics and changes; produce cited findings; recommend without acting; enforce user-specific access. | Needs secure input handling, tool interfaces, source provenance and a strict read-only boundary. |
| P1       | Handle incomplete/contradictory evidence; show useful timeline/report.                                                                | Needs explicit failure states, uncertainty and inspectable events.                               |
| P2       | Reuse capabilities across products; add human-approved remediation later.                                                             | May justify MCP, shared governance, durable workflow and action policy in future increments.     |

### 1.5 Ranked non-functional constraints

| Rank | Constraint                         | Why first?                                                 |
|------|------------------------------------|------------------------------------------------------------|
| 1    | Identity and authorization         | Operational evidence can be sensitive or tenant-scoped.    |
| 2    | Safe behavior: zero initial writes | Unsafe remediation can worsen the incident.                |
| 3    | Evidence correctness               | A plausible answer without valid evidence is not reliable. |
| 4    | Reliability and responsiveness     | Tool failures must not create invented answers.            |
| 5    | Auditability and bounded cost      | Operators need traceable, predictable execution.           |

**Illustrative future target:** a usable initial summary within 30 seconds for
95% of requests. This was a proposed learning target, not a measured or agreed
enterprise SLO.

### 1.6 Source of truth and system boundary

| Data or decision      | Source of truth / owner                         | Assistant role                                             |
|-----------------------|-------------------------------------------------|------------------------------------------------------------|
| Latency / errors      | Monitoring service                              | Read and explain authorized records.                       |
| Deployments           | Change/deployment service                       | Read recent changes; do not infer causality automatically. |
| Incident status       | Incident-management system                      | Read state; never silently rewrite it.                     |
| User access           | Verified identity and business policy           | Use decisions; do not invent grants.                       |
| Remediation execution | Authorized operations service and human process | Recommend only in the initial scope.                       |

#### Included initially

- One incident and one primary engineer
- Metrics + deployment reads
- Evidence-based recommendations
- Synthetic fixtures and a local mock

#### Explicitly excluded

- Automatic rollback/restart
- Live credentials and production systems
- Mandatory MCP, RAG or A2A
- Multi-region scale and shared platform rollout

## STAGE 2 — Essential AI architecture concepts

Introduce a concept only when it helps solve INC-42. A more advanced technology
is not automatically a better design.

| Concept                 | Simple definition                                                       | Applied to INC-42                                                                                               |
|-------------------------|-------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| **LLM**                 | Generates explanations or structured text from its input.               | Summarizes why latency may have increased; does not know live metrics without supplied evidence.                |
| **Fixed workflow**      | Application code determines the order of steps.                         | Always read metrics and deployments, then analyze results.                                                      |
| **Bounded agent**       | Model helps choose from permitted tools under execution limits.         | Can propose which diagnostic read to make; cannot invent permissions.                                           |
| **Tool calling**        | Model proposes a typed operation; application validates and runs it.    | `get_metrics` and `get_deployments` are approved reads.                                                         |
| **Context engineering** | Select information and instructions relevant to the current model call. | Give incident ID, approved evidence, source IDs, and uncertainty rules.                                         |
| **Grounding**           | Base material claims on retrieved records.                              | “Latency is 1,800 ms” cites `METRIC-07`.                                                                        |
| **RAG**                 | Retrieve relevant knowledge passages before generation.                 | Useful later for large runbook or historical incident collections; unnecessary for two direct structured reads. |
| **Control plane**       | Governance/configuration of capabilities.                               | Approved tools, tool versions, identity policy and budgets.                                                     |
| **Runtime/data plane**  | Actual work performed on requests.                                      | Incident workflow, authorized tool reads, and report generation.                                                |
| **Observability**       | Explains what executed, where, and with what latency/errors.            | Shows tool timeline, failures and run correlation.                                                              |
| **Evaluation**          | Tests whether the output is correct and useful.                         | Checks claims, citations, uncertainty and recommendation safety.                                                |

### 2.1 Which execution pattern fits?

#### Fixed workflow — Stage 3/4

Use when required sources and steps are known. Lower complexity and easier
testing.

```
Request
  |
  v
Read metrics
  |
  v
Read deployments
  |
  v
Analyze evidence
```

#### Bounded tool selection — Stage 5A

Use when next reads may vary. The model proposes tools, but the controller
enforces limits.

```
Request
  |
  v
Model proposes reads
  |
  v
Validate + authorize
  |
  v
Execute approved reads
  |
  v
Analyze + validate
```

### 2.2 Facts, hypotheses and missing information

| Type          | Example                                           | Evidence rule                          |
|---------------|---------------------------------------------------|----------------------------------------|
| Observed fact | p95 latency is 1,800 ms.                          | Cite `METRIC-07`.                      |
| Observed fact | `v2.7.4` deployed at 09:55.                       | Cite `CHANGE-03`.                      |
| Hypothesis    | The deployment might contribute to degradation.   | Use both observations; say unverified. |
| Unknown       | Whether database saturation caused slow requests. | Do not manufacture database metrics.   |

> **Key distinction**  
> Observability answers “What happened during the run?” Evaluation answers “Was
> the investigation answer actually correct?” A successful API response can still
> contain a wrong analysis.

### Why MCP, A2A and GenUI are not required yet

**MCP** becomes valuable when tools/resources need a reusable host-to-server
interface. **A2A** is useful for delegating work between independently deployed
agents. **AG-UI** streams agent state to owned frontends; **A2UI** specifies
trusted components declaratively; **MCP Apps** embeds UI in a compatible host.
These are separate boundaries, not substitutes for one another.

Our current scope has one application and two simple read functions. Ordinary
Python functions and a basic report are sufficient.

## STAGE 3 — Minimal working architecture

We selected one logical service boundary with a fixed read-only investigation
workflow. Components can run inside one Python application; they are not
mandatory microservices.

```
+----------------------------------+
| On-call Engineer / UI            |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Investigation API                |
| Identity + incident access       |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Bounded workflow                 |
| Metrics read + deployment read   |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Approved read-only tools         |
| Source-system authorization      |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Synthetic operational records    |
| Monitoring / deployment          |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Analysis + citation validation   |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Human-review investigation report|
+----------------------------------+
```

Logical direction of work; read results return to the workflow for model context
and validation.

### 3.1 Why each component exists

| Component           | Why it exists                                               | Boundary                                   |
|---------------------|-------------------------------------------------------------|--------------------------------------------|
| Investigation API   | Validate the request and verified caller.                   | External user → trusted application.       |
| Workflow/controller | Bound allowed reads and prepare evidence context.           | Model suggestions → application decisions. |
| Read-only tools     | Integrate with operational systems under narrow contracts.  | Application → business source systems.     |
| Analysis            | Explain evidence and uncertainty.                           | Source records → untrusted model output.   |
| Report validator    | Check response shape and that referenced IDs were returned. | Untrusted result → user-visible report.    |

### 3.2 Minimal typed contracts (examples only)

No full implementation code is included. These small JSON examples show the
contracts.

#### Investigation request

```
{
  "incident_id": "INC-42",
  "service": "checkout-api",
  "question": "Why is it slow?"
}
```

#### Metrics tool result

```
{
  "evidence_id": "METRIC-07",
  "p95_latency_ms": 1800,
  "baseline_p95_ms": 240,
  "error_rate_percent": 3.1
}
```

#### Deployment tool result

```
{
  "evidence_id": "CHANGE-03",
  "version": "v2.7.4",
  "deployed_at": "09:55"
}
```

#### Investigation outcome

```
{
  "status": "needs_review",
  "evidence_ids": [
    "METRIC-07", "CHANGE-03"
  ],
  "action_executed": false
}
```

> **Trust the server, not request fields**  
> The backend derives principal, tenant and allowed incident scope from verified
> context. The user’s request and the model do not provide authoritative identity
> or permissions.

### 3.3 Happy-path sequence

1. Validate incident ID and verify engineer access.
2. Call monitoring tool with trusted principal and service scope.
3. Call deployment tool under the same source-specific authorization checks.
4. Build context with retrieved evidence and provenance.
5. Analyze observations and possible causes.
6. Validate response shape and referenced evidence IDs.
7. Return `needs_review`; no production action.

### 3.4 Important failure path: metrics timeout

```
+---------------------------+
| get_metrics: TIMEOUT      |
+---------------------------+
             |
             v
+---------------------------+
| get_deployments: SUCCESS  |
| CHANGE-03 available       |
+---------------------------+
             |
             v
+---------------------------+
| Insufficient evidence     |
| No causal conclusion      |
+---------------------------+
```

Expected status: `insufficient_evidence`, with `missing_evidence: ["metrics"]`
and no supported root-cause claim. An authorization failure is different: stop
before exposing protected evidence.

## STAGE 4 — Local synthetic mock and verification

We then implemented the Stage 3 design in Python using standard-library
components and synthetic JSON records. The workflow ran locally without cloud
credentials. This stage tested architecture behavior, not real LLM intelligence.

### 4.1 Main components of the mock

| File / role            | What it does                                                                           |
|------------------------|----------------------------------------------------------------------------------------|
| `auth.py`              | Simulated identities, tenant scope and incident registry. **Not real authentication.** |
| `tools.py`             | Two read-only tools and repeated service/tenant access checks.                         |
| `investigator.py`      | Fixed workflow, deterministic analysis, evidence-ID validation and events.             |
| `app.py`               | Command-line entry point that prints JSON results.                                     |
| `data/*.json`          | Fictional monitoring and deployment records.                                           |
| `specialist_server.py` | Optional separate local HTTP specialist. **Not A2A.**                                  |
| `timeline.html`        | Offline viewer for recorded scenarios. **Not AG-UI.**                                  |

### 4.2 Observed scenario outcomes

| Scenario                      | Expected/recorded result                                   | Lesson                                                     |
|-------------------------------|------------------------------------------------------------|------------------------------------------------------------|
| Authorized investigation      | `needs_review`; two evidence IDs; `action_executed=false`. | Evidence is shown for human review.                        |
| Metrics tool fails            | `insufficient_evidence`; missing metrics; no hypothesis.   | Missing data must not become a confident answer.           |
| Wrong service or tenant       | `ACCESS_DENIED`.                                           | Data access is controlled independently of the model.      |
| Fabricated citation           | Output rejected.                                           | Claimed IDs must exist in returned evidence.               |
| Optional specialist available | Extra unverified diagnostic suggestion.                    | Remote suggestions are not authoritative operational data. |

> **Verification record from the Stage 4 lesson**  
> Eight automated software tests were reported passing. They checked successful
> execution, denial, cross-tenant access, tool-level authorization, missing
> metrics, fake citations, unknown incidents and invalid requests. This study
> guide summarizes the recorded lesson; it does not rerun that earlier project.

### 4.3 Demo commands (not source files)

```
python app.py
python app.py --fail-metrics
python app.py --user operator-9
python -m unittest discover -s tests -v
```

Commands from the Stage 4 project. They require that project’s Python files;
this study guide intentionally does not embed them.

### 4.4 What Stage 4 did not prove

- **Not a real LLM:** `MockAnalyst` generated deterministic results.
- **Not real login:** the `--user` flag selected a synthetic fixture.
- **Not semantic fact verification:** matching evidence IDs does not prove the
  claim’s truth.
- **Not MCP/A2A:** tools were Python calls; optional specialist was plain HTTP
  JSON.
- **Not enterprise availability:** no persistent audit, traffic management, or
  disaster recovery.

## STAGE 5A — Evolution 1: Bounded model tool calling

We evolve the baseline only where a new requirement justifies the change: the
next diagnostic read may depend on what the incident needs. The model can
propose tools, but never execute arbitrary operations.

### 5.1 Requirement → baseline gap → change → check → trade-off

| Design step             | Evolution 1 decision                                                                                                                            |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| **New requirement**     | Permit model-driven selection of approved diagnostic reads.                                                                                     |
| **Baseline gap**        | Stage 4 always used the same two tools; analysis was deterministic.                                                                             |
| **Architecture change** | Add a bounded agent controller and optional real-model provider. All tool calls pass an application allowlist and incident-scope authorization. |
| **Operational check**   | Reject unknown tools, unexpected arguments, duplicate/excessive calls and unsupported evidence IDs.                                             |
| **Trade-off**           | More flexibility and model cost/uncertainty; less freedom than an unbounded autonomous agent.                                                   |

### 5.2 Revised request flow

```
+-----------------------------------+
| Engineer requests INC-42 analysis |
+-----------------------------------+
                  |
                  v
+-----------------------------------+
| Verify incident access            |
+-----------------------------------+
                  |
                  v
+-----------------------------------+
| Model proposes read-only tools    |
+-----------------------------------+
                  |
                  v
+-----------------------------------+
| Controller validates entire batch |
| Allowlist + schema + call budget  |
+-----------------------------------+
                  |
                  v
+-----------------------------------+
| Tools enforce tenant/service scope|
| Return metrics / deployments      |
+-----------------------------------+
                  |
                  v
+-----------------------------------+
| Model analyzes actual tool results|
+-----------------------------------+
                  |
                  v
+-----------------------------------+
| Validator checks report references|
+-----------------------------------+
                  |
                  v
+-----------------------------------+
| Engineer reviews; no writes       |
+-----------------------------------+
```

A two-phase bounded tool-proposal and analysis flow, not an unrestricted
iterative autonomous loop.

### 5.3 Tool contract: model supplies no scope fields

#### Permitted proposal

```
{
  "name": "get_metrics",
  "arguments": {}
}
```

#### Rejected proposal

```
{
  "name": "restart_service",
  "arguments": {
    "service": "checkout-api"
  }
}
```

The service and tenant are derived from the verified incident registry. The
model is not permitted to supply `user_id`, `tenant_id` or another target
service. The tools themselves repeat authorization checks.

### 5.4 Hard limits in Evolution 1

| Control                    | Bounded policy                               | Safety effect                                       |
|----------------------------|----------------------------------------------|-----------------------------------------------------|
| Allowlist                  | `get_metrics` and `get_deployments` only     | Unknown or write tools are rejected.                |
| Argument schema            | Empty JSON object `{}`                       | Model cannot change incident scope.                 |
| Call budget                | Maximum two distinct tool calls per run      | Limits repeated or unbounded execution.             |
| Batch validation           | Validate proposed calls before executing any | A bad proposal cannot partially execute first.      |
| Missing mandatory evidence | `insufficient_evidence`                      | Skip or timeout does not become a root-cause claim. |
| Report validation          | Check structure and returned evidence IDs    | Reject fabricated references.                       |
| Remediation tools          | None                                         | Cannot restart or roll back through this interface. |

### 5.5 Rejection path: a model requests restart

```
+----------------------------+
| Model proposes restart     |
+----------------------------+
              |
              v
+----------------------------+
| Allowlist check            |
+----------------------------+
              |
              v
+----------------------------+
| REJECT TOOL REQUEST        |
| No source/write call made  |
+----------------------------+
```

> **Model output is not authorization**  
> A system prompt saying “do not restart” is useful guidance, but the actual
> safety control is the application’s deny-by-default dispatch logic and absence
> of write tools.

### 5.6 Optional model adapter and verification status

The Stage 5A study implementation included an optional OpenAI Responses API
adapter. It used a model request to propose tool calls, then a structured
analysis request supplied with the actual results. Tool results were correlated
to proposed calls using their `call_id`. This was not a fully iterative
tool-selection loop.

#### Locally exercised

Scripted model proposals; two-tool dispatch; access-denial and timeout branches;
offline adapter parsing/format tests; citation rejection.

#### Not exercised

Live hosted-model calls, real identity provider, production authorization,
semantic factual verification, rate limiting and real incident remediation.

> **Verification record from the Stage 5A lesson**  
> Twenty-three automated tests were reported passing, including prior Stage 4
> regression tests and new controller/adapter cases. The live model integration
> was **not** executed or model-compatibility-verified in that session.

### 5.7 Stage 5A design judgment

Keep the deterministic workflow for known, predictable steps. Use bounded
model-proposed tool selection when adaptive diagnostics provide real value.
Never let the model choose an arbitrary target service, grant itself access, or
execute a production write.

## Architecture decisions and open gaps

### Decisions made through Stage 5A

| Decision                               | Reason                                         | Current result                                         |
|----------------------------------------|------------------------------------------------|--------------------------------------------------------|
| One incident before many products      | Keep scope testable.                           | INC-42 synthetic case.                                 |
| Read-only tools                        | Prevent accidental high-impact actions.        | No production write capability.                        |
| Source-system ownership                | AI text is not authoritative operational data. | Metrics and changes owned by fixtures/source adapters. |
| Access checks in application and tools | Model/request data are not credentials.        | Incident/tenant/service denial tests.                  |
| Evidence IDs and uncertainty           | A hypothesis needs support and limitations.    | Missing-evidence states and citation checks.           |
| Bounded model proposals                | Introduce useful flexibility with safe limits. | Two approved, no-argument tool names.                  |
| Defer platform protocols               | No demonstrated reuse/delegation need yet.     | MCP/A2A/GenUI not required in current implementation.  |

### What we have deliberately not built

| Future capability                 | Introduce when this requirement appears                                                               |
|-----------------------------------|-------------------------------------------------------------------------------------------------------|
| MCP / tool governance             | Several independent AI clients need interoperable, reusable governed tools.                           |
| RAG / runbook retrieval           | Large, permissioned and changing document collections become necessary.                               |
| Durable orchestration / approvals | Long-running work or production writes must survive interruption and require approved action.         |
| AG-UI, A2UI or MCP Apps           | Specific frontend streaming, declarative rendering or embedded-host UI needs emerge.                  |
| Multi-agent / A2A                 | Independent specialist teams or services require delegated tasks with their own lifecycle.            |
| Enterprise operations             | Real users, tenants, model changes and traffic justify IAM, tracing, eval gates, quotas and recovery. |

> **Next learning step — not included in this guide**  
> Stage 5 Evolution 2 will examine reusable tool integrations and when MCP is
> worth its additional boundary. The current guide ends at Stage 5 Evolution 1.

## Glossary and source map

- **p95 latency** — 95th percentile of request latency; 95% of measured requests
  are at or below this value.
- **Evidence ID** — Stable reference to a record retrieved from an approved
  source.
- **Grounding** — Supporting generated claims with retrieved evidence.
- **Authorization (AuthZ)** — Decision that a verified actor may perform a
  specified operation on a resource.
- **Tool allowlist** — Explicit set of permitted executable operations.
- **Tool budget** — Limit on number or cost of tool calls during one run.
- **Structured output** — Model response shaped according to a defined schema.
- **Trust boundary** — Point where input/data crosses into a system with
  different authority.
- **MCP** — Tool/data interoperability boundary between compatible AI host
  clients and servers.
- **A2A** — Agent-to-agent communication across independently operating
  services.
- **AG-UI** — Agent-to-frontend run/event protocol, distinct from MCP tool
  transport.
- **Idempotency** — Property that retrying the same logical action does not
  create duplicate effects; needed when writes arrive later.

### Source materials

This guide consolidates the teaching decisions, examples and local test reports
from our lessons through Stage 5A, aligned with the following flat Project
sources:

- `SKILL.md` — progressive teaching contract.
- `sdt-catalog.md` — design #73 route.
- `sdt-module-09-advanced-ai.md` — primary capstone module.
- `sdt-anchor-73-unified-enterprise-agentic-platform.md` — case-specific
  sequence and trade-offs.
- `concept-protocol-boundaries.md` — why MCP, A2A and UI protocols solve
  different needs.
- `concept-production-controls.md` — authorization, groundedness, observability
  and failure controls.

**Official documentation for future implementation checks:
** [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling) · [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) · [MCP specification](https://modelcontextprotocol.io/specification).
Version-dependent SDK behavior should be checked again before production use.

> **Accuracy note**  
> All incident figures are fictional. The Stage 4 (8 tests) and Stage 5A (23
> tests) numbers are taken from the earlier lesson reports, not rerun as part of
> generating this standalone study guide. This HTML includes no credentials,
> complete Python code or live API calls.
