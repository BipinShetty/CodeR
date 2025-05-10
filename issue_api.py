from fastapi import APIRouter, HTTPException, Query
from models import Issue
from  memory_store import save_issue, get_issue, get_all_issues, search_issues
from llm_clients.mock import MockLLMClient
import logging, asyncio

router = APIRouter()
# Can be replaced with a real client
llm_client = MockLLMClient()

# Receive issue events from external systems
@router.post("/events")
def receive_event(issue: Issue):
    logging.info(f"Received issue: {issue.id}")
    save_issue(issue)
    return {"status": "received"}

# List all issues, with optional text search
@router.get("/issues")
def list_issues(search: str = Query(None)):
    return search_issues(search) if search else get_all_issues(active_only=True)

# Retrieve specific isue details
@router.get("/issues/{issue_id}")
def issue_detail(issue_id: str):
    issue = get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

# Trigger LLM analysis with retry and timeout
@router.post("/analyze/{issue_id}")
async def analyze(issue_id: str):
    # Retrieve the issue from the in-memory store
    issue = get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Retry logic: attempt LLM analysis up to 3 times with timeout
    for attempt in range(3):
        try:
            # Call the mock LLM client with a timeout to simulate real-world latency
            result = await asyncio.wait_for(llm_client.analyze_issue(issue), timeout=3.0)

            # Update issue fields with LLM response
            issue.labels = result["labels"]
            issue.assignedTo = result["assignedTo"]
            issue.confidence = result["confidence"]
            issue.priority = result.get("priority")

            # Save updated issue back to store
            save_issue(issue)
            return result
        except asyncio.TimeoutError:
            # Log timeout event with retry count
            logging.warning(f"Analyze timeout for issue {issue_id}, attempt {attempt+1}")

    # Raise error if all retries fail
    raise HTTPException(status_code=500, detail="LLM analyze failed after retries")
    issue = get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    for attempt in range(3):
        try:
            result = await asyncio.wait_for(llm_client.analyze_issue(issue), timeout=3.0)
            issue.labels = result["labels"]
            issue.assignedTo = result["assignedTo"]
            issue.confidence = result["confidence"]
            issue.priority = result.get("priority")
            save_issue(issue)
            return result
        except asyncio.TimeoutError:
            logging.warning(f"Analyze timeout for issue {issue_id}, attempt {attempt+1}")
    raise HTTPException(status_code=500, detail="LLM analyze failed after retries")
# Trigger LLM plan generation with retry and timeout
@router.post("/plan/{issue_id}")
async def plan(issue_id: str):
    # Retrieve the issue from the in-memory store
    issue = get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Retry logic: attempt LLM plan generation up to 3 times
    for attempt in range(3):
        try:
            # Simulate latency and failure using mock LLMClient with timeout
            result = await asyncio.wait_for(llm_client.plan_issue(issue), timeout=3.0)

            # Store the generated plan in the issue
            issue.plan = result["plan"]
            save_issue(issue)
            return result
        except asyncio.TimeoutError:
            # Log timeout per retry to help with debugging
            logging.warning(f"Plan timeout for issue {issue_id}, attempt {attempt+1}")

    # Final failure after retries
    raise HTTPException(status_code=500, detail="LLM plan failed after retries")
    issue = get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    for attempt in range(3):
        try:
            result = await asyncio.wait_for(llm_client.plan_issue(issue), timeout=3.0)
            issue.plan = result["plan"]
            save_issue(issue)
            return result
        except asyncio.TimeoutError:
            logging.warning(f"Plan timeout for issue {issue_id}, attempt {attempt+1}")
    raise HTTPException(status_code=500, detail="LLM plan failed after retries")

# Trigger LLM analysis with retry and timeout
@router.post("/analyze/{issue_id}")
async def analyze(issue_id: str):
    # Retrieve the issue from the in-memory store
    issue = get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Retry logic: attempt LLM analysis up to 3 times with timeout
    for attempt in range(3):
        try:
            # Call the mock LLM client with a timeout to simulate real-world latency
            result = await asyncio.wait_for(llm_client.analyze_issue(issue), timeout=3.0)

            # Update issue fields with LLM response
            issue.labels = result["labels"]
            issue.assignedTo = result["assignedTo"]
            issue.confidence = result["confidence"]
            issue.priority = result.get("priority")

            # Save updated issue back to store
            save_issue(issue)
            return result
        except asyncio.TimeoutError:
            # Log timeout event with retry count
            logging.warning(f"Analyze timeout for issue {issue_id}, attempt {attempt+1}")

    # Raise error if all retries fail
    raise HTTPException(status_code=500, detail="LLM analyze failed after retries")
    issue = get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    for attempt in range(3):
        try:
            result = await asyncio.wait_for(llm_client.analyze_issue(issue), timeout=3.0)
            issue.labels = result["labels"]
            issue.assignedTo = result["assignedTo"]
            issue.confidence = result["confidence"]
            issue.priority = result.get("priority")
            save_issue(issue)
            return result
        except asyncio.TimeoutError:
            logging.warning(f"Analyze timeout for issue {issue_id}, attempt {attempt+1}")
    raise HTTPException(status_code=500, detail="LLM analyze failed after retries")