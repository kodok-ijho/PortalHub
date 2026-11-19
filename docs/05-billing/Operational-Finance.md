# Keuangan operasional (record-keeping only)

## Hard boundary

PortalKos sewa/jaminan, PortalWarga IPL dan biaya event, jual-beli pengiklan: dana berpindah **langsung antar pengguna di luar PortalHub**. Tidak ada gateway, escrow, auto-debit bank, atau settlement verification oleh PortalHub.

## Metode dan status

Method: `cash`, `bank_transfer`. Evidence upload optional (terutama transfer); role dapat meminta bukti berdasarkan policy org. Status: `recorded` → `pending_internal_verification` → `verified_internal` / `rejected` / `reversed`. `verified_internal` berarti pengelola telah menyatakan diterima, bukan konfirmasi bank dari PortalHub.

## Separation of duties

Staff boleh mencatat; finance/owner memverifikasi sesuai permission. Perubahan nominal setelah verifikasi dengan reversal/adjustment dan audit, bukan edit tanpa jejak. Laporan menampilkan kategori, periode, cash vs transfer, dan bukti.

## PortalWarga event cashbooks

Setiap event punya account + budget + income + expense + laporan sendiri; kas utama terpisah. Subsidi dari kas utama → event menggunakan linked internal transfer dua sisi, bukan revenue external. Laporan konsolidasi memisahkan transfer internal dari revenue/expense agar tidak terhitung dua kali.

## PortalKos

Tagihan bulanan berdasarkan kontrak; pembayaran partial boleh jika policy diaktifkan; deposit jaminan penyewa adalah **catatan kewajiban pemilik kos**, tidak sama dengan Kantong.

## Report verification

Compare transaction sum by account, by method, by period; verify expense reversals, duplicate proof and event transfers. Semua ekspor harus mewarisi scope RBAC yang sama.


## Storage bukti transfer — Cloudflare R2

Bukti IPL, sewa dan dana event disimpan **private di Cloudflare R2**. Hubungan ke transaksi, status berkas, ownership, metadata dan audit berada di Supabase PostgreSQL + RLS. Backend memeriksa organisasi, event/property, pemilik dan role sebelum upload/download. Bukti lolos scan (`ready`) bukan berarti transaksi bank diverifikasi: status `verified_internal` membutuhkan otorisasi petugas dan audit terpisah. Jangan expose bukti di iklan/ekspor publik atau cache PWA. [File Storage](../03-data/File-Storage.md).
