# Viimeinen erä ja jatkokohta 16.10.2026

Työ pysäytetään käyttäjän pyynnöstä tämän erän pushin jälkeen. Tavoite ei ole valmis: kouluarkiston keruu, teosten erottelu ja puuttuvien lähteiden selvittäminen jatkuvat vasta uudesta pyynnöstä.

## Viimeisimmät paikalliset löydöt

Palautettiin 20 tiedostoa: 19 HTML-sivua ja yksi JPEG-kuva. Kolmetoista täsmää CDX-tarkisteeseen; seitsemän ei: DLC-0680, DLC-0706, DLC-0707, DLC-0708, DLC-0725, DLC-0734 ja DLC-0740. Poikkeamat säilyvät näkyvin varoituksin, eikä niitä käytetty tämän erän tarkistettujen teosten lähteinä. Paikallisia alkuperäistiedostoja on 477, koulun lukusivuja 298 ja esityskuvia 168.

## Teokset, katkelmat ja viimeistelemätön teksti

Katalogiin eroteltiin 15 uutta teostietuetta, T-136–T-150. Kaksitoista sisältää luetun kokonaisen tekstin, kaksi tallenteessa kesken virkkeen päättyvän tekstin ja yksi lähteessä viimeistelemättömäksi merkityn tekstin. Tekijärivit, moniriviset otsikot ja lähteen merkinnät säilyvät litteroinnissa. Tarkat valinnat ja tekstin tilan perusteet ovat reviewed-school-works.json-tiedostossa.

- T-136–T-145: Börje junassa; Possun seikkailut; Jalkapallo; Pelottava maastoratsastus; Luomuviljely; Aavelaiva; Sukeltaja; Hautausmaan aave; Sylvesteri karkuteillä; Terocin seikkailu.
- T-146–T-147: Kalle oli pahassa pulassa; Vampyyri, joka pelkäsi varjoaan. Metatieto yhdistää monirivisen otsikon, mutta litterointi säilyttää lähteen rivit.
- T-148 Reijon kesäloma ja T-149 Lupauksen vanki: tallenteen teksti päättyy kesken virkkeen ennen HTML:n PRE-elementin loppua. Näitä ei esitetä kokonaisina teoksina. Puuttuvan lopun syytä ei päätellä.
- T-150 Matkalla maailmalle: lähde merkitsee tekstin viimeistelemättömäksi. Merkintä näkyy myös teossivulla, ja teksti säilyy kokonaisena sellaisena kuin se on tallenteessa.

Teostietueita on 150, niistä 147:llä on kokonainen tekstiversio ja kolmella katkelma tai viimeistelemätön teksti. Neljä tietuetta on tunnistettu saman teoksen rinnakkaisiksi tietueiksi, joten erillisiä teoksia on 146. Näitä lukumääriä ei pidä sekoittaa.

## Havaitut vanhat päällekkäisyydet

Tuontitarkistus löysi aiemmassa erässä syntyneet rinnakkaiset tietueet T-129/T-084, T-130/T-085, T-131/T-086 ja T-132/T-087. Niiden tekijät ja otsikot ovat samat, ja koko litteroitu teksti täsmää tekijärivin ja välilyöntien eroa lukuun ottamatta. Kyse on Saunalahden ja DLC:n eri lähdetallenteista samalle tekstille.

T-129–T-132 on merkitty duplicateOf-kentällä ja lähteiden vastaavuus on perusteltu. Pysyviä tunnisteita ei poistettu tai numeroitu uudelleen. Rinnakkaisella teossivulla on näkyvä selitys ja linkki aiempaan tietueeseen; myös katalogin kortti kertoo rinnakkaisuudesta. Tarkistus vertaa tekstit ja tekijät toisiinsa. Tulevan uuden tietueen tuonti pysähtyy, jos vastaava otsikko ja tekijä jo ovat katalogissa. Vanhojen lähdeversioiden yhdistäminen yhdeksi monilähteiseksi teosmalliksi jää jatkotyöksi; lähdetallenteet on silloinkin säilytettävä erillisinä.

## Jatkettavat asiat

- Tarkista jäljellä olevat oppilassivujen ja kuvien linkitetyt tiedostot. Palautustyökalu tukee rajattua erää, --retry-valintaa sekä --ids-täsmävalintaa. Älä käynnistä laajaa korvaavaa arkistogeneraattoria.
- Useita luettelosivuja on luettavissa, mutta CDX-tarkistepoikkeaman syy on avoin. Älä luo niistä varmennettuja luokkajäsenyyksiä. Jo varmennetut kaksi luetteloa säilyvät.
- Uusista lukusivuista on yhä paljon tekstejä erottelematta omiksi teostietueiksi. Tarkista ensin nykyinen otsikko ja tekijä: uudelleen palautettu lähde ei automaattisesti ole uusi teos.
- Puuttuvien kuvien uusien CDX-paikantimien selvittäminen ja vaihtoehtoisten tallenteiden haku jatkuu. Yhteysvirhe tai tyhjä saatavuusvastaus ei todista puuttumista.
- Poroilan ja koulun historiaa täydennetään vain lähteistetyillä havainnoilla; oppilastöiden fiktiivisiä tapahtumia ei tulkita elämäkerroiksi.

## Tarkistukset

Teossivujen tarkistus erottaa kokotekstin, katkelman ja viimeistelemättömän tekstin. Kaikki tallenteessa säilynyt teksti verrataan lähteeseen, ja katkelman viimeinen rivi sekä viimeistelemättömyysmerkintä tarkistetaan erikseen. Lisäksi tarkistetaan rinnakkaisten tekstien vastaavuus, vanhojen tunnisteiden säilyminen, paikalliset linkit, kuvat, SHA-256:t ja selaimen käyttöpolut.
