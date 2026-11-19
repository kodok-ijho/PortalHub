# PortalIklan — Marketplace iklan & SEO

## Positioning

Public catalog of kos, kontrakan, local food, laundry, bakery, shops and services. **No PortalHub checkout for transactions between advertiser and buyer.** CTA goes to contact/WhatsApp/form interest only.

## Publication lifecycle

Source PortalKos vacant unit (opt-in) or PortalWarga user business (phase after Kos); draft → review → published → expired/unavailable/rejected. Owner can pause. Update listing status when source unit occupied; retain public URL with unavailable status and related suggestions if content remains valid.

## Initial free quota + packages

Free count and time-limited from configured plan; all ads have dates. Paid extensions require explicit auto-renew consent, wallet available, or direct checkout; no automatic conversion from free. Distinguish monetary wallet balance from purchased package credits.

## SEO requirements

- Next.js SSR/SSG (proposed), first response returns meaningful HTML to crawlers.
- Detail route `/iklan/:category/:city/:slug` with ID suffix for slug collision, stable canonical URL.
- Unique title/description, H1, breadcrumbs, semantic HTML, structured schema types suited to listing (not invented ratings), sitemap index + incremental listing updates.
- Index only approved, public content; noindex rejected/draft/private pages; 404/410 for removed content based on policy.
- Location/category SEO landing pages must contain useful unique content and search filters; avoid thin/duplicate pages.
- Image responsive, webp/avif, descriptive alt, LCP/INP/CLS measured.
- Business contact & location only with explicit consent. Published address can be area-level, not home GPS.

## Moderation & abuse

Duplicate checks, spam reporting, restricted/prohibited categories according to content policy, time-to-moderate metrics, rate limits, safe file scanning, anti-scam warning, paid promotion labeling.

## Growth metrics

Search impressions/clicks from verified analytics, organic landing pages, listing conversion/contact CTR, time-to-fill vacant units, active listings, rejection rates, ad expiry retention.


## Cloudflare R2 public listing media

Foto iklan masuk bucket private/temp R2 hingga diverifikasi ukuran/MIME, scan, consent dan moderasi. Hanya gambar derivatif yang disanitasi (EXIF lokasi dihapus) yang diterbitkan ke **public R2 bucket**. URL publik memakai custom CDN domain Cloudflare saat tersedia; jangan embed signed private URL pada HTML SSR, sitemap, metadata OG atau structured data. Saat listing berakhir/unpublish, jalankan takedown & cache invalidation; foto publik dengan key berversi dan alt text yang tepat. Kuota & pemrosesan gambar dipantau. [File Storage](../03-data/File-Storage.md).
