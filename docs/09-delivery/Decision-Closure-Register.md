# Decision Closure Register — tanpa menebak kebijakan PortalHub

> Dokumen kerja untuk menutup open decisions di [Requirements Traceability](Requirements-Traceability.md) dan [Decisions](../00-product/Decisions.md). **Belum ada keputusan bisnis baru yang disetujui** melalui dokumen ini. Semua angka business/pricing sengaja tidak ditentukan. Prioritaskan status dan pemilik keputusan agar worker tetap bergerak dengan aman.

| ID | Pertanyaan yang harus diputuskan | Pihak yang perlu menyetujui | Default aman saat menunggu | Dampak |
|---|---|---|---|---|
| DEC-ARCH / D012 | Dua deployable Vite PWA + Next.js ads, atau satu Next.js? runtime, workspace, package manager | Engineering lead / product owner bila mengubah kapabilitas/biaya | Spike kedua opsi; tidak mengunci folder besar sebelum ADR | Fase 0 bootstrap |
| DEC-URL / D013 | Domain publik, deployment routing, batas cookie/session | Owner infra + engineering | Path design saja, tanpa klaim domain live | Login dan SEO production |
| DEC-PRICE / D014 | Harga paket, kuota gratis, storage/unit/ads, trial, grace, proration | Product owner | Data model konfigurasi dan fixture test; checkout/live paid off | Entitlement, billing, publish |
| DEC-PAY / D015 | Payment provider, legal Kantong/prabayar, pajak, refund/unused balance, SLA | Product owner + legal/payment/compliance | Mock-only, no live wallet/charge | Billing live/release |
| DEC-ORG | Default org wallet vs personal wallet; verifikasi kepengurusan Warga | Product owner/security | Org-owned billing account, pending approval untuk jabatan Warga | Onboarding/finance |
| DEC-KOS | Denda/prorata/deposit, due date, partial/overpayment, overlap exceptions dan downgrade overquota | Product owner/domain | Manual records/verified_internal; fee auto disabled; no history deletion | Kos invoices/deposits |
| DEC-WARGA | IPL tariff & effective period, koreksi/tutup buku, transfer approval dan klasifikasi akun | Product owner/domain | Kebijakan input pengurus berversi; tanpa auto charge | Warga finance |
| DEC-ADS | Quota/durasi/expiry, approval SLA, ranking/promotion, removal URL, public advertiser rights | Product owner/domain | Draft/moderation, no publish bila mandatory policy belum ada | Ads public |
| DEC-DATA | Retensi/delensi/hold, file size/storage quotas, geographic handling, backups | Owner privasi/legal + ops | Private default, no destructive purge, synthetic-only data | Storage/release |
| DEC-OPS | SLO/monitoring, RPO/RTO, incident priority, restore, backups | Owner operasional | Tulis runbook + jalankan restore drill non-production; no SLO claim | Production |

## Proses menutup keputusan

1. Catat issue `decision-needed`, requirement/risiko/dependensi dan dua atau lebih opsi beserta konsekuensinya.
2. Agent boleh mengusulkan **rekomendasi**, bukan mengubah status `approved` sendiri untuk kelas C/D.
3. Setelah ada approval yang dapat dilacak, perbarui `Decisions.md` / ADR, domain doc, OpenAPI, tests, dan `Requirements-Traceability.md`.
4. Keputusan yang menambah kemampuan sensitif, memproses PII/dana, atau berdampak produksi memerlukan ratifikasi pihak berwenang. Tidak berlaku auto-approve atas batas waktu diam.
5. Ticket independen yang tidak tersentuh keputusan dapat terus dikerjakan; ticket terdampak diberi `blocked`, `mock-only`, atau `partial` yang eksplisit.

## Prioritas untuk meminimalkan pertanyaan pemilik

- **Sebelum bootstrap penuh:** putuskan DEC-ARCH, cukup satu ratifikasi engineering tentang bentuk monorepo.
- **Sebelum finalisasi domain:** batch DEC-KOS, DEC-WARGA, DEC-ADS menjadi satu sesi product review dengan default dan opsi.
- **Sebelum produksi:** batch DEC-PRICE, DEC-PAY, DEC-DATA, DEC-OPS, DEC-ORG sesuai tanggung jawab. Tidak menunda fondasi teknis yang terisolasi.
