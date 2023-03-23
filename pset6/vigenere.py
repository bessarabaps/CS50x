from sys import argv
from cs50 import get_string

if len(argv) != 2:
    exit("Usage: python vigenere.py k")

if not argv[1].isalpha():
    exit("Usage: python vigenere.py k")

keyword = argv[1].lower()
plaintext = get_string("plaintext: ")
ciphertext = ""
d = 0

for s in plaintext:
    if s.isalpha():
        dkey = d % len(keyword)
        key = ord(keyword[dkey].lower())-97
        changing_latter = chr((ord(s.lower()) - 97 + key)%26 + 97)
        if s.isupper():
            ciphertext += changing_latter.upper()
        else:
            ciphertext += changing_latter
        d += 1
    else:
        ciphertext += s
print (f"ciphertext:", ciphertext)
