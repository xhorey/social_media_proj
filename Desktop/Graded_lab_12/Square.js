import { html, render } from 'https://esm.sh/htm/preact/standalone';
let x ="<";
let y =">";
export function Square({pokeId}){
    function url(pokeId){return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"+ pokeId +".png"}
    return html `<section class="square">
    <button id="down" onClick=${e => {
        pokeId--;
        const imgElement = document.querySelector("img");
        const h1Element = document.querySelector("h1");
        imgElement.setAttribute('src', url(pokeId));
        h1Element.textContent = "Pokemon Scroller starting from: " + pokeId;
    }}>${x}</button>
    <img src="${url(pokeId)}" alt="Pokemon image"/>
    <button id="up" onClick=${e => {
        pokeId++;
        const imgElement = document.querySelector("img");
        const h1Element = document.querySelector("h1");
        imgElement.setAttribute('src', url(pokeId));
        h1Element.textContent = "Pokemon Scroller starting from: " + pokeId;
    }}>${y}</button>
    </section>`
}