# RLS Policy Specification — Supabase PostgreSQL

**Status:** technical security specification P0, **bukan SQL migration siap deploy**. Gunakan sebagai kontrak untuk menyusun dan menguji migration terpisah. RLS tidak berlaku pada object Cloudflare R2.

## Aturan umum

- Data tenant memakai `organization_id UUID NOT NULL`, FK komposit dan index sesuai query. `org_id` di beberapa dokumen lama adalah shorthand untuk `organization_id`, **bukan kolom kedua**.
- Tabel yang menampung data organisasi aktifkan `ENABLE ROW LEVEL SECURITY` dan, jika perlu untuk aplikasi, `FORCE ROW LEVEL SECURITY`. Default tanpa policy = deny.
- Query hanya memperoleh `auth.uid()` yang valid; anon/publik hanya melalui **published projection** terpisah untuk iklan, bukan tabel PII.
- Semua akses termasuk writes memerlukan **membership aktif, entitlement produk, role permission dan resource scope**. UI/URL/role header tidak dipercaya.
- `SECURITY DEFINER` hanya untuk helper/operasi teraudit: explicit `search_path`, minimal grants, jangan memperluas privileges via arbitrary arguments. Service role server-only, dan server tetap harus mengecek resource authorization.
- Untuk `INSERT`/`UPDATE`, policy `WITH CHECK` memvalidasi `organization_id` lama/baru, ownership, dan relation. Dilarang mengganti tenant ID untuk memindahkan data. `DELETE` sering disubstitusi soft delete yang butuh izin dan audit.

## Draft helper contracts

```sql
-- PSEUDOCODE CONTRACT, NOT EXECUTABLE MIGRATION
is_active_org_member(user_id uuid, organization_id uuid) -> boolean
has_product_entitlement(organization_id uuid, product_code text) -> boolean
has_scoped_permission(user_id uuid, organization_id uuid,
                      permission_code text, scope_type text, scope_id uuid) -> boolean
is_verified_self_resource(user_id uuid, organization_id uuid, resource_id uuid) -> boolean
```

Panggilan helper harus aman terhadap recursion RLS, menggunakan tipe scope yang di-whitelist dan tidak mengekspos data rahasia melalui hasil/exception. Grant role tidak boleh berasal dari `auth.jwt().user_metadata` yang dapat diubah pengguna.

## Matriks policy target

| Table family | SELECT | INSERT/UPDATE | DELETE/transition |
|---|---|---|---|
| `profiles` | own; minimal org projections jika permitted | own permitted fields | admin retention path only |
| `organizations` | member or public-safe projection | audited org onboarding | archive by authorized owner |
| `organization_members` | own + org.manage grant | admin, verified invitation flow | revoke with last-owner guard |
| `role_assignments` | own + authorized org admin | authorized role manager with no escalation | audited revoke |
| `kos_properties/units` | entitlement + property scope | property manage permission | archive, quota check |
| `kos_leases/tenants` | staff property scope or verified tenant-self | privileged property actor | archive with history |
| `kos_payment_records` | staff property scope or own bill | record grant; verify via dedicated audited transition | reversal, never silent delete |
| `warga_houses/residents` | verified household or permitted org/block role | org resident manager | PII retention checks |
| `warga_ipl_bills/payment_records` | own verified household or finance scope | record/verify distinct grants | reversal, not hard delete |
| `warga_events/event_finance` | event assignment or authorized org finance scope | event finance write; transfer both accounts | correction ledger, no silent delete |
| `ad_listings` | owner/scope; public **published projection only** | source owner/grant/moderation | unpublish, expire, retain trail |
| `billing_accounts/service_orders` | billing account grants | server-priced and audited | immutable final states |
| `wallets/wallet_ledger` | billing viewer | server-only atomic procedure and provider verification | immutable ledger, compensating entries |
| `file_assets/file_links` | actor + file→entity org/scope | upload-intent & finalizer server-verified | retention + legal hold checks |
| `audit_logs` | restricted actor/purpose | append-only authorized writers | retention-controlled archive only |

**Note:** actual table definitions for database migrations are in [Database Schema](../03-data/Database-Schema.md); data model existing is conceptual.

## Public ads + R2

Published API uses explicitly whitelisted `ad_publications` / public projection that omits tenant contacts, home address, household, private file keys and unpublished media. If a product source is revoked, listing projection must be updated/unpublished asynchronously with durable retry and tests. File downloads require API authorization **in addition to** metadata RLS because R2 has no Supabase policy enforcement.

## Race and cross-tenant constraints

- Use composite foreign keys or trusted SQL validation so e.g. lease/property, event/account, file/payment cannot cross tenant even if server bug.
- Prevent TOCTOU: state-changing operations perform authorization inside transaction with appropriate lock where role/ownership/state may change concurrently.
- Payment and wallet writes execute through server-only, idempotent transaction/function with minimal grants; no client direct writes to ledger.
- Reads must check access to the **specific object**, not merely to any record in organization.

## Required negative test matrix

1. unauthenticated read, write and RPC bypass attempt.
2. User A member org 1, not org 2 → cannot read/write with crafted `organization_id`.
3. property-scoped staff A cannot access property B; event treasurer A cannot access event B/general cashbook.
4. user cannot update `organization_id`, `created_by`, `verified_by`, `role_assignment` or another user ID to obtain privileges.
5. disabled/revoked membership, expired entitlement, invited but pending user cannot access.
6. self tenant/warga can access only linked/verified invoices, leases, documents.
7. public anon cannot access draft ads, resident data, original private image or private R2 object.
8. wallet ledger direct client INSERT/UPDATE/DELETE fails; duplicate webhook/debit cannot double post.
9. security helper does not leak membership enumeration; security definer has safe search_path and granted execute only where required.
10. file signed URL API rechecks permission on every issuance; leaked URL exposure capped by TTL, not claimed instantly revoked.

**Release gate:** no P0 schema deployed until RLS+negative integration suite green in staging. See [Permission Matrix](Permission-Matrix.md), [Security & Privacy](Security-Privacy.md), [Test Plan](../09-delivery/Test-Plan.md).
