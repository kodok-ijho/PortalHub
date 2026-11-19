# RBAC + permission + scope

## Model

`allow = active_user AND active_membership(org) AND product_entitled AND role_grants(permission) AND scope_allows(resource) AND policy_guardrails`. Default deny. Akses platform tidak otomatis memberi akses ke PII tenant; support temporary access requires approval and audit.

## Roles

| Domain | Built-in roles |
|---|---|
| Platform | owner, admin, support-limited, moderator |
| Org | owner, admin, billing_manager, viewer |
| Kos | owner, manager, finance, staff, tenant-self |
| Warga | ketua, pengurus, sekretaris, bendahara, koordinator_blok, event_leader, event_treasurer, event_member, warga-self |
| Ads | advertiser, organization_moderator, platform_moderator, public-viewer |

Organization owner tidak otomatis menjadi bendahara event; product-role assignment disyaratkan bila perlu. Event roles assigned **per event**, bukan global role. Property roles assigned **per property**.

## Permission matrix (minimum)

| Permission | Owner | Manager/Admin | Finance | Staff | Self |
|---|---:|---:|---:|---:|---:|
| `hub.billing.manage` | ✓ | by grant | — | — | — |
| `hub.wallet.topup` | ✓ | by grant | — | — | — |
| `hub.wallet.autorenew.manage` | ✓ | by grant | — | — | — |
| `kos.unit.manage` | ✓ | scoped | read | scoped | — |
| `kos.payment.record` | ✓ | scoped | ✓ | by grant | — |
| `kos.payment.verify` | ✓ | by grant | ✓ | — | — |
| `kos.lease.read_own` | — | — | — | — | ✓ |
| `warga.ipl.record` | ✓ | by grant | ✓ | by grant | — |
| `warga.ipl.verify` | ✓ | by grant | ✓ | — | — |
| `warga.event.finance.read` | ✓ | by grant | all assigned | assigned event | — |
| `warga.event.finance.write` | ✓ | by grant | all assigned | event treasurer only | — |
| `ads.listing.publish` | ✓ | by grant | — | source approved | own listing, subject moderation |

✓ tetap bersyarat domain/org/scope. Detail custom role UI paska MVP; platform security hard requirements tidak dapat dicabut.

## Invite, lifecycle, last-owner

Invitation token hashed, expires, one-time; email match and verified account binding. Pending member has no operational permissions. Revoke immediately invalidates server authorization even if client session still active. Prevent removing last active owner; ownership transfer requires audit and reauthentication.

## Configurable onboarding

Policy resolution: platform mandatory guardrails > authorized org override > product default > platform default. Modes: automatic, approval, invite-only. **Override hanya oleh platform authorized admins.** Policy versioned and effective forward for new applications; applying to existing org is explicit migration with audit.

## Negative tests

User A org X reads org Y finance → 403/empty; Kos A staff reads Kos B lease via forged UUID → 403; event treasurer A sees event B → 403; tenant sees others' invoices → 403; public sees draft ad → 404; user forges `role` or `org_id` in request → forbidden.
