"""Preserve exact captured site files and prepare full, source-linked work texts."""
from __future__ import annotations

from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT.parent / "private-research" / "hyk-alkuperaisaineisto-2026-10-15.zip"
CATALOG_PATH = ROOT / "assets/archive/hyk-katalogi.json"
OUTPUT_DIR = ROOT / "assets/archive/originals"
MANIFEST_PATH = ROOT / "assets/archive/originals-manifest.json"
TEXTS_PATH = ROOT / "src/_data/work-texts.json"
SEPARATORS = {"br", "hr", "p", "div", "li", "td", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote"}
MIME_EXTENSIONS = {
    "text/html": ".html",
    "application/xhtml+xml": ".xhtml",
    "text/plain": ".txt",
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/bmp": ".bmp",
    "image/webp": ".webp",
    "image/tiff": ".tif",
    "application/msword": ".doc",
    "application/rtf": ".rtf",
}
SPECIAL_HYK_FILES = {"HYK-033": "hyk-sivukartta.bin"}
ADDITIONAL_PAGES = [
    {
        "id": "MUNI-INFO-2000",
        "zip_file": "municipal-infosivu.bin",
        "collection": "Nummi-Pusulan kunta",
        "filename": "infosivu.htm",
        "original_url": "http://www.nummi-pusula.fi/infosivu.htm",
        "timestamp": "20001012205905",
        "mime_type": "text/html",
    },
    {
        "id": "MBNET-HYK-2001",
        "zip_file": "redirect-2001.bin",
        "collection": "MBnet / Hyrsylän koulu",
        "filename": "HYK-sisäänkäynti-2001.html",
        "original_url": "http://koti.mbnet.fi/~hyk/",
        "timestamp": "20010428205240",
        "mime_type": "text/html",
    },
    {
        "id": "MBNET-HYK-2002",
        "zip_file": "mbnet-hyk-2002.bin",
        "collection": "MBnet / Hyrsylän koulu",
        "filename": "HYK-sisäänkäynti-2002.html",
        "original_url": "http://koti.mbnet.fi:80/hyk/",
        "timestamp": "20020211130751",
        "mime_type": "text/html",
    },
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_html_name(original_filename: str) -> str:
    if original_filename in {"", "/"}:
        return "index.html"
    suffix = Path(original_filename).suffix.lower()
    return suffix if suffix in {".html", ".htm", ".xhtml"} else ".html"


class VisibleText(HTMLParser):
    """Split visible source text on the old pages' line and block boundaries."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.current: list[str] = []
        self.skip_depth = 0

    def flush(self) -> None:
        value = "".join(self.current).strip()
        if value:
            self.lines.append(re.sub(r"\s+", " ", value))
        self.current = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip_depth += 1
        if not self.skip_depth and tag in SEPARATORS:
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self.skip_depth:
            self.skip_depth -= 1
        if not self.skip_depth and tag in SEPARATORS:
            self.flush()

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.current.append(data)

    def finish(self) -> list[str]:
        self.flush()
        return self.lines


def normalized(value: str) -> str:
    return " ".join(value.casefold().split())


def transcribe_works(catalog: dict, raw_pages: dict[str, bytes]) -> tuple[dict, list[str]]:
    by_page: dict[str, list[dict]] = defaultdict(list)
    for work in catalog["works"]:
        by_page[work["page"]].append(work)

    results: dict[str, dict | None] = {}
    unmatched: list[str] = []
    for page_id, works in by_page.items():
        raw = raw_pages.get(page_id)
        if raw is None:
            for work in works:
                results[work["id"]] = None
                unmatched.append(work["id"])
            continue

        parser = VisibleText()
        parser.feed(raw.decode("cp1252", errors="replace"))
        lines = parser.finish()
        candidates: dict[str, list[tuple[int, float]]] = {}
        for work in works:
            title = normalized(work["title"])
            found = []
            for index, line in enumerate(lines):
                # A title can span several <br> or paragraph boundaries in
                # the old markup. Check a short run while preserving the
                # source line index used to split the complete text.
                line_norm = ""
                for end in range(index, min(index + 6, len(lines))):
                    line_norm = (line_norm + " " + normalized(lines[end])).strip()
                    if line_norm.startswith(title):
                        score = (len(line_norm) - len(title)) / max(len(line_norm), 1)
                        found.append((index, score))
                        break
            candidates[work["id"]] = found

        # Match each catalogue work to one distinct beginning line. Ambiguous
        # repeated titles use separate lines.
        assignments: dict[str, int] = {}
        used: set[int] = set()
        ordered = sorted(works, key=lambda w: (len(candidates[w["id"]]) or 10_000, -len(normalized(w["title"])), w["id"]))
        for work in ordered:
            options = sorted(candidates[work["id"]], key=lambda item: (item[1], item[0]))
            choice = next((index for index, _score in options if index not in used), None)
            if choice is not None:
                assignments[work["id"]] = choice
                used.add(choice)

        starts = sorted((line_index, work_id) for work_id, line_index in assignments.items())
        ends = {work_id: (starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)) for pos, (_line, work_id) in enumerate(starts)}
        for work in works:
            work_id = work["id"]
            if work.get("status", "").startswith("Vain alkuperäinen sisältöluettelolinkki"):
                results[work_id] = {
                    "text": None,
                    "sourcePage": page_id,
                    "transcription": None,
                    "reason": "The recovered HTML contains only the index link; the linked work itself was not recovered.",
                }
                continue
            if work_id not in assignments:
                # A sole named text can begin within its source page's prose
                # rather than in a heading; retain the complete page text.
                if len(works) == 1:
                    body = "\n".join(lines).strip()
                    if body:
                        results[work_id] = {
                            "text": body,
                            "sourcePage": page_id,
                            "transcription": "complete-visible-source-page",
                        }
                        continue
                results[work_id] = None
                unmatched.append(work_id)
                continue
            first = assignments[work_id]
            last = ends[work_id]
            body = "\n".join(lines[first:last]).strip()
            # A title-only index link (the unrecovered record) never becomes
            # a fabricated work transcription.
            if len(body) <= len(work["title"].strip()) + 2:
                results[work_id] = None
                unmatched.append(work_id)
                continue
            results[work_id] = {
                "text": body,
                "sourcePage": page_id,
                "transcription": "visible-text-from-complete-original-html",
            }
    return results, unmatched


def copy_sources(dry_run: bool = False) -> tuple[list[dict], dict[str, bytes]]:
    if not ZIP_PATH.exists():
        raise SystemExit(f"Read-only source archive missing: {ZIP_PATH}")
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    pages_by_id = {page["id"]: page for page in catalog["pages"]}
    dlc_by_capture = {(row["original_url"], str(row["timestamp"])): row for row in catalog["dlc_records"]}
    records: list[dict] = []
    raw_pages: dict[str, bytes] = {}

    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = set(archive.namelist())
        for page_id, page in pages_by_id.items():
            ordinal = int(page_id.split("-")[1]) - 1
            zip_name = f"hyk-corpus/{ordinal:02}.bin"
            if zip_name not in names:
                zip_name = SPECIAL_HYK_FILES.get(page_id, "")
            if zip_name not in names:
                continue
            content = archive.read(zip_name)
            raw_pages[page_id] = content
            actual_hash = sha256(content)
            if actual_hash != page["sha256"] or len(content) != page["bytes"]:
                raise SystemExit(f"Original integrity mismatch: {page_id}")
            local = f"assets/archive/originals/{page_id}{safe_html_name(page['filename'])}"
            records.append({
                "id": page_id,
                "collection": "Saunalahti / Hyrsylän koulu",
                "kind": "original-html",
                "filename": page["filename"],
                "original_url": page["original_url"],
                "archive_url": page["archive_url"],
                "raw_archive_url": f"https://web.archive.org/web/{page['timestamp']}id_/{page['original_url']}",
                "timestamp": page["timestamp"],
                "mime_type": "text/html",
                "bytes": len(content),
                "sha256": actual_hash,
                "local_path": "/" + local,
                "exact_original_bytes": True,
            })
            if not dry_run:
                target = ROOT / local
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)

        manifest_rows = [json.loads(line) for line in archive.read("dlc-originals/manifest.jsonl").decode("utf-8").splitlines() if line.strip()]
        saved_rows = [row for row in manifest_rows if row.get("saved")]
        for saved in saved_rows:
            catalog_row = dlc_by_capture.get((saved["original"], str(saved["timestamp"])))
            if catalog_row is None:
                raise SystemExit("Saved DLC source has no exact catalogue URL/timestamp match")
            content = archive.read("dlc-originals/" + saved["file"])
            actual_hash = sha256(content)
            if actual_hash != saved["sha256"] or len(content) != saved["bytes"]:
                raise SystemExit(f"Original integrity mismatch: {catalog_row['id']}")
            mime_type = saved.get("mimetype", "application/octet-stream").split(";", 1)[0].lower()
            extension = MIME_EXTENSIONS.get(mime_type, ".bin")
            local = f"assets/archive/originals/{catalog_row['id']}{extension}"
            records.append({
                "id": catalog_row["id"],
                "collection": "DLC / Hyrsylän koulu",
                "kind": "captured-original-file",
                "filename": catalog_row["filename"],
                "original_url": catalog_row["original_url"],
                "archive_url": catalog_row["archive_url"],
                "raw_archive_url": f"https://web.archive.org/web/{catalog_row['timestamp']}id_/{catalog_row['original_url']}",
                "timestamp": catalog_row["timestamp"],
                "mime_type": mime_type,
                "bytes": len(content),
                "sha256": actual_hash,
                "local_path": "/" + local,
                "exact_original_bytes": True,
            })
            if not dry_run:
                target = ROOT / local
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)

        for extra in ADDITIONAL_PAGES:
            content = archive.read(extra["zip_file"])
            actual_hash = sha256(content)
            extension = MIME_EXTENSIONS.get(extra["mime_type"], ".bin")
            local = f"assets/archive/originals/{extra['id']}{extension}"
            records.append({
                "id": extra["id"],
                "collection": extra["collection"],
                "kind": "captured-original-page",
                "filename": extra["filename"],
                "original_url": extra["original_url"],
                "archive_url": f"https://web.archive.org/web/{extra['timestamp']}/{extra['original_url']}",
                "raw_archive_url": f"https://web.archive.org/web/{extra['timestamp']}id_/{extra['original_url']}",
                "timestamp": extra["timestamp"],
                "mime_type": extra["mime_type"],
                "bytes": len(content),
                "sha256": actual_hash,
                "local_path": "/" + local,
                "exact_original_bytes": True,
            })
            if not dry_run:
                target = ROOT / local
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)

    records.sort(key=lambda row: (row["collection"], row["id"]))
    return records, raw_pages


def main() -> None:
    dry_run = "--dry-run" in sys.argv[1:]
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    records, raw_pages = copy_sources(dry_run=dry_run)
    texts, unmatched = transcribe_works(catalog, raw_pages)
    recoverable_unmatched = [
        work_id for work_id in unmatched
        if next((work for work in catalog["works"] if work["id"] == work_id), {}).get("status") == "Teksti luettu"
    ]
    if not dry_run and not recoverable_unmatched:
        TEXTS_PATH.write_text(json.dumps(texts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest = {
            "title": "Hyrsylän koulun ja Olli Poroilan palautetut alkuperäistiedostot",
            "integrity": "Every saved original is byte-for-byte identical to the source package; verify with SHA-256.",
            "original_file_count": len(records),
            "exact_original_bytes": all(row["exact_original_bytes"] for row in records),
            "files": records,
        }
        MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    saved_texts = sum(value is not None and value.get("text") is not None for value in texts.values())
    print(f"Original source files: {len(records)}; HYK pages: {len(raw_pages)}; works transcribed: {saved_texts}/{len(catalog['works'])}.")
    if unmatched:
        print("Unmatched catalogue work IDs: " + ", ".join(sorted(unmatched)))
    if dry_run:
        print("Dry run: source files and generated data were not written.")
    elif recoverable_unmatched:
        print("Source files were preserved; investigate recoverable work IDs before writing work-text data.")


if __name__ == "__main__":
    main()
