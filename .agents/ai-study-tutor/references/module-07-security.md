# Module 07 — Security, identity and enterprise architecture

**Learning boundary:** Keep permissions, boundaries and high-risk side effects
outside model-controlled logic.

**One-line mental model:**
`Identity -> policy decision -> protected data/tool boundary -> audit`

## Necessary concepts, only when the case needs them

Authentication proves caller identity; authorization determines whether an
action on a resource is allowed. Retrieved data, model outputs, third-party
Agent Cards, documents and HTML are untrusted. Prompt-level warnings cannot
replace tool-side access controls, approval, data classification and isolation.

## Patterns and decisions to reuse

- **Primary decision rule:** Always show the attack/failure path next to the
  allowed path, without asking the learner to defend the system as a quiz.
- Start with the baseline boundary and identify source of truth, authority and
  error semantics before selecting products.
- Show one happy path and one failure path, then justify added components as
  responses to constraints.
- Keep code labs small and local with fake records; label production
  architecture as a design, not deployed implementation.

## Problem briefs (these are design prompts, not pre-solved lessons)

### #50 — Injection-resistant knowledge assistant ★ anchor

**User need:** A retrieved page tries to instruct the model to call a privileged
tool.

- **Teach on demand:** Prompt injection, untrusted data boundary.
- **Small working lab:** Test malicious document and show external policy blocks
  an action.
- **Production evolution:** Independent authorizer, sandbox and red-team tests.
- **Decision to explain:** Prompt wording vs hard technical enforcement.

### #51 — Central policy engine for agent actions

**User need:** Agents share write-capable business tools.

- **Teach on demand:** Policy decision/enforcement, RBAC and ABAC.
- **Small working lab:** Place a policy check before a mock write action.
- **Production evolution:** Fail-safe policy, audit, revocation and versioning.
- **Decision to explain:** Agent-specific guards vs policy service.

### #52 — Delegated identity across MCP

**User need:** Agent calls the user's CRM securely.

- **Teach on demand:** OAuth delegation, scopes, audience.
- **Small working lab:** Mock per-user credentials and revocation.
- **Production evolution:** Server-side verification, token handling and tenant
  isolation.
- **Decision to explain:** Service principal vs delegated identity.

### #53 — Computer-use assistant sandbox

**User need:** Work in a legacy UI without an API.

- **Teach on demand:** Browser sandbox, visual actions, approvals.
- **Small working lab:** Fill a local fake admin form with a preview gate.
- **Production evolution:** Limit network, secrets, downloads and domain access.
- **Decision to explain:** API integration vs computer use fallback.

### #54 — Sensitive-document AI workspace

**User need:** Support restricted contract analysis.

- **Teach on demand:** Classification, DLP, retention.
- **Small working lab:** Query synthetic sensitive documents with role-based
  access.
- **Production evolution:** Minimize prompt exposure, redact and honor deletion.
- **Decision to explain:** Central knowledge base vs isolated store.

### #55 — Multi-tenant agent platform

**User need:** Run many customer agents on shared infrastructure.

- **Teach on demand:** Control/data plane and tenant quotas.
- **Small working lab:** Isolate two simulated tenants' state and credentials.
- **Production evolution:** Audit, noisy-neighbor controls and cross-tenant
  tests.
- **Decision to explain:** Shared runtime vs dedicated tenant deployment.

### #56 — Auditable payment-operations copilot

**User need:** Investigate payment problems without moving funds autonomously.

- **Teach on demand:** Ledger invariants, approval and reconciliation.
- **Small working lab:** Propose remediation using fake transaction records.
- **Production evolution:** Separation of duties, idempotency, unknown outcomes.
- **Decision to explain:** AI recommendations vs deterministic payments.

### #57 — Agent supply-chain security

**User need:** Agents load third-party tools and instruction packs.

- **Teach on demand:** Supply-chain provenance, manifest and capability review.
- **Small working lab:** Check an allowlisted local skill/tool registry.
- **Production evolution:** Version pinning, sandboxing, signature/review and
  revocation.
- **Decision to explain:** Arbitrary discovery vs curated catalog.

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

**Case IDs in this module:** #50, #51, #52, #53, #54, #55, #56, #57.
