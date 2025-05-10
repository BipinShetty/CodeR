# Agentic Issue Planner

This is a modular, event-driven backend system designed to simulate intelligent issue triage and planning using a mock LLM client. Built with FastAPI and Python, the service demonstrates strong typing, clear architecture, robust logging, and extensibility — all aligned with the CodeRabbit take-home specification.

---

## 🏋️ Features

* Accept new issues via `POST /events`
* List all issues: `GET /issues`
* Retrieve specific issue: `GET /issues/:id`
* Trigger LLM-based analysis: `POST /analyze/:id`
* Trigger LLM-based plan generation: `POST /plan/:id`
* Background job for archiving old issues
* Simple search/filtering by title or description
* In-memory storage (can be extended)
* Retry and timeout logic for LLM calls
* Test coverage for main flows

---

## 🔧 Setup Instructions

### 1. Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

### 2. Run the server

```bash
uvicorn main:app --reload
```

The interactive Swagger UI will be available at:

```
http://localhost:8000/docs
```

---

## 📋 Sample Issue Payload

```json
{
  "id": "issue-123",
  "title": "Add retry logic to HTTP client",
  "description": "Requests to external APIs sometimes fail. We need to add automatic retries.",
  "author": "alice@example.com",
  "createdAt": "2024-04-01T10:15:00Z"
}
```

---

## ✅ Testing

Run the tests using:

```bash
pytest tests/test_api.py
```

You can also test endpoints using Postman or directly via Swagger UI.

---

