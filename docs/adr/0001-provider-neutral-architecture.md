# ADR 0001: Provider-Neutral Architecture

## Status

Accepted

## Context

The software factory needs to interact with LLMs, cloud platforms, and execution environments. Directly coupling orchestration code to vendor SDKs would make testing, migration, and multi-cloud deployment unnecessarily difficult.

## Decision

External capabilities are represented through explicit provider interfaces. Vendor-specific implementations will live behind those interfaces.

The initial contracts are:

- `LLMProvider`
- `CloudProvider`
- `ExecutionProvider`

The domain and orchestration layers must not import provider SDKs directly.

## Consequences

### Positive

- Providers can be replaced independently.
- Unit tests can use deterministic fakes.
- Vendor migrations require adapter changes rather than domain rewrites.
- Multi-cloud support becomes an architectural capability rather than duplicated business logic.

### Trade-offs

- Interfaces must be designed carefully.
- Provider-specific capabilities may require optional capability models.
- Abstraction introduces another layer that must be documented and tested.

## Future Evolution

As real providers are implemented, the contracts will be expanded only when a capability is required by the factory rather than exposing every vendor-specific feature.
