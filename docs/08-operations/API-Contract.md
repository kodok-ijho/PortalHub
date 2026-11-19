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

Full OpenAPI schema is a **future implementation deliverable**, not falsely represented as complete here.
