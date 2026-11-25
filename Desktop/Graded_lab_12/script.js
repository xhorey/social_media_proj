import { html, render } from 'https://esm.sh/htm/preact/standalone';
import {Square} from './Square.js';

function App() {
  let pokemonId = Math.floor(Math.random() * 1028);
  return html`<div>
  <h1>Pokemon Scroller starting from: ${pokemonId}</h1>
  <${Square} pokeId=${pokemonId}/>
  </div>`;
}

render(html`<${App} />`, document.body);

