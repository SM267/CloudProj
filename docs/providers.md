# LLM Provider Setup

CloudProj keeps LLM selection outside the application core. Set the provider with `CLOUDPROJ_DEFAULT_LLM_PROVIDER` or override it per planning request with `llm_provider`.

## Stub

Best for CI and development without network access:

```dotenv
CLOUDPROJ_DEFAULT_LLM_PROVIDER=stub
```

No credentials are required.

## OpenAI

```dotenv
CLOUDPROJ_DEFAULT_LLM_PROVIDER=openai
CLOUDPROJ_OPENAI_API_KEY=your-key
CLOUDPROJ_OPENAI_MODEL=gpt-4o-mini
```

Never commit `.env` or an API key. The adapter sends only the requested chat messages and model configuration.

## Gemini

```dotenv
CLOUDPROJ_DEFAULT_LLM_PROVIDER=gemini
CLOUDPROJ_GEMINI_API_KEY=your-key
CLOUDPROJ_GEMINI_MODEL=gemini-2.5-flash
```

The adapter converts CloudProj chat messages into the Gemini REST request format and normalizes the generated text back to the common provider contract.

## Ollama

Start Ollama locally and make a model available, then configure:

```dotenv
CLOUDPROJ_DEFAULT_LLM_PROVIDER=ollama
CLOUDPROJ_OLLAMA_BASE_URL=http://localhost:11434
CLOUDPROJ_OLLAMA_MODEL=llama3.2
```

No cloud credential is required.

## Per-request selection

The API also accepts a provider override:

```json
{
  "requirement": "Build a URL shortener API",
  "language": "python",
  "framework": "fastapi",
  "llm_provider": "ollama"
}
```

## Reliability

Remote adapters share:

- `CLOUDPROJ_LLM_TIMEOUT_SECONDS` — request timeout, default 30 seconds.
- `CLOUDPROJ_LLM_MAX_RETRIES` — retry count, default 2.
- exponential backoff between retries.
- normalized provider errors that do not expose upstream response bodies.

CI uses the stub provider and never requires live API credentials.
