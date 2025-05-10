from llm_clients.base import BaseLLMClient
from models import Issue
import asyncio, random

# Simple mock implementation for local testing
class MockLLMClient(BaseLLMClient):
    async def analyze_issue(self, issue: Issue):
        await asyncio.sleep(0.1)  # Simulate LLM response delay
        return {
            "labels": ["bug", "infra"],
            "assignedTo": "bob@example.com",
            "confidence": round(random.uniform(0.6, 0.95), 2),
            "priority": "high"
        }

    async def plan_issue(self, issue: Issue):
        await asyncio.sleep(0.1)
        return {
            "plan": (
                "[Simulated] Investigate root cause of the HTTP client failures, "
                "define a retry strategy (e.g., exponential backoff), "
                "implement retry logic in the client, "
                "write tests to validate behavior, "
                "and document assumptions and failure handling strategies."
            )
        }