# Hyrsylä / Jäljet

Hyrsylän koulun ja Olli Poroilan vanhojen verkkosivujen lähteisiin perustuva tutkimusarkisto. Eleventy rakentaa sisältösivut ja katalogit tavalliseksi HTML:ksi. Alkuperäinen ulkoasu, navigaatio ja selainkontrollit säilyvät.

## Kehitys

Tarvitaan Node.js 22, pnpm 10 sekä tarkistuksia varten Python 3.

```sh
pnpm install --frozen-lockfile
pnpm run serve
```

Avaa Eleventyn ilmoittama osoite. `pnpm build` tyhjentää vain `_site/`-hakemiston ja rakentaa sen uudelleen. Julkaistavat tiedostot ovat aina `_site/`-hakemistossa.

## Mistä mitäkin muokataan

| Hakemisto | Tarkoitus |
| --- | --- |
| `src/content/` ja aihehakemistot | Sivujen tekstit, osoitteet ja sivukohtainen metadata |
| `src/_includes/sections/` | Alkuperäisten näkymien sisältöosiot |
| `src/_includes/catalog/` | Henkilö-, teos-, kuva- ja tiedostokorttien dataohjatut pohjat |
| `src/_includes/research/` | Aikajanojen, lähdeluettelon ja korkkitaulun pohjat |
| `src/_includes/layouts/` ja `partials/` | Yhteinen sivurunko sekä alkuperäisen näkymän ja artikkelisivun esitystavat |
| `src/_data/` | Tutkimustiedot, navigaatio, korkkitaulu ja teosten kokotekstit |
| `src/assets/controls/` | Pienet selainkontrollit; `main.js` lataa vain sivun tarvitsemat moduulit |
| `src/styles/` | Alkuperäinen CSS; julkaistaan edelleen osoitteessa `/style.css` |
| `assets/archive/` | Julkaistavat arkistokuvat, katalogi, alkuperäistiedostot ja lähdemanifestit |
| `tools/research/` | Tutkimus- ja arkistointityökalut; eivät kuulu buildiin |
| `docs/research/` | Löytöjen lähteet, tutkimusmuistiot ja perustelut |
| `tests/fixtures/original-site/` | Jäädytetty vanha sivusto ulkoasun vertailua varten; ei julkaista |
| `scripts/` | Vain buildin ja laadunvarmistuksen työkalut |

Katalogin metatietojen lähde on `assets/archive/hyk-katalogi.json`. `catalog.js` yhdistää tietueet pohjille; samaa henkilöä ei poimita HTML:stä. Kenttä `catalog_status` säilyttää julkaistun luettelotekstin niissä 12 tietueessa, joiden tutkimusmerkintä `status` oli myöhemmin muuttunut.

`src/_data/work-texts.json` sisältää 97 palautuneen teoksen kokotekstit. Kaikilla 98 teosmerkinnällä on oma sivu. `assets/archive/originals/` sisältää 148 tarkkaa arkistokopiota, joiden lähteet ja SHA-256-tarkisteet ovat `originals-manifest.json`-tiedostossa. Git säilyttää alkuperäistiedostojen tavut ilman rivinvaihtomuunnoksia.

Navigaatio määritellään `navigation.js`- ja `originalNavigation.json`-tiedostoissa. `legacyRoutes.json` ja `src/scripts/bookmarks.js` säilyttävät vanhojen `#/...`-kirjanmerkkien toiminnan. `routeAliases.json` tuottaa uudelleenohjaukset siirrettyjen sivujen vanhoista osoitteista ja pitää sisäiset linkit kanonisina. Kartta ja hypoteesit ovat `/olli-poroila/`-osiossa, entisten oppilaiden myöhemmät vaiheet `/koulu/`-osiossa. Historialliset ulkoiset `~hyk`-osoitteet ovat alkuperäisiä lähdeviitteitä.

## Tarkistukset

Buildin jälkeen:

```sh
python scripts/site_smoke.py
```

Tarkistus varmistaa sivut, sisäiset linkit, kokotekstit, arkistokopioiden tarkisteet ja HTML:ään valmiiksi rakennetut aikajanat, lähteet sekä korkkitaulun kortit. Koko tutkimusdataa ei lähetetä jokaisen sivun mukana. JavaScript lisää suodatuksen, valinnat ja muut kontrollit.

Ulkoasuvertailuun rakennetaan sivusto polulla `/_site/`. PowerShellissä:

```powershell
$env:SITE_PREFIX = '/_site/'
pnpm build
python -m http.server 8765 --bind 127.0.0.1
```

Avaa `http://localhost:8765/scripts/visual-parity.html` ja käynnistä desktop- ja mobiilivertailu. Vertailu tarkistaa näkyvät tekstit, elementtijärjestyksen, sijainnit, mitat ja lasketut tyylit 1440 ja 390 pikselin leveyksillä. Se odottaa kuvat ja fontit sekä pysäyttää animaatiot samalla tavalla molemmissa testikehyksissä. Alkuperäistä vertailukappaletta ei muokata sivuston kehityksen mukana.

Automaattinen ajo on `python scripts/browser_parity.py` (vaatii Playwrightin ja Chromiumin). GitHub Actions ajaa sen ennen julkaisua.

## Julkaisu

GitHub Pages rakentaa sivuston `/poroila-jaljet/`-alipolulle ja julkaisee `_site/`-hakemiston vasta tarkistusten läpäistyä. Sivuston osoite on [penny-five.github.io/poroila-jaljet](https://penny-five.github.io/poroila-jaljet/).

Paikallisesti alipolku valitaan `SITE_PREFIX`-ympäristömuuttujalla. Tavallinen paikallinen kehitys käyttää `/`-juurta. Muutosten tilanne ja toteutuksen tausta ovat [siirtomuistiossa](docs/migration.md).
