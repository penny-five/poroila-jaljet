(() => {
  const board = document.getElementById('corkboard');
  const holder = document.getElementById('boardNodes');
  const svg = document.getElementById('strings');
  const detail = document.getElementById('nodeDetail');
  const dataElement = document.getElementById('graph-data');
  if (!board || !holder || !svg || !detail || !dataElement) return;

  const data = JSON.parse(dataElement.textContent);
  const nodes = new Map(data.nodes.map((node) => [node.id, node]));
  const sources = new Map(data.sources.map((source) => [source.id, source]));
  let selected = 'olli';
  let moving = null;

  function nodeElement(id) {
    return holder.querySelector(`[data-id="${CSS.escape(id)}"]`);
  }

  function center(id) {
    const element = nodeElement(id);
    return {
      x: Number.parseFloat(element.style.left) + element.offsetWidth / 2,
      y: Number.parseFloat(element.style.top) + element.offsetHeight / 2,
    };
  }

  function drawLines() {
    svg.setAttribute('viewBox', `0 0 ${board.clientWidth} 760`);
    svg.replaceChildren();
    for (const edge of data.edges) {
      const start = center(edge.from);
      const end = center(edge.to);
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      const classes = ['string-line'];
      if (edge.status === 'open') classes.push('open');
      if (selected && (edge.from === selected || edge.to === selected)) classes.push('highlight');
      line.setAttribute('class', classes.join(' '));
      line.setAttribute('x1', String(start.x));
      line.setAttribute('y1', String(start.y));
      line.setAttribute('x2', String(end.x));
      line.setAttribute('y2', String(end.y));
      svg.append(line);
    }
  }

  function selectNode(id) {
    const node = nodes.get(id);
    if (!node) return;
    selected = id;
    holder.querySelectorAll('.node').forEach((element) => {
      element.classList.toggle('active', element.dataset.id === id);
    });

    const ordinal = String([...nodes.keys()].indexOf(id) + 1).padStart(3, '0');
    detail.replaceChildren();
    const meta = document.createElement('div');
    meta.className = 'detail-id';
    meta.textContent = 'VALITTU JOHTOLANKA';
    const position = document.createElement('span');
    position.textContent = `${ordinal} / ${String(nodes.size).padStart(3, '0')}`;
    meta.append(position);
    const title = document.createElement('h3');
    title.textContent = node.name;
    const status = document.createElement('div');
    status.className = 'detail-notice';
    status.textContent = node.evidenceStatus;
    const description = document.createElement('p');
    description.textContent = node.description;
    const links = document.createElement('div');
    links.className = 'node-sources';
    for (const sourceId of node.refs) {
      const source = sources.get(sourceId);
      if (!source) continue;
      const link = document.createElement('a');
      link.href = source.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = `[${source.id}] ${source.title} ↗`;
      links.append(link);
    }
    detail.append(meta, title, status, description, links);
    drawLines();
  }

  holder.addEventListener('pointerdown', (event) => {
    const element = event.target.closest('.node');
    if (!element) return;
    moving = {
      element,
      id: element.dataset.id,
      startX: event.clientX,
      startY: event.clientY,
      left: Number.parseFloat(element.style.left),
      top: Number.parseFloat(element.style.top),
      dragged: false,
    };
    try { element.setPointerCapture(event.pointerId); } catch {}
  });

  holder.addEventListener('pointermove', (event) => {
    if (!moving) return;
    const dx = event.clientX - moving.startX;
    const dy = event.clientY - moving.startY;
    if (Math.abs(dx) + Math.abs(dy) > 6) moving.dragged = true;
    if (!moving.dragged) return;
    moving.element.style.left = `${Math.max(0, Math.min(board.clientWidth - moving.element.offsetWidth, moving.left + dx))}px`;
    moving.element.style.top = `${Math.max(38, Math.min(760 - moving.element.offsetHeight, moving.top + dy))}px`;
    drawLines();
  });

  holder.addEventListener('pointerup', (event) => {
    if (!moving) return;
    const finished = moving;
    moving = null;
    if (finished.dragged) finished.element.dataset.skipClick = '1';
    else selectNode(finished.id);
    if (finished.dragged) setTimeout(() => delete finished.element.dataset.skipClick, 50);
    try { finished.element.releasePointerCapture(event.pointerId); } catch {}
  });

  holder.addEventListener('click', (event) => {
    const element = event.target.closest('.node');
    if (element && !element.dataset.skipClick) selectNode(element.dataset.id);
  });

  document.querySelectorAll('.filter[data-filter]').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.filter[data-filter]').forEach((item) => item.classList.toggle('active', item === button));
      const filter = button.dataset.filter;
      holder.querySelectorAll('.node').forEach((element) => {
        const hit = filter === 'all' || element.dataset.type === filter || (filter === 'open' && ['letter', 'kekkonen', 'salla'].includes(element.dataset.id));
        element.classList.toggle('dim', !hit);
      });
    });
  });

  document.getElementById('resetBoard')?.addEventListener('click', () => {
    data.nodes.forEach((node) => {
      const element = nodeElement(node.id);
      element.style.left = `${node.position.x}px`;
      element.style.top = `${node.position.y}px`;
      element.classList.remove('dim');
    });
    document.querySelectorAll('.filter[data-filter]').forEach((button) => button.classList.toggle('active', button.dataset.filter === 'all'));
    selectNode('olli');
  });

  window.addEventListener('resize', drawLines);
  selectNode(selected);
})();
