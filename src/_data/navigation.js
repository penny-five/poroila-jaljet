module.exports = {
  primary: [
    { label: 'Alku', url: '/', prefixes: ['/'] },
    { label: 'Verkkosivut', url: '/verkkoarkisto/sivujaljet/', prefixes: ['/verkkoarkisto/', '/tekijat/', '/teokset/'] },
    { label: 'Koulu ja ihmiset', url: '/koulu/', prefixes: ['/koulu/', '/tekijat/myohemmat-vaiheet/'] },
    { label: 'Poroila', url: '/olli-poroila/', prefixes: ['/olli-poroila/'] },
    { label: 'Fiktio', url: '/fiktiot/', prefixes: ['/fiktiot/'] },
    { label: 'Lähteet', url: '/lahteet/', prefixes: ['/lahteet/', '/tutkimus/'] },
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
      prefixes: ['/koulu/', '/tekijat/myohemmat-vaiheet/'],
      links: [
        { label: 'Hyrsylän koulu', url: '/koulu/' },
        { label: 'Koulun aikajana', url: '/koulu/aikajana/' },
        { label: 'Koulun historia', url: '/koulu/historia/' },
        { label: 'Muistitieto', url: '/koulu/muistitieto/' },
        { label: 'Oppilastyöt', url: '/koulu/oppilastyot/' },
        { label: 'Yhteenveto', url: '/koulu/yhteenveto/' },
        { label: 'Myöhemmät vaiheet', url: '/tekijat/myohemmat-vaiheet/' },
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
      ],
    },
    {
      label: 'Tutkimussivut',
      prefixes: ['/tutkimus/'],
      links: [
        { label: 'Tutkimuksen tausta', url: '/tutkimus/' },
        { label: 'Dokumentoidut yhteydet', url: '/tutkimus/kartta/' },
        { label: 'Avoimet hypoteesit', url: '/tutkimus/hypoteesit/' },
      ],
    },
  ],
};
