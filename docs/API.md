# API

Run locally with:

```bash
uvicorn backend.main:app --reload
```

Endpoints:

- `GET /health` — service health and current operating mode.
- `GET /opportunities/seed` — deterministic starter opportunity set.
- `POST /opportunities/rank` — rank supplied opportunities.
- `POST /venture/experiment` — design a bounded validation experiment.
- `POST /revenue/record` — record a revenue/cost event in the process-local ledger.
- `GET /revenue/metrics` — inspect gross, costs, net, margin and event count.
- `POST /risk/evaluate` — evaluate whether a proposed side effect is blocked, approved or requires confirmation.

For production, put authentication, durable storage, rate limits and provider-specific authorization in front of side-effecting endpoints.
