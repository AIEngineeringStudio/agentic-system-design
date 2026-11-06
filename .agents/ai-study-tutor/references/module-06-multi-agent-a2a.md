# Module 06 — Multi-agent systems and A2A interoperability

**Learning boundary:** Use delegation only with clear capability, ownership,
latency and trust benefits.

**One-line mental model:**
`Coordinator -> specialist or remote A2A agent -> typed result/artifact`

## Necessary concepts, only when the case needs them

A specialist can be an in-process tool/agent handoff; **A2A** is for
interoperating with independent agent services, using discovery metadata, task
lifecycle and artifacts. Cross-agent messages and Agent Cards are untrusted
input until validated. A network of agents is not automatically better than one
agent with tools.

## Patterns and decisions to reuse

- **Primary decision rule:** Define responsibility and task ownership before
  adding supervisors, brokers or agent directories.
- Start with the baseline boundary and identify source of truth, authority and
  error semantics before selecting products.
- Show one happy path and one failure path, then justify added components as
  responses to constraints.
- Keep code labs small and local with fake records; label production
  architecture as a design, not deployed implementation.

## Problem briefs (these are design prompts, not pre-solved lessons)

### #42 — Supervisor and specialist investigators ★ anchor

**User need:** Delegate log, metric and change-history research.

- **Teach on demand:** Supervisor/worker, delegation contracts.
- **Small working lab:** Coordinate three mock specialist agents.
- **Production evolution:** Bound recursion, filter context and resolve
  disagreements.
- **Decision to explain:** Many tools on one agent vs specialists.

### #43 — Remote fraud specialist via A2A ★ anchor

**User need:** Ask an independently deployed agent to score a case.

- **Teach on demand:** A2A Agent Cards, task and artifact flow.
- **Small working lab:** Call a fake external specialist by A2A-compatible
  interface.
- **Production evolution:** Authenticate boundary, validate artifacts and
  correlate tasks.
- **Decision to explain:** Local handoff vs A2A remote agent.

### #44 — Multi-vendor agent broker

**User need:** Select between agents from different providers.

- **Teach on demand:** Agent discovery and routing policy.
- **Small working lab:** Route sample requests to two mock agents.
- **Production evolution:** Capabilities trust, quota, health and data routing.
- **Decision to explain:** Static routing vs dynamic agent registry.

### #45 — Long-running A2A research task

**User need:** Remote research remains pending during other work.

- **Teach on demand:** Task states, progress and artifacts.
- **Small working lab:** Start, poll/cancel and collect mock task artifact.
- **Production evolution:** Durable status, task ACL, late results and expiry.
- **Decision to explain:** Sync vs async remote agent.

### #46 — Customer-service handoff network

**User need:** Triage user problems to billing or technical agents.

- **Teach on demand:** Handoffs, context transfer and ownership.
- **Small working lab:** Implement typed triage/handoff to mock specialists.
- **Production evolution:** Avoid history leakage and unclear responsibility.
- **Decision to explain:** Supervisor retained control vs takeover.

### #47 — Multi-agent peer review

**User need:** A second agent checks the first report.

- **Teach on demand:** Independent review, evidence and conflict.
- **Small working lab:** Produce two analyses and deterministic reconciliation.
- **Production evolution:** Correlated errors, budgets and human accountability.
- **Decision to explain:** One agent with self-review vs independent checks.

### #48 — Cross-organization procurement assistants

**User need:** Buyer and supplier systems exchange bounded quotes.

- **Teach on demand:** Cross-org identity and authority.
- **Small working lab:** Exchange fake quotes between two hosted agents.
- **Production evolution:** Price bounds, signed terms and audit.
- **Decision to explain:** Business rules vs free-form negotiation.

### #49 — Enterprise agent directory

**User need:** Operators need a governed catalog of agents.

- **Teach on demand:** Registry, ownership, capability metadata.
- **Small working lab:** Search sample Agent Cards.
- **Production evolution:** Approve provenance, revoke access and version
  endpoints.
- **Decision to explain:** Open discovery vs trusted registry.

## Example baseline diagram for this module

```text
+-----------------------------+
|       User requirement      |
+-----------------------------+
              |
              v
+-----------------------------+
|      Smallest valid flow    |
+-----------------------------+
              |
              v
+-----------------------------+
|    Business source of truth |
+-----------------------------+
```

**Important:** This is only a visual placeholder. Draw the actual components
from the selected case requirements; do not present this as the final
architecture. Keep diagrams connected with solid `+ - |` lines and arrows.

**Case IDs in this module:** #42, #43, #44, #45, #46, #47, #48, #49.
