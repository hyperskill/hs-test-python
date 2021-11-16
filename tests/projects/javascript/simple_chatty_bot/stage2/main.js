const input = require('sync-input');

let botName = "Aid";
let birthYear = "2020";

console.log(`Hello! My name is ${botName}.
I was created in ${birthYear}.`);

let userName = input("Please, remind me your name.\n");

console.log(`What a great name you have, ${userName}!`);

