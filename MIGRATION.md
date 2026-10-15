# Eleventy migration status

The interrupted migration already installed Eleventy, added recovered-text and
archive pages, and extracted some original sections. It also changed navigation,
page wrappers, the homepage composition and several layouts, and omitted original
interactive controls on the new pages.

The migration now builds the original views as separate Eleventy pages. Each
original section keeps its HTML, the original stylesheet is copied unchanged,
and shared templates preserve the original navigation, breadcrumbs, footer and
article dialogs. The old router has been replaced by ordinary links; existing
`#/...` bookmarks redirect to the corresponding page, including person cards.
The original source files remain available as a comparison baseline.

Edit content in `src/_includes/legacy/sections/`, shared markup in
`src/_includes/layouts/preserved-page.njk` and its partials, interaction code in
`src/assets/legacy.js`, and structured data in `src/_data/`. Normal builds use
these files directly; they do not re-extract the legacy monolith. The additional
recovered texts and archive originals from the previous work are retained.

Verified locally:

- 27 browser comparisons at 1440px and 27 at 390px: all pass. They cover all 19
  original views, a focused person card, and seven interactive states. Comparisons
  check visible text, DOM order, geometry and computed styles, after images/fonts
  load and with animations frozen identically in the test frames.
- Clean builds and smoke checks pass at `/`, `/poroila-jaljet/` and `/_site/`.
- 261 HTML pages, 5,887 local links, all 125 original person cards, 98 work pages,
  97 complete transcriptions and 148 archived originals pass the smoke checks.
- The archived originals pass their SHA-256 checks. `index.html`, `app.js`,
  `research-data.js` and `style.css` remain unchanged from the original Git state.
- Old school and person bookmarks were checked in the browser.

GitHub Pages now installs pnpm before setting up its dependency cache, builds
`_site/` for the repository subpath, and waits for the reusable browser-check job
before deployment. The workflow itself has not run on GitHub during this work.

All changes are local and uncommitted. Nothing has been pushed or deployed.
See `README.md` for preview and verification commands.
