# Workflow bisnis

## Login / pemilihan akses

```mermaid
flowchart TD
 A[Open deep link] --> B{Authenticated?}
 B -->|No| C[Login with safe return path]
 C --> D[Load memberships/products/scopes]
 B -->|Yes| D
 D --> E{Eligible contexts count}
 E -->|0| F[Onboarding or invitation]
 E -->|1| G[Direct redirect to authorized page]
 E -->|Many| H[Organization / product selector]
 H --> G
```

## Organization activation

```mermaid
flowchart TD
 A[Create organization] --> B[Resolve platform/product/org policy]
 B --> C{Policy mode}
 C -->|Auto| D[Product active with minimal permissions]
 C -->|Approval| E[Draft setup]
 E --> F[Verification requested]
 F --> G{Verified?}
 G -->|Yes| H[Grant sensitive management]
 G -->|No| E
 C -->|Invite-only| I[Admin invite needed]
 I --> D
```

## Operational payments

```mermaid
flowchart LR
 A[External bank transfer or cash] --> B[User records transaction]
 B --> C[Pending internal verification]
 C -->|Approved by finance| D[Verified internal]
 C -->|Rejected| E[Rejected/correction]
 D --> F[Operational report]
```

## Services billing

```mermaid
flowchart TD
 A[Service order] --> B{Payment method}
 B -->|Kantong| C[Atomic debit ledger]
 B -->|QRIS/transfer direct| D[Provider checkout]
 B -->|Top-up exact invoice| E[Top-up order]
 E --> F[Provider settled]
 F --> G[Wallet credit ledger]
 G --> C
 D --> H[Verified provider webhook]
 C --> I[Fulfillment idempotent]
 H --> I
 I --> J[Subscription/package/listing entitlement]
```

## Kos availability → listing

```mermaid
flowchart TD
 A[Unit available] --> B{Owner opted to publish?}
 B -->|No| C[Private only]
 B -->|Yes| D[Public content review]
 D --> E[Moderation]
 E --> F[Published and indexed]
 F --> G{Unit rented?}
 G -->|Yes| H[Mark unavailable, retain canonical URL]
 G -->|No| I[Expiry/renewal policy]
```

## Event account transfer

Kas utama --debit transfer--> clearing internal --credit transfer--> kas event. Dua baris yang dipautkan `transfer_id`; dikecualikan dari pendapatan/beban konsolidasi. Semua event reports event_id scoped.
