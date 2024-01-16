import re
from functools import reduce


def acronym(stng):
    words = re.findall(r"\b\w", stng)
    return reduce(lambda x, y: x + y, [word[0].upper() for word in words])
