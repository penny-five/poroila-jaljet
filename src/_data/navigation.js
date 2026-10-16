const schoolSections = require('./schoolSections.json');
const schoolCollections = [
  { label: 'Aineiston alku', url: '/koulu/aineisto/', prefix: '/koulu/aineisto/' },
  { label: 'Koulukuvat ja kuvataide', url: '/koulu/koulukuvat/', prefix: '/koulu/koulukuvat/' },
  ...schoolSections.map(section => ({ label: section.title, url: `/koulu/${section.slug}/`, prefix: `/koulu/${section.slug}/` })),
  { label: 'Henkilöt ja tekijät', url: '/tekijat/', prefix: '/tekijat/' },
  { label: 'Teoskatalogi', url: '/teokset/', prefix: '/teokset/' },
];

module.exports = {
  original: require('./originalNavigation.json'),
  primary: [
    { id: 'alku', label: 'Etusivu', url: '/', prefixes: ['/'] },
    { id: 'koulu', label: 'Koulu', url: '/koulu/', prefixes: ['/koulu/', '/tekijat/', '/teokset/'] },
    { id: 'aineisto', label: 'Poroila', url: '/olli-poroila/', prefixes: ['/olli-poroila/'] },
    { id: 'sivujaljet', label: 'Verkkoarkisto', url: '/verkkoarkisto/', prefixes: ['/verkkoarkisto/'] },
    { id: 'lahteet', label: 'Lähteet ja tutkimus', url: '/lahteet/', prefixes: ['/lahteet/', '/tutkimus/', '/fiktiot/'] },
  ],
  collections: [
    {
      label: 'Koulun aineistoryhmät',
      home: { label: 'Koulun aineisto', url: '/koulu/aineisto/' },
      prefixes: schoolCollections.map(item => item.prefix),
      links: schoolCollections,
    },
  ],
  sections: [
    {
      label: 'Verkkoarkisto ja aineistokatalogi',
      prefixes: ['/verkkoarkisto/'],
      links: [
        { label: 'Arkisto', url: '/verkkoarkisto/' },
        { label: 'Sivujäljet', url: '/verkkoarkisto/sivujaljet/' },
        { label: 'Tallenteet', url: '/verkkoarkisto/tallenteet/' },
        { label: 'Katalogi', url: '/verkkoarkisto/katalogi/' },
        { label: 'Alkuperäistiedostot', url: '/verkkoarkisto/alkuperaistiedostot/' },
        { label: 'Kuvaviitteet', url: '/verkkoarkisto/kuvat/' },
      ],
    },
    {
      label: 'Koulun alasivut',
      prefixes: ['/koulu/', '/tekijat/', '/teokset/'],
      links: [
        { label: 'Hyrsylän koulu', url: '/koulu/' },
        { label: 'Koulun aineisto', url: '/koulu/aineisto/', prefixes: schoolCollections.map(item => item.prefix) },
        { label: 'Koulun historia', url: '/koulu/historia/' },
        { label: 'Aikajana', url: '/koulu/aikajana/' },
        { label: 'Muistitieto', url: '/koulu/muistitieto/' },
        { label: 'Myöhemmät vaiheet', url: '/koulu/myohemmat-vaiheet/' },
      ],
    },
    {
      label: 'Olli Poroilan alasivut',
      prefixes: ['/olli-poroila/'],
      links: [
        { label: 'Poroilan esittely', url: '/olli-poroila/' },
        { label: 'Aikajana', url: '/olli-poroila/aikajana/' },
        { label: 'Tuntemuksiani', url: '/olli-poroila/tuntemuksiani/' },
        { label: 'Kirjoitukset ja lähteet', url: '/olli-poroila/kirjoitukset/' },
        { label: 'Oikeusprosessi', url: '/olli-poroila/oikeus/' },
        { label: 'Dokumentoidut yhteydet', url: '/olli-poroila/kartta/' },
        { label: 'Avoimet hypoteesit', url: '/olli-poroila/hypoteesit/' },
      ],
    },
    {
      label: 'Tutkimussivut',
      prefixes: ['/lahteet/', '/tutkimus/', '/fiktiot/'],
      links: [
        { label: 'Lähdeluettelo', url: '/lahteet/' },
        { label: 'Tutkimuksen tausta', url: '/tutkimus/' },
        { label: 'Fiktiiviset muistiinpanot', url: '/fiktiot/' },
      ],
    },
  ],
};
