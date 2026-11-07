"""Offline transport-mocked tests; these do NOT call an OpenAI model."""
import json
import unittest
from openai_provider import OpenAIProvider


class StubResponsesProvider(OpenAIProvider):
    def __init__(self, outputs):
        super().__init__(model="test-model", api_key="test-key")
        self.outputs = list(outputs)
        self.payloads = []

    def _post(self, payload):
        self.payloads.append(payload)
        return self.outputs.pop(0)


class ProviderAdapterTests(unittest.TestCase):
    def test_tool_call_output_is_interpreted(self):
        provider = StubResponsesProvider([{
            "status": "completed",
            "output": [
                {"type": "function_call", "name": "get_metrics",
                 "arguments": "{}", "call_id": "call-01"},
                {"type": "function_call", "name": "get_deployments",
                 "arguments": "{}", "call_id": "call-02"},
            ],
        }])
        actions = provider.propose("INC-42", "checkout-api", "Why slow?")
        self.assertEqual([a.name for a in actions], ["get_metrics", "get_deployments"])
        self.assertEqual(provider.payloads[0]["store"], False)
        self.assertEqual(len(provider.payloads[0]["tools"]), 2)

    def test_structured_output_is_parsed(self):
        example = {"observations": [{"text": "Slow", "evidence_ids": ["METRIC-07"]}],
                   "hypothesis": None, "next_step": "Inspect"}
        provider = StubResponsesProvider([{
            "status": "completed",
            "output": [{"type": "message", "content": [
                {"type": "output_text", "text": json.dumps(example)}]}],
        }])
        provider._proposed_calls = []  # No prior call for this isolated parsing test
        observed = provider.analyze("Why slow?", [{"evidence_id": "METRIC-07"}])
        self.assertEqual(observed, example)
        self.assertEqual(provider.payloads[0]["text"]["format"]["type"], "json_schema")

    def test_tool_outputs_keep_call_id(self):
        example = {"observations": [], "hypothesis": None, "next_step": "Inspect"}
        provider = StubResponsesProvider([
            {"status": "completed", "output": [{"type": "function_call",
                "name": "get_metrics", "arguments": "{}", "call_id": "c1"}]},
            {"status": "completed", "output": [{"type": "message", "content": [
                {"type": "output_text", "text": json.dumps(example)}]}]},
        ])
        provider.propose("INC-42", "checkout-api", "Why slow?")
        provider.analyze("Why slow?", [{"source": "monitoring", "evidence_id": "METRIC-07"}])
        second_request = provider.payloads[1]
        outputs = [item for item in second_request["input"]
                   if item.get("type") == "function_call_output"]
        self.assertEqual(outputs[0]["call_id"], "c1")
        self.assertIn("METRIC-07", outputs[0]["output"])
        self.assertEqual(second_request["tool_choice"], "none")

    def test_invalid_model_tool_arguments_rejected(self):
        provider = StubResponsesProvider([{"status": "completed", "output": [
            {"type": "function_call", "name": "get_metrics",
             "arguments": "not-json", "call_id": "x"}]}])
        with self.assertRaises(ValueError):
            provider.propose("INC-42", "checkout-api", "Why slow?")


if __name__ == "__main__":
    unittest.main()
