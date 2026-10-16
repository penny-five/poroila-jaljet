const navigation = require('../src/_data/navigation.js');

function breadcrumbs(url, { title, parent, person, work, source, breadcrumbTitle } = {}) {
  const route = String(url).replace(/index\.html$/, '');
  if (route === '/') return [];
  const owner = navigation.primary.flatMap(item => item.prefixes
    .filter(prefix => prefix !== '/' && route.startsWith(prefix))
    .map(prefix => ({ item, prefix })))
    .sort((a, b) => b.prefix.length - a.prefix.length)[0]?.item;
  const links = navigation.sections.flatMap(section => section.links);
  const labelFor = path => links.find(link => link.url === path)?.label;
  const trail = [{ label: 'Etusivu', url: '/' }];
  if (owner && owner.url !== route) trail.push({ label: owner.label, url: owner.url });
  if (parent?.url && parent.url !== route && !trail.some(item => item.url === parent.url)) {
    trail.push({ label: labelFor(parent.url) || parent.label, url: parent.url });
  }
  const label = breadcrumbTitle || person?.name || work?.title || source?.title ||
    (owner?.url === route ? owner.label : labelFor(route)) ||
    String(title || route).replace(/\s+[—|]\s+HYRSYLÄ[\s\S]*$/i, '');
  trail.push({ label, url: null });
  return trail;
}

module.exports = breadcrumbs;
module.exports.pageHeading = function pageHeading(url, metadata = {}) {
  const route = String(url).replace(/index\.html$/, '');
  if (route === '/') return null;
  const trail = breadcrumbs(route, metadata);
  const owner = navigation.primary.find(item => item.prefixes.some(prefix => prefix !== '/' && route.startsWith(prefix)));
  const intros = require('../src/_data/pageIntros.json');
  return {
    title: metadata.headingTitle || metadata.person?.name || metadata.work?.title || metadata.source?.title ||
      String(metadata.title || trail.at(-1).label).replace(/\s+[—|]\s+HYRSYLÄ[\s\S]*$/i, ''),
    eyebrow: owner?.label || 'Tutkimusarkisto',
    lead: metadata.lead || intros[metadata.legacyPage] || null,
  };
};
