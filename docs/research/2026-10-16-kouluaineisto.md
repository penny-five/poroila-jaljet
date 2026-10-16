# Koulun lukusivut, kuvat ja ensimmäinen laajennus 16.10.2026

## Toteutunut erä

Alkuperäisessä tutkimuspaketissa oli 148 tiedostoa. Tässä erässä haettiin säilyneiden sivujen linkeistä 119 uutta tiedostoa: kokonaismäärä on 267. Kouluaineistosta on nyt 180 paikallista HTML-lukusivua ja 76 paikallista kuvatiedostoa. Muut tiedostot ovat muun muassa PDF:iä ja alkuperäispaketin erillisiä kunta-/MBnet-lähteitä. Tiedostokohtaiset lähteet, arkistoajankohdat, hakupäivät ja SHA-256 ovat `assets/archive/originals-manifest.json`-tiedostossa. Vanhojen alkuperäistiedostojen tavuja ei muutettu.

Lukusivut jakautuvat viiteen ryhmään: 91 oppilaiden sivua tai kirjoitelmasivua, 19 luokka- tai luettelosivua, 15 runo-/oppilastyösivua, 12 kuva-/taidehakemistoa sekä 43 muuta koulusivua. Nämä ovat säilyneitä lähdesivuversioita, eivät eri henkilöiden tai teosten lukumääriä.

Kuvista 15 on luokka-/ryhmäkuvien ryhmässä, 14 oppilastöiden/kuvataiteen ryhmässä, 31 oppilassivujen kuvissa, 7 koulutilojen/tapahtumien ryhmässä ja 9 muussa grafiikassa. Luokitus perustuu tiedostonimeen ja lähdesivuyhteyteen; se ei vahvista kuvassa olevien henkilöiden nimiä. Esityskopion tavut ovat samat kuin manifestin säilytetyssä tiedostossa; oikea tiedostopääte mahdollistaa vanhojen `.bin`-kuvien näyttämisen selaimessa.

## Hierarkia

Koulu sisältää historian, luokat, ihmiset, oppilassivut, teokset ja kuvat. Henkilöiden ja teosten pysyvät osoitteet säilyvät `/tekijat/`- ja `/teokset/`-poluissa. Verkkoarkisto on alkuperäisten sivustojen, tiedostojen ja palautustilanteen lähdenäkymä. Poroilan historia ja korkkitaulu ovat erillinen kokonaisuus. Päävalikko on yhteinen kaikilla sivuilla. Fiktio löytyy Lähteet ja tutkimus -osiosta.

Koulun aineiston aloitus on `/koulu/aineisto/`. Siitä pääsee koulukuviin, luokka- ja oppilasluetteloihin, oppilaiden sivuihin, runoihin ja kirjoitelmiin sekä muihin koulusivuihin. Lukusivun osoite on `/koulu/aineisto/<lähteen-id>/`. Linkit yhdistetään säilytettyihin sivuihin ja kuviin saman alkuperäisosoitteen perusteella; eri palvelimia ei tulkita automaattisesti samaksi lähteeksi. Henkilösivulta pääsee takaisin sitä koskevaan lähdetekstiin.

## Merkittävät havainnot ja rajaukset

- `DLC-0129`, `entiset-luokkakuvat.htm`, sisältää lukuvuosittaisen vanhojen luokkakuvien hakemiston vuosista 1985–1986 lähtien. Sen linkkitekstit ja edeltävä lukuvuosiotsikko tuodaan myös kuvagallerian lähdeviitteisiin. Hakemistossa on edelleen paljon palauttamattomia kuvia.
- Luokkasivuilla oleva `VALITSE OPPILAS` -valikko on koulun yhteinen navigaatio, ei kyseisen luokan rosteri. Sen nimiä ei sisällytetä luokkasivun varsinaiseen lukutekstiin. Valikon lähdelinkit säilytetään erillisessä linkkiosassa.
- Lähteen tekstissä esiintyvä kokonainen nimiasu yhdistetään olemassa olevaan historialliseen henkilömerkintään. Tämä on nimiosuma, ei varmistettu henkilöllisyys tai luokkajäsenyys. Pelkkä URL-perusteinen katalogin henkilövihje merkitään tarkistettavaksi. Uusia henkilöllisyyksiä ei tässä erässä päätelty.
- Olemassa olevat 98 teostietuetta ja 97 kokotekstiä säilyvät. Uusissa oppilassivuissa on lisää kirjoitelmia ja taidetta, jotka ovat jo kokonaisina lähdelukusivuina mutta odottavat erottelua teostietueiksi.
- Poroilan kouluesittely (`DLC-0313`) ja Sähköikkuna-tekstit ovat nyt paikallisina lukusivuina. Tässä erässä ei lisätty niiden perusteella uusia elämäkertaväitteitä tai korkkitauluyhteyksiä; aiempi tutkimus on jo käyttänyt osaa näistä lähteistä. Uudet väitteet edellyttävät vertailua nykyiseen aikajanaan ja alkuperäiseen lähdekohtaan.

## Tarkisteet ja hakujen epävarmuudet

119 uudesta vastauksesta 98 täsmää CDX-hakemiston SHA-1-tarkisteeseen. 21 HTML-vastauksen tarkiste poikkeaa hakemiston tarkisteesta, vaikka palautuksen URL ilmoittaa pyydetyn ajan. Myös rivinvaihtojen LF/CRLF-vertailu kokeiltiin kolmelle esimerkille (`DLC-0035`, `DLC-0053`, `DLC-0523`); se ei selittänyt eroa. Syytä ei ole vielä ratkaistu. Nämä vastaukset säilytetään muuttamattomina, mutta `capture_digest_match=false` ja `exact_original_bytes=false`; lukusivuilla ja tiedostoluettelossa on varoitus. Niitä ei esitetä varmennettuina täsmälleen CDX:n kuvaamiksi alkuperäistallenteiksi.

Kunkin yrityksen tiedot ovat `assets/archive/recovery-attempts.json`-tiedostossa. Erän lopussa 179 eri tietuetta on yritetty hakea, joista 60 jäi ilman paikallista kopiota yhteysvirheiden takia. Yhteysvirhe ei osoita aineiston puuttumista arkistosta. Uudelleenyrityksiä tehdään pienissä erissä ja hakuloki säilyy.

## Seuraavat työt

Tämän erän tarkistukset: build, kaikkien sisäisten linkkien tarkistus sekä 180 lukusivun tekstien, henkilöpaluulinkkien ja 76 kuvan tavujen tarkistus läpäisivät paikallisen `/`-juuren ja Pagesin `/poroila-jaljet/`-alipolun. Uusi navigaatio ja kuvagalleria tarkistettiin 1440 ja 390 pikselin selaimessa. Historiallisten sisältöjen 54 ulkoasu-/toimintavertailua läpäisivät tarkistuksen vanhalla navigaatiorungolla; uuden valikon toimivuus ja ajantasaiset palautustilat tarkistetaan erikseen.

1. Jatka linkkiverkon läpikäyntiä, uusi yhteysvirheisiin päätyneet haut ja etsi vielä tuntemattomien kuvaviitteiden tallenteet. Laajenna hakua havaittuihin palvelin- ja sivustoversioihin lähdekohtaisesti.
2. Selvitä 21 CDX-poikkeamaa toisesta raakapalautuksesta, toisesta tallenteesta tai WARC-vastauksesta; älä poista poikkeavaa todistusaineistoa.
3. Erota uusista sivuista yksittäiset kirjoitelmat, runot ja kuvataidetyöt teoskatalogiin sekä tarkista tekijämerkinnät käsin. Oppilassivun ylläpitäjä ei automaattisesti ole jokaisen kuvan tekijä.
4. Tee lähteistetyt luokkakohtaiset tietueet ja jäsenyydet sivujen varsinaisista nimilistoista. Älä sekoita valikkoa, valokuvan kuvatekstiä ja oppilasluetteloa.
5. Vertaa uusia lähdekohtia koulun ja Poroilan aikajanoihin sekä korkkitauluun. Täydennä vain perusteltuja väitteitä, merkitse epävarmat ajoitukset ja pidä henkilösuhteet erillään yhteisestä koulukontekstista.
6. Selvitä ulkopuolisista lähteistä löytyvät täydennykset havaittujen otsikoiden, projektien ja päiväysten avulla. Kirjaa erikseen alkuperäinen koulusisältö ja myöhempi ulkopuolinen tieto.
