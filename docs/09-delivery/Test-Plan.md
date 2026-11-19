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


## Cloudflare R2 — storage UAT

| ID | Test | Expected |
|---|---|---|
| STO-01 | Tenant A meminta signed GET/PUT untuk file tenant B | 403/no signed URL |
| STO-02 | Staff properti A akses kontrak/bukti properti B | Denied |
| STO-03 | Panitia event A mengunduh lampiran event B | Denied |
| STO-04 | File berlebih, MIME palsu, malware, checksum salah | Rejected/quarantine, tidak `ready`, tidak public |
| STO-05 | Upload orphan atau intent expired | Cleanup idempotent, kuota released |
| STO-06 | 2 upload paralel di batas kuota | Tidak dapat melampaui reservasi kuota |
| STO-07 | Signed URL private expired / permission revoked | Tidak ada URL baru setelah revoke; URL lama expired sesuai TTL, tidak cached |
| STO-08 | Gambar listing masih draft/rejected | Tidak dapat diakses di public media bucket atau SEO HTML |
| STO-09 | Media iklan published kemudian takedown | Sanitized, EXIF GPS removed, CDN invalidation/revocation diuji |
| STO-10 | Restore Supabase DB + R2 object backup | File dan metadata cocok (checksum/link/audit) |
| STO-11 | Upload bukti `ready` | Payment tetap pending internal verification hingga petugas approve |
| STO-12 | R2 secret di frontend bundle/telemetry | Security check gagal; credential hanya server |

Browser CORS dan S3 presigned hostname harus diuji di staging; jangan menggantungkan tes izin hanya pada RLS metadata. [File Storage](../03-data/File-Storage.md).


## Tambahan verifikasi audit spesifikasi

| ID | Test | Hasil wajib |
|---|---|---|
| AUTH-01 | Google OAuth callback dengan unsafe return path | Ditolak, tidak open redirect |
| AUTH-02 | User baru login tanpa membership | Onboarding only, no tenant data |
| AUTH-03 | Invitation token replay/expired/email mismatch | Ditolak dan diaudit |
| RBAC-01 | Org owner tanpa event-specific grant membaca kas event | Denied (bukan implicit owner grant) |
| RLS-01 | Forbidden SELECT/INSERT/UPDATE/DELETE lintas org/property/event | Denied server+DB |
| RLS-02 | Client mengubah organization_id atau role assignment | No privilege escalation |
| DB-01 | Cross-tenant FK injected into lease/account/file | DB constraint rejects |
| BILL-01 | Bayar subscription dari Kantong yang sudah funded | Atomic debit + entitlement once **tanpa webhook provider baru** |
| BILL-02 | Direct provider payment settled | Verified webhook + fulfillment once |
| BILL-03 | Exact top-up succeeds but wallet spend fails | Top-up credit retained, no unauthorized charge |
| BILL-04 | Double webhook, parallel renew, timeout after ledger commit | At-most-one posting, recoverable via outbox |
| ADS-01 | Unit occupied and listing published | Durable unavailable sync, no misleading vacancy claim |
| OPS-01 | Duplicate jobs, dead-letter recovery | Idempotent side effect, visible incident trail |
| DR-01 | Restore Supabase database and R2 objects | Links/checksums/auth/quota consistent |

Coverage mapping: [Requirements Traceability](Requirements-Traceability.md). Draft API [OpenAPI](../08-operations/OpenAPI.yaml) needs schema/lint and contract tests after implementation. All rows currently **planned**, not executed.
