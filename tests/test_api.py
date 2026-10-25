"""
tests/test_api.py — API Contract and Integration Tests for CI/CD Pipeline
"""

import sys
import unittest
from pathlib import Path

# Ensure repo root is on python path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient
from backend.main import app


class TestSupportMemoryCopilotAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        """Verify API health check endpoint returns 200 and healthy status."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertEqual(data.get("service"), "support-memory-copilot")

    def test_tickets_list_endpoint(self):
        """Verify /api/tickets returns list of ticket summaries matching TRS contract."""
        response = self.client.get("/api/tickets")
        self.assertEqual(response.status_code, 200)
        tickets = response.json()
        self.assertIsInstance(tickets, list)
        self.assertGreater(len(tickets), 0)
        
        first = tickets[0]
        self.assertIn("customer_id", first)
        self.assertIn("display_label", first)
        self.assertIn("risk_level", first)
        self.assertIn("last_message_preview", first)

    def test_customer_detail_endpoint(self):
        """Verify /api/tickets/cust_0001 returns customer details, risk profile, and frustration metrics."""
        response = self.client.get("/api/tickets/cust_0001")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("customer", data)
        self.assertEqual(data["customer"]["customer_id"], "cust_0001")
        self.assertIn("risk_profile", data)
        self.assertIn("frustration_trajectory", data)
        self.assertIn("action_recommendation", data)


if __name__ == "__main__":
    unittest.main()
