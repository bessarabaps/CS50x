from cs50 import get_int

while True:

    number = get_int("Card number: ")

    if number > 0:
        break

x1 = number
x1sum = 0

while x1 > 0:

    x1sum += int(x1 % 10)
    x1 = int(x1 / 100)

x2 = int(number/10)
x2sum = 0

while x2 > 0:

    if 2 * (x2 % 10) > 9:
        x2sum += int((2 * (x2 % 10)) / 10)
        x2sum += int((2 * (x2 % 10)) % 10)
    else:
        x2sum += int(2 * (x2 % 10))

    x2 = int(x2 / 100)

sum = x1sum + x2sum;

if int(sum) % 10 == 0:

    if (number >= 340000000000000 and number < 350000000000000) or (number >= 370000000000000 and number < 380000000000000):

        print("AMEX")

    elif number >= 5100000000000000 and number < 5600000000000000:

        print("MASTERCARD")

    elif (number >= 4000000000000 and number < 5000000000000) or (number >= 4000000000000000 and number < 5000000000000000):

        print("VISA")

    else:

         print("INVALID")

else:
    print("INVALID")

