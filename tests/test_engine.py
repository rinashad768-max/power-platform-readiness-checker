import unittest

from readiness_checker import evaluate


class ReadinessEngineTests(unittest.TestCase):
    def test_healthy_production_scores_100(self):
        environment = {
            "type": "production",
            "dedicated_production": True,
            "business_owner": "Operations",
            "audit_enabled": True,
            "dlp_policy": "Enterprise",
            "backup_enabled": True,
            "solutions": [{"name": "Core", "managed": True}],
            "flows": [{"name": "Notify", "owner_type": "service_account"}],
            "connection_references": [{"name": "dataverse", "configured": True}],
            "environment_variables": [{"name": "ApiUrl", "has_current_value": True}],
        }
        score, findings = evaluate(environment)
        self.assertEqual(100, score)
        self.assertTrue(all(item.passed for item in findings))

    def test_unmanaged_solution_is_critical_in_production(self):
        score, findings = evaluate(
            {
                "type": "production",
                "audit_enabled": True,
                "dlp_policy": "Enterprise",
                "backup_enabled": True,
                "solutions": [{"name": "Core", "managed": False}],
            }
        )
        result = next(item for item in findings if item.control == "Managed solutions")
        self.assertFalse(result.passed)
        self.assertEqual("critical", result.severity)
        self.assertLess(score, 100)


if __name__ == "__main__":
    unittest.main()
