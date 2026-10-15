const loaders = {
  catalog: () => import('./controls/catalog.js'),
  timeline: () => import('./controls/timeline.js'),
  sources: () => import('./controls/sources.js'),
  articles: () => import('./controls/articles.js'),
  board: () => import('./controls/board.js'),
  copy: () => import('./controls/copy.js'),
  archive: () => import('./controls/archive.js'),
};

try {
  await Promise.all((document.body.dataset.features || '').split(' ').filter(Boolean).map(async feature => {
    const module = await loaders[feature]();
    module.init();
  }));
  document.body.dataset.siteReady = 'true';
} catch (error) {
  console.error('Sivuston toimintojen alustaminen epäonnistui', error);
}
