# NOVA CORE — Integration status

## Live Supabase
- Project: ALPHA TECH (`mbrxsitcnlmwlpmdwxhf`), region `eu-west-1`.
- Current project status: ACTIVE_HEALTHY.
- Tables verified: `public.nova_missions` and `public.nova_tasks`.
- Row-level security is enabled on both tables.
- Applied migrations confirmed by Supabase history: `nova_core_foundation`, `nova_tasks_mission_fk_index`.
- Security advisor returned no lints at the last check.
- Performance advisor reports only unused indexes while the tables have no data; these are informational.

## Edge Function
- `nova-plan` is ACTIVE with JWT verification enabled.
- Current behavior is a safe planning baseline and explicitly returns `connected_model: false`.
- No external LLM provider key has been installed; do not describe this as a fully connected AI agent.
- Browser client should call the function only after authentication.

## Repository interface
- The local-first dashboard is in `NOVA-CORE/index.html`.
- It includes task checklists, local persistence, a local plan template, customer outreach draft, manual finance register and JSON export.
- A direct GitHub update attempt to add the Supabase authentication/cloud-sync module was blocked by a platform security control and was not committed. Therefore, do not claim that login/cloud sync has been integrated into the dashboard yet.
- The Supabase publishable key is public by design; never embed a service-role key, database password, or model-provider secret in frontend files.

## Remaining production work
1. Integrate Supabase Auth in the dashboard and test sign-up/sign-in/session restoration.
2. Replace local-only persistence with authenticated cloud sync and test cross-user isolation.
3. Configure a server-side model provider secret in Supabase Edge Function secrets, then update `nova-plan` to call the model with strict timeouts, input/output limits and usage caps.
4. Test `nova-plan` with an authenticated session; do not disable JWT verification.
5. Verify GitHub Pages workflow succeeds and test the published site on Android.
6. Review billing/usage for the active Supabase project before leaving it running.
7. Add account recovery, privacy/retention documentation, backups, accessibility tests, abuse/rate limits and monitoring.

## Honest release status
The backend schema and baseline planning function are live. The dashboard remains local-first. Cloud sync, real model inference, end-to-end auth tests and verified public release are not yet complete. Revenue generation is not guaranteed and no payment provider is connected.
