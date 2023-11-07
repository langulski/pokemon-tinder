var newCards = document.querySelectorAll('.tinder--card:not(.removed)');

const typeColor = {
    bug: "#26de81",
    dragon: "#ffeaa7",
    electric: "#fed330",
    fairy: "#FF0069",
    fighting: "#30336b",
    fire: "#f0932b",
    flying: "#81ecec",
    grass: "#00b894",
    ground: "#EFB549",
    ghost: "#a55eea",
    ice: "#74b9ff",
    normal: "#95afc0",
    poison: "#6c5ce7",
    psychic: "#a29bfe",
    rock: "#2d3436",
    water: "#0190FF",
  };


newCards.forEach(function (card, index) {
    const cardType = card.querySelector('.invisible-p').innerText;
    const colorType = typeColor[cardType];
    card.style.background = `radial-gradient(circle at 50% 0%, ${colorType} 36%, #ffffff 36%)`;
    card.querySelectorAll('.stats div p').forEach((p) => {
      p.style.backgroundColor = colorType;
  });
  });