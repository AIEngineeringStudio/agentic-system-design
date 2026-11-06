# Module 06 — Multi-agent systems and A2A interoperability

**File:** `sdt-module-06-multi-agent-a2a.md`  
**IDs:** #42–#49  
**Module learning goal:** Use specialists and cross-service agent delegation
only with clear ownership and task boundaries.

## Architectural mental model

`Coordinator -> specialist/remote A2A -> evidence/artifacts -> merge`

Independent services justify A2A; two functions in one process do not require a
remote agent protocol.

## Teaching requirements within this module

Start with the stated business scenario and source of truth. Introduce the
concepts in the **Basics** field only when they unblock the current stage. First
draw the smallest appropriate architecture and implement a safe local mock. Then
show how the named production concern changes it. Do not reveal the reference
final architecture at the beginning of a lesson. Do not quiz the learner. If a
case is marked as an anchor in `sdt-catalog.md`, check whether its individual
anchor file is available; otherwise derive the same depth from this case brief.

## Case briefs

### #42 Supervisor and specialist investigators [DEEP-DIVE ANCHOR]

- **Problem:** Delegate diagnostics to log/metrics/change specialists.
- **Basics at point of use:** Supervisor-worker, agent as tool, evidence merge.
- **Working mock:** Coordinate three mock specialist findings.
- **Production evolution:** Loop caps, source attribution and conflicts.
- **Architectural trade-off:** One agent with tools vs specialists.

### #43 Remote fraud specialist via A2A [DEEP-DIVE ANCHOR]

- **Problem:** Invoke an independently deployed risk agent.
- **Basics at point of use:** Agent Card, tasks, artifacts, remote trust.
- **Working mock:** Call a mock A2A endpoint and validate typed result.
- **Production evolution:** Authentication, status tracking and untrusted cards.
- **Architectural trade-off:** In-process handoff vs A2A.

### #44 Multi-vendor agent broker

- **Problem:** Route work among specialized external agents.
- **Basics at point of use:** Discovery, capabilities, fallback and routing.
- **Working mock:** Route sample tasks to two mock vendor agents.
- **Production evolution:** Privacy routing, quotas, health and interface
  normalization.
- **Architectural trade-off:** Static integration vs agent registry.

### #45 Long-running A2A research task

- **Problem:** Await a separate remote research agent's report.
- **Basics at point of use:** Task lifecycle, status and artifacts.
- **Working mock:** Start, monitor, cancel and retrieve a mock task.
- **Production evolution:** Expiry, task ACL and late replies.
- **Architectural trade-off:** Sync remote call vs async task.

### #46 Customer-service handoff network

- **Problem:** Route issues to billing, returns or tech specialists.
- **Basics at point of use:** Context transfer, handoff and ownership.
- **Working mock:** Simulate typed triage and two specialists.
- **Production evolution:** Limit shared history, keep responsibility and
  fallback.
- **Architectural trade-off:** Manager retains control vs handoff.

### #47 Multi-agent peer review

- **Problem:** Have a second agent independently check draft claims.
- **Basics at point of use:** Independent review and evidence comparison.
- **Working mock:** Compare two mock reports and merge substantiated claims.
- **Production evolution:** Correlated errors, caps and human oversight.
- **Architectural trade-off:** Single-model self-critique vs independent
  analysis.

### #48 Cross-organization procurement assistants

- **Problem:** Exchange quotes safely between buyer/supplier systems.
- **Basics at point of use:** Cross-org identity, bounded terms and negotiation.
- **Working mock:** Simulate proposals between two independently operated
  agents.
- **Production evolution:** Validate contract conditions in code, audit final
  agreement.
- **Architectural trade-off:** Open negotiation vs constraints.

### #49 Enterprise agent directory

- **Problem:** Catalog governed agents and their capabilities.
- **Basics at point of use:** Registry, owner, Agent Card metadata.
- **Working mock:** Search mock agent metadata by capability.
- **Production evolution:** Provenance, revocation, versioning and trust.
- **Architectural trade-off:** Open discovery vs curated directory.

## Common misconceptions to correct

- Having an AI model in a request path does not automatically require agent
  orchestration.
- A technically valid diagram is not sufficient without authorization, state
  ownership and failure behavior.
- Examples should use synthetic data, explicitly labeled assumptions and local
  runnable behavior where possible.
