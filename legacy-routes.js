(() => {
  function redirectLegacyBookmark() {
  const raw = window.location.hash;
  if (!raw.startsWith('#/')) return;

  const data = document.getElementById('legacy-route-map');
  if (!data) return;

  let routes;
  try {
    routes = JSON.parse(data.textContent);
  } catch {
    return;
  }

  const base = document.querySelector('meta[name="site-base"]')?.content || '/';
  let parts;
  try {
    parts = decodeURIComponent(raw.slice(2)).split('/').filter(Boolean);
  } catch {
    return;
  }
  let route = routes[parts[0]];
  if (parts[0] === 'henkilot' && /^H-[a-f0-9]{10}$/i.test(parts[1] || '')) {
    route = `/tekijat/${parts[1]}/`;
  }
  if (route) window.location.replace(`${base}${route.replace(/^\/+/, '')}`);
  }
  window.addEventListener('hashchange', redirectLegacyBookmark);
  redirectLegacyBookmark();
})();
