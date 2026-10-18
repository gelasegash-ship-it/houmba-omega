# Deployment and integration status

## What is now in the repository
- `NOVA-CORE/index.html`: mobile-first dashboard with task progress, local browser persistence, local action-plan generator, client-message draft, manual revenue/cost calculation and JSON export.
- `NOVA-CORE/README.md`: product scope and roadmap.
- `NOVA-CORE/AGENT_SPEC.md`: agent orchestration and safety requirements.
- `NOVA-CORE/QA_CHECKLIST.md`: manual mobile/desktop, functionality and production-security checks.
- `supabase/migrations/202610170001_nova_core_foundation.sql`: private user-owned mission/task schema with row-level security (RLS), committed and applied to the live database on 2026-10-18.
- `supabase/functions/nova-plan/index.ts`: authenticated planning baseline; no live model call.
- `vercel.json`: baseline security headers for a future deployment.
- `.github/workflows/nova-core-checks.yml` and `scripts/check_static.py`: static smoke check automation.

## Supabase ALPHA TECH — verified state
- Project ref: `mbrxsitcnlmwlpmdwxhf`, region `eu-west-1`, organization `ALPHA TECH`.
- Project restore was requested successfully on 2026-10-17.
- Project status is now `ACTIVE_HEALTHY`; the database is accepting connections.
- Edge Function `nova-plan` was deployed successfully, version 1, with JWT verification enabled.
- Migration `nova_core_foundation` was applied successfully; Supabase migration history confirms version `20261018043540`.
- No provider API key or other secret was added to the repository.
- Billing plan and the account's invoice/usage page were not available through the connected project metadata. Supabase docs state paused projects incur no compute charges; active compute may incur usage-based charges depending on the organization plan and compute size. Confirm the ALPHA TECH billing plan and current usage in the Supabase dashboard before leaving the project running.

## Verified limitations
- The dashboard's plan and message generators are local templates, not a connected AI model.
- Task and finance data are stored in the browser on the current device; there is no cloud sync or user authentication yet.
- No bank, mobile-money wallet, payment processor, prospecting channel or revenue source is connected.
- Vercel deployment has not been verified. A repository file is not proof of a live deployment.

## Required before production
1. Confirm the ALPHA TECH plan and usage in billing settings; monitor spend if the project remains active.
2. Verify the mission/task tables and RLS behavior with authenticated test accounts; migration history confirms the DDL ran, but a full authenticated isolation test remains outstanding.
3. Add authentication, cloud persistence, and account recovery.
4. Keep JWT verification enabled. Add a model-provider secret only through the Supabase server-side secrets manager, then implement provider calls, validation, rate limits and usage/cost limits.
5. Connect Vercel, set only the required public client configuration, deploy and verify the actual URL.
6. Complete accessibility, privacy, backup, security and mobile-device testing.

## Release rule
Do not describe this project as a production-ready autonomous AI, a live service, or a source of guaranteed income until those checks pass. The present version is a useful local prototype plus a deployed safe-planning Edge Function.
