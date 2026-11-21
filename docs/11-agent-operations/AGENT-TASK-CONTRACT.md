# Agent Task Contract & Review Gate — PortalHub

> **Status: DRAFT.** Template standar untuk menugaskan pekerjaan kepada satu atau banyak AI coding agent. Berlaku bersama [`AGENTS.md`](../../AGENTS.md), [`AI-Agents.md`](../AI-Agents.md), [`Roadmap.md`](../09-delivery/Roadmap.md), [`Requirements-Traceability.md`](../09-delivery/Requirements-Traceability.md), [`AUTONOMOUS-DEVELOPMENT.md`](AUTONOMOUS-DEVELOPMENT.md), dan [`MULTI-AGENT-PROTOCOL.md`](MULTI-AGENT-PROTOCOL.md). Template ini tidak mengesahkan operasi produksi atau credential.

## 1. Prinsip kontrak tugas

Setiap task hanya boleh mempunyai **satu accountable owner**, satu ID unik, tujuan yang terukur, dan *scope* terbatas. Sebelum menjalankan task, agent harus tahu apa yang boleh diubah, apa yang tidak, kontrak apa yang perlu dijaga, siapa pemilik integrasi, serta bukti yang diperlukan untuk menandai selesai.

**Status yang digunakan:** `backlog`, `ready`, `claimed`, `implementing`, `pr_open`, `in_review`, `changes_requested`, `approved`, `merged`, `verified`, `blocked`, `cancelled`. Status `verified` membutuhkan bukti; tidak boleh dilaporkan hanya dari penilaian agent.

## 2. Definition of Ready (DoR)

Task boleh diambil jika seluruh item berikut benar:

- [ ] Berada dalam fase [`Roadmap.md`](../09-delivery/Roadmap.md) yang diizinkan atau merupakan desain/test independen untuk dependensi kemudian.
- [ ] Task ID unik, *requirement ID*, target hasil dan acceptance criteria tersedia.
- [ ] Dependensi sudah merged, atau interface/mock contract yang sah tersedia.
- [ ] File/folder yang boleh diedit serta *shared-file owner* disepakati; tidak berkonflik dengan task lain.
- [ ] Risk class A/B/C/D ditentukan; tidak ada approval penting yang dianggap implisit.
- [ ] Pengujian dan review yang diperlukan dinyatakan.
- [ ] Feature flag/fallback untuk keputusan belum final dinyatakan bila relevan.

Jika satu item tidak terpenuhi, task diberi `blocked` atau dikembalikan ke `backlog`, **bukan** dimulai dengan asumsi tersembunyi.

## 3. Template GitHub issue / tugas agent (copy-paste)

```markdown
# [TASK-ID] Judul hasil yang spesifik

## Metadata
- Phase / milestone: [sesuai Roadmap.md]
- Requirement IDs: [PH-..., PK-..., BL-..., dll.]
- Status: backlog | ready | claimed | implementing | blocked | ...
- Risk class: A | B | C | D
- Owner agent: [satu agen]
- Reviewer: [agen/maintainer]
- Integration owner: [Lead/Integrator]
- Base branch / SHA: [main / commit SHA]
- Task branch: [agent/pX/TASK-ID-slug]

## Intent / outcome
[Kemampuan yang dihasilkan; bukan sekadar daftar file yang dibuat.]

## Authoritative references
- [docs/PRD.md section / requirement]
- [docs/09-delivery/Roadmap.md phase]
- [accepted Decisions.md / ADR atau status proposed]
- [domain doc / Permission Matrix / RLS Spec / OpenAPI]

## In scope
- [perubahan produk/komponen/schema/API yang diizinkan]

## Out of scope
- [fitur, domain, pembayaran atau infra yang tidak boleh disentuh]

## Files ownership
- Allowed paths: [...]
- Shared paths (requires integration owner): [...]
- Forbidden paths: [...]

## Dependencies & integration contracts
- Depends on: [ticket/PR/commit]
- Provides: [API/schema/event/component contract]
- Consumes: [API/schema/event/component contract]
- Tenant/role/resource scopes: [...]
- State transitions/idempotency: [...]
- Data/migration implications: [...]

## Acceptance criteria (verifiable)
- [ ] Given ..., when ..., then ...
- [ ] Negative case: unauthorized org/property/event/user is denied
- [ ] Failure/edge case: ...

## Required tests & evidence
- Unit: [command/suite]
- SQL/RLS integration: [command/suite]
- API contract/E2E: [command/suite]
- UI/SEO/PWA: [if relevant]
- Security/finance negative tests: [if relevant]

## Decision & fallback
- Open questions: [...]
- Engineering default (if safe): [...]
- Feature flag/mock: [...]
- Human approval required before: [...]

## Deliverables & handoff
- PR link: [after creation]
- Test result / CI link: [after execution]
- Migration/rollback notes: [...]
- Screenshots: [if UI]
- Docs/ADR/traceability changes: [...]
- Known risks / blocked follow-ups: [...]
```

## 4. Contoh penugasan konkret: HUB-001

> **Hanya contoh pemecahan task dari tiket `HUB-001` yang sudah disebut dalam roadmap.** Ini belum menyatakan ada PR, branch, test run atau keputusan stack final.

```markdown
# [HUB-001] Bootstrap monorepo dan pipeline build awal

- Phase: 0
- Requirement IDs: infrastructure enabler PH-001/PH-002 (traceability link); bukan bukti fitur selesai
- Status: backlog (ubah ke ready setelah integrator menyetujui batas stack)
- Risk class: B
- Owner: Repo/Tooling agent
- Reviewer: QA/Integrator
- Integration owner: Lead
- Depends on: keputusan engineering sementara untuk workspace (ADR-0001 masih proposed)

Intent:
Menyiapkan workspace monorepo yang dapat di-install, lint, typecheck, test dan build
secara reproducible tanpa menyambungkan credential atau layanan live.

In scope:
Root workspace, package scripts, lint/format config, smoke tests,
apps skeleton, shared config, basic CI workflow dengan data sintetis.

Out of scope:
Login Google production, schema tenant nyata, live provider payment,
R2 production, mengedit repository PortalWarga legacy, deploy production.

Shared paths:
Root package.json, lockfile, configs, docs/Architecture.md
(semua perubahan shared memerlukan integrator owner).

Acceptance:
- Fresh checkout dapat install dengan lockfile pinned.
- `lint`, `typecheck`, `test` dan `build` benar-benar berhasil di CI.
- Belum ada data/secret live; .env contoh hanya nama variabel non-rahasia.
- Apps skeleton tidak mengklaim auth, billing atau storage sudah berjalan.
- PR menjelaskan alasan stack sementara dan ADR/keputusan yang diperlukan.
```

## 5. Definition of Done (DoD)

Setiap item yang relevan wajib ditandai beserta bukti; `N/A` harus disertai alasan.

| Gate | Bukti minimum |
|---|---|
| Scope / requirements | PR mengutip task ID, requirement IDs, perubahan sesuai *in/out of scope* |
| Build & code quality | Commit + output lint/typecheck/unit/build yang dapat ditelusuri |
| Authorization | Negative tests untuk unauthorized org/product/property/event/self, kalau menyentuh data tenant |
| Database | Migration additive, FK/unique/RLS, rollback atau recovery plan, migration tests |
| Finance | State transitions, idempotency/replay/race/insufficient funds, audit; **mock-only** jika produksi belum approved |
| Files | R2 private authorization, scan/quarantine, quota, signed URL, no public leak bila menyentuh storage |
| Frontend | Loading/empty/error/forbidden, responsive, accessible, no private data flash/cache; screenshot bila relevan |
| Public SEO | Approved-only projection, canonical/sitemap/noindex, no PII in SSR bila menyentuh Ads |
| Operations | Error handling, logs sanitized, outbox/retry/metrics bila relevan |
| Documentation | Contract/doc/ADR diperbarui bila desain berubah; `Requirements-Traceability.md` berisi evidence sesuai mekanisme integrasi |
| Review | PR review independen, CI pada base terbaru dan konflik shared files selesai |

**Tidak boleh menandai selesai:** tes hanya direncanakan, provider tidak terverifikasi, secret belum ada sehingga kode tidak bisa dibangun, atau feature flag masih nonaktif tetapi fitur diklaim live. Gunakan `partial` di narasi dan `blocked` pada task yang memerlukan approval berikutnya.

## 6. Template PR untuk handoff antartim

```markdown
## Task & requirement
- Ticket / phase:
- Requirement IDs and authoritative documents:

## Implementation
- Changes and affected paths:
- API, schema, events, roles/scopes:
- Migrations / rollback:

## Verification (actual execution)
| Check | Command / CI link | Result |
| --- | --- | --- |
| Unit/lint/build | | Pass / Fail / Not run |
| RLS/security | | Pass / Fail / Not run |
| E2E/contract | | Pass / Fail / Not run |

## Safety & product decisions
- Risk class and approvals:
- Money/PII/permissions impact:
- Mock / disabled feature flags:
- ADR/decision-needed links:

## Traceability & handoff
- Requirements-Traceability rows updated or integration owner action:
- Known gaps / follow-up tasks:
- Screenshots / evidence:
- Reviewer + integration owner:
```

## 7. Template `decision-needed` tanpa menghentikan proyek

```markdown
# Decision needed: [AREA] [ringkasan]

- Source: [requirement, existing docs, conflicting statements]
- Decision class: C or D
- Owner: [product owner / legal / operator / domain authority]
- Options with tradeoffs: A / B / C
- Recommendation (non-binding): ...
- Safe fallback now: disabled / mock / config-only
- Blocked task IDs: ...
- Unblocked task IDs to continue: ...
- Acceptance test to add once approved: ...
- No auto-approval deadline: yes
```

Lead mengonsolidasikan pertanyaan yang sejenis; agent tidak menebak keputusan hanya karena belum ada jawaban.

## 8. Traceability dan update dokumen pusat

`docs/09-delivery/Requirements-Traceability.md` tetap menjadi matriks resmi. **Setiap perubahan requirement harus terefleksi sebelum merge**, tetapi jangan menugaskan beberapa agent menulis berkas itu serentak. Worker menyiapkan bukti/patch dalam PR; integration owner menyatukan perubahan matriks dan memverifikasinya, atau mengalokasikan satu PR khusus untuk update dokumen pusat. Status `implemented`/`tested` hanya boleh dicatat bersama referensi commit dan CI/UAT yang benar.

## 9. Acceptance / release gate berbeda dari DoD

DoD per task bukan izin rilis. Produksi memerlukan seluruh release gate pada [`MVP-and-Release.md`](../01-product/MVP-and-Release.md) dan [`Test-Plan.md`](../09-delivery/Test-Plan.md), termasuk negative RLS, payment idempotency, DB+R2 restore, kebijakan data, persetujuan hukum/provider yang dibutuhkan, serta sign-off product owner. Tidak ada otorisasi produksi yang timbul otomatis dari banyak PR yang sudah merged.