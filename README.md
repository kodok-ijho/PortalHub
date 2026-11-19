# PortalHub — Product & Engineering Documentation

**Versi:** 0.1 (baseline desain) · **Tanggal:** 19 November 2026 · **Status:** Draft untuk implementasi, bukan klaim implementasi berjalan.

PortalHub adalah ekosistem SaaS multi-tenant dengan PortalWarga, PortalKos, PortalIklan, serta Kantong/billing untuk membeli **layanan PortalHub sendiri**.

## Baca dahulu

| Dokumen utama | Kegunaan |
|---|---|
| [PRD.md](docs/PRD.md) | Kebutuhan produk, user stories, acceptance criteria |
| [Design-System.md](docs/Design-System.md) | Design tokens, layout desktop/mobile, aksesibilitas |
| [Architecture.md](docs/Architecture.md) | Komponen teknis, integrasi, deployment, isolasi tenant |
| [AI-Agents.md](docs/AI-Agents.md) | Aturan AI coding agent dan definisi selesai |
| [docs/README.md](docs/README.md) | Indeks dokumen pelengkap |

## Keputusan produk yang sudah disepakati

1. Satu akun bisa masuk ke beberapa organisasi dengan role berbeda per organisasi, produk, dan resource.
2. PortalKos dapat mengelola banyak properti dalam satu organisasi; kuota dihitung dari total unit sewa aktif.
3. PortalWarga mendukung IPL, rumah/warga, dokumen, event, **kas utama dan kas event terpisah**.
4. PortalIklan adalah katalog publik SEO-friendly. Pengiklan awal dari PortalKos, lalu PortalWarga, masyarakat umum menyusul. Transaksi pembeli/penjual di luar platform.
5. IPL, sewa, iuran event dan transaksi iklan pihak ketiga hanya dicatat sebagai tunai/transfer dan bukti pembayaran (verifikasi internal), **bukan diproses** oleh PortalHub.
6. Pembayaran yang diproses hanya **layanan PortalHub** (subscription, paket, iklan, top-up Kantong) melalui QRIS atau transfer terverifikasi. Bayar langsung tanpa mengisi Kantong harus didukung; jika pelanggan memilih, dapat top-up sejumlah tagihan lalu bayar dari Kantong.
7. Kantong adalah saldo tertutup untuk layanan PortalHub, dengan tiga riwayat: **Top Up**, **Transaksi** pemotongan saldo, **Payment** pembayaran langsung. Auto-renew harus opt-in.
8. Aktivasi organisasi default **Hybrid**: PortalKos self-service, PortalWarga verifikasi kewenangan sebelum hak sensitif; semua kebijakan produk bisa dikonfigurasi dengan guardrail keamanan wajib.
9. UI **Clean Minimal + Mobile First PWA**. Desktop lebih lengkap; mobile lebih ringkas dan informatif.
10. URL awal yang diusulkan: `portalhub.vercel.app/app`, `/warga/:org`, `/kos/:org`, `/iklan`.

## Status source code

Repository [kodok-ijho/PortalWarga](https://github.com/kodok-ijho/PortalWarga) menjadi **referensi legacy**, bukan otomatis repositori induk. Audit menemukan React 18, Vite, Tailwind, Supabase, n8n, PWA, modul event, dan migrasi event finance. Proses QRIS IPL yang ada pada legacy **tidak boleh otomatis dipindah** karena desain PortalHub kini hanya mencatat IPL, bukan menerima pembayarannya. Verifikasi hasil migrasi harus dilakukan di staging.

## Mulai implementasi

Mulai dengan [ADR](docs/10-decisions/ADR-0001-modular-monolith.md), [data model](docs/03-data/Data-Model.md), [RBAC](docs/04-security/RBAC.md), [billing](docs/05-billing/Kantong-and-Payments.md), dan [backlog](docs/09-delivery/Roadmap.md). Jangan deploy pembayaran produksi sebelum review provider, hukum, dan pengujian idempotensi.