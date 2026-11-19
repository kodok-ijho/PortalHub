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
