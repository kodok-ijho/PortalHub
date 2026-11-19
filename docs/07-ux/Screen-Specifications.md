# Screen Specifications — Mobile First / Desktop

**Status:** initial screen-level UX contract P1; not finished wireframes or running screens. Design language: Clean Minimal × Mobile First PWA. See [Design System](../Design-System.md).

## Global shell

- Header: current organization/product context, clear role, account controls. If one eligible context, open permitted landing; if many, user selects.
- Mobile: role-sensitive bottom navigation (4–5 primary destinations) and accessible "Lainnya". Desktop: sidebar, search, bulk actions, tables, filters, optional split-view.
- Every private screen supports `loading`, `empty`, `error`, `forbidden`, `offline` and `success` where appropriate. Unauthorized data **never** briefly flashes before permission resolves.
- No sensitive cached data retained when user logs out, switches org, or loses membership; monetary actions and contract changes network-only.
- Accessible actions: keyboard navigation, visible focus, form errors linked to input, touch target minimum recommended 44px, contrast review.

## Screen inventory and user actions

| Screen/route | Persona | Main content | Safe states/guards |
|---|---|---|---|
| `/` | Public | Product overview, login, plans (when approved) | No private tenant data |
| `/login` | Anonymous | **Continue with Google**, optional email OTP | OAuth error, safe return path |
| `/app` | Signed in | Portal Saya, org/product switcher, onboarding | 0/1/multiple contexts |
| `/app/subscription` | Billing actor | Current plans, quota, expiry, renewal opt-in, orders | Billing permission, no stealth charge |
| `/app/kantong` | Billing actor | Balance; **Top Up / Transaksi / Payment** tabs | Insufficient funds, pending, settled, audit |
| `/kos/:orgSlug/dashboard` | Kos owner/manager | Occupancy, arrears, unit quota, property selector | Property scope, aggregated across allowed units |
| `/kos/:orgSlug/properti/:propertySlug` | Kos staff | Units, leases, charges, tickets, photos | Scoped resource, no leakage |
| `/kos/:orgSlug/penyewa` | Tenant self | Own lease, bills, payment proof, notices | Verified tenant link only |
| `/warga/:orgSlug/beranda` | Resident | House/IPL status, announcements, events | Verified household link only |
| `/warga/:orgSlug/keuangan` | Treasurer | General cashbook, IPL verification, reports | Explicit finance role |
| `/warga/:orgSlug/event/:eventId` | Assigned committee | Event tasks, finance if granted | Event-specific role, no general treasury |
| `/iklan` | Public | Category, area, search, listings | Only published projection |
| `/iklan/:category/:city/:slug` | Public | Published detail, media, approved contact | No private R2 file or exact private address |
| Admin/moderation (route TBD) | Authorized admin | Organization verification, policies, ads moderation, audit | Platform access not blanket PII |

## Transactional flows

### Manual proof upload (IPL/sewa)

1. Select own bill/authorized payment, choose cash vs external transfer.
2. For transfer, optionally select evidence file; show file type/size/consent. Request upload intent.
3. `Uploading → Checking → Ready`; user can cancel/retry. **"Ready" means file safe/available, not transfer bank verified**.
4. Submit payment record with external method, amount and period; label `Menunggu verifikasi`.
5. Authorized finance verifies/rejects with reason; status clearly labelled `Terverifikasi internal`.
6. Preview/download from **private Cloudflare R2** only after reauthorization; never use public URL.

### Platform service checkout

- Show server-calculated service order, plan/price version, fee/tax disclosures when approved, funding choices **Kantong / QRIS direct / transfer direct / exact top-up+wallet**.
- Payment state visible: `pending`, `settled`, `failed`, `fulfilling`, `fulfilled`. Do not show success solely from browser redirect.
- Auto-renew toggles **off** until explicit consent; show next due and opt-out without removing paid term.
- Distinguish Top Up credit and Transaksi debit clearly; direct Payment tab never implies Kantong credit.

### Listing publishing

- Choose source unit/business, eligible public fields, photos and consent; preview exact public output.
- Submit to moderation. States `draft/pending/rejected/published/unavailable/expired` show allowed next actions and reason.
- Free quota/expiry shown before confirming publish; no implicit upgrade to paid.

## Forms/components

- `MoneyField` uses integer IDR validation and formatted display, not floating point amounts.
- `EvidenceUploader` and `DocumentUploader` display R2 scan state; stop reuse of rejected/quarantined files.
- `OrganizationSwitcher` resets scoped UI query cache; deep links display forbidden/404 safely.
- `StatusBadge` must distinguish R2 file ready, internal recorded payment and platform provider settled (different semantics).
- No hardcoded plan price, retention period, late fee or domain until approved.

## Acceptance checklist

- All screens tested at 320, 375, 768, 1024 and 1440px with accessible keyboard and screen reader labels.
- Tests cover loading/empty/error/offline, permission revocation during session, multi-org switching, no private flash.
- Financial confirmation happens only after actual authorized transaction state.
- Ads SSR/public HTML contains only published projection and safe media.
- PWA caching disallows private R2 assets, financial responses and auth session.

**Reference:** [Journeys](Routes-and-Journeys.md), [Auth](../04-security/Auth-and-SSO.md), [Payment State Machines](../05-billing/Payment-and-Wallet-State-Machines.md).
