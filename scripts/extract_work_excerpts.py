"""Extract short, source-linked quotations from the read-only research archive."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT.parent / "private-research" / "hyk-alkuperaisaineisto-2026-10-15.zip"
CATALOG = json.loads((ROOT / "assets/archive/hyk-katalogi.json").read_text(encoding="utf-8"))


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in {"br", "p", "div", "li", "td", "tr", "h1", "h2", "h3"}:
            self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in {"p", "div", "li", "td", "tr", "h1", "h2", "h3"}:
            self.parts.append("\n")
    def handle_data(self, data):
        self.parts.append(data)


def read_page(zf, page_id):
    number = int(page_id.split("-")[1]) - 1
    name = f"hyk-corpus/{number:02}.bin"
    try:
        raw = zf.read(name)
    except KeyError:
        return ""
    text = raw.decode("cp1252", "replace")
    parser = PlainText()
    parser.feed(text)
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()


def clean_excerpt(text, max_chars=125):
    text = re.sub(r"\s+", " ", text).strip(" \t\r\n-–—:;,.!?·")
    text = re.sub(r"\b[\w.+-]+@[\w.-]+\.[a-zA-Z]+\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        clipped = text[:max_chars]
        boundary = clipped.rfind(" ")
        text = clipped[:boundary if boundary > 50 else max_chars].rstrip(" ,;:") + "…"
    return text


by_page = {}
for work in CATALOG["works"]:
    by_page.setdefault(work["page"], []).append(work)
results = {}
with zipfile.ZipFile(ARCHIVE) as zf:
    for page_id, works in by_page.items():
        text = read_page(zf, page_id)
        cursor = 0
        for work in works:
            title = work["title"]
            match = re.search(re.escape(title), text[cursor:], re.IGNORECASE)
            if not match:
                results[work["id"]] = None
                continue
            title_start = cursor + match.start()
            start = cursor + match.end()
            author_positions = []
            for name in work["authors"]:
                author_match = re.search(re.escape(name), text[start:], re.IGNORECASE)
                if author_match:
                    author_positions.append(start + author_match.start())
            next_start = len(text)
            if author_positions:
                next_start = min(author_positions)
            excerpt = clean_excerpt(text[start:next_start])
            if excerpt:
                results[work["id"]] = {"text": excerpt, "sourcePage": page_id}
                cursor = next_start + max((len(name) for name in work["authors"]), default=0)
            else:
                results[work["id"]] = None
                cursor = title_start + len(title)

output = ROOT / "src/_data/work-excerpts.json"
output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Short excerpts: {sum(value is not None for value in results.values())}/{len(results)} works.")
