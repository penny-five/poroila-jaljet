export function init() {
  const modal = document.getElementById('articleDialog');
  const content = document.getElementById('articleContent');
  for (const button of document.querySelectorAll('[data-article]')) button.addEventListener('click', () => {
    const template = document.getElementById(`article-${button.dataset.article}`);
    if (!template) return;
    content.replaceChildren(template.content.cloneNode(true));
    modal.showModal();
    modal.scrollTop = 0;
  });
  document.getElementById('articleClose').addEventListener('click', () => modal.close());
  modal.addEventListener('click', event => { if (event.target === modal) modal.close(); });
}
