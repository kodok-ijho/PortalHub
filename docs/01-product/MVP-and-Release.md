# MVP, release gates & prioritization

## MVP 0: SaaS core + PortalKos private

P0: auth multi-org, membership + roles, configurable onboarding basic, properties/units/leases, catat pembayaran cash/transfer, owner dashboard, subscription order + direct QRIS/transfer, Kantong top-up/debit, audit dan RLS. Subscription baru aktif setelah **pembayaran direct terkonfirmasi settled oleh provider ATAU debit Kantong yang saldonya sudah settled berhasil secara atomik**; aktivasi idempotent. Pembelian dengan saldo Kantong tidak memerlukan webhook provider baru.

## MVP 1: PortalIklan publik

P0: SSR catalog/listing, moderasi, kategori/area, approval publish, expiry, free quotas, basic sitemap. P1: lead/contact, listing Kos sync. Tidak membangun checkout pembeli/penjual.

## MVP 2: Integrasi kos → iklan

P0: publish kamar kosong opt-in, auto-status saat terisi, kuota iklan. P1: paket promosi, auto-renew iklan.

## MVP 3: Migrasi PortalWarga → iklan warga

P0: auth/org migration, rumah/warga/IPL pencatatan, event finance, iklan usaha warga opt-in. Wajib regression test laporan keuangan legacy.

## MVP 4: Monetisasi dan scale

Paket berbayar, analytics, public advertiser onboarding, custom roles advanced, SEO growth.

## Pemetaan MVP ke fase roadmap (bukan urutan baru)

Pemetaan berikut menjelaskan **cakupan**; urutan dan acceptance gate tetap mengikuti [Roadmap.md](../09-delivery/Roadmap.md).

| Kelompok release | Fase roadmap terkait | Keterangan |
|---|---|---|
| Fondasi lintas MVP | 0 | Workspace, CI, Supabase auth/RLS, kontrak API, security baseline |
| MVP 0 — Core + PortalKos | 1–2 | Billing fase 1 boleh dibangun dengan mock; aktivasi uang riil tetap tertahan approval; PortalKos private fase 2 |
| MVP 1 — PortalIklan publik | 3 | SEO, moderasi, free quotas berdasarkan nilai yang telah disetujui |
| MVP 2 — Kos → Iklan | 4 | Opt-in, sinkron status ketersediaan |
| MVP 3 — Warga dan iklan warga | 5–6 | Migrasi/reconciliation Warga lebih dahulu, kemudian integrasi iklan |
| MVP 4 — Monetisasi & skala | 7 | Paket/promosi/pengiklan publik setelah keputusan legal, produk, operasi |

**Aturan dependensi:** penyebutan fitur dalam MVP bukan otorisasi untuk melewati fase roadmap. Fitur monetisasi/platform payment yang berisiko dapat diuji secara mock di fase awal namun **tidak boleh live** sebelum approval terkait; jika release gate itu belum terpenuhi, laporkan milestone sebagai partial/blocked, bukan menandainya selesai.

## Fitur ditunda

Escrow, payment gateway untuk sewa/IPL, dompet transfer P2P, mobile native, booking property otomatis, dynamic pricing/AI recommendations. Tidak ada angka harga atau jaminan rangking SEO dalam MVP.

## Release gates

1. Cross-tenant RLS/authorization negative tests hijau.
2. Gateway webhook replay/invalid signature/race tests hijau.
3. Backups tested + rollback runbook.
4. Budget/reports event and manual payment reconciliation tested.
5. PWA offline privacy + SEO public HTML validated.


## Storage release gate (P0 lintas produk)

Sebelum mengaktifkan unggahan bukti transfer/kontrak/dokumen, wajib ada R2 private/temp bucket terisolasi per environment, backend API otorisasi signed PUT/GET, tabel `file_assets`/RLS, scan/quarantine, kuota, cleanup orphan dan backup restore DB+R2. Media iklan publik punya bucket dan moderation tersendiri.

Gate produksi: negative tests lintas org/property/event, presigned URL expiry, file MIME/size/malware, public-leak, quota racing, retention & restore berhasil. Lihat [File Storage](../03-data/File-Storage.md).


## Implementation dependency gates (audit follow-up)

Fase auth/tenancy memerlukan [Auth & SSO](../04-security/Auth-and-SSO.md), [Permission Matrix](../04-security/Permission-Matrix.md), [RLS Policy Spec](../04-security/RLS-Policy-Spec.md) dan [Database Schema](../03-data/Database-Schema.md). Billing harus mengikuti [Subscription Lifecycle](../05-billing/Subscription-Lifecycle.md) dan [Payment State Machines](../05-billing/Payment-and-Wallet-State-Machines.md) sebelum live checkout. Fase produk mengacu ke rules PortalKos, Warga Finance, Ads Publishing, serta [Requirements Traceability](../09-delivery/Requirements-Traceability.md). Semua masih rancangan sampai ada implementasi/tes nyata.
