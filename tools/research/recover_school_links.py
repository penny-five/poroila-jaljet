"""Recover a bounded batch of catalogued school files linked by preserved pages.

Uses known capture URLs, validates content, logs every attempt, never overwrites originals.
Run inventory first. Network required. --limit defaults to 40; --retry retries failed attempts.
"""
from __future__ import annotations
import argparse
import base64
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import urllib.request
from build_school_archive import ROOT, load


def fetch(record):
    url = f'https://web.archive.org/web/{record["timestamp"]}id_/{record["original_url"]}'
    result = {"id": record["id"], "original_url": record["original_url"], "requested_url": url,
              "retrieved_at": datetime.now(timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hyrsylan-school historical archive preservation"})
        with urllib.request.urlopen(req, timeout=15) as response:
            raw = response.read(8_000_001)
            result.update(effective_url=response.url, content_type=response.headers.get("Content-Type", ""))
        if not raw or len(raw) > 8_000_000:
            raise ValueError("empty or oversized response")
        mime = record.get("mimetype", "text/html")
        if mime.startswith("image/") or mime == "im":
            if not (raw.startswith((b"GIF87a", b"GIF89a", b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n"))):
                raise ValueError("not a supported original image")
            result['detected_mime_type'] = 'image/gif' if raw.startswith(b'GIF8') else 'image/png' if raw.startswith(b'\x89PNG') else 'image/jpeg'

        elif mime == "application/pdf":
            if not raw.startswith(b"%PDF-"):
                raise ValueError("not a PDF")
        else:
            if b"<html" not in raw.lower() and b"<body" not in raw.lower():
                raise ValueError("not original HTML")
            if any(marker in raw[:12000].lower() for marker in [b"wayback machine has not archived", b"cannot be crawled", b"__wm.init", b"wayback-toolbar"]):
                raise ValueError("archive error or replay wrapper")
            if mime == 'text/plain':
                result['detected_mime_type'] = 'text/html'
        result.update(saved=True, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        if record.get('digest'):
            result['cdx_digest'] = record['digest']
            result['response_sha1_base32'] = base64.b32encode(hashlib.sha1(raw).digest()).decode()
            result['capture_digest_match'] = result['response_sha1_base32'] == record['digest']
        return result, raw
    except Exception as error:
        result.update(saved=False, error=str(error))
        return result, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--retry", action="store_true")
    parser.add_argument("--ids", nargs="+", help="Select specific referenced catalog IDs within the bounded batch")
    args = parser.parse_args()
    inventory = load("src/_data/schoolArchive.json")
    catalog = load("assets/archive/hyk-katalogi.json")
    manifest = load("assets/archive/originals-manifest.json")
    report_path = ROOT / "assets/archive/recovery-attempts.json"
    attempts = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else []
    attempted = {a["id"] for a in attempts}
    saved_ids = {f["id"] for f in manifest["files"]}
    referenced = {x["sourceId"] for p in inventory["pages"] for x in p["images"] + p["links"] if x["sourceId"]}
    todo = [r for r in catalog["dlc_records"] + catalog["pages"] if r["id"] in referenced and r["id"] not in saved_ids
            and (args.retry or r["id"] not in attempted) and r.get("archive_status", "200") == "200"
            and r.get("mimetype", "text/html") in {"image/jpeg", "image/gif", "image/png", "text/html", "application/pdf", "im", "text/plain"}]
    # Prioritize linked photographs, artworks, pupil pages and class rosters over decoration.
    todo.sort(key=lambda r: (0 if re.search(r"oppilaat|luokkakuva|kuva-puu|oppilas-", r["filename"]) else 1, r["id"]))
    if args.ids:
        requested = set(args.ids)
        unknown = requested - {record['id'] for record in catalog['dlc_records'] + catalog['pages']}
        if unknown:
            parser.error('Unknown catalog IDs: ' + ', '.join(sorted(unknown)))
        todo = [record for record in todo if record['id'] in requested]
    todo = todo[:args.limit]
    print(f"Recovering {len(todo)} catalogued linked files", flush=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for record, (result, raw) in zip(todo, pool.map(fetch, todo)):
            if raw is not None:
                mime = result.get("detected_mime_type", record.get("mimetype", "text/html"))
                ext = {"image/jpeg": ".jpg", "image/gif": ".gif", "image/png": ".png", "application/pdf": ".pdf"}.get(mime, ".html")
                local_path = f'/assets/archive/originals/{record["id"]}{ext}'
                destination = ROOT / local_path.lstrip("/")
                assert not destination.exists(), destination
                destination.write_bytes(raw)
                effective = result["effective_url"]
                capture = re.search(r"/web/(\d{14})", effective)
                stamp = capture[1] if capture else record["timestamp"]
                manifest["files"].append({"id": record["id"], "collection": "DLC / Hyrsylän koulu" if record["id"].startswith("DLC-") else "Saunalahti / Hyrsylän koulu",
                    "kind": "captured-original-file", "filename": record["filename"], "original_url": record["original_url"],
                    "archive_url": f'https://web.archive.org/web/{stamp}/{record["original_url"]}',
                    "raw_archive_url": effective, "timestamp": stamp, "mime_type": mime,
                    "bytes": result["bytes"], "sha256": result["sha256"], "local_path": local_path,
                    **({'archive_mime_type': record['mimetype'], 'mime_detection': 'payload signature for image; HTML markup for text/plain'} if mime != record.get('mimetype', 'text/html') else {}),
                    "exact_original_bytes": result.get('capture_digest_match') is True, "retrieved_at": result["retrieved_at"],
                    **{field: result[field] for field in ['cdx_digest','response_sha1_base32','capture_digest_match'] if field in result}})
                record.update(status="Alkuperäinen tiedosto tallennettu; lähiluku erikseen" if result.get('capture_digest_match') is True else "Tallennevastauksen tavut säilytetty; CDX-tarkiste varmistamatta", sha256=result["sha256"], bytes=result["bytes"])
            attempts.append(result)
            results.append(result)
            # Persist after each completed request, so interruption never hides a saved file.
            manifest["original_file_count"] = len(manifest["files"])
            manifest['exact_original_bytes'] = all(f.get('exact_original_bytes') for f in manifest['files'])
            manifest['integrity'] = 'Stored bytes are unchanged; SHA-256 verifies local preservation. Per-file capture_digest_match records independent CDX SHA-1 verification for new downloads. A mismatch is retained as an unverified archive response, not certified original content.'
            for path, data in [(report_path, attempts), (ROOT / "assets/archive/originals-manifest.json", manifest), (ROOT / "assets/archive/hyk-katalogi.json", catalog)]:
                path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(record["id"], "saved" if result["saved"] else result["error"], flush=True)
    print(f'Saved {sum(r["saved"] for r in results)}/{len(results)}', flush=True)


if __name__ == "__main__":
    main()
