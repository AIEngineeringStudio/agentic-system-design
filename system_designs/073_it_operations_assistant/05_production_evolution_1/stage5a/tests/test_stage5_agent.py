"""Software tests of the Stage 5A authorization and tool-dispatch boundary."""
import unittest
from auth import simulated_identity
from stage5_agent import ToolRequest, ScriptedProvider, RejectedToolRequest, investigate_with_model
from investigator import InvalidModelOutput


class BadCitations(ScriptedProvider):
    def analyze(self, question, evidence):
        return {
            "observations": [{"text": "False evidence", "evidence_ids": ["FAKE-ID"]}],
            "hypothesis": None,
            "next_step": "Check logs",
        }


class Stage5AgentTests(unittest.TestCase):
    def setUp(self):
        self.operator = simulated_identity("operator-5")

    def run_case(self, provider=None, **kwargs):
        return investigate_with_model(
            self.operator, "INC-42", "Why is the service slow?", provider, **kwargs
        )

    def test_happy_path(self):
        result = self.run_case()
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["evidence_ids"], ["METRIC-07", "CHANGE-03"])
        self.assertFalse(result["action_executed"])

    def test_unknown_write_tool_rejected(self):
        with self.assertRaises(RejectedToolRequest):
            self.run_case(ScriptedProvider([ToolRequest("restart_service", {}, "c1")]))

    def test_model_supplied_service_rejected(self):
        with self.assertRaises(RejectedToolRequest):
            self.run_case(ScriptedProvider([ToolRequest("get_metrics", {"service": "payroll-api"}, "c1")]))

    def test_excessive_tool_calls_rejected(self):
        with self.assertRaises(RejectedToolRequest):
            self.run_case(ScriptedProvider([
                ToolRequest("get_metrics", {}, "c1"),
                ToolRequest("get_deployments", {}, "c2"),
                ToolRequest("get_metrics", {}, "c3"),
            ]))

    def test_duplicate_calls_rejected(self):
        with self.assertRaises(RejectedToolRequest):
            self.run_case(ScriptedProvider([
                ToolRequest("get_metrics", {}, "c1"),
                ToolRequest("get_metrics", {}, "c2"),
            ]))

    def test_no_tools_is_insufficient_evidence(self):
        result = self.run_case(ScriptedProvider([]))
        self.assertEqual(result["status"], "insufficient_evidence")
        self.assertCountEqual(result["missing_evidence"], ["metrics", "deployments"])
        self.assertIsNone(result["hypothesis"])

    def test_missing_metrics_is_not_root_cause(self):
        result = self.run_case(simulate_metrics_timeout=True)
        self.assertEqual(result["missing_evidence"], ["metrics"])
        self.assertIsNone(result["hypothesis"])

    def test_unauthorized_operator_rejected(self):
        with self.assertRaises(PermissionError):
            investigate_with_model(simulated_identity("operator-9"), "INC-42", "Why?", ScriptedProvider())

    def test_cross_tenant_rejected(self):
        with self.assertRaises(PermissionError):
            investigate_with_model(simulated_identity("external-1"), "INC-42", "Why?", ScriptedProvider())

    def test_fake_citation_rejected(self):
        with self.assertRaises(InvalidModelOutput):
            self.run_case(BadCitations())

    def test_malformed_arg_type_rejected(self):
        with self.assertRaises(RejectedToolRequest):
            self.run_case(ScriptedProvider([ToolRequest("get_metrics", "{}", "c1")]))


if __name__ == "__main__":
    unittest.main()
