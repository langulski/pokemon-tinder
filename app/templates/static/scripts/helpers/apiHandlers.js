import {handleCardInteractions, initCards} from './cardHandlers.js';
export function saveLikedCard(cardId,loveCard) {
    fetch('/save_liked_card', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: cardId,
            love:loveCard,
        }),
    })
    .then((response) => response.json())
    .catch((error) => {
        console.error('Error saving liked card: ', error);
    });
  }


  export function loadAndApplyCards() {
    fetch('/get_more_cards')
        .then(response => response.json())
        .then(data => {
            const newCards = data.cards;
            const cardContainer = document.querySelector('.tinder--cards');
            newCards.forEach(card => {
                const cardDiv = document.createElement('div');
                cardDiv.classList.add('tinder--card');
                cardDiv.innerHTML = `
                <p class="hp">
                <span>HP</span>
                ${card.hp}
              </p>
              <img src="${ card.img_url }" />
              <h2 class="poke-name">${ card.name }</h2>
              <div class="types"></div>
              <div class="stats">
                <div>
                  <h3>${card.attack}</h3>
                  <p>Attack</p>
                </div>
                <div>
                  <h3>${card.defense}</h3>
                  <p>Defense</p>
                </div>
                <div>
                  <h3>${card.speed}</h3>
                  <p>Speed</p>
                </div>
              </div>
              <p>${ card.description }</p>
              <p class="invisible-p" style="display: none">${ card.type_1 }</p>
              <p class="invisible-id" style="display: none">${ card.id }</p>
                `;
                cardContainer.appendChild(cardDiv);
                handleCardInteractions(cardDiv);
            });
            initCards();
        })
        .catch(error => {
            console.error('Error loading more cards: ', error);
        });
  }