# Architecture

## Goal

CloudProj separates orchestration logic from infrastructure and AI vendors. The core domain depends on stable interfaces; adapters depend on external SDKs.

## Layers

```text
HTTP/API
   |
Application Services
   |
Domain Models + Provider Contracts
   |
Adapters
   +-- LLM: OpenAI / Gemini / Ollama
   +-- Cloud: AWS / GCP / Azure
   +-- Execution: Docker / Kubernetes
```

## AI workflow

The first production workflow will be a staged pipeline:

1. Requirements analysis — normalize goals, constraints, inputs, and acceptance criteria.
2. Architecture — produce a technology-neutral component model and API/data contracts.
3. Planning — decompose the architecture into implementation tasks.
4. Code generation — generate repository artifacts from the accepted plan.
5. Test generation — generate unit, integration, and contract tests.
6. Validation — build and run tests in an isolated execution environment.
7. Review — inspect correctness, security, maintainability, and policy constraints.

Stages should exchange typed, versionable objects rather than unstructured strings wherever practical.

## Provider abstraction

### LLMProvider

`LLMProvider.generate()` is the minimum common interface. Concrete adapters should own authentication, SDK quirks, retry policies, request formatting, and provider-specific telemetry.

### CloudProvider

`CloudProvider.deploy()` should receive a provider-neutral deployment request and return a normalized result. Cloud-specific resource creation belongs in adapters or IaC modules, not in orchestration code.

### ExecutionProvider

Generated artifacts are untrusted input. Execution must happen in an isolated environment with explicit resource limits, a timeout, restricted networking, and a disposable filesystem.

## Non-functional requirements

- **Portability:** changing a provider should not require changing domain or workflow code.
- **Testability:** core workflow tests must run with deterministic local providers.
- **Security:** secrets never enter generated source control artifacts.
- **Observability:** every stage gets a correlation/job ID and structured event lifecycle.
- **Reproducibility:** plans, prompts, model metadata, and generated artifacts should be versioned or content-addressed where appropriate.
- **Idempotency:** retrying a workflow stage should not create duplicate external resources without an explicit operation key.
