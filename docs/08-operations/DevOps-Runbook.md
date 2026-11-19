# DevOps / release / runbook

## Environments

`dev`, `staging`, `production`: separate Supabase projects, payment credentials, buckets, webhook endpoints and Vercel deployments. No staging/production shared financial ledger. Rehearse migrations in staging first.

## Proposed CI

1. Install pinned deps and lockfile check.
2. Lint, formatting, unit tests, type checks if TS adopted.
3. Schema migration test, RLS negative tests, privacy constraints.
4. Integration: provider mock signature/replay, Kantong racing debit, event transfer totals.
5. Build PWA/SSR + automated E2E with Playwright for critical paths.
6. PR review, staging deploy, smoke, prod approval.

## Operational checklist

- Monitor payment webhook failures, retry queue, duplicate events, unmatched settlement, wallet reconciliation, expired listing jobs, auth errors, RLS denials spikes.
- Daily finance reconciliation of provider-settled platform payments vs service orders/top-ups.
- Backup DB and files; period + RPO/RTO chosen, perform a restore drill before production.
- Rotate secrets; test credential revocation. Do not store PII in observability logs.
- Document paging/contacts, rollback migrations, partial outage communication and incident logging.

## Deployment notes

Vercel SPA fallback for private app vs SSR rewrites for public ads must not conflict. Cache private pages `no-store`; static content cache by hash. Validate deep-link login and redirect on preview and production.

## Failure response

If provider callback invalid or provider unreachable: keep order pending, never grant entitlement. If ledger mismatch: freeze affected wallet writes until investigated, compensate only via authorized journal entry. If cross-tenant leak: disable affected endpoint, revoke credentials, preserve evidence and follow incident plan.
