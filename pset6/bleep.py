from cs50 import get_string
from sys import argv

banned = []

def main():

    if len(argv) != 2:
        exit("Usage: python bleep.py dictionary")


    file = open(argv[1])
    for line in file:
        banned.append(line.strip("\n"))

    plaintext = get_string("What message would you like to censor?\n")


    for s in plaintext:
        if not s.isalpha() and s !=" ":

            exit("Usage: python bleep.py dictionary")

    text = plaintext.split(" ")
    resault = ""
    cword = ""

    for word in text:
        coincidence = False
        for bword in banned:
            if len(word) == len(bword):
                for c in range(len(word)):
                    if word[c].lower() == bword[c].lower():
                        coincidence = True
                    else:
                        coincidence = False
                        break
            if coincidence == True:
                break
            else:
                coincidence == False
        if coincidence == False:
            resault += word + " "
        else:
            for q in range(len(word)):
                cword += "*"
            resault += cword + " "
            cword = ""

    print (resault[:-1])

if __name__ == "__main__":
    main()
