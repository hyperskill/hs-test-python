water = 400
milk = 540
beans = 120
cups = 9
money = 550

def machine_status():
    print(f'''The coffee machine has:
    {water} of water
    {milk} of milk
    {beans} of coffee beans
    {cups} of disposable cups
    {money} of money''')

machine_status()

action = input("Write action (buy, fill, take):\n")

if action == 'buy':
    typ = int(input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n"))
    if typ == 1:
        water -= 250
        beans -= 16
        money += 4
        cups -= 1
    elif typ == 2:
        water -= 350
        milk -= 75
        beans -= 20
        money += 7
        cups -= 1
    else:
        water -= 200
        milk -= 100
        beans -= 12
        money += 6
        cups -= 1
elif action == 'fill':
    water += int(input("Write how many ml of water do you want to add:\n"))
    milk += int(input("Write how many ml of milk do you want to add:\n"))
    beans += int(input("Write how many grams of coffee beans do you want to add:\n"))
    cups += int(input("Write how many disposable cups of coffee do you want to add:\n"))
elif action == 'take':
    print(f"I gave you ${money}")
    money = 0

machine_status()

""" s_water = int(input("Write how many ml of water the coffee machine has:\n"))
s_milk = int(input("Write how many ml of milk the coffee machine has:\n"))
s_beans = int(input("Write how many grams of coffee beans the coffee machine has:\n"))

cups_max = min([(s_water // 200), (s_milk // 50), (s_beans // 15)])
cups = int(input("Write how many cups of coffee you will need:\n"))

if cups_max == cups:
    print("Yes, I can make that amount of coffee")
elif cups_max > cups:
    print(f"Yes, I can make that amount of coffee (and even {cups_max - cups} more than that)")
else:
    print(f"No, I can make only {cups_max} cups of coffee") """