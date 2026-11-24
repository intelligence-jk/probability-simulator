"""Seeded Monte Carlo estimates with a 95 percent Wilson interval."""
import random
from math import sqrt
from typing import Callable

Z95 = 1.959963984540054


def wilson(successes: int, trials: int, z: float = Z95) -> tuple[float, float]:
    """95 percent Wilson score interval for a proportion."""
    if trials == 0:
        return (0.0, 1.0)
    p = successes / trials
    d = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / d
    half = z * sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def estimate(trial: Callable[[random.Random], bool], trials: int, seed: int = 1):
    """Run `trials` seeded trials. Returns (estimate, low, high)."""
    rng = random.Random(seed)
    hits = sum(1 for _ in range(trials) if trial(rng))
    lo, hi = wilson(hits, trials)
    return hits / trials, lo, hi


def convergence(trial, steps=(10, 100, 1000, 10000, 100000), seed: int = 1):
    """One running seeded stream, reported at each size in `steps`."""
    rng = random.Random(seed)
    hits = done = 0
    rows = []
    for target in steps:
        while done < target:
            hits += bool(trial(rng))
            done += 1
        lo, hi = wilson(hits, done)
        rows.append((done, hits / done, lo, hi))
    return rows


# One-trial samplers

def t_dice_sum(n: int, total: int, sides: int = 6):
    return lambda r: sum(r.randint(1, sides) for _ in range(n)) == total


def t_at_least_one_six(n: int):
    return lambda r: any(r.randint(1, 6) == 6 for _ in range(n))


def t_coins(n: int, k: int):
    return lambda r: sum(r.random() < 0.5 for _ in range(n)) == k


def _deck():
    return [(rank, suit) for suit in range(4) for rank in range(13)]  # rank 0 = ace


def t_aces(draws: int, k: int):
    deck = _deck()
    return lambda r: sum(1 for c in r.sample(deck, draws) if c[0] == 0) == k


def t_same_suit(draws: int):
    deck = _deck()
    return lambda r: len({c[1] for c in r.sample(deck, draws)}) == 1


def t_birthday(people: int, days: int = 365):
    def trial(r):
        seen = set()
        for _ in range(people):
            d = r.randrange(days)
            if d in seen:
                return True
            seen.add(d)
        return False
    return trial
