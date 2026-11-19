# MVP, release gates & prioritization

## MVP 0: SaaS core + PortalKos private

P0: auth multi-org, membership + roles, configurable onboarding basic, properties/units/leases, catat pembayaran cash/transfer, owner dashboard, subscription order + direct QRIS/transfer, Kantong top-up/debit, audit dan RLS. Subscription baru aktif setelah provider settled.

## MVP 1: PortalIklan publik

P0: SSR catalog/listing, moderasi, kategori/area, approval publish, expiry, free quotas, basic sitemap. P1: lead/contact, listing Kos sync. Tidak membangun checkout pembeli/penjual.

## MVP 2: Integrasi kos → iklan

P0: publish kamar kosong opt-in, auto-status saat terisi, kuota iklan. P1: paket promosi, auto-renew iklan.

## MVP 3: Migrasi PortalWarga → iklan warga

P0: auth/org migration, rumah/warga/IPL pencatatan, event finance, iklan usaha warga opt-in. Wajib regression test laporan keuangan legacy.

## MVP 4: Monetisasi dan scale

Paket berbayar, analytics, public advertiser onboarding, custom roles advanced, SEO growth.

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
