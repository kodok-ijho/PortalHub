# Database data model (logical, not migration SQL)

## Conventions

- UUID primary keys, timestamp `created_at/updated_at`, soft delete for non-immutable records when required.
- Tenant tables require `organization_id uuid NOT NULL`, composite indexes, and composite FK when cross-table tenant id is a risk.
- Money `amount_minor bigint` (IDR whole rupiah), ISO currency `IDR`. No float for money.
- `created_by`, `verified_by`, `audit_log` for sensitive actions.
- Public ad projection stores only fields explicitly approved for publication.

## Core entities

| Table | Key columns | Notes |
|---|---|---|
| `profiles` | id auth user FK, display_name | PII private |
| `organizations` | id, slug unique, type, verification_status | org identity |
| `organization_members` | org_id, user_id, status | many-to-many |
| `products` | id, code | catalog |
| `organization_products` | org_id, product_id, state | entitlements |
| `roles` / `permissions` / `role_permissions` | role_code, permission_code | role bundles |
| `role_assignments` | org_id, user_id, product_id, role_id, scope_type, scope_id | check scope exists + same org |
| `organization_invitations` | org_id, email_hash/ref, invite_token_hash, expires_at | single use |
| `policy_versions` / `organization_policy_overrides` | key, value, effective_at, author | audited |

## Kos

`kos_properties`(org_id, property_id, slug, address_private), `kos_units`(org_id, property_id, status, rentable, unit_type), `kos_tenants`(org_id, person_id, linked_user_id nullable), `kos_leases`(org_id, unit_id, tenant_id, start/end/status), `kos_occupants`, `kos_charges`, `kos_payment_records`(method cash/transfer, status pending_internal_verification/verified_internal/rejected), `kos_payment_evidence`, `kos_expenses`, `kos_deposit_records` (tenant security deposit **only recorded**, not Kantong), `kos_maintenance_tickets`.

**Constraints:** no active lease overlap for same unit unless explicit sharing model; unit belongs to property in same org; active-unit quota count server-side.

## Warga

`warga_houses`(org_id, house_id, block), `warga_residents`(org_id, person_id, linked_user_id nullable), `warga_house_memberships`, `warga_ipl_schedules`, `warga_ipl_bills`, `warga_payment_records` (manual only), `warga_events`, `warga_event_members`, `warga_financial_accounts`(type general/event), `warga_financial_transactions`(account_id, event_id nullable, transfer_id nullable), `warga_internal_transfers`, `warga_documents`.

**Constraint:** every event financial account belongs to one event; expense/income event_id must match account event_id; internal transfer posts equal opposite movements atomically; reports avoid double count.

## Ads

`ad_categories`, `ad_listings`(org_id, source_product, source_type, source_id, status, title, slug, public_location, expires_at), `ad_listing_media`, `ad_moderation`, `ad_publications`, `ad_free_quotas`, `ad_packages`, `ad_package_usage`, `ad_inquiries`, `ad_event_metrics`. Keep source linkage, publication moderation, and availability as separate concerns.

## Platform billing

`billing_accounts`(org_id), `service_orders`(billing_account_id, idempotency_key, status, total_minor), `service_order_items`, `platform_invoices`, `platform_payments`(provider, provider_ref unique, state), `wallets`(billing_account_id, currency), `wallet_topups`, `wallet_ledger`(wallet_id, direction, amount_minor, reference_type/id, created_at; append-only), `subscriptions`, `subscription_renewals`, `product_packages`, `package_entitlements`, `entitlement_consumption`, `payment_webhook_events`, `audit_logs`.

## Ledger invariants

- Wallet unique per billing account+currency. `wallet_ledger` is source of truth; cached balance is reconciled and protected under row-level lock/transaction.
- Unique `(wallet_id, idempotency_key)` or equivalent transaction identity for debit; zero negative balance.
- Posting a payment requires verified provider state and unique event ID; direct payments bypass wallet ledger.
- Correction is a compensating entry, never edit/delete settled ledger entry.

## Tenant access model

RLS policy should call vetted security functions to check active membership, org product, role permission and resource assignment. Administrative APIs employ service credentials server-side only and still explicitly enforce authorization. Tests must include cross-org FK injection and cross-scope UUID accesses.

## Naming tradeoff

`warga_houses` intentionally distinct from `kos_units`. Event and property assignments separate or generic scope with validated references; avoid polymorphic FK without database constraints for sensitive access.
