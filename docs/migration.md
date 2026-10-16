# Eleventy migration and modernization

The appearance-preserving migration is saved in baseline commit `62d7af2`.
The site uses Eleventy throughout; the original single-page implementation is
retained only as a frozen test fixture.

## Repository cleanup

- Active website source lives under `src/`; only published archive assets remain
  under `assets/`. The repository root contains the README and build configuration.
- Research notes moved to `docs/research/`, and research/recovery scripts to
  `tools/research/`. These are not build inputs or deployed files.
- The old HTML, browser application, data module and stylesheet moved to
  `tests/fixtures/original-site/`. The fixture's image URLs point at the retained
  archive assets; its content, design and behavior remain the comparison baseline.
- One-time extraction/conversion scripts, unused styles, the duplicate board
  script, unused quick-links partial and unused excerpt dataset were removed.
  Their previous versions remain recoverable from the baseline commit.
- `.gitattributes` disables text conversion for archived originals and test
  fixtures. Original archival bytes and their hashes now survive Git checkout.

## Templates and shared structure

The catalogue, person, work and image views now use small data-driven Nunjucks
macros. The four former sections totaled about 1 MB of repeated HTML; their entry
partials now total roughly 7 KB. Person pages render their record directly; the
build no longer extracts cards from HTML using regular expressions.

`assets/archive/hyk-katalogi.json` remains the shared metadata source. Twelve
records carry `catalog_status` to retain their published listing wording alongside
later research annotations in `status`. There is no second copy of the catalogue.

`layouts/base.njk` owns the shared document structure, navigation, footer and script
loading. The original and article wrappers retain their existing visible
presentations. Prose uses Markdown; entry files containing Nunjucks includes use
`.njk`.

## Page delivery

Timelines, source lists, court-article paragraphs, initial corkboard cards and
article-dialog content are rendered during the build. Initial content is present
without browser scripting. Small controls under `src/assets/controls/` provide
search, filtering, card selection/dragging, dialogs and copying. A page only loads
the control module it needs. The graph page receives only graph-related sources;
other pages receive no full research JSON payload.

The original stylesheet remains byte-for-byte unchanged. Generated HTML totals
about 3.1 MB instead of 9.8 MB (about 69% less); the homepage is about 7 KB instead
of 55 KB. These figures exclude the untouched historical archive copies.

## Verification

- All 54 browser appearance/interaction comparisons passed: 27 each at 1440px and
  390px, covering 19 original views, a focused person card and seven control states.
- Replacing the catalogue templates preserved the complete section markup across
  137 catalogue/person pages, including collapsed card contents.
- Consolidating layouts preserved body markup across all 117 supplementary pages.
- Smoke checks cover 261 pages, 5,887 local links, 125 original person cards,
  98 work pages, 97 full transcriptions and 148 SHA-256-verified originals.
- Smoke checks also confirm that initial timeline, source, court and corkboard
  content is rendered at build time and that full research JSON is not embedded
  in ordinary pages.
- Builds were checked at `/`, `/poroila-jaljet/` and `/_site/`. Asset-copy targets
  are separate to avoid overlapping directory-copy races on Windows.

GitHub Pages waits for browser checks before deployment. Pushes to `main` publish
only after verification passes.
See the root README for development and verification commands.


## Canonical page paths

Page addresses now follow the subject shown in navigation:

| Old address | Canonical address |
| --- | --- |
| `/tutkimus/kartta/` | `/olli-poroila/kartta/` |
| `/tutkimus/hypoteesit/` | `/olli-poroila/hypoteesit/` |
| `/tekijat/myohemmat-vaiheet/` | `/koulu/myohemmat-vaiheet/` |

The source templates live in the matching subject directories. Old addresses
remain as small static redirects; browser redirects retain query parameters and
fragments. Old hash bookmarks use the same canonical routes. Internal links and
both navigation presentations now use the canonical addresses. The Poroila
primary link consistently opens its original writings-and-sources view.

GitHub research-note links now point into `docs/research/`. Smoke checks validate
redirect targets, reject internal links through old aliases and verify links to
files in this repository. Builds now contain 261 content pages plus three
compatibility redirects.
