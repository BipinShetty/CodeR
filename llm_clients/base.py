from abc import ABC, abstractmethod
from models import Issue

# Abstract base class to allow plug in  LLM clients (mock/real)
class BaseLLMClient(ABC):
    @abstractmethod
    async def analyze_issue(self, issue: Issue):
        pass

    @abstractmethod
    async def plan_issue(self, issue: Issue):
        pass