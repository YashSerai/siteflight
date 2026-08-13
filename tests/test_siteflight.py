import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "skills" / "siteflight" / "scripts" / "siteflight.py"
SPEC = importlib.util.spec_from_file_location("siteflight_collector", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SiteFlightCollectorTests(unittest.TestCase):
    def test_parser_extracts_core_signals(self):
        html = b"""<!doctype html><html><head>
        <title>Roof repair in Vancouver</title>
        <meta name="description" content="Residential roof repair.">
        <link rel="canonical" href="https://example.com/">
        <link rel="icon" href="/favicon.ico">
        <meta property="og:image" content="https://example.com/share.jpg">
        <script type="application/ld+json">{"@type":"LocalBusiness","name":"Example"}</script>
        </head><body><a href="tel:+16045550100">Call</a>
        <a href="/privacy">Privacy</a><img src="team.webp" alt="The Example team"></body></html>"""
        page = MODULE.parse_page("https://example.com/", 200, "text/html; charset=utf-8", html)
        self.assertEqual(page.title, "Roof repair in Vancouver")
        self.assertEqual(page.canonical, "https://example.com/")
        self.assertEqual(page.og_image, "https://example.com/share.jpg")
        self.assertIn("LocalBusiness", MODULE.jsonld_types(page.jsonld))
        self.assertTrue(any(link["href"].startswith("tel:") for link in page.links))

    def test_signal_set_has_exactly_40_unique_ids(self):
        page = MODULE.parse_page("https://example.com/", 200, "text/html", b"<title>Home</title>")
        endpoints = {
            path: {"status": 404, "bytes": 0, "preview": ""}
            for path in ("/sitemap.xml", "/robots.txt", "/llms.txt", "/__siteflight_missing_page_8f30b1")
        }
        signals = MODULE.collect_signals("https://example.com/", [page], endpoints)
        self.assertEqual(len(signals), 40)
        self.assertEqual([item["id"] for item in signals], [f"{n:02d}" for n in range(1, 41)])

    def test_url_normalization_drops_fragments(self):
        self.assertEqual(
            MODULE.normalize_url("HTTPS://Example.com//services/#quote"),
            "https://example.com/services/",
        )


if __name__ == "__main__":
    unittest.main()
