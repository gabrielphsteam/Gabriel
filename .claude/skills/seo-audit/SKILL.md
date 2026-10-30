---
name: seo-audit
description: Audit a website or page for technical, on-page and content SEO issues and produce a prioritized fix list. Use when the user mentions SEO audit, not ranking, traffic drop, indexing problems, meta tags, page speed or Core Web Vitals.
---

# SEO Audit

## Inputs
URL or repo, target keywords and audience, country/language, and access to Search Console data if available.

## Checks
**Technical**
- Crawl and index: robots.txt, sitemap.xml, status codes, redirect chains, canonical tags, noindex, hreflang
- Performance: Core Web Vitals (LCP, INP, CLS), image sizes and formats, render-blocking resources
- Mobile friendliness, HTTPS, duplicate URLs (www, trailing slash, parameters)

**On-page**
- Title (about 50 to 60 characters) and meta description (about 150 to 160) unique per page
- One H1, logical H2/H3 structure, keyword and intent match
- Image alt text, internal links with descriptive anchors, URL structure
- Structured data (Organization, Article, Product, FAQ, Breadcrumb) valid and relevant

**Content**
- Search intent match, depth versus competitors, thin or duplicate pages, outdated content
- E-E-A-T signals: authorship, sources, contact and about pages

**Off-page**
- Backlink quality and gaps, brand mentions (only if data is available)

## Method
Fetch pages and inspect real HTML and headers instead of guessing. Mark anything you could not verify as "not verified".

## Output
Table with: issue, where, impact (high/medium/low), effort, fix. Then a top-5 quick-win list and a 30-day plan. Do not claim ranking results; SEO outcomes are not guaranteed.
