# PortalWarga product specification

## Legacy direction

Reuse concepts from `kodok-ijho/PortalWarga`: residents, houses, IPL matrix, expense, docs, events, event finance and event assignment. Do not copy legacy payment settlement assumptions.

## Key modules

Houses/blocks; resident membership, occupancy; IPL schedules and bills; manual cash/transfer payment records and internal verification; operational cashbook and reports; documents/announcements; event management/assignments/RSVP as validated; **event-specific financial accounts**; classifieds/ads of warga businesses.

## Event finance

Event has budget, members with event-scoped role, income, expense, separate account. Event members never gain global treasurer rights just by joining one event. Optional transfer from main cashbook must have two linked entries. Report has event, main, consolidated views with internal transfer elimination.

## Access

Org approval policy before organization-wide sensitive resident access. Self-resident reads only verified house/household relationship and own bill. Treasurer sees finance as granted; coordinator reads assigned block; panitia only assigned event. Residents without email don't require login account.

## Business Ads

Advertiser must approve public photo, phone, city/area; no automatic publication of private household records. Org moderator and platform moderator may review based on policy.


## Dokumen warga/event & bukti IPL — Cloudflare R2

Simpan bukti transfer IPL, lampiran kas, surat organisasi, dokumen rumah dan event di R2 private. Metadata dalam Supabase dengan scope rumah/blok/event; akses baca/tulis harus diverifikasi backend per file, bukan sekadar role global. Panitia event tidak mendapat akses kas utama secara implisit. Foto usaha warga untuk PortalIklan perlu consent, moderasi, sanitasi dan salinan media publik terpisah. Berkas privat PortalWarga legacy harus diaudit sebelum migrasi. [File Storage](../03-data/File-Storage.md).
