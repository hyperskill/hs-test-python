const prompt = require('prompt-sync');

var money  = 550;
var water  = 400;
var milk   = 540;
var beans  = 120;
var cups   = 9;

function printState() {
	console.log("The coffee machine has:")
	console.log(
		water + " of water \n" +
		milk + " of milk \n" +
		beans + " of coffee beans \n" +
		cups + " of disposable cups \n" +
		money + " of money")
}

function takeMoney() {
	console.log("I gave you $" + money)
	money = 0
}

function sellCoffee() {
	let choice = prompt("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino: ")
	if (choice == '1') {
		console.log(123)
		money += 4
		water -= 250
		beans -= 16
		cups -= 1
	}
	else if (choice == '2') {
		money += 7
		water -= 350
		milk -= 75
		beans -= 20
		cups -= 1
	}
	else if (choice == '3') {
		money += 6
		water -= 200
		milk -= 100
		beans -= 12
		cups -= 1
	} else {
		console.log(234)
	}
}

function fillMachine() {
	water += Number(prompt("Write how many ml of water do you want to add: "))
	milk += Number(prompt("Write how many ml of milk do you want to add: "))
	beans += Number(prompt("Write how many grams of coffee beans do you want to add: "))
	cups += Number(prompt("Write how many disposable cups of coffee do you want to add: "))
}

printState();

action = prompt("Write action (buy, fill, take): ");

if (action === 'buy') {
	sellCoffee()
} else if (action === 'fill') {
	fillMachine()
} else if (action === "take") {
	takeMoney()
}

printState();
