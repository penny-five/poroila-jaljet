#!/usr/bin/env python3
"""Playwright smoke test for the live-built static research archive.

Starts against a local http.server started in GitHub Actions. Checks every route,
the research board, bibliography filtering, article modal and mobile menu.
Does not visit external sources.
"""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = os.environ.get("SITE_URL", "http://127.0.0.1:8765")
ROUTES = [
  "alku", "sivujaljet", "koulu", "muistitieto", "oppilaat", "arkisto",
  "kartta", "aikajana", "aineisto", "hypoteesit", "fiktiot", "lahteet", "jatkovaiheet", "kouluaikajana", "oikeus"
]

def check(condition, msg):
    if not condition:
        raise AssertionError(msg)

def test_view(browser, mobile=False):
    viewport={"width":390,"height":844} if mobile else {"width":1440,"height":900}
    ctx=browser.new_context(viewport=viewport, is_mobile=mobile, has_touch=mobile)
    page=ctx.new_page()
    errors=[]
    page.on("pageerror", lambda err: errors.append(str(err)))
    page.goto(f"{BASE}/#/alku", wait_until="domcontentloaded")
    page.locator("#sourceList .source-entry").first.wait_for(state="attached", timeout=20000)
    board_count=page.locator("#corkboard .node").count()
    check(board_count>=14, f"Corkboard only has {board_count} cards")
    check(page.locator("#strings .string-line").count()>=12, "Corkboard links did not render")
    initial_count=page.locator("#sourceList .source-entry").count()
    check(initial_count>=35, f"Only {initial_count} source cards were rendered")

    for route in ROUTES:
        page.goto(f"{BASE}/#/{route}",wait_until="domcontentloaded")
        page.wait_for_function("(id) => document.body.dataset.page === id", arg=route, timeout=12000)
        check(page.locator(f"main > section#{route}").is_visible(), f"Page invisible: {route}")
        check("HYRSYLÄ" in page.title(), f"Wrong page title: {page.title()}")
        visible=page.locator("main > section:not([hidden])").count()
        check(visible == 1 or (route=="alku" and visible==3), f"Wrong number of visible sections for {route}: {visible}")
        if route=="arkisto":
            check(page.locator(".legacy-archive-dossier").count()==1, "Archived HTML link dossier missing")
        if route=="muistitieto":
            check(page.locator(".oral-numbers .oral-bar").count()==4, "Pupil-count visualization missing")
        if route=="oppilaat":
            check(page.get_by_role("heading", name="Missä oppilaiden sivut ovat?").is_visible(), "Pupil-work research page missing")
        if route=="sivujaljet":
            check(page.locator(".dig-child-pages li").count()>=13, "Historical school page tree missing")
        print(f"OK route {route}", flush=True)

    # Filter and clear the source index.
    page.goto(f"{BASE}/#/lahteet")
    page.locator("#sourceSearch").fill("tuntematon_hakutermi_123")
    check(page.locator(".source-entry").count()==0, "Source index search has no effect")
    page.locator("#sourceSearch").fill("Hyrsyl")
    check(page.locator(".source-entry").count()>0, "School-related source search returned nothing")
    page.locator("#sourceSearch").fill("")
    check(page.locator(".source-entry").count()==initial_count, "Source list did not restore")

    # Timeline controls are functional.
    page.goto(f"{BASE}/#/aikajana")
    page.locator('#timeFilters [data-decade="1990"]').click()
    check(page.locator(".time-row").count()>0, "1990s timeline filter returned nothing")
    page.locator('#timeFilters [data-decade="all"]').click()
    check(page.locator(".time-row").count()>=10, "Timeline did not reset")

    page.goto(f"{BASE}/#/kouluaikajana")
    check(page.locator("#schoolTimelineList .time-row").count() > 0, "School timeline empty")
    check(page.locator("#schoolTimelineList").get_by_text("Kokeile elektroniikkaa", exact=True).count() == 0, "Personal publication leaked into school timeline")
    page.goto(f"{BASE}/#/oikeus")
    check(page.locator("#courtArticle").inner_text().strip(), "Court article empty")

    # Research articles must open and close without JavaScript exceptions.
    page.goto(f"{BASE}/#/aineisto")
    page.locator('[data-article="tech"]').first.click()
    check(page.locator("#articleDialog").evaluate("(el) => el.open"), "Article dialog did not open")
    page.locator("#articleClose").click()
    check(not page.locator("#articleDialog").evaluate("(el) => el.open"), "Article dialog did not close")

    if mobile:
        page.goto(f"{BASE}/#/alku")
        page.locator('#navigation a[href="#/koulu"]').click()
        page.wait_for_function("document.body.dataset.page === 'koulu'", timeout=12000)
        check(page.locator("body").get_attribute("data-page")=="koulu", "Mobile primary navigation failed")
        overflow=page.evaluate("document.documentElement.scrollWidth-window.innerWidth")
        check(overflow<=8,f"Mobile horizontal overflow is {overflow}px")
    check(not errors, f"Uncaught JavaScript browser errors: {errors}")
    print(f"PASS {'mobile' if mobile else 'desktop'}: {len(ROUTES)} routes, {initial_count} sources, {board_count} evidence cards.",flush=True)
    ctx.close()

def main():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=["--no-sandbox"])
        try:
            test_view(browser,mobile=False)
            test_view(browser,mobile=True)
        finally:
            browser.close()
    return 0

if __name__=="__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"BROWSER SMOKE TEST FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
