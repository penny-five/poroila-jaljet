export function init() {
  for (const input of document.querySelectorAll('[data-catalog-search]')) {
    const list = document.getElementById(input.dataset.catalogSearch);
    const entries = [...list.querySelectorAll('[data-catalog-item]')];
    const output = document.querySelector(`[data-catalog-count="${list.id}"]`);
    const update = () => {
      const query = input.value.toLocaleLowerCase('fi').trim();
      let shown = 0;
      for (const entry of entries) {
        entry.hidden = !entry.textContent.toLocaleLowerCase('fi').includes(query);
        if (!entry.hidden) shown++;
      }
      output.textContent = `${shown} / ${entries.length} merkintää`;
    };
    input.addEventListener('input', update);
    update();
  }
}
