# Objectives
> Implement simple component with a single prop
> Implement simple events in Preact to dynamically change the CSS of a page 
# Part 0: Look at the files

The project has 4 files (For now):
1. Week12_2Lab_GRADED.md: This file! All the steps of what to do for this lab
2. index.html: Basic HTML
3. style.css: Extremely basic CSS 
4. script.js: The JS file, with an App component and a render call, but almost nothing in that component

- [ ] Make a git project called Week12-2Lab_graded in your 320 subgroup
- [ ] Read ALL the instructions before starting to code
- [ ] Remember that both stamps are required for full marks
- [ ] Open the folder containing index.html in VS Code and look at the three code files.
- [ ] In script.js, you already have the Preact import line. If you start a live server, you should see Hello World.

## Some Helpful Reminders:
- `` `This is a ${i % 2 ? "even" : "odd"} number` ``: Template strings allow for a single variable/value/line of code to be parsed into a string
- `` html`HTM is specific to ${framework}` ``: Preact uses HTM, which is template strings with html written at the start
- `` return html`<section><${Thing} message="hi"/>`;`` Returning an instance of the `Thing` component
- ``render(html`<${App} />`, document.body);``: Render the `App` component into the body of the website
- `export function myFunc() { ...;`: makes the function myFunc available to be imported into another file
- `import { myFunc } from "./module_file.js"`: imports the function myFunc from the given filename

## Lab Task Summary: Starting from a random pokemon, scroll through pictures

This website will initially load a picture of a random pokemon, and will have left and right buttons that will scroll through the pokemon in order by ids. It will look something like this:
![[Pasted image 20261119104241.png|519]]

You are going to make a Square component and add some interactivity to that Square. If you do it right, you should be able to add a second Square once the first is working and they will behave independently

Because we are working with Preact as a module, you will **need** to use the Go Live option in VS Code to run a local server to see your page running correctly.
# Part 1: Making the Square component
First you'll make a Square component and write the HTM for a single square.
## Steps to complete:
- [ ] Make a new file `Square.js` and add the import line for preact
- [ ] Make a component called `Square`, and export it
- [ ] `Square` has 1 prop:
	- [ ] `pokeId`: an id between 1 and 1028 (inclusive)
- [ ] The HTM for `Square`:
	- [ ] is a section with the class "square"
	- [ ] contains a `button` with id "down" and the label "<"
	- [ ] contains an `img` element (for now make the src an empty string)
	- [ ] contains a `button` with id "up" and the label ">"
	- [ ] HINT: the < and > will be parsed as HTM unless you put them in template strings
- [ ] In the `App` component in `script.js`:
	- [ ] Create a variable for the starting pokemon ID with a random number between 1 and 1028
		- `Math.floor(Math.random() * max)` gives you a random integer between 0 and `max`, inclusive
	- [ ] Replace the Hello World text in `App` with:
		- [ ] An `h1` that says "Pokemon Scroller starting from: ID" where ID is the starting ID
		- [ ] a `Square` with the `pokeId` set to that starting Pokemon ID (It won't show a pokemon yet)
- [ ] **TEST YOUR CODE**
	- [ ] Check the browser to make sure a teal square with 2 buttons shows up

# Part 2: Make a Pokemon show up
Add a function **inside** the `Square` component

## Steps to complete:
- [ ] In the Square component function, **before** the return line, make a function that will return a valid url for a pokemon image using the prop pokeId.
	- A pokemon image url looks like this: `"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/ID.png"` where ID is the number between 1 and 1028
	- [ ] Update the `img` tag in the component to use this function to set the `src`
- [ ] **TEST YOUR CODE**:
	- [ ] Does a random pokemon show up each time you refresh?
- [ ] **GET A STAMP**: Before you move on:
	- If you add 1 the value of `pokeId` in `Square`, will that change the picture, the header text, or both? Why?
# Part 3:  
Now we make the buttons do something
## Steps to complete:
- [ ] In `Square.js`, add a click event to the `#down` button that does 2 things: it **decrements** the value of `pokeId` by 1, and then sets the `src` of the image to the pokemon url for that new value. (Use your helper function from Part 2 for that)
	- HINT: A click event in Preact looks like: `onClick=${e => ...}` 
	- [ ] use `e.target` to navigate the DOM from this `button` to the `img`. You could use `.parentElement`, `.children`, `.querySelector()` , or other tools!
	- NOTE: You do not need to handle the ID going below 1
- [ ] **TEST YOUR CODE**:
	- [ ] Click the < button. Does the displayed pokemon change?
	- [ ] Click it again just for fun. It should keep changing
- [ ] Repeat that first step for the `#up` button, but **incrementing** the value of `pokeId`
- [ ] **TEST YOUR CODE**:
	- [ ] Click the > button. Does the displayed pokemon change?
- [ ] **GET A STAMP**
	- [ ] How would you change the `Square` component so the user could type in an ID instead of just going up or down?

# Part OPTIONAL: Make a bunch of small Squares
If you have time, make a bunch of different pokemon at once
## Steps to complete:
- [ ] Update `Square` to take a second prop, `small`, and give it a default value of false
- [ ] A `Square` gets the class "small" when the prop `small` is true. That's in addition to the class "square"
	- HINT: Use a ternary statement here: `boolean ? valIfTrue : valIfFalse`
- [ ] **TEST YOUR CODE** 
	- [ ] Nothing should have changed because the default value is false
- [ ] In `App`, add 50 `Square`s instead of just 1. Use this syntax to create a bunch of the same components:
	- `Array(SIZE).fill(WHATEVER).map(ARROW FUNCTION THAT RETURNS A SQUARE COMPONENT)`
- [ ] The `Square` components should now each pass true for the prop `small` and should each pass their own random value for the prop `pokeId` instead of using the variable
	- (yes this ruins the header, but you're in the bonus exercise already so shhh)
- [ ] **TEST YOUR CODE**:
	- [ ] You should see a lot of different pokemon now

# Part 4: Code submission
## Steps to complete BY END OF LAB:
- [ ] add all modified files to the project
	- `git status`
	- `git add {filename}` or `git add .` or `git add -A`
	- `git status`
- [ ] Commit to git with a DETAILED message describing the work you did. It is recommended to write this message in a text editor first (you already have VS code open) and then copy/paste it into the terminal.
	- `git commit -m "Implementing..."`
- [ ] Push to main (or whatever branch you're working on)
	- `git push origin main`
## Steps to complete BEFORE NEXT CLASS:
- [ ] Complete and submit the self-assess form