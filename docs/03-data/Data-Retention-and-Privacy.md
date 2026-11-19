# Data Retention & Privacy — PortalHub

**Status:** baseline policy design P1, **bukan nasihat hukum atau penetapan masa simpan final**. Keputusan legal/operasional Indonesia harus direview oleh pihak berwenang sebelum produksi.

## Data classes

| Class | Examples | Storage | Default exposure |
|---|---|---|---|
| Identity | Supabase user ID, display name, verified contact | Supabase Auth/DB | Private |
| Residents/tenants | House relation, lease, address, personal data | Supabase PostgreSQL | Private, scoped |
| Manual finance | IPL/sewa records, event cash, proof metadata | PostgreSQL + private Cloudflare R2 | Private, scoped |
| Platform billing | Invoice, Kantong ledger, provider reference | PostgreSQL + private R2 attachments if any | Billing role only |
| Public advertising | Approved listing title, public area, sanitized media | Public projection + R2 public | Public after consent/moderation |
| Operational security | Audit logs, failed login metadata, access history | Restricted DB/observability | Security authorized only |
| Temporary uploads | Unscanned objects, orphan intents, quarantine | Private R2 temp | No user/public access except controlled workflow |

## Data minimization and purpose

- Collect only fields required for explicit use case. Do not force every resident/tenant into Auth user account.
- Keep confidential home address, phone, ID document, transfer evidence and lease details away from public ads by default.
- Each public field needs owner publication approval/consent policy and records of version/actor. Withdrawal triggers unpublish and media takedown workflow.
- Limit access by tenant, product, role, property/household/event scope; platform support does not gain blanket file access.
- Do not put private document content, signed R2 URLs, full payment provider payload, auth/session tokens or identity numbers into logs, emails or notification bodies.

## Retention policy table (values unresolved)

| Category | Start of retention | Delete/hold handling |
|---|---|---|
| Auth profile/session | Account lifecycle | Provider/security/legal obligations |
| Resident/lease history | Relationship concluded | Export, lawful recordkeeping, review |
| Operational payment & finance | Financial record finalized | Audit/financial retention, legal hold |
| Service order/Kantong ledger | Platform financial posting | Immutable accounting retention; compensating corrections |
| Transfer proofs / contracts R2 | Object classification / record close | Document-class retention; private storage + metadata link |
| Unscanned temporary object | Upload intent expiry | Worker cleanup/reconciliation |
| Expired public ads and photos | Publication withdrawn | Unpublish/CDN invalidation; retention review |
| Security/audit logs | Event occurred | Risk-dependent authorized archive/erasure |

**No numerical period is approved here.** Each class requires `retention_policy_key`, legal basis/purpose, legal hold procedure, accountable owner, retention clock, deletion mechanism and audit log. Never delete payment/ledger records just because a user clicks delete.

## Subject data requests

1. Authenticate requester and verify legal relationship to person/organization.
2. Classify requested access, rectification, export or erasure; record request ID and due policy, without exposing cross-tenant data.
3. Locate in PostgreSQL and R2 via indexed `file_assets`/`file_links`; export permitted scope only and check private file access.
4. Apply permitted correction via versioning/reversal for financial records, or restrict/delete when legal basis allows. Legal holds and audit retention override immediate deletion as applicable.
5. Reconcile public ad projection and Cloudflare CDN copies; preserve transparent status and notify appropriately.
6. Audit fulfillment; protect downloaded export and ensure expiry/secure disposal.

## R2 lifecycle and backup

- Metadata soft deletion is distinct from object byte deletion; durable worker removes object **after** approved retention/hold, with retries and audit.
- Orphan upload/unfinished multipart cleanup must not remove files referenced by valid records.
- Storage backups and DB backups have their own retention and restoration rules; erasure handling should consider backup expiry and legal obligations.
- Public CDN takedown is best effort within the configured control; copies outside PortalHub may be beyond immediate removal.
- Region/cross-border transfer, consent, processor agreements, retention periods and breach notification obligations require qualified compliance review.

## Tests and launch gate

- Resident A cannot export data of resident B or private docs from another org.
- Verified consent withdrawal removes listing and public derivative (including cache controls).
- Orphan cleanup does not delete active file; legal hold prevents deletion.
- Backup/restore does not reintroduce unapproved public publication or cross-tenant rights.
- Deletion audit contains actor/reason without exposing document bytes.

**Related:** [Security](../04-security/Security-Privacy.md), [R2 Storage](File-Storage.md), [Disaster Recovery](../08-operations/Disaster-Recovery.md), [Ads Publishing](../06-products/PortalIklan-Publishing-Rules.md).
