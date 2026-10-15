# Rakennekatselmus ja arkistokuvien tallennus 15.10.2026

## Rakenteen korjaukset

Päävalikossa on seitsemän tutkimuksen pääkohtaa. Viisi täydentävää osaa on Lisää-valikossa; kaikki aiemmat jaettavat osoitteet säilyvät. Sivujäljitys tarkoittaa osoitteiden ja puuttuvien kohteiden tutkimista. Tallenteet ja kuvat sisältää avatun aineiston. Poroila sisältää taustoittavat artikkelit. Näiden sivujen alussa on yhteinen lukupolku lähdeluetteloon asti.

Poroila-sivulta korjattiin vanhentunut väite, ettei kotisivua olisi nähty. Samalla oikeusprosessia kuvaava otsikko muutettiin vastaamaan lähdetyyppien eroa: uutinen ja blogireferaatti eivät ole kaksi alkuperäistä tuomiota. Avoimet kysymykset erotettiin otsikkotasollakin kirjallisesta fiktiosta.

## Aidot kuvakaappaukset

Kuvat otettiin selaimella Waybackin avaamista tallenteista. Ne eivät ole tekoälykuvia tai jäljitelmiä. Arkiston toistossa puuttuvia kuvia tai tyylejä ei paikattu. Arkistopalkki säilytettiin, jotta tallennusaika ja osoite näkyvät kuvassa. Kuvakaappauspäivä on eri asia kuin alkuperäisen tallenteen päivä.

Kuvien alkuperäisosoitteet, arkisto-URL:t, päivät ja rajaukset: [manifest.json](assets/archive/manifest.json).

- [Saunalahti 22.6.2001](assets/archive/saunalahti-20010622.jpg): selainnäkymä. Keskellä oleva henkilökuva ei latautunut.
- [Kouluportaali 3.12.2008](assets/archive/kouluportaali-20081203.jpg): selainnäkymä kunnan yhteisestä koulusivusta.
- [Hyrsylän sivupuu 29.11.2011](assets/archive/hyrsylan-sivupuu-20111129.jpg): rajattu Hyrsylän haaraan, arkistopalkki mukana.
- [DNA-etusivu 29.6.2013](assets/archive/dna-20130629-otsake.jpg): rajattu otsakkeeseen ja sisäänkäyntiin. Sivun muita henkilöitä koskevia väitteitä ei toisteta kuvagalleriassa.

## Uusi lähdekriittinen rajaus

Vuoden 2011 sivukartan `Oppilaiden kirjoituksia` -linkki on `default.asp?sivu=123&alasivu=166&kieli=246`. Alkuperäisessä HTML:ssä se sijaitsee Koisjärven koulun haarassa. Hyrsylä käyttää parametria `sivu=121`. Siksi kyseistä oppilaskirjoitusten osiota ei voi merkitä Hyrsylän löydöksi.

Lähde: https://web.archive.org/web/20111129034532/http://www.nummi-pusula.fi:80/koulut/sivukartta.asp?kieli=246

## Tämän kierroksen tuloksettomat haut

- Hyrsylän `Linkit`-haaran (`sivu=121&alasivu=245&kieli=246`) seuraaminen arkistoidusta sivukartasta johti Waybackin ilmoitukseen, ettei kyseistä URL:ia ole arkistoitu. Tulos kirjataan tämän avaustavan vastauksena, ei todisteena kaikkien URL-varianttien puuttumisesta.
- Vuoden 2001 etusivun `olli-perustiedot.htm`-kuvalinkki johti samaan arkiston ilmoitukseen.
- Vuoden 2008 kouluportaalin Hyrsylän joululauluilmoituksen linkki `http://www.nummi-pusula.fi/ajankohtaista.asp?id_tiedote=113&kieli=246` ei avannut kohdesisältöä Waybackissa. Portaalin säilynyt linkkiteksti ja kohdesivun puuttuva sisältö ovat eri asioita.
- Saunalahden HTML-osoitteiden CDX-haku palautti HTTP 503:n. Common Crawlin `CC-MAIN-2013-20`-kokoelman täsmähaku DNA:n `tuntemuksiani.htm`-osoitteelle palautti HTTP 404:n. Näistä ei päätellä muiden kokoelmien tai arkistojen kattavuutta.

Uutta Hyrsylän oppilassivun sisältötallennetta ei löytynyt tällä kierroksella. Kuvagalleria dokumentoi aiemmin löytyneet alkuperäistallenteet ja helpottaa niiden tarkistamista.

## Henkilötietojen minimointi rakennekatselmuksessa

Entisten oppilaiden henkilöprofiilit poistettiin sivulta. Vanha `#/oppilaat`-osoite ohjaa nyt Oppilastyöt-näkymään: siinä kuvataan sivujen etsintää ja löydön todentamisen ehtoja. Muistitiedossa säilyvät julkisten kouluhistoriallisten lähteiden tarpeelliset tekijäviitteet. Myös aiempi kuolintiedon etsimistä koskeva sivuhuomautus poistettiin tämän verkkosivututkimuksen ulkopuolisena. Uusia henkilö- tai oikeusväitteitä ei lisätty.
