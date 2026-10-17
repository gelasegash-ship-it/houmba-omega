# Deployment and integration status

## Prepared in this repository
- `NOVA-CORE/index.html`: mobile-first static prototype.
- `NOVA-CORE/README.md`: product scope and roadmap.
- `NOVA-CORE/AGENT_SPEC.md`: agent orchestration and safety requirements.
- `supabase/migrations/202610170001_nova_core_foundation.sql`: private user-owned missions and tasks with RLS.
- `supabase/functions/nova-plan/index.ts`: authenticated planning baseline (not connected to a live model).
- `vercel.json`: baseline security headers for a future Vercel deployment.

## Still required before production
1. Activate or choose a Supabase project and apply the migration.
2. Configure Supabase URL and publishable key in the client; never expose service-role keys.
3. Deploy the Edge Function with JWT verification enabled.
4. Add a server-side model provider secret in Supabase function secrets. No secret is stored in Git.
5. Connect Vercel and deploy the repository; configure environment variables in the Vercel project.
6. Add authentication UI, persistence integration, automated tests, monitoring and security review.

The currently linked Supabase projects were returned as INACTIVE. No project was reactivated, no paid resource was created, and no model API was called. Vercel was not connected at the time this status was written. Therefore the app is not live yet.
