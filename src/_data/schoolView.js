const archive = require('./schoolArchive.json');
const catalog = require('./catalog.js');

const sections = [
  { slug: 'oppilaiden-sivut', title: 'Oppilaiden sivut', category: 'Oppilaiden sivut', intro: 'Oppilaiden omat sivut, yhteiset sivut ja kirjoitelmat. Kunkin lähdesivun teksti on luettavissa täällä; palautuneet kuvat näkyvät samassa lukusivussa.' },
  { slug: 'luokat', title: 'Luokat ja oppilasluettelot', category: 'Luokat ja oppilasluettelot', intro: 'Alkuperäisten sivujen luokka- ja nimiluettelot. Sivun tallennusajankohta ei yksin osoita luettelon lukuvuotta, eikä kaikkia nimiluetteloita ole yhdistetty luokkajäsenyyksiksi.' },
  { slug: 'kuva-ja-taidesivut', title: 'Kuva- ja taidesivut', category: 'Kuva- ja taidesivut', intro: 'Koulun alkuperäiset kuva- ja taidehakemistot. Palautunut hakemistosivu ei tarkoita, että sen kaikki kuvat olisivat vielä löytyneet.' },
  { slug: 'runot-ja-kirjoitelmat', title: 'Runot ja kirjoitelmat', category: 'Runot ja oppilastyöt', intro: 'Runokokoelmat ja muut oppilastöiden lähdesivut kokonaisina lukuteksteinä. Teoskatalogiin erotellut työt löytyvät lisäksi pysyviltä teossivuilta.' },
  { slug: 'koulun-sivut', title: 'Koulun muut sivut', category: 'Koulun muut sivut', intro: 'Koulutilat, toiminta, henkilökunnan esittelyt, lukujärjestykset ja muut säilyneet sivut.' },
].map(section => ({ ...section, pages: archive.pages.filter(page => page.category === section.category) }));
const byId = Object.fromEntries(archive.pages.map(page => [page.id, page]));
const pages = archive.pages.map(page => ({
  ...page,
  works: catalog.works.filter(work => page.workIds.includes(work.id)),
  incoming: archive.pages.filter(source => source.id !== page.id && source.links.some(link => link.readerPath === `/koulu/aineisto/${page.id}/`)),
  localImages: page.images.filter(image => image.displayPath && image.role !== 'background'),
  missingImages: page.images.filter(image => !image.localPath),
}));
module.exports = {
  pages, sections, byId,
  mediaGroups: archive.mediaGroups.map(title => ({ title, images: archive.media.filter(image => image.group === title) })),
  pageCount: pages.length,
  imageCount: archive.media.length,
};
