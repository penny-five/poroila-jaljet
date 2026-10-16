const prefix = (process.env.SITE_PREFIX || '/').replace(/\/*$/, '/') || '/';
const legacyRoutes = require('./src/_data/legacyRoutes.json');
const routeAliases = require('./src/_data/routeAliases.json');

function canonicalPath(value) {
  const [_, path, suffix] = String(value).match(/^([^?#]*)(.*)$/);
  const local = prefix !== '/' && path.startsWith(prefix) ? `/${path.slice(prefix.length)}` : path;
  const route = local.replace(/\/index\.html$/, '/');
  return routeAliases[route] ? `${routeAliases[route]}${suffix}` : value;
}

function canonicalLegacyHash(value) {
  const parts = decodeURIComponent(value).split('/').filter(Boolean);
  if (parts[0] === 'henkilot' && /^H-[a-f0-9]{10}$/i.test(parts[1] || '')) {
    return `/tekijat/${parts[1]}/`;
  }
  return legacyRoutes[parts[0]] || null;
}

function prefixLocalPath(value) {
  const url = String(canonicalPath(value));
  if (/^(?:[a-z]+:|\/\/|#)/i.test(url)) return url;
  if (url.startsWith('/')) {
    const base = prefix.replace(/^\/+|\/+$/g, '');
    if (!base || url === `/${base}` || url.startsWith(`/${base}/`)) return url;
    return `${prefix}${url.replace(/^\/+/, '')}`;
  }
  if (url.startsWith('./') || url.startsWith('../')) {
    const normalized = require('node:path').posix.normalize(url).replace(/^\.\//, '');
    return prefixLocalPath(`/${normalized}`);
  }
  if (/^(?:assets\/|style\.css$|app\.js$|research-data\.js$)/.test(url)) return `${prefix}${url}`;
  return url;
}

module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({
    'assets/archive': 'assets/archive',
    'src/assets': 'assets',
    'src/styles/site.css': 'style.css',
    '.nojekyll': '.nojekyll',
    'src/scripts/bookmarks.js': 'legacy-routes.js',
  });

  eleventyConfig.addFilter('localUrl', (value = '/') => {
    const url = String(value);
    if (/^(?:[a-z]+:|\/\/|#)/i.test(url)) return url;
    return prefixLocalPath(`/${url.replace(/^\/+/, '')}`);
  });

  eleventyConfig.addFilter('prefixPaths', (html = '') => String(html).replace(
    /\b(href|src|poster)=(['"])([^'"]*)\2/gi,
    (match, attr, quote, value) => {
      if (attr.toLowerCase() === 'href' && value.startsWith('#/')) {
        const route = canonicalLegacyHash(value.slice(2));
        if (route) return `${attr}=${quote}${prefix}${route.replace(/^\/+/, '')}${quote}`;
      }
      const path = prefixLocalPath(value);
      return path === value ? match : `${attr}=${quote}${path}${quote}`;
    },
  ));

  eleventyConfig.addFilter('findSource', (sources, id) => sources.find((source) => source.id === id));
  eleventyConfig.addFilter('dateStamp', (value) => String(value).slice(0, 8));
  eleventyConfig.addFilter('sourceType', group => group === 'Katalogit' ? 'primary' : ['Oikeusuutiset', 'Aikalaisblogit'].includes(group) ? 'press' : 'open');
  eleventyConfig.addFilter('sourceLabel', kind => ({primary:'KIRJASTOLUETTELO',press:'UUTISOINTI / AIKALAISBLOGI',open:'AVOIN TUTKIMUSPOLKU'})[kind]);
  eleventyConfig.addFilter('legacyGroup', (groups, page) => groups.find((group) => group.pages.includes(page)) || groups[0]);
  eleventyConfig.addFilter('concat', (first = [], second = []) => [...first, ...second]);
  eleventyConfig.addFilter('pathForPerson', (authors, name) => authors.find((author) => author.name === name));
  eleventyConfig.addFilter('sectionForPath', (sections = [], path = '') => sections
    .flatMap((section) => section.prefixes.filter((item) => String(path).startsWith(item)).map((prefixValue) => ({ section, prefixValue })))
    .sort((a, b) => b.prefixValue.length - a.prefixValue.length)[0]?.section);
  eleventyConfig.addFilter('primaryIsCurrent', (item, items = [], path = '') => {
    const match = items.flatMap((candidate) => candidate.prefixes
      .filter((prefixValue) => prefixValue === '/' ? path === '/' : String(path).startsWith(prefixValue))
      .map((prefixValue) => ({ candidate, prefixValue })))
      .sort((a, b) => b.prefixValue.length - a.prefixValue.length)[0];
    return match?.candidate === item;
  });
  eleventyConfig.addFilter('navItemIsCurrent', (item, path = '') => item.url === path || Boolean(item.prefix && String(path).startsWith(item.prefix)));
  eleventyConfig.addFilter('toJson', (value) => JSON.stringify(value).replace(/</g, '\\u003c'));
  eleventyConfig.addGlobalData('sitePrefix', prefix);

  return {
    dir: {
      input: 'src',
      output: '_site',
      includes: '_includes',
      data: '_data',
    },
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
    htmlOutputSourcemap: false,
  };
};
