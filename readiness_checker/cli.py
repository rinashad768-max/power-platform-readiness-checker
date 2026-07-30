import argparse
import json
from pathlib import Path

from .engine import evaluate
from .report import render_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Power Platform environment release readiness.")
    parser.add_argument("inventory", type=Path, help="Path to the environment inventory JSON file.")
    parser.add_argument("--output", type=Path, default=Path("readiness-report.md"))
    parser.add_argument("--fail-on", choices=("critical", "warning"), default="critical")
    args = parser.parse_args()

    try:
        environment = json.loads(args.inventory.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        parser.error(str(error))

    score, findings = evaluate(environment)
    args.output.write_text(render_report(environment.get("name", "Unnamed environment"), score, findings), encoding="utf-8")

    counts = {
        severity: sum(1 for item in findings if not item.passed and item.severity == severity)
        for severity in ("critical", "warning")
    }
    passed = sum(1 for item in findings if item.passed)
    print(f"Environment: {environment.get('name', 'Unnamed environment')}")
    print(f"Readiness score: {score}/100")
    print(f"Critical: {counts['critical']} | Warning: {counts['warning']} | Passed: {passed}")
    print(f"Report: {args.output}")

    if args.fail_on == "warning" and (counts["critical"] or counts["warning"]):
        return 1
    return 2 if counts["critical"] else (1 if counts["warning"] else 0)
