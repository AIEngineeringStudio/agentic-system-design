"""CLI entry point for the INC-42 local investigation mock."""
import argparse
import json
from auth import simulated_identity
from investigator import InvalidModelOutput, investigate


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only synthetic IT incident investigator")
    parser.add_argument("--incident", default="INC-42")
    parser.add_argument("--user", default="operator-5", help="SIMULATED identity; not authentication")
    parser.add_argument("--question", default="Why is Checkout API slow?")
    parser.add_argument("--fail-metrics", action="store_true")
    parser.add_argument("--specialist-url", help="Optional localhost-only JSON mock specialist")
    args = parser.parse_args()
    try:
        principal = simulated_identity(args.user)
        result = investigate(principal, args.incident, args.question,
                             simulate_metrics_timeout=args.fail_metrics,
                             specialist_url=args.specialist_url)
        print(json.dumps(result, indent=2))
        return 0
    except (PermissionError, LookupError, ValueError, InvalidModelOutput) as exc:
        print(json.dumps({"status": "error", "code": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
