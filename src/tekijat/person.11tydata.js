const ids = require('../_data/legacyPersonIds.json');
module.exports = {
  eleventyComputed: {
    layout: data => ids.includes(data.person.id) ? 'layouts/preserved-page.njk' : 'layouts/legacy-page.njk',
    legacyPage: data => ids.includes(data.person.id) ? 'henkilot' : null,
    title: data => `${data.person.name} — HYRSYLÄ / JÄLJET | Historiallinen henkilömerkintä`,
  },
};
