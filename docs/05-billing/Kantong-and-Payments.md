# Kantong, subscription, paket & payment

## Functional definition

**Kantong** adalah saldo prabayar terbatas untuk **layanan PortalHub**, bukan alat untuk mengirim uang ke user lain, refund otomatis ke user lain, atau membayar sewa/IPL. Satu billing account organisasi memiliki Kantong IDR. Design legal/funds custody perlu verifikasi sebelum produksi.

## Tiga history tabs

1. **Top Up:** `wallet_topups` lengkap dengan tanggal order, metode QRIS/transfer, nominal, status dan provider reference. Tampilkan kredit hanya setelah settled.
2. **Transaksi:** `wallet_ledger` debit/credit adjustments untuk subscription, listing, paket beserta `service_order_id`, sumber produk/fitur, tanggal dan outcome.
3. **Payment:** `platform_payments` direct checkout QRIS/transfer untuk service order tanpa top-up. **Tidak** menambah saldo Kantong.

## Payment channels

**A. Wallet:** order → validasi entitlement/price → lock wallet & atomic debit ledger → fulfill service idempotently.

**B. Direct:** order → QRIS/transfer checkout provider → webhook verified → mark settled → fulfill; no ledger wallet entry.

**C. Top-up sesuai nominal invoice:** order → top-up wallet same amount → provider verified → credit wallet → user-authorized debit for order; show two linked records transparently. Never silently assume a top-up authorizes all future spending.

## State machine & idempotency

`service_order`: `draft` → `pending_payment` → `paid` → `fulfilling` → `fulfilled`; alternative `expired`/`cancelled`/`retryable_failure`.

`wallet_topup`: `created` → `pending` → `settled` (or `expired`/`failed`/`refunded`).

`subscription`: `trial`/`active`/`past_due`/`suspended`/`cancelled`; terms and grace period configurable, but not invented by implementation.

`listing`: `draft`/`pending_moderation`/`published`/`paused`/`expired`/`rejected`/`unavailable`.

Provider webhook dedup `provider_event_id UNIQUE`; renewal dedup `subscription_id+period_start`; wallet debit dedup `service_order_id`. Each transition has actor/trigger/time and immutable audit.

## Subscription & packages

- Per-product subscription and quota; org can buy both Warga/Kos. Kos unit limit aggregate of active rentable units across all properties; Warga house quota aggregate active houses.
- `product_packages` provide entitlement (e.g., 5 ads x 30 days) independent of Kantong IDR; package usage checks expiration and allowance.
- Auto-renew per product/listing only after explicit opt-in, renewal timing, price transparency and advance reminder. Insufficient Kantong → request payment; no negative balances.
- Promotion marked clearly; initial free quota has start/end and never silently bills.

## Accounting and operations

Use append-only ledger and double-entry design for wallet liability and platform revenue at accounting layer, subject to accounting review. Reconcile provider settlement daily; unmatched payments flagged, not guessed. Refund: authorized order + compensating ledger/payment transaction, reason, audit. Legal policy for unused balance, expiry, and returns pending.

## Example acceptance tests

- Two duplicate webhook events grant exactly one top-up credit.
- Two simultaneous renewal workers debit exactly once.
- Direct QRIS order records Payment history but no Top Up/ledger credit.
- Exact invoice top-up creates a credit and a matched debit, never a single opaque entry.
- Tenant staff cannot top up/spend org wallet without grant.


## Lampiran platform payments & R2

Lampiran invoice, kuitansi, atau bukti transfer untuk **layanan PortalHub** (jika digunakan) disimpan di private Cloudflare R2 dan ditautkan ke `platform_invoices`/`platform_payments` memakai metadata `file_assets` yang terotorisasi. File upload tidak pernah secara otomatis mengubah status payment settled, menambah saldo Kantong, atau mengaktifkan entitlement; server tetap memerlukan provider verification dan idempotency. [File Storage](../03-data/File-Storage.md).
