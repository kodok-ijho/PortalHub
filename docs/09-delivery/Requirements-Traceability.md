# Requirements Traceability Matrix

**Status:** baseline mapping desain. Tidak ada klaim fitur sudah diimplementasikan atau tes sudah dieksekusi. Source requirement: [PRD](../PRD.md). Ini adalah daftar kontrol agar requirement tidak hilang saat coding.

## Interpretasi status

- `specified`: sudah dibahas dalam dokumen; bukan bukti implementasi.
- `needs-detail`: rule/parameter final belum disepakati atau kontrak kurang rinci.
- `implemented`/`tested`: **belum boleh dipakai** sampai ada PR, commit, dan hasil CI/UAT nyata.
- `blocked`: perlu keputusan hukum/provider/produk sebelum implementasi/aktivasi produksi.

## Core identity & security

| Requirement | Source of implementation design | Test gates | Status |
|---|---|---|---|
| PH-001 Google login / one identity | [Auth & SSO](../04-security/Auth-and-SSO.md) | OAuth callback, 0/1/multi org, safe redirect | specified |
| PH-002 multi-org + scoped roles | [Permission Matrix](../04-security/Permission-Matrix.md) | Cross-org/property/event negatives | specified |
| PH-003 product entitlement / subscription | [Subscription Lifecycle](../05-billing/Subscription-Lifecycle.md) | Activation, expiry, quota | specified |
| PH-004 Hybrid onboarding | [Auth](../04-security/Auth-and-SSO.md), [RBAC](../04-security/RBAC.md) | Approval, invite-only, no retroactive grants | needs-detail |
| PH-005 invitations / verified relations | [Auth & SSO](../04-security/Auth-and-SSO.md) | Expire, replay, verified self | specified |
| PH-006 role/custom roles | [Permission Matrix](../04-security/Permission-Matrix.md), [RLS](../04-security/RLS-Policy-Spec.md) | Role escalation, disable, RLS | specified |

## Produk

| Requirements | Design | Tests | Status |
|---|---|---|---|
| PK-001..002 (multi-property/units/status) | [Kos Rules](../06-products/PortalKos-Business-Rules.md), [Database](../03-data/Database-Schema.md) | Overlap/unit quota/status transition | needs-detail |
| PK-003..005 (leases/bills/manual finance/reports) | [Kos Rules](../06-products/PortalKos-Business-Rules.md), [Operational Finance](../05-billing/Operational-Finance.md) | Full/partial, reversal, scope | needs-detail |
| PK-006..007 (ads sync/tenant self) | [Ads Rules](../06-products/PortalIklan-Publishing-Rules.md), [Permission](../04-security/Permission-Matrix.md) | Occupied unit takedown, self-only | specified |
| PW-001..003 (residents/IPL/cashbook/docs) | [Warga Finance](../06-products/PortalWarga-Finance-Rules.md) | Household, IPL totals, adjustment | needs-detail |
| PW-004 (separate event finance) | [Warga Finance](../06-products/PortalWarga-Finance-Rules.md), [RLS](../04-security/RLS-Policy-Spec.md) | Event/account permission, transfer no double-count | specified |
| PW-005..006 (ads privacy/self scope) | [Ads Rules](../06-products/PortalIklan-Publishing-Rules.md), [Permission](../04-security/Permission-Matrix.md) | Private info leakage, verified household | specified |
| PI-001..003 (public SEO/moderation/privacy) | [Ads Rules](../06-products/PortalIklan-Publishing-Rules.md), [SEO](../06-products/PortalIklan-SEO.md) | SSR, no draft indexed, consent | specified |
| PI-004..007 (expiry/packages/checkout boundary) | [Ads Rules](../06-products/PortalIklan-Publishing-Rules.md), [Subscription](../05-billing/Subscription-Lifecycle.md) | Grace, package quotas, no buyer checkout | needs-detail |

## Billing, storage & operasional

| Requirements | Design | Tests | Status |
|---|---|---|---|
| BL-001..002 (Kantong/topup) | [Payment State Machines](../05-billing/Payment-and-Wallet-State-Machines.md) | Provider verified, no P2P | blocked (legal/provider) |
| BL-003..004 (3 histories/direct payments) | [Payment State Machines](../05-billing/Payment-and-Wallet-State-Machines.md), [OpenAPI](../08-operations/OpenAPI.yaml) | No wrong ledger credit, idempotent activation | specified; launch blocked |
| BL-005..007 (renewal/packages/refund) | [Subscription](../05-billing/Subscription-Lifecycle.md), [ADR-0002](../10-decisions/ADR-0002-wallet.md) | Consent, due, insufficient, refunds | blocked |
| STO-001..006 (R2) | [File Storage](../03-data/File-Storage.md), [ADR-0003](../10-decisions/ADR-0003-cloudflare-r2.md) | Cross-tenant, scan, signed URL, restore | specified |
| API contract | [OpenAPI](../08-operations/OpenAPI.yaml), [API Contract](../08-operations/API-Contract.md) | Schema validation/contract tests | needs-detail |
| Job, notification, retention & DR | [Jobs](../02-architecture/Notifications-and-Jobs.md), [Privacy](../03-data/Data-Retention-and-Privacy.md), [DR](../08-operations/Disaster-Recovery.md) | Scheduled idempotency, deletion and restore | needs-detail |

## Definition of implementation complete

For each ticket require: `requirement ID` → `design reference` → `schema/migration` → `API contract` → `permission policy` → `tests` → `PR/commit` → `CI result` → `UAT acceptance`. Fields `implemented` and `tested` must remain empty until actual evidence exists.

## Open decision register

| ID | Decision needed | Impact |
|---|---|---|
| DEC-PRICE | Prices, free quotas, trial/grace, proration | Billing, subscriptions, Kos/Warga plan limits |
| DEC-PAY | Provider/legal/tax/refund and unused Kantong balance | Production platform payments |
| DEC-ORG | Individual vs org wallet; verification criteria for Warga | Identity, billing ownership |
| DEC-KOS | Prorata/deposit/late fee/overlap and over-quota policy | Kos rules & invoice engine |
| DEC-WARGA | IPL effective dates/corrections/account closure | Warga finance |
| DEC-ADS | Ad packages, extensions, ranking, takedown SLA | Listing lifecycle |
| DEC-DATA | Personal data retention, deletion/holds, storage plan quotas | R2/legal/compliance |
| DEC-OPS | SLO, backup RPO/RTO, monitoring thresholds | Operations & DR |

**Do not infer missing decisions as production requirements.** See [Decision Register](../00-product/Decisions.md), [Test Plan](Test-Plan.md).
