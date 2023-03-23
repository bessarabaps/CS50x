from sys import argv
from cs50 import get_string


if len(argv) != 2:
    exit("Usage: python caesar.py k")

if int(argv[1]) < 0:
    exit("Usage: python caesar.py k")

key = int(argv[1])
plaintext = get_string("plaintext: ")
ciphertext = ""

for s in plaintext:
    if s.isalpha():
        changing_latter = chr((ord(s.lower()) - 97 + key)%26 + 97)
        if s.isupper():
            ciphertext += changing_latter.upper()
        else:
            ciphertext += changing_latter
    else:
        ciphertext += s
print (f"ciphertext:", ciphertext)

