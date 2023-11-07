import {saveLikedCard,loadAndApplyCards } from './helpers/apiHandlers.js';
import {handleCardInteractions, initCards,allCards,} from './helpers/cardHandlers.js';

'use strict';



var nope = document.getElementById('nope');
var love = document.getElementById('love');


initCards();

allCards.forEach(function (el) {
  handleCardInteractions(el);
});

function createButtonListener(love) {
  return function (event) {
    var cards = document.querySelectorAll('.tinder--card:not(.removed)');
    var moveOutWidth = document.body.clientWidth * 1.5;

    if (!cards.length) return false;

    var card = cards[0];

    card.classList.add('removed');
    const cardId = card.querySelector('.invisible-id').innerText;

    if (love) {
      card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
      saveLikedCard(cardId,true);

    } else {
      card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
      saveLikedCard(cardId,false);
    }

    initCards();

    event.preventDefault();
  };
}

var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);

nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);


function loadAndApplyCardsLoop() {

  const removedCards = document.querySelectorAll('.tinder--card.removed');
  if (removedCards.length > 2) {
      loadAndApplyCards();
      $('.tinder--card.removed').remove();
  }
 setTimeout(loadAndApplyCardsLoop, 1000);
}

loadAndApplyCardsLoop();


