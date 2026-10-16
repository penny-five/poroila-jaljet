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

Aineistoa täydentäville agenteille: [AGENTS.md](AGENTS.md) kuvaa sivuston osiot ja toteutuksen. [Sisällönkeruun ohje](docs/content-collection.md) määrittää koulukuvien, oppilassivujen, luetteloiden ja töiden tavoitehierarkian sekä uusien löytöjen arkistoinnin ja linkityksen.

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

`src/_data/work-texts.json` sisältää teosten kokotekstit, ja kaikilla katalogin teosmerkinnöillä on oma sivu. Teos- ja tekstimäärät muodostetaan katalogista. Tarkistetut uudet kirjoitelmat tuodaan `reviewed-school-works.json`-valinnan ja `tools/research/import_reviewed_school_works.py`-työkalun avulla. `assets/archive/originals/` sisältää alkuperäisen 148 tiedoston tutkimuspaketin sekä uudet arkistohaut. Lähteet ja SHA-256-tarkisteet ovat `originals-manifest.json`-tiedostossa. Uusien hakujen CDX-tarkistevertailu kirjataan tiedostokohtaisesti; poikkeava vastaus säilytetään varmistamattomana ja merkitään lukusivulla. Git säilyttää tiedostojen tavut ilman rivinvaihtomuunnoksia.

Päävalikko on Etusivu, Koulu, Poroila, Verkkoarkisto sekä Lähteet ja tutkimus. Koulu omistaa myös `/tekijat/`- ja `/teokset/`-sivujen navigaation. Fiktio on Lähteet ja tutkimus -osion alasivu. Koulun yleissivujen alanavigaatio ja aineiston sisäinen ryhmävalikko erotetaan toisistaan. Aineiston kaikki ryhmät tulevat `schoolSections.json`-määritelmästä myös valikkoon. Luokkaluettelot ovat `school-collections.json`-tiedostossa. Yhteinen navigaatio määritellään `navigation.js`-tiedostossa; `originalNavigation.json` säilyttää vanhojen näkymien nimet. `legacyRoutes.json` ja `src/scripts/bookmarks.js` säilyttävät vanhojen `#/...`-kirjanmerkkien toiminnan. `routeAliases.json` tuottaa uudelleenohjaukset siirrettyjen sivujen vanhoista osoitteista ja pitää sisäiset linkit kanonisina. Kartta ja hypoteesit ovat `/olli-poroila/`-osiossa, entisten oppilaiden myöhemmät vaiheet `/koulu/`-osiossa. Historialliset ulkoiset `~hyk`-osoitteet ovat alkuperäisiä lähdeviitteitä.

Koulun aihekohtainen aineistohakemisto on `/koulu/aineisto/`: kuvat, oppilassivut, luokat ja luettelot, runokokoelmat, taidesivut ja muu kouluaineisto. Paikalliset lukusivut generoidaan säilytetyistä HTML-tiedostoista `schoolArchive.json`-aineistoon komennolla `python tools/research/build_school_archive.py`. `schoolView.js` yhdistää ne henkilöihin, teoksiin ja toisiinsa. Koulun yhteisen oppilasvalikon nimiä ei käsitellä yksittäisen luokan oppilasluettelona. Lukusivut eivät suorita historiallisia skriptejä eivätkä tarvitse Waybackia tekstin tai palautettujen kuvien näyttämiseen.

Murupolku ja otsikkoalue ovat yhteisiä kaikille sisältösivuille. `lib/breadcrumbs.cjs` määrittää osion, vanhemmat ja näyttönimet; yhteiset pohjat ovat `partials/breadcrumbs.njk` ja `partials/page-heading.njk`. Eyebrow näyttää pääosion, H1 sivun nimen ja ingressi sivun `lead`-tekstin. Vanhojen näkymien ingressit ovat `pageIntros.json`-tiedostossa. Sivun sisältöön ei kirjoiteta toista pääotsikkoa. Etusivu säilyttää oman hero-otsikkonsa. Yhteiset tyylit ovat `breadcrumbs.css`- ja `page-heading.css`-tiedostoissa.

`python tools/research/recover_school_links.py --limit 20` hakee rajatun erän katalogin tunnetuista tallenteista, joihin säilyneet sivut linkittävät. `--retry` yrittää uudelleen aiemmin epäonnistuneita hakuja. Työkalu päivittää manifestin ja katalogin ja kirjaa kaikki yritykset `assets/archive/recovery-attempts.json`-tiedostoon. Aja sen jälkeen aineistogeneraattori uudelleen. Varmista aina build ja alla olevat tarkistukset ennen julkaisua.

## Tarkistukset

Buildin jälkeen:

```sh
python scripts/site_smoke.py
python scripts/school_archive_smoke.py
node --test tests/breadcrumbs.test.cjs
```

Tarkistus varmistaa sivut, sisäiset linkit, kokotekstit, arkistokopioiden tarkisteet ja HTML:ään valmiiksi rakennetut aikajanat, lähteet sekä korkkitaulun kortit. Koko tutkimusdataa ei lähetetä jokaisen sivun mukana. JavaScript lisää suodatuksen, valinnat ja muut kontrollit.

Ulkoasuvertailuun rakennetaan sivusto polulla `/_site/`. PowerShellissä:

```powershell
$env:SITE_PREFIX = '/_site/'
pnpm build
python -m http.server 8765 --bind 127.0.0.1
```

Avaa `http://localhost:8765/scripts/visual-parity.html` ja käynnistä desktop- ja mobiilivertailu. Vertailu tarkistaa näkyvät tekstit, elementtijärjestyksen, sijainnit, mitat ja lasketut tyylit 1440 ja 390 pikselin leveyksillä. Se odottaa kuvat ja fontit sekä pysäyttää animaatiot samalla tavalla molemmissa testikehyksissä. Alkuperäistä vertailukappaletta ei muokata sivuston kehityksen mukana.

Automaattinen ajo on `python scripts/browser_parity.py` (vaatii Playwrightin ja Chromiumin; paikallisen selaimen polun voi antaa `BROWSER_EXECUTABLE`-muuttujalla). Uusi navigaatio, aktiiviset osiot, henkilöiden paluulinkit ja koko paikallinen kuvagalleria tarkistetaan erikseen molemmilla leveyksillä. Historiallisten sisältöjen vertailu käyttää testissä vanhaa navigaatiorunkoa ja palautustilatekstejä; lisätyt aineistolohkot piilotetaan vain tässä vertailussa. Julkaistulla sivulla ovat aina uudet valikot, ajantasainen palautustila ja uudet aineistot. Ainoa GitHub Actions -työnkulku on `.github/workflows/pages.yml`: se tarkistaa ulkoasun ja toiminnan ennen julkaisua. Vanhat tutkimusajot on poistettu.

## Julkaisu

GitHub Pages rakentaa sivuston `/poroila-jaljet/`-alipolulle ja julkaisee `_site/`-hakemiston vasta tarkistusten läpäistyä. Sivuston osoite on [penny-five.github.io/poroila-jaljet](https://penny-five.github.io/poroila-jaljet/).

Paikallisesti alipolku valitaan `SITE_PREFIX`-ympäristömuuttujalla. Tavallinen paikallinen kehitys käyttää `/`-juurta. Muutosten tilanne ja toteutuksen tausta ovat [siirtomuistiossa](docs/migration.md).
