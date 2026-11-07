"""Software tests for the mock. These test the code, not the learner."""
import unittest
from auth import simulated_identity, authorized_incident
from investigator import InvalidModelOutput, MockAnalyst, investigate
from tools import get_metrics


class InventedCitationAnalyst:
    def analyze(self, evidence):
        return {
            "observations": [{"text": "Fabricated result", "evidence_ids": ["FAKE-999"]}],
            "hypothesis": None,
            "next_step": "Check logs",
        }


class InvestigationTests(unittest.TestCase):
    def setUp(self):
        self.operator = simulated_identity("operator-5")

    def test_happy_path(self):
        result = investigate(self.operator, "INC-42", "Why is it slow?")
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["evidence_ids"], ["METRIC-07", "CHANGE-03"])
        self.assertEqual(result["analysis_mode"], "deterministic_mock_not_llm")
        self.assertFalse(result["action_executed"])
        self.assertEqual(len(result["events"]), 4)

    def test_access_denied_different_service(self):
        with self.assertRaises(PermissionError):
            investigate(simulated_identity("operator-9"), "INC-42", "Check")

    def test_access_denied_other_tenant(self):
        with self.assertRaises(PermissionError):
            investigate(simulated_identity("external-1"), "INC-42", "Check")

    def test_tool_rechecks_authorization(self):
        with self.assertRaises(PermissionError):
            get_metrics(simulated_identity("operator-9"), "checkout-api", "company-A")

    def test_metrics_timeout_returns_partial(self):
        result = investigate(self.operator, "INC-42", "Check", simulate_metrics_timeout=True)
        self.assertEqual(result["status"], "insufficient_evidence")
        self.assertEqual(result["missing_evidence"], ["metrics"])
        self.assertIsNone(result["hypothesis"])
        self.assertFalse(result["action_executed"])

    def test_fake_citation_rejected(self):
        with self.assertRaises(InvalidModelOutput):
            investigate(self.operator, "INC-42", "Check", analyst=InventedCitationAnalyst())

    def test_unknown_incident(self):
        with self.assertRaises(LookupError):
            authorized_incident(self.operator, "INC-UNKNOWN")

    def test_empty_question_rejected(self):
        with self.assertRaises(ValueError):
            investigate(self.operator, "INC-42", "")


if __name__ == "__main__":
    unittest.main()
