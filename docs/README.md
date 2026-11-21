# PortalHub — Indeks Dokumentasi

**Status:** spesifikasi desain dan baseline implementasi, **bukan** aplikasi yang telah di-deploy. Pembaruan kelengkapan 19 November 2026. Sebagian aturan (harga, kebijakan Kantong, SLA, retensi) sengaja tetap **TBD** sampai disetujui. **Bagian credential tidak termasuk ruang lingkup dokumentasi ini.**

Kembali ke [README proyek](../README.md) · [Pemetaan requirement ke tes](09-delivery/Requirements-Traceability.md) · [Instruksi coding agent](../AGENTS.md).

## Dokumen utama

| Area | Dokumen |
|---|---|
| Produk | [PRD](PRD.md) |
| Desain UI/PWA | [Design System](Design-System.md) |
| Arsitektur | [Architecture](Architecture.md) |
| Coding agent | [AI Agents](AI-Agents.md) dan [root AGENTS.md](../AGENTS.md) |
| Status cakupan | [Requirements Traceability](09-delivery/Requirements-Traceability.md) |

## 00 — Keputusan dan 01 — Rencana rilis

- [Decision Register](00-product/Decisions.md)
- [MVP and Release Gates](01-product/MVP-and-Release.md)
- [ADR-0001 Modular Monolith](10-decisions/ADR-0001-modular-monolith.md)
- [ADR-0002 Kantong](10-decisions/ADR-0002-wallet.md)
- [ADR-0003 Cloudflare R2](10-decisions/ADR-0003-cloudflare-r2.md)

## 02 — Arsitektur, workflow dan migrasi

- [Business Workflows](02-architecture/Workflows.md)
- [Routing & Deployment](02-architecture/Routing-Deployment.md)
- [Notifications, Scheduled Jobs & Outbox](02-architecture/Notifications-and-Jobs.md)
- [Legacy PortalWarga Migration](02-architecture/Legacy-Migration.md)

## 03 — Database, file & privacy

- [Database Schema Blueprint](03-data/Database-Schema.md)
- [Logical Data Model](03-data/Data-Model.md)
- [High-Level ERD](03-data/ERD.md)
- [Cloudflare R2 File Storage](03-data/File-Storage.md)
- [Data Retention & Privacy](03-data/Data-Retention-and-Privacy.md)

## 04 — Auth dan keamanan

- [Auth & SSO: Supabase Google Login](04-security/Auth-and-SSO.md)
- [RBAC Baseline](04-security/RBAC.md)
- [Permission Matrix](04-security/Permission-Matrix.md)
- [RLS Policy Spec](04-security/RLS-Policy-Spec.md)
- [Security & Privacy](04-security/Security-Privacy.md)

## 05 — Billing / Kantong / keuangan operasional

- [Kantong & Payments](05-billing/Kantong-and-Payments.md)
- [Subscription Lifecycle](05-billing/Subscription-Lifecycle.md)
- [Payment & Wallet State Machines](05-billing/Payment-and-Wallet-State-Machines.md)
- [Operational Finance — Record Only](05-billing/Operational-Finance.md)

## 06 — Produk dan business rules

- [PortalKos](06-products/PortalKos.md) · [PortalKos Business Rules](06-products/PortalKos-Business-Rules.md)
- [PortalWarga](06-products/PortalWarga.md) · [PortalWarga Finance Rules](06-products/PortalWarga-Finance-Rules.md)
- [PortalIklan & SEO](06-products/PortalIklan-SEO.md) · [PortalIklan Publishing Rules](06-products/PortalIklan-Publishing-Rules.md)

## 07 — UX & routes

- [Routes & User Journeys](07-ux/Routes-and-Journeys.md)
- [Screen Specifications](07-ux/Screen-Specifications.md)

## 08 — API dan operasional

- [API Contract Narrative](08-operations/API-Contract.md)
- [Draft OpenAPI 3.1 Contract](08-operations/OpenAPI.yaml)
- [Development Setup Blueprint](08-operations/Development-Setup.md)
- [DevOps Runbook](08-operations/DevOps-Runbook.md)
- [Disaster Recovery](08-operations/Disaster-Recovery.md)

## 09 — Delivery dan testing

- [Delivery Roadmap](09-delivery/Roadmap.md)
- [Test Plan / UAT](09-delivery/Test-Plan.md)
- [Requirements Traceability](09-delivery/Requirements-Traceability.md)

## Contoh kontrak

- [Service Order JSON Example](contracts/service-order.example.json)
- [Policy Config JSON Example](examples/policy-config.example.json)

## Batasan penting

Google OAuth melalui Supabase Auth adalah login utama, sedangkan Supabase PostgreSQL RLS + API menegakkan hak akses. Cloudflare R2 menyimpan objek file; RLS hanya melindungi metadata DB, sehingga backend harus memeriksa izin sebelum URL privat dibuat. **IPL, sewa dan dana event hanya dicatat** sebagai pembayaran di luar platform; payment gateway dan Kantong hanya untuk layanan PortalHub sendiri.

Setiap file berlabel *proposed*, *draft*, *TBD* atau *not implemented* tidak boleh dianggap keputusan produksi. Belum ada implementasi, migrations, credential ataupun CI yang dinyatakan siap tanpa bukti terverifikasi.

## 11 — Agent operations (draft)

- [Autonomous Development Policy](11-agent-operations/AUTONOMOUS-DEVELOPMENT.md)
- [Multi-Agent Collaboration Protocol](11-agent-operations/MULTI-AGENT-PROTOCOL.md)
- [Implementation Defaults](11-agent-operations/IMPLEMENTATION-DEFAULTS.md)
- [Agent Task Contract & Review Gate](11-agent-operations/AGENT-TASK-CONTRACT.md)

Dokumen ini merupakan pedoman tambahan untuk AI coding agent paralel, **belum keputusan implementasi/produksi yang final**. Ikuti [Roadmap](09-delivery/Roadmap.md), [Decision Register](00-product/Decisions.md) dan [AI-Agents](AI-Agents.md) sebagai acuan yang tetap berlaku.

## Kesiapan eksekusi agent — audit 21 November 2026

- [Agent Readiness & Go/No-Go Checklist](11-agent-operations/AGENT-READINESS-CHECKLIST.md)
- [Agent Execution Backlog dan dependency DAG](09-delivery/Agent-Execution-Backlog.md)
- [Decision Closure Register](09-delivery/Decision-Closure-Register.md)
- [API Contract Coverage Matrix](08-operations/API-Coverage.md)
- [OpenAPI 3.1 design draft](08-operations/OpenAPI.yaml) — kontrak tambahan, **bukan endpoint yang sudah diimplementasikan**
- [Documentation CI script](../scripts/check_docs.py) dan [GitHub Actions workflow](../.github/workflows/docs-quality.yml)

Panduan baru **tidak mengesahkan** keputusan C/D, tidak menunjukkan CI sudah lulus, dan tidak menggantikan aturan [AGENTS](../AGENTS.md). Agent boleh mulai pekerjaan aman fase 0; pengembangan paralel dan produksi memiliki gate terpisah.
