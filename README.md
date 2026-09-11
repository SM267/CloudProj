# CloudProj — Cloud-Agnostic AI Software Factory

> **An AI-native software engineering platform that transforms natural-language requirements into structured architecture, implementation plans, tests, and deployment-ready artifacts through provider-neutral abstractions.**

[![CI](https://github.com/SM267/CloudProj/actions/workflows/ci.yml/badge.svg)](https://github.com/SM267/CloudProj/actions/workflows/ci.yml)

CloudProj is a production-oriented exploration of an **AI software factory**: instead of using an LLM as a simple code-completion tool, it models software development as a controlled engineering workflow.

A developer provides a requirement such as:

```text
Build a task management REST API with authentication,
PostgreSQL persistence, Docker support, and automated tests.
```

The factory is designed to transform that requirement through:

```text
Requirement
    ↓
Requirements Analysis
    ↓
Architecture
    ↓
Task Planning
    ↓
Code Generation
    ↓
Test Generation
    ↓
Automated Review
    ↓
Sandboxed Validation
    ↓
Deployment Artifact
```

## Why CloudProj?

AI development platforms can become tightly coupled to a particular LLM vendor, cloud provider, or execution environment. CloudProj treats those systems as **replaceable infrastructure** rather than business logic.

The core application depends on contracts such as:

```text
LLMProvider
 ├── OpenAI
 ├── Gemini
 └── Ollama

CloudProvider
 ├── AWS
 ├── GCP
 └── Azure

ExecutionProvider
 ├── Docker
 └── Kubernetes
```

This separation makes the architecture easier to test, extend, migrate, and operate across environments.

## Engineering Highlights

- **AI/LLM abstraction** — model vendors are isolated behind interfaces.
- **Cloud abstraction** — deployment capabilities are designed around provider-neutral contracts.
- **Workflow orchestration** — software development is represented as explicit stages and state transitions.
- **Structured domain models** — typed contracts reduce fragile string-to-string agent communication.
- **Testability** — the core workflow can run without live model credentials.
- **Containerization** — Docker-based development and deployment foundations.
- **CI/CD** — automated linting and tests through GitHub Actions.
- **Secure execution roadmap** — generated code is treated as untrusted and is planned to execute in an isolated sandbox.
- **Infrastructure as Code roadmap** — cloud deployment is intended to be represented through Terraform/Kubernetes rather than vendor-specific application logic.

## Architecture

```text
                    Developer
                        │
                        ▼
                 ┌─────────────┐
                 │  API Layer  │
                 └──────┬──────┘
                        │
                        ▼
              ┌───────────────────┐
              │  AI Orchestrator  │
              └─────────┬─────────┘
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
 Requirements       Architect         Planner
       │                │                │
       └────────────────┼────────────────┘
                        ▼
                 Code Generator
                        │
                        ▼
                 Test Generator
                        │
                        ▼
                  Code Reviewer
                        │
                        ▼
               Validation Sandbox
                        │
                        ▼
              Deployment Artifact
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
         AWS           GCP           Azure
```

The important architectural rule is that provider-specific SDKs belong in **adapter implementations**, not in the domain or orchestration layers.

## Technology Stack

### Backend

- Python 3.11+
- FastAPI
- Pydantic / Pydantic Settings
- SQLAlchemy (planned persistence layer)
- PostgreSQL (planned persistent storage)

### AI

- LLM provider interface
- OpenAI adapter — planned
- Gemini adapter — planned
- Ollama adapter — planned
- Structured model outputs
- Agent/workflow orchestration

### Infrastructure

- Docker
- Docker Compose
- Kubernetes — planned
- Terraform — planned
- AWS / GCP / Azure adapters — planned

### Developer Experience

- Pytest
- Ruff
- GitHub Actions
- OpenAPI

## Current Status

### Phase 1 — Foundation ✅

- FastAPI application
- Health and metadata endpoints
- Typed factory domain models
- LLM, cloud, and execution provider interfaces
- Deterministic stub LLM provider
- Initial software-factory orchestration service
- Unit/API tests
- Docker development environment
- GitHub Actions CI
- Architecture and roadmap documentation

### Phase 2 — Real AI Providers 🚧

- OpenAI adapter
- Gemini adapter
- Ollama adapter
- Provider configuration
- Structured model output contract
- Centralized retries/timeouts
- Evaluation tests

### Phase 3 — AI Software Factory 🚧

- Requirement analysis agent
- Architecture agent
- Task decomposition
- Repository-aware code generation
- Test generation
- Automated code review
- Human approval gates

### Phase 4 — Secure Execution

- Isolated Docker executor
- Resource limits
- Build/test execution
- Security scanning
- Artifact collection

### Phase 5 — Cloud Portability

- Kubernetes execution backend
- Terraform generation
- AWS adapter
- GCP adapter
- Azure adapter
- Environment-independent deployment manifests

### Phase 6 — Developer Dashboard

- React + TypeScript frontend
- Project management
- Live pipeline status
- Generated-code inspection
- Build/test results
- Provider selection
- Deployment management

## Example Target Output

For a generated application, CloudProj aims to produce a reproducible project such as:

```text
generated-project/
├── src/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── infrastructure/
│   ├── kubernetes/
│   └── terraform/
└── README.md
```

The generated application should pass automated validation before being marked successful.

## Design Principles

### 1. Provider Independence

Core business logic must not import or depend directly on a particular AI or cloud SDK.

### 2. Interface-Driven Architecture

External capabilities are represented through explicit contracts so implementations can be replaced independently.

### 3. Structured Communication

Workflow stages should exchange typed, validated objects rather than relying on unstructured text wherever possible.

### 4. Testability

The system must remain testable without requiring live cloud accounts or API credentials.

### 5. Secure-by-Design Execution

AI-generated code is untrusted input. Production execution will therefore require isolation, resource limits, and validation.

### 6. Reproducibility

Configuration, generated artifacts, and infrastructure definitions should be versionable and reproducible.

### 7. Observable Workflows

Each factory stage should eventually expose status, timing, inputs/outputs metadata, errors, and evaluation results.

## Quick Start

### Local Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive OpenAPI documentation.

### Docker

```bash
docker compose up --build
```

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Generate a Planning Artifact

```bash
curl -X POST http://127.0.0.1:8000/api/v1/factory/plan \
  -H 'Content-Type: application/json' \
  -d '{
    "requirement": "Build a task management REST API with authentication and PostgreSQL",
    "language": "python",
    "framework": "fastapi"
  }'
```

## Repository Structure

```text
CloudProj/
├── app/
│   ├── api/              # HTTP/API boundary
│   ├── core/             # Cross-cutting application concerns
│   ├── domain/           # Typed domain models
│   ├── providers/        # External provider contracts/adapters
│   ├── services/         # Factory orchestration
│   └── main.py           # FastAPI application entry point
├── docs/
│   ├── architecture.md
│   └── roadmap.md
├── tests/
├── .github/workflows/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Development Philosophy

CloudProj is intentionally being built in increments rather than presented as a fictional finished platform. The repository records the architecture, interfaces, tests, CI, and implementation milestones as the system evolves.

The long-term objective is to demonstrate how **LLMs, software architecture, cloud infrastructure, containers, testing, security, and CI/CD can be combined into a coherent engineering system**.

## Roadmap Issues

The GitHub issue tracker is used to turn the roadmap into concrete engineering milestones. The first tracked milestone is implementation of real LLM provider adapters while preserving the provider-neutral architecture.

## Author

**Shreyas Mahajan**  
Computer Science Engineering Student

Areas of interest: software engineering, AI/LLM systems, cloud computing, backend development, DSA, DevOps, and application development.

## License

MIT — see [LICENSE](LICENSE).
