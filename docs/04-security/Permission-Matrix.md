# Permission Matrix — Role × Product × Resource

**Status:** baseline rancangan P0 untuk implementasi; permission harus dicek server-side dan melalui Supabase PostgreSQL RLS jika melibatkan data tenant. **Tidak ada akses implisit dari jabatan lintas produk.**

## Formula otorisasi

`allow = authenticated AND active_membership(organization) AND active_product_entitlement AND grants(permission) AND resource_scope_matches AND mandatory_policy_checks`.

Istilah:
- **Platform scope:** konfigurasi layanan/moderasi, bukan hak baca PII seluruh tenant.
- **Organization scope:** satu organisasi yang diverifikasi membership-nya.
- **Property scope:** kos/property yang secara eksplisit ditugaskan.
- **Household/self scope:** rumah/kontrak yang sudah dikaitkan ke user secara terverifikasi.
- **Event scope:** satu event spesifik; event finance **tidak otomatis** mengikuti jabatan owner organisasi.
- **Billing scope:** billing account organisasi; tidak sama dengan kewenangan mengakses kas IPL/sewa.

## Permission registry minimal (expansion of RBAC.md)

| Permission | Allowed scope | Eligible role/grant | Guardrail |
|---|---|---|---|
| `org.member.invite` | org | org owner/admin | Tidak boleh mengangkat last owner melalui client |
| `org.member.manage` | org | owner/admin | Audit, last-owner protection |
| `org.policy.manage` | org/platform | platform authorized admin | Effective forward, approval/sensitive restrictions |
| `hub.subscription.view` | billing/org | owner, billing_manager | No tenant private finance implied |
| `hub.subscription.manage` | billing/org | owner, billing_manager | Order server-priced, audit |
| `hub.wallet.view` | billing/org | owner, billing_manager | RLS billing account |
| `hub.wallet.topup` | billing/org | owner/billing_manager (grant) | Provider settled only |
| `hub.wallet.spend` | billing/org | owner/billing_manager (grant) | Atomic debit, consent |
| `hub.wallet.autorenew.manage` | billing/org | owner/billing_manager | Explicit opt-in |
| `kos.property.manage` | org/property | kos owner, assigned manager | Property scope |
| `kos.unit.manage` | property | assigned owner/manager/staff by grant | Unit belongs to assigned property |
| `kos.lease.read` | property | owner/manager/finance by grant | PII minimization |
| `kos.lease.read_own` | verified self lease | tenant-self | Relationship verified |
| `kos.payment.record` | property/self bill | assigned staff/finance, tenant self by policy | No gateway settlement |
| `kos.payment.verify` | property | assigned finance/manager explicit grant | Separation of duties |
| `warga.household.read_own` | verified household | warga-self | Verified relationship |
| `warga.ipl.record` | own bill or org finance | warga-self or assigned treasurer/staff | Manual only |
| `warga.ipl.verify` | org/assigned area | assigned bendahara/pengurus explicit grant | Audit and separation |
| `warga.cashbook.manage` | general financial account | explicitly assigned treasury | Not granted to event volunteers |
| `warga.event.manage` | assigned event | event_leader / scoped admin | Event ID mandatory |
| `warga.event.finance.read` | assigned event OR explicit org finance scope | event_treasurer or explicitly assigned treasury | **Not auto-granted to org owner** |
| `warga.event.finance.write` | assigned event | event_treasurer or explicit delegated grant | **Not auto-granted to org owner** |
| `warga.event.transfer` | general account + destination event | explicitly authorized two-account financial role | Check both account scopes, audit |
| `ads.listing.create` | own org/source listing | advertiser, designated source owner | Consent/privacy |
| `ads.listing.publish` | own listing + moderation | owner and assigned moderator in distinct steps | Cannot bypass moderation |
| `ads.moderate` | platform/assigned org | moderator | Cannot blindly reveal source PII |
| `file.upload` | resource-bound | linked domain actor | Private default, quota |
| `file.view` | resource-bound | verified actor/grantee | Server checks before R2 signed GET |
| `file.remove` | resource-bound | resource manager with audit | Retention/legal hold |
| `file.publish_public` | approved listing | owner consent + authorized moderator | Sanitized derivative only |
| `file.audit` | authorized support/org | narrowed audit role | No blanket file body access |

## Default grants yang **tidak boleh** disimpulkan

- Org owner memiliki administrasi organisasi dan billing sesuai policy, **bukan otomatis** jabatan bendahara event, properti lain, atau seluruh dokumen warga.
- Assigned property staff tidak melihat kontrak property lainnya.
- Warga/penyewa self tidak dapat mencari profile/kontrak orang lain berdasarkan UUID.
- Event leader **bukan** event treasurer tanpa role finance tambahan.
- Platform support/ads moderator **bukan** superuser untuk membuka dokumen tenant.
- `file_assets` metadata RLS tidak otomatis mengendalikan byte Cloudflare R2; URL dibuat oleh API setelah pemeriksaan relasi file→entity.

## Role templates (contoh default, bukan permission bypass)

| Role | Bundel contoh | Catatan |
|---|---|---|
| org_owner | org.member.*, hub.subscription.*, hub.wallet.* | Semua aksi tetap audit/step-up dan deny pada event finance tanpa assignment |
| org_admin | org.member.invite, limited product administration | Tidak otomatis manage wallet |
| billing_manager | hub.subscription.*, hub.wallet.* | Tidak membaca IPL/sewa private |
| kos_manager | kos.property/manage, kos.unit/manage, scoped lease/payment permissions | Per-property |
| kos_finance | kos.payment.record + verify | Per-property; self-approval policy perlu diputuskan |
| warga_bendahara | warga.cashbook.manage, warga.ipl.verify | Event finance memerlukan assignment eksplisit |
| event_treasurer | warga.event.finance.read/write | Event-specific only |
| platform_moderator | ads.moderate | Hanya projection untuk moderasi |
| tenant_self/warga_self | own verified resources only | Tidak mendapatkan org-wide read |

**Custom role:** setelah MVP dapat merakit subset permission, tetapi tidak bisa melewati mandatory checks, separation of duties, atau mengangkat diri sendiri.

## Pengujian negatif wajib

| Actor | Target | Hasil |
|---|---|---|
| org owner tanpa event grant | event finance | Denied |
| event treasurer A | event B / general cashbook | Denied |
| kos finance assigned property A | lease/payment property B | Denied |
| warga A | rumah/tagihan warga B | Denied |
| billing_manager | data sewa/IPL organisasi | Denied |
| platform support tanpa approval | bukti transfer di R2 | Denied |
| removed org member | semua endpoint tenant | Denied |
| forged org ID / role / scope / object key | any resource | Denied |

Rujukan: [RBAC](RBAC.md), [RLS Policy Spec](RLS-Policy-Spec.md), [Auth & SSO](Auth-and-SSO.md), [File Storage](../03-data/File-Storage.md).
