# PortalHub — Coding Agent Entry Point

PortalHub is currently in the **documentation/design stage**. Do not claim production readiness or existing implementation when only specifications exist.

Read these first:
1. [README.md](README.md) — project summary and current state.
2. [docs/AI-Agents.md](docs/AI-Agents.md) — authoritative AI coding rules.
3. [docs/PRD.md](docs/PRD.md), [docs/Architecture.md](docs/Architecture.md), [docs/Design-System.md](docs/Design-System.md).
4. [docs/README.md](docs/README.md) — all domain documents, including [Requirement Traceability](docs/09-delivery/Requirements-Traceability.md).

Critical principles:
- Supabase Auth with Google OAuth is primary login. RLS, server permission and scoped organization membership enforce authorization.
- Cloudflare R2 is primary file storage; Supabase RLS only governs metadata, not R2 objects.
- Kantong is closed-loop credit for **PortalHub services only**. Do not route IPL/rent/event funds through PortalHub.
- Owner/org roles do not automatically grant event-finance or property scope; deny by default.
- No charging without consent; no ledger updates without idempotency and audit.
- Do not edit legacy `kodok-ijho/PortalWarga` without separate explicit authorization.
- Keep change sets small, test cross-tenant failures, and update docs/traceability for every requirement change.
- **Never create, request, include or publish credential values in documentation, source examples, pull requests or logs.** Credential setup is outside the current documentation scope.

See [docs/AI-Agents.md](docs/AI-Agents.md) for complete policies.
