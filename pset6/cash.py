from cs50 import get_float

while True:

    dollars = get_float("Change owed,$: ")

    if dollars > 0:
        break

cents = dollars * 100
coins = 0

while cents > 0:
    if cents >= 25:
        coins += 1
        cents -= 25

    elif cents >= 10:
        coins += 1
        cents -= 10

    elif cents >= 5:
        coins += 1
        cents -= 5

    elif cents >= 1:
        coins += 1
        cents -= 1
print(coins);