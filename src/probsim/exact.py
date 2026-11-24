"""Exact probabilities as Fractions, by counting or combinatorics."""
from fractions import Fraction
from math import comb


def dice_sum(n: int, total: int, sides: int = 6) -> Fraction:
    """P(sum of n fair dice = total), by counting every way the sum can arise."""
    ways = {0: 1}
    for _ in range(n):
        new: dict[int, int] = {}
        for s, c in ways.items():
            for face in range(1, sides + 1):
                new[s + face] = new.get(s + face, 0) + c
        ways = new
    return Fraction(ways.get(total, 0), sides ** n)


def at_least_one_six(n: int) -> Fraction:
    """P(at least one six in n rolls) = 1 - (5/6)^n."""
    return 1 - Fraction(5, 6) ** n


def coins(n: int, k: int) -> Fraction:
    """P(exactly k heads in n fair coin tosses) = C(n,k) / 2^n."""
    if k < 0 or k > n:
        return Fraction(0)
    return Fraction(comb(n, k), 2 ** n)


def hypergeometric(pop: int, good: int, draws: int, k: int) -> Fraction:
    """P(exactly k good items when drawing `draws` from `pop` without replacement)."""
    if k < 0 or k > good or draws - k > pop - good or draws - k < 0:
        return Fraction(0)
    return Fraction(comb(good, k) * comb(pop - good, draws - k), comb(pop, draws))


def aces(draws: int, k: int) -> Fraction:
    """P(exactly k aces in `draws` cards from a 52 card deck)."""
    return hypergeometric(52, 4, draws, k)


def same_suit(draws: int) -> Fraction:
    """P(all `draws` cards are of one suit), drawing without replacement."""
    return 4 * Fraction(comb(13, draws), comb(52, draws))


def birthday(people: int, days: int = 365) -> Fraction:
    """P(at least two of `people` share a birthday), ignoring 29 February."""
    if people > days:
        return Fraction(1)
    none = Fraction(1)
    for i in range(people):
        none *= Fraction(days - i, days)
    return 1 - none
