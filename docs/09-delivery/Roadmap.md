# Delivery roadmap & backlog

Milestones are **ordered dependencies**, not promised calendar dates. Estimate after team and scope review.

| Phase | Deliverable | Acceptance gate |
|---|---|---|
| 0 | Repo/CI, ADR, auth architecture, DB tenancy, baseline policies | RLS test suite green |
| 1 | Organizations & invites; product subscriptions; service orders; direct QRIS/transfer & Kantong | Replay/atomic debit/reconciliation pass |
| 2 | PortalKos properties, units, leases, manual finance, reports | Property-scoped E2E, unit quota |
| 3 | PortalIklan public SSR SEO, moderation, expiry, free quota | SEO HTML tests, public privacy |
| 4 | PortalKos → PortalIklan source sync | Vacancy/occupancy linked, opt-in |
| 5 | PortalWarga migration from legacy, event separate finance | UAT/financial reconciliation |
| 6 | PortalWarga → PortalIklan | Verified business owner publishing |
| 7 | Packages, promoted listings, monetization, public advertisers | Legal & provider review + UAT |

## First sprint ticket suggestions

- HUB-001 bootstrap monorepo and build pipeline.
- HUB-002 organizations/member identities & context switch.
- SEC-001 tenant RLS + negative tests.
- HUB-003 policies + versioned activation workflow.
- BILL-001 service order and entitlement projection.
- BILL-002 direct payment mock provider contract.
- BILL-003 append-only Kantong ledger transaction procedure.
- KOS-001 property/unit master schema.
- ADS-001 public listing publication projection.
- LEGACY-001 migration inventory & mapping, payment flow impact.

Every ticket needs acceptance criteria, tests, DB migration and permission checks. User-visible flags off until authorized release.


## Cloudflare R2 — additional P0 backlog

- **STO-001:** Provision private/temp/public buckets per env, least-privilege R2 credentials, browser CORS dan monitoring biaya.
- **STO-002:** Buat `file_assets`, `file_links`, `file_upload_intents`, RLS metadata, quota reservation dan audit.
- **STO-003:** Backend storage adapter, presigned PUT/GET, upload complete, HEAD, MIME/size/scanning, retry dan orphan cleanup.
- **STO-004:** Integrasi lampiran bukti transfer/kontrak/doc Warga & Kos, per-event/per-property scope dan status upload terpisah dari verifikasi pembayaran.
- **STO-005:** Media publik PortalIklan: consent, moderation, EXIF scrub, public R2 derivative, CDN caching & takedown.
- **STO-006:** Backup object R2 + DB restore bersama; security tests unauthorized access, quotas, malware dan expiry.

**Release gate:** private object tidak dapat diakses pengguna tidak berhak, public listing tidak membocorkan draft/private, biaya/retensi/backup diketahui dan teruji. [File Storage](../03-data/File-Storage.md).


## Penguatan dependensi implementasi (audit)

- **SEC-002** [Google Auth & SSO](../04-security/Auth-and-SSO.md), callback/session, invitation and verified self-link; 0/1/multi-context tests.
- **SEC-003** [Permission Matrix](../04-security/Permission-Matrix.md), [RLS Policy Spec](../04-security/RLS-Policy-Spec.md): org owner **bukan** otomatis event treasurer; role/scoped negative tests sebelum UI.
- **DB-001** [Database Schema](../03-data/Database-Schema.md): numbered migrations, composite tenant constraints, indexes, SQL RLS implementation and migration rollback in staging.
- **BILL-004** [Subscription Lifecycle](../05-billing/Subscription-Lifecycle.md) + [Payment State Machines](../05-billing/Payment-and-Wallet-State-Machines.md): direct settled vs atomic wallet debit, idempotency, reconciliation & legal gate.
- **API-001** [Draft OpenAPI](../08-operations/OpenAPI.yaml): implement endpoints contract-first and expand per product; do not equate spec with working API.
- **KOS-002 / WARGA-002 / ADS-002**: detailed [Kos Rules](../06-products/PortalKos-Business-Rules.md), [Warga Finance Rules](../06-products/PortalWarga-Finance-Rules.md), [Ads Publishing Rules](../06-products/PortalIklan-Publishing-Rules.md).
- **OPS-001** [Notifications & Jobs](../02-architecture/Notifications-and-Jobs.md), [Privacy](../03-data/Data-Retention-and-Privacy.md), [DR](../08-operations/Disaster-Recovery.md), [Development Setup](../08-operations/Development-Setup.md).
- **QA-001** Update [Requirements Traceability](Requirements-Traceability.md) for each accepted ticket with commit, test and UAT evidence.

**No credentials included or requested in these docs.** Production launch still gated by pricing, legal/provider and security approval.
