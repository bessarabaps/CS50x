
from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    list_a = set(a.split("\n"))
    list_b = set(b.split("\n"))

    return list_a & list_b


def sentences(a, b):
    """Return sentences in both a and b"""

    list_a = set(sent_tokenize(a))
    list_b = set(sent_tokenize(b))

    return list_a & list_b


def str_substrings(str, n):

    substrings = []

    for i in range(len(str)-n+1):
        substrings.append(str[i:i+n])

    return substrings

def substrings(a, b, n):

    substrings_a = set(str_substrings(a,n))
    substrings_b = set(str_substrings(b,n))

    return substrings_a & substrings_b

