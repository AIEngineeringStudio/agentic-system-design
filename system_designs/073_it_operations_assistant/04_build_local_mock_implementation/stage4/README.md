# Stage 4: INC-42 IT Operations Assistant (local mock)

A **fully local, synthetic, read-only demonstration** of the architecture from Stage 3 of AI Design #73.

## Requirements

- Python 3.10+ (standard library only)
- No API keys, third-party packages, network access, or real data for the default mode

## Run

```bash
python app.py
python app.py --user operator-9
python app.py --user external-1
python app.py --fail-metrics
python -m unittest discover -s tests -v
```

## Optional independently running mock specialist (plain HTTP, **not A2A**)

Terminal 1:

```bash
python specialist_server.py
```

Terminal 2:

```bash
python app.py --specialist-url http://127.0.0.1:8765/diagnose
```

This specialist is optional. It receives only the service name and evidence IDs, and returns an **unverified investigation suggestion**, not a fact or an authorization. Neither A2A nor MCP is implemented. The two initial tool calls are direct in-process Python functions.

## Source of truth and permissions

- `data/metrics.json`: synthetic monitoring evidence.
- `data/deployments.json`: synthetic change evidence.
- `auth.py`: fictional incident registry and simulated identity fixture.
- `tools.py`: rechecks tenant/service access at each data operation.
- `investigator.py`: fixed two-tool workflow, visible event timeline, deterministic mock analyst, evidence-ID validation.
- `app.py`: CLI interface, **not** a production authentication/API layer.

## Limitations and safeguards

1. **No real LLM**: `MockAnalyst` is deterministic Python code. It exercises the contract and workflow, but it is not an agent model or an AI-generated diagnosis.
2. `--user` chooses a local fixture; it **does not authenticate** a real person. Do not expose this demo as a service or connect it to production.
3. Model output is checked for claimed evidence IDs. This is not semantic fact verification; future stages require groundedness evaluation and stronger report validation.
4. No operations can restart, roll back, or write to any service. All operational tools read synthetic JSON.
5. The optional localhost HTTP specialist is deliberately minimal and unauthenticated. Do not expose it to a network.
6. No MCP, A2A, AG-UI, or production workflow engine is claimed or needed for this baseline.

## Offline visual preview

Open `timeline.html` in a browser. It is a self-contained, light-mode, print-friendly viewer for the four sample JSON outputs. Selecting a scenario changes the displayed recorded data; it does not execute a new investigation.
