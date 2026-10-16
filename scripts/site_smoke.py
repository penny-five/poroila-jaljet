#!/usr/bin/env python3
"""Lightweight checks for the Eleventy output and preserved archive files."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from html import unescape
import hashlib
import json
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PREFIX = os.environ.get("SITE_PREFIX", "/").strip() or "/"
if not PREFIX.startswith("/"):
    PREFIX = "/" + PREFIX
PREFIX = PREFIX.rstrip("/") + "/"

LEGACY_PAGES = (
    "/", "/koulu/", "/koulu/aikajana/", "/koulu/muistitieto/",
    "/koulu/oppilastyot/", "/koulu/myohemmat-vaiheet/",
    "/olli-poroila/kirjoitukset/", "/olli-poroila/aikajana/",
    "/olli-poroila/oikeus/", "/verkkoarkisto/tallenteet/",
    "/verkkoarkisto/sivujaljet/", "/verkkoarkisto/katalogi/",
    "/tekijat/", "/teokset/", "/verkkoarkisto/kuvat/",
    "/olli-poroila/kartta/", "/olli-poroila/hypoteesit/", "/fiktiot/", "/lahteet/",
)
REQUIRED_PAGES = (
    *LEGACY_PAGES, "/koulu/historia/", "/olli-poroila/",
    "/koulu/yhteenveto/",
    "/olli-poroila/tuntemuksiani/", "/verkkoarkisto/",
    "/verkkoarkisto/alkuperaistiedostot/", "/tutkimus/",
)


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src", "poster"} and value:
                self.links.append(value)


def page_file(route: str) -> Path:
    path = unquote(route)
    if PREFIX != "/" and path.startswith(PREFIX):
        path = "/" + path[len(PREFIX):]
    path = path.lstrip("/")
    target = SITE / path
    if not path or path.endswith("/") or not target.suffix:
        target = target / "index.html"
    return target


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    check(SITE.is_dir(), "Eleventy output _site/ is missing; build the site first")
    routes = json.loads((ROOT / "src/_data/legacyRoutes.json").read_text(encoding="utf-8"))
    aliases = json.loads((ROOT / 'src/_data/routeAliases.json').read_text(encoding='utf-8'))
    for old, current in aliases.items():
        redirect = page_file(old).read_text(encoding='utf-8')
        destination = PREFIX + current.lstrip('/')
        check(f'<link rel="canonical" href="{destination}">' in redirect, f'Wrong canonical redirect: {old}')
        check('window.location.replace(' in redirect and 'window.location.search + window.location.hash' in redirect, f'Redirect drops bookmark state: {old}')
        check(page_file(current).is_file(), f'Redirect destination missing: {old} -> {current}')
    for asset in ("style.css",):
        check((SITE / asset).read_bytes() == (ROOT / "tests/fixtures/original-site" / asset).read_bytes(), f"Original asset changed: {asset}")
    for route in REQUIRED_PAGES:
        check(page_file(route).is_file(), f"Missing page: {route}")
    for name, route in routes.items():
        body = page_file(route).read_text(encoding="utf-8")
        check(f'data-page="{name}"' in body, f"Wrong page identity: {route}")
        check(f'id="{name}"' in body, f"Original section missing: {route}")
        check(f'href="{PREFIX}style.css"' in body, f"Original stylesheet missing: {route}")
        check('site-layout.css' not in body, f"Migration CSS overrides original layout: {route}")
        check('id="legacy-data"' not in body, f"Unneeded research dataset sent to browser: {route}")
        check(f'src="{PREFIX}assets/main.js"' in body, f"Original controls missing: {route}")
        check(f'src="{PREFIX}app.js"' not in body, f"Old page router still loaded: {route}")
        if name == 'aineisto':
            check('id="articleDialog"' in body, f"Article dialog missing: {route}")
        check('JULKAISE KORJAUKSET AVOIMESTI' in body, f"Original footer missing: {route}")
        check(body.count('aria-current="page"') >= 1, f"Active navigation missing: {route}")
    home = page_file('/').read_text(encoding="utf-8")
    check('id="pageTrail"' not in home, "Homepage must not show a redundant breadcrumb")
    check('id="corkboard"' not in home, "Homepage gained the separate corkboard page")
    check('class="ticker"' in home and 'id="copyOriginal"' in home, "Unnamed home sections were lost")
    research = json.loads((ROOT / 'src/_data/research.json').read_text(encoding='utf-8'))
    for route, rows in (('/olli-poroila/aikajana/', research['timeline']), ('/koulu/aikajana/', research['schoolTimeline'])):
        body = page_file(route).read_text(encoding='utf-8')
        check(body.count('<article class="time-row ') == len(rows), f"Timeline requires JavaScript for its initial content: {route}")
    source_page = page_file('/lahteet/').read_text(encoding='utf-8')
    check(source_page.count('<a class="source-entry"') == len(research['sources']), 'Source list was not rendered at build time')
    board_page = page_file('/olli-poroila/kartta/').read_text(encoding='utf-8')
    check(board_page.count('<button class="node paper-') == 14, 'Initial corkboard cards were not rendered at build time')
    court_page = page_file('/olli-poroila/oikeus/').read_text(encoding='utf-8')
    court_article = next(article for article in research['articles'] if article['slug'] == 'koulu-auktoriteetti-ja-oikeuden-kieli')
    check(all(paragraph in unescape(court_page) for paragraph in court_article['paragraphs']), 'Court article requires JavaScript for its content')
    archive = json.loads((ROOT / "assets/archive/hyk-katalogi.json").read_text(encoding="utf-8"))
    people = [person["id"] for person in archive["people"]]
    for person_id in people:
        body = page_file(f'/tekijat/{person_id}/').read_text(encoding='utf-8')
        check('data-page="henkilot"' in body, f"Person lost original layout: {person_id}")
        check(body.count('data-person-id=') == 1, f"Person view must show exactly its original card: {person_id}")
        check(f'data-person-id="{person_id}"' in body, f"Wrong original person card: {person_id}")

    manifest = json.loads((ROOT / "assets/archive/originals-manifest.json").read_text(encoding="utf-8"))
    saved = manifest["files"]
    check(len(saved) == manifest["original_file_count"] and len(saved) >= 148, "Original-file inventory count inconsistent or baseline lost")
    check(len({item["id"] for item in saved}) == len(saved), "Duplicate exact-copy identifiers")
    for item in saved:
        target = page_file(item["local_path"])
        check(target.is_file(), f"Exact original is missing: {item['id']} -> {item['local_path']}")
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        check(digest == item["sha256"], f"Exact-copy SHA-256 mismatch: {item['id']}")

    work_texts = json.loads((ROOT / "src/_data/work-texts.json").read_text(encoding="utf-8"))
    available_texts = {work_id: item for work_id, item in work_texts.items() if item.get("text")}
    full_texts = {work_id: item for work_id, item in available_texts.items() if item.get('textStatus', 'complete') == 'complete'}
    check(set(work_texts) == {work['id'] for work in archive['works']}, 'Work text inventory differs from catalogue')
    check(len(work_texts) >= 98 and len(full_texts) >= 97, 'Baseline work texts were lost')
    for work_id, work_text in available_texts.items():
        target = SITE / "teokset" / work_id / "index.html"
        check(target.is_file(), f"Work page missing: {work_id}")
        body = target.read_text(encoding="utf-8")
        if work_text.get('textStatus', 'complete') == 'complete':
            check("Koko teos" in body, f"Complete transcription missing on {work_id}")
        else:
            check('<h2>Koko teos</h2>' not in body and 'data-text-status="'+work_text['textStatus']+'"' in body, f'Partial work is incorrectly presented as complete: {work_id}')
            check(work_text['completenessNote'] in unescape(body), f'Missing partial-text explanation: {work_id}')
        match = re.search(r'<pre class="work-copy">([\s\S]*?)</pre>', body)
        check(match is not None, f"Full transcription block missing on {work_id}")
        check(unescape(match.group(1)).strip() == work_text["text"].strip(), f"Transcription differs from source data on {work_id}")
    check(len({work['id'] for work in archive['works']}) == len(archive['works']), 'Duplicate work IDs')
    check((SITE / "teokset/T-098/index.html").is_file(), "Previously incomplete work must retain its permanent catalog page")

    author_pages = list((SITE / "tekijat").glob("H-*/index.html"))
    work_pages = list((SITE / "teokset").glob("T-*/index.html"))
    check(len(author_pages) >= len(archive["people"]), "One or more catalog people pages were lost")
    check(len(work_pages) == len(archive["works"]), "One or more work pages were lost")
    if author_pages:
        author_body = author_pages[0].read_text(encoding="utf-8")
        check('id="navigation"' in author_body and 'id="sectionNavigation"' in author_body, "Person pages have lost the shared two-level navigation")
    if work_pages:
        work_body = work_pages[0].read_text(encoding="utf-8")
        check('id="navigation"' in work_body and 'id="sectionNavigation"' in work_body, "Work pages have lost the shared two-level navigation")

    html_pages = [
        path for path in SITE.rglob("*.html")
        if "assets/archive/originals" not in path.as_posix()
    ]
    broken: list[str] = []
    checked_links = 0
    for source in html_pages:
        body = source.read_text(encoding="utf-8", errors="replace")
        if 'window.location.replace(' not in body:
            check(len(re.findall(r'<h1\b', body)) == 1, f'Expected exactly one page H1: {source.relative_to(SITE)}')
        if source != SITE / 'index.html' and 'window.location.replace(' not in body:
            heading = re.search(r'<header class="page-heading">([\s\S]*?)</header>', body)
            check(heading is not None and body.count('class="page-heading"') == 1, f'Expected one shared page heading: {source.relative_to(SITE)}')
            check('<p class="eyebrow">' in heading.group(1) and '<h1>' in heading.group(1), f'Shared heading hierarchy missing: {source.relative_to(SITE)}')
            trail = re.search(r'<nav id="pageTrail"[^>]*>([\s\S]*?)</nav>', body)
            check(trail is not None and body.count('id="pageTrail"') == 1, f'Expected one shared breadcrumb: {source.relative_to(SITE)}')
            check('aria-label="Murupolku"' in trail.group(0), f'Breadcrumb accessibility label missing: {source.relative_to(SITE)}')
            check(trail.group(1).count('aria-current="page"') == 1, f'Breadcrumb current page missing: {source.relative_to(SITE)}')
            check(f'href="{PREFIX}"' in trail.group(1), f'Breadcrumb root prefix incorrect: {source.relative_to(SITE)}')
            check('data-layout-feature="breadcrumbs"' in body, f'Shared breadcrumb style missing: {source.relative_to(SITE)}')
        check(not re.search(r'\bhref\s*=\s*["\'](?:#/|\.\.?/)', body, re.I), f"A legacy or relative link may route differently by page in {source.relative_to(SITE)}")
        parser = Links()
        parser.feed(body)
        for raw in parser.links:
            url = urlsplit(raw)
            repository_path = '/penny-five/poroila-jaljet/blob/main/'
            if url.netloc == 'github.com' and url.path.startswith(repository_path):
                check((ROOT / unquote(url.path[len(repository_path):])).is_file(), f'Repository file link is broken: {raw}')
            if url.scheme or url.netloc or raw.startswith("//"):
                continue
            if not url.path:
                continue
            checked_links += 1
            path = unquote(url.path)
            local_path = '/' + path[len(PREFIX):] if PREFIX != '/' and path.startswith(PREFIX) else path
            check(local_path.replace('/index.html', '/') not in aliases, f'Internal link still uses an old page address: {source.relative_to(SITE)} -> {raw}')
            if path.startswith("/"):
                target = page_file(path)
            else:
                target = source.parent / path
                if target.is_dir() or (not target.suffix and not target.exists()):
                    target = target / "index.html"
            if not target.is_file():
                broken.append(f"{source.relative_to(SITE)} -> {raw}")
    check(not broken, "Broken local links:\n" + "\n".join(broken[:30]))

    print(
        f"PASS: {len(LEGACY_PAGES)} legacy sections, {len(author_pages)} person pages, "
        f"{len(work_pages)} work pages, {len(full_texts)} full transcriptions and {len(available_texts) - len(full_texts)} partial/draft texts, {len(saved)} SHA-256-verified originals, "
        f"{checked_links} local links across {len(html_pages)} pages; shared navigation, canonical page routes, original page layouts, controls, person cards, and exact originals are present."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"SITE SMOKE CHECK FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
