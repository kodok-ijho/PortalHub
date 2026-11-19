# API contract conventions (design)

## Response envelope

```json
{"ok":true,"data":{},"error":null,"meta":{"request_id":"req_123","timestamp":"2026-11-19T00:00:00Z"}}
```

Error: `{ "ok": false, "data": null, "error": {"code":"FORBIDDEN","message":"Tidak punya akses"}, "meta":{"request_id":"req_123"} }`.

## Endpoint registry (illustrative, versioned `/api/v1`)

| Method | Route | Auth / permission |
|---|---|---|
| POST | `/organizations` | signed-in; onboarding policy |
| GET | `/me/contexts` | signed-in |
| POST | `/organizations/:id/invitations` | `org.member.invite` |
| PATCH | `/organizations/:id/policy` | platform policy manage |
| GET | `/organizations/:id/wallet` | `hub.wallet.view` |
| POST | `/organizations/:id/wallet/topups` | `hub.wallet.topup`, idempotency |
| GET | `/organizations/:id/wallet/ledger` | `hub.wallet.view` |
| POST | `/service-orders` | `hub.service.purchase` |
| POST | `/service-orders/:id/checkout` | billing owner, idempotency |
| POST | `/webhooks/payments/:provider` | provider signature only; no user bearer auth |
| POST | `/subscriptions/:id/renewal-settings` | billing manager |
| GET | `/kos/:orgId/properties` | product+property scope |
| POST | `/kos/:orgId/payment-records` | `kos.payment.record` |
| POST | `/kos/:orgId/payment-records/:id/verify` | `kos.payment.verify` |
| GET | `/warga/:orgId/events/:eventId/finance` | event scope finance read |
| POST | `/warga/:orgId/events/:eventId/transactions` | event finance write |
| GET | `/public/ads` | public, approved projection only |
| GET | `/public/ads/:id` | public, published only |
| POST | `/ads/:id/publish` | verified owner/permission+moderation |

## Security contract

- Require `Idempotency-Key` on financial writes; request identity from server auth, not role headers.
- Validate org membership and resource scope on every request; consistent 401/403/404 semantics to prevent enumeration.
- API never trusts `amount` from browser for final service price; server calculates from catalog.
- Checkout success URL is informational only; actual fulfillment comes from verified provider result.
- Use pagination, stable cursor, validation and rate limits; private endpoints no-cache.

Draft machine-readable [OpenAPI.yaml](OpenAPI.yaml) **sudah tersedia** sebagai starting contract (sebagian endpoint dasar). Ini **bukan** full production OpenAPI/endpoint siap dijalankan; schema, error mapping dan provider-specific callback perlu diperdalam dan diuji saat implementasi.


## Cloudflare R2 — API contract file (design, belum implementasi)

| Method | Route | Kewajiban server |
|---|---|---|
| POST | `/files/upload-intents` | Supabase Auth + org/product/resource permission; quota reserve; return `asset_id` + presigned R2 S3 PUT TTL pendek |
| POST | `/files/:assetId/complete` | Verify actor, R2 object HEAD, actual size/type, enqueue scan; idempotent |
| GET | `/files/:assetId` | Metadata setelah PostgreSQL RLS + backend authorization |
| POST | `/files/:assetId/download` | Private file `ready`, permission rechecked; presigned R2 S3 GET TTL pendek atau authenticated proxy |
| POST | `/files/:assetId/publish` | Listing owner consent+moderation+scan; sanitasi derivative ke R2 public |
| DELETE | `/files/:assetId` | Permission, retention/legal hold, soft-delete & asynchronous object removal |
| GET | `/organizations/:id/storage-usage` | Owner/billing manager, quota used/reserved per kategori |

Prefix versi `/api/v1`, request-id dan idempotency untuk upload; error `INVALID_FILE_TYPE`, `FILE_TOO_LARGE`, `FILE_NOT_READY`, `STORAGE_QUOTA_EXCEEDED`, `FILE_QUARANTINED`. Client tidak boleh memilih bucket/key atau mengirim credential R2. RLS **hanya berlaku di database**; permission untuk signed URL dievaluasi server. Presigned S3 tidak berlaku pada custom domain CDN. [File Storage](../03-data/File-Storage.md).


## Contract-first implementation checklist

[Draft OpenAPI 3.1](OpenAPI.yaml) memetakan onboarding, contexts, wallet, service orders/checkout, subscription renewals, public ads dan file R2. Tambahkan endpoint Kos/Warga detail dan provider-specific webhook schema setelah perancangan domain disetujui. CI harus memvalidasi spec YAML/OpenAPI, compatibility, response envelope/error semantics dan negative authorization tests. Jangan klaim endpoint deployed hanya karena spec tersedia.
