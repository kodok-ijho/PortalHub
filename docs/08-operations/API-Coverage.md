# API Contract Coverage Matrix — PortalHub

> **Status: design coverage, not implemented endpoints.** [OpenAPI.yaml](OpenAPI.yaml) adalah sumber yang dapat diparse untuk endpoint yang sudah didefinisikan. [API-Contract.md](API-Contract.md) menjelaskan kebutuhan luas yang **tidak otomatis tertulis di OpenAPI**. Agent tidak boleh menganggap endpoint berjalan sebelum ada implementasi & contract tests.

## Status cakupan dan prioritas

| Domain | Baseline OpenAPI saat audit | Harus dicakup sebelum agent frontend/backend integrasi | Gate |
|---|---|---|---|
| Identity | `GET /me/contexts` | auth/session, invitation accept, linking verified tenant/resident, context release | PH-001/002/005 |
| Organizations | `POST /organizations` | list/detail, members/invite, onboarding approval, policies/versioning, roles/scope | PH-002/004/006 |
| Billing | Wallet, topup, orders, checkout, renewal | wallet ledger, orders/status, entitlement, provider contract after selection | BL-001..007; live blocked |
| PortalKos | Not represented in initial OpenAPI | property/unit/lease, charges, manual pay/verify, reporting | PK-001..007 |
| PortalWarga | Not represented in initial OpenAPI | house/residents, IPL, general/event accounts & transactions, transfers | PW-001..006 |
| PortalIklan | Public list/detail only | draft CRUD, moderation/approval, publish/expire/takedown, source sync | PI-001..007 |
| Cloudflare R2 | upload intent/complete/download | authorized metadata, publish sanitized media, delete under legal hold, usage quota | STO-001..006 |
| Events/jobs | Not represented in initial OpenAPI | internal event schema, retry/dedup/outbox, notification preferences | OPS-001 |

## Contract-first instructions for each new endpoint

1. Define authorization matrix for membership **and** product entitlement, role, property/event/self scope; decide when missing resources return 404 rather than 403 to reduce enumeration.
2. Define method, path params, query params, request schema, response schema, standard errors, pagination/idempotency key, and state transitions.
3. Add negative tests (cross-org UUID, disabled member, forbidden property/event, unavailable listing/asset, replay/race).
4. Get integration owner to freeze shared contract revision before independent frontend/backend implementation.
5. Add schema to OpenAPI 3.1, generate types or validate mocks, execute contract tests, then mark requirement evidence in traceability.
6. Anything touching payment live, price, publish quota/expiry, or data deletion remains **mock/disabled until approved**.

## Critical consistency constraints

- Prefix `/api/v1` is a design path; use canonical `organization_id` in paths/database. UI slug must never bypass auth on UUID.
- `amount_minor` = **whole IDR rupiah** despite identifier name. No float.
- Successful mutation on a browser does not imply provider settlement.
- Private R2 objects only via backend-issued, short-lived presigned URL; never include such URL in logs, public SSR, or cache.
- `organization_id` and `resource_id` must be verified server-side from trusted session, not trusted by request presence.
- Do not infer complete API coverage from a path count; track coverage by requirement, not quantity.

## Completion checklist

- [ ] Core identity & organization contracts and tests
- [ ] Kos full CRUD/finance contracts and tests
- [ ] Warga full CRUD/finance/event contracts and tests
- [ ] Ads content/moderation/source sync/SEO contracts and tests
- [ ] Billing real provider contracts **after provider approval**
- [ ] R2 metadata/publish/delete/usage contracts and tests
- [ ] Consistent errors, pagination, RLS checks and generated clients
