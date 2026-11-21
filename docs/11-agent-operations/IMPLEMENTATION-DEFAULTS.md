# Implementation Defaults & Safe Fallbacks — PortalHub

> **Status: DRAFT / engineering proposals, bukan keputusan produk baru.** Dokumen ini dipakai hanya ketika sumber kebenaran tidak menentukan detail teknis. Semua pilihan harus sesuai [`Decisions.md`](../00-product/Decisions.md), ADR yang *accepted*, [`Architecture.md`](../Architecture.md), [`AI-Agents.md`](../AI-Agents.md) dan [`AUTONOMOUS-DEVELOPMENT.md`](AUTONOMOUS-DEVELOPMENT.md). Baris berlabel **proposed** memerlukan ratifikasi engineering sebelum dijadikan fondasi yang sulit dibalik. **Tidak berisi credential atau nilai rahasia.**

## 1. Cara menggunakan default

Tiga kelas aturan:

- **MUST — baseline yang sudah ditetapkan di repo:** tidak boleh diganti oleh agent melalui dokumen ini.
- **PROPOSED — default engineering awal:** agent boleh membuat evaluasi/spike/ADR dan mengimplementasikan secara terbatas setelah approval integrator jika tidak mengubah keputusan produk.
- **DISABLED UNTIL APPROVED — keputusan bisnis/legal/provider:** buat interface, schema, mock dan tes, tetapi **jangan aktifkan perilaku produksi** sampai keputusan disahkan.

Pilihan default bukan alasan melewati UAT atau menganggap seluruh deployment sudah tersedia.

## 2. Stack, workspace dan frontend

| Area | Default / aturan | Kategori | Validasi yang wajib |
|---|---|---|---|
| Arsitektur domain | Modular monolith dengan batas domain dan service/API lintas domain | **PROPOSED** sesuai ADR-0001/D012; perlu ratifikasi engineering | ADR, build test, evaluasi tradeoff |
| Private app | React + Vite + Tailwind + React Router + TanStack Query, PWA | **PROPOSED** sejalan Architecture dan legacy | Routing, auth guard, security/cache test |
| Public Ads | Next.js SSR/SSG/ISR untuk HTML SEO | **PROPOSED** sejalan ADR-0001 | SSR crawlable, sitemap, published-only projection |
| Alternatif | Satu aplikasi Next.js dapat dievaluasi jika lebih sederhana | **PROPOSED**, jangan pindah tanpa ADR | Benchmark SEO, routing, maintenance, cost |
| Language | TypeScript `strict` di code baru | **PROPOSED** | `typecheck`, typed domain contracts |
| Package manager | `pnpm` workspace + lockfile pinned untuk monorepo | **PROPOSED**; bukan persyaratan existing | CI install reproducible, deployment support |
| Runtime | Node.js versi LTS yang kompatibel saat bootstrap; versi dipin dan didokumentasikan | **PROPOSED** | Build lokal/CI/Vercel konsisten |
| Format/lint | ESLint, Prettier, import boundaries lint | **PROPOSED** | CI lint/format |
| Testing | Vitest untuk unit, Playwright untuk E2E, SQL/RLS tests terpisah | **PROPOSED** | Seed sintetis; coverage kasus kritis |
| Deployment | Vercel; private PWA `/app`, `/kos`, `/warga`, public SEO `/iklan` | **PROPOSED** sesuai routing docs | Preview rewrites dan noindex private |

**Konvensi:** jika keputusan stack D012 masih bertanda *usulan teknis*, Lead tidak mengubah label menjadi *accepted* hanya karena proof-of-concept sudah berjalan. Catat hasil dan minta ratifikasi pada ADR; implementasi awal tetap bisa diisolasi dan diganti.

## 3. Identitas, tenancy dan permission (MUST)

- Supabase Auth dengan Google OAuth adalah login utama. OTP/magic link hanya pilihan jika dikonfigurasi. Berhasil login **tidak** memberikan hak akses organisasi.
- Data tenant memakai `organization_id uuid NOT NULL`; relasi sensitif memiliki FK komposit, indeks dan policy RLS yang diuji.
- Akses = login valid **dan** membership aktif **dan** product entitlement **dan** grants permission **dan** cocok resource scope **dan** mandatory checks.
- Akses tenant-self hanya melalui relasi rumah/kontrak terverifikasi; tidak cukup sekadar email sama.
- Peran event finance per-event, property staff per-property; org owner tidak otomatis boleh membaca kas event atau data yang tidak diberikan.
- RLS deny-by-default, API recheck, service-role tidak di browser. Unauthorized private data tidak boleh berkedip saat loading atau tersimpan offline.
- Login 0/1/multi konteks: tanpa org ke onboarding/undangan; satu konteks ke route yang diizinkan; banyak konteks ke selector. Context switch mengosongkan cache privat.

## 4. Database dan API (MUST + PROPOSED)

**Baseline MUST:** UUID, `timestamptz` UTC, uang sebagai `amount_minor bigint` **rupiah utuh** (nama historis, bukan sen), audit pada operasi sensitif, RLS, composite tenant constraints, append-only posting finansial, no direct browser ledger writes.

**Default engineering PROPOSED:**

- Migrations numbered dan additive-first; migration yang sudah merged immutable. SQL transaction/constraint untuk invariant yang bisa dijaga database.
- `OpenAPI.yaml` sebagai kontrak desain yang harus divalidasi dan dilengkapi per endpoint; typed client/server schemas dihasilkan dari satu kontrak bila tooling mendukung.
- API `/api/v1`, server-validated input, pagination yang konsisten, error envelope dengan `request_id`; private response `no-store`.
- `Idempotency-Key` untuk financial writes, dedup event external, replay-safe outbox. Asynchronous at-least-once delivery diimbangi idempotent consumers, tidak mengklaim queue exactly-once.
- Format tanggal penyimpanan UTC; presentasi mengikuti zona waktu organisasi, dengan `Asia/Jakarta` hanya sebagai fallback UI bila organisasi belum mengatur timezone.
- Tidak menduplikasi enum status antar frontend/backend; jika status canonical belum diputuskan, dokumentasikan proposal dan tes sebelum migration.

## 5. Billing / Kantong: jangan mengarang angka atau memproses dana riil

**MUST:** pembayaran sewa, IPL, deposit serta dana event **tidak** melewati gateway/Kantong. Pencatatan operasional melalui `cash`/`bank_transfer`, status `verified_internal` setelah pemeriksaan petugas. Gateway hanya layanan PortalHub sendiri.

Untuk layanan PortalHub:

- Semua pembelian melewati `service_orders`. Pilihan Kantong (atomic debit saldo yang sudah settled), provider direct checkout (setelah verified settlement), atau top-up exact invoice lalu **debit terpisah yang diotorisasi**.
- Saldo Kantong closed-loop, nonnegative; ledger immutable, idempotency dan audit. `Top Up`, `Transaksi`, `Payment` adalah histori terpisah.
- Auto-renew **off** secara default, tidak ada fallback charge yang tidak diotorisasi. Gratis tidak otomatis menjadi berbayar.
- **DISABLED UNTIL APPROVED:** harga produksi, paket/kuota trial, payment provider live, legal Kantong, refund, pajak, fee, grace, proration, penyelesaian saldo tidak terpakai.
- **Safe fallback:** schema + order state machine + **mock provider** + seeded test catalog; `payments_live_enabled=false`, `wallet_live_enabled=false` untuk semua environment awal. Nilai `false` adalah contoh guardrail desain, bukan klaim flag sudah ada di kode.
- Test: duplicate/out-of-order webhook, concurrent debit, exact top-up credit without debit, retry fulfillment, outbox crash, insufficient balance, permission denial.

## 6. PortalKos: default aman saat business rule TBD

- **MUST:** satu org banyak properti; kuota dihitung dari **active rentable units** gabungan, bukan jumlah properti; property-scoped staff; kontrak eksklusif tidak boleh overlap.
- Periode/nominal kontrak disimpan sebagai snapshot berversi; tagihan dibentuk idempotent berdasarkan lease/period/type.
- **DISABLED UNTIL APPROVED:** denda, prorata, potongan, biaya otomatis, refund deposit, auto-penagihan bank, kebijakan partial/overpayment, downgrade over-quota.
- **Safe fallback:** data dasar, kontrak, unit, charge manual/terjadwal hanya bila aturan periode disahkan, pembayaran eksternal tercatat dan diverifikasi internal; saat kuota lewat batas, cegah aktivasi unit baru tanpa menghapus histori/kontrak lama.
- Perubahan occupancy yang telah diverifikasi mengirim event untuk listing, bukan publish otomatis tanpa opt-in owner dan moderasi.

## 7. PortalWarga: kas event dan IPL

- **MUST:** rumah/tagihan dan akses warga sendiri terkait relasi yang diverifikasi. Kas umum dan tiap kas event adalah akun berbeda; transfer internal memasang dua posting atomik, dikecualikan dari pendapatan/beban konsolidasi.
- **DISABLED UNTIL APPROVED:** tarif IPL numerik, denda keterlambatan, diskon, masa jatuh tempo default, tutup buku, koreksi lintas periode, ketentuan warga penanggung jawab IPL.
- **Safe fallback:** tampilan dan pencatatan dengan kebijakan versi yang diinput pengurus berwenang; jangan generate atau collect iuran otomatis tanpa tarif/periode yang terotorisasi; tangguhkan rule penutupan buku yang belum disepakati.
- Migrasi legacy dilakukan read-only analysis dan dry-run sintetis lebih dulu; **jangan edit repo `kodok-ijho/PortalWarga` atau memigrasi data riil** tanpa persetujuan khusus.

## 8. PortalIklan / SEO

- **MUST:** halaman publik SSR/SEO hanya dari *approved published projection*, tanpa PII privat. Pemilik opt-in, moderasi, iklan punya expiry, dan source Kos occupied/unavailable memicu pembaruan publik yang aman.
- **DISABLED UNTIL APPROVED:** jumlah kuota gratis, durasi default, ranking/promosi berbayar, auto-renew, metode pengiklan umum, SLA moderasi/takedown, handling URL 404/410 yang tidak final.
- **Safe fallback:** schema draft/pending/moderated, preview, published projection dan automated tests; publikasi ditahan jika izin, moderasi, masa tayang, atau kuota belum dapat ditentukan secara sah. Jangan membuat angka “gratis 5 iklan 30 hari” sebagai keputusan produk.
- Tes canonical URL, sitemap publik saja, private noindex, EXIF sanitization, source vacancy sync, rate limits dan abuse moderation.

## 9. Cloudflare R2 (MUST) dan mock storage

- **MUST:** file baru di R2; Supabase PostgreSQL menyimpan metadata/izin, **tidak** file bytes. Bucket private/temp/public terpisah per environment dan akses backend credential-only.
- API: upload intent → presigned PUT via R2 S3 API → HEAD/type/size/scan → `ready`/`quarantined` → scoped signed GET. Signed URL bukan custom CDN URL.
- Hanya media listing yang mendapat consent + approval + scan + EXIF scrub diterbitkan sebagai derivatif di public bucket.
- Private R2 object/URL tidak ada di cache PWA, HTML Ads, log, email, atau analytics. Backup DB **dan** R2 diuji bersama.
- **PROPOSED untuk dev/test:** implementasikan `StorageService` interface dengan fake/in-memory object store untuk unit/integration test; R2 sungguhan hanya saat lingkungan terisolasi sudah diotorisasi. **DISABLED UNTIL APPROVED:** retensi numerik, kuota/ukuran per paket, provider scanner, data residency, storage cleanup destructive production.

## 10. Feature flags & environment

Gunakan tiga environment terpisah (`development`, `staging`, `production`), terpisah pula database, buckets, provider callbacks dan secrets. Tidak ada credential yang disimpan dalam repo/docs/log.

**PROPOSED** flag awal (nama hanya contoh, bukan fitur yang sudah berjalan):

```yaml
flags:
  payments_live_enabled: false
  wallet_live_enabled: false
  public_ads_publish_enabled: false
  production_file_upload_enabled: false
  legacy_migration_live_enabled: false
```

Flag **tidak mengganti** izin backend/RLS, legal review, atau release approval. Flag hanya gate tambahan. Hanya pemilik otorisasi yang sesuai yang boleh mengaktifkan produksi setelah semua tes dan keputusan disahkan.

## 11. Kriteria mengubah default menjadi keputusan

1. Jelaskan masalah dan opsi, termasuk alternatif yang sudah disebut dalam ADR/Architecture.
2. Ukur bila relevan (build, deploy, SEO SSR, DX, biaya, RLS/security).
3. Buat perubahan ADR atau decision record, cantumkan dampak migration/rollback serta requirement ID.
4. Dapatkan persetujuan engineering (dan product owner bila mengubah produk/kontrak/kebijakan).
5. Update docs, OpenAPI/types/migration/test dan traceability.
6. Jika perubahan mengubah accepted decision, jangan merge sampai otorisasi yang sama telah diberikan.

**Ingat:** angka contoh di fixture/mock/test bukan harga, kuota, atau periode yang boleh muncul sebagai janji produk produksi.