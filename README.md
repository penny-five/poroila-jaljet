# Hyrsylä / Jäljet

Lähteisiin perustuva verkkosivusto Hyrsylän koulusta, Olli Poroilasta ja heidän vanhoista verkkosivuistaan. Eleventy rakentaa Markdown-sivut, Nunjucks-pohjat ja JSON-katalogit tavallisiksi, suoraan avattaviksi HTML-sivuiksi. Alkuperäisten sivujen HTML, ulkoasu ja selainkontrollit säilyvät. Sivujen välillä liikutaan tavallisilla URL-osoitteilla vanhan hash-reitittimen sijaan.

## Paikallinen esikatselu

Asenna riippuvuudet ja käynnistä kehityspalvelin:

```sh
pnpm install
pnpm run serve
```

Avaa Eleventyn ilmoittama paikallinen osoite (oletuksena `http://localhost:8080`). Tuotantorakennelman voi luoda komennolla `pnpm build`; julkaistavat tiedostot syntyvät `_site/`-hakemistoon.

## Sisältö ja arkistokopiot

- `src/_includes/legacy/sections/` sisältää alkuperäiset 21 sisältöosiota täsmälleen alkuperäisen HTML:n mukaisina. Muokkaa sisältöä näissä osissa. Eleventy näyttää kullakin alkuperäisellä sivulla saman osion kuin vanha reititin. Etusivun ticker ja loppukehote säilyvät etusivulla; korkkitaulu on alkuperäisellä omalla sivullaan.
- `src/_includes/layouts/preserved-page.njk`, `legacy/head.njk`, `legacy/footer.njk` ja `partials/preserved-navigation.njk` säilyttävät alkuperäisen sivurungon, valikot, osionavigaation, murupolun ja artikkeli-ikkunat. Alkuperäisillä sivuilla ladataan vain alkuperäinen `style.css`; lisäsivujen tyylejä ei tuoda niiden päälle.
- `src/assets/legacy.js` sisältää alkuperäiset aikajana- ja lähdesuodattimet, katalogihaun, korkkitaulun ja artikkeli-ikkunat. Jokainen toiminto käynnistyy vain sitä tarvitsevalla sivulla. Data on tiedostoissa `src/_data/research.json` ja `graph.json`.
- `index.html`, `app.js` ja `research-data.js` säilyvät vanhan sivuston vertailukappaleina. Eleventy ei rakenna eikä julkaise vanhaa `index.html`-tiedostoa. `scripts/port_legacy_site.py`, `port_legacy_behaviour.py` ja `export_legacy_*` ovat kertaluonteisen siirron työkaluja; niitä ei ajeta normaalissa buildissa, sillä ne korvaisivat muokattavat osat vertailukappaleiden sisällöllä.
- `src/content/` ja aihehakemistot ovat sivujen reittikohtaiset aloitustiedostot. Alkuperäisten näkymien tiedostot sisällyttävät vastaavan HTML-osion; siirron aikana tehdyt täydentävät artikkeli-, kokoteksti- ja arkistosivut ovat edelleen käytettävissä.
- `src/_data/legacyRoutes.json` on vanhojen `#/...`-kirjanmerkkien ja niiden kanonisten alasivujen yhteinen reittikartta. Sivuston sisäiset linkit muunnetaan tavallisiksi sivuosoitteiksi; vanhat kirjanmerkit ohjataan oikealle alasivulle.
- `assets/archive/hyk-katalogi.json` on teos-, nimi- ja arkistoluetteloiden metatietojen lähde.
- `assets/archive/originals/` sisältää 148 talteen saatua alkuperäistiedostoa sellaisinaan. `originals-manifest.json` tallentaa lähdeosoitteet, arkistotallenteet ja SHA-256-tarkisteet.
- `src/_data/work-texts.json` sisältää 97 palautuneen teoksen täydet näkyvät tekstilitteroinnit. Lähdesivun koko alkuperäinen HTML on lisäksi ladattavissa alkuperäistiedostojen sivulta. Yhden 98 katalogimerkinnästä sisältöä ei saatu palautettua.
- `RESEARCH-*.md` sisältää tutkimusmuistiot ja perustelut.
- Tekijä- ja teoskohtaiset lisäsivut löytyvät tekijä-, teos- ja arkistoluetteloista. Historialliset `~hyk`-osoitteet jäävät alkuperäisiksi ulkoisiksi lähdeviitteiksi, ja sivuston sisäinen navigaatio käyttää kanonisia Eleventy-osoitteita.

Alkuperäistiedostojen kopioita ei normalisoida tai korjata. Niiden eheyden, vanhojen osioreittien, alasivujen ja sisäisten linkkien kevyt tarkistus ajetaan komennolla `python scripts/site_smoke.py` buildin jälkeen.

## Julkaisu

GitHub Actions asentaa pnpm:n ennen Node-välimuistin käyttöönottoa ja rakentaa sivuston GitHub Pagesin `/poroila-jaljet/`-alipolulle, tarkistaa vanhat osioreitit, sisäiset linkit ja alkuperäistiedostojen tarkisteet sekä julkaisee `_site/`-hakemiston. Julkaisuosoite on [penny-five.github.io/poroila-jaljet](https://penny-five.github.io/poroila-jaljet/).

## Ulkoasun ja toimintojen vertailu

`scripts/visual-parity.html` vertaa vanhaa sivustoa ja Eleventy-tulosta samalla selainmoottorilla. Tarkistus käy läpi 19 alkuperäistä näkymää ja henkilökohtaisen kortin sekä aikajanat, haut, lähdesuodattimen, artikkeli-ikkunan ja korkkitaulun. Näkyvät tekstit, elementtijärjestys, sijainnit, mitat ja lasketut tyylit verrataan 1440 ja 390 pikselin leveyksillä. Vain testikehyksissä animaatiot pysäytetään ja kuvat sekä fontit odotetaan valmiiksi.

Vertailu käyttää buildia polulla `/_site/`. PowerShellissä:

```powershell
$env:SITE_PREFIX = '/_site/'
pnpm build
python -m http.server 8765 --bind 127.0.0.1
```

Avaa `http://localhost:8765/scripts/visual-parity.html` ja käynnistä molemmat vertailut. Automaattinen versio on `python scripts/browser_parity.py` (vaatii Playwrightin ja Chromiumin). GitHub Actions ajaa sen erillisessä laatutyössä. Tavallinen `pnpm build` tekee aina puhtaan `_site/`-hakemiston; `SITE_PREFIX` asetetaan buildin julkaisuosoitteen mukaiseksi.
