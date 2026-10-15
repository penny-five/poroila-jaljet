const ids = new Set(require('../../assets/archive/hyk-katalogi.json').people.map(person => person.id));
module.exports = {
  eleventyComputed: {
    layout: data => ids.has(data.person.id) ? 'layouts/original-page.njk' : 'layouts/article-page.njk',
    presentation: data => ids.has(data.person.id) ? 'original' : 'article',
    legacyPage: data => ids.has(data.person.id) ? 'henkilot' : null,
    title: data => `${data.person.name} — HYRSYLÄ / JÄLJET | Historiallinen henkilömerkintä`,
  },
};
