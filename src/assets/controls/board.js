export function init() {
const graph=JSON.parse(document.getElementById('graph-data').textContent);
const sources=graph.sources;const byId=Object.fromEntries(sources.map(source=>[source.id,source]));
const enc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const sourceLink=id=>{const s=byId[id];return s?'<a href="'+enc(s.url)+'" target="_blank" rel="noopener noreferrer">['+enc(s.id)+'] '+enc(s.title)+' ↗</a>':''};
const sourceLinks=refs=>refs.map(sourceLink).join('');
const nodeData=graph.nodes.map(n=>({...n,x:n.position.x,y:n.position.y,text:n.description,notice:n.evidenceStatus}));
const edges=graph.edges.map(e=>[e.from,e.to,e.status]);
const board=document.getElementById('corkboard'),holder=document.getElementById('boardNodes'),svg=document.getElementById('strings');
let chosen='olli',moving=null;
function center(id){const n=document.getElementById('node-'+id);return {x:parseFloat(n.style.left)+n.offsetWidth/2,y:parseFloat(n.style.top)+n.offsetHeight/2};}
function lines(){svg.setAttribute('viewBox','0 0 '+board.clientWidth+' 760');svg.innerHTML=edges.map(([a,b,t])=>{const p=center(a),q=center(b);return '<line class="string-line '+(t==='open'?'open ':'')+(chosen&&(a===chosen||b===chosen)?'highlight':'')+'" x1="'+p.x+'" y1="'+p.y+'" x2="'+q.x+'" y2="'+q.y+'"/>';}).join('');}
function selectNode(id){chosen=id;const n=nodeData.find(x=>x.id===id);if(!n)return;document.querySelectorAll('.node').forEach(x=>x.classList.toggle('active',x.dataset.id===id));lines();document.getElementById('nodeDetail').innerHTML='<div class="detail-id">VALITTU JOHTOLANKA <span>'+String(nodeData.indexOf(n)+1).padStart(3,'0')+' / 014</span></div><h3>'+enc(n.name)+'</h3><div class="detail-notice">'+enc(n.notice)+'</div><p>'+enc(n.text)+'</p><div class="node-sources">'+sourceLinks(n.refs)+'</div>';}
selectNode('olli');
holder.addEventListener('pointerdown',e=>{const el=e.target.closest('.node');if(!el)return;moving={el,id:el.dataset.id,sx:e.clientX,sy:e.clientY,left:parseFloat(el.style.left),top:parseFloat(el.style.top),dragged:false};try{el.setPointerCapture(e.pointerId);}catch{}});
holder.addEventListener('pointermove',e=>{if(!moving)return;const dx=e.clientX-moving.sx,dy=e.clientY-moving.sy;if(Math.abs(dx)+Math.abs(dy)>6)moving.dragged=true;if(moving.dragged){moving.el.style.left=Math.max(0,Math.min(board.clientWidth-moving.el.offsetWidth,moving.left+dx))+'px';moving.el.style.top=Math.max(38,Math.min(760-moving.el.offsetHeight,moving.top+dy))+'px';lines();}});
holder.addEventListener('pointerup',e=>{if(!moving)return;const m=moving;moving=null;if(!m.dragged)selectNode(m.id);else{m.el.dataset.skipClick='1';setTimeout(()=>delete m.el.dataset.skipClick,50)}});
holder.addEventListener('click',e=>{const n=e.target.closest('.node');if(n&&!n.dataset.skipClick)selectNode(n.dataset.id);});
document.getElementById('resetBoard').addEventListener('click',()=>{nodeData.forEach(n=>{const el=document.getElementById('node-'+n.id);el.style.left=n.x+'px';el.style.top=n.y+'px';el.classList.remove('dim');});document.querySelectorAll('.filter').forEach(b=>b.classList.toggle('active',b.dataset.filter==='all'));selectNode('olli');});
document.querySelectorAll('.filter').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.filter').forEach(x=>x.classList.toggle('active',x===b));const f=b.dataset.filter;document.querySelectorAll('.node').forEach(el=>{const n=nodeData.find(x=>x.id===el.dataset.id);const hit=f==='all'||n.type===f||(f==='open'&&(n.type==='open'||['letter','kekkonen','salla'].includes(n.id)));el.classList.toggle('dim',!hit);});}));
window.addEventListener('resize',lines);
}
