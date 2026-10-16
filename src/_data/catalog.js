const path = require('node:path');
const crypto = require('node:crypto');
const archive = require(path.join(__dirname, '..', '..', 'assets', 'archive', 'hyk-katalogi.json'));
const originals = require(path.join(__dirname, '..', '..', 'assets', 'archive', 'originals-manifest.json'));
const workTexts = require('./work-texts.json');

const originalById = new Map(originals.files.map((file) => [file.id, file]));

const pages = archive.pages.map((page) => ({ ...page, localCopy: originalById.get(page.id) || null }));
const pageById = new Map(pages.map((page) => [page.id, page]));
const recordByName = new Map(archive.people.map((person) => [person.name, person]));
const dlcRecords = archive.dlc_records.map((record) => ({ ...record, localCopy: originalById.get(record.id) || null }));
const documentById = new Map(dlcRecords.map((record) => [record.id, record]));
const works = archive.works.map((work) => ({
  ...work,
  sourcePage: pageById.get(work.page) || documentById.get(work.page) || null,
  fullText: workTexts[work.id] || null,
}));
const workById = new Map(works.map((work) => [work.id, work]));
const allWorksByName = new Map();

for (const work of works) {
  for (const name of work.authors) {
    if (!allWorksByName.has(name)) allWorksByName.set(name, []);
    allWorksByName.get(name).push(work);
  }
}

const authors = [...allWorksByName.entries()].map(([name, works]) => {
  const record = recordByName.get(name);
  const id = record?.id || `H-${crypto.createHash('sha1').update(`author:${name}`).digest('hex').slice(0, 10)}`;
  const documents = (record?.documents || []).map((docId) => pageById.get(docId) || documentById.get(docId)).filter(Boolean);
  const images = archive.images.filter((image) =>
    image.labels.some((label) => label.toLocaleLowerCase('fi') === name.toLocaleLowerCase('fi')) ||
    image.sources.some((source) => (record?.documents || []).includes(source)),
  );
  return { id, name, sourceRecord: Boolean(record), observations: record?.observations || [], documents, works, images };
}).sort((a, b) => a.name.localeCompare(b.name, 'fi'));

const authorByName = new Map(authors.map((person) => [person.name, person]));
const people = archive.people.map((record) => ({
  ...record,
  author: authorByName.get(record.name) || null,
  documents: record.documents.map((docId) => pageById.get(docId) || documentById.get(docId)).filter(Boolean),
  works: record.works.map((workId) => workById.get(workId)).filter(Boolean),
  images: archive.images.filter((image) =>
    image.labels.some((label) => label.toLocaleLowerCase('fi') === record.name.toLocaleLowerCase('fi')) ||
    image.sources.some((source) => record.documents.includes(source)),
  ),
}));

const pagesById = new Map(people.map((person) => [person.id, person]));
for (const author of authors) {
  if (!pagesById.has(author.id)) {
    pagesById.set(author.id, { id: author.id, name: author.name, observations: [], documents: [], works: author.works, images: author.images, author });
  }
}

module.exports = {
  ...archive,
  pages,
  dlc_records: dlcRecords,
  originalFiles: originals.files,
  originalFileCount: originals.files.length,
  preservedHyKFilesCount: originals.files.filter((file) => file.collection === 'Saunalahti / Hyrsylän koulu').length,
  preservedDlcFilesCount: originals.files.filter((file) => file.collection === 'DLC / Hyrsylän koulu').length,
  works,
  distinctWorksCount: works.filter(work => !work.duplicateOf).length,
  readPagesCount: archive.pages.filter((page) => page.status === 'HTML luettu').length,
  authors,
  people,
  recordsById: Object.fromEntries([...pages, ...dlcRecords].map(record => [record.id, record])),
  peopleById: Object.fromEntries(people.map(person => [person.id, person])),
  nonAuthorsCount: people.filter((person) => !person.author).length,
  personPages: [...pagesById.values()].sort((a, b) => a.name.localeCompare(b.name, 'fi')),
};
