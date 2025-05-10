from typing import Dict
from models import Issue

# In-memory key-value store simulating persistent DB
issue_store: Dict[str, Issue] = {}

# Save or update issue
def save_issue(issue: Issue):
    issue_store[issue.id] = issue

# Retrieve issue by ID
def get_issue(issue_id: str) -> Issue:
    return issue_store.get(issue_id)

# List all active or all issues
def get_all_issues(active_only: bool = False):
    return [i for i in issue_store.values() if not i.is_archived] if active_only else list(issue_store.values())

# Search issues by title/description
def search_issues(query: str):
    return [i for i in issue_store.values() if query.lower() in i.title.lower() or query.lower() in i.description.lower()]

# Archive issues older than a threshold e.g default is 30 days
def archive_old_issues(threshold_days: int = 30):
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=threshold_days)
    for issue in issue_store.values():
        if issue.createdAt < cutoff:
            issue.is_archived = True