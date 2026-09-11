# CloudProj — Cloud-Agnostic AI Software Factory

> **An AI-native software engineering platform that turns natural-language requirements into structured software plans through provider-neutral AI, execution, and deployment contracts.**

[![CI](https://github.com/SM267/CloudProj/actions/workflows/ci.yml/badge.svg)](https://github.com/SM267/CloudProj/actions/workflows/ci.yml)

CloudProj explores software development as a controlled, observable pipeline rather than a single LLM prompt. The long-term goal is to accept a requirement and produce validated architecture, implementation tasks, source code, tests, review findings, and deployment artifacts.

## Current MVP

The repository currently provides a production-minded **planning foundation**:

- FastAPI service with health, metadata, and planning endpoints.
- Typed Pydantic domain contracts for factory stages and plans.
- Provider-neutral `LLMProvider` abstraction.
- Working HTTP adapters for **OpenAI, Gemini, and Ollama**.
- Deterministic stub provider for offline development and tests.
- Centralized timeout/retry behavior for remote LLM calls.
- Provider selection through configuration or an API request.
- Non-destructive Docker deployment planning contract.
- Ruff + Pytest + GitHub Actions CI.
- Architecture, provider setup, security, contribution, evaluation, and ADR documentation.

The generated-code and cloud-deployment stages are intentionally marked as roadmap work; the project does **not** claim those capabilities are implemented yet.

## Product Vision

```text
Natural-language requirement
            │
            ▼
   Requirements Analysis
            │
            ▼
       Architecture
            │
            ▼
      Task Planning
            │
            ▼
      Code Generation
            │
            ▼
       Test Generation
            │
            ▼
    Automated Review
            │
            ▼
  Sandboxed Validation
            │
            ▼
   Deployment Artifacts
```

Each stage will consume and produce versioned, typed artifacts. Stage status, errors, timing, and artifact references are part of the domain model so the workflow can eventually be observed and resumed safely.

## Provider-Neutral Architecture

CloudProj treats external vendors as replaceable adapters:

```text
                    Application Core
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
         LLMProvider  CloudProvider  ExecutionProvider
              │           │           │
        ┌─────┼─────┐  future       future
        ▼     ▼     ▼  adapters     adapters
     OpenAI Gemini Ollama
```

**Rule:** provider-specific SDKs, URLs, credentials, and wire formats stay inside adapter modules. Domain models and orchestration services depend only on provider contracts.

## API

### Health

```http
GET /health
```

### Metadata

```http
GET /api/v1/meta
```

### Create a plan

```http
POST /api/v1/factory/plan
Content-Type: application/json

{
  "requirement": "Build a task management REST API with authentication and PostgreSQL",
  "language": "python",
  "framework": "fastapi",
  "llm_provider": "stub"
}
```

`llm_provider` is optional. When omitted, `CLOUDPROJ_DEFAULT_LLM_PROVIDER` is used.

## LLM Providers

| Provider | Status | Configuration |
|---|---|---|
| Stub | Ready | Default; no credentials |
| OpenAI | Ready | `CLOUDPROJ_OPENAI_API_KEY` |
| Gemini | Ready | `CLOUDPROJ_GEMINI_API_KEY` |
| Ollama | Ready | Local HTTP endpoint |

Remote adapters use a shared timeout/retry policy. Credentials are loaded through environment-backed settings and are never returned by the API.

See [`docs/providers.md`](docs/providers.md) for setup instructions.

## Technology Stack

- **Backend:** Python 3.11+, FastAPI, Pydantic, Pydantic Settings
- **HTTP:** HTTPX
- **Testing:** Pytest, pytest-asyncio
- **Quality:** Ruff, GitHub Actions
- **Containers:** Docker / Docker Compose
- **Future:** PostgreSQL, SQLAlchemy, Kubernetes, Terraform, React + TypeScript

## Quick Start

### 1. Clone

```bash
git clone https://github.com/SM267/CloudProj.git
cd CloudProj
```

### 2. Create an environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

### 3. Configure

```bash
cp .env.example .env
```

The default provider is `stub`, so no API key is required for local development.

### 4. Run

```bash
uvicorn app.main:app --reload
```

Open the generated OpenAPI documentation at `/docs`.

### 5. Verify quality

```bash
ruff check .
pytest
```

## Repository Structure

```text
CloudProj/
├── app/
│   ├── api/              # HTTP boundary
│   ├── domain/           # Provider-neutral models
│   ├── providers/        # External-system adapters/contracts
│   ├── services/         # Application orchestration
│   └── config.py         # Environment-backed settings
├── tests/                # Unit and API integration tests
├── docs/                 # Architecture, ADRs, evaluation, providers, roadmap
├── .github/workflows/    # CI
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Roadmap

### Phase 1 — Foundation ✅

Core FastAPI service, domain contracts, provider interfaces, stub provider, Docker foundation, tests, CI, and documentation.

### Phase 2 — Provider Layer ✅

OpenAI/Gemini/Ollama adapters, configuration, shared retries/timeouts, and provider-selection tests.

### Phase 3 — Multi-stage AI Factory 🚧

Requirements analysis, architecture generation, task decomposition, code generation, test generation, review, artifact versioning, and approval gates.

### Phase 4 — Secure Execution

Isolated execution, resource limits, build/test validation, artifact collection, and security scanning.

### Phase 5 — Cloud Portability

Kubernetes execution, Terraform generation, and AWS/GCP/Azure deployment adapters.

### Phase 6 — Developer Dashboard

React/TypeScript dashboard for projects, pipeline state, generated artifacts, test results, provider selection, and deployment operations.

## Engineering Principles

1. **Contracts before integrations.** External systems are behind explicit interfaces.
2. **Structured data over prompt chaining.** Pipeline boundaries use typed artifacts.
3. **Deterministic tests.** CI must not require paid model credentials.
4. **Secure by default.** Generated code is untrusted and must never execute directly on the host.
5. **Honest capability claims.** README and documentation distinguish implemented functionality from roadmap work.
6. **Observable workflows.** Stages should expose state, errors, timing, and artifact identity.

## Documentation

- `docs/architecture.md` — system boundaries and data flow
- `docs/providers.md` — LLM provider configuration
- `docs/adr/0001-provider-neutral-architecture.md` — architectural decision record
- `docs/evaluation.md` — evaluation methodology and quality gates
- `docs/roadmap.md` — implementation roadmap
- `CONTRIBUTING.md` — development workflow
- `SECURITY.md` — security reporting and design expectations

## Author

**Shreyas Mahajan** — Computer Science Engineering student interested in software engineering, AI/LLM systems, cloud computing, backend development, DSA, DevOps, and application development.

## License

MIT License. See `LICENSE`.
