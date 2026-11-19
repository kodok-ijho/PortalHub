# ADR-0003 — Cloudflare R2 sebagai storage file PortalHub

**Status: Accepted · 19 November 2026**  
**Pemilik keputusan:** Product owner PortalHub.

## Konteks
PortalHub membutuhkan penyimpanan bukti transfer, dokumen organisasi/kontrak, file event, dan media iklan dengan trafik publik. Supabase Auth + PostgreSQL/RLS telah dipilih untuk identitas serta data relasional; media dan dokumen membutuhkan object storage yang dapat diskalakan dan dibatasi per organisasi.

## Keputusan
Gunakan **Cloudflare R2** untuk seluruh file baru PortalHub. **Supabase Auth** tetap untuk Google Login; **Supabase PostgreSQL + RLS** untuk metadata, relasi ke entitas, permission, kuota, audit, dan retensi. **RLS tidak melindungi object R2** secara langsung. Semua akses private memakai backend-verified permissions dan short-lived presigned S3 URL/proxy.

Pisahkan bucket private/public/temp **per environment**. Media publik hanya dibuat dari file yang telah memperoleh consent, lolos moderation/scan dan disanitasi. Storage adapter backend menjaga fleksibilitas jika provider berganti. Supabase Storage bukan target penyimpanan baru; data file legacy tetap diinventaris dan dimigrasikan secara aman bila ada.

## Alasan
- R2 kompatibel dengan S3 API, sesuai untuk upload langsung dan distribusi media publik.
- Egress R2 tidak dikenai biaya, tetapi operasi/storage layanan tetap memiliki biaya.
- Metadata tetap mengikuti desain organisasi/RLS yang sudah disepakati.

## Konsekuensi
- Dibutuhkan backend signing, R2 API credentials server-only, CORS, scanner/worker, quota reservation, cleanup, CDN takedown, dan backup objek terpisah.
- Signed URL tetap bisa digunakan selama masa berlakunya; TTL pendek dan kontrol logging diperlukan.
- Presigned S3 URLs **tidak** dapat digunakan lewat public custom domain; domain CDN khusus untuk media publik.
- Perlu review hukum tentang retensi/keamanan data, konfigurasi region, serta rincian biaya dan kuota.

## Belum final
Nama domain media, besar kuota tiap paket, file size policy, retention/legal hold, pilihan malware scanner, SOP data residency, RPO/RTO dan metode backup final.

## Implementasi dan verifikasi
Ikuti [File Storage](../03-data/File-Storage.md), [Architecture](../Architecture.md), [Security & Privacy](../04-security/Security-Privacy.md), dan [Test Plan](../09-delivery/Test-Plan.md). Keputusan ini **tidak** berarti bucket R2 sudah dibuat atau integrasi sudah terpasang.
