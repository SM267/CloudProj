# Architecture

## Purpose

CloudProj separates application workflow logic from external AI, cloud, and execution providers. The application core depends on stable contracts; provider modules own transport details, authentication, and vendor-specific response formats.

## Current layers

```text
HTTP/API
   │
   ▼
Application Service (SoftwareFactory)
   │
   ├── Domain Models
   │
   └── Provider Contracts
          │
          ├── LLMProvider
          │     ├── Stub
          │     ├── OpenAI
          │     ├── Gemini
          │     └── Ollama
          │
          ├── CloudProvider
          │     └── Docker planner (current)
          │
          └── ExecutionProvider
                └── contract only (current)
```

## Request flow

1. `PlanRequest` validates the HTTP payload.
2. The API selects an LLM through `build_llm_provider()`.
3. `SoftwareFactory` receives only the `LLMProvider` contract.
4. The service calls the provider and builds a typed `SoftwarePlan`.
5. FastAPI serializes the plan as JSON.
6. Provider failures are translated into a safe `502` response; credentials and upstream bodies are not exposed.

## LLM provider design

`LLMProvider.generate()` is the stable application-facing interface. `generate_json()` adds a provider-neutral JSON parsing contract.

Remote adapters share timeout and exponential-backoff retry behavior through `_HTTPProvider`. They are responsible for:

- authentication;
- provider-specific HTTP payloads;
- response parsing;
- provider-specific URLs/models;
- transport failures.

The domain and service layers must not import provider SDKs or depend on provider-specific response shapes.

## Factory pipeline

The intended staged workflow is:

1. **Requirements** — normalize goals, constraints, inputs, and acceptance criteria.
2. **Architecture** — produce component, API, and data contracts.
3. **Planning** — decompose the architecture into implementation tasks.
4. **Code generation** — produce versioned repository artifacts.
5. **Test generation** — produce executable tests.
6. **Review** — inspect correctness, security, maintainability, and policy constraints.
7. **Validation** — build and test generated code in an isolated executor.
8. **Deployment** — produce or apply provider-neutral deployment artifacts.

Only the initial planning foundation is implemented today. The remaining stages are explicit roadmap work.

## Security boundaries

Generated code is untrusted. When execution is implemented it must use a disposable sandbox with:

- strict CPU, memory, process, and wall-clock limits;
- restricted or disabled network access by default;
- a temporary filesystem with no host credentials;
- non-root execution;
- explicit artifact allowlists;
- complete cleanup after execution.

Secrets must come only from runtime configuration and must never be committed to generated projects or logs.

## Non-functional requirements

- **Portability:** provider changes must not require domain changes.
- **Testability:** CI runs without live model credentials.
- **Observability:** stages expose status, timing, errors, and artifact references.
- **Reproducibility:** inputs and generated artifacts should be versioned or content-addressed.
- **Idempotency:** external operations require an explicit operation key before they become destructive.
