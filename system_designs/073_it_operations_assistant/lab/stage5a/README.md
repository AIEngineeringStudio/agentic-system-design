# Stage 5A — Bounded model-proposed tools

This builds on Stage 4. All records remain **synthetic**, the CLI identity remains **simulated**, and the application has **no write tool**.

## Local runnable path (no dependencies)

```bash
python app_agent.py
python app_agent.py --fail-metrics
python app_agent.py --user operator-9
python -m unittest discover -s tests -v
```

`ScriptedProvider` simulates what a model would request. It is **not an LLM**.

## Optional hosted-model path (not executed in this environment)

If you have separate API credentials and access to a supported model, set:

```bash
export OPENAI_API_KEY='your-api-key'
export OPENAI_MODEL='a-model-available-in-your-api-project'
python app_agent.py --real-model
```

This calls the OpenAI Responses API with **synthetic data only**. No SDK package is required. The adapter has two model calls: (1) tool proposal, (2) structured evidence analysis using matching `function_call_output` items. It does not perform a full iterative tool selection loop. Real model behavior and model-specific compatibility **have not been tested here**. Model calls may incur API charges.

Official API documentation (verified 2026-11-06):
- https://developers.openai.com/api/docs/guides/function-calling
- https://developers.openai.com/api/docs/guides/structured-outputs

## Key safety behavior

- Server resolves `incident_id` to a trusted service/tenant.
- Model tool names and arguments are validated against an allowlist before **any** tool executes.
- `get_metrics` and `get_deployments` both check authorization.
- A model **cannot** set a service name, user ID or tenant ID for tool execution.
- Tool-call budget is two distinct read-only tool names per run.
- Bad citations are rejected; a valid ID alone does not prove semantic support.
- Missing metrics or skipped required tools yields `insufficient_evidence`.
- Unauthorized incident access terminates before contacting the model.

## Not production-ready

No real authentication, no deployment environment, no persistent audit storage, no factual verifier, no rate limiting, no durable orchestration, no formal data retention/prompt-leakage review, no certified uptime. The local fixtures are for learning only. Add those controls by requirement in later Stage 5 increments.
