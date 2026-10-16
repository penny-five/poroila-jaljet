# Kuvankäsittelytyöt ja runosivut 16.10.2026

## Palautuserä

Paikallisesti palautettiin 40 aiemmin puuttunutta, säilyneiden koulusivujen linkittämää tiedostoa: neljä HTML-sivua ja 36 JPEG-kuvaa. Kaikki 40 vastausta täsmäävät tunnetun tallenteen CDX SHA-1 -tarkisteeseen. Alkuperäistavut, lähde- ja tallenneosoitteet, tallennusajat, hakupäivät, tavumäärät ja SHA-256 ovat originals-manifest.json-tiedostossa; pyyntökohtainen loki on recovery-attempts.json.

Alkuperäistiedostoja on nyt 386, paikallisia koulusivujen lukutekstejä 246 ja esityskuvia 129. Teoskatalogin 135 tekstiteosta ja kokotekstiä säilyvät ennallaan. Kuvaryhmät ovat uusi lähdepohjainen selausnäkymä, eivät 43 uutta tekstiteosta.

Palautuneet runosivut ovat DLC-0105 (5/6:n runohakemisto), DLC-0071 (hakemiston linkittämä vapaiden runojen sivu 96/97), DLC-0824 (Annan ja Sirkun runosivu) ja DLC-0315 (Olli Poroilan runoja). Runoihin viittaava tiedostonimi voidaan näyttää myös Runot ja kirjoitelmat -koonnissa, vaikka sama lukusivu kuuluu ensisijaisesti Oppilaiden sivuihin. Paikallinen sisältö ja tunniste säilyvät yhtenä.

## Kuvaryhmät

Uusi /koulu/kuva-ja-taidesivut/kuvamuunnokset/ kokoaa 43 kuvaryhmää neljältä lähdesivulta: DLC-0080, DLC-0081, DLC-0082 ja DLC-0083. Kaikkien näiden HTML-lähteiden alkuperäistavut on säilytetty ja tarkistettu. Lähteiden lukuvuositekstit ovat 97/98, 98/99 ja 99/00; kahdella jälkimmäisellä sivulla on eri luokka-aste.

Kuvaryhmät erotetaan alkuperäisen HTML:n HR-elementeillä. Lohkossa ovat ENSIN/SITTEN- tai yhdistelmämerkityt kuvat sekä tekijäteksti. Henkilöviite perustuu saman kokonaiseen nimiasuun samassa tekijätekstissä. Siitä ei päätellä kuvassa esiintymistä tai nykyistä henkilöllisyyttä. Nimimuotoja ei täydennetä tiedostonimien perusteella.

Tärkeä vastaesimerkki: DLC-0083:n kuvamuunnos-elsa-ensin.jpg ja kuvamuunnos-elsa-sitten.jpg kuuluvat samassa lohkossa olevan tekstin mukaan Paula Savolaiselle. Elsa Hagelbergin nimi esiintyy eri, pasa-nimisessä kuvalohkossa. DLC-0081:n jose-arttu-tiedostonimien tekijämerkintä taas on Jose Riikonen / Jarno Virtamo. Näiden lähderivien merkitys säilytetään; tiedostonimeä ei koroteta tekijätiedoksi.

43 lähdekohtaisessa ryhmässä on yhteensä 84 kuvaviitettä: 38 voidaan näyttää paikallisesti ja 46 on merkitty puuttuviksi. Sama tiedosto voi esiintyä eri lukuvuosien sivuilla; tällaiset lähdehavainnot säilyvät erillisinä. Puuttuvaa kuvaa ei korvata toisen palvelimen tai samannimisen tiedoston kuvalla.

Näkymään pääsee sekä koulukuvista että Kuva- ja taidesivut -koonnista. Henkilösivuilla ovat paluulinkit tekstin tukemiin kuvaryhmiin. Raakatiedostot ja lähdesivujen lukutekstit ovat edelleen saatavilla. Digitaalisten kuvien rinnakkaisuus perustuu lähteen merkintöihin, ei myöhemmin keksittyyn ennen/jälkeen-tapahtuma-aikaan.

## Poroilan kirjoitukset

DLC-0315:n otsikko ja tekijärivi nimeävät Olli Poroilan. Sivulla on viisi runo-otsikkoa: Kuoleman kuva, Uruk sisälläni, Kadonnut kaupunkini, Kahlittu ja Kafkan näkemät. Koko näkyvä teksti on paikallisella lukusivulla ja raaka-HTML on säilytetty. Kirjoitukset ja lähteet -sivulle lisättiin lähdelinkki ja lähdeluetteloon S73.

Tallennepäivä on 22.10.2000; runojen päiväystä ei lähteessä ole. Runojen puhujasta tai kuvastosta ei muodostettu elämäkertaväitteitä, aikajanatapahtumia tai korkkitaulun henkilösuhteita. Verkkoartikkelin vanhentunut väite oppilassivujen tallenteiden puuttumisesta korjattiin viittaamaan jo palautettuihin koulusivuihin ja S72:n koulun verkkotyötä kuvaavaan tekstiin.

## Puuttuvat ja jatko

Kolmen katalogista puuttuvan kuvaviitteen julkista CDX-indeksiä kokeiltiin: oppilas-jussi-kanervo-animaatio.gif, oppilas-kalle-saukkolin-pannunalusta.jpg ja 56-luokkahuone-etuosa-p.jpg (kaikki DLC:n ~hyk-hakemistossa). Pyynnöt epäonnistuivat yhteysvirheeseen WinError 10061. Tämä ei osoita tallenteiden puuttumista. Metadataa ei keksitty eikä osoitteille luotu palautettua tiedostoa tarkoittavaa tilaa. Myöhempi täsmähaku on yhä tarpeen.

Palautustyökaluun lisättiin --ids-valinta, jolla lähteissä jo linkitetyt katalogitietueet voidaan valita rajattuun erään. Se säilyttää linkkiperusteisen rajauksen ja annetun tiedostorajan. Tämä mahdollisti runo- ja kuvataide-erän palauttamisen yleisen oppilassivujonon rinnalla.

Tarkistukset kattavat 43 lohkon lähdetarkisteet, kuvaliitännät ja nimiviitteiden paluulinkit. Erillinen tarkistus estää elsa-tiedostonimen käyttämisen vääränä tekijätodisteena. Selaimessa kuvat ladataan paikallisista tiedostoista sekä puhelin- että työpöytäleveydellä ja Poroilan kirjoituksista kuljetaan paikalliseen runolähteeseen. Lähdeluettelon nykyinen rivimäärä tarkistetaan datasta; vanhojen näkymien ulkoasuvertailussa uusi lähderivi rajataan pois vain testikehyksessä. Jäädytettyä alkuperäisfixturea ei muutettu.
