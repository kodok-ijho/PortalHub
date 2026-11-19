# Test strategy and UAT

## Layers

- Unit: pricing, quota, status transition, IDR money math, utility functions.
- Integration: RLS, composite FK, API auth, service order transaction, provider webhook.
- E2E: signup+invite, org switch, property staff restrictions, rent recording, Kantong QRIS, ad publish and SEO.
- Security: cross-tenant and cross-scope references, replays, tampered webhook, PII leak, stale caches.
- Non-functional: page load/SEO, PWA install/offline, mobile device matrix, accessibility.

## UAT critical cases

| ID | Scenario | Expected |
|---|---|---|
| UAT-01 | A user belongs to two orgs | Switching reveals only authorized resources |
| UAT-02 | Staff Kos A reads Kos B | Denied in API/RLS |
| UAT-03 | Tenant sees another lease | Denied |
| UAT-04 | Event treasurer tries general cashbook | Denied |
| UAT-05 | Subsidy transferred main → event | Accounts net correctly, consolidated no double count |
| UAT-06 | Warga pays IPL externally | Manual transfer/cash record and internal verification, no gateway |
| UAT-07 | Duplicate top-up webhook | One credit only |
| UAT-08 | Direct pay QRIS | Service activated once; Payment history only |
| UAT-09 | Top-up exact amount then pay | Separate linked top-up credit + debit |
| UAT-10 | Insufficient auto-renew wallet | No debit or renewal, notify |
| UAT-11 | Ads publication without opt-in | Not public/indexed |
| UAT-12 | Unit occupied after ad active | Mark unavailable promptly |
| UAT-13 | Private page search crawler | noindex and no sensitive HTML |
| UAT-14 | Policy changed auto→approval | New applications use policy; old grants unchanged unless explicit process |
| UAT-15 | Org with 3 properties 15+20+10 units | Usage = 45 active rentable units |

## Exit

All P0 pass; zero critical security/privacy/payment defects; audit/rollback demonstrated, product owner signs UAT. Record known issues in issue tracker.
