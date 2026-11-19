# Migrasi PortalWarga legacy

**Sumber:** `https://github.com/kodok-ijho/PortalWarga`, diaudit secara read-only pada 19 Nov 2026.

## Temuan terverifikasi dari file repo

- `client/package.json`: React 18, Vite 5, Tailwind 3, Supabase JS, TanStack Query, vite-plugin-pwa, Playwright.
- `client/src/pages/Events.jsx` dan `EventFinance.jsx` tersedia.
- `supabase/migrations/202608010001_event_finance_foundation.sql`: event roles, `event_members`, `non_ipl_incomes`, event-scoped expenses.
- `docs/production/EVENT_FINANCE_API_CONTRACT.md`: event permission event-scoped, soft-delete, no global event role enum.
- `docs/production/MIDTRANS_TRANSACTION_FLOW.md`: menggambarkan QRIS IPL lama; bertentangan dengan desain pembayaran operasional PortalHub yang baru dan **harus ditinjau, bukan diadopsi otomatis**.
- `docs/production/EVENT_FINANCE_BASELINE_CHECK.md` mencatat status suatu environment pada 1 Agustus 2026. **Jangan menganggap status tersebut masih berlaku.**

## Migration mapping

| Legacy | Target |
|---|---|
| `profiles` | `profiles` + `organization_members` + product assignments |
| `units` (rumah) | `warga_houses` (jangan bentrok dengan `kos_units`) |
| `ipl_bills`, `payments` | `warga_ipl_bills`, `warga_payment_records` (no gateway) |
| `events`, `event_members` | org-scoped event + scope permissions |
| `non_ipl_incomes`, event expenses | `warga_financial_transactions` with account/event link |
| existing QRIS IPL flows | archival / feature flag disabled in PortalHub |

## Safe cutover

1. Freeze schema inventory; export anonymized fixtures.
2. Define immutable org mapping; decide duplicated unit/person merge policy.
3. Additive schema in staging; backfill IDs and FK; tests + totals comparison.
4. Remove payment gateway action for IPL in new UI/API; preserve historical records as legacy.
5. Validate event cashbook and reports against legacy totals, check transfers.
6. Pilot one organization; parallel reconciliation; sign-off; progressive rollout.
7. Keep legacy app unchanged until separate migration authorization.

**Open issue:** existing payment statuses/webhooks must be mapped to new manual-recording semantics transparently; do not falsify financial history.
