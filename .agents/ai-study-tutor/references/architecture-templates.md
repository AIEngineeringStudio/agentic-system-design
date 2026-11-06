# ASCII diagrams and solution-architecture templates

Use only for a case's relevant stage. Replace placeholders with case-derived
components. Boxes use solid continuous lines; no dotted outlines, Mermaid, or
SVG.

## Minimal baseline

```text
+-----------------------+
|   User / application  |
+-----------------------+
            |
            v
+-----------------------+
|    Application API    |
+-----------------------+
            |
            v
+-----------------------+
|   Source of truth     |
+-----------------------+
```

Add an agent runtime only if dynamic model reasoning/tool choice is justified.
Not every design needs an agent.

## Read-only agent/tool security boundary

```text
+-----------------------+
|  Authenticated user   |
+-----------------------+
            |
            v
+-----------------------+
|  Application server   |
|  Authentication       |
+-----------------------+
            |
            v
+-----------------------+      +-----------------------+
|  Model / agent loop   |----->|  Proposed tool call   |
+-----------------------+      +-----------------------+
                                        |
                                        v
                              +-----------------------+
                              |  Service-side AuthZ   |
                              +-----------------------+
                                        |
                                        v
                              +-----------------------+
                              |  Business source      |
                              |  of truth             |
                              +-----------------------+
```

The trust check is performed by application/service code, not by a prompt.

## Sequence diagram

```text
Client              API              Tool             Source
  |                  |                 |                 |
  |---- request ---->|                 |                 |
  |                  |---- check ----->|                 |
  |                  |<--- allowed ----|                 |
  |                  |---- read ------------------------>|
  |                  |<--- response ---------------------|
  |<--- answer ------|                 |                 |
  |                  |                 |                 |
```

For side effects add `propose`, `approve`, `execute`, `reconcile`, and
unknown/timeout branches. Do not treat a timeout as confirmed failure.

## State ownership

| State            | Owner                         | Lifetime  | Who can change it?          | Failure to consider   |
|------------------|-------------------------------|-----------|-----------------------------|-----------------------|
| Session          | Application                   | Session   | Authenticated session code  | Expiry                |
| Agent execution  | Orchestrator/checkpoint store | Workflow  | Runtime state machine       | Crash/resume          |
| Business records | System of record              | Durable   | Authorized business service | Duplicate writes      |
| UI filter        | Frontend                      | Ephemeral | User action                 | Refresh or stale view |

## Decision record

1. Requirement / named constraint.
2. Option A and when it works.
3. Option B and when it works.
4. Choice and reasons.
5. Cost, failure mode and owner.
6. Signal that should trigger reconsideration.

## Production upgrade ladder

| Requirement         | Baseline failure                      | Design change                                           | Verification             |
|---------------------|---------------------------------------|---------------------------------------------------------|--------------------------|
| Record access       | Model supplies an arbitrary record ID | Server derives principal and enforces ownership         | Negative access test     |
| Duplicate operation | Retry can repeat a business effect    | Stable operation ID, idempotency ledger, reconciliation | Crash/retry smoke test   |
| Long execution      | Request times out                     | Durable task state; async interface if supported        | Resume after restart     |
| Slow retrieval      | Expensive unbounded query             | Measure, index and bound requests; cache only if needed | p95 and freshness        |
| Quality regression  | Changed prompt breaks known use cases | Repeatable evaluation and controlled release            | Evaluation before deploy |

## Protocol decision guide

- **MCP:** reusable client/server tools, resources or prompts.
- **MCP Apps:** optional inline sandboxed HTML inside a host that supports MCP
  Apps.
- **AG-UI:** events/state between agent runtime and first-party frontend.
- **A2UI:** declarative component descriptions rendered by a trusted compatible
  host.
- **A2A:** exchange tasks, metadata and artifacts with independent agents.
- **Agent Skills:** reusable instructions and supporting files; not tool
  execution or authorization.

These mechanisms can coexist, but no case needs all by default.
