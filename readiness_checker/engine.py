from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Finding:
    control: str
    severity: str
    passed: bool
    message: str
    recommendation: str = ""


def _finding(control: str, passed: bool, severity: str, message: str, recommendation: str = "") -> Finding:
    return Finding(control, severity, passed, message, recommendation)


def evaluate(environment: dict[str, Any]) -> tuple[int, list[Finding]]:
    """Evaluate an environment inventory and return its score and findings."""
    production = str(environment.get("type", "")).lower() == "production"
    findings = [
        _finding(
            "Audit logging",
            bool(environment.get("audit_enabled")),
            "critical" if production else "warning",
            "Dataverse audit logging is enabled.",
            "Enable auditing at the environment and required table levels.",
        ),
        _finding(
            "DLP policy",
            bool(environment.get("dlp_policy")),
            "critical" if production else "warning",
            "A Data Loss Prevention policy is assigned.",
            "Assign an approved DLP policy before release.",
        ),
        _finding(
            "Backups",
            bool(environment.get("backup_enabled")),
            "critical" if production else "warning",
            "Environment backups are enabled.",
            "Enable backups and document restore testing.",
        ),
    ]

    solutions = environment.get("solutions", [])
    unmanaged = [item.get("name", "Unnamed solution") for item in solutions if not item.get("managed")]
    findings.append(
        _finding(
            "Managed solutions",
            not production or not unmanaged,
            "critical",
            "All production solutions are managed.",
            f"Replace unmanaged production solutions: {', '.join(unmanaged)}.",
        )
    )

    flows = environment.get("flows", [])
    personal_flows = [item.get("name", "Unnamed flow") for item in flows if item.get("owner_type") != "service_account"]
    findings.append(
        _finding(
            "Flow ownership",
            not personal_flows,
            "warning",
            "Automated flows use service-account ownership.",
            f"Move these flows to a service account: {', '.join(personal_flows)}.",
        )
    )

    references = environment.get("connection_references", [])
    missing_references = [item.get("name", "Unnamed reference") for item in references if not item.get("configured")]
    findings.append(
        _finding(
            "Connection references",
            not missing_references,
            "critical",
            "All connection references are configured.",
            f"Configure connection references: {', '.join(missing_references)}.",
        )
    )

    variables = environment.get("environment_variables", [])
    missing_variables = [item.get("name", "Unnamed variable") for item in variables if not item.get("has_current_value")]
    findings.append(
        _finding(
            "Environment variables",
            not missing_variables,
            "critical",
            "All environment variables have current values.",
            f"Set current values for: {', '.join(missing_variables)}.",
        )
    )

    findings.extend(
        [
            _finding(
                "Environment isolation",
                not production or bool(environment.get("dedicated_production")),
                "warning",
                "Production workloads use a dedicated environment.",
                "Move production workloads to a dedicated production environment.",
            ),
            _finding(
                "Owner documented",
                bool(environment.get("business_owner")),
                "warning",
                "A business owner is documented.",
                "Record an accountable business owner.",
            ),
        ]
    )

    weights = {"critical": 15, "warning": 5}
    deductions = sum(weights[item.severity] for item in findings if not item.passed)
    return max(0, 100 - deductions), findings
