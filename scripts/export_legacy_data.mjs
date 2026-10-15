import fs from 'node:fs';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const sourcePath = new URL('app.js', root);
const source = fs.readFileSync(sourcePath, 'utf8');
const research = await import(new URL('research-data.js', root));

const extrasStart = source.indexOf('const extras=[');
const lookupStart = source.indexOf('const byId=', extrasStart);
if (extrasStart < 0 || lookupStart < 0) throw new Error('Legacy source registry boundary not found');
const extrasBlock = source.slice(extrasStart, lookupStart).replace('const extras=', 'let extras=');
const extraSources = vm.runInNewContext(`${extrasBlock}\nextras`, { originals: research.sources });

function getArrayBetween(startMarker, endMarker, variable, context = {}) {
  const start = source.indexOf(startMarker);
  if (start < 0) throw new Error(`Legacy data block missing: ${startMarker}`);
  const end = source.indexOf(endMarker, start);
  if (end < 0) throw new Error(`Legacy data block terminator missing: ${endMarker}`);
  return vm.runInNewContext(`${source.slice(start, end + endMarker.length)}\n${variable}`, context);
}

const schoolTimeline = getArrayBetween('const schoolTimeline=[', '].sort((a,b)=>a.year-b.year);', 'schoolTimeline');
const timeline = getArrayBetween('const timeline=[', '].sort((a,b)=>a.year-b.year);', 'timeline', { DATA: research });
const sources = [...research.sources, ...extraSources];
const ids = new Set();
for (const item of sources) {
  if (ids.has(item.id)) throw new Error(`Duplicate source ID: ${item.id}`);
  ids.add(item.id);
}

const outputPath = new URL('../src/_data/research.json', import.meta.url);
fs.mkdirSync(new URL('../src/_data/', import.meta.url), { recursive: true });
const navigationStart = source.indexOf('const pageNames=');
const navigationEnd = source.indexOf('function showPage()', navigationStart);
const navigation = vm.runInNewContext(`${source.slice(navigationStart, navigationEnd)}\n({names: pageNames, groups: pageGroups})`);
fs.writeFileSync(outputPath, `${JSON.stringify({ sources, timeline, schoolTimeline, articles: research.articles, navigation }, null, 2)}\n`);
console.log(`Exported ${sources.length} sources, ${timeline.length} Poroila timeline rows, ${schoolTimeline.length} school timeline rows, and ${research.articles.length} articles.`);
