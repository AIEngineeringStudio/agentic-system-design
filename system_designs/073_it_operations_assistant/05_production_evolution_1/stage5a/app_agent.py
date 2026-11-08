"""Entry point for Stage 5A; default scripted model, optionally hosted LLM."""
import argparse
import json
from auth import simulated_identity
from stage5_agent import RejectedToolRequest, investigate_with_model
from investigator import InvalidModelOutput


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded INC-42 investigation (synthetic data)")
    parser.add_argument("--user", default="operator-5", help="Synthetic identity, NOT login")
    parser.add_argument("--incident", default="INC-42")
    parser.add_argument("--question", default="Why is Checkout API slow?")
    parser.add_argument("--fail-metrics", action="store_true")
    parser.add_argument("--real-model", action="store_true", help="Use hosted Responses API (optional)")
    args = parser.parse_args()
    try:
        provider = None
        if args.real_model:
            from openai_provider import OpenAIProvider
            provider = OpenAIProvider()
        result = investigate_with_model(
            simulated_identity(args.user), args.incident, args.question,
            provider=provider, simulate_metrics_timeout=args.fail_metrics,
        )
        print(json.dumps(result, indent=2))
        return 0
    except (PermissionError, LookupError, ValueError, RuntimeError,
            RejectedToolRequest, InvalidModelOutput) as exc:
        print(json.dumps({"status": "error", "code": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
