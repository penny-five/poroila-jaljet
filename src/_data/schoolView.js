const archive = require('./schoolArchive.json');
const catalog = require('./catalog.js');
const classRecords = require('./school-collections.json');
const classes = classRecords.map(group => ({ ...group,
  source: archive.pages.find(page => page.id === group.sourceId),
  members: group.members.map(member => ({ ...member, person: catalog.peopleById[member.personId] })),
}));

const sections = require('./schoolSections.json').map(section => ({ ...section, pages: archive.pages.filter(page => page.category === section.category || (section.slug === 'runot-ja-kirjoitelmat' && /runo|kirjoitelma/i.test(page.filename))) }));
const byId = Object.fromEntries(archive.pages.map(page => [page.id, page]));
const pages = archive.pages.map(page => ({
  ...page,
  works: catalog.works.filter(work => page.workIds.includes(work.id)),
  incoming: archive.pages.filter(source => source.id !== page.id && source.links.some(link => link.readerPath === `/koulu/aineisto/${page.id}/`)),
  localImages: page.images.filter(image => image.displayPath && image.role !== 'background'),
  missingImages: page.images.filter(image => !image.localPath),
}));
module.exports = {
  pages, sections, byId, classes,
  schoolYears: require('./schoolYears.json').map(year => ({ ...year, source: byId[year.sourceId],
    rosters: classes.filter(group => group.period === year.period),
  })),
  imageSets: archive.imageSets,
  imageSetGroups: ['DLC-0080', 'DLC-0081', 'DLC-0082', 'DLC-0083'].map(id => ({
    source: byId[id], sets: archive.imageSets.filter(set => set.sourceId === id),
  })),
  mediaGroups: archive.mediaGroups.map(title => ({ title, images: archive.media.filter(image => image.group === title) })),
  pageCount: pages.length,
  imageCount: archive.media.length,
};
