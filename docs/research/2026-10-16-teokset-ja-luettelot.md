# Uudet teokset, nimiluettelot ja aineiston navigaatio 16.10.2026

## Teokset

Katalogiin lisättiin 30 yksittäistä kirjoitelmaa, tunnisteet T-099–T-128. Valinta, otsikko, tekijämerkinnät ja lajimääritys ovat `assets/archive/reviewed-school-works.json`-tiedostossa. Lähdesivujen alku- ja loppukohdat käytiin läpi; ne sisältävät varsinaiset teokset, eivät vain hakemistolinkkiä. Importti tarkistaa otsikon, tekijärivin ja lähteen SHA-256:n ennen tallennusta. Lähteet ovat joko muuttumattomina säilytetystä alkuperäispaketista tai uusista CDX-tarkisteeseen täsmäävistä vastauksista. Edellisen erän 21 tarkistepoikkeamaa eivät ole tämän teoserottelun lähteinä.

Mukana on 21 kertomusta, kahdeksan tietokirjoitelmaa ja yksi kirja-arvio. Esimerkkejä ovat Anna Saukkolinin Laivamatka (DLC-0358), Antti Kokkosen eläin- ja Mars-kirjoitelmat (DLC-0367–DLC-0370), Astra Kanervon Harry Potter -kirjat (DLC-0401) sekä Elina Laineen kertomukset. Tieteelliseltä kuulostavat tiedot esitetään historiallisina oppilastöinä, ei nykyisenä luonnontieteellisenä ohjeistuksena.

Lyhyet tekijämerkinnät Antti, Anu L, Jatta sekä yhteisteoksen Roosa, Kreeta ja Jatta säilyvät lähteen mukaisina. URL:n pidempää nimimuotoa ei käytetty täydentämään näitä automaattisesti. Tekstien fiktiivisiä tapahtumia ei tulkita kirjoittajien elämäkertatiedoiksi.

Katalogissa on nyt 128 teosta ja 127 kokotekstiä. T-098 Pontus-piru on edelleen pelkkä säilynyt luettelolinkki. Vanhat 98 tietuetta ja 97 kokotekstiä säilyvät. Teossivut tukevat nyt sekä HYK- että DLC-lähteitä. Teoskatalogin kortista pääsee kokotekstiin, sieltä tekijään ja lähdesivun paikalliseen lukusivuun. Myös henkilökorttien teosnimet linkittävät teossivuille.

## Luokkaluettelot

`src/_data/school-collections.json` sisältää kaksi lähdekohtaista luetteloa, yhteensä 21 nimimerkintää:

- L-DLC-0011: ensimmäisen luokan varsinaisen nimiluettelon 14 nimeä. Sivun arkistopäivä on 21.10.2000; lukuvuotta ei ole vahvistettu tämän perusteella.
- L-HYK-002: viidennen luokan luettelon seitsemän nimeä. Lukuvuoden 2000–2001 peruste on saman lähdesivun kuvan ALT-teksti ”5. luokka 00/01”.

Viidelle ennen rekisteristä puuttuneelle kokonaiselle nimiasulle luotiin uudet historialliset henkilömerkinnät. Henkilörekisterissä on nyt 130 tietuetta. Tietueet eivät väitä tunnistavansa henkilöiden nykyisiä henkilöllisyyksiä. Luokkaluettelon nimi ei myöskään ole yksittäisen valokuvassa esiintyvän henkilön tunnistus.

Luettelosivulta pääsee henkilömerkintään ja siitä takaisin luetteloon. Jos henkilöllä on teoksia, ne voidaan esittää saman tietueen perusteella; työn kuulumista juuri tähän luokkaan tai lukuvuoteen ei päätellä pelkästä tekijänimestä. Suuri osa luokkasivujen muista nimilistoista ja niiden ajoituksista odottaa edelleen lähilukua. Epävarmoihin CDX-vastauksiin perustuvia luokkajäsenyyksiä ei lisätty.

## Navigaatio ja tarkistukset

Koulun yleisvalikko sisältää koulun yleissivut. Aineiston sisällä sama alanavigaatio vaihtuu kaikkiin aineistoryhmiin, henkilö- ja teoshakemistoihin sekä paluulinkkiin Kouluun. Koonnit ja valikko käyttävät yhteistä `schoolSections.json`-määritelmää. Murupolku lisää aineiston pääsivun myös henkilö- ja teossivuille. Sisäisen tietuesivun kohdalla valikko merkitsee aktiivisen ryhmän `aria-current="location"`-attribuutilla.

Tarkistukset käyvät läpi kaikki teostekstit, 30 uuden työn lähdevastaavuuden, luetteloiden 21 nimimerkintää, lähdetarkisteet ja molempiin suuntiin toimivat linkit. Selaimessa tarkistetaan katalogin ajantasaiset tietueet ja lukumäärät, haku, jokaisen aineistoryhmän valikko sekä teos-/henkilö- ja luettelo-/henkilöpolut. Vanhan aineiston ulkoasuvertailu käyttää alkuperäistä tietuejoukkoa ja vanhoja lukumäärätekstejä vain testikehyksessä; julkaistulla sivulla on aina koko ajantasainen aineisto. Alkuperäistä vertailufixturea ei muutettu.

Uusia elämäkertaväitteitä tai korkkitauluyhteyksiä ei johdettu oppilaiden fiktiivisistä teksteistä. Arkistokeruun, puuttuvien kuvien, CDX-poikkeamien ja ulkopuolisten täydentävien lähteiden selvittäminen jatkuu.
