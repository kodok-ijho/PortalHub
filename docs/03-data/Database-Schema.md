# Database Schema — Logical-to-Physical Blueprint

**Status:** rancangan implementasi P0, belum SQL migration dan belum dijalankan. Keputusan produk berasal dari [PRD](../PRD.md), [Data Model](Data-Model.md), [RLS Policy Spec](../04-security/RLS-Policy-Spec.md), dan [File Storage](File-Storage.md).

## Konvensi kanonik

- ID primary `uuid`; timestamp `timestamptz` UTC; audit `created_at`, `updated_at`, `created_by` bila sesuai. Uang **IDR integer rupiah** disimpan pada `amount_minor bigint` sesuai model awal (nama field historis, bukan sen).
- **Nama target untuk kolom tenant adalah `organization_id`** pada tabel tenant-scoped. Singkatan `org_id` dalam spesifikasi lama berarti field tersebut, bukan kolom ganda.
- FK lintas entity mencakup `organization_id` untuk memastikan hubungan tidak bisa silang tenant. Unique/index multi-tenant diawali organization bila sesuai pola query. `auth.users.id` adalah identitas stabil.
- Hindari delete data akuntansi tersettlement; gunakan reversal/compensating entry dan audit. Desain detail enum, unique partial index, exclusion constraint harus diverifikasi dalam migration SQL.
- Identitas `profiles` tidak otomatis berhubungan dengan `warga_residents`/`kos_tenants` hingga verification link disetujui.

## Core identity / organisasi

| Tabel | Key fields | Constraint/relasi wajib |
|---|---|---|
| `profiles` | `user_id PK FK auth.users`, `display_name`, `status` | Public-safe projection tersendiri; PII private |
| `organizations` | `id PK`, `slug UNIQUE`, `type`, `verification_status` | Slug tidak menjadi authority |
| `organization_members` | `id PK`, `organization_id`, `user_id`, `status` | UNIQUE(org,user) untuk membership aktif/riwayat perlu kebijakan |
| `products` | `id PK`, `code UNIQUE`, `status` | Catalog server-managed |
| `organization_products` | `organization_id`, `product_id`, `status`, `entitlement_id` | Composite UNIQUE(org,product) active |
| `roles`, `permissions`, `role_permissions` | role id/code, permission code | Unique normalized code, server-authorized management |
| `role_assignments` | `organization_id`, `user_id`, `product_id`, `scope_type`, `scope_id`, `role_id` | Scope exists within org; no self-escalation |
| `organization_invitations` | `organization_id`, `target_email_hash`, `token_hash`, `status`, `expires_at` | Single-use token; replay rejection |
| `policy_versions` / `organization_policy_overrides` | policy key, version, effective_at, author | Effective forward and immutable audit |

## PortalKos

| Tabel | Key fields | Invariant |
|---|---|---|
| `kos_properties` | `organization_id`, `id`, `slug`, `address_private` | Unique slug within org |
| `kos_units` | `organization_id`, `property_id`, `status`, `rentable` | Composite FK property+org; quota active rentable units |
| `kos_tenants` | `organization_id`, `id`, `linked_user_id NULL` | No automatic login/proof |
| `kos_leases` | `organization_id`, `unit_id`, `tenant_id`, `start_at`, `end_at`, `status` | Non-overlapping effective active lease for single-exclusive unit |
| `kos_charges` | `organization_id`, `lease_id`, `period`, `amount_minor`, `status` | Unique invoice identity per lease/category/period; immutable paid history |
| `kos_payment_records` | `organization_id`, `charge_id`, `method`, `status`, `amount_minor`, `verified_by` | External manual records only; adjustments/reversal |
| `kos_deposit_records` | `organization_id`, `lease_id`, `amount_minor`, `movement_type` | Recording liability, **not Kantong** |
| `kos_expenses`, `kos_maintenance_tickets` | org+property refs | Property scope, audit, attachments via file_links |

## PortalWarga

| Tabel | Key fields | Invariant |
|---|---|---|
| `warga_houses` | `organization_id`, `id`, `block`, `address_private` | House unique identity per org |
| `warga_residents` / `warga_house_memberships` | org+house/person/verified link | Self access only on verified house relation |
| `warga_ipl_schedules`, `warga_ipl_bills` | org+house+period, amount_minor, due_at, state | Unique org+house+period+charge type |
| `warga_payment_records` | org+bill, method, status, verifier | No gateway settlement |
| `warga_events`, `warga_event_members` | org+event, user/role assignment | Event-scoped roles |
| `warga_financial_accounts` | org+id, account_type `general/event`, `event_id` | Event account must point to event same org |
| `warga_financial_transactions` | org+account, event_id?, transfer_id?, direction, amount_minor | Event_id matches account; immutable approved history |
| `warga_internal_transfers` | org+source_account+destination_account, amount, state | Paired debit/credit, unique transfer_id, atomic, excluded from revenue/expense consolidation |
| `warga_documents` | org+resource+file link | Private Cloudflare R2, scoped read |

## PortalIklan

| Tabel | Key fields | Invariant |
|---|---|---|
| `ad_listings` | org+id, source_product, source_type/id, state, slug, expires_at | Source verified, privacy default private |
| `ad_publications` | listing_id, version, moderation_decision, public projection | Only reviewed fields published |
| `ad_listing_media` | listing_id, file_asset_id, sort_order | Public media derivative only |
| `ad_categories`, `ad_moderation`, `ad_free_quotas` | policy/version, actors | Audit moderation |
| `ad_packages`, `ad_package_usage` | billing entitlement + listing | Consume quota atomically, expiry enforced |
| `ad_inquiries`, `ad_event_metrics` | listing_id, permitted public data | PII minimization and rate limits |

## Billing & Kantong

| Tabel | Key fields | Invariant |
|---|---|---|
| `billing_accounts` | id, organization_id UNIQUE | Default org-owned; individual wallet model unresolved |
| `service_orders`, `service_order_items` | billing_account_id, amount_minor, status, idempotency key | Server-priced order snapshot, no client amount authority |
| `platform_invoices`, `platform_payments` | service_order_id, provider_ref, state | Unique provider reference+event, verified settlement |
| `wallets` | billing_account_id, currency | UNIQUE(billing_account_id,currency), nonnegative available balance |
| `wallet_topups`, `wallet_ledger` | wallet_id, movement, amount_minor, reference_id, idempotency key | Append-only, atomic unique spend; no P2P |
| `subscriptions`, `subscription_renewals` | billing_account_id, product_id, period, renewal preference | Unique subscription+period+renewal-type, consent recorded |
| `product_packages`, `package_entitlements`, `entitlement_consumption` | package, quantity, expiry | Package entitlement **not** monetary balance |
| `payment_webhook_events`, `audit_logs` | event unique, received_at, actor/action | Append-only processing audit and replay prevention |

## File metadata (Cloudflare R2)

`file_assets` stores bucket/key, class, scope, size, checksum, status; `file_links` associates asset with verified payment/lease/event/listing resource; `file_upload_intents` reserves quota; `file_access_audit` tracks authorized access. RLS limits **metadata**, while private object access is authorized by backend before signed R2 URL. See [File Storage](File-Storage.md).

## Physical constraints and transaction boundaries

1. Unique: `(billing_account_id,idempotency_key)`, provider reference, webhook event ID, wallet debit service order, subscription renewal period.
2. Index: org+scope+status and org+period columns; all FK columns used in RLS joins indexed appropriately.
3. Lease overlapping periods: implement exclusion constraint or equivalent serialized lock; document shared-unit exceptions before enabling.
4. `warga_internal_transfers`: transaction inserts exactly two signed movements or none; paired `transfer_id`; never double-count.
5. Wallet atomic debit: DB transaction locks wallet/cached balance, rechecks entitlements and amount, writes immutable ledger and order association; no negative balance, retries idempotent.
6. File finalization: object R2 is **external to PostgreSQL transaction**. Use durable pending status, worker, retry/compensation, orphan collector and reconciliation. Do not claim distributed atomicity.
7. Row-level authorization: explicit policies for select/insert/update/delete and tested security helper functions. Platform service access is restricted and not automatic tenant superuser.
8. Public ads read approved projection only; never join directly to private resident/tenant or file key.

## Migration plan (not executable SQL)

- 001 core identity/org/products/roles + unique/FKs and RLS tests.
- 002 scoped Kos/Warga data with composite FKs, constraints and policy tests.
- 003 service orders, Kantong ledger, webhook and entitlement transaction procedures.
- 004 ads projection, publication/expiry/consumption flows.
- 005 R2 file metadata, upload intents, audit, quota, backup reconciliation.
- Legacy PortalWarga backfill requires explicit dry run, reconciliation, cutover/rollback approval.
- Migrations additive first; avoid dropping fields until data reconciliation, deploy compatibility and backout reviewed.

**Open decisions:** statuses, tenant-link model for one user across households, tax fields/provider contract, retention, billing account ownership, quota numerical values. Do not invent production defaults.
