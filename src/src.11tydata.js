module.exports = {
  eleventyComputed: {
    features(data) {
      const page = data.legacyPage;
      if (!page) return data.page.url === '/verkkoarkisto/alkuperaistiedostot/' ? ['archive'] : [];
      return {
        alku: ['copy'], aineisto: ['articles'], kartta: ['board'],
        aikajana: ['timeline'], kouluaikajana: ['timeline'], lahteet: ['sources'],
        katalogi: ['catalog'], henkilot: ['catalog'], tuotokset: ['catalog'], kuvat: ['catalog'],
      }[page] || [];
    },
  },
};
