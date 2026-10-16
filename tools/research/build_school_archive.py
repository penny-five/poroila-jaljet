"""Index preserved school HTML into safe, local reading pages. No network or rewrites of originals."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

ROOT = Path(__file__).resolve().parents[2]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def key(url):
    parts = urlsplit(url)
    return (parts.hostname or "").lower().removeprefix("www."), unquote(parts.path), parts.query


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.links = []
        self.images = []
        self.title = []
        self.hidden = 0
        self.in_title = False
        self.anchor = None
        self.base = None
        self.in_select = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in {"script", "style"}:
            self.hidden += 1
        if tag == "title":
            self.in_title = True
        if tag == "select":
            self.in_select += 1
        if tag == "base":
            self.base = a.get("href")
        if tag in {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "hr", "pre"}:
            self.text.append("\n")
        if tag in {"td", "th"}:
            self.text.append(" | ")
        if tag == "a" and a.get("href"):
            self.anchor = {"href": a["href"], "label": "", "context": clean(''.join(self.text)[-400:])}
            self.links.append(self.anchor)
        if tag == "area" and a.get("href"):
            self.links.append({"href": a["href"], "label": a.get("alt", "")})
        if tag == "option" and a.get("value"):
            self.anchor = {"href": a["value"], "label": ""}
            self.links.append(self.anchor)
        if tag in {"frame", "iframe"} and a.get("src"):
            self.links.append({"href": a["src"], "label": "Kehyksen sisältö"})
        if tag == "img" and a.get("src"):
            self.images.append({"href": a["src"], "label": a.get("alt", ""), "role": "image"})
            if self.anchor and a.get("alt"):
                self.anchor["label"] += a["alt"]
        if a.get("background"):
            self.images.append({"href": a["background"], "label": "Taustakuva", "role": "background"})

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden = max(0, self.hidden - 1)
        if tag == "title":
            self.in_title = False
        if tag == "select":
            self.in_select = max(0, self.in_select - 1)
            self.anchor = None
        if tag in {"a", "option"}:
            self.anchor = None
        if tag in {"p", "div", "tr", "li", "h1", "h2", "h3", "pre"}:
            self.text.append("\n")

    def handle_data(self, data):
        if self.hidden:
            return
        if self.in_title:
            self.title.append(data)
            return
        # The school-wide pupil dropdown is navigation, not the roster of the
        # class currently being read. Its option labels remain in source links.
        if self.in_select:
            if self.anchor:
                self.anchor["label"] += data
            return
        self.text.append(data)
        if self.anchor:
            self.anchor["label"] += data


def clean(value):
    return re.sub(r"\s+", " ", value).strip()


def category(filename):
    name = filename.lower()
    if name.startswith("oppilas-") or name == "entiset-oppilaat.htm":
        return "Oppilaiden sivut"
    if "oppilaat" in name or name in {"koko-hyk.htm", "koko-hyk2.htm"}:
        return "Luokat ja oppilasluettelot"
    if "kuvi" in name or "kuvasivu" in name or "luokkakuvat" in name:
        return "Kuva- ja taidesivut"
    if "runo" in name or "tuotoks" in name:
        return "Runot ja oppilastyöt"
    return "Koulun muut sivut"


def build():
    manifest = load("assets/archive/originals-manifest.json")
    catalog = load("assets/archive/hyk-katalogi.json")
    school_files = [f for f in manifest["files"] if "Hyrsylän koulu" in f["collection"]]
    display_paths = {}
    for f in school_files:
        if f["mime_type"].startswith("image/"):
            ext = {"image/jpeg": ".jpg", "image/gif": ".gif", "image/png": ".png"}.get(f["mime_type"])
            if not ext:
                continue
            local_path = f'/assets/archive/media/{f["id"]}{ext}'
            target = ROOT / local_path.lstrip("/")
            target.parent.mkdir(exist_ok=True)
            source = ROOT / f["local_path"].lstrip("/")
            assert hashlib.sha256(source.read_bytes()).hexdigest() == f["sha256"], f["id"]
            if target.exists():
                assert target.read_bytes() == source.read_bytes(), target
            else:
                shutil.copyfile(source, target)
            display_paths[f["id"]] = local_path
    files_by_url = {key(f["original_url"]): f for f in school_files}
    records = {key(r["original_url"]): r for r in catalog["pages"] + catalog["dlc_records"]}
    pages = []
    image_uses = {}
    for f in school_files:
        if "html" not in f["mime_type"]:
            continue
        raw = (ROOT / f["local_path"].lstrip("/")).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == f["sha256"], f["id"]
        declared = re.search(rb"charset\s*=\s*['\"]?([\w-]+)", raw, re.I)
        encoding = declared[1].decode("ascii") if declared else "windows-1252"
        if encoding.lower() in {"iso-8859-1", "latin1"}:
            encoding = "windows-1252"
        text = raw.decode(encoding, errors="replace")
        parser = PageParser()
        parser.feed(text)
        base = urljoin(f["original_url"], parser.base or "")
        links = []
        images = []
        for refs, output in [(parser.links, links), (parser.images, images)]:
            seen = set()
            for ref in refs:
                url = urljoin(base, ref["href"])
                if urlsplit(url).scheme not in {"http", "https"}:
                    continue
                if url in seen:
                    continue
                seen.add(url)
                local = files_by_url.get(key(url))
                record = records.get(key(url))
                item = {"url": url, "label": clean(ref["label"]) or unquote(urlsplit(url).path.rsplit("/", 1)[-1]) or url,
                        "sourceId": record["id"] if record else None,
                        "localPath": local["local_path"] if local else None,
                        "readerPath": f'/koulu/aineisto/{local["id"]}/' if local and "html" in local["mime_type"] else None}
                if ref.get("role"):
                    item["role"] = ref["role"]
                    item["displayPath"] = display_paths.get(local["id"]) if local else None
                    image_uses.setdefault(key(url), []).append({"pageId": f["id"], "label": item["label"], "role": ref["role"]})
                elif local and local["mime_type"].startswith("image/"):
                    context = ref.get("context", "")
                    years = re.findall(r'LUKUVUOSI\s+\d{2}/\d{2}', context, re.I)
                    image_uses.setdefault(key(url), []).append({"pageId": f["id"], "label": item["label"], "role": "linked-image",
                                                               "periodLabel": years[-1] if years else ""})
                output.append(item)
        lines = [clean(line).strip(" |") for line in "".join(parser.text).splitlines()]
        lines = [line for line in lines if line]
        people = []
        for person in catalog["people"]:
            evidence = [o for o in person["observations"] if o.get("source") == f["id"]]
            exact_name = re.search(r'(?<!\w)' + re.escape(person['name']) + r'(?!\w)', ' '.join(lines), re.I)
            if f["id"] in person["documents"] or evidence or exact_name:
                people.append({"id": person["id"], "name": person["name"], "observations": evidence,
                               "basis": "Sama kokonainen nimiasu sivun tekstissä" if exact_name else "Katalogin lähdeviite; tunnistuksen peruste tarkistettava"})
        fallback_title = ' '.join(lines[:2]) if lines and lines[0].upper() == 'HYRSYLÄN KOULUN' else (lines[0] if lines else f["filename"])
        pages.append({"id": f["id"], "filename": f["filename"], "title": clean("".join(parser.title)) or fallback_title[:150],
                      "category": category(f["filename"]), "text": "\n\n".join(lines), "encoding": encoding,
                      "originalUrl": f["original_url"], "archiveUrl": f["archive_url"], "timestamp": f["timestamp"],
                      "localPath": f["local_path"], "sha256": f["sha256"], "links": links, "images": images,
                      "digestMismatch": f.get('capture_digest_match') is False,
                      "people": people, "workIds": [w["id"] for w in catalog["works"] if w["page"] == f["id"] or w.get("previousSourceId") == f["id"]]})
    media = []
    for f in school_files:
        if not f["mime_type"].startswith("image/"):
            continue
        name = f["filename"].lower()
        group = "Muut kuvat ja sivugrafiikka"
        if re.match(r"\d.*oppilaat|kokokoulu", name):
            group = "Luokka- ja ryhmäkuvat"
        elif name.startswith(("kuva-puu-", "kuvamuunnos-")) or any(x in name for x in ["animaatio", "animation", "-yhteisanimaatio", "-auto.jpg", "-talo.jpg", "-puu.gif"]):
            group = "Oppilastyöt ja kuvataide"
        elif any(x in name for x in ["luokkahuone", "koulunpiha", "koulurakennus", "eteinen", "joulu98"]):
            group = "Koulutilat ja tapahtumat"
        elif name.startswith("oppilas-"):
            group = "Oppilassivujen kuvat"
        media.append({"id": f["id"], "filename": f["filename"], "group": group, "localPath": f["local_path"],
                      "displayPath": display_paths.get(f["id"]),
                      "digestMismatch": f.get('capture_digest_match') is False,
                      "originalUrl": f["original_url"], "archiveUrl": f["archive_url"], "timestamp": f["timestamp"],
                      "uses": image_uses.get(key(f["original_url"]), []), "sha256": f["sha256"]})
    result = {"method": "HTMLParser; declared charset or windows-1252 fallback; scripts/styles omitted; original files unchanged",
              "pages": pages, "media": media,
              "categories": list(dict.fromkeys(p["category"] for p in pages)),
              "mediaGroups": list(dict.fromkeys(m["group"] for m in media))}
    target = ROOT / "src/_data/schoolArchive.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f'{len(pages)} local reading pages; {len(media)} preserved images; {sum(len(p["links"]) for p in pages)} links indexed')


if __name__ == "__main__":
    build()
