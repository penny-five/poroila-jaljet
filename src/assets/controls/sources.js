export function init() {
  const input = document.getElementById('sourceSearch');
  const type = document.getElementById('sourceType');
  const list = document.getElementById('sourceList');
  const output = document.getElementById('sourceCount');
  const rows = [...list.querySelectorAll('.source-entry')].map(element => ({
    element,
    kind: element.dataset.sourceKind,
    search: [element.querySelector('.source-index').textContent, element.querySelector('h3').textContent,
      element.dataset.publisher, element.querySelector('.source-date').textContent,
      element.querySelector('p').textContent].join(' ').toLowerCase(),
  }));
  function update() {
    const query = input.value.trim().toLowerCase();
    const hits = rows.filter(row => (type.value === 'all' || type.value === row.kind) && row.search.includes(query));
    output.textContent = `${hits.length} / ${rows.length} LÄHDEVIITETTÄ`;
    if (hits.length) list.replaceChildren(...hits.map(row => row.element));
    else {
      const empty = document.createElement('p');
      empty.className = 'no-results';
      empty.textContent = 'Lähteitä ei löytynyt näillä ehdoilla.';
      list.replaceChildren(empty);
    }
  }
  input.addEventListener('input', update);
  type.addEventListener('change', update);
  update();
}
