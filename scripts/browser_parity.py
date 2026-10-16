"""Run the browser appearance/interaction harness against a local root server.

Build with SITE_PREFIX=/_site/ and serve the repository root on port 8765.
Requires Playwright and its Chromium browser (installed by the Pages deployment workflow).
"""
import json
import os
import time
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
from playwright.sync_api import sync_playwright

origin = os.environ.get('PARITY_ORIGIN', 'http://127.0.0.1:8765')
for attempt in range(50):
    try:
        with urlopen(origin + '/scripts/visual-parity.html', timeout=1) as response:
            assert response.status == 200
        break
    except URLError:
        if attempt == 49:
            raise
        time.sleep(.1)
with sync_playwright() as playwright:
    executable = os.environ.get('BROWSER_EXECUTABLE')
    browser = playwright.chromium.launch(**({'executable_path': executable} if executable else {}))
    page = browser.new_page(viewport={"width": 1500, "height": 1000})
    # Verify the actual new navigation and additive archive content independently
    # of the historical-content comparison, which restores the frozen nav shell.
    expected_labels = ['Etusivu', 'Koulu', 'Poroila', 'Verkkoarkisto', 'Lähteet ja tutkimus']
    catalog = json.loads(Path('assets/archive/hyk-katalogi.json').read_text(encoding='utf-8'))
    page.goto(origin + '/_site/verkkoarkisto/katalogi/')
    displayed = page.locator('[data-source-record]').evaluate_all("cards=>Object.fromEntries(cards.map(card=>[card.dataset.sourceRecord,card.querySelector('summary span').textContent]))")
    for record in catalog['dlc_records']:
        expected = record['mimetype'] + ' · ' + record.get('catalog_status', record['status'])
        assert displayed[record['id']] == expected, f'Stale recovery status: {record["id"]}'
    for width in (1440, 390):
        page.set_viewport_size({'width': width, 'height': 900})
        breadcrumb_style = None
        heading_style = None
        for route, labels in [('/olli-poroila/tuntemuksiani/', ['Etusivu','Poroila','Tuntemuksiani']),
                              ('/olli-poroila/', ['Etusivu','Poroila']),
                              ('/koulu/', ['Etusivu','Koulu']),
                              ('/teokset/T-001/', ['Etusivu','Koulu','Teokset','MUTANAAMIO']),
                              ('/tekijat/H-f95b196f07/', ['Etusivu','Koulu','Henkilöt ja tekijät','Aila Rantanen'])]:
            page.goto(origin + '/_site' + route)
            trail = page.locator('#pageTrail')
            assert trail.locator('a,strong').all_text_contents() == labels, route
            assert trail.get_attribute('aria-label') == 'Murupolku'
            assert trail.locator('[aria-current="page"]').count() == 1
            assert trail.locator('a').first.get_attribute('href') == '/_site/'
            style = trail.evaluate("el=>{const s=getComputedStyle(el);return ['fontFamily','fontSize','lineHeight','padding','backgroundColor','color'].map(key=>s[key])}")
            if breadcrumb_style is not None:
                assert style == breadcrumb_style, f'Inconsistent breadcrumb style: {route}'
            breadcrumb_style = style
            heading = page.locator('.page-heading')
            assert heading.count() == 1 and page.locator('h1').count() == 1, route
            expected_eyebrow = 'Poroila' if route.startswith('/olli-poroila/') else 'Koulu'
            assert heading.locator(':scope > .eyebrow').text_content() == expected_eyebrow, route
            page.evaluate('document.fonts.ready')
            style = heading.locator('h1').evaluate("el=>{const s=getComputedStyle(el);return ['fontFamily','fontSize','lineHeight','fontWeight','color'].map(key=>s[key])}")
            if heading_style is not None:
                assert style == heading_style, f'Inconsistent page heading style: {route}'
            heading_style = style
            if os.environ.get('QA_SCREENSHOTS') and route == '/olli-poroila/tuntemuksiani/':
                page.screenshot(path=f'.cache/shared-heading-{width}.png')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Breadcrumb overflow: {route}'
        page.goto(origin + '/_site/')
        assert page.locator('#pageTrail').count() == 0
        for route, active in [('/koulu/aineisto/', 'Koulu'), ('/tekijat/H-f95b196f07/', 'Koulu'),
                              ('/teokset/T-001/', 'Koulu'), ('/olli-poroila/kartta/', 'Poroila'),
                              ('/verkkoarkisto/', 'Verkkoarkisto'), ('/fiktiot/', 'Lähteet ja tutkimus')]:
            page.goto(origin + '/_site' + route)
            assert page.locator('#navigation a').all_text_contents() == expected_labels
            assert page.locator('#navigation a', has_text='Poroila').get_attribute('href') == '/_site/olli-poroila/'
            assert page.locator('#navigation a[aria-current="page"]').text_content().strip() == active, route
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Horizontal overflow: {width} {route}'
            for link in page.locator('#navigation a').all():
                assert link.is_visible()
                assert link.bounding_box()['height'] >= 40, f'Primary link too small: {width} {route}'
        page.goto(origin + '/_site/koulu/aineisto/DLC-0373/')
        page.get_by_role('link', name='Antti Kokkonen', exact=True).click()
        assert '/tekijat/' in page.url
        assert page.locator('[data-archive-expansion]').get_by_role('link').count() >= 2
        page.goto(origin + '/_site/koulu/koulukuvat/')
        page.locator('.prose img').evaluate_all("images => images.forEach(image => image.loading='eager')")
        page.wait_for_function("Array.from(document.querySelectorAll('.prose img')).every(image=>image.complete && image.naturalWidth>0)")
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Gallery overflow: {width}'
        if os.environ.get('QA_SCREENSHOTS'):
            Path('.cache').mkdir(exist_ok=True)
            page.screenshot(path=f'.cache/school-gallery-{width}.png')
        print(f'PASS: {width}px school hierarchy, active navigation, person round-trip and all local gallery images')
    page.set_viewport_size({'width': 1500, 'height': 1000})
    page.goto(origin + '/scripts/visual-parity.html')
    for viewport in ('desktop (1440px)', 'mobile (390px)'):
        page.get_by_role('button', name='Run ' + viewport, exact=True).click()
        page.wait_for_function("['passed','failed','error'].includes(document.body.dataset.status)", timeout=180000)
        report = page.locator('#results').inner_text()
        status = page.locator('body').get_attribute('data-status')
        if status != 'passed':
            print(report)
            raise AssertionError(f'{viewport}: {status}')
        print(f'PASS: {viewport}: {len(json.loads(report))} appearance and interaction comparisons')
    browser.close()
