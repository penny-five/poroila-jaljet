# POROILA / JÄLJET

Suomenkielinen, lähdeviitteisiin perustuva tutkimuksellinen verkkosivusto Olli Poroilan julkisista dokumenttijäljistä. Tumma arkistoulkoasu, siirreltävä 14 kortin korkkitaulu (16 dokumentoitua tai avoimeksi merkittyä yhteyttä), suodatettava aikajana, tutkivat artikkelit ja 16 verkkolähdettä. Fiktiiviset kenttämuistiinpanot on erotettu todennettavista väitteistä.

## Sisältö

- `index.html` – tutkimussivun rakenne ja dokumentaarinen sisältö.
- `style.css` – responsiivinen, mysteerihenkinen ulkoasu.
- `app.js` – korkkitaulu, viivat, korttien siirtely, suodattimet, haku ja artikkeli-ikkunat.
- `research-data.js` – lähteet, aikajanan merkinnät sekä kolme laajempaa tutkimusartikkelia.
- `.nojekyll` – staattisen sivuston GitHub Pages -asetus.

## Esikatselu paikallisesti

Käynnistä tämän hakemiston sisällä `python3 -m http.server 8000` ja avaa `http://localhost:8000`. Pelkkä `index.html`-tiedoston kaksoisklikkaus ei välttämättä toimi, koska sivusto tuo tutkimusaineiston ES-moduulina.

## Julkaiseminen GitHub Pagesiin

1. Avaa repositorion **Settings → Pages**.
2. Valitse **Build and deployment → Deploy from a branch**, sitten **main** ja **/(root)**. Tallenna.
3. Jos GitHub Pages ei ole saatavilla: GitHub Free -tilillä Pages edellyttää tavallisesti *julkista* repositoriota. GitHubin maksullisissa suunnitelmissa yksityisen repositorion Pages-julkaisu voi olla tuettu. Huomaa, että Pages-sivusto on lähtökohtaisesti julkinen, vaikka sen lähdekoodi olisi yksityisessä repossa.
4. Tämän repositorion odotettu osoite Pages-julkaisun jälkeen on `https://penny-five.github.io/poroila-jaljet/`. Se ei ole vahvistettu toimivaksi ennen julkaisun aktivoitumista.
5. Jos repo halutaan pitää yksityisenä ilman maksullista GitHub Pages -ominaisuutta, vaihtoehtona on liittää yksityinen GitHub-repo esimerkiksi Netlifyyn tai Verceliin ja julkaista sieltä.

## Lähdekritiikki ja fiktio

Tämä on keskeneräinen julkinen lähdeselvitys, ei kokonaiselämäkerta eikä oikeudellinen lainvoimaisuusselvitys. Eri nimiosumat, bibliografiset tietueet, aikalaisblogit ja uutisreferaatit on eroteltu toisistaan. Vuoden 2007 jatkoratkaisusta käytetään vain blogin referoimaa aikalaistietoa, ei alkuperäistä tuomioasiakirjaa. Presidentin kirjeaineiston samannimisen kirjoittajan henkilöllisyyttä ei pidetä varmana. Fiktiiviset osuudet kuvaavat kuvitteellisen arkistotutkijan työskentelyä, eivät todellisten henkilöiden salaisia tekoja, puheita tai motiiveja.

Päivitetty 15.10.2026.
