"""One-time extraction of editorial pages from the former single-file site."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "index.html"
TARGETS = {
    "aineisto": ("olli-poroila/kirjoitukset", "Poroilan kirjoitukset ja lähteet", "olli"),
    "hypoteesit": ("tutkimus/hypoteesit", "Avoimet hypoteesit", "research"),
    "oikeus": ("olli-poroila/oikeus", "Oikeusprosessin vaiheet", "olli"),
    "fiktiot": ("fiktiot", "Fiktiiviset kenttämuistiinpanot", "fiction"),
    "koulu": ("koulu/historia", "Hyrsylän koulun historia", "school"),
    "sivujaljet": ("verkkoarkisto/sivujaljet", "Hyrsylän koulun verkkosivut", "archive"),
    "oppilaat": ("koulu/oppilastyot", "Oppilaiden verkkotyöt", "school"),
    "jatkovaiheet": ("tekijat/myohemmat-vaiheet", "Entisten oppilaiden myöhemmät vaiheet", "authors"),
    "muistitieto": ("koulu/muistitieto", "Koulun muistitieto", "school"),
    "arkisto": ("verkkoarkisto/tallenteet", "Tallennetut verkkosivut ja tiedostot", "archive"),
}
PARENTS = {
    "olli": ("Olli Poroila", "/olli-poroila/"),
    "school": ("Hyrsylän koulu", "/koulu/"),
    "archive": ("Verkkoarkisto", "/verkkoarkisto/"),
    "authors": ("Tekijät", "/tekijat/"),
    "research": ("Tutkimuksen tausta", "/tutkimus/"),
}
HASH_ROUTES = json.loads((ROOT / "src" / "_data" / "legacyRoutes.json").read_text(encoding="utf-8"))
ARTICLE_ROUTES = {
    "tech": "/olli-poroila/kirjoitukset/teknologiaa-ennen-internetia/",
    "law": "/olli-poroila/oikeus/",
    "web": "/olli-poroila/kirjoitukset/kadonnut-kotisivu/",
}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class ExtractSections(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.current = None
        self.depth = 0
        self.parts = {}

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == "section" and not self.current and attr.get("id"):
            self.current = attr["id"]
            self.depth = 0
            self.parts[self.current] = []
            return
        if self.current:
            self.parts[self.current].append(self.get_starttag_text())
            if tag not in VOID:
                self.depth += 1

    def handle_startendtag(self, tag, attrs):
        if self.current:
            self.parts[self.current].append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if not self.current:
            return
        if tag == "section" and self.depth == 0:
            self.current = None
            return
        self.parts[self.current].append(f"</{tag}>")
        if tag not in VOID:
            self.depth -= 1

    def handle_data(self, data):
        if self.current:
            self.parts[self.current].append(data)

    def handle_entityref(self, name):
        if self.current:
            self.parts[self.current].append(f"&{name};")

    def handle_charref(self, name):
        if self.current:
            self.parts[self.current].append(f"&#{name};")


class Markdown(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.anchors = []
        self.inline = []

    def block(self):
        if self.out and not self.out[-1].endswith("\n\n"):
            self.out.append("\n\n")

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.skip:
            if tag not in VOID:
                self.skip += 1
            return
        if tag in {"script", "style", "svg", "select", "option", "noscript"}:
            self.skip = 1
            return
        if tag in {"p", "div", "article", "figure", "figcaption", "aside", "details", "summary", "header", "footer", "label"}:
            self.block()
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.block()
            self.out.append("#" * int(tag[1]) + " ")
        elif tag == "br":
            self.out.append("  \n")
        elif tag == "hr":
            self.block(); self.out.append("---\n\n")
        elif tag in {"ul", "ol"}:
            self.block()
        elif tag == "li":
            self.block(); self.out.append("- ")
        elif tag in {"strong", "b"}:
            self.out.append("**"); self.inline.append((tag, "**"))
        elif tag in {"em", "i"}:
            self.out.append("*"); self.inline.append((tag, "*"))
        elif tag == "code":
            self.out.append("`"); self.inline.append((tag, "`"))
        elif tag == "blockquote":
            self.block(); self.out.append("> ")
        elif tag == "img":
            src = a.get("src", "")
            if src and not src.startswith(("http://", "https://", "//", "/")):
                src = "/" + src
            self.out.append(f"![{a.get('alt', '')}]({src})")
        elif tag == "a":
            href = a.get("href", "")
            if href.startswith("#/"):
                parts = href[2:].split("/")
                href = HASH_ROUTES.get(parts[0], "/")
                if len(parts) > 1 and parts[0] == "henkilot":
                    href = f"/tekijat/{parts[1]}/"
            self.anchors.append((len(self.out), href))
        elif tag == "button" and a.get("data-article") in ARTICLE_ROUTES:
            self.anchors.append((len(self.out), ARTICLE_ROUTES[a["data-article"]]))

    def handle_startendtag(self, tag, attrs):
        if self.skip:
            return

    def handle_endtag(self, tag):
        if self.skip:
            self.skip -= 1
            return
        if tag == "a" or tag == "button":
            if self.anchors:
                start, href = self.anchors.pop()
                label = "".join(self.out[start:]).strip()
                del self.out[start:]
                if href == HASH_ROUTES.get("arkisto") and any(
                    phrase.casefold() in label.casefold()
                    for phrase in ("Tuntemuksiani", "Kirjoitusten muu lähiluku")
                ):
                    href = "/olli-poroila/tuntemuksiani/"
                if href and label:
                    self.out.append(f"[{label}]({href})")
                elif label:
                    self.out.append(label)
        elif self.inline and self.inline[-1][0] == tag:
            _, marker = self.inline.pop()
            self.out.append(marker)
        elif tag in {"p", "div", "article", "figure", "figcaption", "aside", "details", "summary", "header", "footer", "label", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "blockquote"}:
            self.block()

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

    def finish(self):
        return re.sub(r"[ \t]+\n", "\n", "".join(self.out)).strip()


parser = ExtractSections()
parser.feed(SOURCE.read_text(encoding="utf-8"))
missing = set(TARGETS) - set(parser.parts)
if missing:
    raise SystemExit(f"Missing legacy sections: {sorted(missing)}")

for section, (route, title, group) in TARGETS.items():
    converter = Markdown()
    converter.feed("".join(parser.parts[section]))
    body = converter.finish()
    body = re.sub(r"(?m)^DOSSIER \d+ /[^\n]*\n*", "", body, count=1)
    body = re.sub(r"(?m)^HISTORIALLINEN ARKISTO /[^\n]*\n*", "", body, count=1)
    body = re.sub(r"(?m)^## [^\n]*\n*", "", body, count=1)
    body = re.sub(r"\n{3,}", "\n\n", body)
    if section == "muistitieto":
        body = body.replace("Oppilasverkkosivujen tekstejä ei ole palautettu.", "Hyrsylän koulun oppilastöitä ja niiden alkuperäisiä sivuja on palautunut Saunalahden arkistotallenteista. Niitä esitellään [oppilastöiden sivulla](/koulu/oppilastyot/) ja [tekijäkatalogissa](/tekijat/).")
        body = body.replace("Missä olivat oppilaiden tekemät nettisivut?", "Oppilastyöt ja niiden arkistotallenteet löytyivät")
    output = ROOT / "src" / "content" / f"{section}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    parent = PARENTS.get(group)
    parent_yaml = f'parent:\n  label: "{parent[0]}"\n  url: "{parent[1]}"\n' if parent else ""
    frontmatter = (
        "---\n"
        f'title: "{title}"\n'
        f'permalink: "/{route}/index.html"\n'
        f'group: "{group}"\n'
        f"{parent_yaml}"
        "layout: layouts/legacy-page.njk\n"
        "---\n\n"
    )
    output.write_text(frontmatter + body + "\n", encoding="utf-8")
    print(f"{section}: {len(body)} Markdown characters -> {route}/")
