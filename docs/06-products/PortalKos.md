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
