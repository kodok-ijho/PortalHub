# Agent Readiness & Go/No-Go — PortalHub

> **Status: draft operational checklist, not production approval.** Membantu memutuskan kapan agent boleh mulai coding, kapan pekerjaan boleh paralel, dan kapan release boleh diklaim selesai. Roadmap utama: [Roadmap](../09-delivery/Roadmap.md), [MVP](../01-product/MVP-and-Release.md). Credential tidak dicatat di repo.

## Tiga tingkat kesiapan yang berbeda

| Gate | Tujuan | Bukti minimum | Status per 21-11-2026 |
|---|---|---|---|
| **G0 — Mulai coding aman** | Bootstrap fase 0, kontrak, mock, schema & tes | Agent membaca docs; scope/tiket jelas; tidak memerlukan uang/live data; reversible; branch terpisah | **Dapat dimulai**, dengan asumsi operator menyediakan akses GitHub yang sesuai |
| **G1 — Kolaborasi paralel terkontrol** | Beberapa agent mengerjakan tiket berbeda dengan aman | Owner integrasi; dependency DAG; agreed contracts; branch protection/ruleset; CI dan review aktif; no conflicting migrations | **Belum terverifikasi** |
| **G2 — Rilis production** | Produk dan provider live | UAT, auth/RLS negatif, finance replay, DB+R2 restore drill, monitoring, SLO/RPO/RTO, persetujuan legal/provider/privacy/pricing & owner sign-off | **Blocked** |

G0 bukan bukti G1, dan G1 bukan izin G2. Setiap fase roadmap harus lulus acceptance gate-nya sendiri. Satu label `verified` hanya sah bila ada bukti CI/PR/commit dan acceptance yang disebut dalam kontrak.

## Checklist sebelum Lead mengaktifkan banyak worker

- [ ] Root `AGENTS.md`, `docs/AI-Agents.md` dan empat dokumen `docs/11-agent-operations/` dibaca, serta status **draft** dipahami.
- [ ] ADR-0001 dan pilihan stack dibuat keputusan engineering eksplisit sebelum mengunci monorepo utama; semua alternatif direkam.
- [ ] Pekerjaan GitHub tercatat dalam Issues/tiket dengan requirement, phase, owner, dependencies, scope path, negative tests dan acceptance.
- [ ] File bersama (migrations, `OpenAPI.yaml`, lockfile, traceability) punya satu integration owner/merge queue.
- [ ] Pull request **wajib** review independen; direct push `main` dan force-push dilarang melalui settings/ruleset GitHub; bukan sekadar aturan tertulis.
- [ ] CI benar-benar dieksekusi dan required checks dilindungi; job yang belum mungkin dilakukan diberi status belum tersedia, bukan pass.
- [ ] Agent credential/permission: least privilege, token tidak disalin ke docs/log/issues, tidak ada akses uang produksi atau data warga nyata.
- [ ] Synthetic seed, secure test data, local/staging sandbox tanpa provider live; mock dan feature flags fail-closed.
- [ ] Dokumen central contracts dan keputusan C/D memiliki mekanisme proposal/approval, bukan pengesahan otomatis.

## Exit gate per fase

1. Ambil target fase dan acceptance dari `Roadmap.md` serta `MVP-and-Release.md`.
2. Daftarkan requirement ID, PR merged, commit, CI run, negative/security tests, dan hasil UAT terkait.
3. Lakukan review independen: permission/scope, payment/idempotency (bila relevan), retention/PII, public SEO, dan storage.
4. Tidak menandai lulus jika decision `blocked` berpengaruh terhadap fitur tersebut. Tandai fitur `partial/mock-only/disabled`; lanjutkan dependensi aman bila memungkinkan.
5. Lead memelihara `Requirements-Traceability.md`; jadwalkan review persetujuan pemilik produk untuk keputusan kelas C/D secara terkelompok.

## Yang tetap dibutuhkan dari manusia

Persetujuan kebijakan bisnis, pricing/kuota/trial, provider dan legal Kantong, privacy/retention, live payment, migrasi legacy/data nyata, rilis produksi, serta konfigurasi akses/infrastruktur. Developer dapat mengimplementasikan **konfigurasi** sebelum angka/batas bisnis final, tetapi tidak boleh menganggap nilai fixture adalah keputusan produksi.

## Sumber aksi

- [Execution Backlog](../09-delivery/Agent-Execution-Backlog.md): ticket, DAG, area yang tidak bisa diparalelkan.
- [Decision Closure](../09-delivery/Decision-Closure-Register.md): blocked vs nonblocking dan apa yang membutuhkan approval.
- [API Coverage](../08-operations/API-Coverage.md): status kontrak dan aturan contract-first.
- [Multi-Agent Protocol](MULTI-AGENT-PROTOCOL.md): branch/worktree/PR/merge.
