# Auth & SSO — Supabase Auth + Google Login

**Status:** spesifikasi desain P0; Google OAuth dipilih sebagai metode utama. Belum ada deployment atau credentials yang disiapkan. **Tidak memuat informasi credential.**

## Prinsip

- **Satu identitas Supabase Auth (`auth.users.id`)** lintas PortalHub, PortalKos, PortalWarga, PortalIklan. Google OAuth adalah autentikasi, bukan grant ke organisasi.
- **Authorization:** membership organisasi aktif + entitlement produk + permission/role + resource scope + kebijakan; enforcement dilakukan API dan PostgreSQL RLS, bukan UI.
- Default deny. User dapat berstatus tenant/warga di beberapa organisasi dengan izin berbeda. Data calon penyewa/warga tanpa akun tidak otomatis dibuatkan login.
- Login utama Google; email OTP/magic link **opsi configurable** bila diaktifkan. Jangan menyalakan password login tanpa keputusan produk tersendiri.

## Alur login dan callback

```mermaid
sequenceDiagram
 participant B as Browser
 participant A as Supabase Auth
 participant P as PortalHub API
 participant D as PostgreSQL
 B->>A: Login Google via OAuth PKCE
 A-->>B: Callback/session
 B->>P: Request /me/contexts
 P->>A: Verify authenticated session
 P->>D: Active memberships, product entitlements, role & scopes
 D-->>P: Permitted contexts only
 P-->>B: 0 => onboarding; 1 => authorized redirect; >1 => selector
```

1. Login callback menggunakan allowlist domain dan path kembali yang **relative**, bukan open redirect. Lindungi flow OAuth dengan PKCE/state dan penanganan callback gagal, batal, kedaluwarsa serta akun belum disetujui.
2. Jangan gunakan email atau domain Google sebagai permission organisasi; user ID Supabase adalah identitas stabil. Verifikasi status email/provider yang diizinkan sebelum mengikat invitation.
3. `profiles` dibuat secara idempotent ketika login pertama, berisi atribut minimal. Nama/avatar dari provider bukan sumber klaim role.
4. Setelah login, API hanya mengembalikan daftar konteks **yang diotorisasi**. Perubahan organisasi mengosongkan cache data tenant di client; URL slug tidak membuktikan akses.
5. Session expired, revoked, atau member disabled → API menolak request; UI mengarah ke login/halaman akses ditolak tanpa kebocoran data.
6. Logout membersihkan state dan cache sensitif; signed URL R2 lama dapat tetap berlaku sampai TTL pendek yang ditetapkan dalam storage policy.

## Invitation, account linking dan lifecycle

- Invitation menyimpan `organization_id`, `product_id`, scope yang diizinkan, hashed one-time token, email target (atau hash sesuai kebijakan), inviter, expiry, status dan audit.
- **Accept** harus dilakukan oleh authenticated user setelah alamat email target diverifikasi; bila berbeda, jelaskan kesalahan, jangan langsung assign role. Undangan belum diterima tidak membuka data.
- Penambahan relasi warga→rumah atau penyewa→kontrak membutuhkan verifikasi pengurus/pengelola sesuai kebijakan produk. Identitas Google **tidak otomatis** memverifikasi hubungan dengan rumah/sewa.
- Perubahan email Google/akun duplikat **tidak digabung otomatis** berdasarkan kemiripan nama/email. Pemindahan kepemilikan atau merge identity butuh alur pemulihan manual yang diaudit (rincian final menunggu keputusan operasional).
- Cabut membership → izin API/RLS berhenti segera. Hindari menghapus histori keuangan saat akun keluar.
- Jangan menghapus pemilik aktif terakhir; transfer ownership mensyaratkan re-auth, penerima setuju dan audit.

## Keamanan login dan session

| Skenario | Perilaku wajib |
|---|---|
| OAuth callback ke domain tak dikenal | Tolak redirect |
| User login tanpa org | Menu onboarding/invitation, tidak diberi data tenant |
| User dengan banyak org | Context selector, cek izin ulang setiap switch |
| Session invalid | HTTP 401, clear state private |
| Member disabled / produk tidak aktif | HTTP 403/404 sesuai kebijakan tanpa bocor resource |
| Invite reused/expired | Tolak secara idempotent, audit |
| Privileged operation | Re-auth/MFA step-up sesuai kemampuan provider dan risk policy |
| Login brute-force/invite spam | Rate limit dan pemantauan |
| Browser PWA offline | Tidak tampilkan data pribadi lintas user/konteks |

Gunakan cookie/session handling yang melindungi CSRF bila diperlukan; jangan menyimpan elevated authorization sebagai klaim client yang dapat dipalsukan.

## Testing minimum

- Login Google sukses/gagal/batal, callback unsafe, session expiry, logout, multi-context, 0-context.
- Invitation target email mismatch, token expired/replay, member revoked, last owner transfer.
- Multi-provider/duplicate email tidak menimbulkan grant lintas akun.
- Privileged flow memerlukan step-up/re-auth sesuai policy; token session tidak pernah menggantikan RLS.
- Preview/staging redirect allowlist diuji terpisah dari production.

**Baca:** [Permission Matrix](Permission-Matrix.md), [RLS Policy Spec](RLS-Policy-Spec.md), [Routes](../02-architecture/Routing-Deployment.md), [Test Plan](../09-delivery/Test-Plan.md).

**Belum final:** jalur pemulihan akun, opsi email fallback per paket, MFA enforcement per role. Tidak ada instruksi mengisi atau membagikan credential dalam dokumen ini.
