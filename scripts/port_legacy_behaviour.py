"""One-time extraction of original interactions without the hash page router.

The resulting src/assets/legacy.js is editable source, not a build artifact.
Run this only when intentionally refreshing it from the legacy reference.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'app.js').read_text(encoding='utf-8')

def between(start, end):
    return source[source.index(start):source.index(end)]

header = ''''use strict';
// Original controls, scoped to the elements present on each Eleventy page.
(() => {
const DATA=JSON.parse(document.getElementById('legacy-data').textContent);
const sources=DATA.sources;
const byId=Object.fromEntries(sources.map(s=>[s.id,s]));
const enc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const sourceLink=id=>{const s=byId[id];return s?'<a href="'+enc(s.url)+'" target="_blank" rel="noopener noreferrer">['+enc(s.id)+'] '+enc(s.title)+' ↗</a>':''};
const sourceLinks=refs=>refs.map(sourceLink).join('');
'''
board_data = '''const graph=JSON.parse(document.getElementById('graph-data').textContent);
const rotations=[-2,2,-3,4,-2,3,1,-2,1,-3,4,-4,3,2];
const nodeData=graph.nodes.map((n,i)=>({...n,sub:n.subtitle,x:n.position.x,y:n.position.y,text:n.description,notice:n.evidenceStatus,rot:rotations[i]}));
const edges=graph.edges.map(e=>[e.from,e.to,e.status]);
'''
board = between('function placeNodes()', 'const schoolTimeline=[')
timeline = between('function renderTimelineRows(', 'const lawArticle=')
timeline = timeline.replace("document.getElementById(mount).innerHTML=", "const target=document.getElementById(mount);if(!target)return;target.innerHTML=")
court = between('const lawArticle=', 'const groupType=')
sources = between('const groupType=', 'const modal=')
modal = between('const modal=', 'const copy=')
copy = between('const copy=', '/* Sivunäkymien reititys:')
copy = copy.replace("copy.addEventListener", "if(copy)copy.addEventListener")
catalog = between("document.querySelectorAll('[data-catalog-search]')", "window.addEventListener('hashchange'")
result = header
result += "if(document.getElementById('corkboard')){\n" + board_data
result += "const board=document.getElementById('corkboard'),holder=document.getElementById('boardNodes'),svg=document.getElementById('strings');\nlet chosen='olli',moving=null;\n" + board + '}\n'
result += 'const timeline=DATA.timeline,schoolTimeline=DATA.schoolTimeline;\n' + timeline
result += "if(document.getElementById('courtArticle')){\n" + court + '}\n'
result += "if(document.getElementById('sourceSearch')){\n" + sources + '}\n'
result += modal + copy + catalog + "\ndocument.body.dataset.legacyReady='true';\n})();\n"
(ROOT / 'src/assets/legacy.js').write_text(result, encoding='utf-8')
print('Extracted original board, timelines, source filters, article dialogs, copying and catalog search.')
