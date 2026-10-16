# Heponiemen leirikoulu ja vanhojen MIME-merkintöjen käsittely 16.10.2026

## Palautuserä

Edellisen julkaisun jälkeen palautettiin 53 tiedostoa: 15 HTML-sivua, 30 JPEG-kuvaa ja kahdeksan GIF-kuvaa. Näistä 49 täsmää tallenteen CDX SHA-1 -tarkisteeseen. Neljä ei täsmää: DLC-0103, DLC-0982, DLC-0675 ja DLC-0709. Ne säilyvät merkittyinä varmistamattomina vastauksina; niistä ei johdettu tässä uusia varmennettuja historiallisia väitteitä.

Paikallisia alkuperäistiedostoja on nyt 439. Koulun lukusivuja on 261 ja esityskuvia 167. Katalogin 135 teosta ja 135 kokotekstiä säilyvät. Kaikkien tiedostojen pyydetty ja lopullinen URL, hakuajankohta, tavumäärä ja SHA-256 ovat manifestissa ja yrityslokissa. Vanhoja alkuperäisiä ei korvattu.

Kuvamuunnosten viimeiset kolme tunnetussa katalogissa ollutta puuttuvaa kuvaa saatiin talteen, DLC-0238–DLC-0240. Lähdekohtaisissa 43 kuvaryhmässä on nyt 41 paikallista kuvaviitettä ja 43 puuttuvaa. Saman tiedoston viittaaminen eri lähdesivuilla ei tee siitä eri alkuperäistiedostoa.

## MIME-tiedon puutteet

Keruuta tarkastettaessa löytyi linkitettyjä kuvia vanhalla MIME-merkinnällä im sekä HTML-sivuja merkinnällä text/plain. Ne jäivät aiemmin sallitun tyyppilistan ulkopuolelle, vaikka tallenne ja CDX-tarkiste olivat tiedossa.

Palautustyökalu sallii nyt nämä tyypit ja tunnistaa kuvan JPEG-, GIF- tai PNG-alkutavuista. HTML:ksi epäilty text/plain hyväksytään HTML:ksi vain HTML- tai BODY-merkinnän ja tavallisten arkiston virhesivu- ja replay-tarkistusten jälkeen. Manifestin mime_type kuvaa tunnistettua esitysmuotoa, archive_mime_type säilyttää eriävän indeksimerkinnän ja mime_detection kertoo menetelmän. Katalogin alkuperäinen mimetype ei muutu. Riippumaton CDX-tarkiste tarkistetaan edelleen koko vastauksen tavuista.

Tämän aukon kautta palautui muun muassa Anna Rasinkankaan sivun kuvia ja animaatio, Artturi Pekkolan, Jarno Virtamon ja Joonas Lehtosen kirjoitelmahakemistot sekä koulun vanha leirikoulusivu. Kuvat näytetään paikallisista tiedostoista ja HTML-sivut turvallisina lukuteksteinä.

## Heponiemi keväällä 1986

DLC-0052 otsikoi sisällön viidennen luokan leirikouluksi Karjalohjan Heponiemessä keväällä 1986. Teksti sanoo, ettei lukuvuonna 85/86 Hyrsylässä ollut vielä kuudetta luokkaa ja että viidennellä oli yhdeksän tyttöä eikä yhtään poikaa. Sivu mainitsee myös Karjalohjan kyläkoulun Rolf Oinosen opastuksen. Tämä on koulun oma myöhemmin verkossa julkaistu kertomus, ei tarkistettu luokkapäiväkirja tai osallistujaluettelo.

Sivun viidestä sisältökuvaviitteestä ryhmäkuva DLC-0051 palautui. HTML ja kuva täsmäävät kumpikin CDX-tarkisteeseen. Kuvassa esiintyviä henkilöitä ei tunnistettu, nimetty tai liitetty henkilörekisteriin. Muiden kuvien puuttuminen näkyy paikallisella lukusivulla.

Koulun historiaan lisättiin leirikoulua käsittelevä kappale, paikallinen ryhmäkuva ja linkki koko lähdesivuun. Lähdeluetteloon lisättiin S74, joka avautuu paikalliseen lukusivuun. Aikajanan tapahtumavuosi 1986 perustuu tekstin nimenomaiseen kevätmerkintään; tallennepäivä 28.10.2000 säilyy eri tietona. Aikajanalla on nyt myös 1980-luvun suodatin. Havaintoa ei tulkittu näytöksi yksittäisen opettajan osallistumisesta tai oppilaiden henkilöllisyydestä.

## Uusien kuvapaikantimien selvittäminen

CDX:n kontrollihaku tunnettuun kuvaan kuvamuunnos-elsa-ensin.jpg aikakatkaistiin. Archive.orgin saatavuusrajapinta vastasi tuntemattoman kuvamuunnos-astra-ensin.jpg-kuvan hakuun HTTP 200 mutta tyhjällä archived_snapshots-objektilla. Kumpikaan tulos ei todista kuvan puuttumista kaikista tallenteista. Tarkat pyynnöt, ajat ja vastaukset ovat media-metadata-attempts.json-tiedostossa. Uutta palautettua kuvaa tai olematonta CDX-tietuetta ei luotu näiden perusteella.

Edellisen raportin jatkoviitteenä mainittu Suomenmaan virallisen tilaston julkaisu on jo nykyisessä lähdeluettelossa S23. Sitä ei siksi lisätty uutena lähteenä eikä pidetty uutena riippumattomana vahvistuksena. Samannimiset Karjalan koulut pysyvät tämän Nummen/Lohjan koulun aineistosta erillään.

## Tarkistukset ja jatko

Tarkistus vertaa kaikkien uudelleen tunnistettujen MIME-tyyppien sisältöä todellisiin alkutavuihin ja varmistaa myös leirikoulun päivämäärätekstin, ryhmäkuvan liitännän sekä historian paikalliset linkit. Selainkoe käyttää 1980-luvun suodatinta ja seuraa vuoden 1986 lähdeviitettä paikalliseen tekstiin. Kuvagallerian paikalliset kuvat ja vanhojen näkymien asettelu tarkistetaan molemmilla näyttöleveyksillä.

Seuraavaksi keruu jatkuu sivukartan ja luokkahakemistojen uusista linkeistä, muista im-merkinnällä indeksoiduista kuvasisällöistä sekä yhä ilman katalogitunnistetta olevien kuvien tallenteista. Tarkistepoikkeamien vaihtoehtoiset versiot ja lähteistä eroteltavat uudet teokset odottavat edelleen työtä.
