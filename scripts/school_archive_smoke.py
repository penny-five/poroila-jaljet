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
    work_by_id = {work['id']: work for work in catalog['works']}
    page_by_id = {page['id']: page for page in data['pages']}
    texts = json.loads((ROOT / 'src/_data/work-texts.json').read_text(encoding='utf-8'))
    selections = json.loads((ROOT / 'assets/archive/reviewed-school-works.json').read_text(encoding='utf-8'))
    for selection in selections:
        work = work_by_id[selection['id']]
        source = page_by_id[selection['sourceId']]
        check(work['title'] == selection['title'] and work['authors'] == selection['authors'], f'Reviewed attribution changed: {work["id"]}')
        check(texts[work['id']]['text'] == source['text'].replace('\n\n','\n'), f'Reviewed text differs from source: {work["id"]}')
        check(work['reviewedSourceSha256'] == originals[source['id']]['sha256'], f'Stale reviewed work: {work["id"]}')
        check(work['id'] in source['workIds'], f'Work missing from source reader: {work["id"]}')
        body = page_file('/teokset/'+work['id']+'/').read_text(encoding='utf-8')
        check('/koulu/aineisto/'+source['id']+'/' in body, f'Missing local work source link: {work["id"]}')
        if selection.get('previousSourceId'):
            previous = page_by_id[selection['previousSourceId']]
            check(work['id'] in previous['workIds'], 'Recovered work lost its original listing relationship')
            check(any(link['url'] == selection['previousLinkUrl'] and link['label'].casefold() == work['title'].casefold() for link in previous['links']), 'Recovered work does not match the reviewed listing link')
            check('/koulu/aineisto/'+previous['id']+'/' in body, 'Recovered work lost its previous-source link')
            check(not source['digestMismatch'] and bool(texts[work['id']]['text']), 'Recovered text is missing or unverified')

    image_sets = data['imageSets']
    check(len(image_sets) == 43 and len({item['id'] for item in image_sets}) == 43, 'Reviewed image comparison blocks lost or duplicated')
    comparisons = page_file('/koulu/kuva-ja-taidesivut/kuvamuunnokset/').read_text(encoding='utf-8')
    check(comparisons.count('data-image-set=') == len(image_sets), 'Comparison blocks missing from gallery')
    for item in image_sets:
        check(item['sourceSha256'] == originals[item['sourceId']]['sha256'], 'Comparison source changed')
        check(not page_by_id[item['sourceId']]['digestMismatch'], 'Comparison source is unverified')
        for person in item['people']:
            check(person['name'] in item['caption'], 'Comparison credit does not contain the person name')
            person_body = page_file('/tekijat/'+person['id']+'/').read_text(encoding='utf-8')
            check('/koulu/kuva-ja-taidesivut/kuvamuunnokset/#'+item['id'] in person_body, 'Comparison credit backlink missing')
        for image in item['images']:
            check(image in page_by_id[item['sourceId']]['images'], 'Comparison image detached from source')
    counterexample = next(item for item in image_sets if item['id'] == 'K-DLC-0083-010')
    check(counterexample['caption'] == 'Paula Savolainen' and all('kuvamuunnos-elsa-' in image['url'] for image in counterexample['images']), 'Image filename was incorrectly used as author evidence')
    poetry = page_file('/olli-poroila/kirjoitukset/').read_text(encoding='utf-8')
    check('/koulu/aineisto/DLC-0315/' in poetry and 'S73' in poetry, 'Poroila poetry source is missing from writings')
    groups = json.loads((ROOT / 'src/_data/school-collections.json').read_text(encoding='utf-8'))
    check(len({group['id'] for group in groups}) == len(groups), 'Duplicate roster IDs')
    for group in groups:
        source = page_by_id[group['sourceId']]
        check(group['sourceSha256'] == originals[source['id']]['sha256'], f'Stale roster: {group["id"]}')
        check(not source['digestMismatch'], f'Unverified roster source: {group["id"]}')
        body = page_file('/koulu/luokat/'+group['id']+'/').read_text(encoding='utf-8')
        check(body.count('data-roster-person=') == len(group['members']), f'Roster members missing: {group["id"]}')
        for member in group['members']:
            check(member['sourceName'] in source['text'] and member['evidence'] in source['text'], f'Unsupported roster name: {member["sourceName"]}')
            check(member['personId'] in people, f'Unknown roster person: {member["personId"]}')
            person_body = page_file('/tekijat/'+member['personId']+'/').read_text(encoding='utf-8')
            check('/koulu/luokat/'+group['id']+'/' in person_body, f'Missing roster backlink: {member["personId"]}')
    dated = next(group for group in groups if group['id'] == 'L-HYK-002')
    check(dated['period'] == '2000–2001' and any(image['label'] == '5. luokka 00/01' for image in page_by_id['HYK-002']['images']), 'Roster period lacks source caption')
    for item in originals.values():
        if 'cdx_digest' in item:
            raw = page_file(item['local_path']).read_bytes()
            actual = base64.b32encode(hashlib.sha1(raw).digest()).decode()
            check(actual == item['response_sha1_base32'], f'Archive response SHA-1 mismatch: {item["id"]}')
            check(item['capture_digest_match'] == (actual == item['cdx_digest']), f'Incorrect CDX verification flag: {item["id"]}')
    for item in originals.values():
        if item.get('archive_mime_type'):
            raw = page_file(item['local_path']).read_bytes()
            if item['archive_mime_type'] == 'im':
                expected = 'image/jpeg' if raw.startswith(b'\xff\xd8\xff') else 'image/gif' if raw.startswith((b'GIF87a', b'GIF89a')) else 'image/png' if raw.startswith(b'\x89PNG\r\n\x1a\n') else None
                check(expected == item['mime_type'], f'Incorrect payload MIME detection: {item["id"]}')
            elif item['archive_mime_type'] == 'text/plain':
                check(item['mime_type'] == 'text/html' and (b'<html' in raw.lower() or b'<body' in raw.lower()), 'Plain-text capture is not HTML')
    trip = page_by_id['DLC-0052']
    check('Karjalohjan Heponiemessä keväällä 1986' in trip['text'] and not trip['digestMismatch'], 'Trip date lacks verified source text')
    check(any(image['sourceId'] == 'DLC-0051' and image['displayPath'] for image in trip['images']), 'Trip photo not preserved or not connected to source')
    history = page_file('/koulu/historia/').read_text(encoding='utf-8')
    check('/koulu/aineisto/DLC-0052/' in history and 'DLC-0051.jpg' in history, 'Local trip source missing from school history')
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
