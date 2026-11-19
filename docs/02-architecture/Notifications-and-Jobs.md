# Notifications, Scheduled Jobs & Outbox

**Status:** architecture design; delivery providers, frequencies and numeric thresholds remain open. Does not include connection or credential information.

## Event-driven boundaries

Use a durable outbox in the same DB transaction as domain state changes (when in PostgreSQL), then process asynchronous delivery with idempotency. Never rely only on a browser callback, in-memory timer or unacknowledged webhook for irreversible actions.

| Event | Origin | Consumer/action |
|---|---|---|
| `member.invited` | organization | Invite notification (token one time) |
| `subscription.due` | billing | Reminder based on opt-in & approved schedule |
| `subscription.renewal_requested` | renewal job | Idempotent service order/wallet debit |
| `payment.platform_settled` | verified webhook | Order fulfillment once |
| `wallet.topup_settled` | verified webhook | Wallet credit exactly once |
| `kos.charge_due` | billing schedule | Private payment reminder (external only) |
| `warga.ipl_due` | IPL schedule | Private IPL reminder (external only) |
| `listing.source_availability_changed` | Kos | Update PortalIklan publication/availability |
| `listing.expiry_reached` | scheduler | Unpublish/expire without hidden charge |
| `file.upload_completed` | storage | Scan/verify/quarantine/ready |
| `file.delete_eligible` | retention | Remove R2 object safely/audit |

## Job metadata and guarantees

- `outbox_events`: id, event_type/version, aggregate_id, organization_id, payload reference, occurred_at, delivery attempts, next_attempt_at, state. Do not put raw PII or payment details unnecessarily in payloads/logs.
- `job_runs`: job identity, affected period/resource, progress, retry count, error class, trace ID; unique work identity for financial and billing tasks.
- Delivery is **at-least-once**; consumers implement idempotency keys and DB unique constraints. Exactly-once side effects are achieved at domain boundary via unique transition, not assumed from queue delivery.
- Retry transient errors with bounded exponential backoff/jitter and dead-letter/manual intervention after policy threshold. Permanent invalid request/permission failure must not spin forever.
- A failed job must not silently trigger payment, publish private media or grant role. Errors are surfaced to ops with sanitized context.
- Catch-up after downtime should not bill expired renewal periods without consent; state checks and version checks before each side effect.

## Notifications policy

| Class | Example | Privacy / timing |
|---|---|---|
| Security | New invitation, owner change, sensitive role grant | Immediate/audited according to policy |
| Platform payment | Service order pending/paid, top-up confirmed | Verified state only; never fake bank settlement |
| Subscription | Upcoming expiry/auto-renew failure | Consent and configurable notice schedule |
| Operational finance | IPL/rent due, manual proof rejected | Do not call it platform-collected payment; scoped recipient |
| Ads | Moderation result, listing expiry/unavailable | Ad owner only, no confidential tenant info |
| Documents | Upload quarantined, retention warning | Minimal metadata, no private R2 URL in notification |

- Email/in-app notification preferences and local timezone should be respected; legally mandatory/security messages must be classified separately. Quiet hours and cadence **TBD**.
- No plaintext identity documents, landlord bank details, signed R2 download links or sensitive PII in push notifications.
- Template variables are whitelisted and escaped; avoid leaking private org context to wrong recipients after membership revocation.
- Web push/FCM/other transport not selected; don't declare provider installed.

## Operational gates

- Duplicate event and crash-retry tests show one billing debit/one entitlement activation.
- Source unit changed while notification queued → processor revalidates source state before sending/publishing.
- Repeated permission changes → no notification sent to revoked user when possible; audit required.
- Dead-letter queue dashboard, lag alerts, job backpressure, rate limits, owner review, and traceability in [DevOps](../08-operations/DevOps-Runbook.md).

**Related:** [Payment State Machines](../05-billing/Payment-and-Wallet-State-Machines.md), [Ads Publishing](../06-products/PortalIklan-Publishing-Rules.md), [Data Retention](../03-data/Data-Retention-and-Privacy.md).
