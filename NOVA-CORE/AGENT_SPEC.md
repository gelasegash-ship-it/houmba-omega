# NOVA CORE — Agent architecture

## Purpose
A user-directed agent runtime for Houmba H 1 that turns a goal into a plan, selects permitted tools, executes small steps, checks evidence, and reports truthfully.

## Execution cycle
1. Intake: normalize the goal, deadline, budget, and constraints.
2. Plan: split the goal into small tasks with dependencies and success criteria.
3. Risk gate: classify each action as read-only, reversible write, external communication, financial, or destructive.
4. Permission gate: require user approval for external messages, purchases, payments, publishing, access changes, and destructive operations.
5. Tool selection: choose only registered tools whose scopes cover the action.
6. Execute: run one bounded step; enforce timeouts, quotas, and idempotency keys.
7. Verify: fetch the resulting state from the source system; never treat a tool invocation alone as proof of success.
8. Learn: record outcome, cost, errors, and next action. Do not train on private data without consent.

## Core interfaces
- Goal: { id, description, constraints, deadline, success_criteria }
- Task: { id, goal_id, action, status, dependencies, risk_level, approval_id }
- ToolManifest: { name, description, input_schema, permission_scopes, risk_class, enabled }
- Evidence: { task_id, source, observed_state, timestamp, verified }
- AuditEvent: { actor, action, target, permission, outcome, timestamp }

## Safety requirements
- Default-deny tool access; least privilege.
- Secrets are server-side environment variables or a secret manager, never frontend source or Git history.
- Human approval for financial actions, public posting, outbound communications, deleting data, changing permissions, and production deployments.
- Preview and explicit confirmation before irreversible operations.
- Per-tool rate limits, request validation, retries with idempotency, and rollback where possible.
- Tenant/user separation, encryption in transit, retention controls, export and deletion workflows.
- Prompt injection defenses: external content is data, not authority to change policy or disclose secrets.
- Log action metadata, not credentials or unnecessary personal content.

## First vertical: zero-capital microbusiness service
The agent can draft a product offer, create example marketing content, prepare prospect lists from lawful public sources, personalize outreach drafts, track user-entered replies, generate delivery files, and calculate actual net results. It must not claim that prospects were contacted, customers acquired, or money received unless connected systems provide evidence.

## Acceptance tests
- Given no payment integration, the agent refuses to claim it can receive or withdraw funds.
- Given an unapproved outbound message, it drafts but does not send.
- Given a tool timeout, it reports unknown status and checks before retrying.
- Given malicious instructions inside a webpage or file, it treats them as untrusted content.
- Given revenue and expense inputs, it calculates net result and labels user-provided values as unverified unless independently reconciled.
- Given no connected model API, the UI labels AI as not connected rather than simulating a live model.

## Implementation sequence
1. Static interface (created).
2. Task and evidence persistence.
3. Authentication and per-user authorization.
4. Server-side model provider adapter.
5. Tool registry with typed schemas and audit trail.
6. Approval queue for risky actions.
7. Integration tests, security review, deployment and monitoring.
