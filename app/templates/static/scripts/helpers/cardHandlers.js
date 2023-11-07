import {saveLikedCard } from './apiHandlers.js';


export var tinderContainer = document.querySelector('.tinder');
export var allCards = document.querySelectorAll('.tinder--card');

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


export function handleCardInteractions(el) {
    var hammertime = new Hammer(el);
    var moveOutWidth = document.body.clientWidth;
  
    function onPan(event) {
        el.classList.add('moving');
  
        if (event.deltaX === 0) return;
        if (event.center.x === 0 && event.center.y === 0) return;
  
        tinderContainer.classList.toggle('tinder_love', event.deltaX > 0);
        tinderContainer.classList.toggle('tinder_nope', event.deltaX < 0);
  
        var xMulti = event.deltaX * 0.03;
        var yMulti = event.deltaY / 80;
        var rotate = xMulti * yMulti;
  
        event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';
    }
  
    function onPanEnd(event) {
        el.classList.remove('moving');
        tinderContainer.classList.remove('tinder_love');
        tinderContainer.classList.remove('tinder_nope');
  
        var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;
  
        event.target.classList.toggle('removed', !keep);
        const cardId = el.querySelector('.invisible-id').innerText;
  
        if (!keep && event.deltaX > 0) {
          
          saveLikedCard(cardId,true);
        } else if (!keep && event.deltaX < 0){
          saveLikedCard(cardId,false);
        }
  
        if (keep) {
            event.target.style.transform = '';
        } else {
            var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
            var toX = event.deltaX > 0 ? endX : -endX;
            var endY = Math.abs(event.velocityY) * moveOutWidth;
            var toY = event.deltaY > 0 ? endY : -endY;
            var xMulti = event.deltaX * 0.03;
            var yMulti = event.deltaY / 80;
            var rotate = xMulti * yMulti;
  
            event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';
            initCards();
  
        }
    }
  
    hammertime.on('pan', onPan);
    hammertime.on('panend', onPanEnd);
  }

  export function initCards(card, index) {
    var newCards = document.querySelectorAll('.tinder--card:not(.removed)');
  
    newCards.forEach(function (card, index) {
      const cardType = card.querySelector('.invisible-p').innerText;
      const colorType = typeColor[cardType];
      card.style.zIndex = allCards.length - index;
      card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
      card.style.opacity = (10 - index) / 10;
      card.style.background = `radial-gradient(circle at 50% 0%, ${colorType} 36%, #ffffff 36%)`;
      card.querySelectorAll('.stats div p').forEach((p) => {
        p.style.backgroundColor = colorType;
    });
    });
    
    tinderContainer.classList.add('loaded');
  }