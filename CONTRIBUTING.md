# Contributing to CloudProj

CloudProj is being developed as a modular AI software-engineering platform. Contributions should preserve the separation between the core workflow and external providers.

## Development Rules

1. Keep provider-specific SDK imports inside provider adapters.
2. Prefer typed Pydantic/domain contracts over unstructured dictionaries at service boundaries.
3. Add tests for new provider behavior and workflow logic.
4. Do not commit API keys, cloud credentials, generated secrets, or `.env` files.
5. Keep changes focused and document architectural decisions when they affect public interfaces.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
ruff check .
```

## Pull Requests

A useful pull request should explain:

- what changed;
- why the change is needed;
- how it was tested;
- any architectural trade-offs;
- any follow-up work required.
