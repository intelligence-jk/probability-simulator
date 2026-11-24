"""Command line: python -m probsim <experiment> [numbers] [--trials N] [--seed S]."""
import argparse

from . import exact, simulate as sim


def build(args):
    e = args.experiment
    a = args.numbers
    if e == "dice-sum":      # n dice, target sum
        n, t = a
        return f"sum of {n} dice = {t}", exact.dice_sum(n, t), sim.t_dice_sum(n, t)
    if e == "dice-six":      # n rolls
        (n,) = a
        return f"at least one six in {n} rolls", exact.at_least_one_six(n), sim.t_at_least_one_six(n)
    if e == "coins":         # n tosses, k heads
        n, k = a
        return f"exactly {k} heads in {n} tosses", exact.coins(n, k), sim.t_coins(n, k)
    if e == "aces":          # cards drawn, aces wanted
        d, k = a
        return f"exactly {k} aces in {d} cards", exact.aces(d, k), sim.t_aces(d, k)
    if e == "suit":          # cards drawn, all one suit
        (d,) = a
        return f"all {d} cards of one suit", exact.same_suit(d), sim.t_same_suit(d)
    if e == "birthday":      # people
        (p,) = a
        return f"shared birthday among {p} people", exact.birthday(p), sim.t_birthday(p)
    raise SystemExit("unknown experiment")


ARITY = {"dice-sum": 2, "dice-six": 1, "coins": 2, "aces": 2, "suit": 1, "birthday": 1}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="probsim", description=__doc__)
    ap.add_argument("experiment", choices=sorted(ARITY))
    ap.add_argument("numbers", type=int, nargs="+")
    ap.add_argument("--trials", type=int, default=100000)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args(argv)
    if len(args.numbers) != ARITY[args.experiment]:
        ap.error(f"{args.experiment} needs {ARITY[args.experiment]} number(s)")
    label, exact_p, trial = build(args)
    steps = [s for s in (10, 100, 1000, 10000, 100000, 1000000) if s <= args.trials]
    if args.trials not in steps:
        steps.append(args.trials)
    print(label)
    frac = str(exact_p)
    if len(frac) > 30:
        frac = f"a fraction of {len(frac)} digits"
    print(f"exact    = {frac} = {float(exact_p):.6f}")
    print(f"{'trials':>9}  {'estimate':>9}  {'95% interval':>21}  exact inside?")
    for n, est, lo, hi in simulate_rows(trial, steps, args.seed):
        inside = "yes" if lo <= float(exact_p) <= hi else "no"
        print(f"{n:>9}  {est:>9.6f}  [{lo:.6f}, {hi:.6f}]  {inside}")
    return 0


def simulate_rows(trial, steps, seed):
    return sim.convergence(trial, steps, seed)


if __name__ == "__main__":
    raise SystemExit(main())
