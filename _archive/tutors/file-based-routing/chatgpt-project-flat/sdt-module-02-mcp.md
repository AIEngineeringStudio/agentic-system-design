# Module 02 — MCP tools, data access and remote integrations

**File:** `sdt-module-02-mcp.md`  
**IDs:** #9–#17  
**Module learning goal:** Connect AI hosts to external tools and knowledge using
governed MCP boundaries.

## Architectural mental model

`Host -> MCP client -> MCP server -> tool/resource -> owner system`

MCP core is not MCP Apps. An MCP server still needs service-side authorization,
transport validation and version-aware client support.

## Teaching requirements within this module

Start with the stated business scenario and source of truth. Introduce the
concepts in the **Basics** field only when they unblock the current stage. First
draw the smallest appropriate architecture and implement a safe local mock. Then
show how the named production concern changes it. Do not reveal the reference
final architecture at the beginning of a lesson. Do not quiz the learner. If a
case is marked as an anchor in `sdt-catalog.md`, check whether its individual
anchor file is available; otherwise derive the same depth from this case brief.

## Case briefs

### #09 Local ticket-lookup MCP server [DEEP-DIVE ANCHOR]

- **Problem:** Expose local support records to an AI host.
- **Basics at point of use:** MCP host/client/server, tool schema, JSON-RPC.
- **Working mock:** Serve list_tickets/get_ticket with fake records and a local
  client.
- **Production evolution:** Validate schemas, authorize data reads and test
  protocol errors.
- **Architectural trade-off:** Direct functions vs reusable MCP integration.

### #10 Remote CRM MCP server

- **Problem:** Expose enterprise CRM tools over network.
- **Basics at point of use:** Remote MCP transport, identity, connectivity.
- **Working mock:** Create a mock CRM MCP endpoint using verified SDK patterns.
- **Production evolution:** HTTPS, scope checks, timeouts, logging and version
  negotiation.
- **Architectural trade-off:** Local vs remote MCP integration.

### #11 MCP tool gateway

- **Problem:** Govern many teams' MCP servers in one platform.
- **Basics at point of use:** Gateway, discovery, schema catalog, tool policy.
- **Working mock:** Aggregate three mock MCP services under one routing layer.
- **Production evolution:** Origin identity, allowlists, quotas and outage
  containment.
- **Architectural trade-off:** Direct per-server access vs central broker.

### #12 Internal knowledge exposed as MCP resources

- **Problem:** Deliver reference documents to compatible clients.
- **Basics at point of use:** Tools vs resources vs prompts, URI, ACL.
- **Working mock:** Expose a versioned mock policy via an MCP resource.
- **Production evolution:** Object ACLs, cache invalidation, redaction and
  tombstones.
- **Architectural trade-off:** Resource read vs tool search.

### #13 Reusable MCP prompt catalog

- **Problem:** Publish repeatable host-visible workflow prompts.
- **Basics at point of use:** MCP prompt primitives, template parameters.
- **Working mock:** Expose support and incident review prompt templates.
- **Production evolution:** Review, governance, versioning and compatibility.
- **Architectural trade-off:** MCP prompts vs app-owned templates.

### #14 Enterprise MCP authorization broker [DEEP-DIVE ANCHOR]

- **Problem:** Call SaaS APIs with delegated per-user access.
- **Basics at point of use:** OAuth scopes, audience, consent and confused
  deputy.
- **Working mock:** Protect mock CRM calls with user-scoped grants.
- **Production evolution:** Prevent token passthrough/scope escalation; audit
  and revoke grants.
- **Architectural trade-off:** User delegation vs shared service credential.

### #15 Multi-tenant MCP service

- **Problem:** Serve several enterprises without cross-tenant reads.
- **Basics at point of use:** Tenant boundary, row-level checks, isolation.
- **Working mock:** Write negative tests for cross-tenant fake tickets.
- **Production evolution:** Separate tenant secrets, usage budgets and audit
  trails.
- **Architectural trade-off:** Shared remote MCP vs isolated endpoints.

### #16 Scalable MCP catalog and lookup

- **Problem:** Select tools from hundreds of available schemas.
- **Basics at point of use:** Tool discovery, schema routing, context budgets.
- **Working mock:** Filter a synthetic tool catalog before a model sees tools.
- **Production evolution:** Cache versioning, stale schema handling and observed
  selection quality.
- **Architectural trade-off:** Broad tool exposure vs curated relevant subset.

### #17 Long-running report via MCP Tasks

- **Problem:** Support report generation beyond an interactive timeout.
- **Basics at point of use:** Optional MCP Tasks extension, status,
  cancellation.
- **Working mock:** Simulate start/status/cancel/result with a durable job
  record.
- **Production evolution:** Host support fallback, retries, task authorization
  and expiry.
- **Architectural trade-off:** Synchronous call vs long-running task protocol.

## Common misconceptions to correct

- Having an AI model in a request path does not automatically require agent
  orchestration.
- A technically valid diagram is not sufficient without authorization, state
  ownership and failure behavior.
- Examples should use synthetic data, explicitly labeled assumptions and local
  runnable behavior where possible.
