"""Validate the entire local school reading collection, media and relationship links."""
from html import unescape
import hashlib
import base64
import json
from pathlib import Path
import re
from site_smoke import ROOT, SITE, page_file, check


def main():
    data = json.loads((ROOT / 'src/_data/schoolArchive.json').read_text(encoding='utf-8'))
    manifest = json.loads((ROOT / 'assets/archive/originals-manifest.json').read_text(encoding='utf-8'))
    catalog = json.loads((ROOT / 'assets/archive/hyk-katalogi.json').read_text(encoding='utf-8'))
    originals = {f['id']: f for f in manifest['files'] if 'Hyrsylän koulu' in f['collection']}
    records = {r['id'] for r in catalog['pages'] + catalog['dlc_records']}
    people = {p['id'] for p in catalog['people']}
    for item in originals.values():
        if 'cdx_digest' in item:
            raw = page_file(item['local_path']).read_bytes()
            actual = base64.b32encode(hashlib.sha1(raw).digest()).decode()
            check(actual == item['response_sha1_base32'], f'Archive response SHA-1 mismatch: {item["id"]}')
            check(item['capture_digest_match'] == (actual == item['cdx_digest']), f'Incorrect CDX verification flag: {item["id"]}')
    check({p['id'] for p in data['pages']} == {f['id'] for f in originals.values() if 'html' in f['mime_type']}, 'School reading inventory is stale')
    check({m['id'] for m in data['media']} == {f['id'] for f in originals.values() if f['mime_type'].startswith('image/')}, 'School media inventory is stale')
    for route in ['aineisto','koulukuvat','oppilaiden-sivut','luokat','kuva-ja-taidesivut','runot-ja-kirjoitelmat','koulun-sivut']:
        check(page_file('/koulu/'+route+'/').is_file(), f'Missing school section: {route}')
    for page in data['pages']:
        target = page_file('/koulu/aineisto/'+page['id']+'/')
        check(target.is_file(), f'Missing reading page: {page["id"]}')
        body = target.read_text(encoding='utf-8')
        if page.get('digestMismatch'):
            check('sen tarkiste poikkeaa' in body, f'Missing archive discrepancy warning: {page["id"]}')
        check(page['sha256'] == originals[page['id']]['sha256'], f'Stale source hash: {page["id"]}')
        for paragraph in page['text'].split('\n\n'):
            if paragraph:
                check(paragraph in unescape(body), f'Reading text missing: {page["id"]}: {paragraph[:80]}')
        for person in page['people']:
            check(person['id'] in people, f'Unknown person: {person["id"]}')
            person_body = page_file('/tekijat/'+person['id']+'/').read_text(encoding='utf-8')
            check('/koulu/aineisto/'+page['id']+'/' in person_body, f'Missing person backlink: {person["id"]} -> {page["id"]}')
        for link in page['links'] + page['images']:
            if link['sourceId']:
                check(link['sourceId'] in records, f'Unknown source ID: {link["sourceId"]}')
            for field in ['localPath','readerPath','displayPath']:
                if link.get(field):
                    check(page_file(link[field]).is_file(), f'Missing linked {field}: {link[field]}')
        check(not re.search(r'<img[^>]+src=[\'"]https?://', body), f'External image dependency: {page["id"]}')
    gallery = page_file('/koulu/koulukuvat/').read_text(encoding='utf-8')
    for image in data['media']:
        check(image['displayPath'] in gallery, f'Image absent from gallery: {image["id"]}')
        raw = page_file(image['displayPath']).read_bytes()
        check(hashlib.sha256(raw).hexdigest() == image['sha256'] == originals[image['id']]['sha256'], f'Image byte mismatch: {image["id"]}')
        for use in image['uses']:
            check(use['pageId'] in originals, f'Unknown image source: {use["pageId"]}')
    print(f'PASS: {len(data["pages"])} complete reading pages, {len(data["media"])} local images; source integrity, text, person backlinks and local media verified')


if __name__ == '__main__':
    main()
