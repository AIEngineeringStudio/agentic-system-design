# Optional production-design completeness reference

**This is a tutor reference, never a learner assessment.** Use only when
finalizing a design or when asked for a production review.

- Problem, actors, scope, assumptions and quality priorities are explicit.
- The design names the source of truth and trust boundaries.
- Every added component has a requirement justifying it.
- Model/tool boundary has server-side authorization.
- Data minimization, privacy and tenant isolation are considered.
- One happy path and one failure/recovery sequence are shown.
- Side-effecting calls include idempotency and unknown-outcome handling.
- UI-host support, capabilities and fallback are clear if using MCP Apps or
  A2UI.
- Telemetry covers actual task outcomes and errors.
- Quality evaluation and safe rollout are considered where appropriate.
- Cost and operational ownership have been identified.
- Alternatives, trade-offs and residual risks are explained.
- Diagrams use continuous ASCII outlines and arrows.
