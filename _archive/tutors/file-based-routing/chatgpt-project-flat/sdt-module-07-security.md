# Module 07 — Security, identity and enterprise architecture

**File:** `sdt-module-07-security.md`  
**IDs:** #50–#57  
**Module learning goal:** Keep authorization, privacy and action policy outside
the model and at business boundaries.

## Architectural mental model

`Identity -> policy decision -> protected tool/data -> audited effect`

Prompt instructions are not access control. Every privileged action is
re-authorized at the service boundary.

## Teaching requirements within this module

Start with the stated business scenario and source of truth. Introduce the
concepts in the **Basics** field only when they unblock the current stage. First
draw the smallest appropriate architecture and implement a safe local mock. Then
show how the named production concern changes it. Do not reveal the reference
final architecture at the beginning of a lesson. Do not quiz the learner. If a
case is marked as an anchor in `sdt-catalog.md`, check whether its individual
anchor file is available; otherwise derive the same depth from this case brief.

## Case briefs

### #50 Injection-resistant knowledge assistant [DEEP-DIVE ANCHOR]

- **Problem:** Block instructions hidden in untrusted documents.
- **Basics at point of use:** Trust boundaries, prompt injection, least
  privilege.
- **Working mock:** Plant a fake hostile passage; verify privileged action is
  rejected.
- **Production evolution:** Red teaming, tool policy, context labeling and
  audits.
- **Architectural trade-off:** Prompt warnings vs enforcement.

### #51 Central policy engine for agent actions

- **Problem:** Apply consistent rules across high-risk tools.
- **Basics at point of use:** RBAC/ABAC, policy decisions, enforcement.
- **Working mock:** Put mock policy service before writes.
- **Production evolution:** Revocation, fail-safe availability and logs.
- **Architectural trade-off:** Agent-specific policy vs shared policy layer.

### #52 Delegated identity across MCP

- **Problem:** Access a user's records through an MCP tool.
- **Basics at point of use:** OAuth, token audience, delegated rights.
- **Working mock:** Simulate scoped tokens and unauthorized access tests.
- **Production evolution:** Prevent token passthrough and confused deputies.
- **Architectural trade-off:** Delegation vs service account.

### #53 Computer-use assistant sandbox

- **Problem:** Work through a browser when APIs are missing.
- **Basics at point of use:** Browser isolation, action grounding, approvals.
- **Working mock:** Preview changes to a local admin form.
- **Production evolution:** Credential secrecy, domain allowlist and human
  consent.
- **Architectural trade-off:** Direct API vs computer use.

### #54 Sensitive-document AI workspace

- **Problem:** Query confidential contracts without leakage.
- **Basics at point of use:** Classification, DLP, retention.
- **Working mock:** Build role-scoped retrieval over fake sensitive docs.
- **Production evolution:** Redaction, encryption, deletion and policy audit.
- **Architectural trade-off:** Shared search index vs restricted isolation.

### #55 Multi-tenant agent platform

- **Problem:** Keep multiple customer workspaces isolated.
- **Basics at point of use:** Tenant separation and quotas.
- **Working mock:** Run fake tenants through an agent with isolated state.
- **Production evolution:** Cross-tenant cache/credential tests and metering.
- **Architectural trade-off:** Shared runtime vs dedicated tenant.

### #56 Auditable payment-operations copilot

- **Problem:** Recommend remediation without automatically moving funds.
- **Basics at point of use:** Immutable audit, approval, ledger invariants.
- **Working mock:** Produce fake case recommendations and mock authorized steps.
- **Production evolution:** Separation of duties and transaction reconciliation.
- **Architectural trade-off:** AI recommendation vs deterministic financial
  execution.

### #57 Agent supply-chain security

- **Problem:** Review third-party skills, tools and integrations.
- **Basics at point of use:** Manifest trust, dependency provenance.
- **Working mock:** Allowlist mock tool/skill packages by version.
- **Production evolution:** Quarantine untrusted extensions and audit upgrades.
- **Architectural trade-off:** Dynamic discovery vs approved catalog.

## Common misconceptions to correct

- Having an AI model in a request path does not automatically require agent
  orchestration.
- A technically valid diagram is not sufficient without authorization, state
  ownership and failure behavior.
- Examples should use synthetic data, explicitly labeled assumptions and local
  runnable behavior where possible.
