# File Storage — Cloudflare R2

**Status: Disepakati (19 November 2026).** Berlaku untuk PortalHub Core, PortalWarga, PortalKos, dan PortalIklan.

**Keputusan:** semua file baru memakai **Cloudflare R2**. **Supabase Auth** menangani login Google; **Supabase PostgreSQL + RLS** menangani metadata, organisasi, role, scope, audit, kuota. **RLS tidak otomatis melindungi object R2**. Backend wajib mengecek otorisasi sebelum memberi akses objek. Baca [ADR-0003](../10-decisions/ADR-0003-cloudflare-r2.md).

## 1. Bucket dan isolation

Pisahkan *per environment* (dev/staging/prod) dan secret aksesnya; nama di bawah berupa desain, bukan resources yang sudah dibuat.

| Logical bucket | Policy | Isi |
|---|---|---|
| `portalhub-{env}-private` | private, tanpa custom public domain | Bukti transfer IPL/sewa/event, kontrak, identitas, dokumen pengurus, file billing platform |
| `portalhub-{env}-temp` | private | Upload belum diproses, karantina, pemrosesan gambar |
| `portalhub-{env}-public` | public hanya setelah approval | Foto listing, foto properti disetujui, logo publik |

Contoh object key tanpa data pribadi pada path:

```text
organizations/{org_uuid}/warga/payments/{payment_uuid}/{file_uuid}.pdf
organizations/{org_uuid}/warga/events/{event_uuid}/{file_uuid}.pdf
organizations/{org_uuid}/kos/leases/{lease_uuid}/{file_uuid}.pdf
organizations/{org_uuid}/kos/payments/{payment_uuid}/{file_uuid}.jpg
listings/{listing_uuid}/{image_variant_uuid}.webp
uploads/{upload_uuid}/{random_uuid}
```

**Object key dan prefix bukan security boundary**. Jangan gunakan nama asli/NIK/email untuk key. Upload privat tidak boleh diberikan public URL; foto publik dibuat sebagai *derivative* setelah consent, moderasi, scanning dan penghilangan metadata EXIF sensitif.

## 2. Metadata Supabase

Rancangan logical (migrasi SQL masih perlu disusun):

- `file_assets`: `id uuid`, `organization_id`, `bucket_name`, `object_key`, `original_filename`, `mime_type`, `size_bytes`, `checksum_sha256`, `classification`, `visibility`, `status`, `uploaded_by`, `created_at`, `deleted_at`, `retention_policy_key`, `retention_until`.
- Status: `pending_upload` → `uploaded` → `scanning` → `ready`, atau `rejected`/`quarantined`/`deleted`.
- `file_links`: file terhubung ke pembayaran, kontrak, event, rumah atau listing berdasarkan whitelist jenis entitas dan pemeriksaan pemilik org+resource; untuk data sensitif utamakan foreign key dan invariant lintas tenant yang dapat diuji.
- `file_upload_intents`: masa berlaku, idempotency, expected type/size dan reserved quota; **tidak** menyimpan URL bertanda tangan.
- `file_access_audit`: actor, asset, action, request ID dan waktu; tidak merekam token URL maupun isi dokumen.
- Bila perlu, `file_versions` untuk revisi dokumen dengan objek baru, bukan overwrite diam-diam.

RLS: default deny, active membership, product entitlement, permission + property/household/event scope. Public ads hanya membaca approved public projection. API tetap memverifikasi scope sebelum meminta presigned URL R2.

## 3. Workflow unggah file

```mermaid
sequenceDiagram
 participant U as Browser/PWA
 participant API as PortalHub API
 participant DB as Supabase Postgres
 participant R2 as Cloudflare R2
 participant W as Scanner/Worker
 U->>API: POST /api/v1/files/upload-intents
 API->>DB: Check member, resource, type, quota; create pending
 API-->>U: Asset ID + short-lived presigned PUT URL
 U->>R2: PUT via R2 S3 API hostname
 U->>API: POST /api/v1/files/{id}/complete
 API->>R2: HEAD/verify object, size, type
 API->>W: Scan malware, content, sanitize if image
 W->>DB: ready OR quarantined/rejected
```

1. API mengautentikasi Supabase session dan memeriksa organisasi/role/entitlement/resource. Server membuat key acak; client tidak bebas menentukan bucket/key.
2. Reservasi kuota dilakukan secara atomik agar upload bersamaan tidak melampaui batas; return presigned **PUT** dengan expiry pendek.
3. Browser upload langsung ke **R2 S3 API**, bukan domain media publik. Konfigurasi bucket CORS origin/metode/header yang dibutuhkan; **CORS bukan autentikasi**.
4. Setelah `complete`, backend sendiri mengecek objek, ukuran sebenarnya, MIME dari isi (bukan hanya ekstensi/Content-Type), checksum jika digunakan, dan scan malware. File `ready` saja boleh dipakai sebagai lampiran yang dipercaya.
5. Kegagalan, upload terputus, intent kedaluwarsa, dan file orphan ditangani dengan cleanup worker idempotent serta pengembalian reservasi kuota. Quarantine tidak boleh tampil di halaman publik.
6. Bukti transfer yang lolos scan **bukan** bukti dana bank telah diterima. Status pembayaran `verified_internal` tetap aksi bendahara terpisah.

**Batas awal untuk dibahas, bukan harga/kuota final:** bukti JPG/PNG/WebP/PDF 5 MB; dokumen PDF 10–25 MB; foto iklan ditranscode dan thumbnail. Kuota diset per organisasi/paket dan kategori file; aturan file type/size tetap configurable.

## 4. Download dan media publik

**Private download:** `POST /api/v1/files/{id}/download` → cek membership+scope+status `ready` → terbitkan presigned **GET** R2 S3 URL berumur singkat (mis. 60 detik, sebagai usulan), atau authenticated proxy untuk kasus sensitif. Signed URL adalah bearer capability: setelah diterbitkan dapat dipakai penerima sampai expiry, jadi jangan masukkan ke log, browser analytics, referer, cache publik, CDN, atau PWA offline. Pencabutan role mencegah penerbitan URL baru tetapi tidak menjamin pencabutan URL lama sebelum expiry.

**Public listing media:** perlu consent pemilik, lolos moderation/scan, scrub EXIF GPS, render versi optimal WebP/AVIF bila sesuai; lalu salin ke bucket **public** menggunakan object key berversi. Gunakan **custom domain Cloudflare** (contoh usulan `media.portalhub.id`) untuk CDN produksi, bukan `r2.dev`. **R2 presigned S3 URLs hanya bekerja pada S3 API hostname, bukan custom domain**. Saat listing takedown/unpublish, lakukan penghapusan akses publik dan cache invalidation sesuai kebijakan; URL terlanjur tersebar mungkin tidak dapat langsung ditarik dari luar.

## 5. Retention, backup, operations

- Setiap kategori file perlu retention policy dan jalur legal hold serta penghapusan data yang sah; **jangan** menghapus bukti keuangan otomatis saat status pembayaran berubah.
- Soft delete metadata dan hapus objek melalui worker sesuai policy, audit, dan retry idempotent; jangan menggantungkan proses hanya pada tombol UI.
- Backup **PostgreSQL metadata** dan **R2 object bytes** secara terpisah; uji restore bersama berdasarkan manifest, checksum dan referensi; database backup saja tidak memulihkan file.
- Pantau GB-month, operasi R2, upload gagal, layanan transformasi gambar, Workers/CDN jika dipakai. R2 tidak memungut biaya egress R2, tetapi storage dan operasi tetap berbiaya; jangan hardcode kuota/harga produksi.
- Bucket/credentials development, staging, production harus terisolasi; secret disimpan hanya di server. Usulan env: `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_PRIVATE_BUCKET`, `R2_TEMP_BUCKET`, `R2_PUBLIC_BUCKET`; **jangan** gunakan prefix `VITE_` atau `NEXT_PUBLIC_` untuk credential.
- Buat `StorageService` adapter backend: `createUploadIntent`, `finalizeUpload`, `createPrivateDownload`, `publishMedia`, `deleteObject`, `getStorageUsage`. R2 SDK dipakai server-only. Backup/restore, malware scanning vendor, lokasi data, periode retensi dan angka kuota **belum final**.

## 6. Tests dan definition of done

- Tenant A tidak bisa mengakses file tenant B, termasuk dengan menebak asset UUID, entity ID, bucket/key.
- Staff Kos A tidak dapat mengunduh dokumen Kos B; panitia event A tidak dapat melihat bukti event B.
- Intent/complete salah actor, expired signed URL, invalid CORS origin, oversized MIME mismatch/malware, quota racing upload → ditolak tanpa kebocoran.
- File pending/rejected tidak dapat diakses atau dipublikasikan sebagai file siap; listing draft/unpublished tidak memaparkan URL file privat atau object temp.
- Public image tidak mengandung EXIF lokasi; takedown menangani cache; PWA tidak menyimpan file privat/signed URL.
- Orphan cleanup & delete idempotent; restore database+R2 mengembalikan file tepat beserta metadata dan audit.
- Upload bukti tidak memicu gateway IPL/sewa; status upload dan verifikasi pembayaran tetap terpisah.

## 7. Rujukan Cloudflare resmi

- [Presigned URLs](https://developers.cloudflare.com/r2/api/s3/presigned-urls/)
- [Public buckets & custom domains](https://developers.cloudflare.com/r2/buckets/public-buckets/)
- [Configure CORS](https://developers.cloudflare.com/r2/buckets/cors/)
- [Upload objects](https://developers.cloudflare.com/r2/objects/upload-objects/)
- [R2 pricing](https://developers.cloudflare.com/r2/pricing/)
