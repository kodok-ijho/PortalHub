# PRD — PortalHub

**Versi:** 0.1 · **Tanggal:** 19-11-2026 · **Status:** Baseline keputusan + rancangan MVP. **Pemilik keputusan:** product owner PortalHub.

## 1. Problem & visi

Pengurus warga dan pemilik properti sering memakai spreadsheet terpisah untuk rumah, penghuni, iuran, kontrak, dan laporan. Pelaku usaha lokal juga kesulitan memperoleh eksposur. PortalHub memberi satu identitas dan billing untuk produk administrasi yang terpisah secara domain, serta satu marketplace iklan publik.

**Bukan tujuan:** menerima dana IPL/sewa/event, melakukan escrow, menangani pembayaran jual-beli pelanggan, menyediakan transfer saldo antarpengguna, atau menjamin transaksi dari iklan.

## 2. Target pengguna

- Platform owner/admin/support yang mengelola layanan, kebijakan, verifikasi, billing.
- Organization owner/admin/billing manager.
- Ketua/pengurus, sekretaris, bendahara, koordinator blok, panitia event dan warga.
- Pemilik kos, manager, finance, penjaga/staf, penyewa.
- Pengiklan dan pengunjung publik tanpa login.

## 3. Lingkup produk

### PortalHub Core (P0)

- **PH-001** Registrasi/login; satu `auth.users` untuk seluruh produk, tidak ada akun login otomatis untuk penghuni/penyewa pasif.
- **PH-002** Organisasi multi-membership; user berpindah konteks organisasi/produk; role + scope.
- **PH-003** Organisasi mengaktifkan satu/lebih produk, subscription/kuota per produk, billing terpusat.
- **PH-004** Policy onboarding configurable: auto, approval, invite-only; default Kos auto, Warga approval untuk kewenangan sensitif; perubahan kebijakan diaudit dan tidak mengaktifkan organisasi lama secara massal.
- **PH-005** Invite member, verifikasi identitas/relasi ke penghuni, revoke akses, audit trail.
- **PH-006** Role bawaan dan custom role (paska MVP untuk editing granular), enforce di API dan RLS.

### PortalKos (P0/P1)

- **PK-001** Organisasi memiliki banyak properti; tiap properti banyak unit (kamar/kontrakan/apartemen).
- **PK-002** Unit memiliki status tersedia, dipesan, terisi, maintenance, nonaktif; sumber status berasal dari kontrak/reservasi tervalidasi.
- **PK-003** Data calon penghuni/penyewa, kontrak, penghuni tambahan, deposit jaminan **sebagai pencatatan**, tagihan bulanan, denda sesuai konfigurasi.
- **PK-004** Catat pembayaran **tunai atau transfer di luar platform**, bukti opsional, diverifikasi petugas berwenang; koreksi melalui reversal, bukan hapus diam-diam.
- **PK-005** Expense, laporan per properti dan konsolidasi; property-scoped staff.
- **PK-006** Publish iklan unit kosong dengan persetujuan pemilik; saat terisi status iklan diperbarui otomatis. Grupkan unit identik menjadi listing tipe kamar bila sesuai.
- **PK-007** Portal penyewa untuk data/kontrak/tagihan milik sendiri; login opsional.

### PortalWarga (migrasi bertahap)

- **PW-001** Rumah, warga, penghuni, profil, IPL dan matriks tunggakan.
- **PW-002** Pembayaran IPL hanya pencatatan tunai/transfer + bukti + verifikasi internal. Fitur legacy QRIS IPL langsung tidak diteruskan ke arsitektur baru.
- **PW-003** Kas utama, pengeluaran, laporan, dokumen dan pengumuman.
- **PW-004** Event dengan assignment panitia event-scoped, pemasukan, biaya, budget, dan **kas/laporan event terpisah dari kas utama**. Transfer kas menjadi dua pencatatan berpasangan agar laporan konsolidasi tidak double-count.
- **PW-005** Warga dapat mengiklankan usaha melalui PortalIklan setelah moderasi, tidak pernah membocorkan data rumah/penduduk tanpa izin.
- **PW-006** Akses warga hanya untuk household/unit yang ditautkan melalui verifikasi/undangan.

### PortalIklan

- **PI-001** Katalog publik mobile-first, detail listing dapat dibuka tanpa login, kategori + kota/area + search + filter.
- **PI-002** Listing usaha (laundry, makanan, bakery, jasa, toko, kontrakan) dan properti sewa.
- **PI-003** Moderasi, laporan iklan, pencegahan spam, consent menampilkan kontak dan lokasi umum.
- **PI-004** Kuota gratis awal dan masa tayang berbatas; semua iklan memiliki expiry. Gratis tidak otomatis menjadi berbayar kecuali opt-in dan menyetujui harga.
- **PI-005** Paket iklan, prioritas/promosi berlabel, perpanjangan via Kantong atau bayar langsung.
- **PI-006** SEO server-rendered: title/description unik, URL kanonis, sitemap, robots, structured data sesuai tipe, gambar optimal, internal links. Halaman private di-noindex.
- **PI-007** Marketplace adalah media periklanan, bukan perantara checkout/escrow; kontak WhatsApp/lead di luar transaksi.

### Kantong & billing (P0 untuk SaaS, monetisasi iklan P2)

- **BL-001** Satu Kantong milik organisasi/billing account; saldo terbatas untuk layanan PortalHub. Tentukan kasus akun individu secara eksplisit sebelum coding.
- **BL-002** Top Up QRIS/transfer otomatis setelah webhook provider tervalidasi.
- **BL-003** Tiga histori: Top Up, Transaksi (debit Kantong per layanan), Payment (direct QRIS/transfer tanpa top-up). Direct top-up tepat senilai invoice juga didukung sebagai dua langkah terpisah.
- **BL-004** Checkout layanan melalui service order yang sama untuk saldo ataupun direct pay; aktivasi setelah pembayaran final verified.
- **BL-005** Subscription & auto-renew Kantong **default off**, per produk; pemberitahuan sebelum jatuh tempo; saldo tidak boleh negatif; webhook/job idempotent.
- **BL-006** Paket sekali beli (kuota/durasi) terpisah dari saldo uang; perhitungan entitlement dijalankan di server.
- **BL-007** Refund/expired credit/tax/terms harus melalui review legal dan kebijakan provider sebelum produksi.

## 4. Business invariants

1. Setiap baris organisasi memuat `organization_id`; seluruh read/write dibatasi tenant yang benar.
2. Role/scope tidak boleh diperoleh dari klaim frontend saja.
3. Payment operasional `verified_internal` ≠ bank settled/verified by PortalHub.
4. `wallet_ledger` append-only; transaksi debit dan service activation atomik atau memakai state machine + retry yang idempotent.
5. Hanya invoice untuk layanan PortalHub yang memicu payment gateway.
6. Kuota PortalKos menghitung unit aktif pada seluruh properti organisasi. Jumlah properti bukan dasar kuota.
7. Event cashbook terpisah, transfer antar kas berpasangan, laporan gabungan mengeliminasi transfer internal.
8. Listing berakhir pada expiry dan tidak diperpanjang berbayar tanpa otorisasi.

## 5. User stories & acceptance criteria

| ID | User story | Acceptance criteria |
|---|---|---|
| US-01 | Sebagai pemilik kos, saya mendaftarkan beberapa properti | Satu org, banyak property; unit usage agregat; staff hanya melihat property assigned |
| US-02 | Sebagai penyewa, saya melihat tagihan sendiri | Tidak dapat membaca kontrak/akun penyewa lain, termasuk melalui URL atau API |
| US-03 | Sebagai bendahara, saya memverifikasi pembayaran transfer | Ada recorder, verifier, timestamp dan bukti; status `verified_internal`; tidak mengubah rekening pihak lain |
| US-04 | Sebagai panitia, saya melihat kas event saya | Tidak bisa melihat kas utama atau event lain tanpa grant |
| US-05 | Sebagai pelanggan, saya membeli subscription | QRIS direct atau Kantong; activated sekali setelah settled; histori yang benar |
| US-06 | Sebagai pengiklan, saya menerbitkan kamar kosong | Owner opt-in, listing melewati moderasi; status auto-closed saat unit terisi |
| US-07 | Sebagai pengunjung, saya menemukan usaha melalui Google | Halaman detail SSR, meta unik, canonical, sitemap, tanpa data internal |
| US-08 | Sebagai admin, saya mengganti policy onboarding | Berlaku ke onboarding baru; audit trail; tidak mengubah grant sensitif secara retroaktif |
| US-09 | Sebagai pelanggan, saya mengaktifkan auto-renew | Opt-in tersimpan, debit tepat satu kali per periode; gagal jika saldo tidak cukup |

## 6. Non-functional requirements

- **Security:** deny-by-default, RLS enforced, cross-tenant API tests, rate limiting dan MFA untuk tindakan berisiko tinggi (sesuai dukungan Auth).
- **Performance target awal:** LCP publik <=2.5 s, INP <=200 ms, CLS <=0.1 pada p75; evaluasi data lapangan; dashboard menampilkan data pertama secara responsif.
- **Reliability target usulan:** uptime 99.5% awal; queue retry/backoff untuk event pembayaran; backup dan restore test berkala.
- **UX:** mobile-first, minimum 44px touch target, desktop detail & tabel, mobile ringkas & kartu; WCAG 2.2 AA sebagai target.
- **SEO:** public indexable; aplikasi login, data pribadi, pembayaran: noindex; sitemap membuang listing ilegal/ditolak.
- **Observability:** correlation ID, error rate, audit change dan payment reconciliation dashboard.

## 7. Delivery & release gates

**Fase fondasi:** identity, tenant, role/scopes, product catalog, service order & subscription, Kantong. **Fase marketplace publik:** katalog + SEO + kuota gratis. **Integrasi iklan:** PortalKos dahulu, PortalWarga kemudian. **Monetisasi lanjutan:** paket, promosi, auto-renew iklan. Detail di `09-delivery/Roadmap.md`.

**Go/no-go:** isolasi RLS, payment idempotency, backup+restore, SEO public SSR, pengujian hak akses event, dan verifikasi langkah migrasi legacy harus lulus sebelum produksi.

## 8. Masih perlu validasi

Harga paket, periode trial/gratis, merek/domain final, apakah satu individu tanpa organisasi boleh punya Kantong, detail refund/saldo tidak terpakai, provider QRIS/VA/transfer, legal saldo layanan, retention data, dan aturan verifikasi organisasi warga. **Jangan mengarang nilai default produksi untuk hal ini.**
## 9. Autentikasi (keputusan)
Login utama via Google OAuth menggunakan Supabase Auth. Email OTP/magic link dapat diaktifkan secara configurable. Login tidak otomatis memberikan membership atau akses ke data organisasi; authorization tetap memerlukan membership aktif, product entitlement, scope, dan PostgreSQL RLS.


## 10. File storage — Cloudflare R2 (requirement disepakati)

- **STO-001:** Cloudflare R2 menyimpan seluruh file baru: bukti transfer IPL/sewa/event, kontrak, dokumen organisasi, media iklan dan lampiran pembayaran layanan PortalHub.
- **STO-002:** Supabase Auth tetap mengelola Google Login; Supabase PostgreSQL + RLS menyimpan metadata, org, file links, role, scope, izin dan audit. RLS **tidak otomatis melindungi R2**.
- **STO-003:** Bucket privat/publik/temp per environment. Bukti dan dokumen privat tidak mendapat public URL; media iklan hanya menjadi publik setelah consent, moderasi, scan dan sanitasi.
- **STO-004:** Upload via server-authorized intent → presigned PUT R2 S3 API → validasi server/scan → metadata ready; private download sesudah cek izin dengan short-lived signed GET/proxy. Kuota dan cleanup upload orphan wajib.
- **STO-005:** Backup file R2 dan metadata PostgreSQL secara terpisah serta latihan restore bersama. Penentuan kapasitas paket, retensi, dan legal hold masih perlu validasi.
- **STO-006:** Status file siap tidak mengubah pembayaran IPL/sewa menjadi bank-settled; verifikasi keuangan tetap internal.

**Acceptance:** uji isolasi tenant/event/property, MIME/size/malware, quota race, signed URL expiry, no public-leak, retention, restore dan biaya. [File Storage](03-data/File-Storage.md).


## 11. Implementation reference & open decisions

Sumber detail pelaksanaan yang berkaitan langsung: [Auth & SSO](04-security/Auth-and-SSO.md), [Permission Matrix](04-security/Permission-Matrix.md), [RLS Policy Spec](04-security/RLS-Policy-Spec.md), [Database Schema](03-data/Database-Schema.md), [Subscription Lifecycle](05-billing/Subscription-Lifecycle.md), [Payment State Machines](05-billing/Payment-and-Wallet-State-Machines.md), [PortalKos Rules](06-products/PortalKos-Business-Rules.md), [PortalWarga Finance Rules](06-products/PortalWarga-Finance-Rules.md), [PortalIklan Publishing Rules](06-products/PortalIklan-Publishing-Rules.md), [Draft OpenAPI](08-operations/OpenAPI.yaml), dan [Traceability](09-delivery/Requirements-Traceability.md). Dokumen ini menetapkan kebutuhan; parameter harga/provider, retensi, SLA serta fitur yang berstatus TBD tidak boleh ditafsirkan sebagai keputusan produksi.
