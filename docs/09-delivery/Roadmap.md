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
