'use strict';
(async()=>{
const DATA=await import('./research-data.js');
const originals=DATA.sources;
const extras=[
{id:'S11',date:'23.5.2007',title:'Hyvä paha opettaja osa II — STT:n uutisen referaatti',publisher:'Martti Hellström / blogi',group:'Aikalaisblogit',url:'https://pedagogiikkaa.blogspot.com/2007/05/hyv-paha-opettaja-osa-ii.html',note:'Hellström selostaa STT:n uutisointia: Turun hovioikeus oli kumonnut aiemman ratkaisun käsittelyvirheen vuoksi ja uusi käräjäoikeuskäsittely uutisoitiin vuonna 2007. Alkuperäiset tuomioasiakirjat puuttuvat.'},
{id:'S12',date:'1981',title:'Nuori sähkökokeilija',publisher:'Kirjastotietue / JYKDOK',group:'Katalogit',url:'https://jyu.finna.fi/Record/keski.353652',note:'Infopress. Kirjastoluetteloon merkitty Olli Poroilan nimellä julkaistu sähkökokeilukirja.'},
{id:'S13',date:'1985',title:'PX-8 — Epsonin uusittu laitos',publisher:'Kansalliskirjasto / Arto',group:'Katalogit',url:'https://kansalliskirjasto.finna.fi/Record/arto.012683420',note:'I.D.E.A-lehden artikkelimerkintä, s. 14–15. Alkuperäisen artikkelin sisältöä ei ole kokonaisuudessaan tarkistettu.'},
{id:'S14',date:'1990',title:'MikroBITTI 2/1990 — Hyrsylän koulun nimellä esiintyvä ilmoitus',publisher:'RetroBitti / Isojako, digitoitu lehti',group:'Avoimet viitteet',url:'https://www.isojako.com/bitti/RetroBitti84_92/RetroBitti90_02.pdf',note:'Olli Poroilan nimellä julkaistussa tietokoneilmoituksessa mainitaan Hyrsylän koulu. Historiallisia yhteystietoja ei toisteta.'},
{id:'S15',date:'1980',title:'Taide 4/1980 — kirjoittajanimiosuma',publisher:'Taide-lehden numeroluettelo',group:'Avoimet viitteet',url:'https://taidelehti.fi/numerot/',note:'Taide-lehden numeroluettelossa esiintyy samanniminen kirjoittaja. Henkilöllisyysyhteys rehtoriin on selvittämättä.'},
{id:'S16',date:'1975',title:'Kekkosen kirjeaineiston tekstijäljennös',publisher:'Doria / kirjeaineisto',group:'Avoimet viitteet',url:'https://www.doria.fi/bitstream/handle/10024/9638/TMP.objres.4561.html?sequence=1',note:'Aholanvaaran koulun johtajaopettajana esiintyvän Olli Poroilan nimisen henkilön kirje. Yhteyttä Hyrsylän koulun rehtoriin ei ole varmennettu.'}
];
const sources=[...originals,...extras];
const byId=Object.fromEntries(sources.map(s=>[s.id,s]));
const enc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c]));
const nodeData=[
['olli','Olli Poroila','Henkilö / tutkimuksen kohde','Hyrsylän koulun rehtori',479,295,'person',['S06','S14'],'Vuoden 2005 STT-uutinen nimeää Poroilan Hyrsylän koulun rehtoriksi. Vuoden 1990 lehti-ilmoitus sisältää sekä Olli Poroilan että Hyrsylän koulun nimen. Tämä on tutkimuksen keskuskohde.','DOKUMENTOITU'],
['hellstrom','Martti Hellström','Henkilö / julkinen kirjoittaja','Blogikirjoituksia vuosilta 2006–2007',840,106,'person',['S08','S09','S11'],'Kirjoitti blogissaan Poroilasta vuonna 2006 ja referoi STT:n vuotta 2007 koskevaa uutista. Tämä osoittaa julkisen kirjoittaja–aihe-yhteyden, ei henkilökohtaista suhdetta.','JULKINEN AIKALAISKIRJOITUS'],
['kekkonen','Urho Kekkonen','Henkilö / arkiston vastaanottaja','Vuoden 1975 nimiosuma',42,120,'person',['S10','S16'],'Kekkosen kirjeaineistossa esiintyy Olli Poroilan nimi. Kirjeen kirjoittajan identtisyyttä Hyrsylän rehtoriin ei ole vahvistettu. Tämä kortti kuvaa dokumenttien yhteyttä, ei osoitettua henkilökohtaista suhdetta.','HENKILÖYHTEYS AVOIN'],
['letter','Vuoden 1975 kirje','Dokumentti / henkilöllisyys avoin','Aholanvaaran johtajaopettaja',262,100,'document',['S10','S16'],'Kirjetekstissä Olli Poroilan niminen kirjoittaja kertoo työstään Sallan Aholanvaaran koulussa. Vuoden 1975 kirje ei yksin todista hänen olevan sama kuin Hyrsylän rehtori.','AVOIN NIMIOSUMA'],
['website','Kadonnut kotisivu','Verkkojälki / avaamaton','dnainternet.net/poroila/',522,69,'open',['S08','S09'],'Hellström mainitsi 11.4.2006 uuden väliaikaisen kotisivun osoitteen. Sivuston sisältöä tai Internet Archiven arkistokopiota ei ole tässä vahvistettu.','ARKISTOSISÄLTÖ TARKISTAMATTA'],
['school','Hyrsylän koulu','Instituutio / työpaikka','Nummi-Pusula',858,319,'institution',['S06','S14'],'Vuoden 2005 oikeusuutinen sijoittaa Olli Poroilan Hyrsylän kouluun. Vuoden 1990 MikroBITTI-ilmoitus sisältää saman koulun nimen.','DOKUMENTOITU TYÖYHTEYS'],
['court','Lohjan käräjäoikeus','Instituutio / oikeusvaihe','Uutisoitu 2005 ja 2007',757,518,'institution',['S06','S11'],'STT:n vuoden 2005 uutinen kertoo käräjäoikeusratkaisusta. Vuoden 2007 jatkokäsittelystä on Hellströmin referaatti. Täydet oikeuden päätösasiakirjat pitää vielä hankkia.','UUTISOINTI / EI ALKUPERÄINEN TUOMIO'],
['appeal','Turun hovioikeus','Instituutio / muutoksenhaku','Menettelyvirhettä koskeva uutisreferointi',1014,522,'institution',['S11'],'Hellströmin 2007 blogikirjoitus referoi STT:n uutista hovioikeuden käsittelyvirheperusteisesta kumoamisesta. Yhteys on prosessuaalinen.','REFEROITU RATKAISU'],
['books','Tekniikkakirjat','Dokumentit / kirjastoluettelot','1974 · 1975 · 1980 · 1981',275,324,'document',['S01','S02','S03','S12'],'Finnassa on Olli Poroilan nimellä teoksia vuosilta 1974, 1975, 1980 ja 1981. Tekijäidentiteettien pitkäketju edellyttää vielä ristiintarkastelua.','JULKAISUTIETOJA'],
['finna','Finna / Doria','Instituutio / tiedon säilyttäjä','Kirja- ja kirjeviitteet',37,484,'institution',['S01','S02','S10'],'Kirjastotietueet ovat lähteitä, eivät osoitus henkilökohtaisesta yhteydestä kirjaston henkilöstöön.','LÄHDEINSTITUUTIO'],
['micro','MikroBITTI 1990','Dokumentti / digitoitu lehti','Hyrsylän koulun nimiosuma',288,563,'document',['S14'],'MikroBITTI-lehden tietokoneilmoituksessa mainitaan Olli Poroila sekä Hyrsylän koulu. Ilmoituksen sisältö tulee vielä varmistaa alkuperäiseltä lehtisivulta.','DOKUMENTOITU LEHTIJÄLKI'],
['stt','STT / uutisointi','Instituutio / uutislähde','2005 ja 2007',519,561,'institution',['S06','S07','S11'],'Vuoden 2005 uutinen julkaistiin MTV:ssä; Kaleva julkaisi saman STT-tekstin. Vuotta 2007 koskeva tieto on toisessa lähteessä referoitu STT-uutinen.','MEDIALÄHTEIDEN KETJU'],
['salla','Aholanvaaran koulu','Instituutio / mahdollinen työpaikka','Salla, kirje 1975',43,300,'institution',['S16'],'Vuoden 1975 kirjeessä samanniminen henkilö ilmoittaa työskennelleensä tämän koulun johtajaopettajana. Yhteys Hyrsylän rehtoriin on varmentamatta.','HENKILÖLLISYYS AVOIN'],
['taide','Taide 4/1980','Dokumentti / nimiosuma','Ammatti ilman ammattia',1052,167,'open',['S15'],'Kirjoittajaluettelossa esiintyy Olli Poroilan nimi. Alkuperäistä tekstiä tai identiteettiä ei ole täsmäytetty.','NIMIOSUMA']
].map(([id,name,label,sub,x,y,type,refs,text,notice],i)=>({id,name,label,sub,x,y,type,refs,text,notice,rot:[-2,2,-3,4,-2,3,1,-2,1,-3,4,-4,3,2][i]}));
const edges=[
['olli','hellstrom','solid'],['hellstrom','website','solid'],['olli','school','solid'],
['olli','court','solid'],['court','appeal','solid'],['court','stt','solid'],
['olli','books','open'],['books','finna','solid'],['school','micro','solid'],
['micro','olli','solid'],['olli','website','solid'],['kekkonen','letter','solid'],
['letter','salla','solid'],['letter','olli','open'],['olli','taide','open'],
['stt','hellstrom','solid']
];
const board=document.getElementById('corkboard'), holder=document.getElementById('boardNodes'),svg=document.getElementById('strings');
if(!board||!holder||!svg)throw Error('Korkkitaulun pohja puuttuu');
let chosen='olli',moving=null;
const sourceLink=id=>{const s=byId[id];return s?'<a href="'+enc(s.url)+'" target="_blank" rel="noopener noreferrer">['+enc(s.id)+'] '+enc(s.title)+' ↗</a>':''};
const sourceLinks=refs=>refs.map(sourceLink).join('');
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
const timeline=[...DATA.timeline.map(x=>({year:+x.year,title:x.title,description:x.text,refs:x.refs||[],open:x.open})),
 {year:1981,title:'Nuori sähkökokeilija',description:'Olli Poroilan nimellä kirjattu sähkökokeilukirja.',refs:['S12']},
 {year:1985,title:'Epson PX-8',description:'I.D.E.A-lehden artikkelimerkintä.',refs:['S13']},
 {year:1990,title:'MikroBITTI ja Hyrsylän koulu',description:'Nimen ja koulun yhdistävä alkuperäinen lehti-ilmoitus.',refs:['S14']},
 {year:2007,title:'Oikeusprosessin uutisoitu jatkovaihe',description:'Hellström referoi STT:n tietoja uudesta käsittelystä ja hovioikeuden käsittelyvirheen takia kumoamasta aiemmasta ratkaisusta. Ei alkuperäinen tuomio.',refs:['S11'],open:true}
].sort((a,b)=>a.year-b.year);
function renderTimeline(decade='all'){const matches=timeline.filter(t=>decade==='all'||String(t.year).startsWith(decade.slice(0,3)));document.getElementById('timelineList').innerHTML=matches.map(t=>'<article class="time-row '+(t.open?'open':'')+'"><div class="time-year">'+t.year+'</div><div class="time-dot"></div><div><p class="time-title">'+enc(t.title)+'</p><p class="time-summary">'+enc(t.description)+'</p></div><div class="time-refs">'+t.refs.map(id=>'<a href="'+enc(byId[id]?.url||'#')+'" rel="noopener noreferrer" target="_blank">['+enc(id)+'] ↗</a>').join('')+'</div></article>').join('')||'<p class="no-results">Ei merkintöjä.</p>';}
document.querySelectorAll('.time-filter').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.time-filter').forEach(x=>x.classList.toggle('active',x===b));renderTimeline(b.dataset.decade);}));
renderTimeline();
const groupType=g=>g==='Katalogit'?'primary':g==='Oikeusuutiset'||g==='Aikalaisblogit'?'press':'open';
const sourceSearch=document.getElementById('sourceSearch'),sourceType=document.getElementById('sourceType');
function renderSources(){const q=sourceSearch.value.trim().toLowerCase(),type=sourceType.value;const hits=sources.filter(s=>(type==='all'||groupType(s.group)===type)&&[s.id,s.title,s.publisher,s.date,s.note].join(' ').toLowerCase().includes(q));document.getElementById('sourceCount').textContent=hits.length+' / '+sources.length+' LÄHDEVIITETTÄ';document.getElementById('sourceList').innerHTML=hits.map(s=>'<a class="source-entry" href="'+enc(s.url)+'" target="_blank" rel="noopener noreferrer"><span class="source-index">'+enc(s.id)+'</span><span class="source-date">'+enc(s.date)+'</span><div><h3>'+enc(s.title)+'</h3><p>'+enc(s.note)+'</p></div><span class="source-kind">'+enc(s.publisher)+'<br>↳ '+(groupType(s.group)==='primary'?'KIRJASTOLUETTELO':groupType(s.group)==='press'?'UUTISOINTI / AIKALAISBLOGI':'AVOIN TUTKIMUSPOLKU')+'</span><span class="source-link-arrow">↗</span></a>').join('')||'<p class="no-results">Lähteitä ei löytynyt näillä ehdoilla.</p>';}
sourceSearch.addEventListener('input',renderSources);sourceType.addEventListener('change',renderSources);renderSources();
const modal=document.getElementById('articleDialog');
function openArticle(which){const slug={tech:'teknologiaa-ennen-internetia',law:'koulu-auktoriteetti-ja-oikeuden-kieli',web:'kadonnut-kotisivu'}[which];const a=DATA.articles.find(x=>x.slug===slug);if(!a)return;const additional=which==='law'?'<p><strong>Vuoden 2007 jatkokäsittelyn tutkimuslisäys.</strong> Martti Hellström kirjoitti 23.5.2007 STT:n uutisen perusteella, että hovioikeus oli kumonnut aiemman ratkaisun menettelyvirheen vuoksi ja että Lohjan käräjäoikeudessa asiaa oli käsitelty uudelleen. Blogi mainitsee 1 200 euron sakot. Tämä on sekundäärinen aikalaiskertomus, ei alkuperäinen oikeuden ratkaisu. <a target="_blank" rel="noopener noreferrer" href="'+enc(byId.S11.url)+'">Avaa vuoden 2007 lähde ↗</a>.</p>':which==='tech'?'<p><strong>Myöhemmät julkaisulöydöt.</strong> Luetteloissa esiintyvät myös <em>Nuori sähkökokeilija</em> (1981) ja <em>PX-8 – Epsonin uusittu laitos</em> (1985). Vuoden 1990 MikroBITTI-ilmoitus yhdistää Olli Poroilan nimen ja Hyrsylän koulun. Yksittäiset teosmerkinnät eivät silti vahvista kaikkien vuosikymmenien henkilöllisyysketjua.</p>':'<p><strong>Arkistotutkimuksen raja.</strong> Internet Archive -haun avaaminen ei vahvista tallenteen olemassaoloa eikä sisältöä. <a href="https://web.archive.org/web/*/http://kotisivu.dnainternet.net/poroila/" target="_blank" rel="noopener noreferrer">Avaa hakuyritys ↗</a>.</p>';
document.getElementById('articleContent').innerHTML='<p class="article-label">'+enc(a.category)+'</p><h2>'+enc(a.title)+'</h2><p class="article-lead">'+enc(a.intro)+'</p><div class="article-body">'+a.paragraphs.map(p=>'<p>'+enc(p)+'</p>').join('')+additional+'</div><p class="ref-head">RAPORTIN LÄHTEET</p>'+a.refs.map(sourceLink).map(s=>'<div class="article-ref">'+s+'</div>').join('')+'<div class="article-disclaimer">Avoin lähdeselvitys: dokumentoituja väitteitä, tutkimusaukkoja ja fiktiivistä näkökulmaa ei pidä sekoittaa. Alkuperäisiä oikeuden ratkaisukappaleita ei tässä tutkimuksessa ole luettu.</div>';modal.showModal();modal.scrollTop=0;}
document.querySelectorAll('[data-article]').forEach(b=>b.addEventListener('click',()=>openArticle(b.dataset.article)));
document.getElementById('articleClose').addEventListener('click',()=>modal.close());
modal.addEventListener('click',e=>{if(e.target===modal)modal.close()});
const copy=document.getElementById('copyOriginal');copy.addEventListener('click',async()=>{const addr='http://kotisivu.dnainternet.net/poroila/';try{await navigator.clipboard.writeText(addr);copy.textContent='KOPIOITU ✓';}catch{copy.textContent=addr;}});
const menu=document.getElementById('menuToggle'),nav=document.getElementById('navigation');menu.addEventListener('click',()=>{const visible=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(visible))});nav.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false')}));

/* Sivunäkymien reititys: GitHub Pages -yhteensopivat jaettavat hash-URL:t. */
const pageNames={alku:'Etusivu',kartta:'Yhteyskartta',aineisto:'Tutkintalinjat',hypoteesit:'Hypoteesit',aikajana:'Aikajana',fiktiot:'Fiktiiviset muistiinpanot',lahteet:'Lähteet'};
function showPage(){
  const raw=decodeURIComponent((location.hash||'').replace(/^#\/?/,'')).split('/')[0];
  const page=Object.prototype.hasOwnProperty.call(pageNames,raw)?raw:'alku';
  document.body.dataset.page=page;
  document.querySelectorAll('main > section').forEach(section=>{
    section.hidden=(section.id||'alku')!==page;
  });
  const breadcrumb=document.getElementById('pageTrail');
  breadcrumb.hidden=page==='alku';
  document.getElementById('currentPageName').textContent=pageNames[page].toUpperCase();
  document.querySelectorAll('#navigation a').forEach(link=>{
    if(link.getAttribute('href')==='#/'+page)link.setAttribute('aria-current','page');
    else link.removeAttribute('aria-current');
  });
  document.title=(page==='alku'?'POROILA / JÄLJET':pageNames[page]+' — POROILA / JÄLJET')+' | Tutkimusarkisto';
  if(modal.open)modal.close();
  window.scrollTo({top:0,behavior:'instant'});
  if(page==='kartta')requestAnimationFrame(lines);
}
window.addEventListener('hashchange',showPage);
showPage();
})().catch(e=>{console.error('Sivuston tietojen alustaminen epäonnistui',e);const el=document.getElementById('nodeDetail');if(el)el.textContent='Tutkimusaineiston lataaminen epäonnistui. Päivitä sivu ja tarkista verkkoyhteys.';});
