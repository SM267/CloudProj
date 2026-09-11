# Security Policy

CloudProj is intended to become a system capable of processing and executing AI-generated software. Security is therefore a first-class design concern.

## Reporting a Vulnerability

Please do not publicly disclose a suspected vulnerability before it has been investigated. Open a private security report through GitHub's supported security-reporting mechanism when available.

## Security Principles

- Never commit credentials or secrets.
- Treat AI-generated code as untrusted input.
- Do not execute generated code directly on the host in production.
- Enforce isolation and resource limits for execution backends.
- Validate generated artifacts before deployment.
- Keep cloud-provider credentials outside generated application code.
