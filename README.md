<div align="center">

# SiteFlight

### A 40-point website pre-launch checklist for Claude Code and Codex.

[![GitHub stars](https://img.shields.io/github/stars/YashSerai/siteflight?style=flat-square&logo=github&color=24292F)](https://github.com/YashSerai/siteflight/stargazers)
[![License](https://img.shields.io/github/license/YashSerai/siteflight?style=flat-square&color=24292F)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-supported-24292F?style=flat-square)](https://github.com/anthropics/skills)
[![Codex](https://img.shields.io/badge/Codex-supported-24292F?style=flat-square)](https://github.com/openai/plugins)

Forty checks before your website leaves the ground.

[The original checklist came from this TikTok by @yatesvids.](https://www.tiktok.com/@yatesvids/video/7672218589990112520?_r=1)

</div>

The 40 checks came from @yatesvids' video. They lined up with a lot of what I had seen while building and launching websites, so I turned the checklist into a skill Claude Code and Codex can run before a site goes live.

It tells the agent to check every item, show the evidence, and mark anything it cannot verify as blocked.

SiteFlight covers the details a normal build prompt often skips: `sitemap.xml`, `robots.txt`, `llms.txt`, Search Console, form errors, opening hours, a real 404, a thank-you page, service pages, customer reviews, payment information, cookie consent, mobile calls to action, and a photo of the actual team.

This does not replace a security review. It covers the launch work outside that review.

It checks the repository, the rendered website, production, and connected accounts when access exists. Every finding needs evidence. Missing access stays blocked instead of quietly turning green.

## Install

```bash
npx skills add YashSerai/siteflight --skill siteflight
```

Install it globally for Codex and Claude Code:

```bash
npx skills add YashSerai/siteflight --skill siteflight -g -a codex -a claude-code
```

<details>
<summary>Codex installation</summary>

Ask Codex:

```text
$skill-installer install https://github.com/YashSerai/siteflight/tree/main/skills/siteflight
```

Restart Codex after installation.

</details>

<details>
<summary>Claude Code installation</summary>

```text
/plugin marketplace add YashSerai/siteflight
/plugin install siteflight@siteflight
```

</details>

## The overlooked launch layer

### Discovery, indexing, and technical SEO

- `sitemap.xml`, `robots.txt`, canonicals, unique titles, meta descriptions, internal links, and real 404 responses
- accidental production `noindex` or crawler blocks
- Google Search Console property verification, sitemap submission, and indexing evidence when account access is available

### Business information and local search

- structured data and rich-result eligibility
- separate service pages, useful FAQs, case studies, internal linking, and original blog coverage
- local-business schema, opening hours, phone number, map directions, service area, and attributable reviews

### AI-readable site information

- a useful and accurate `llms.txt`
- clear entity, service, author, and business information in visible HTML and structured data
- content that can be parsed and cited without hiding the useful answer behind vague marketing copy

`llms.txt` is not treated as a ranking switch. SiteFlight checks it as one machine-facing artifact alongside the sitemap, robots rules, structured data, and accessible HTML.

### Conversion and customer trust

- tap-to-call, visible email, working social profiles, clear calls to action, and a mobile sticky action when appropriate
- specific form errors, safe success behavior, a thank-you state, and an honest response-time promise
- real team photography, an About story, before-and-after work, customer reviews, case studies, guarantees, and payment information when those claims apply

### Content, operations, and compliance

- compressed and responsive images, alt text, favicon, social share images, breadcrumbs, and a custom 404
- privacy policy, terms, cookie consent behavior, and Google Analytics event receipt when access exists
- desktop and phone rendering, keyboard behavior, console errors, failed requests, clipping, and overflow

The complete pass conditions live in [The SiteFlight 40](skills/siteflight/references/checklist.md).

## Use it

Audit a repository and preview before deployment:

```text
Use SiteFlight to audit this website before launch. Inspect the source and rendered preview, cover all 40 checks, and show me anything the site still needs before it is ready. Do not deploy.
```

Audit a live local-business website with external verification:

```text
Run SiteFlight on https://example.com. Check all 40 pre-launch items across discoverability, content, conversion, trust, local-business information, forms, analytics, legal pages, mobile behavior, and connected accounts. Mark anything you cannot prove as blocked.
```

Fix the verified defects:

```text
Run SiteFlight on this repo and local preview. Fix every P0 and P1 issue you can verify locally, rerun the affected checks, and stop before deployment or third-party account changes.
```

## The report does not hide behind a score

Every one of the 40 checks ends in one state:

| Status | Meaning |
|---|---|
| `PASS` | The agent observed enough evidence to support the claim. |
| `FAIL` | The check applies and the site does not meet it. |
| `BLOCKED` | The required production, account, or behavioral evidence is unavailable. |
| `NOT APPLICABLE` | The check genuinely does not fit this business, with a written reason. |

The final verdict is `READY`, `NOT READY`, or `BLOCKED`.

A tracking snippet in source is not proof that Google Analytics receives events. A Search Console meta tag is not proof that the correct property is verified. A branded error component is not proof that unknown URLs return HTTP 404. A passing build is not a launch verdict.

## Signal collector

SiteFlight includes a dependency-free crawler that gathers initial evidence from a reachable site:

```bash
python skills/siteflight/scripts/siteflight.py \
  --url https://example.com \
  --output siteflight-signals.json
```

It collects signals for all 40 checks, including discoverability files, metadata, internal pages, structured data, images, contact methods, and obvious gaps.

The crawler cannot verify Search Console ownership, analytics receipt, real form delivery, legal sufficiency, review provenance, real team identity, or visual placement. The agent finishes those checks in the rendered website and external systems.

## Why the skill is strict about evidence

Launch audits often collapse four different claims into one:

- the code exists;
- the feature rendered locally;
- the preview worked;
- production and the connected account received it.

SiteFlight keeps those claims separate. It also refuses to invent reviews, guarantees, hours, policies, payment methods, response times, or team details to complete a checklist.

The skill does not deploy, publish, create third-party properties, place calls, or contact a live business without explicit approval.

SiteFlight is a launch-quality workflow, not legal advice. Privacy, cookie, terms, accessibility, and regulated-industry requirements still need review appropriate to the business and jurisdiction.

## Repository

```text
skills/siteflight/
  SKILL.md
  agents/openai.yaml
  references/checklist.md
  references/report-contract.md
  scripts/siteflight.py
.claude-plugin/marketplace.json
.codex-plugin/plugin.json
skill.json
```

## License

[MIT](LICENSE)
