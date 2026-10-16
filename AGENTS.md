# Ohjeet sivustoa ja aineistoa täydentäville agenteille

## Tavoite

Tämä on Hyrsylän koulun ja Olli Poroilan lähteisiin perustuva tutkimusarkisto. Seuraava painopiste on koulun vanhojen verkkosivujen sisältöjen keruu: oppilassivut, oppilastyöt, koulukuvat, luokka- ja oppilasluettelot sekä koulun muut alasivut. Lukijan pitää voida lukea teokset ja katsoa palautetut kuvat tämän sivuston sisällä. Wayback-linkki on lähdeviite, ei valmiin arkistoinnin korvike.

Lue ennen sisältötyötä [sisällönkeruun ohje](docs/content-collection.md). Se erottaa nykyisen toteutuksen tavoitehierarkiasta ja määrittää löydön käsittelyn. Käyttäjän ohjeet ovat ensisijaisia.

## Sivuston loogiset osiot

| Osio | Sisältö ja vastuu |
| --- | --- |
| `/koulu/` | Koulun historia, toiminta, luokat, koulukuvat, oppilassivut ja oppilastöiden aihekohtaiset koonnit. Koulun sisältöjen ensisijainen selauspaikka. |
| `/tekijat/` ja `/tekijat/<id>/` | Samat historialliset henkilömerkinnät kaikista kokoelmista. Henkilösivulta linkit lähteessä osoitettuihin töihin, oppilassivuihin ja luokkamerkintöihin. Myös muut kuin teosten tekijät kuuluvat tähän rekisteriin. |
| `/teokset/` ja `/teokset/<id>/` | Runojen, kertomusten, kuvataiteen ja muiden yksilöitävien töiden pysyvät tietueet; koko sisältö, tekijämerkintä ja lähde. Koulun koonnit linkittävät näihin, eivät luo rinnakkaiskopioita. |
| `/verkkoarkisto/` | Alkuperäisten sivustojen rakenne, tallenteet, katalogi, tiedostot ja palautustilanne. Tekninen lähdenäkymä koulun aihekohtaisten koontien rinnalla. |
| `/olli-poroila/` | Poroilan oma historia, kirjoitukset, aikajana, lähteistetyt yhteydet eli korkkitaulu (`kartta/`), avoimet hypoteesit ja oikeusprosessin lähteet. |
| `/lahteet/` ja `/tutkimus/` | Lähdeluettelo, tutkimuksen menetelmät, epävarmuudet ja tausta. Työmuistiot ovat lisäksi `docs/research/`-hakemistossa. |
| `/fiktiot/` | Selvästi fiktioksi merkitty sisältö. Fiktiota ei käytetä historiallisen väitteen todisteena. |

Päävalikko on **Etusivu · Koulu · Poroila · Verkkoarkisto · Lähteet ja tutkimus**. Henkilöt ja teokset kuuluvat navigaatiossa Kouluun, vaikka niiden pysyvät osoitteet ovat `/tekijat/` ja `/teokset/`. Fiktio löytyy Lähteet ja tutkimus -osion alasivuista. Sisältöä selataan aiheen mukaan, alkuperäisiä sivustoja ja palautustilannetta Verkkoarkistossa.

Älä sijoita koulun sisältöjä Poroilan osioon vain rehtoriyhteyden vuoksi. Älä siirrä Poroilan karttaa takaisin tutkimusosion alle. Tavoitteena on ristiinlinkitys, ei saman aineiston kopiointi eri osioihin.

## Toteutuksen kartta

- Eleventy 3, Nunjucks/Markdown; `eleventy.config.cjs` määrittää polut ja suodattimet. Lähde on `src/`, generoitu julkaisu `_site/`. Älä muokkaa `_site/`-tiedostoja käsin.
- Sivujen sisääntulot ovat `src/content/`- ja aihehakemistoissa. Tarkista front matterin `permalink`: tiedoston nimi ei välttämättä vastaa julkista osoitetta.
- `src/_includes/layouts/base.njk` on yhteinen runko. `original-page.njk` säilyttää vanhojen näkymien esityksen, `article-page.njk` sopii uusille sisältösivuille. `sections/`, `catalog/` ja `research/` sisältävät näkymien osat.
- Kaikki sisältösivut käyttävät yhteisiä `partials/breadcrumbs.njk`- ja `partials/page-heading.njk`-osia. `lib/breadcrumbs.cjs` johtaa murupolun ja eyebrow-osionimen navigaatiosta. Pääotsikko tulee sivun `title`-kentästä tai henkilö-/teos-/lähdetietueesta; ingressi `lead`-kentästä, vanhoilla näkymillä tarvittaessa `pageIntros.json`-tiedostosta. Älä lisää sivukohtaista pääotsikkoa tai dossier-eyebrow'ta sisältöön. Sivulla on yksi H1. Etusivun oma hero säilyy poikkeuksena. `breadcrumbTitle` ja `headingTitle` ovat tarvittaessa lyhyiden näyttönimien poikkeukset, eivät uusia rinnakkaisia otsikkojärjestelmiä.
- `assets/archive/hyk-katalogi.json` on henkilöiden, töiden, lähdesivujen ja kuvaviitteiden metatietojen lähde. `src/_data/catalog.js` yhdistää tietueet sivuille. Älä ylläpidä henkilöluetteloa käsin HTML:ssä.
- `src/_data/work-texts.json` sisältää töiden kokotekstit. `assets/archive/originals/` ja `originals-manifest.json` säilyttävät tarkat alkuperäistavut ja niiden alkuperätiedot. `assets/archive/manifest.json` koskee erillisiä tallennekuvia, ei kaikkia koulukuvia.
- `src/_data/research.json`: lähteet, Poroilan aikajana, koulun aikajana ja artikkelit. `graph.json`: korkkitaulun solmut ja yhteydet. `graphView.js` muodostaa käytetyt lähteet.
- `src/_data/navigation.js`: kaikille sivuille yhteinen pää- ja alanavigaatio. `originalNavigation.json`: vanhojen näkymien nimet ja historiallinen ryhmittely; ryhmittelyä ei enää käytetä valikon muodostamiseen. `legacyRoutes.json` ja `src/scripts/bookmarks.js`: vanhat hash-osoitteet. `routeAliases.json`: siirrettyjen osoitteiden uudelleenohjaukset.
- `src/_data/schoolArchive.json`: paikallisista alkuperäisistä generoitu lukuteksti, linkkiverkko ja media; päivitä komennolla `python tools/research/build_school_archive.py`. `schoolView.js` muodostaa koonnit ja paluulinkit. `src/koulu/aineisto/`: paikalliset lukusivut ja koontien pohjat. `assets/archive/media/`: kuvien saman sisältöiset, oikealla tiedostopäätteellä tarjoillut esityskopiot.
- Linkit tehdään `localUrl`-suodattimella ja sivurungon `prefixPaths`-käsittelyn mukaisesti. Älä kovakoodaa tuotannon `/poroila-jaljet/`-etuliitettä sisältöön. Paikallisen `/`-juuren ja Pages-alipolun pitää toimia.
- `src/styles/site.css`: säilytettävä ulkoasu. Uudet sisällöt sovitetaan nykyisiin rakenteisiin. `src/assets/main.js` lataa sivun tarvitsemat kontrollit; toimivan sisällön pitää syntyä HTML:ään jo buildissa.
- `tools/research/`: erikseen ajettavat tutkimustyökalut. Lue polut ja kirjoituskohteet ennen ajoa; siirrettyjen työkalujen oletuspolut eivät ole automaattisesti luotettavia. Älä aja palautusskriptiä koko arkiston päälle uusien löytöjen lisäämiseksi.

## Työn perussäännöt

1. Inventoi olemassa oleva aineisto ennen uutta verkkokeruuta. Älä tulkitse katalogimerkintää luetuksi sivuksi tai palautetuksi kuvaksi.
2. Säilytä nykyiset tunnisteet ja osoitteet. Älä numeroi tietueita uudelleen. Uudelle tietueelle annetaan vapaa pysyvä tunniste; sama tiedostonimi eri palvelimella ei tarkoita samaa lähdettä.
3. Säilytä alkuperäinen tiedosto muuttamattomana. Tee lukuteksti, turvallinen esityssivu ja mahdollinen esikatselu erillisiksi johdannaisiksi. Älä suorita vanhojen sivujen skriptejä uudessa sivurungossa.
4. Dokumentoi jokaiselle uudelle tiedostolle lähdeosoite, arkistotallenne, tallenteen ajankohta, hakupäivä, paikallinen polku, tavumäärä ja SHA-256. Säilytä vanhat versiot; muuttuneen sisällön ei pidä korvata aiempaa tallennetta huomaamatta.
5. Lähdehavainto, tulkinta ja avoin kysymys erotetaan. Tallennuspäivä ei ole teoksen syntymäpäivä. Nimen tai kuvan tulkintaa ei vahvisteta pelkällä arvauksella.
6. Henkilötietue käsittelee lähteessä näkyvää historiallista nimeä. Älä päättele nykyistä henkilöllisyyttä, yhteystietoja tai myöhempää elämää nimiosuman perusteella. Oppilaan työ tai koulunkäynti ei itsessään ole henkilökohtainen yhteys Poroilaan korkkitaululle.
7. Päivitä löydön kaikki perustellut yhteydet: lähdesivu → paikallinen sisältö → luokka/koonti → henkilö → teos; tarvittaessa koulun tai Poroilan aikajana ja lähteistetty korkkitauluyhteys.
8. Säilytä toimiva ulkoasu. Uuden sisällön lisääminen on sallittua; vanhan vertailufixturen muokkaaminen testin läpäisemiseksi ei ole. Katso sisältömuutosten vertailuohje pidemmästä ohjeesta.
9. Synkronoitu `sources/` repojuuren ulkopuolella on vain luettavaa viiteaineistoa. Älä muokkaa, siirrä tai poista sen tiedostoja.
10. GitHubissa on vain `.github/workflows/pages.yml`, jossa ovat tarkistukset ja julkaisu. Älä palauta vanhoja tutkimustyönkulkuja. Commit/push tehdään käyttäjän antaman toimeksiannon laajuudessa; push `main`-haaraan julkaisee sivuston.

## Valmis sisältöerä

Löytöä ei merkitä palautetuksi ennen kuin tiedosto tai kokoteksti on paikallisesti olemassa, alkuperä on kirjattu ja sisältö löytyy sivuston selaushierarkiasta. Puuttuva aineisto saa näkyvän puuttumistilan ja perustellun seuraavan hakutoimen. Raportoi erän jälkeen lisätyt lähteet, paikalliset sisällöt, linkitykset ja jäljelle jääneet aukot.

Tarkistukset: `pnpm build`, `python scripts/site_smoke.py` sekä sisältöerään sopivat selain- ja linkkitarkistukset. Julkaisua varten varmista myös `SITE_PREFIX=/poroila-jaljet/`-build. Tarkat komennot ja ulkoasuvertailu ovat [README:ssa](README.md).
