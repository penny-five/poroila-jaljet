export function init() {
  const button = document.getElementById('copyOriginal');
  button.addEventListener('click', async () => {
    const address = 'http://kotisivu.dnainternet.net/poroila/';
    try {
      await navigator.clipboard.writeText(address);
      button.textContent = 'KOPIOITU ✓';
    } catch {
      button.textContent = address;
    }
  });
}
