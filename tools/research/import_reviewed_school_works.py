"""Import individually reviewed full works from preserved school reading pages.

The explicit selection file fixes IDs, headings, genres and literal author names.
Original files are never edited. Run build_school_archive.py after this import.
"""
from __future__ import annotations
import hashlib
import json
from build_school_archive import ROOT, load


def main():
    catalog = load('assets/archive/hyk-katalogi.json')
    texts = load('src/_data/work-texts.json')
    inventory = load('src/_data/schoolArchive.json')
    selected = load('assets/archive/reviewed-school-works.json')
    sources = {page['id']: page for page in inventory['pages']}
    originals = {file['id']: file for file in load('assets/archive/originals-manifest.json')['files']}
    works = {work['id']: work for work in catalog['works']}
    people = {person['name']: person for person in catalog['people']}
    for selection in selected:
        source = sources[selection['sourceId']]
        original = originals[source['id']]
        # Baseline originals are checked against their preserved package SHA-256;
        # later downloads must also have a matching CDX payload digest.
        assert original.get('exact_original_bytes') is True and original.get('capture_digest_match') is not False, f'Unverified source: {source["id"]}'
        raw = (ROOT / original['local_path'].lstrip('/')).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == source['sha256'] == original['sha256']
        lines = source['text'].split('\n\n')
        assert lines[:2] == [selection['authorHeading'], selection['title']], selection['sourceId']
        assert len(lines) > 3, 'Source must contain the actual work, not just a link'
        record = {
            'id': selection['id'], 'title': selection['title'], 'authors': selection['authors'],
            'genre': selection['genre'], 'period': 'Ei päiväystä lähdesivulla', 'page': source['id'],
            'status': 'Kokoteksti paikallisessa arkistossa',
            'note': 'Tekijämerkintä säilytetään lähteen mukaisena. Tallennuspäivä ei ole kirjoituspäivä. Oppilastyön sisältöä ei tulkita kirjoittajan elämäkertatiedoksi.',
            'reviewedSourceSha256': source['sha256'],
        }
        if record['id'] in works:
            assert works[record['id']]['page'] == source['id'], 'Existing ID belongs to another work'
            works[record['id']].update(record)
        else:
            catalog['works'].append(record)
        texts[record['id']] = {'text': '\n'.join(lines), 'sourcePage': source['id'],
                              'transcription': 'visible-text-from-complete-original-html; automatic whitespace normalization; original spelling and line breaks retained',
                              'sourceSha256': source['sha256']}
        for name in record['authors']:
            if name in people and record['id'] not in people[name]['works']:
                people[name]['works'].append(record['id'])
    for path, data in [('assets/archive/hyk-katalogi.json', catalog), ('src/_data/work-texts.json', texts)]:
        (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Imported {len(selected)} reviewed works; total {len(catalog["works"])}')


if __name__ == '__main__':
    main()
