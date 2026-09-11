# AI Software Factory Evaluation Plan

CloudProj will eventually evaluate generated software on more than whether an LLM returned syntactically valid code.

## Evaluation Dimensions

| Dimension | Example measurement |
|---|---|
| Build correctness | Build succeeds in isolated environment |
| Test correctness | Generated and existing tests pass |
| API correctness | Contract/integration tests pass |
| Code quality | Static analysis and maintainability checks |
| Security | Dependency and generated-code security scans |
| Reproducibility | Same specification produces compatible artifacts |
| Cost | Model tokens and infrastructure execution cost |
| Latency | End-to-end factory duration and per-stage duration |

## Evaluation Principles

- Keep evaluation datasets versioned.
- Separate generation from scoring.
- Record model/provider/version metadata.
- Use deterministic tests where possible.
- Never treat an LLM's self-assessment as the sole quality signal.

## Planned Benchmark

A future benchmark will contain representative software tasks covering CRUD APIs, authentication, persistence, asynchronous jobs, integrations, and deployment configuration. Each task will have explicit acceptance tests.
