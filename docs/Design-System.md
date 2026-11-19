# Design System — PortalHub

**Status:** v0.1 — UI design specification, bukan stylesheet yang sudah aktif. **Tema:** Clean Minimal × Mobile First.

## Prinsip desain

- **Clear before clever:** satu layar menjawab kebutuhan terpenting per persona.
- **Progressive disclosure:** aksi sederhana terlihat lebih dahulu, filter/report lanjutan dibuka saat dibutuhkan.
- **Adaptive, not separate products:** komponen bisnis sama, presentasi mobile/desktop berbeda.
- **Accessible by default:** keyboard navigation, screen reader labels, focus visible, contrast audit, touch target minimal 44×44 CSS px.
- **Trustworthy finance:** nominal, periode, status dan sumber verifikasi tampil jelas; bedakan pembayaran operasional tercatat vs layanan PortalHub terbayar.

## Tokens (usulan awal)

| Token | Value | Pemakaian |
|---|---|---|
| `color.brand.500` | `#6D4AFF` | CTA, active tab, focus |
| `color.text.primary` | `#111827` | Heading/body |
| `color.text.muted` | `#6B7280` | Meta, caption |
| `color.canvas` | `#F8FAFC` | App background |
| `color.surface` | `#FFFFFF` | Card, dialog |
| `color.border` | `#E5E7EB` | Stroke |
| `color.success` | `#15803D` | Verified/success |
| `color.warning` | `#B45309` | Pending/warning |
| `color.danger` | `#B91C1C` | Rejected/error |
| `radius.card` | `16px` | Card |
| `radius.input` | `12px` | Inputs |
| `shadow.card` | subtle | Tidak berlebihan |
| `font.ui` | Inter / Plus Jakarta Sans | Fallback system-ui |

> Lakukan kontras terukur (WCAG AA) pada kombinasi warna final; status **tidak boleh hanya dibedakan warna**.

## Layout

| Viewport | UI |
|---|---|
| Small/mobile (<768px, usulan) | Header ringkas, kartu 1–2 kolom, bottom navigation 4–5 item, tombol aksi utama mudah dijangkau, filter di bottom sheet |
| Tablet (768–1023px) | Grid 2–3 kolom, collapsible sidebar atau bottom nav sesuai kebutuhan |
| Desktop (>=1024px) | Sidebar, toolbar dan filter terlihat, KPI 4–6, grafik, tabel density normal, detail split-view |

Breakpoint ini **token desain**, bukan aturan bisnis atau otorisasi. Jangan sembunyikan fitur penting hanya karena ukuran layar; sediakan jalur lewat menu lainnya.

## Navigasi produk

- **PortalHub**: `Portal Saya`, `Organisasi`, `Langganan`, `Kantong`, `Profil`.
- **PortalKos mobile**: `Beranda`, `Properti`, `Tambah`, `Tagihan`, `Lainnya`; konten mengikuti role.
- **PortalWarga mobile**: `Beranda`, `IPL`, `Event`, `Iklan`, `Lainnya`; role warga dan pengurus dapat berbeda.
- **PortalIklan publik**: pencarian dan lokasi di atas, kategori horizontal, listing cards, detail SEO.
- Untuk role tunggal masuk langsung ke portal; banyak akses tampilkan selector. Return URL harus divalidasi.

## Komponen standar

`AppShell`, `OrganizationSwitcher`, `ProductSwitcher`, `BottomNav`, `Sidebar`, `PageHeader`, `KPICard`, `DataTable`, `MobileListCard`, `StatusBadge`, `SearchFilter`, `MoneyField`, `EvidenceUploader`, `ConfirmDialog`, `AuditTimeline`, `EmptyState`, `LoadingSkeleton`, `OfflineBanner`, `ExpiryCountdown`, `WalletHistoryTabs`, `SubscriptionCard`, `ListingCard`.

**Status label standar**: `Draft`, `Menunggu verifikasi`, `Terverifikasi internal`, `Ditolak`, `Aktif`, `Berakhir`, `Tidak tersedia`, `Dibatalkan`. Hindari label “pembayaran terjamin” untuk sewa/IPL.

## Screen inventory

1. Landing; login; accept invitation; chooser organisasi+produk; pengaturan profil.
2. Admin platform: organisasi, policy, verifikasi, produk, paket, subscription, payment reconciliation, moderation, audit.
3. Kantong: saldo, Top Up, Transaksi, Payment, top-up form, invoice detail, auto-renew toggles.
4. Kos: dashboard konsolidasi, properties, units, tenants, leases, charges, payment recording, expenses, reports, listing publish.
5. Warga: dashboard, units/houses, residents, IPL matrix, payment proof, general cashbook, events, event cashbook, documents, businesses.
6. Iklan: homepage, category/city SEO, detail, contact CTA, listing form, moderation, expiry/renewal.

## Pengalaman inti

**Pembayaran operasional**: `Catat pembayaran` → pilih tunai/transfer → lampirkan bukti bila ada → `Menunggu verifikasi` → finance verifies/rejects → laporan. Jangan tampilkan tombol payment gateway.

**Bayar subscription**: order → pilih `Bayar dengan Kantong`/`QRIS`/`Transfer`/`Isi Kantong sejumlah tagihan` → verified → subscription active. Tampilkan expiry dan invoice.

**Iklan**: detail foto, judul, harga bila relevan, ketersediaan, area, kontak yang disetujui, informasi promo berlabel; jangan expose detail alamat privat otomatis.

## PWA

- Install manifest, icons 192/512+maskable, splash yang disediakan OS, update notification, offline fallback.
- Cache asset statis; **jangan cache** halaman sensitif, token, atau response tenant secara publik/shared. Hapus private cache saat logout/ganti org.
- Operasi finansial dan perubahan kontrak **online-only** dalam MVP. No optimistic success untuk pembayaran.

## Copy dan notifikasi

Gunakan Bahasa Indonesia yang jelas, contoh: “Pembayaran dicatat dan menunggu pemeriksaan bendahara.”; “Saldo Kantong tidak cukup untuk perpanjangan.”; “Iklan berakhir 3 hari lagi.” Gunakan format uang `Rp 100.000`, waktu lokal Asia/Jakarta dengan UTC di database.

## Definition of done UI

Responsif diuji pada lebar 320, 375, 768, 1024, 1440; tidak ada horizontal scroll tak sengaja; form keyboard accessible; error loading/empty/offline; unit dan role diuji; audit visual manual dan Lighthouse diperiksa di CI bila memungkinkan.