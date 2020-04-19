from random import randint, seed

# Functions that deal with randomness
def set_seed(value: str):
    seed(a=value, version=2)


def roll(d: int):
    return randint(1, d)


def roll_no_min(d: int):
    if d == 1:
        return 1
    
    r = roll(d)

    # Reroll 1s
    while r == 1:
        r = roll(d)

    return r