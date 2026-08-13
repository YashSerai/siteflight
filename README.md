# SiteFlight

### Forty checks before your website leaves the ground.

SiteFlight is an Agent Skill for the awkward moment before launch, when the site looks finished but nobody has checked whether the inquiry form explains its errors, the mobile phone number actually calls, the 404 returns a real 404, or analytics is collecting anything.

It gives Codex, Claude Code, and other compatible coding agents one job: inspect all 40 launch checks, show the evidence, and refuse to hand out a fake green light.

[![skills.sh](https://skills.sh/b/YashSerai/siteflight)](https://skills.sh/YashSerai/siteflight)

## Install

The quickest route works with Codex, Claude Code, Cursor, and other Agent Skills-compatible tools:

```bash
npx skills add YashSerai/siteflight --skill siteflight
```

Install globally for specific agents:

```bash
npx skills add YashSerai/siteflight --skill siteflight -g -a codex -a claude-code
```

### Codex

Ask Codex to install the skill from its GitHub directory:

```text
$skill-installer install https://github.com/YashSerai/siteflight/tree/main/skills/siteflight
```

Restart Codex after installation.

### Claude Code

Install it as a Claude Code plugin:

```text
/plugin marketplace add YashSerai/siteflight
/plugin install siteflight@siteflight
```

## Use it

Point your agent at a repository, preview, or live site:

```text
Use SiteFlight to audit this website before launch. Check the source and rendered site, cover all 40 checks, and give me the blockers first.
```

If you want fixes too, say so explicitly:

```text
Run SiteFlight on this repo and local preview. Fix every P0 and P1 issue you can prove locally, then rerun the affected checks. Do not deploy.
```

## The SiteFlight 40

The checklist covers the parts that are easy to forget and expensive to discover after launch:

- Search and machine readability: sitemap, rich results, canonicals, favicon, Search Console, `llms.txt`, `robots.txt`, titles, descriptions, and share cards.
- Conversion: tap-to-call, useful form errors, above-the-fold calls to action, thank-you states, response promises, and mobile actions.
- Content and trust: service pages, FAQs, case studies, reviews, team photography, opening hours, guarantees, payment methods, and real business contact details.
- Navigation and accessibility: internal links, breadcrumbs, 404 behavior, alt text, maps, and working social profiles.
- Operations and compliance: image delivery, cookie consent, privacy, terms, and analytics verification.

Read the [full 40-check specification](skills/siteflight/references/checklist.md) for the exact pass conditions.

## What makes the report useful

Every item ends in one of four states:

| Status | Meaning |
|---|---|
| `PASS` | The agent observed enough evidence to support the claim. |
| `FAIL` | The check was applicable and the observed site did not meet it. |
| `BLOCKED` | The agent could not verify the account, production system, or behavior. |
| `NOT APPLICABLE` | The check genuinely does not fit this business, with a written reason. |

SiteFlight keeps source, local preview, production, and account evidence separate. A tracking snippet in the repo is not proof that Google Analytics receives events. A branded error component is not proof that unknown URLs return HTTP 404. A passing build is not a launch verdict.

The final result is `READY`, `NOT READY`, or `BLOCKED`. There is no percentage score that can hide a broken inquiry path.

## Deterministic signal collector

The skill includes a dependency-free crawler for collecting initial signals from a reachable site:

```bash
python skills/siteflight/scripts/siteflight.py \
  --url https://example.com \
  --output siteflight-signals.json
```

The crawler finds metadata, discoverability files, internal pages, structured data, image and contact signals, and obvious gaps. It does not pretend to verify visual placement, real customer identities, legal sufficiency, account ownership, form delivery, or analytics receipt. The agent must finish those checks in the rendered site and external systems.

## Scope and safety

SiteFlight never invents reviews, guarantees, opening hours, policies, payment methods, response times, or team details. It does not deploy, publish, create third-party properties, place calls, or contact a live business unless the user explicitly authorizes that action.

This skill is a launch-quality workflow, not legal advice. Privacy, cookie, terms, accessibility, and regulated-industry requirements still need review appropriate to the business and jurisdiction.

## Repository layout

```text
skills/siteflight/
  SKILL.md
  agents/openai.yaml
  references/checklist.md
  references/report-contract.md
  scripts/siteflight.py
.claude-plugin/marketplace.json
.codex-plugin/plugin.json
```

## License

[MIT](LICENSE)
