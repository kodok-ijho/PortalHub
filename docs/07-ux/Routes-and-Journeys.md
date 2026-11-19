# Roles, routes & user journeys

## Roles → landing

- Penyewa only: login → `/kos/:org/penyewa`.
- Warga only: login → `/warga/:org/beranda`.
- Owner of multiple orgs: login → `/app` chooser, remember last authorized product.
- Admin platform: private admin with audited privileges; no implicit tenant PII.
- Anonymous visitor: `/iklan` and public listing details without login.

## Journey sample: Budi

Budi can be tenant in Kos Melati and Bendahara in RT Melati. Identity is one `auth_user`, assignments are separate `(org, product, role, scope)`. Switching context triggers new authorization check and clears sensitive cached data.

## Journey sample: tenant payment

Tenant receives external bank account instructions from kos owner (provided by owner directly) → pays outside system → uploads transfer proof or asks staff to record cash → finance marks `verified_internal` → personal invoice displays appropriate internal status. No PortalHub payment button for rent.

## Journey sample: subscriptions

Billing owner opens `/app/subscription` → selects package and period → chooses Kantong, direct QRIS/transfer, or top-up exact invoice → verified settlement → receives receipt and entitlement. Consent is separately required for auto-renew.

## Journey sample: publishing ads

Owner marks unit vacant and opts in → selects which info may be public → preview → moderation → published SEO link. Listing expires on schedule, may renew via package/wallet/direct payment; occupancy invalidates available claim.
