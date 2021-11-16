const input = require('sync-input');

let botName = "Aid";
let birthYear = "2020";

console.log(`Hello! My name is ${botName}.
I was created in ${birthYear}.`);

let userName = input("Please, remind me your name.\n");

console.log(`What a great name you have, ${userName}!`);

console.log(`Let me guess your age.
Enter remainders of dividing your age by 3, 5 and 7.`);

let remainder3 = Number(input());
let remainder5 = Number(input());
let remainder7 = Number(input());

let userAge = (remainder3 * 70 + remainder5 * 21 + remainder7 * 15) % 105;
console.log(`Your age is ${userAge}; that's a good time to start programming!`);

console.log("Now I will prove to you that I can count to any number you want.");

let number = Number(input());

for (let i = 0; i <= number; i++) {
    console.log(i + " !");
}

console.log('Completed, have a nice day!');
