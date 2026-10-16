# Kouluaineiston keruu ja julkaiseminen

Tämä ohje määrittää sisältötyön menetelmät. Lähtöinventaario on tarkistettu 16.10.2026. Ensimmäiset aihekohtaiset koonnit, paikalliset HTML-lukusivut, kuvagalleria ja henkilösivujen paluulinkit on sittemmin toteutettu; katso [ensimmäisen erän raportti](research/2026-10-16-kouluaineisto.md). Luetteloiden tietomalli ja ensimmäiset 30 uutta kirjoitelmaa on toteutettu; katso [teos- ja luetteloerän raportti](research/2026-10-16-teokset-ja-luettelot.md). Uudemmat oppilassivut, kuvat ja Pontus-pirun palautus on kuvattu [jatkoerän raportissa](research/2026-10-16-oppilassivut-ja-pontus.md). Kuvankäsittelytöiden lähdepohjaiset rinnakkaisnäkymät ja uudet runosivut on kuvattu [kuva- ja runoerän raportissa](research/2026-10-16-kuvamuunnokset-ja-runot.md). Leirikoulun historiatäydennys ja vanhojen MIME-merkintöjen kautta palautunut aineisto on kuvattu [Heponiemi-erän raportissa](research/2026-10-16-heponiemi-ja-mime.md). Jäljellä olevan aineiston erottelu jatkuu.

## Lähtötilanne ennen sisältövaihetta

Katalogissa on 34 HYK-sivumerkintää, 1 104 DLC-paikanninta, 125 henkilömerkintää, 98 työtä ja 105 kuvaviitettä. Paikallisia alkuperäistiedostoja on 148 ja kokotekstejä 97. Luvut ovat lähtötilanteen inventaario, eivät keruun kattavuuslupaus. Kuvaviite ei tarkoita palautettua kuvaa eikä DLC-paikannin luettua sisältöä. Henkilösivuja syntyy myös töiden tekijänimistä, joten niiden määrä eroaa henkilörekisterin määrästä.

Aloita paikallisista alkuperäistiedostoista ja tutkimusmuistioista. Poimi luokka-, lukuvuosi-, oppilassivu-, luettelo-, kuva- ja teoslinkit alkuperäisine suhteellisine osoitteineen. Ratkaise ne alkuperäisen sivun URL:n, mahdollisen `base`-elementin ja palvelimen hakemistorakenteen avulla. Tallenna samalla sivun kuvatekstit, otsikot ja tekijämerkinnät. Selvitä vasta tämän jälkeen, mitä pitää hakea verkkoarkistoista.

Ensimmäinen toteutuserä on yksi lähteissä selvästi rajautuva luokka/lukuvuosi tai oppilassivukokonaisuus: palautetaan sivut ja niiden media, tehdään koonti ja linkitetään tekijät sekä työt. Älä aloita kaikkien 1 104 paikantimen sokkolatauksella. Etene löydetyistä hakemistoista ja linkeistä, pidä sivustojen eri aikakaudet erillään ja kirjaa myös epäonnistuneet haut toistuvan turhan työn välttämiseksi.

## Tavoitehierarkia

Koulun koonnit perustuvat löydettyyn aineistoon. Aineistohakemisto `/koulu/aineisto/`, koulukuvat, oppilaiden sivut ja luokka-/luettelosivujen koonti on toteutettu. Luokkakohtaiset jäsenyydet ja kaikkien uusien teosten erottelu odottavat vielä lähteiden lähilukua. Päävalikon Koulu omistaa myös henkilö- ja teossivut; Verkkoarkisto on tallenteiden ja alkuperäisten sivustojen lähdenäkymä.

| Koonti | Ehdotettu osoite | Mitä lukija löytää |
| --- | --- | --- |
| Koulukuvat | `/koulu/koulukuvat/` | Luokka-, ryhmä-, tapahtuma- ja koulurakennuskuvat erillisinä ryhminä. Lukuvuosi ja luokka vain lähteen perusteella. Kuvakortista paikallinen kuva, kuvateksti, lähdesivu ja mahdollinen luokkakoonti. |
| Oppilaiden sivut | `/koulu/oppilaiden-sivut/` | Palautettujen omien ja yhteisten sivujen hakemisto; sivun alkuperäinen otsikko, tekijämerkinnät, ajallinen rajaus, paikallinen lukusivu ja säilytystila. |
| Luokat ja oppilasluettelot | `/koulu/luokat/` | Kunkin lähteessä esiintyvän luokan/lukuvuoden oma koonti: alkuperäinen luettelodokumentti, henkilöt, kuvat ja työt. Pelkkää nimilistaa ei nimetä luokaksi ilman lähdeperustetta. |
| Oppilastyöt | olemassa oleva `/koulu/oppilastyot/` | Teoskoonnit lajeittain ja lähteen sallimissa rajoissa lukuvuosittain/luokittain. Linkit pysyviin `/teokset/<id>/`-tietueisiin. |
| Koulun muut sivut | koonti `/koulu/`-sivulla; tarvittaessa omat alasivut | Projektit, retket, juhlat, opetussisällöt ja henkilökunnan esittelyt. Säilytä alkuperäisen sivun konteksti. |

Esimerkkipolku: **Koulu → Luokat → lähteessä nimetty luokka ja lukuvuosi → oppilaan henkilömerkintä → teos → paikallinen alkuperäislähde**. Koulukuvasta voi siirtyä samaan luokkakoontiin. Henkilösivun osoite säilyy `/tekijat/<id>/`, vaikka koulun navigaatiossa käytetään sanaa oppilas.

Koulun koonnit ovat aihekohtainen lukijanäkymä. Verkkoarkisto säilyttää palvelin-/sivustokohtaisen lähdenäkymän. Yksi lähde tai teos voi näkyä useassa koonnissa saman tietueen avulla.

## Tietueet ja suhteet

Nykyiset kentät ja tunnisteet säilytetään. Älä kirjoita uuden skeeman näköistä dataa ilman, että lukevat pohjat ja tarkistukset päivitetään samassa muutoksessa.

| Tieto | Nykyinen tallennuspaikka | Täydennysohje |
| --- | --- | --- |
| Lähdesivu | `hyk-katalogi.json`: `pages`, `dlc_records` | `id`, `original_url`, `archive_url`, `timestamp`, palautustila. Säilytä eri versioiden tiedot erikseen. |
| Henkilömerkintä | saman katalogin `people` | `id`, `name`, `observations`, `documents`, `works`. Perustele rooli, nimiasu, luokka ja tekijyys havaintokohtaisesti. |
| Teos | saman katalogin `works` | `id`, `title`, `authors`, `genre`, `period`, `page`, `status`, `note`. `authors` sisältää nyt nimiä; jos tarvitaan tarkempi henkilö-ID-suhde, toteuta se yhteensopivasti. |
| Kokoteksti | `src/_data/work-texts.json`, teoksen ID avaimena | `text`, `sourcePage`, `transcription`; puuttuva sisältö kuvataan, sitä ei täytetä arvauksella. |
| Kuva | katalogin `images` | Nykyiset `id`, `original_url`, `filename`, `kind`, `status`, `sources`, `labels`. Lisää paikallisen tiedoston ja kuvatekstin tuki sekä kuvan esityspohja keruun yhteydessä. |
| Paikallinen alkuperäistiedosto | `assets/archive/originals/` ja `originals-manifest.json` | Tiedoston `id`, kokoelma, lähde- ja raaka-arkisto-URL, aikaleima, MIME, tavut, SHA-256, `local_path`, tarkkojen alkuperäistavujen tila. Johdannaista ei merkitä tarkaksi alkuperäiskopioksi. |
| Luokkaluettelo | `src/_data/school-collections.json` | Pysyvä ID, otsikko, luokka-aste, ajallinen rajaus perusteluineen, lähde-ID ja SHA-256 sekä nimimerkintöjen henkilöviitteet. Älä yhdistä eri vuosien listoja samaksi luokaksi ilman näyttöä. |
| Historiallinen väite | `src/_data/research.json` | Lisää lähde `sources`-listaan ja käytä sen ID:tä aikajanan/artikkelin `refs`-kentässä. Katalogin `HYK-*`/`DLC-*`-tunniste ei yksin ole `S*`-lähdetunniste. |
| Korkkitaulu | `src/_data/graph.json` | Solmuilla on `refs`, kuvaus ja todistustila; nykyisillä reunoilla vain `from`, `to`, `status`. Suhteen perustelun ja lähdeviitteen tuki pitää toteuttaa, jos nykyinen solmukuvaus ei yksilöi sitä. |

Luokkajäsenyys, tekijyys, kuvassa esiintyminen ja sivulla mainitseminen ovat eri suhteita. Kullekin uudelle suhteelle tarvitaan lähde ja perustelu. Säilytä nimiasu lähteen mukaisena; mahdollinen korjattu hakumuoto on erillinen tieto. Samannimisiä tai pelkällä etunimellä esiintyviä henkilöitä ei yhdistetä ilman näyttöä.

Nykyinen `catalog.js` yhdistää kuvia henkilöihin myös yhteisen lähdesivun ja nimilabelin avulla. Tämä on hakuvihje, ei varmennettu kuvantunnistus. Ennen nimettyä koulukuvagalleriaa erottele lähdesivuyhteys ja lähteen vahvistama kuvassa esiintyminen tietomallissa ja näkyvässä tekstissä. Myös tekijälistan nimipohjainen yhdistäminen on arvioitava, jos vastaan tulee erillisiä samannimisiä henkilöitä.

## Yhden löydön käsittely

1. **Tunnista lähde.** Kirjaa alkuperäinen URL, mistä linkki löytyi, arkistotallenne ja tallenteen aikaleima. Tarkista olemassa olevat tunnisteet ja duplikaatit. Verkkoarkiston aikaleima kertoo säilymisestä, ei sisällön syntymisestä.
2. **Palauta sisältö ja riippuvuudet.** Hae HTML:n lisäksi siihen kuuluvat kuvat, piirrokset, ladattavat työt ja sisältöä kantavat kehykset. Suosi saman tallennusajankohdan resursseja; jos kuva palautuu eri tallenteesta, kirjaa ero. Tarkista, että vastaus on oikea sisältö eikä Waybackin virhe- tai käyttöliittymäsivu. CDX-merkintä tai HTTP 200 ei yksin riitä.
3. **Tallenna tavut.** Säilytä alkuperäistiedosto omassa arkistossa, laske SHA-256 ja kirjaa alkuperätiedot manifestiin. Nimeä uusi tiedosto törmäyksettömästi tietueen ja tarvittaessa version perusteella. Jos samoilla tavuilla on useita lähteitä, säilytä kaikkien alkuperätiedot.
4. **Tee sivuston oma esitys.** Näytä kuva paikallisesta tiedostosta, runo tai kertomus kokotekstinä ja oppilassivu turvallisena lukuversiona. Säilytä rivijako, tekijämerkintä ja lähteen kirjoitusasu; merkitse lukukelvottomat kohdat. OCR ja korjattu lukuteksti ovat johdannaisia, joiden menetelmä ja epävarmuudet kerrotaan. Älä korvaa puuttuvaa kuvaa tekoälyllä tehdyllä kuvalla.
5. **Kirjaa suhteet.** Linkitä lähdesivu, tekijä, teos, kuva, luokka ja lukuvuosi vain siltä osin kuin lähde osoittaa. Yhteisteos voi kuulua usealle tekijälle. Yksi oppilassivu voi sisältää monta teosta ja yhteisiä kuvia.
6. **Julkaise oikeassa koonnissa.** Paikallinen tiedosto yksin ei riitä: sen pitää löytyä koulun selauspolulta. Lisää paluulinkit henkilölle ja lähteeseen. Näytä lähdeviitteenä myös alkuperäinen URL sekä Wayback-versio.
7. **Arvioi historiallinen merkitys.** Täydennä tarvittaessa koulun tai Poroilan historiaa alla kuvatulla tavalla. Kirjaa myös tulkintaa vastaan puhuva tai aiempaa ajoitusta muuttava näyttö.
8. **Tarkista ja kirjaa erä.** Testaa sivut, paikalliset tiedostot ja suhteet. Tee työmuistio `docs/research/`-hakemistoon: mitä tutkittiin, palautui ja jäi puuttumaan sekä seuraavat konkreettiset hakukohteet.

Palautustiloissa erotetaan vähintään **vain viite**, **haettu mutta tarkistamatta**, **paikallisesti säilytetty**, **luettu ja linkitetty** sekä **ei löytynyt tarkistetuista tallenteista**. Nämä ovat käsitteelliset tilat; sovita ne nykyisiin kenttiin dokumentoidusti tai toteuta yhtenäinen tilakenttä. Vanhaa `catalog_status`-esitystekstiä ei käytetä todisteena tiedoston nykyisestä palautustilasta.

## Omat tiedostot ja ulkoiset arkistot

Julkaistavan kuvan `src` tai teoksen sisältö ei saa riippua Waybackista. Johdannaiset voi sijoittaa esimerkiksi `assets/archive/media/`-hakemistoon, alkuperäistavut pysyvät `originals/`-hakemistossa. Kummatkin kopioituvat nykyisellä Eleventy-asetuksella julkaisuun.

Pidä tarkka HTML-kopio ja sivuston oma lukusivu erillään: vanhassa HTML:ssä voi olla rikkinäisiä suhteellisia linkkejä, ulkoisia kuvaviitteitä, kehyksiä ja skriptejä. Pelkkä HTML-kopion lataaminen ei tee siitä itsenäisesti toimivaa paikallista sivua. Raakakopiosta kertovan linkin nimi erotetaan paikallisesta lukusivusta.

Puuttuva tiedosto jää näkyväksi aukoksi: kerro mitä on säilynyt, mitä ei ja millä perusteella tiedetään tiedoston olleen olemassa. Älä merkitse koko sivua täydelliseksi, jos sen kuvat puuttuvat. Esityskuvan tai kuvakaappauksen säilyminen ei tarkoita alkuperäisen kuvatiedoston palautumista.

## Poroilan historia ja korkkitaulu

Koulusivun allekirjoitus, tehtäväluettelo, päivätty kirjoitus tai projektin vastuuhenkilömerkintä voi täydentää Poroilan historiaa. Kirjaa täsmällinen lähdekohta ja erottele lähteen oma päiväys, päätelty aikaväli ja tallennuspäivä. Lisää `research.json`-lähde, aikajanatapahtuma ja tarvittaessa artikkelitekstin täydennys. Koulun tapahtuma kuuluu `schoolTimeline`-listaan, Poroilaa koskeva tapahtuma `timeline`-listaan; sama lähde voi perustella molempia eri kuvauksin.

Lisää korkkitaulun solmu tai yhteys vain, jos sillä on tutkimuskysymyksen kannalta selvä merkitys ja lähde osoittaa juuri kuvatun suhteen. Oppilaan nimi, runon aihe, samassa kuvassa esiintyminen tai yhteinen koulu eivät itsessään osoita henkilökohtaista suhdetta, yhteistyötä tai mitään oikeusasiaan liittyvää. Älä siirrä koko oppilasrekisteriä korkkitaululle.

Kuvaa yhteys täsmällisesti, esimerkiksi lähteessä nimenomaisesti mainittu toimitus- tai ohjaustehtävä, älä epämääräisesti ”yhteys”. Dokumentoitu suhde ja avoin hypoteesi erotetaan myös näkyvässä esityksessä. Hypoteesille kirjataan näyttö, epävarmuus ja se, mikä havainto voisi vahvistaa tai kumota sen. Pelkkä katkoviiva ei korvaa perustelua.

## Laadunvarmistus ja valmistumisraja

- Rakenna sivusto ja aja `scripts/site_smoke.py` samalla `SITE_PREFIX`-arvolla. Tarkista ainakin paikallinen `/` ja ennen julkaisua `/poroila-jaljet/`.
- Varmista uusien tietueiden yksilölliset ID:t, viitteiden olemassaolo, manifestien tavumäärät ja tarkisteet sekä uuden median päätyminen `_site/`-hakemistoon. Lisää merkitykselliset datatarkistukset, kun uusi kokoelma- tai suhdetietomalli toteutetaan.
- Avaa uusi koonti, henkilö, teos ja lukusivu sekä tietokoneen että puhelimen leveydellä. Tarkista kuvien latautuminen, kuvatekstit, pitkät tekstit ja polku koonnista takaisin lähteeseen. Varmista, että ensisijainen sisältö toimii ilman verkkoarkiston yhteyttä.
- `tests/fixtures/original-site/` on jäädytetty vertailuaineisto. Sisällön kasvattaminen voi muuttaa vanhaan sivuun vertaavan testin tekstiä ja mittoja tarkoituksella. Säilytä fixture ja ulkoasun tarkistus; rajaa tai täydennä testi koskemaan säilyvää rakennetta ja tarkista uusi sisältö erikseen. Älä poista koko vertailua äläkä päivitä fixturea vastaamaan uutta sivua.
- Tarkista uusi navigaatio molemmissa esitystavoissa. Siirrettävälle vanhalle sivulle lisätään uudelleenohjaus, ja sisäiset linkit vaihdetaan kanoniseen osoitteeseen.
- Valmis erä sisältää paikalliset sisällöt, todennettavat lähteet, toimivan hierarkian ja työmuistion aukoista. Kerro toteutuneet lisäykset erikseen jatkosuunnitelmista. Älä ilmoita koko koulun arkistoa palautetuksi yhden osakokonaisuuden perusteella.
