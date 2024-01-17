import math


def cthulhu_round(fl: float, higher_is_better=True):
    if higher_is_better:
        return math.floor(fl)
    return math.ceil(fl)
