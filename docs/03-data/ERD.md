# ERD high-level

```mermaid
erDiagram
 AUTH_USER ||--|| PROFILE : has
 AUTH_USER ||--o{ ORGANIZATION_MEMBER : joins
 ORGANIZATION ||--o{ ORGANIZATION_MEMBER : has
 ORGANIZATION ||--o{ ORGANIZATION_PRODUCT : subscribes
 ORGANIZATION_MEMBER ||--o{ ROLE_ASSIGNMENT : receives
 ROLE ||--o{ ROLE_ASSIGNMENT : grants
 ORGANIZATION ||--o{ KOS_PROPERTY : owns
 KOS_PROPERTY ||--o{ KOS_UNIT : contains
 KOS_UNIT ||--o{ KOS_LEASE : rented_by
 ORGANIZATION ||--o{ WARGA_HOUSE : manages
 ORGANIZATION ||--o{ WARGA_EVENT : hosts
 WARGA_EVENT ||--o{ WARGA_EVENT_MEMBER : assigned
 WARGA_EVENT ||--|| EVENT_CASHBOOK : records
 ORGANIZATION ||--o{ AD_LISTING : advertises
 ORGANIZATION ||--|| BILLING_ACCOUNT : bills
 BILLING_ACCOUNT ||--o{ SERVICE_ORDER : buys
 BILLING_ACCOUNT ||--|| WALLET : owns
 WALLET ||--o{ WALLET_LEDGER : posts
 SERVICE_ORDER ||--o{ PLATFORM_PAYMENT : funds
 BILLING_ACCOUNT ||--o{ SUBSCRIPTION : maintains
```

Diagram konseptual; migrasi SQL detail harus memperkuat FK tenant, constraints event account, RLS dan unique idempotency.


## ERD — Cloudflare R2 file references

```mermaid
erDiagram
 ORGANIZATION ||--o{ FILE_ASSET : owns
 AUTH_USER ||--o{ FILE_ASSET : uploads
 FILE_ASSET ||--o{ FILE_LINK : referenced_by
 FILE_ASSET ||--o{ FILE_UPLOAD_INTENT : uploads
 FILE_ASSET ||--o{ FILE_ACCESS_AUDIT : audited
 FILE_ASSET ||--o{ FILE_VERSION : revision
```

`FILE_ASSET` dan `FILE_LINK` berada di Supabase PostgreSQL/RLS; byte file berada di R2. Referensi payment/event/lease/listing bersifat domain-specific dan harus memiliki FK/validasi scope (diagram ini tidak mengizinkan polymorphic IDs tanpa validasi). Lihat [File-Storage.md](File-Storage.md).
