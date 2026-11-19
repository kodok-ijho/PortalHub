# ADR-0001 — Modular Monolith

**Status:** Proposed for engineering ratification · 2026-11-19.

## Context

PortalHub has three products sharing auth/org/billing but separate operational finance domains. Small initial team benefits from low operations overhead, yet public ads needs SEO SSR.

## Decision

Start modular monolith with typed domain boundaries, Supabase Postgres RLS, React/Vite private PWA, Next.js public ads frontend as deployable module. Shared packages for design system/contract. Cross-domain writes through services and outbox.

## Consequences

+ Simpler infra, reuse legacy React components.
+ Isolate SSR advertising from private app.
− Requires strict code boundaries, data access discipline, coordinated DB migration.

## Alternatives

Single Next.js app for all products; full microservices. Re-evaluate if monorepo routing overhead becomes excessive; benchmark first.
