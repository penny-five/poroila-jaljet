# Navigaatio, kieliasu ja uusi koulusivuston arkistohaku

15.10.2026.

## Julkaisun toimitus

Poistettu kolme vanhaa `research-path`-valikkoa Poroila-, Sivujäljitys- ja Tallenteet ja kuvat -sivuilta. Ne toistivat nykyistä osion alasivuvalikkoa. Niihin liittyvät tyylit poistettiin; kuvagallerian puhelintyylit säilytettiin.

Sivuston HTML-leipätekstit luettiin läpi. Korjauksia ovat muun muassa Johtolankakartta-yhdyssana, AVAA-painikkeen kirjoitusvirhe, yksikölliset linkkimäärät, footerin Lähteet edellä -teksti, sijamuoto opetusmateriaalien käytöstä sekä puuttuva pilkku. Kankeita ilmaisuja ja työvaiheiden selostuksia sujuvoitettiin. Oikeusartikkelin lähdekriittinen raja säilytettiin lyhyemmässä tekstissä.

Sisällöllisiä täsmennyksiä: Tuntemuksiani-pääsivu sisältää vuoden 2013 tekstit ja linkkejä aiempien vuosien koosteisiin. Kouluosio ei enää johdata sen sisältöön kuulumattomaan fiktioon. Hypoteesisivun vuoden 1975 henkilöyhteyden kuvauksessa huomioidaan nyt myös 19.2.2013 Aholanvaara-muistelma. Vuoden 2013 koulusivua koskeva aikajanan otsikko kuvaa tallennetun sivun ajankohtaa, ei myöhempää palautustyötä.

## Wayback: kouluhakemiston CDX-vastaus onnistui

Kysely:
https://web.archive.org/cdx/search/cdx?url=www.nummi-pusula.fi%2Fkoulut%2F&matchType=prefix&output=json&filter=statuscode%3A200&collapse=urlkey&limit=100

HTTP 200, 16 tulosriviä. Kysely rajaa palvelimen HTTP 200 -vastauksiin ja yhdistää saman URL-avaimen tallenteita. Tulos ei ole luettelo koko sivuston kaikista tallennusyrityksistä eikä jokaisesta ajankohdasta. Yhtään Hyrsylän `sivu=121`-sisältösivua ei ollut tässä vastauksessa.

Kuusi tulosjoukosta poimittua HTML-tallennetta avattiin ja luettiin:

| Tallennusaika | Alkuperäinen polku | Luettu sisältö |
|---|---|---|
| 28.4.2012 20.26.52 UTC | `/koulut/default.asp?sivu=126&alasivu=126&kieli=246` | Nummi-Pusulan lukio; ei Hyrsylä |
| 11.5.2013 09.05.20 UTC | `/koulut/default.asp?sivu=153&alasivu=153&kieli=246` | Nummi-Pusulan yläkoulu; ei Hyrsylä |
| 17.2.2012 09.08.52 UTC | `/koulut/Default.htm` | HTML:n meta-refresh ohjaa `default.asp`-sivulle |
| 29.11.2011 03.46.07 UTC | `/koulut/tapahtumat.asp?tyyppi=vanhat&kieli=246` | Käytännössä otsikko ja navigaatio; ei tapahtumaluetteloa |
| 29.11.2011 03.46.12 UTC | `/koulut/tulosta.asp?sivu=1&alasivu=&tiedote=510&tapahtuma=&kieli=246` | Kunnan yhteisen koulusivun tulostusversio, Hyrsylä alakoulujen joukossa |
| 1.9.2012 07.13.55 UTC | `/koulut/tulosta.asp?sivu=1&alasivu=&tiedote=593&tapahtuma=&kieli=246` | Vastaava yhteinen koulusivu, asiakirjalinkit päivitetty vuodelle 2012 |

Tulostusversioiden alkuperäiset HTML:t luettiin `id_`-muodossa. Julkiset replay-URL:t:

- https://web.archive.org/web/20111129034612/http://www.nummi-pusula.fi:80/koulut/tulosta.asp?sivu=1&alasivu=&tiedote=510&tapahtuma=&kieli=246
- https://web.archive.org/web/20120901071355/http://www.nummi-pusula.fi:80/koulut/tulosta.asp?sivu=1&alasivu=&tiedote=593&tapahtuma=&kieli=246

Molemmat sisälsivät 4 529 merkkiä pelkkää tekstiä poiminnan välilyöntien normalisoinnin jälkeen. Sisältö ei silti ole täysin sama: oppaan ja ilmoittautumislomakkeen linkkien vuosiluvut vaihtuvat 2011:stä 2012:een. URL:n tiedotenumero ei tässä vastaa erillisen tiedotteen tekstiä. Siksi tallenteita ei nimetty uutisiksi 510 ja 593. Tarpeettomia henkilökohtaisia yhteystietoja ei toistettu sivustolla. Tallenteet lisättiin lähteiksi S44 ja S45.

## Poroilan hakemistojen uusintatarkistus

Seuraavat rajatut CDX-kyselyt onnistuivat HTTP 200 -vastauksella:

- https://web.archive.org/cdx/search/cdx?url=www.saunalahti.fi%2Fporoila%2F&matchType=prefix&output=json&filter=statuscode%3A200&collapse=urlkey&limit=200
- https://web.archive.org/cdx/search/cdx?url=kotisivu.dnainternet.net%2Fporoila%2F&matchType=prefix&output=json&filter=statuscode%3A200&collapse=urlkey&limit=200

Saunalahti-vastaus sisälsi tutun 22.6.2001 etusivun ja yhdeksän vuoden 2005 kuvatiedostoa. DNA-vastaus sisälsi tutut 29.6.2013 etusivun ja 1.7.2013 Tuntemuksiani-sivun. Uutta HTML-sisältöä ei palautunut. Saunalahden `ilta-juoru-p.gif` avattiin myös selaimessa: pienikokoinen kuvajälki näkyy, mutta kuvan koko tekstisisältöä ei tulkittu eikä julkaistu.

## Muut arkistot

- Common Crawl `CC-MAIN-2014-52`, `www.nummi-pusula.fi/koulut/*`: HTTP 504.
- Common Crawl `CC-MAIN-2017-26`, sama osoiterajaus: HTTP 404. Vastauksesta ei tehty päätelmää koko arkiston sisällöstä.
- Arquivo.pt:n täsmällinen Hyrsylän kunnallisen pääsivun versionHistory-haku palautti HTTP 200 ja nolla tulosta: https://arquivo.pt/textsearch?versionHistory=http%3A%2F%2Fwww.nummi-pusula.fi%2Fkoulut%2Fdefault.asp%3Fsivu%3D121%26kieli%3D246&maxItems=10
- Arquivo.pt:n sanahaku palautti pääosin Aira Samulinin Hyrsylän Mutkaa ja koulun myöhempää rakennushanketta. Nämä erotettiin vanhasta koulusivustosta.
- Alkuperäisen HTML:n MikroBitti-osoitteen `http://koti.mbnet.fi/poroila/` Wayback-saatavuushaku vastasi HTTP 200 ja tyhjällä `archived_snapshots`-kentällä.

Palvelinvirhe, tyhjä saatavuusvastaus ja hakutuloksen puuttuminen eivät osoita, ettei sivua olisi koskaan tallennettu.
