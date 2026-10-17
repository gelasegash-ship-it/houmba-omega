# Deployment and integration status

## What is now in the repository
- `NOVA-CORE/index.html`: mobile-first dashboard with task progress, local browser persistence, local action-plan generator, client-message draft, manual revenue/cost calculation and JSON export.
- `NOVA-CORE/README.md`: product scope and roadmap.
- `NOVA-CORE/AGENT_SPEC.md`: agent orchestration and safety requirements.
- `NOVA-CORE/QA_CHECKLIST.md`: manual mobile/desktop, functionality and production-security checks.
- `supabase/migrations/202610170001_nova_core_foundation.sql`: proposed private user-owned mission/task schema with RLS.
- `supabase/functions/nova-plan/index.ts`: authenticated planning baseline; it does not call a live model yet.
- `vercel.json`: baseline security headers for a future deployment.

## Verified limitations
- The dashboard can be opened as a static page, but its plan and message generators are local templates, not a connected AI model.
- Task and finance data are stored in the browser on the current device; there is no cloud sync or user authentication yet.
- No bank, mobile-money wallet, payment processor, prospecting channel or revenue source is connected.
- The Supabase projects currently visible to the connected account were `gelase-pro` and `ALPHA TECH`, both reported as `INACTIVE`.
- No Supabase project was reactivated and no migration or Edge Function was deployed.
- Vercel deployment has not been verified. A repository file is not proof of a live deployment.
- No model API secret is stored in the repository.

## Required before production
1. Explicitly choose and activate the intended Supabase project; check any cost implications first.
2. Apply the migration and verify RLS with separate user accounts.
3. Add authentication, cloud persistence, and account recovery.
4. Deploy the Edge Function with JWT verification and add a server-side model-provider secret through the provider's secret manager.
5. Implement request validation, rate limits, error handling, usage/cost limits and automated tests.
6. Connect Vercel, set only the required public client configuration, deploy and verify the actual URL.
7. Complete accessibility, privacy, backup, security and mobile-device testing.

## Release rule
Do not describe this project as a production-ready autonomous AI, a live service, or a source of guaranteed income until those checks pass. The present version is a useful local prototype with transparent boundaries.
