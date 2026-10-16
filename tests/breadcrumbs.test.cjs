const test = require('node:test');
const assert = require('node:assert/strict');
const breadcrumbs = require('../lib/breadcrumbs.cjs');

test('the introduction is the Poroila owner, without duplicate ancestors', () => {
  assert.deepEqual(breadcrumbs('/olli-poroila/tuntemuksiani/', { title: 'Tuntemuksiani', parent: { label: 'Olli Poroila', url: '/olli-poroila/' } }), [
    { label: 'Etusivu', url: '/' }, { label: 'Poroila', url: '/olli-poroila/' }, { label: 'Tuntemuksiani', url: null },
  ]);
});
test('works belong to school and retain the work index as a parent', () => {
  assert.deepEqual(breadcrumbs('/teokset/T-001/', { title: 'Ignored title', work: { title: 'MUTANAAMIO' }, parent: { label: 'Oppilaiden teokset', url: '/teokset/' } }).map(item => item.label), ['Etusivu', 'Koulu', 'Teokset', 'MUTANAAMIO']);
});
test('person pages use their person name rather than a generic legacy page name', () => {
  assert.deepEqual(breadcrumbs('/tekijat/H-123/', { title: 'Henkilömerkintä — HYRSYLÄ / JÄLJET', person: { name: 'Aila Rantanen' }, parent: { label: 'Tekijät', url: '/tekijat/' } }).map(item => item.label), ['Etusivu', 'Koulu', 'Henkilöt ja tekijät', 'Aila Rantanen']);
});
test('home has no redundant trail; owner landing pages have no duplicate owner', () => {
  assert.deepEqual(breadcrumbs('/', { title: 'Etusivu' }), []);
  assert.deepEqual(breadcrumbs('/koulu/', { title: 'Pitkä otsikko', parent: { label: 'Etusivu', url: '/' } }).map(item => item.label), ['Etusivu', 'Koulu']);
});
test('source readers use original titles, not their already escaped document titles', () => {
  assert.deepEqual(breadcrumbs('/koulu/aineisto/DLC-1/', { title: 'X &amp; Y', source: { title: 'X & Y' }, parent: { label: 'Koulun aineisto', url: '/koulu/aineisto/' } }).map(item => item.label), ['Etusivu', 'Koulu', 'Koulun aineisto', 'X & Y']);
});
test('page headings use one taxonomy-based eyebrow and clean title', () => {
  assert.deepEqual(breadcrumbs.pageHeading('/olli-poroila/tuntemuksiani/', {title:'Tuntemuksiani',lead:'Ingressi'}), {title:'Tuntemuksiani',eyebrow:'Poroila',lead:'Ingressi'});
  assert.equal(breadcrumbs.pageHeading('/tekijat/H-123/', {title:'Aila Rantanen — HYRSYLÄ / JÄLJET | Historiallinen henkilömerkintä'}).title, 'Aila Rantanen');
  assert.equal(breadcrumbs.pageHeading('/', {title:'Etusivu'}), null);
});
