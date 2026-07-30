from datetime import datetime, timezone

from .engine import Finding


def render_report(environment_name: str, score: int, findings: list[Finding]) -> str:
    status = "READY" if score >= 80 and not any(not f.passed and f.severity == "critical" for f in findings) else "ACTION REQUIRED"
    rows = []
    actions = []
    for finding in findings:
        result = "PASS" if finding.passed else finding.severity.upper()
        rows.append(f"| {finding.control} | {result} | {finding.message if finding.passed else finding.recommendation} |")
        if not finding.passed:
            actions.append(f"- **{finding.control} ({finding.severity.upper()})**: {finding.recommendation}")

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return "\n".join(
        [
            f"# Power Platform Readiness Report: {environment_name}",
            "",
            f"**Status:** {status}  ",
            f"**Score:** {score}/100  ",
            f"**Generated:** {generated}",
            "",
            "## Control results",
            "",
            "| Control | Result | Detail |",
            "|---|---|---|",
            *rows,
            "",
            "## Recommended actions",
            "",
            *(actions or ["- No remediation is required."]),
            "",
        ]
    )
