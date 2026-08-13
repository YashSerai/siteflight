# The SiteFlight 40

Read all 40 checks before auditing. Each check requires a status and evidence. “Conditional” means `NOT APPLICABLE` is allowed only with a site-specific reason.

## Discovery and machine readability

### 01. Sitemap.xml

Pass when a valid, reachable XML sitemap contains the canonical indexable URLs and is referenced from `robots.txt` or submitted in Search Console. Check for stale, redirected, blocked, or non-canonical URLs.

### 02. Rich results readiness

Pass when structured data matches visible content, validates for the intended rich-result type, and contains no invented fields. If the user literally means UI tooltips, audit those separately for accessible names, keyboard, touch, focus, and dismissal.

### 03. Canonical tags

Pass when every indexable page has one absolute self-referencing canonical, unless a deliberate cross-canonical is documented. Canonicals must resolve without redirecting to the wrong locale or protocol.

### 04. Site favicon

Pass when a real brand favicon loads in supported formats and appears correctly in the rendered browser. A missing file, framework default, or invisible monochrome asset fails.

### 05. Tap-to-call phone number

Conditional for businesses that accept phone calls. Pass when the visible number is readable and the mobile action uses a correct `tel:` link. Do not place calls during an audit.

### 06. Form error messages

Pass when every public form has specific inline errors, preserves useful input, moves or announces focus appropriately, and works with keyboard and screen readers. Test invalid, empty, slow, offline, server-error, and success states when safe.

### 07. Opening hours

Conditional for businesses with customer-facing hours. Pass when hours are visible, current, timezone-aware, consistent across the site, and represented accurately in local-business schema.

### 08. Google Search Console

Pass only with account-side evidence that the correct canonical property is verified and the sitemap or indexing state has been checked. A verification meta tag alone is not enough.

## Content and trust

### 09. Five useful blog posts

Conditional when editorial content supports discovery or buyer education. Pass with at least five substantive, original, internally linked posts that answer real customer questions. Thin or generated filler fails.

### 10. About page with a story

Pass when the page explains who the business is, why it exists, who it serves, and provides specific, supportable details. A generic mission paragraph fails.

### 11. Before-and-after gallery

Conditional for work with a visible transformation and with customer permission. Pass when examples are authentic, clearly labeled, accessible, performant, and not misleading.

### 12. Separate page per service

Conditional for multi-service businesses. Pass when each meaningful service has a distinct useful page with unique intent, copy, metadata, proof, and CTA. Doorway pages or near-duplicates fail.

### 13. Visible email address

Conditional when email is a supported contact channel. Pass when a readable address is visible where users expect it and the `mailto:` link is correct. A form alone does not satisfy this check.

### 14. Working social links

Pass when every visible social link opens the correct active profile, uses safe external-link behavior, and has an accessible name. Remove dead or empty profiles.

### 15. Compressed images

Pass when delivered images are appropriately sized and encoded, use responsive sources where useful, avoid layout shifts, and preserve acceptable visual quality. Check bytes, intrinsic dimensions, rendered dimensions, and loading behavior.

### 16. Working cookie consent

Conditional based on tracking and jurisdiction. Pass when consent choices are clear, equally usable, remembered, reversible, keyboard accessible, and actually govern non-essential tags. A decorative banner that loads tracking first fails.

### 17. llms.txt

Pass when `/llms.txt` is reachable, plain text, concise, accurate, and links to canonical public resources. Treat it as supplemental guidance, never an access-control or SEO guarantee.

### 18. Terms of service

Conditional based on the site's transactions and relationship with users. Pass when the page is reachable, current, identifies the business, and matches the service. Recommend qualified legal review rather than inventing terms.

### 19. Clear payment methods

Conditional for paid products or services. Pass when accepted methods, timing, currency, deposits, financing, and relevant limitations are explained before commitment. Do not infer methods from payment-provider logos alone.

### 20. Guarantee statement

Conditional when the business offers a guarantee. Pass when scope, exclusions, duration, claim process, and responsible business are clear. If no guarantee exists, recommend honest risk-reversal copy rather than fabricating one.

## Conversion and navigation

### 21. Custom 404 page

Pass when an unknown URL returns HTTP 404, uses the real site shell, explains what happened, and offers useful navigation. A branded page returning 200 fails.

### 22. Clear calls to action above the fold

Pass when the primary next action is visible and understandable without scrolling at representative desktop and phone sizes. The CTA must match the page intent and lead somewhere that works.

### 23. Internal links

Pass when important pages are reachable through contextual links and navigation, with descriptive anchor text and no broken, redirected, orphaned, or circular traps.

### 24. Thank-you page after inquiry

Conditional for inquiry forms. Pass when successful submission reaches a distinct confirmation state or URL, sets expectations, preserves privacy, avoids duplicate submission, and supports conversion measurement. Do not submit to real recipients without approval.

### 25. Breadcrumbs

Conditional for sites with hierarchy beyond a shallow brochure. Pass when visible breadcrumbs reflect the real hierarchy, are keyboard accessible, link correctly, and match `BreadcrumbList` structured data.

### 26. Case study section

Conditional when project evidence exists and permission allows publication. Pass when case studies name the problem, work, constraints, and supported outcome without invented metrics.

### 27. Five frequently asked questions

Pass with at least five useful, visible questions based on real buyer friction. Answers must be specific and consistent with the service. FAQ schema must match the visible text if used.

### 28. Response-time promise

Conditional for inquiry-led businesses. Pass when a realistic response window and applicable hours/timezone are visible near the contact action. Do not invent a service-level promise.

### 29. Sticky mobile call to action

Conditional for high-intent local/service sites. Pass when the action remains useful without hiding content, respects safe areas and keyboards, has a large touch target, and can be reached by keyboard without trapping focus.

## Search presentation and local proof

### 30. robots.txt

Pass when `/robots.txt` is reachable, syntactically sensible, references the sitemap, and does not block intended public content or assets. Confirm production does not inherit preview `Disallow: /` or `noindex` behavior.

### 31. Unique page titles

Pass when every indexable page has one concise, descriptive, unique title aligned with its visible heading and search intent. Framework defaults and repeated titles fail.

### 32. Meta descriptions

Pass when every important indexable page has a useful, unique, supportable description. Missing, duplicated, truncated, or keyword-stuffed descriptions fail.

### 33. Social share images

Pass when important pages expose absolute Open Graph and relevant card metadata, the images load at appropriate dimensions, and a real share preview has been checked.

### 34. Maps and directions

Conditional for customer-facing locations or service areas. Pass when the address or service area is accurate, directions open correctly, and map embeds do not create unnecessary privacy or performance harm.

### 35. Real customer reviews

Conditional when reviews are published. Pass only with attributable, permissioned, non-placeholder reviews and honest source context. Do not invent, paraphrase, or imply review volume.

### 36. Alt text on images

Pass when informative images have useful contextual alt text and decorative images use empty alt text. Filename alt text, keyword stuffing, and duplicated captions fail.

### 37. Local business schema

Conditional for eligible local businesses. Pass when one valid `LocalBusiness` subtype accurately matches visible name, address or service area, phone, URL, hours, and other supported facts.

### 38. Privacy policy

Pass when the policy is reachable, current, names the responsible business, and accurately covers forms, analytics, cookies, embeds, vendors, retention, and user choices. Recommend qualified legal review.

### 39. Google Analytics

Conditional when Google Analytics is the chosen measurement system. Pass with evidence that the correct production property receives consent-compliant test events without duplicate page views or leaked sensitive data. Script presence alone is insufficient.

### 40. Real team photo

Conditional when a team or owner is part of the trust proposition. Pass only when the site contains an authentic, permissioned photo of the real people, with appropriate alt text, cropping, and performance. Stock or generated people fail.
