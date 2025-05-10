from fastapi.testclient import TestClient
from main import app
from datetime import datetime
from memory_store import get_issue

client = TestClient(app)

# Validate issue creation and retrieval
def test_create_and_get_issue():
    payload = {
        "id": "issue-001",
        "title": "Test Retry Logic",
        "description": "Test description",
        "author": "test@example.com",
        "createdAt": datetime.utcnow().isoformat()
    }
    res = client.post("/events", json=payload)
    assert res.status_code == 200

    res = client.get("/issues/issue-001")
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Test Retry Logic"
    assert data["author"] == "test@example.com"

# Validate integration with LLM analysis + planning
def test_analyze_and_plan():
    issue_id = "issue-002"
    client.post("/events", json={
        "id": issue_id,
        "title": "Analyze Plan",
        "description": "Check integration",
        "author": "dev@example.com",
        "createdAt": datetime.utcnow().isoformat()
    })

    res = client.post(f"/analyze/{issue_id}")
    assert res.status_code == 200
    assert "labels" in res.json()

    res = client.post(f"/plan/{issue_id}")
    assert res.status_code == 200
    assert "plan" in res.json()

# Validate 404 for unknown issue
def test_invalid_issue_id():
    res = client.get("/issues/nonexistent")
    assert res.status_code == 404

    res = client.post("/analyze/nonexistent")
    assert res.status_code == 404

    res = client.post("/plan/nonexistent")
    assert res.status_code == 404

# Validate search filtering
def test_search_issues():
    client.post("/events", json={
        "id": "issue-search-1",
        "title": "Add search support",
        "description": "This issue is for testing search.",
        "author": "bob@example.com",
        "createdAt": datetime.utcnow().isoformat()
    })

    res = client.get("/issues?search=search")
    assert res.status_code == 200
    results = res.json()
    assert any("search" in issue["title"].lower() for issue in results)

# Validate that archived issues are excluded by default
def test_archived_issue_exclusion():
    client.post("/events", json={
        "id": "issue-archive-1",
        "title": "Old bug",
        "description": "Should be archived",
        "author": "archiver@example.com",
        "createdAt": "2000-01-01T00:00:00Z"
    })

    issue = get_issue("issue-archive-1")
    issue.is_archived = True  # simulate archive manually

    res = client.get("/issues")
    assert res.status_code == 200
    issues = res.json()
    assert all(issue["id"] != "issue-archive-1" for issue in issues)
