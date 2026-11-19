# PortalKos product specification

## Persona

Owner, manager, finance, guard/staff per property, tenant self. Tenant record may exist without login.

## Key modules

- Properties: alamat privat, nama, fasilitas, pengaturan.
- Units: tipe kamar, harga, status, occupancy, foto, amenity, service history.
- Tenant/leases: data penyewa, occupants, start/end, deposit jaminan (pencatatan), kontrak.
- Billing records: schedule, invoice/charge, record cash/transfer, optional evidence, internal verification.
- Expenses + reports: per property and overall; occupancy, overdue, income/expense trends.
- Maintenance: ticket, assignment, updates.
- Listing publication: explicit opt-in, source sync, moderation.

## Invariants

One organization holds many properties; one subscription quota counts active rentable units across all properties. Property assignments enforce scope. Avoid overlapping active lease for a single-exclusive unit. A unit becoming occupied triggers listing availability update; eventual consistency tracked with outbox retry.

## Views

Desktop: combined KPI + filters/tables, drill down by property. Mobile: compact KPI, property cards, quick add payment/maintenance, bottom navigation.

## Tenant portal

Read own lease, bills, payment record, notices, complaints. No read access to other tenant data; tenant may hold more than one lease. Never accept tenant ID directly from browser as sole auth filter.


## Dokumen dan foto dengan Cloudflare R2

Kontrak sewa, dokumen penyewa, lampiran maintenance dan bukti transfer disimpan private di R2; metadata, org/property/lease/payment link dan izin berada di Supabase PostgreSQL + RLS. Tenant hanya dapat akses kontrak/bukti miliknya; petugas hanya pada properti assigned. Public listing hanya dapat memakai foto derivatif yang telah di-opt-in pemilik, di-scan dan dimoderasi; jangan menyalin identitas/kontrak ke bucket publik. [File Storage](../03-data/File-Storage.md).
