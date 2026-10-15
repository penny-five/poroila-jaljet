# Koulun vanha oma osoite, oikeuslinjojen erottelu ja oppilasmuistelu

15.10.2026.

## Keskeinen uusi löytö: Hyrsylän koulun oma hakemisto vuonna 2007

Kunnan koko sivustoon kohdistunut URL-avainten haku löysi aiempaa `/koulut/`-hakemistoa vanhemman osoitteen:

`http://www.nummi-pusula.fi/sivistys/hyrsylankoulu/`

Löytö ei perustu arvattuun osoitteeseen. Se tuli seuraavasta Wayback CDX -vastauksesta:
https://web.archive.org/cdx/search/cdx?url=www.nummi-pusula.fi%2F&matchType=prefix&output=json&filter=urlkey%3A.%2Ahyrs.%2A&collapse=urlkey&limit=80

Indeksirivi: aikaleima `20070711094945`, alkuperäinen URL portilla `:80`, MIME `text/html`, HTTP 200, arkiston digest `ZZSGGYQKXTNP33CGOBOSVXS47AONNUOU`.

Luettu raaka HTML:
https://web.archive.org/web/20070711094945id_/http://www.nummi-pusula.fi:80/sivistys/hyrsylankoulu/

Tarkistettu HTTP 200 ja sama lopullinen arkisto-URL. Vastaus on 339 tavua. Windows-1252-dekoodaus palauttaa otsikon `HYRSYLÄN KOULU`. HTML ei ole varsinainen sisältösivu vaan `frameset rows="27%,*"`, jossa on kaksi kehystä:

- `http://www.nummi-pusula.fi/sivistys/hyrsylankoulu/ylaosa.htm`
- `http://www.nummi-pusula.fi/sivistys/hyrsylankoulu/alaosa.htm`

Kummankin kehystiedoston raaka-arkistoavaus aikaleimalla `20070711094945` palautti 404:n. Hakemiston kaikkien vastauskoodien CDX-haku palautti vain yhden, edellä mainitun pääsivun:
https://web.archive.org/cdx/search/cdx?url=http%3A%2F%2Fwww.nummi-pusula.fi%2Fsivistys%2Fhyrsylankoulu%2F&matchType=prefix&output=json&collapse=urlkey&limit=100

Löytö varmentaa koulun oman vanhan hakemiston, otsikon ja kehysrakenteen. Se ei palauta oppilastöitä eikä osoita Poroilan tekijyyttä. Arkistotallennuspäivä ei ole sivuston perustamispäivä.

Julkaistu `assets/archive/hyrsylan-frameset-20070711.txt` on tämän HTML:n tekstikopio UTF-8-muodossa. Alkuperäiseen sisältöön ei lisätty mitään. Tarkistus perustuu arkiston alkuperäisiin tavuihin; tiedoston paikallinen uudelleenkoodaus muuttaa tavumäärää.

Alkuperäisten 339 tavun SHA-256: `904e4c2a3bd7560b3d9bf0a6712c3d15e778d214828610b1f2a89825e46ebb49`.

## Muut koulusivuhaut

`/koulut/`-hakemiston kaikkien vastauskoodien CDX-haku palautti myös vanhat 404-tallenteet. Niistä Hyrsylän `sivu=121&alasivu=177` on jo tunnettu; se ei ole sisältölöytö. Koko kunnan Hyrsylä-URL-haku erotti myös matkailukohteen kuvat koulun hakemistosta.

Arquivo.pt:n aikarajattu sanahaku vuosilta 1996–2015 sekä uuden vanhan osoitteen versionHistory-haku palauttivat nolla tulosta. Varhaisen Common Crawl -kokoelman `/koulut/*`-haku palautti 504:n; vuoden 2013 kokoelman uuden `/sivistys/hyrsylankoulu/*`-haun vastaus oli 404. Näitä ei tulkittu todisteiksi koko arkiston kattavuudesta.

## Poroilan oma oikeuskertomus

Tuntemuksiani-pääsivun aloitus erotettiin päivätyistä merkinnöistä. Aloituksessa Poroila luettelee itselleen myönteisiksi tulkitsemiaan hallinto-oikeuksien ratkaisuja, syyttäjän esteellisyyttä ja hovioikeuden vähemmistökantaa. Näiden päätösasiakirjoja ei ole avattu. Ne eivät muodosta automaattisesti samaa asiaa kuin vuosien 2005–2007 oppilaisiin kohdistuvia opetusmenetelmiä koskeva rikosprosessi.

Oikeussivun otsikko ”Yksi prosessi” korjattiin. Sivu erottaa nyt rikosasian, kirjoittajan kuvaaman virkasuhdeasian ja verkkosivujen sulkemisen. Analyysi käsittelee myös kirjoittajan pyrkimystä siirtää asetelma puolustautumisesta omien vaatimusten käsittelyyn (9.1. ja 1.5.2013).

Henkilöviitteitä tarkennettiin:

- R. Erma mainitaan kirjoitussivun aloituksessa käräjätuomarina. Finlex KKO:2006:98 nimeää Ritva Erman Lohjan käräjäoikeuden tuomariksi eri asiassa. Tämä tukee mahdollista tunnistusta, ei vahvista osallistumista Poroilan asiaan. https://finlex.fi/fi/oikeuskaytanto/korkein-oikeus/ennakkopaatokset/2006/98 (S47).
- Rauli Pajuharjun julkinen rikoskomisarion tehtävä vahvistuu hänen omasta Yle-haastattelustaan 21.1.2010. Haastattelu koskee eri asiaa eikä vahvista Poroilan moitteita. https://yle.fi/a/3-5495048 (S48).
- Pauli Korhosen rooli esitetään Poroilan tekstissä mainittuna kunnallisena toimijana. Kunnallista tehtävää tai prosessiasemaa ei väitetä itsenäisesti vahvistetuksi.

Poroilan muista ihmisistä käyttämät halventavat nimitykset ja rikosväitteet jätettiin toistamatta.

## Uusi aikalaislinkki

https://f1-forum.fi/threads/nummi-pusulalla-menee-hyvin.5161/post-399052

Nykyinen alkuperäinen HTML avattiin HTTP 200. Viestin 399052 `time datetime` on `2005-09-26T18:01:51+0300`. HTML sisältää linkin `http://www.saunalahti.fi/poroila/pauli-parka.wav`. Waybackin saatavuuskysely palautti HTTP 200 ja tyhjän `archived_snapshots`-kentän. Ääntä ei ole palautettu tai kuunneltu. Linkki on uusi dokumentoitu tiedostonimi ja osoitteen aikalaisviite, ei vahvistus keskustelijoiden henkilöväitteille (S49).

Hellströmin blogin kaksi alkuperäistä Länsi-Uusimaa-linkkiä tarkistettiin saatavuusrajapinnasta: vuoden 2005 polut `27-09/lehti/1461218.shtml` ja `27-10/lehti/1486832.shtml`. Molemmat palauttivat tyhjät saatavuustulokset; alkuperäisiä lehtijuttuja ei avattu.

## Entiseksi oppilaaksi esittäytyvän kommentoijan muistelu

https://marttifi.wordpress.com/2006/04/11/elavalta-haudattu/#comment-116

Alkuperäinen blogi-HTML avattiin uudelleen. Kommentit 116 ja 117 on julkaistu 8.3.2011. Kirjoittaja kertoo yhden vuoden koulunkäynnistä ja omasta myöhemmästä suhtautumisestaan auktoriteetteihin. Niitä käsitellään omakohtaiseksi esitettynä muisteluna: henkilöllisyys, koulunkäyntivuosi ja yksittäisten tapahtumien oikeellisuus ovat varmistamatta (S50).

Kommentoijan nimeä, loukkaavia luonnehdintoja tai mahdollista yhteyttä koulun oppilasluetteloihin ei julkaistu. Lyhyt lähteistetty kuvaus lisättiin Myöhemmät vaiheet -sivulle.
