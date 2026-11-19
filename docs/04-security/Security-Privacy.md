# Security & privacy baseline

## Threats

Cross-tenant disclosure, privilege escalation, listing leakage, fraudulent payment callbacks, wallet replay/double debit, malicious file upload, stale PWA cache, insecure support access, XSS from listing descriptions, mass enumeration of private entities.

## Required controls

- Supabase RLS per tenant with negative integration tests; server-side checks for all mutations; no service-role token in frontend.
- MFA/re-auth for billing owner/policy edits as supported; per-IP/account rate limits for login/invites/lead forms.
- Signed/verified payment webhooks, provider amount reconciliation, secrets in server environment only.
- Money ledger immutable, audit log append-only, actor and request IDs, privileged actions with four-eyes review where appropriate.
- Evidence uploads private bucket, MIME validation, size cap, virus scan if possible, short-lived signed URL, retention policy.
- PII minimization and explicit publishing consent; mask residence address, tenant data, owner phone by default.
- HTTPS, security headers (CSP/etc), CSRF protections where cookies used, parameterized SQL, dependency audit.
- Data export/erasure requests handled respecting financial audit retention requirements; detailed legal retention window to be decided.
- Public ad markup escapes user content; reporting and moderation; no personal data in sitemap/robots/cache.

## Legality gates

Indonesia personal-data obligations, consumer protection, tax invoice requirements, payment provider agreements, wallet/store-value treatment and refund terms require qualified legal/compliance review. Do **not** represent this doc as legal advice or claim Kantong has regulatory exemption.

## Incident runbook minimum

Detect → contain (disable affected capability, revoke keys) → preserve logs → identify tenant blast radius → recover from verified backup → notify responsible parties according to applicable obligations → postmortem. Review restore testing before public launch.
