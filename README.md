# CloudProj — Cloud-Agnostic AI Software Factory

CloudProj is a provider-neutral AI software development factory that turns a natural-language software requirement into a structured engineering workflow: requirements, architecture, implementation tasks, generated code, tests, review, and deployment metadata.

The project deliberately separates **application workflow** from **AI model providers**, **cloud providers**, and **execution backends** so that the factory is not coupled to one vendor.

## Vision

```text
Developer requirement
        |
        v
+-------------------+
| AI Orchestrator   |
+---------+---------+
          |
    +-----+-----+-------------------+
    |           |                   |
 Planner    Architect           Reviewer
    |           |                   |
    +-----------+-------------------+
                |
                v
          Code + Tests
                |
                v
         Validation/Sandbox
                |
                v
       Provider-neutral artifact
                |
       +--------+--------+
       |        |        |
      AWS      GCP     Azure
```

## Current status

**Phase 1 — Foundation** is implemented:

- FastAPI service with health and API metadata endpoints.
- Provider abstraction for LLMs, cloud deployment, and code execution.
- Configuration through environment variables using Pydantic Settings.
- Initial orchestration domain model and deterministic stub LLM provider.
- Pytest test suite for health, provider contracts, and orchestration.
- Dockerfile and Docker Compose for local development.
- GitHub Actions CI for linting and tests.
- Architecture and development documentation.

The AI integrations and real deployment backends are intentionally introduced behind interfaces in later phases.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the component model and provider-neutral design.

## Roadmap

See [docs/roadmap.md](docs/roadmap.md) for the phased implementation plan.

## Quick start

### Local Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the OpenAPI UI.

### Docker

```bash
docker compose up --build
```

## API examples

Health:

```bash
curl http://127.0.0.1:8000/health
```

Create an initial software-factory plan:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/factory/plan \
  -H 'Content-Type: application/json' \
  -d '{
    "requirement": "Build a task management REST API with authentication and PostgreSQL",
    "language": "python",
    "framework": "fastapi"
  }'
```

## Repository layout

```text
CloudProj/
├── app/
│   ├── api/
│   ├── core/
│   ├── domain/
│   ├── providers/
│   ├── services/
│   └── main.py
├── docs/
├── tests/
├── .github/workflows/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Design principles

1. **Provider-neutral interfaces first.** Vendor-specific SDKs live behind adapters.
2. **Structured outputs.** Domain objects define stable contracts between workflow stages.
3. **Deterministic orchestration.** The workflow engine remains testable without requiring an external model.
4. **Secure execution.** Generated code is never treated as trusted input; sandboxing is a planned deployment requirement.
5. **Observable workflows.** Each stage will expose status, inputs, outputs, latency, and failure information.

## License

MIT. See [LICENSE](LICENSE).
