import unittest
from mock_business_service import Principal, read_ticket

class TicketPolicyTests(unittest.TestCase):
    def test_authorized(self):
        self.assertEqual(
            read_ticket(Principal("u1", "A"), "T-100")["status"], "open"
        )

    def test_cross_tenant_denied(self):
        self.assertEqual(
            read_ticket(Principal("u1", "A"), "T-200")["result"],
            "not_available"
        )

    def test_unknown_not_invented(self):
        self.assertEqual(
            read_ticket(Principal("u1", "A"), "T-999")["result"],
            "not_available"
        )

if __name__ == "__main__":
    unittest.main()
