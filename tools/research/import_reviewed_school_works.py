"""Import individually reviewed full works from preserved school reading pages.

The explicit selection file fixes IDs, headings, genres and literal author names.
Original files are never edited. Run build_school_archive.py after this import.
"""
from __future__ import annotations
import hashlib
import json
from urllib.parse import urlsplit
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
        headings = selection.get('sourceHeadingLines', [selection['authorHeading'], selection.get('sourceTitle', selection['title'])])
        assert lines[:len(headings)] == headings, selection['sourceId']
        assert selection['authorHeading'] in headings
        title_lines = headings[headings.index(selection['authorHeading']) + 1:]
        assert ' '.join(title_lines) == selection.get('sourceTitle', selection['title']), 'Reviewed title differs from source headings'
        text_status = selection.get('textStatus', 'complete')
        assert text_status in {'complete', 'fragment', 'draft'}
        if text_status == 'fragment':
            assert len(selection['endingEvidence']) > 8 and source['text'].endswith(selection['endingEvidence']), 'Fragment ending differs from reviewed source'
        elif text_status == 'draft':
            assert selection['draftEvidence'] in lines[:3], 'Draft marking is absent from source heading'
        if text_status != 'complete':
            assert selection.get('completenessNote'), 'Partial texts need an explicit completeness note'
        identity = lambda title, authors: (' '.join(title.casefold().split()), tuple(sorted(name.casefold() for name in authors)))
        assert selection['id'] in works or not any(work['id'] != selection['id'] and identity(work['title'], work['authors']) == identity(selection['title'], selection['authors']) for work in catalog['works']), 'Another work has the same title and author; review before importing'

        assert len(lines) > 3, 'Source must contain the actual work, not just a link'
        record = {
            'id': selection['id'], 'title': selection['title'], 'authors': selection['authors'],
            'genre': selection['genre'], 'period': selection.get('period', 'Ei päiväystä lähdesivulla'), 'page': source['id'],
            'status': {'complete':'Kokoteksti paikallisessa arkistossa', 'fragment':'Säilynyt tekstikatkelma; loppu päättyy kesken virkkeen', 'draft':'Lähteessä viimeistelemättömäksi merkitty teksti'}[text_status],
            'textStatus': text_status,
            'note': 'Tekijämerkintä säilytetään lähteen mukaisena. Tallennuspäivä ei ole kirjoituspäivä. Oppilastyön sisältöä ei tulkita kirjoittajan elämäkertatiedoksi.',
            'reviewedSourceSha256': source['sha256'],
            **({'previousSourceId': selection['previousSourceId']} if selection.get('previousSourceId') else {}),
        }
        if record['id'] in works:
            assert works[record['id']]['page'] in {source['id'], selection.get('previousSourceId')}, 'Existing ID belongs to another work'
            if selection.get('previousSourceId'):
                previous = sources[selection['previousSourceId']]
                assert any(link['url'] == selection['previousLinkUrl'] and link['label'].casefold() == selection['title'].casefold() for link in previous['links']), 'Previous listing must contain the reviewed work link and title'
                assert urlsplit(selection['previousLinkUrl']).path == urlsplit(source['originalUrl']).path, 'Recovered work path differs from reviewed listing'
                assert works[record['id']]['title'].casefold() == selection['title'].casefold(), 'Existing title differs from recovered work'
                assert works[record['id']]['authors'] == selection['authors'], 'Recovered attribution differs from original entry'
                record['note'] += ' Aiempi luettelolähde ' + selection['previousSourceId'] + '; kokoteksti palautettu DLC-tallenteesta.'
            works[record['id']].update(record)
        else:
            catalog['works'].append(record)
        texts[record['id']] = {'text': '\n'.join(lines), 'sourcePage': source['id'],
                              'transcription': 'visible-text-from-complete-original-html; automatic whitespace normalization; original spelling and line breaks retained',
                              'sourceSha256': source['sha256'], 'textStatus': text_status,
                              **({'completenessNote': selection['completenessNote']} if text_status != 'complete' else {})}
        for name in record['authors']:
            if name in people and record['id'] not in people[name]['works']:
                people[name]['works'].append(record['id'])
    for path, data in [('assets/archive/hyk-katalogi.json', catalog), ('src/_data/work-texts.json', texts)]:
        (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Imported {len(selected)} reviewed works; total {len(catalog["works"])}')


if __name__ == '__main__':
    main()
