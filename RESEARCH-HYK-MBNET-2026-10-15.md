# HYK ja MBnet: varmistettu Hyrsylä–Poroila-sisäänkäynti

Tarkistettu 15.10.2026. Lähtökohtana käyttäjän epävarma muistikuva pre-2007-koulusivun HYK-osoitteesta MBnetissä. Osoite testattiin ensin hypoteesina; alla mainittu alkuperäinen HTML varmensi yhteyden.

## Luetut alkuperäistallenteet

1. https://web.archive.org/web/20010428205240id_/http://koti.mbnet.fi/~hyk/
2. https://web.archive.org/web/20020211130751id_/http://koti.mbnet.fi:80/hyk/

Ensimmäinen palautui HTTP 200:na, 664 tavua, Windows-1252. Sen lopullinen arkistoaikaleima on **28.4.2001 klo 20.52.40 UTC**. Se löytyi seuraamalla vuoden 1999 arkistoidun uudelleenohjauksen nykyistä arkistoketjua. Vuoden 1999 URL:n avaaminen päätyi vuoden 2001 sisältöön: tätä ei kirjata vuoden 1999 HTML-tallenteeksi.

Sivun tekninen sisältö:

```html
<BODY BACKGROUND="tausta_puna_musta.jpg" LINK="#12A501" ALINK="#FF0000" VLINK="#005500">
<meta http-equiv="Refresh" content="5; URL=http://www.mbnet.fi/~hyk/linkkisivu.htm">
```

Alkuperäisen `keywords`-kentän alussa ovat `poroila, olli, hyrsylä, hyrsylän, hyrsyla, hyrsylan`; mukana ovat myös kouluun ja opetukseen liittyvät sanat. Näkyvä teksti lupaa siirtymistä kahden sivuston linkkisivulle ja kehuu linkkikuvia. Sivulla ei ole varsinaisia koulun esittelytekstejä, oppilastöitä tai oppilasluetteloa.

Tämä varmentaa MBnetin HYK-hakemiston yhteyden Hyrsylään ja Olli Poroilaan. Pelkkä avainsanalista ja kahden sivuston maininta eivät vielä todista, mitkä kaksi kohdesivustoa linkkisivulla olivat tai kuka kirjoitti ne. HYK:n lyhennettä ei avata säilyneessä HTML:ssä.

Vuoden 2001 vastauksen arkistoidut alkuperäisotsakkeet:

- `Last-Modified: Tue, 16 Mar 1999 22:30:10 GMT`
- `Content-Length: 664`
- `Server: Apache/1.3.9 (Unix)`
- arkistotiedosto: `DE_crawl3.20010428133122-c/DE_crawl3.20010428205048.arc.gz`

Muokkausaika on palvelimen ilmoittama metatieto, ei riippumaton todistus vuoden 1999 sisällöstä tai sivuston perustamisesta. Alkuperäisten 664 tavun SHA-256: `0d00d7f89859c1d0cc6ded0b37325e95a652b4a8463e62644016c077b0d3df8c`.

Julkaistu `assets/archive/hyk-mbnet-20010428.txt` on Windows-1252:sta UTF-8:aan muunnettu HTML-tekstikopio. Sen tavut eivät vastaa alkuperäistavujen tarkistussummaa. Kuva `assets/archive/hyk-mbnet-20010428.jpg` otettiin aidosta Wayback-näkymästä ennen automaattista siirtymistä. Taustakuva ei latautunut; puuttuvaa ulkoasua ei rekonstruoitu. Kuvan tarkistussumma on manifestissa.

## CDX-hakujen tulokset

https://web.archive.org/cdx/search/cdx?url=koti.mbnet.fi%2Fhyk%2F&output=json&limit=500

Palautti seuraavat tarkat tallennusaikaleimat:

- `20020211130751`, HTTP 200
- `20030319033735`, HTTP 200
- `20031208133524`, HTTP 200
- `20040816153554`, HTTP 200
- `20221011075942`, HTTP 302

Ensimmäisillä neljällä on sama CDX-digest `BGERTKLKJDSBMYEGPQJ2KQKFIFHMPZZ3`. Tämä osoittaa saman arkistoidun sisältötiivisteen näillä kerroilla; uusia alisivuja ei näistä synny. Vuoden 2002 HTML luettiin myös suoraan.

https://web.archive.org/cdx/search/cdx?url=www.mbnet.fi%2F~hyk%2F&output=json&limit=500&matchType=prefix&collapse=urlkey

Palautti vuoden 1999 HTTP 301 -tietueen `http://mbnet.fi:80/%7Ehyk`, aikaleima `19990823030432`. Sen arkistoavaus päätyi edellä kuvattuun vuoden 2001 tallenteeseen. Hakutuloksen 301 ei ole sisältösivu.

Tilde-muotoisen koti.mbnet.fi-osoitteen prefix-haku palautti vuoden 2001 HTTP 301 -juuritietueen ja rivinvaihdon sisältävän virheosoitteen HTTP 404:n. Selainarkiston kalenterissa näkyi yhdeksän saman juuriosoitteen tallennetta. Täydentävä kaikkien versioiden haku aikakatkaistiin. Prefix-vastausta ei siksi tulkita tyhjentäväksi luetteloksi HYK-aineistosta.

## Avoimeksi jäävä linkkisivu

Alkuperäisen HTML:n täsmällinen ohjauskohde on:

`http://www.mbnet.fi/~hyk/linkkisivu.htm`

Raaka arkistoavaus 11.2.2002 aikaleimalla palautti 404:n. Waybackin saatavuusrajapinta palautti tyhjän `archived_snapshots`-kentän sekä tälle osoitteelle että koti.mbnet.fi:n tilde-vastineelle. Erilliset täsmälliset CDX-haut aikakatkaistiin tai palauttivat 503:n. Linkkisivun sisältöä ei saatu luettua. Myöskään taustakuvaa ei tässä tutkimuskierroksessa palautettu.

Arquivo.pt:n versionHistory-haku `http://koti.mbnet.fi/hyk/` palautti HTTP 200 ja nolla tulosta. Common Crawlin `CC-MAIN-2013-20`-kokoelman `*.mbnet.fi/*hyk*`-haku palautti HTTP 502. Nämä eivät osoita aineiston puuttumista kaikista kokoelmista.

Poroilan vuoden 2013 DNA-HTML:n jo tunnetut MBnet-linkit johtavat hakemistoon `koti.mbnet.fi/poroila/`. Niissä ei löytynyt HYK-linkkiä. Poroila-hakemistoa ei yhdistetä HYK-hakemiston alihakemistoksi.

Seuraava ratkaiseva lähde olisi aidosti palautuva `linkkisivu.htm` tai aikalaislähteen suora linkki sen koulusivustoon. Kunnan vuonna 2007 tallennettu `/sivistys/hyrsylankoulu/` on erillinen, myöhempi osoitelöytö; siirtymistä MBnetistä siihen ei ole dokumentoitu.
