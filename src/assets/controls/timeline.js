export function init() {
  for (const list of document.querySelectorAll('.timeline-list')) {
    const rows = [...list.querySelectorAll('[data-year]')];
    const buttons = [...list.closest('section').querySelectorAll('[data-decade]')];
    for (const button of buttons) button.addEventListener('click', () => {
      buttons.forEach(item => item.classList.toggle('active', item === button));
      const decade = button.dataset.decade;
      const hits = rows.filter(row => decade === 'all' || (decade === '1900'
        ? +row.dataset.year >= 1900 && +row.dataset.year < 1970
        : row.dataset.year.startsWith(decade.slice(0, 3))));
      if (hits.length) list.replaceChildren(...hits);
      else {
        const empty = document.createElement('p');
        empty.className = 'no-results';
        empty.textContent = 'Ei merkintöjä.';
        list.replaceChildren(empty);
      }
    });
  }
}
