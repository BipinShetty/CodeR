from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Comment model to track threaded discussion of an issue
class IssueComment(BaseModel):
    author: str
    comment: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Core issue model to track issue details and LLM responses
class Issue(BaseModel):
    id: str
    title: str
    description: str
    author: str
    createdAt: datetime
    labels: List[str] = []
    assignedTo: Optional[str] = None
    confidence: Optional[float] = None
    priority: Optional[str] = None
    comments: List[IssueComment] = []
    plan: Optional[str] = None
    is_archived: bool = False