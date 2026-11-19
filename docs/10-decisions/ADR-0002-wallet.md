# ADR-0002 — Kantong as closed-loop service credit

**Status:** Product direction accepted, regulatory/provider model pending review · 2026-11-19.

## Context

Customers want prepaid balance to renew services/ads, plus direct QRIS/transfer checkout. PortalHub does not handle rent/IPL/consumer sale funds.

## Decision

Design Kantong for PortalHub services only; append-only ledger, no negative balances, no peer-to-peer cash transfer. Service orders support `wallet`, `direct`, or `topup_exact_then_wallet`. Auto-renew opt-in, price disclosure and idempotency. Separately show Top Up, Transaksi, Payment.

## Alternatives / risk

Purchased package credits reduce exposure to arbitrary stored value but cannot replace all requested Kantong functions. Holding prepaid funds still creates legal/accounting/provider obligations. **Launch blocked pending legal, tax and payment partner review.**
