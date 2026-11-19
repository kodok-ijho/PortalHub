# URL routing, Vercel & PWA

## Route contract

| Route | Scope | Auth | SEO |
|---|---|---|---|
| `/` | Marketing PortalHub | Public | index |
| `/login`, `/auth/callback` | Auth | mixed | noindex |
| `/app` | User service chooser | required | noindex |
| `/app/kantong` | Org wallet | required | noindex |
| `/app/subscription` | Org billing | required | noindex |
| `/kos/:orgSlug/dashboard` | Owner/manager | required | noindex |
| `/kos/:orgSlug/properti/:propertySlug` | Property scope | required | noindex |
| `/kos/:orgSlug/penyewa` | Own lease | required | noindex |
| `/warga/:orgSlug/beranda` | Resident | required | noindex |
| `/warga/:orgSlug/keuangan` | Treasurer | required | noindex |
| `/warga/:orgSlug/event/:eventId` | Event scope | required | noindex |
| `/iklan` | Public marketplace | public | index |
| `/iklan/:category/:city/:slug` | Published listing | public | index conditional |

`slug` hanya presentation ID, lookup ke ID stabil dalam DB. Tidak boleh digunakan sebagai bukti hak akses. URL yang menyimpan token tidak boleh masuk log publik; callback return path relative dan allowlisted.

## Deployment

**Development URL:** `https://portalhub.vercel.app` bila tersedia/dimiliki. **Production domain:** belum diputuskan. Vercel projects dapat dipisah `hub-web` (private PWA) dan `ads-web` (SSR), dipaparkan melalui rewrite yang diuji. Alternatif satu Next.js app untuk seluruh UI dipertimbangkan jika mengurangi biaya routing; gunakan ADR sebelum mengubah stack.

## PWA caching

Cache hanya app shell dan asset statis. Jangan menyimpan API tenant, Kantong, bukti bayar, PII sebagai public offline cache. Gunakan network-only untuk endpoint finansial. Clear caches on logout/context switch. Perhatikan batasan push di browser.


## File / media routing — Cloudflare R2

Aplikasi mengakses API `/api/v1/files/*` di Vercel (server protected), yang membuat short-lived **R2 S3 API presigned PUT/GET** sesudah cek permission. R2 presigned URL **bukan** URL custom CDN domain. Browser CORS harus mengizinkan origin dev/staging/prod yang tepat; CORS tidak memberikan hak akses.

Media iklan approved dapat diakses publik melalui custom domain Cloudflare (mis. `media.portalhub.id`, **belum disiapkan**) dengan cache. `r2.dev` hanya untuk penggunaan non-produksi. Private bucket tidak pernah dibuka via CDN. Jangan cache signed URL atau file pribadi di PWA. [File Storage](../03-data/File-Storage.md).
