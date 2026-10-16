module.exports = {
  original: require('./originalNavigation.json'),
  primary: [
    { id: 'alku', label: 'Alku', url: '/', prefixes: ['/'] },
    { id: 'sivujaljet', label: 'Verkkosivut', url: '/verkkoarkisto/sivujaljet/', prefixes: ['/verkkoarkisto/', '/tekijat/', '/teokset/'] },
    { id: 'koulu', label: 'Koulu ja ihmiset', url: '/koulu/', prefixes: ['/koulu/'] },
    { id: 'aineisto', label: 'Poroila', url: '/olli-poroila/kirjoitukset/', prefixes: ['/olli-poroila/'] },
    { id: 'fiktiot', label: 'Fiktio', url: '/fiktiot/', prefixes: ['/fiktiot/'] },
    { id: 'lahteet', label: 'Lähteet', url: '/lahteet/', prefixes: ['/lahteet/', '/tutkimus/'] },
  ],
  sections: [
    {
      label: 'Verkkoarkisto ja aineistokatalogi',
      prefixes: ['/verkkoarkisto/', '/tekijat/', '/teokset/'],
      links: [
        { label: 'Arkisto', url: '/verkkoarkisto/' },
        { label: 'Sivujäljet', url: '/verkkoarkisto/sivujaljet/' },
        { label: 'Tallenteet', url: '/verkkoarkisto/tallenteet/' },
        { label: 'Katalogi', url: '/verkkoarkisto/katalogi/' },
        { label: 'Alkuperäistiedostot', url: '/verkkoarkisto/alkuperaistiedostot/' },
        { label: 'Kuvat', url: '/verkkoarkisto/kuvat/' },
        { label: 'Tekijät', url: '/tekijat/', prefix: '/tekijat/' },
        { label: 'Teokset', url: '/teokset/', prefix: '/teokset/' },
      ],
    },
    {
      label: 'Koulun alasivut',
      prefixes: ['/koulu/'],
      links: [
        { label: 'Hyrsylän koulu', url: '/koulu/' },
        { label: 'Koulun aikajana', url: '/koulu/aikajana/' },
        { label: 'Koulun historia', url: '/koulu/historia/' },
        { label: 'Muistitieto', url: '/koulu/muistitieto/' },
        { label: 'Oppilastyöt', url: '/koulu/oppilastyot/' },
        { label: 'Yhteenveto', url: '/koulu/yhteenveto/' },
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
      prefixes: ['/tutkimus/'],
      links: [
        { label: 'Tutkimuksen tausta', url: '/tutkimus/' },
      ],
    },
  ],
};
