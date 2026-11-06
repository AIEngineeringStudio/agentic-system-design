# Module 02 — MCP tools, data access and remote integrations

**Learning boundary:** Design governed tool/resource boundaries and distinguish
MCP core from optional extensions.

**One-line mental model:**
`AI host -> MCP client -> MCP server -> service/data source`

## Necessary concepts, only when the case needs them

**MCP core** is a protocol for tools, resources and prompts between clients and
servers. **Host** is the application that manages clients. Tool calls have typed
contracts; resources are readable context. **MCP Apps** and **MCP Tasks** are
optional extensions; never assume all hosts support them. Exact
handshake/transport and authorization rules depend on the negotiated spec/SDK
version.

## Patterns and decisions to reuse

- **Primary decision rule:** Do not expose privileged actions just because the
  MCP schema lists them. Authorize at the service.
- Start with the baseline boundary and identify source of truth, authority and
  error semantics before selecting products.
- Show one happy path and one failure path, then justify added components as
  responses to constraints.
- Keep code labs small and local with fake records; label production
  architecture as a design, not deployed implementation.

## Problem briefs (these are design prompts, not pre-solved lessons)

### #09 — Local ticket-lookup MCP server ★ anchor

**User need:** Let a compatible AI host inspect local ticket records.

- **Teach on demand:** MCP client/server/tool contracts and JSON-RPC.
- **Small working lab:** Make list_tickets and get_ticket tools with a local
  test client.
- **Production evolution:** Validate arguments, restrict fields and test errors.
- **Decision to explain:** Direct function tools vs reusable MCP service.

### #10 — Remote CRM MCP server

**User need:** Access CRM data through a remote MCP service.

- **Teach on demand:** Remote MCP, network transport, identity.
- **Small working lab:** Serve mock CRM tools using an official SDK.
- **Production evolution:** HTTPS, scoped credentials, timeouts and
  compatibility checks.
- **Decision to explain:** Local versus remote hosting.

### #11 — MCP tool gateway

**User need:** Several teams own MCP servers with overlapping tools.

- **Teach on demand:** Gateway, policy, tool routing.
- **Small working lab:** Route to three mock MCP services behind one catalog.
- **Production evolution:** Tool allowlists, origin checks, quotas and auditing.
- **Decision to explain:** Direct host integration vs brokered governance.

### #12 — Internal knowledge exposed as MCP resources

**User need:** Clients need controlled document reads.

- **Teach on demand:** MCP resources vs tools vs prompts.
- **Small working lab:** Expose versioned policy texts as resources.
- **Production evolution:** Source ACLs, freshness and deletion handling.
- **Decision to explain:** Resource read vs search tool invocation.

### #13 — Reusable MCP prompt catalog

**User need:** Teams reuse guided workflows in compatible hosts.

- **Teach on demand:** MCP prompts, versioning, parameter contracts.
- **Small working lab:** Publish parameterized support and incident prompts.
- **Production evolution:** Review content, safe defaults, compatibility and
  ownership.
- **Decision to explain:** Server-provided prompts vs app-owned templates.

### #14 — Enterprise MCP authorization broker ★ anchor

**User need:** Users grant limited access to internal SaaS services.

- **Teach on demand:** OAuth, delegated consent, token audience.
- **Small working lab:** Simulate per-user scoped CRM access.
- **Production evolution:** Deny token passthrough, confused-deputy access and
  cross-tenant calls.
- **Decision to explain:** User delegation vs shared service credentials.

### #15 — Multi-tenant MCP service

**User need:** Multiple customers share a service without sharing data.

- **Teach on demand:** Identity and tenant boundaries.
- **Small working lab:** Test isolated tenant ticket queries.
- **Production evolution:** Enforce tenancy at data access and budget layers.
- **Decision to explain:** Shared multi-tenant endpoint vs isolated deployment.

### #16 — Scalable MCP catalog and lookup

**User need:** Hundreds of tools make tool selection noisy.

- **Teach on demand:** Discovery, schemas, tool filtering.
- **Small working lab:** Filter a fake 100-tool catalog by user intent.
- **Production evolution:** Version schemas, cap context and handle stale
  discovery.
- **Decision to explain:** Expose all tools vs curated selection.

### #17 — Long-running report via MCP Tasks

**User need:** Reporting exceeds interactive request duration.

- **Teach on demand:** MCP Tasks optional extension, async lifecycle.
- **Small working lab:** Simulate job start, status, cancel and result
  retrieval.
- **Production evolution:** Persist task identity, reconcile retries and support
  clients without Tasks.
- **Decision to explain:** Synchronous call vs async task pattern.

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

**Case IDs in this module:** #9, #10, #11, #12, #13, #14, #15, #16, #17.
