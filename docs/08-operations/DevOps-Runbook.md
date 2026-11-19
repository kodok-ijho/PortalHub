# DevOps / release / runbook

## Environments

`dev`, `staging`, `production`: separate Supabase projects, payment credentials, **Cloudflare R2 buckets and S3 credentials**, webhook endpoints and Vercel deployments. No staging/production shared financial ledger. Rehearse migrations in staging first.

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


## Cloudflare R2 provisioning & operations

- Dev/staging/prod harus memiliki bucket `private`, `temp`, `public` dan R2 S3 API credentials sendiri; hanya backend memiliki `R2_SECRET_ACCESS_KEY`. Jangan gunakan `VITE_`/`NEXT_PUBLIC_` untuk secret.
- Aktifkan custom domain CDN **hanya** bagi approved public media; `r2.dev` tidak direkomendasikan untuk trafik produksi. Konfigurasi bucket CORS origin/method/header untuk upload presigned dari aplikasi.
- Deploy upload intents, R2 storage adapter, post-upload HEAD+MIME/size+scan/quarantine, quota reservations, orphan cleanup dan retention worker. Monitor 4xx/5xx, malware findings, unexpected public exposure, biaya storage & operasi/CDN/transform.
- Backup data **Supabase PostgreSQL** dan objek **R2** secara terpisah; jalankan tes restore bersama berdasar metadata/checksum, pastikan RPO/RTO dan legal hold. Database backup saja tidak mencadangkan file.
- Rotasi credential, audit secret scope dan rollback. Presigned GET/PUT TTL pendek, jangan log signed URL atau lampiran sensitif. Uji takedown dari CDN public dan non-leak PWA.

[File Storage](../03-data/File-Storage.md) · [ADR-0003](../10-decisions/ADR-0003-cloudflare-r2.md).
