---
name: siteflight
description: Run an evidence-based 40-point website pre-launch audit for the important work AI coding agents often leave unfinished unless instructed. Use for site launch checklists, launch-readiness reviews, SEO and indexing audits, local-business sites, Google Search Console, sitemap.xml, robots.txt, llms.txt, forms, conversion paths, trust content, analytics, legal pages, or any request to decide whether a website is ready to publish. Inspect source, rendered pages, production, and connected accounts when available; recommend exact fixes and never call the site ready when required evidence is missing.
---

# SiteFlight

Audit the website as if a real launch decision depends on the result. Check all 40 items. Do not replace evidence with a generic checklist.

## Audit contract

- Inspect both the repository and the rendered website when both are available.
- Distinguish source evidence, local rendered evidence, preview evidence, and live production evidence.
- Record one status for every check: `PASS`, `FAIL`, `BLOCKED`, or `NOT APPLICABLE`.
- Use `PASS` only after observing the behavior or artifact at the strongest surface available.
- Use `BLOCKED` when access, credentials, consent, analytics ownership, Search Console, DNS, or a third-party system prevents verification.
- Use `NOT APPLICABLE` only when the business model clearly makes the check irrelevant. State why.
- Do not infer that a form works because markup exists, that analytics works because a script is present, or that a page is indexed because it is crawlable.
- Do not invent reviews, guarantees, team photos, opening hours, addresses, payment methods, response times, policies, or business claims.
- Do not change provider accounts, publish, deploy, submit forms that contact a real business, or create Search Console/analytics properties without explicit approval.

## Workflow

1. Establish the audit target.
   - Identify the repository or URL, launch environment, site type, service area, conversion goal, analytics platform, and whether the user authorized fixes.
   - Read repository instructions before touching files.
2. Read [the 40-check specification](references/checklist.md) completely.
3. Collect deterministic signals.
   - If a URL is reachable, run `python scripts/siteflight.py --url <URL> --output siteflight-signals.json` from this skill directory.
   - Treat script output as leads, not final proof. It cannot confirm visual placement, real photos, account ownership, legal sufficiency, or complete interaction behavior.
4. Inspect source.
   - Find routing, metadata, structured data, forms, analytics, consent, images, legal pages, error routes, and content collections.
   - Record exact file paths and lines for relevant evidence.
5. Inspect the rendered site.
   - Test representative desktop and phone sizes.
   - Navigate from the home page instead of opening only guessed routes.
   - Exercise navigation, internal links, social links, forms with invalid input, form success behavior using a safe test target, cookie choices, phone links, maps, the 404 route, and the sticky mobile action.
   - Check keyboard focus, console errors, failed requests, clipping, overflow, and whether content remains usable without motion.
6. Verify external systems only when access exists.
   - Search Console, analytics collection, DNS verification, review provenance, and production indexing remain `BLOCKED` without direct evidence.
7. Assign statuses and severity.
   - `P0`: launch-breaking, deceptive, unsafe, or legally material for this site.
   - `P1`: important discovery, conversion, trust, accessibility, or measurement defect.
   - `P2`: valuable maturity improvement that need not block launch.
8. Read [the report contract](references/report-contract.md), then produce the final report.
9. If fixes are authorized, implement the smallest complete batch, rerun affected checks, and report the new evidence. Do not silently expand into deployment or third-party account changes.

## Launch verdict

Return exactly one verdict:

- `READY`: all applicable P0 and P1 checks pass, every check has a status, and no launch-critical evidence is blocked.
- `NOT READY`: one or more applicable P0 or P1 checks fail.
- `BLOCKED`: the available evidence is insufficient to make a reliable launch decision.

Never use a score by itself to declare readiness. A site with 39 passes and one broken inquiry form is not ready.

## Interpretation rules

- Treat “rich tooltips” in an intake as rich-result eligibility unless the user explicitly means UI tooltips. If UI tooltips exist, also test accessible naming, keyboard access, escape behavior, and touch behavior.
- A detectable tag is not proof of a working integration. Confirm network delivery or account-side receipt when possible.
- A policy page existing is not proof that the policy matches the site's data collection or jurisdiction.
- A review counts only when it is attributable to a real source. Placeholder testimonials fail.
- A stock image or generated portrait does not satisfy the real-team-photo check.
- An image is not “compressed” merely because it has a modern extension. Check delivered bytes, dimensions, responsive sources, and visible quality.
- `llms.txt` is a requested discoverability artifact, not a substitute for robots, sitemaps, structured data, or accessible HTML.

## Final quality gate

Before returning:

- confirm IDs 01 through 40 appear exactly once;
- remove unsupported claims and duplicate recommendations;
- separate verified defects from blocked verification;
- make every recommendation specific to the observed stack and page;
- include the exact next action for each P0/P1 failure;
- state which environment was tested and when;
- avoid “guaranteed,” “fully optimized,” or “production-ready” unless the evidence genuinely supports it.
