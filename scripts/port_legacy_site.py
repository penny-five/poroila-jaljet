#!/usr/bin/env python3
"""Split the former site's exact HTML shell and sections into Eleventy includes."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "index.html"
INCLUDES = ROOT / "src" / "_includes" / "legacy"
LEGACY_ROUTES = json.loads((ROOT / "src" / "_data" / "legacyRoutes.json").read_text(encoding="utf-8"))
class Sections(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=False)
        self.source = source
        self.offsets = [0]
        for match in re.finditer("\n", source):
            self.offsets.append(match.end())
        self.depth = 0
        self.current: dict[str, str | int] | None = None
        self.sections: list[dict[str, str | int]] = []

    def source_offset(self) -> int:
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "section":
            return
        if self.current is None:
            section_id = dict(attrs).get("id")
            ordinal = len(self.sections) + 1
            name = str(section_id) if section_id else f"section-{ordinal:02d}"
            self.current = {"name": name, "start": self.source_offset(), "depth": 1}
            return
        self.current["depth"] = int(self.current["depth"]) + 1

    def handle_endtag(self, tag: str) -> None:
        if tag != "section" or self.current is None:
            return
        self.current["depth"] = int(self.current["depth"]) - 1
        if self.current["depth"] == 0:
            self.current["end"] = self.source_offset() + len("</section>")
            self.sections.append(self.current)
            self.current = None


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    if any(token in source for token in ("{{", "{%", "{#")):
        raise SystemExit("Legacy HTML contains Nunjucks tokens; escape them before porting.")
    parser = Sections(source)
    parser.feed(source)
    if parser.current is not None or len(parser.sections) != 21:
        raise SystemExit(f"Expected 21 complete legacy sections, found {len(parser.sections)}")

    INCLUDES.mkdir(parents=True, exist_ok=True)

    section_dir = INCLUDES / "sections"
    section_dir.mkdir(parents=True, exist_ok=True)
    for section in parser.sections:
        name = re.sub(r"[^a-z0-9-]+", "-", str(section["name"]).lower()).strip("-")
        start, end = int(section["start"]), int(section["end"])
        section_html = source[start:end]
        # Keep the markup exact. URL rewriting belongs to the Eleventy output
        # filter, so the reference and editable includes remain comparable.
        (section_dir / f"{name}.njk").write_text(section_html, encoding="utf-8", newline="")

    head = source[:source.index('<body>')]
    head = re.sub(r'<title>.*?</title>', '<title>{{ title }}</title>', head)
    head = head.replace('href="style.css"', 'href="{{ "/style.css" | localUrl }}"')
    head = head.replace('<script defer src="app.js"></script>', '''<meta name="site-base" content="{{ '/' | localUrl }}" />
<script defer src="{{ '/assets/legacy.js' | localUrl }}"></script>''')
    (INCLUDES / 'head.njk').write_text(head, encoding='utf-8')
    tail = source[source.rindex('</section>') + len('</section>'):]
    tail = tail.replace('</main>', '').replace('</body></html>', '')
    (INCLUDES / 'footer.njk').write_text(tail.strip(), encoding='utf-8')

    # Replace only the existing route entry points. Extra recovered-text and
    # archive pages from the interrupted migration are retained.
    names = json.loads((ROOT / 'src/_data/research.json').read_text(encoding='utf-8'))['navigation']['names']
    for name, route in LEGACY_ROUTES.items():
        permalink = route + 'index.html'
        targets = []
        for path in (ROOT / 'src').rglob('*'):
            if path.suffix not in {'.md', '.njk'} or '_includes' in path.parts:
                continue
            text = path.read_text(encoding='utf-8')
            match = re.search(r'^permalink:\s*[\"\']?([^\"\'\n]+)', text, re.M)
            if match and match[1].strip() == permalink:
                targets.append(path)
        if len(targets) != 1:
            raise SystemExit(f'Expected one template for {route}, found {targets}')
        title = ('HYRSYLÄ / JÄLJET' if name == 'alku' else names[name] + ' — HYRSYLÄ / JÄLJET') + ' | Tutkimusarkisto'
        text = f'---\nlayout: layouts/preserved-page.njk\ntitle: {title}\npermalink: {permalink}\nlegacyPage: {name}\n---\n'
        text += '{% include "legacy/sections/' + name + '.njk" %}\n'
        if name == 'alku':
            # The original router treats every unnamed section as home content.
            for section in parser.sections:
                if str(section['name']).startswith('section-'):
                    text += '{% include "legacy/sections/' + str(section['name']) + '.njk" %}\n'
        targets[0].write_text(text, encoding='utf-8')

    people = next(section for section in parser.sections if section['name'] == 'henkilot')
    person_html = source[int(people['start']):int(people['end'])]
    ids = re.findall(r'data-person-id="([^"]+)"', person_html)
    (ROOT / 'src/_data/legacyPersonIds.json').write_text(json.dumps(ids, indent=2) + '\n', encoding='utf-8')
    print(f'Preserved {len(parser.sections)} sections, original head/footer, {len(LEGACY_ROUTES)} page views and {len(ids)} historical person views.')


if __name__ == "__main__":
    main()
