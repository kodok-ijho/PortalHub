# Development Setup — PortalHub (Blueprint)

**Status:** persiapan developer P0; **repository saat ini hanya berisi dokumentasi, belum source code yang dapat dijalankan**. Jangan menampilkan perintah seolah aplikasi sudah bisa dimulai. **Bagian credentials, akses akun, key dan secret sengaja tidak disertakan.**

## Target struktur monorepo (belum dibuat)

```text
apps/
  hub-web/              # React/Vite PWA: /app, /warga, /kos
  ads-web/              # Next.js SSR: /iklan
packages/
  ui/                   # Shared components
  auth/                 # Login context & permission interfaces
  contracts/            # API schemas/types
  config/               # Tooling (non-sensitive)
services/
  billing/
  notifications/
supabase/
  migrations/
  tests/
  seed/
docs/
```

Struktur ini masih **usulan arsitektur**, bukan klaim folder tersebut sudah ada. Keputusan apakah tetap dua deployables atau satu Next.js app harus dievaluasi lewat ADR-0001.

## Urutan bootstrap yang disarankan

1. Pilih package manager/workspace dan runtime Node LTS sesuai kompatibilitas dependency **pada waktu implementasi**; pin versi di repository dan lockfile. Belum ada perintah package manager yang dapat dijamin berjalan.
2. Buat workspace monorepo, tooling lint/format/typecheck/test, React app privat, Next.js public app, dan shared packages.
3. Siapkan tiga environment logis terisolasi: dev, staging, production. Pemisahan juga berlaku untuk Supabase project, Cloudflare R2 buckets, payment provider test/live, dan deployment target.
4. Definisikan kontrak konfigurasi **non-secret**: domain publik, site origin, timezone display `Asia/Jakarta`, feature flags, product codes, dan redirect/callback allowlists.
5. Migrasi database Supabase secara additive dengan RLS deny-by-default, lalu uji negative cross-tenant sebelum mengaktifkan fitur.
6. Bangun login Google OAuth dan context selector, lalu API server authorization. Implementasi login aktif memerlukan setup integrasi oleh pemilik infrastruktur di luar dokumen ini.
7. Bangun R2 storage adapter serta upload proof UI, tapi nonaktifkan upload production sampai scan/permissions/quota/backup lulus.
8. Integrasikan provider payment hanya setelah model legal, provider contract, webhook signature verification dan reconciliation disetujui.

## Kontrak development (ketika source tersedia)

| Concern | Acceptance |
|---|---|
| Workspace | Lint, typecheck, unit test dan build scripts tersedia serta berjalan di CI |
| Database | Migration forward, seed sintetis, negative RLS tests dan rollback plan |
| Auth | OAuth redirect aman, 0/1/multi-context, revoke session/member |
| Private PWA | Logout/context switch menghapus cache data tenant; offline tidak mengungkap PII |
| Public ads | SSR HTML SEO, published projection only, no private documents |
| Billing | Mock provider callback dan wallet tests, tanpa real financial charges |
| R2 | Mock object store, upload intents, scan/quarantine, RLS metadata, object restore testing |
| CI/CD | Staging smoke, review release gate, rollback |
| Secrets | **Tidak didokumentasikan di sini**; integrasi produksi dilakukan lewat pengelola infrastruktur yang berwenang |

## Development data & tooling policy

- Semua seed/test data **sintetis**; jangan memasukkan data warga, penyewa, pembayaran atau dokumen asli ke development/CI.
- Stub/mock pembayaran harus jelas membedakan `provider_settled` dari `verified_internal` pembayaran operasional.
- Test storage menggunakan bucket terisolasi dan objek sintetis; jangan memakai aset production.
- GitHub Actions/CI baru dapat dirancang setelah code/workspace ada. Hindari status palsu "CI passed" ketika belum tersedia.
- Setiap PR dokumentasi/implementasi memperbarui [Requirements Traceability](../09-delivery/Requirements-Traceability.md) jika requirement berubah.

## Checklist sebelum "first run" diumumkan

- [ ] Monorepo files dan lockfile benar-benar ada.
- [ ] Dependensi di-install sesuai README paket.
- [ ] Migration schema serta RLS tests sudah ada dan lolos.
- [ ] Auth callback dan API gateway tersedia secara aman.
- [ ] Ada instruksi start lokal yang diuji pada lingkungan development.
- [ ] File storage dan payment mock terisolasi dan security checks lulus.
- [ ] CI and smoke test link tercantum; unsupported features diberi label.

**Rujukan:** [Architecture](../Architecture.md), [Auth & SSO](../04-security/Auth-and-SSO.md), [Database Schema](../03-data/Database-Schema.md), [File Storage](../03-data/File-Storage.md), [DevOps Runbook](DevOps-Runbook.md).
