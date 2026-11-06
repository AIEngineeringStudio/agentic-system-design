# Cross-module reference — production controls for agentic systems

Use this reference only when the case requires production hardening, a failure
scenario, or a cross-cutting security / operations explanation. Do not teach
this as a disconnected checklist before a basic design.

## Derive controls from risks

| Requirement / risk                 | What breaks in a naïve agent                     | Mechanism                                                      | Operational evidence                           |
|------------------------------------|--------------------------------------------------|----------------------------------------------------------------|------------------------------------------------|
| Identity and per-record access     | Agent uses guessed or model-provided record ID   | Verified identity + server-side AuthZ on each data/tool call   | Denied cross-user access                       |
| Prompt injection in retrieved text | Untrusted source sends instruction-like text     | Treat source as data; restrict high-impact tools independently | Red-team execution blocked                     |
| Unauthorized UI action             | Generated button appears to approve an operation | Backend checks user, resource, expiry and action intent        | Negative authorization test                    |
| Duplicate writes after timeout     | Tool retries email/refund twice                  | Stable operation ID + dedupe ledger + reconciliation           | Crash/retry replay produces one logical effect |
| Interrupted workflow               | Model run loses steps after failure              | Durable state machine/checkpoint and explicit recovery         | Restart resumes from committed state           |
| Outdated retrieval                 | AI answers from old index                        | Freshness contract, rebuild/change propagation and timestamp   | Stale data detected/labelled                   |
| High request rate                  | Tokens/tools exceed budgets                      | Quotas, admission control and bounded retries                  | Cost, p95 and throttled request metrics        |
| Hallucination / citation failure   | Model cites nonexistent evidence                 | Evidence IDs, retrieval evals, output validation               | Grounding regression dataset                   |
| Cross-tool debugging               | Tool error hidden behind chat answer             | Correlation IDs and trace spans over calls                     | Full failure timeline with redaction           |
| Bad model update                   | Candidate silently regresses                     | Version pinning, offline evaluation and canary                 | Rollback on quality failure                    |
| Tenant data leakage                | Shared context/cache crosses company scope       | Tenant-scoped state, credentials and retrieval                 | Isolation tests and audits                     |

## Example authorized action sequence

```text
+----------------------------+
|  Agent proposes an action  |
+----------------------------+
              |
              v
+----------------------------+
|  Application stores draft  |
|  and stable operation ID   |
+----------------------------+
              |
              v
+----------------------------+
|  User reviews and approves |
+----------------------------+
              |
              v
+----------------------------+
|  Business service checks   |
|  identity + policy + state |
+----------------------------+
              |
              v
+----------------------------+
|    Idempotent execution    |
+----------------------------+
              |
              v
+----------------------------+
|  Audit + reconcile result  |
+----------------------------+
```

**Important:** a timeout does not prove that the business effect failed. Use
provider/status reconciliation before blindly retrying.

## Agent quality is not the same as service uptime

Production monitoring should distinguish: service availability, individual
model/tool step errors, true task success, factual accuracy/grounding, human
correction rate, user-visible latency, token spend and sensitive-data incidents.
Quality evaluation should use representative test cases and known failure
scenarios, not a learner quiz.

## Official starting points

- OWASP GenAI Security: https://genai.owasp.org/
- OpenTelemetry GenAI semantic
  conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- LangGraph persistence (implementation
  reference): https://docs.langchain.com/oss/python/langgraph/persistence
- AWS Agentic AI Well-Architected
  Lens: https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/

Validate version- and cloud-specific claims before stating exact limits, SDK
behavior or service guarantees.
