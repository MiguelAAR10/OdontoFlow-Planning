# SANDBOX-REAL-MODEL-01 — Real LLM sandbox smoke — FOREMAN living brief

## Executive status

**BLOCKED — NEEDS_MODEL_PROVIDER.** At backend `main@22e2b51011a83fbf1e2c745aecda29b44265c71e`, the current runtime resolves to the OpenAI model `openai:gpt-5.4-mini`, but no `OPENAI_API_KEY` is configured. The existing Sales Agent endpoint also has no `SALES_AGENT_V0_CREDENTIAL`, so it cannot pass its server-side agent authentication gate. No provider request, product change, or production write was made.

## Objective and success criteria

Run the already-proven controlled loop with one real provider:

```text
sandbox inbound → canonical persistence → authenticated Sales Agent
  → typed tools → sandbox outbound → loopback receipt
```

The run would need to prove real model execution, authorized tool calls,
one sandbox outbound and receipt, tenant/auth isolation, zero appointments,
and fail-closed booking if free-text confirmation is attempted. Existing fake
model behavior and booking policy remain unchanged. WhatsApp, n8n, paid-model
provider changes, consent changes, IAM redesign, and production data are out
of scope.

## Repository reality

The verified base is the PASS commit from SANDBOX-INBOUND-01. The existing
Sales Agent configuration in `sales_agent/config.py` defaults to
`openai:gpt-5.4-mini`; `SALES_AGENT_MODEL` may override it, while
`SALES_AGENT_V0_CREDENTIAL` supplies the server-issued backend credential.
`SalesAgentRuntime._resolve_model()` calls LangChain's
`init_chat_model(self.settings.model)`, and `sales_agent/api.py` requires the
configured agent credential to exactly match the authenticated PostgreSQL
agent principal before invoking the runtime.

The locked optional dependency set contains `langchain-openai==1.6.1`,
`openai==3.10.0`, `langchain==1.4.0`, and `langgraph==1.2.11`. There is no
`langchain-google-genai` package or Gemini adapter in current `main`.
The ignored local configuration has a `GEMINI_API_KEY`, but no Gemini model
setting and no current adapter that can consume it. It therefore cannot be
treated as usable provider configuration.

The backend worktree retains unrelated pre-existing modifications and
untracked tooling/documentation paths. They were not changed. The previous
SANDBOX-INBOUND-01 sender, authenticated boundaries, sandbox consumer, and
fail-closed booking policy remain the only intended execution path.

## Authority and evidence used

This brief uses `AGENTS.md`, the SANDBOX-INBOUND-01 technical handoff, current
Sales Agent configuration/runtime/API code, `pyproject.toml` and `uv.lock`,
and the installed OdontoFlow engineering, security-hardening,
verification-before-completion, and Foreman-handoff skills. No historical
provider assumption was used; provider support was determined from current
code, lockfile, imports, and sanitized environment presence checks.

## What we will build and how

Nothing is authorized for implementation while the provider boundary is
missing. Once the existing OpenAI configuration is supplied, the intended run
is a disposable real-PostgreSQL smoke using the committed
`integrations/sandbox/sender.py`, authenticated `/sales-agent/turn`, typed
`BackendGateway`, existing `SandboxConsumer`, and loopback receiver. No second
runtime or provider will be added. A Gemini path would require a separate
approved provider/dependency contract and is not a defect repair for this
activity.

## Execution model

Solo FOREMAN. The run is a single coupled authenticated/database/provider
sequence; parallel execution would add no value and could contend for the
shared local PostgreSQL environment.

## Risks, conflicts, and protected surfaces

The main risk is mistaking a configured key for a supported provider or
reporting a provider HTTP response as business success. The OpenAI key and
agent service credential are both absent, so no request was attempted. No
secret value was printed or persisted. Protected paths, the sandbox transport,
IAM, and booking policy remain untouched.

## Evidence and validation

Credential-free preflight results:

```text
effective_model_provider=openai
effective_model=gpt-5.4-mini
sales_agent_backend_url_configured=True
sales_agent_backend_credential_configured=False
openai_api_key_configured=False
gemini_api_key_configured=True
langchain_openai_available=True
langchain_google_genai_available=False
```

The current environment and ignored local configuration were checked by name
only; secret values were not read into output. Installed versions and import
paths were verified without making a model call. No real-model test was run,
so this activity has no new database, tool, outbound, or receipt evidence.
The previous fake-model loop remains documented in the linked
SANDBOX-INBOUND-01 handoff.

## Decision and progress log

- 2026-09-16 — Verified base HEAD, dirty state, and the latest sandbox inbound
  handoff without repeating the reality audit.
- 2026-09-16 — Confirmed current `main` has one usable real-provider adapter:
  OpenAI via `langchain-openai`; the effective model is the OpenAI default.
- 2026-09-16 — Blocked before execution because `OPENAI_API_KEY` and
  `SALES_AGENT_V0_CREDENTIAL` are absent. The present `GEMINI_API_KEY` cannot
  be used by current `main` without adding an unapproved provider adapter.

## Next approval / next step

Supply a valid local `OPENAI_API_KEY` and a server-issued, tenant-bound
`SALES_AGENT_V0_CREDENTIAL` for the existing configured OpenAI path, then rerun
this activity. Alternatively, approve a separate Gemini provider/dependency
contract. Do not start the next activity automatically.
