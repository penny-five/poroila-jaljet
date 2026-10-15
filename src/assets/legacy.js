'use strict';
// Original controls, scoped to the elements present on each Eleventy page.
(() => {
const DATA=JSON.parse(document.getElementById('legacy-data').textContent);
const sources=DATA.sources;
const byId=Object.fromEntries(sources.map(s=>[s.id,s]));
const enc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const sourceLink=id=>{const s=byId[id];return s?'<a href="'+enc(s.url)+'" target="_blank" rel="noopener noreferrer">['+enc(s.id)+'] '+enc(s.title)+' ↗</a>':''};
const sourceLinks=refs=>refs.map(sourceLink).join('');
if(document.getElementById('corkboard')){
const graph=JSON.parse(document.getElementById('graph-data').textContent);
const rotations=[-2,2,-3,4,-2,3,1,-2,1,-3,4,-4,3,2];
const nodeData=graph.nodes.map((n,i)=>({...n,sub:n.subtitle,x:n.position.x,y:n.position.y,text:n.description,notice:n.evidenceStatus,rot:rotations[i]}));
const edges=graph.edges.map(e=>[e.from,e.to,e.status]);
const board=document.getElementById('corkboard'),holder=document.getElementById('boardNodes'),svg=document.getElementById('strings');
let chosen='olli',moving=null;
function placeNodes(){holder.innerHTML=nodeData.map(n=>'<button class="node paper-'+enc(n.type)+'" data-id="'+enc(n.id)+'" data-type="'+enc(n.type)+'" id="node-'+enc(n.id)+'" style="left:'+n.x+'px;top:'+n.y+'px;--rot:'+n.rot+'deg" aria-label="Avaa kortti: '+enc(n.name)+'"><span class="node-tape"></span><span class="node-type">'+enc(n.label)+'</span><strong class="node-title">'+enc(n.name)+'</strong><span class="node-sub">'+enc(n.sub)+'</span></button>').join('');}
function center(id){const n=document.getElementById('node-'+id);return {x:parseFloat(n.style.left)+n.offsetWidth/2,y:parseFloat(n.style.top)+n.offsetHeight/2};}
function lines(){svg.setAttribute('viewBox','0 0 '+board.clientWidth+' 760');svg.innerHTML=edges.map(([a,b,t])=>{const p=center(a),q=center(b);return '<line class="string-line '+(t==='open'?'open ':'')+(chosen&&(a===chosen||b===chosen)?'highlight':'')+'" x1="'+p.x+'" y1="'+p.y+'" x2="'+q.x+'" y2="'+q.y+'"/>';}).join('');}
function selectNode(id){chosen=id;const n=nodeData.find(x=>x.id===id);if(!n)return;document.querySelectorAll('.node').forEach(x=>x.classList.toggle('active',x.dataset.id===id));lines();document.getElementById('nodeDetail').innerHTML='<div class="detail-id">VALITTU JOHTOLANKA <span>'+String(nodeData.indexOf(n)+1).padStart(3,'0')+' / 014</span></div><h3>'+enc(n.name)+'</h3><div class="detail-notice">'+enc(n.notice)+'</div><p>'+enc(n.text)+'</p><div class="node-sources">'+sourceLinks(n.refs)+'</div>';}
placeNodes();selectNode('olli');
holder.addEventListener('pointerdown',e=>{const el=e.target.closest('.node');if(!el)return;moving={el,id:el.dataset.id,sx:e.clientX,sy:e.clientY,left:parseFloat(el.style.left),top:parseFloat(el.style.top),dragged:false};try{el.setPointerCapture(e.pointerId);}catch{}});
holder.addEventListener('pointermove',e=>{if(!moving)return;const dx=e.clientX-moving.sx,dy=e.clientY-moving.sy;if(Math.abs(dx)+Math.abs(dy)>6)moving.dragged=true;if(moving.dragged){moving.el.style.left=Math.max(0,Math.min(board.clientWidth-moving.el.offsetWidth,moving.left+dx))+'px';moving.el.style.top=Math.max(38,Math.min(760-moving.el.offsetHeight,moving.top+dy))+'px';lines();}});
holder.addEventListener('pointerup',e=>{if(!moving)return;const m=moving;moving=null;if(!m.dragged)selectNode(m.id);else{m.el.dataset.skipClick='1';setTimeout(()=>delete m.el.dataset.skipClick,50)}});
holder.addEventListener('click',e=>{const n=e.target.closest('.node');if(n&&!n.dataset.skipClick)selectNode(n.dataset.id);});
document.getElementById('resetBoard').addEventListener('click',()=>{nodeData.forEach(n=>{const el=document.getElementById('node-'+n.id);el.style.left=n.x+'px';el.style.top=n.y+'px';el.classList.remove('dim');});document.querySelectorAll('.filter').forEach(b=>b.classList.toggle('active',b.dataset.filter==='all'));selectNode('olli');});
document.querySelectorAll('.filter').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.filter').forEach(x=>x.classList.toggle('active',x===b));const f=b.dataset.filter;document.querySelectorAll('.node').forEach(el=>{const n=nodeData.find(x=>x.id===el.dataset.id);const hit=f==='all'||n.type===f||(f==='open'&&(n.type==='open'||['letter','kekkonen','salla'].includes(n.id)));el.classList.toggle('dim',!hit);});}));
window.addEventListener('resize',lines);
}
const timeline=DATA.timeline,schoolTimeline=DATA.schoolTimeline;
function renderTimelineRows(items,mount,decade='all'){const matches=items.filter(t=>decade==='all'||(decade==='1900'?(t.year>=1900&&t.year<1970):String(t.year).startsWith(decade.slice(0,3))));const target=document.getElementById(mount);if(!target)return;target.innerHTML=matches.map(t=>'<article class="time-row '+(t.open?'open':'')+'"><div class="time-year">'+t.year+'</div><div class="time-dot"></div><div><p class="time-title">'+enc(t.title)+'</p><p class="time-summary">'+enc(t.description)+'</p></div><div class="time-refs">'+t.refs.map(id=>'<a href="'+enc(byId[id]?.url||'#')+'" rel="noopener noreferrer" target="_blank">['+enc(id)+'] ↗</a>').join('')+'</div></article>').join('')||'<p class="no-results">Ei merkintöjä.</p>';}
document.querySelectorAll('#timeFilters .time-filter').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('#timeFilters .time-filter').forEach(x=>x.classList.toggle('active',x===b));renderTimelineRows(timeline,'timelineList',b.dataset.decade);}));
renderTimelineRows(timeline,'timelineList');
renderTimelineRows(schoolTimeline,'schoolTimelineList');
document.querySelectorAll('.school-time-filter').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.school-time-filter').forEach(x=>x.classList.toggle('active',x===b));renderTimelineRows(schoolTimeline,'schoolTimelineList',b.dataset.decade);}));
if(document.getElementById('courtArticle')){
const lawArticle=DATA.articles.find(x=>x.slug==='koulu-auktoriteetti-ja-oikeuden-kieli');
document.getElementById('courtArticle').innerHTML=lawArticle.paragraphs.map(p=>'<p>'+enc(p)+'</p>').join('');
}
if(document.getElementById('sourceSearch')){
const groupType=g=>g==='Katalogit'?'primary':g==='Oikeusuutiset'||g==='Aikalaisblogit'?'press':'open';
const sourceSearch=document.getElementById('sourceSearch'),sourceType=document.getElementById('sourceType');
function renderSources(){const q=sourceSearch.value.trim().toLowerCase(),type=sourceType.value;const hits=sources.filter(s=>(type==='all'||groupType(s.group)===type)&&[s.id,s.title,s.publisher,s.date,s.note].join(' ').toLowerCase().includes(q));document.getElementById('sourceCount').textContent=hits.length+' / '+sources.length+' LÄHDEVIITETTÄ';document.getElementById('sourceList').innerHTML=hits.map(s=>'<a class="source-entry" href="'+enc(s.url)+'" target="_blank" rel="noopener noreferrer"><span class="source-index">'+enc(s.id)+'</span><span class="source-date">'+enc(s.date)+'</span><div><h3>'+enc(s.title)+'</h3><p>'+enc(s.note)+'</p></div><span class="source-kind">'+enc(s.publisher)+'<br>↳ '+(groupType(s.group)==='primary'?'KIRJASTOLUETTELO':groupType(s.group)==='press'?'UUTISOINTI / AIKALAISBLOGI':'AVOIN TUTKIMUSPOLKU')+'</span><span class="source-link-arrow">↗</span></a>').join('')||'<p class="no-results">Lähteitä ei löytynyt näillä ehdoilla.</p>';}
sourceSearch.addEventListener('input',renderSources);sourceType.addEventListener('change',renderSources);renderSources();
}
const modal=document.getElementById('articleDialog');
function openArticle(which){const slug={tech:'teknologiaa-ennen-internetia',law:'koulu-auktoriteetti-ja-oikeuden-kieli',web:'kadonnut-kotisivu'}[which];const a=DATA.articles.find(x=>x.slug===slug);if(!a)return;const additional=which==='law'?'<p><strong>Vuoden 2007 jatkokäsittelyn tutkimuslisäys.</strong> Martti Hellström kirjoitti 23.5.2007 STT:n uutisen perusteella, että hovioikeus oli kumonnut aiemman ratkaisun menettelyvirheen vuoksi ja että Lohjan käräjäoikeudessa asiaa oli käsitelty uudelleen. Blogi mainitsee 1 200 euron sakot. Tämä on sekundäärinen aikalaiskertomus, ei alkuperäinen oikeuden ratkaisu. <a target="_blank" rel="noopener noreferrer" href="'+enc(byId.S11.url)+'">Avaa vuoden 2007 lähde ↗</a>.</p>':which==='tech'?'<p><strong>Myöhemmät julkaisulöydöt.</strong> Luetteloissa esiintyvät myös <em>Nuori sähkökokeilija</em> (1981) ja <em>PX-8 – Epsonin uusittu laitos</em> (1985). Vuoden 1990 MikroBITTI-ilmoitus yhdistää Olli Poroilan nimen ja Hyrsylän koulun. Yksittäiset teosmerkinnät eivät silti vahvista kaikkien vuosikymmenien henkilöllisyysketjua.</p>':'<p><strong>Arkistotutkimuksen raja.</strong> Internet Archive -haun avaaminen ei vahvista tallenteen olemassaoloa eikä sisältöä. <a href="https://web.archive.org/web/*/http://kotisivu.dnainternet.net/poroila/" target="_blank" rel="noopener noreferrer">Avaa hakuyritys ↗</a>.</p>';
document.getElementById('articleContent').innerHTML='<p class="article-label">'+enc(a.category)+'</p><h2>'+enc(a.title)+'</h2><p class="article-lead">'+enc(a.intro)+'</p><div class="article-body">'+a.paragraphs.map(p=>'<p>'+enc(p)+'</p>').join('')+additional+'</div><p class="ref-head">RAPORTIN LÄHTEET</p>'+a.refs.map(sourceLink).map(s=>'<div class="article-ref">'+s+'</div>').join('')+'<div class="article-disclaimer">Avoin lähdeselvitys: dokumentoituja väitteitä, tutkimusaukkoja ja fiktiivistä näkökulmaa ei pidä sekoittaa. Alkuperäisiä oikeuden ratkaisukappaleita ei tässä tutkimuksessa ole luettu.</div>';modal.showModal();modal.scrollTop=0;}
document.querySelectorAll('[data-article]').forEach(b=>b.addEventListener('click',()=>openArticle(b.dataset.article)));
document.getElementById('articleClose').addEventListener('click',()=>modal.close());
modal.addEventListener('click',e=>{if(e.target===modal)modal.close()});
const copy=document.getElementById('copyOriginal');if(copy)copy.addEventListener('click',async()=>{const addr='http://kotisivu.dnainternet.net/poroila/';try{await navigator.clipboard.writeText(addr);copy.textContent='KOPIOITU ✓';}catch{copy.textContent=addr;}});


document.querySelectorAll('[data-catalog-search]').forEach(input=>{const target=document.getElementById(input.dataset.catalogSearch);const entries=[...target.querySelectorAll('[data-catalog-item]')];const output=document.querySelector('[data-catalog-count="'+target.id+'"]');const update=()=>{const query=input.value.toLocaleLowerCase('fi').trim();let shown=0;entries.forEach(entry=>{entry.hidden=!entry.textContent.toLocaleLowerCase('fi').includes(query);if(!entry.hidden)shown++;});output.textContent=shown+' / '+entries.length+' merkintää';};input.addEventListener('input',update);update();});

document.body.dataset.legacyReady='true';
})();
