# NOA H 1 security model

## Control boundary

The agent may research, rank, draft, measure and propose actions. Side effects remain behind a policy gate. Financial actions require provider-specific authorization and an auditable decision.

## Modes

- `research`: read-only analysis and opportunity discovery.
- `paper`: simulated execution and backtesting; no real-money side effects.
- `live`: only supported provider actions, within configured limits and approval rules.

## Secrets

API keys, payment credentials, webhook secrets and privileged Supabase keys belong only in server-side secret storage. Never put them in frontend code or Git history.

## Database

When Supabase is used, exposed tables must have Row Level Security and ownership-aware policies. Supabase recommends RLS for every exposed table and warns that service/secret keys must remain server-side.

## Agent governance

Use tool guardrails and human approval for consequential actions. OpenAI's current Agents guidance recommends human review for sensitive side effects and tracing for tool calls, handoffs and guardrails.
