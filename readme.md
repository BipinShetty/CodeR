# 🐇 Agentic Issue Planner

A modular, type-safe, event-driven backend system simulating intelligent issue triage and planning using a mock LLM client.

Built in **FastAPI (Python)** with a focus on clear architecture, strong typing, composability, observability, and extensibility — aligned with the CodeRabbit specification and real-world engineering principles.

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

## ⚙️ Setup Instructions

### Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

### Run the server

```bash
uvicorn main:app --reload
```

Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Example Payload

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

Run all tests:

```bash
pytest tests/test_api.py
```

---

## 🧠 Design Decisions & Trade-Offs

This section outlines not just what choices were made, but also *why* they were made over other viable alternatives — reflecting judgment under time constraints and practical engineering trade-offs.

This section outlines not just what choices were made, but also *why* they were made over other viable alternatives — to reflect thoughtful system design and real-world engineering trade-offs.

### 💃️ Why In-Memory DB?

**Decision**: Used a Python `dict`-based in-memory store for simplicity.

**Pros:**

* Simplifies development under time constraints (no external services required)
* Fast read/write performance for small workloads
* Avoids schema setup, migrations, or connection handling

**Cons:**

* Volatile — data is lost on restart
* Unsuitable for multi-instance deployments or distributed coordination

**Alternatives Considered:**

* **SQLite/PostgreSQL**: Persistent but needs schema management and connections
* **Redis**: Good for ephemeral state but adds infra and orchestration complexity

**Scaling Strategy:**

* Replace with a distributed database (e.g., PostgreSQL, DynamoDB, or Cassandra)
* Shard across tenants or issue categories if dataset grows large
* Add distributed locking or row-level versioning for consistency
* Replace with **PostgreSQL** (if schema/querying is primary) or **Redis** (if TTL/cache-first)
* Run on cloud (e.g., AWS RDS / Elasticache)

---

### 🔄 Why Retry & Timeout Logic?

**LLM calls are I/O-bound and error-prone**, especially if later replaced with real HTTP/gRPC models. The retry layer improves robustness.

**Strategy**:

* Retry on transient exceptions (e.g., timeouts)
* Clear logs on success/failure

---

### ⏳ Why Background Cleanup?

Used for **auto-archiving old issues(30+ days)** (simulating TTL on stale data like abandoned tasks or outdated events).

**Implementation**: `asyncio.create_task` with periodic purging of issues older than a threshold.

**Why not use Celery or distributed task queues initially?**
For the prototype, I chose `asyncio` due to its lightweight setup and minimal infra requirements. It avoids additional brokers or services (e.g., Redis) and keeps the system easy to run and review. In production, this would be replaced by:

**Scaling**:

* A **Celery beat job** (with Redis or RabbitMQ backend)
* A **serverless function** on a timer (e.g., Azure Functions)
* A **cronjob** in Kubernetes or ECS Scheduled Tasks

---

## 🌐 Extensibility & Real-World Readiness

| Component   | Designed For                      |
| ----------- | --------------------------------- |
| LLMClient   | Easily swappable (via interface)  |
| Models      | Strong typing via `pydantic`      |
| Endpoints   | RESTful, documented, testable     |
| Storage     | Abstracted, can support real DB   |
| Retry Layer | Pluggable, resilient, centralized |

---

## 🔍 Improvements with More Time

If given more time, I would:

* Add persistent DB + ORM (e.g., PostgreSQL + SQLAlchemy)
* Deploy via Docker & Helm on Kubernetes
* Add proper async test coverage with mock injection
* Separate business logic from transport layer (Hex architecture)
* Add Prometheus-compatible metrics and tracing

---

## 🧭 Architectural Overview

```
                  +---------------------+
                  |  /events (FastAPI)  |
                  +----------+----------+
                             |
                       Normalizer
                             |
            +------------------------------+
            |   IssueService (Core Logic)  |
            +--------+----------+---------+
                     |          |
          +----------+          +--------------+
          |                                |
    In-MemoryStore                  LLMClientAdapter (mock)
    (can be swapped)               (can inject real client)
```

---

