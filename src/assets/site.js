document.addEventListener('input', (event) => {
  const input = event.target.closest('[data-filter-input]');
  if (!input) return;
  const list = document.getElementById(input.dataset.filterInput);
  if (!list) return;
  const query = input.value.trim().toLocaleLowerCase('fi');
  let visible = 0;
  for (const row of list.querySelectorAll('[data-filter-item]')) {
    row.hidden = !row.textContent.toLocaleLowerCase('fi').includes(query);
    if (!row.hidden) visible += 1;
  }
  const count = document.getElementById(input.dataset.filterCount || '');
  if (count) count.textContent = `${visible} merkintää`;
});

document.addEventListener('click', async (event) => {
  const button = event.target.closest('[data-copy-url]');
  if (!button) return;
  const value = button.dataset.copyUrl;
  try {
    await navigator.clipboard.writeText(value);
    button.textContent = 'KOPIOITU ✓';
  } catch {
    button.textContent = value;
  }
});
