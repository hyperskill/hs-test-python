const input = require('sync-input');

const greet = (botName, birthYear)  => {
    console.log(`Hello! My name is ${botName}.
I was created in ${birthYear}.`);
};

const remindName = () => {
    let userName = input("Please, remind me your name.\n");
    console.log(`What a great name you have, ${userName}!`);
};

const guessAge = () => {
    console.log(`Let me guess your age.
Enter remainders of dividing your age by 3, 5 and 7.`);
   let remainder3 = Number(input());
   let remainder5 = Number(input());
   let remainder7 = Number(input());

   let userAge = (remainder3 * 70 + remainder5 * 21 + remainder7 * 15) % 105;
    console.log(`Your age is ${userAge}; that's a good time to start programming!`);
};

const count = () => {
    console.log("Now I will prove to you that I can count to any number you want.");

   let number = Number(input());
   let current = 0;

    while (current <= number) {
        console.log(current + " !");
        current += 1;
    }

};

const testSkills = () => {
    console.log("Let's test your programming knowledge.")

    while (true) {
        let question = Number(input(`Why do we use methods?
        1. To repeat a statement multiple times.
        2. To decompose a program into several small subroutines.
        3. To determine the execution time of a program.
        4. To interrupt the execution of a program.`))

        if (question === 2) {
            console.log('Completed, have a nice day!')
            break
        } else
            console.log("Please, try again.")
    }
};

const endProgram = () => {
    console.log('Congratulations, have a nice day!');
};

const main = () => {
    let botName = "Aid";
    let birthYear = "2020";

    greet(botName, birthYear);
    remindName();
    guessAge();
    count();
    testSkills();
    endProgram();
};

main();












