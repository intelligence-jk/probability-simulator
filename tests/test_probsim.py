from fractions import Fraction

import pytest

from probsim import exact, simulate as sim
from probsim.cli import main


def test_two_dice_seven():
    assert exact.dice_sum(2, 7) == Fraction(1, 6)


def test_dice_sums_total_one():
    assert sum(exact.dice_sum(3, s) for s in range(3, 19)) == 1


def test_at_least_one_six_in_four():
    assert exact.at_least_one_six(4) == Fraction(671, 1296)


def test_six_two_ways_agree():
    # by counting: 1 minus the all-non-six outcomes
    assert exact.at_least_one_six(3) == 1 - Fraction(5 ** 3, 6 ** 3)


def test_birthday_23_above_half():
    assert exact.birthday(23) > Fraction(1, 2)
    assert exact.birthday(22) < Fraction(1, 2)


def test_birthday_edges():
    assert exact.birthday(1) == 0
    assert exact.birthday(366) == 1


def test_coins():
    assert exact.coins(4, 2) == Fraction(3, 8)
    assert sum(exact.coins(10, k) for k in range(11)) == 1


def test_aces_and_suit():
    assert sum(exact.aces(5, k) for k in range(5)) == 1
    assert exact.aces(2, 2) == Fraction(1, 221)
    assert exact.same_suit(2) == Fraction(12, 51)
    assert exact.same_suit(1) == 1


@pytest.mark.parametrize("name,exact_p,trial", [
    ("two dice seven", exact.dice_sum(2, 7), sim.t_dice_sum(2, 7)),
    ("six in four", exact.at_least_one_six(4), sim.t_at_least_one_six(4)),
    ("coins", exact.coins(10, 5), sim.t_coins(10, 5)),
    ("aces", exact.aces(5, 1), sim.t_aces(5, 1)),
    ("suit", exact.same_suit(3), sim.t_same_suit(3)),
    ("birthday", exact.birthday(23), sim.t_birthday(23)),
])
def test_seeded_simulation_inside_interval(name, exact_p, trial):
    est, lo, hi = sim.estimate(trial, 20000, seed=2024)
    assert lo <= float(exact_p) <= hi


def test_same_seed_same_answer():
    t = sim.t_dice_sum(2, 7)
    assert sim.estimate(t, 1000, seed=5) == sim.estimate(t, 1000, seed=5)


def test_interval_narrows():
    rows = sim.convergence(sim.t_dice_sum(2, 7), (100, 10000), seed=3)
    assert (rows[1][3] - rows[1][2]) < (rows[0][3] - rows[0][2])


def test_cli(capsys):
    assert main(["dice-sum", "2", "7", "--trials", "1000"]) == 0
    assert "exact    = 1/6" in capsys.readouterr().out
