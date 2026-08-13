#!/usr/bin/env python3
"""Collect non-authoritative signals for the SiteFlight 40-point audit."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter, deque
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

USER_AGENT = "SiteFlight/1.0 (+https://github.com/YashSerai/siteflight)"
HTML_TYPES = ("text/html", "application/xhtml+xml")
SOCIAL_HOSTS = (
    "facebook.com", "instagram.com", "linkedin.com", "x.com", "twitter.com",
    "youtube.com", "tiktok.com", "pinterest.com", "threads.net",
)


@dataclass
class Page:
    url: str
    status: int
    content_type: str
    title: str = ""
    description: str = ""
    canonical: str = ""
    og_image: str = ""
    text: str = ""
    metas: dict[str, str] = field(default_factory=dict)
    links: list[dict[str, str]] = field(default_factory=list)
    images: list[dict[str, str]] = field(default_factory=list)
    forms: list[dict[str, Any]] = field(default_factory=list)
    icons: list[str] = field(default_factory=list)
    jsonld: list[Any] = field(default_factory=list)
    raw_lower: str = ""


class PageParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.metas: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.forms: list[dict[str, Any]] = []
        self.icons: list[str] = []
        self.jsonld: list[Any] = []
        self._in_title = False
        self._anchor: dict[str, str] | None = None
        self._form: dict[str, Any] | None = None
        self._jsonld_parts: list[str] | None = None

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key.lower(): value or "" for key, value in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = self._attrs(attrs)
        tag = tag.lower()
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = (data.get("name") or data.get("property") or data.get("http-equiv", "")).lower()
            if key:
                self.metas[key] = data.get("content", "").strip()
        elif tag == "link":
            rel = data.get("rel", "").lower()
            href = urljoin(self.base_url, data.get("href", ""))
            if "icon" in rel and href:
                self.icons.append(href)
            if rel == "canonical" and href:
                self.metas["canonical"] = href
        elif tag == "a":
            self._anchor = {
                "href": urljoin(self.base_url, data.get("href", "")),
                "text": "",
                "aria_label": data.get("aria-label", ""),
            }
        elif tag == "img":
            self.images.append({
                "src": urljoin(self.base_url, data.get("src", "")),
                "alt": data.get("alt", "__MISSING__"),
                "loading": data.get("loading", ""),
                "width": data.get("width", ""),
                "height": data.get("height", ""),
                "srcset": data.get("srcset", ""),
            })
        elif tag == "form":
            self._form = {
                "action": urljoin(self.base_url, data.get("action", "")),
                "method": data.get("method", "get").lower(),
                "required_fields": 0,
            }
        elif tag in ("input", "select", "textarea") and self._form is not None:
            if "required" in data or data.get("aria-required", "").lower() == "true":
                self._form["required_fields"] += 1
        elif tag == "script" and data.get("type", "").lower() == "application/ld+json":
            self._jsonld_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "a" and self._anchor is not None:
            self._anchor["text"] = " ".join(self._anchor["text"].split())
            self.links.append(self._anchor)
            self._anchor = None
        elif tag == "form" and self._form is not None:
            self.forms.append(self._form)
            self._form = None
        elif tag == "script" and self._jsonld_parts is not None:
            raw = "".join(self._jsonld_parts).strip()
            if raw:
                try:
                    self.jsonld.append(json.loads(raw))
                except json.JSONDecodeError:
                    self.jsonld.append({"_invalid_jsonld": raw[:160]})
            self._jsonld_parts = None

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._anchor is not None:
            self._anchor["text"] += " " + data
        if self._jsonld_parts is not None:
            self._jsonld_parts.append(data)
        self.text_parts.append(data)


def normalize_url(url: str) -> str:
    parsed = urlparse(urldefrag(url)[0])
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))


def fetch(url: str, timeout: float) -> tuple[int, str, bytes, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xml,text/plain,*/*;q=0.5"})
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read(3_000_000)
            return response.status, response.headers.get("Content-Type", ""), body, response.geturl()
    except HTTPError as exc:
        body = exc.read(1_000_000)
        return exc.code, exc.headers.get("Content-Type", ""), body, exc.geturl()
    except (URLError, TimeoutError, OSError) as exc:
        return 0, "", str(exc).encode("utf-8", errors="replace"), url


def parse_page(url: str, status: int, content_type: str, body: bytes) -> Page:
    charset_match = re.search(r"charset=([^;\s]+)", content_type, re.I)
    charset = charset_match.group(1).strip('"\'') if charset_match else "utf-8"
    text = body.decode(charset, errors="replace")
    parser = PageParser(url)
    try:
        parser.feed(text)
    except Exception:
        pass
    visible = " ".join(" ".join(parser.text_parts).split())
    return Page(
        url=url,
        status=status,
        content_type=content_type,
        title=" ".join(" ".join(parser.title_parts).split()),
        description=parser.metas.get("description", ""),
        canonical=parser.metas.get("canonical", ""),
        og_image=parser.metas.get("og:image", ""),
        text=visible,
        metas=parser.metas,
        links=parser.links,
        images=parser.images,
        forms=parser.forms,
        icons=parser.icons,
        jsonld=parser.jsonld,
        raw_lower=text.lower(),
    )


def crawl(start_url: str, max_pages: int, timeout: float) -> tuple[list[Page], dict[str, dict[str, Any]]]:
    start_url = normalize_url(start_url)
    origin = urlparse(start_url)
    queue: deque[str] = deque([start_url])
    seen: set[str] = set()
    pages: list[Page] = []
    fetch_log: dict[str, dict[str, Any]] = {}
    while queue and len(pages) < max_pages:
        url = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        status, content_type, body, final_url = fetch(url, timeout)
        fetch_log[url] = {"status": status, "content_type": content_type, "final_url": final_url}
        if not any(kind in content_type.lower() for kind in HTML_TYPES):
            continue
        page = parse_page(final_url, status, content_type, body)
        pages.append(page)
        for link in page.links:
            href = normalize_url(link["href"]) if link["href"] else ""
            parsed = urlparse(href)
            if parsed.scheme in ("http", "https") and parsed.netloc == origin.netloc:
                if not re.search(r"\.(?:pdf|jpe?g|png|gif|webp|avif|svg|zip|mp4|mp3|docx?|xlsx?)(?:$|\?)", parsed.path, re.I):
                    queue.append(href)
    return pages, fetch_log


def jsonld_types(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        kind = value.get("@type")
        if isinstance(kind, str):
            found.add(kind)
        elif isinstance(kind, list):
            found.update(str(item) for item in kind)
        for child in value.values():
            found.update(jsonld_types(child))
    elif isinstance(value, list):
        for child in value:
            found.update(jsonld_types(child))
    return found


def make_signal(check_id: int, name: str, signal: str, evidence: str) -> dict[str, str]:
    return {"id": f"{check_id:02d}", "check": name, "signal": signal, "evidence": evidence}


def collect_signals(base_url: str, pages: list[Page], endpoints: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    all_text = " ".join(page.text for page in pages)
    lower = all_text.lower()
    all_links = [link for page in pages for link in page.links]
    hrefs = [link["href"] for link in all_links if link["href"]]
    all_images = [image for page in pages for image in page.images]
    all_forms = [form for page in pages for form in page.forms]
    types = set().union(*(jsonld_types(page.jsonld) for page in pages)) if pages else set()
    titles = [page.title for page in pages if page.status == 200]
    descriptions = [page.description for page in pages if page.status == 200]
    blog_links = {url for url in hrefs if re.search(r"/(blog|news|insights|articles?)/", url, re.I)}
    service_links = {url for url in hrefs if re.search(r"/(services?|solutions?)/[^/?#]+", url, re.I)}
    missing_alt = sum(1 for image in all_images if image["alt"] == "__MISSING__")
    invalid_jsonld = sum(1 for page in pages for item in page.jsonld if isinstance(item, dict) and "_invalid_jsonld" in item)
    endpoint = lambda path: endpoints.get(path, {"status": 0, "bytes": 0, "preview": ""})
    sitemap = endpoint("/sitemap.xml")
    robots = endpoint("/robots.txt")
    llms = endpoint("/llms.txt")
    not_found = endpoint("/__siteflight_missing_page_8f30b1")
    signals = [
        make_signal(1, "Sitemap.xml", "present" if sitemap["status"] == 200 else "missing", f"HTTP {sitemap['status']}; {sitemap['bytes']} bytes"),
        make_signal(2, "Rich results readiness", "detected" if types else "missing", f"JSON-LD types: {', '.join(sorted(types)) or 'none'}; invalid blocks: {invalid_jsonld}"),
        make_signal(3, "Canonical tags", "detected" if pages and all(p.canonical for p in pages if p.status == 200) else "incomplete", f"{sum(bool(p.canonical) for p in pages)}/{len(pages)} crawled HTML pages expose a canonical"),
        make_signal(4, "Site favicon", "detected" if any(p.icons for p in pages) else "missing", f"{sum(len(p.icons) for p in pages)} favicon declarations"),
        make_signal(5, "Tap-to-call phone number", "detected" if any(url.startswith("tel:") for url in hrefs) else "review", f"{sum(url.startswith('tel:') for url in hrefs)} tel links"),
        make_signal(6, "Form error messages", "review", f"{len(all_forms)} forms; rendered invalid/error/success testing required"),
        make_signal(7, "Opening hours", "detected" if re.search(r"\b(mon(?:day)?|tue(?:sday)?|hours|open)\b.{0,80}\b\d{1,2}(?::\d{2})?\s*(?:am|pm)", lower, re.I) or "OpeningHoursSpecification" in types else "review", "Visible hours pattern or schema detected" if "OpeningHoursSpecification" in types or "hours" in lower else "No obvious hours signal"),
        make_signal(8, "Google Search Console", "detected" if any("google-site-verification" in p.metas for p in pages) else "blocked", "Verification tag detected; account-side verification still required" if any("google-site-verification" in p.metas for p in pages) else "No account-side evidence available to crawler"),
        make_signal(9, "Five useful blog posts", "detected" if len(blog_links) >= 5 else "incomplete", f"{len(blog_links)} distinct blog/article links found; quality requires review"),
        make_signal(10, "About page with a story", "detected" if any(re.search(r"/about(?:/|$)", p.url, re.I) and len(p.text.split()) >= 120 for p in pages) else "review", "About route with substantial text detected" if any("/about" in p.url.lower() for p in pages) else "No crawled About route"),
        make_signal(11, "Before-and-after gallery", "detected" if "before" in lower and "after" in lower and all_images else "review", "Before/after wording and images detected" if "before" in lower and "after" in lower else "No obvious before/after signal"),
        make_signal(12, "Separate page per service", "detected" if len(service_links) >= 2 else "review", f"{len(service_links)} distinct service/solution detail links found"),
        make_signal(13, "Visible email address", "detected" if any(url.startswith("mailto:") for url in hrefs) else "review", f"{sum(url.startswith('mailto:') for url in hrefs)} mailto links"),
        make_signal(14, "Working social links", "detected" if any(any(host in urlparse(url).netloc for host in SOCIAL_HOSTS) for url in hrefs) else "review", f"{sum(any(host in urlparse(url).netloc for host in SOCIAL_HOSTS) for url in hrefs)} social links found; destinations require verification"),
        make_signal(15, "Compressed images", "review", f"{len(all_images)} images; {sum(bool(i['srcset']) for i in all_images)} srcset; {sum(i['loading'].lower() == 'lazy' for i in all_images)} lazy; delivered bytes require review"),
        make_signal(16, "Working cookie consent", "detected" if re.search(r"cookie|consent|onetrust|cookiebot", lower + " " + " ".join(p.raw_lower for p in pages), re.I) else "review", "Consent-related text/code detected; behavior requires testing" if "cookie" in lower else "No obvious consent signal"),
        make_signal(17, "llms.txt", "present" if llms["status"] == 200 and llms["bytes"] > 0 else "missing", f"HTTP {llms['status']}; {llms['bytes']} bytes"),
        make_signal(18, "Terms of service", "detected" if any(re.search(r"/(terms|terms-of-service)(?:/|$)", urlparse(url).path, re.I) for url in hrefs) else "review", "Terms link detected" if "terms" in lower else "No obvious Terms link"),
        make_signal(19, "Clear payment methods", "detected" if re.search(r"\b(visa|mastercard|amex|paypal|apple pay|google pay|cash|credit card|debit card|financing)\b", lower, re.I) else "review", "Payment method wording detected" if re.search(r"\b(visa|mastercard|paypal|credit card|cash)\b", lower, re.I) else "No obvious payment-method wording"),
        make_signal(20, "Guarantee statement", "detected" if re.search(r"\b(guarantee|warranty|money.back)\b", lower, re.I) else "review", "Guarantee/warranty wording detected" if re.search(r"\b(guarantee|warranty)\b", lower, re.I) else "No obvious guarantee wording"),
        make_signal(21, "Custom 404 page", "detected" if not_found["status"] == 404 and not_found["bytes"] > 200 else "fail-signal", f"Unknown route returned HTTP {not_found['status']}; {not_found['bytes']} bytes"),
        make_signal(22, "Clear CTA above the fold", "review", "Requires rendered desktop and phone inspection"),
        make_signal(23, "Internal links", "detected" if len(hrefs) > 0 else "missing", f"{len(hrefs)} total links found across {len(pages)} HTML pages; broken-link review still required"),
        make_signal(24, "Thank-you page after inquiry", "detected" if any(re.search(r"/(thank-you|thanks|success)(?:/|$)", urlparse(url).path, re.I) for url in hrefs) else "review", "Confirmation route detected" if re.search(r"thank.you|thanks", lower, re.I) else "No obvious confirmation route; form success requires testing"),
        make_signal(25, "Breadcrumbs", "detected" if "BreadcrumbList" in types or "aria-label=\"breadcrumb" in " ".join(p.raw_lower for p in pages) else "review", "Breadcrumb schema or accessible nav signal detected" if "BreadcrumbList" in types else "No obvious breadcrumb signal"),
        make_signal(26, "Case study section", "detected" if re.search(r"case stud|our work|projects?", lower, re.I) else "review", "Case-study/project wording detected" if "case stud" in lower else "No obvious case-study signal"),
        make_signal(27, "Five FAQs", "detected" if lower.count("?") >= 5 or "FAQPage" in types else "incomplete", f"{lower.count('?')} visible question marks; FAQPage schema: {'yes' if 'FAQPage' in types else 'no'}"),
        make_signal(28, "Response-time promise", "detected" if re.search(r"(?:respond|reply|get back|hear from us).{0,60}(?:within|in)\s+\d+\s*(?:business\s+)?(?:hours?|days?)", lower, re.I) else "review", "Response-time wording detected" if re.search(r"(?:respond|reply|get back).{0,60}(?:hours?|days?)", lower, re.I) else "No obvious response-time promise"),
        make_signal(29, "Sticky mobile CTA", "review", "Requires rendered mobile, keyboard, safe-area, and overlap testing"),
        make_signal(30, "robots.txt", "present" if robots["status"] == 200 else "missing", f"HTTP {robots['status']}; {robots['bytes']} bytes; directives require review"),
        make_signal(31, "Unique page titles", "detected" if titles and len(titles) == len(set(titles)) and all(titles) else "fail-signal", f"{len(titles)} titles across {len(pages)} pages; {sum(count > 1 for count in Counter(titles).values())} duplicated values"),
        make_signal(32, "Meta descriptions", "detected" if descriptions and len(descriptions) == len(pages) and all(descriptions) else "incomplete", f"{sum(bool(p.description) for p in pages)}/{len(pages)} pages have descriptions"),
        make_signal(33, "Social share images", "detected" if pages and all(p.og_image for p in pages) else "incomplete", f"{sum(bool(p.og_image) for p in pages)}/{len(pages)} pages expose og:image"),
        make_signal(34, "Maps and directions", "detected" if any(re.search(r"google\.[^/]+/maps|maps\.apple\.com|goo\.gl/maps", url, re.I) for url in hrefs) else "review", "Map/directions link detected" if "maps" in " ".join(hrefs).lower() else "No obvious map/directions link"),
        make_signal(35, "Real customer reviews", "detected" if "Review" in types or re.search(r"testimonial|customer review", lower, re.I) else "review", "Review/testimonial signal detected; provenance requires review" if "Review" in types or "testimonial" in lower else "No obvious review signal"),
        make_signal(36, "Alt text on images", "detected" if all_images and missing_alt == 0 else "incomplete", f"{missing_alt}/{len(all_images)} images omit the alt attribute; quality requires contextual review"),
        make_signal(37, "Local business schema", "detected" if any(kind == "LocalBusiness" or kind.endswith("Business") for kind in types) else "review", f"JSON-LD types: {', '.join(sorted(types)) or 'none'}"),
        make_signal(38, "Privacy policy", "detected" if any(re.search(r"/privacy(?:-policy)?(?:/|$)", urlparse(url).path, re.I) for url in hrefs) else "review", "Privacy link detected; accuracy/legal review still required" if "privacy" in lower else "No obvious privacy link"),
        make_signal(39, "Google Analytics", "detected" if re.search(r"googletagmanager\.com/(?:gtag/js|gtm\.js)|google-analytics\.com", " ".join(p.raw_lower for p in pages), re.I) else "blocked", "Google Analytics/Tag Manager code detected; account receipt and consent require verification" if "googletagmanager" in " ".join(p.raw_lower for p in pages) else "No account-side analytics evidence available"),
        make_signal(40, "Real team photo", "review", f"{len(all_images)} images found; authenticity and permission cannot be inferred by crawler"),
    ]
    return signals


def endpoint_probe(base_url: str, path: str, timeout: float) -> dict[str, Any]:
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    status, content_type, body, final_url = fetch(url, timeout)
    preview = body[:180].decode("utf-8", errors="replace").replace("\n", " ")
    return {"url": url, "status": status, "content_type": content_type, "bytes": len(body), "final_url": final_url, "preview": preview}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect preliminary signals for all 40 SiteFlight checks.")
    parser.add_argument("--url", required=True, help="HTTP(S) site URL to crawl")
    parser.add_argument("--max-pages", type=int, default=25, help="Maximum same-origin HTML pages (default: 25)")
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout in seconds (default: 10)")
    parser.add_argument("--output", type=Path, help="Write JSON to this path; otherwise print to stdout")
    args = parser.parse_args()
    if not re.match(r"^https?://", args.url, re.I):
        parser.error("--url must begin with http:// or https://")
    if not 1 <= args.max_pages <= 200:
        parser.error("--max-pages must be between 1 and 200")

    started = time.time()
    pages, fetch_log = crawl(args.url, args.max_pages, args.timeout)
    base_url = normalize_url(args.url)
    endpoint_paths = ["/sitemap.xml", "/robots.txt", "/llms.txt", "/__siteflight_missing_page_8f30b1"]
    endpoints = {path: endpoint_probe(base_url, path, args.timeout) for path in endpoint_paths}
    signals = collect_signals(base_url, pages, endpoints)
    payload = {
        "tool": "SiteFlight signal collector",
        "version": "1.0.0",
        "target": base_url,
        "generated_at_epoch": int(time.time()),
        "duration_seconds": round(time.time() - started, 2),
        "disclaimer": "Signals are not final PASS/FAIL decisions. Finish the audit in source, rendered UI, production, and external accounts.",
        "crawl": {
            "pages_parsed": len(pages),
            "max_pages": args.max_pages,
            "pages": [{"url": p.url, "status": p.status, "title": p.title} for p in pages],
            "fetch_log": fetch_log,
        },
        "endpoints": endpoints,
        "signals": signals,
    }
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {len(signals)} signals to {args.output}")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
