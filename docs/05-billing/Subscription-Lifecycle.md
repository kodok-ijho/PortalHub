# Subscription Lifecycle & Entitlement Rules

**Status:** design contract P0. Product catalog, prices, trial duration, grace period and provider selection **remain configurable/unresolved**. No production charging without legal and provider review; see [ADR-0002](../10-decisions/ADR-0002-wallet.md).

## Entities

`billing_account` (default organization-owned) → product-specific `subscription` → plan/price version → service orders/renewal attempts → entitlement projection. `package_entitlements` are separate quota/duration rights, **not** Kantong money.

## Lifecycle states

| State | Accessible features | Entry/exit |
|---|---|---|
| `draft` | no paid entitlement | Org chooses plan; not yet ordered |
| `trial` | explicitly allowed trial quotas | Trial enrollment if policy permits; never silently transitions to paid |
| `pending_payment` | no new paid entitlement | Checkout created awaiting wallet debit/provider settled |
| `active` | entitled by product & plan limits | Successful **wallet debit OR verified direct payment OR approved promotional grant** |
| `past_due` | configurable restricted access, no fake active | Renewal due, no success; policy grace if permitted |
| `suspended` | non-destructive restricted access | Entitlement suspended due to policy/nonpayment |
| `cancelled` | defined end-of-term behavior | Explicit cancellation, preserve historical records |
| `expired` | read/export/archival only by policy | Term ended, no entitlement renewal |

These are a **proposed canonical state map**; existing PRD mentions slightly different subsets. Every code path must map to these or adopt explicit ADR before implementation.

## Activation and payment

1. Order uses server-side price snapshot, plan version, period, tax rules and discount validation; client price is informational.
2. **Kantong checkout:** sufficient settled credit → atomic debit with unique service-order ID → order paid → idempotent entitlement activation. **Does not require another provider webhook** for funds already in Kantong.
3. **Direct checkout:** payment provider verifies settled amount/reference/currency via signed webhook and reconciliation → order paid → activate entitlement exactly once. Browser success redirect alone never activates.
4. **Exact top-up then wallet:** provider verifies top-up → credit wallet once → **separate user-authorized debit** for service order → activate. Do not treat top-up as blanket auto-spend permission.
5. Promotional/free grants need audited operator/policy authority and must not simulate a payment.

## Renewal and consent

- Auto-renew **OFF by default** for every product/listing; store explicit actor, timestamp, displayed price/plan version, funding source and consent version.
- Renewal job at most once per `subscription_id + period_start + renewal_type`, with atomic guard/unique key. Send reminder in advance per configured policy.
- Kantong insufficient → `past_due`/`payment_required`, no negative balance and no silent fallback charging external payment instrument.
- Opt-out stops future renewals, not previously paid term. Price or plan changes require notification; material differences may require new opt-in.
- Direct-pay renewal is **not automatically possible** merely because a previous QRIS payment succeeded; a reusable authorized payment mandate, provider support, consent and legal review would be required.
- Free trial and free ad allowance never silently become paid at expiry.

## Plan changes / quotas

- Upgrade/downgrade effective date (immediate/next term) and proration are **open policy decisions**. Until defined, do not auto-charge partial amounts.
- Kos paid unit quota counts all **active rentable units** across properties; flags and unit definitions must be agreed with billing catalog before enforcement.
- Warga quota (if used) counts active registered houses, but exact unit policy is not finalized.
- Over-quota: do not delete leases/houses or financial history; pause creating more entitled units/features as permitted, communicate limits and provide read/export.
- Suspension, expiry, cancellation and owner leave **must not wipe historical finance data** or files; retention policy applies.

## Failure cases

| Case | Expected safe outcome |
|---|---|
| Webhook duplicate/out-of-order | One settlement and one fulfillment; journal event and reconcile |
| Concurrent renewal workers | One renewal attempt/debit only |
| Worker crashes after settlement | Durable order remains paid; retry fulfillment idempotently |
| Wallet debit fails | No entitlement granted |
| Refund/chargeback | Follow authorized reversal/accounting and entitlement review; do not mutate settled ledger |
| Price mismatch/expired quote | Requote and request acceptance, no implicit payment |
| Organization loses product access mid-term | Preserve audit; implement explicit suspension/cancellation policy |
| Package expires | Stop new usage, do not delete published artifacts without lifecycle decision |

## Tests and gates

- Wallet vs direct vs exact top-up histories stay distinct.
- Trial/expiry never charges without opt-in; insufficient balance never becomes negative.
- Double-click/duplicate event/parallel worker never double activates/debits.
- Non-billing actor cannot modify subscription; scoped owner/manager cannot spend Kantong without grant.
- Quota changes do not silently delete active operational records.
- Eventual consistency between order, payment, entitlement and notification resolved via reconciliation job.

See [Payment State Machines](Payment-and-Wallet-State-Machines.md), [Kantong](Kantong-and-Payments.md), [Permission Matrix](../04-security/Permission-Matrix.md).

**Launch blockers:** approved pricing & plan catalogue, refunds, tax, subscription terms, legal/payment-provider design for Kantong.
