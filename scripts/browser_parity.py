"""Run the browser appearance/interaction harness against a local root server.

Build with SITE_PREFIX=/_site/ and serve the repository root on port 8765.
Requires Playwright and its Chromium browser (installed by site-quality CI).
"""
import json
import os
import time
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
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1500, "height": 1000})
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
