#!/usr/bin/env python3
"""Static content and routing checks for the Hyrsylä / Jäljet archive.

Runs offline without dependencies. Catches regressions in navigation, source
provenance, local assets, page content and basic accessible markup before publish.
External URLs and historical factual claims require separate editorial review.
"""
from __future__ import annotations
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
FATAL = []
NOTES = []

def fail(message: str) -> None:
    FATAL.append(message)

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.sections: list[str] = []
        self.nav_links: list[str] = []
        self.all_links: list[str] = []
        self.local_refs: list[str] = []
        self.unlabeled_images: int = 0
        self.lang = False
        self.has_h1 = False
        self.has_title = False
        self.nav_depth = 0
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html":
            self.lang = d.get("lang") == "fi"
        if tag == "title":
            self.has_title = True
        if tag == "h1":
            self.has_h1 = True
        if d.get("id"):
            self.ids.append(d["id"])
            if tag == "section":
                self.sections.append(d["id"])
        if tag == "nav" and d.get("id") == "navigation":
            self.nav_depth += 1
        if tag == "a":
            href = d.get("href", "")
            self.all_links.append(href)
            if self.nav_depth:
                self.nav_links.append(href)
        if tag == "img" and "alt" not in d:
            self.unlabeled_images += 1
        if tag in ("script", "link", "img"):
            local = d.get("src") or (d.get("href") if tag == "link" else "")
            if local and not (local.startswith(("http://", "https://", "//", "data:"))):
                self.local_refs.append(local.split("?")[0].split("#")[0])
    def handle_endtag(self, tag):
        if tag == "nav" and self.nav_depth:
            self.nav_depth -= 1

def validate() -> int:
    html = (ROOT/"index.html").read_text(encoding="utf-8")
    app = (ROOT/"app.js").read_text(encoding="utf-8")
    data = (ROOT/"research-data.js").read_text(encoding="utf-8")
    css = (ROOT/"style.css").read_text(encoding="utf-8")
    doc = Document()
    doc.feed(html)
    if not doc.lang: fail("Missing html lang=fi")
    if not doc.has_h1: fail("Missing page H1")
    if not doc.has_title: fail("Missing page title")
    if doc.unlabeled_images: fail(f"{doc.unlabeled_images} images lack alt attribute")
    id_counts = Counter(doc.ids)
    for key, qty in id_counts.items():
        if qty > 1: fail(f"Duplicate HTML id: {key} ({qty} occurrences)")
    route_match = re.search(r"const pageNames\s*=\s*\{([^{}]+)\}", app)
    if not route_match:
        fail("Navigation route registry missing")
        routes = set()
    else:
        routes = set(re.findall(r"([a-z][a-z0-9]*)\s*:", route_match.group(1)))
    for href in doc.nav_links:
        if not href.startswith("#/"):
            fail(f"Navigation entry missing route URL: {href}")
            continue
        route = href[2:]
        if route not in routes: fail(f"Navigation {route} missing from app route registry")
        if route not in doc.sections: fail(f"Navigation {route} missing matching section id")
    if len(doc.nav_links) < 8: fail(f"Expected >=8 independent page links, found {len(doc.nav_links)}")
    for route in routes:
        if route not in doc.sections: fail(f"Route without HTML section: {route}")
    for href in doc.all_links:
        if href.startswith("#/") and href[2:].split("/")[0] not in routes:
            fail(f"Unknown internal route URL: {href}")
        if href.startswith("javascript:"): fail("Unsafe javascript: hyperlink")
    for rel in doc.local_refs:
        if not rel: continue
        if not (ROOT/rel).is_file(): fail(f"Missing local asset: {rel}")
    for rel in ["index.html", "style.css", "app.js", "research-data.js", ".nojekyll"]:
        if not (ROOT/rel).is_file(): fail(f"Missing deployment file: {rel}")
    if "import('./research-data.js')" not in app:
        fail("App no longer imports research-data.js")
    if "await import(" in app and ".catch(" not in app:
        fail("Uncaught asynchronous application entrypoint")
    # The project records editorial source keys in both source data modules.
    defs = re.findall(r"\bid\s*:\s*['\"](S\d{2,3})['\"]", app + "\n" + data)
    seen = Counter(defs)
    for key, count in seen.items():
        if count > 1: fail(f"Duplicate source key: {key} ({count} entries)")
    if len(defs) < 25: fail(f"Suspicious bibliography shrinkage: {len(defs)} references")
    used = set(re.findall(r"['\"](S\d{2,3})['\"]", app + "\n" + data))
    for key in sorted(used - set(defs)):
        fail(f"Reference key {key} used but not defined")
    if not re.search(r"const byId\s*=\s*Object\.fromEntries", app):
        fail("Source lookup map missing")
    if "main > section[hidden]" not in css:
        fail("Hidden-route CSS rule missing; multi-page layout would break")
    if 'id="sourceList"' not in html or 'id="timelineList"' not in html:
        fail("Bibliography or timeline mount element missing")
    if 'id="corkboard"' not in html:
        fail("Research evidence board is missing")
    if "Hyrsyl" not in html:
        fail("School project identity is missing")
    if len(html) < 20000: fail("Unexpectedly short index.html")
    if len(app) < 12000: fail("Unexpectedly short app.js")
    if len(css) < 12000: fail("Unexpectedly short CSS")
    print(f"Pages: {len(routes)}, menu links: {len(doc.nav_links)}, bibliography IDs: {len(defs)}, local assets: {len(doc.local_refs)}")
    if NOTES:
        for note in NOTES: print(f"NOTE: {note}")
    if FATAL:
        for issue in FATAL: print(f"ERROR: {issue}", file=sys.stderr)
        print(f"FAILED ({len(FATAL)} problems)", file=sys.stderr)
        return 1
    print("PASS: all static archive integrity checks")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
