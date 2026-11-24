# probability-simulator

Probability: exact answer against simulation.

## What it solves
Probability answers are easy to get wrong and hard to trust. This tool gives the exact answer, as a fraction found by counting, next to a seeded random simulation with a 95 percent interval. You can watch the estimate close in on the exact value as the number of trials grows. It covers dice, coins, cards drawn without replacement, and the birthday problem. Standard library only, Python 3.10 or newer.

## Example
```bash
python -m probsim dice-six 4 --trials 100000
```
```
at least one six in 4 rolls
exact    = 671/1296 = 0.517747
   trials   estimate           95% interval  exact inside?
       10   0.500000  [0.236593, 0.763407]  yes
      100   0.500000  [0.403832, 0.596168]  yes
     1000   0.504000  [0.473055, 0.534914]  yes
    10000   0.511500  [0.501700, 0.521291]  yes
   100000   0.515110  [0.512012, 0.518207]  yes
```
Other experiments:
```bash
python -m probsim dice-sum 2 7      # sum of 2 dice equals 7
python -m probsim coins 10 5        # exactly 5 heads in 10 tosses
python -m probsim aces 5 1          # exactly 1 ace in 5 cards
python -m probsim suit 3            # 3 cards all of one suit
python -m probsim birthday 23       # two of 23 people share a birthday
```
Options: `--trials N` (default 100000) and `--seed S` (default 1). The same seed always gives the same output.

## The maths behind it
- Dice sum: count every way n dice can total s, then divide by 6^n. For two dice and a total of 7 there are 6 ways out of 36, so 1/6.
- At least one six in n rolls: easier through the opposite event. P = 1 - (5/6)^n. For n = 4 this is 1 - 625/1296 = 671/1296.
- Coins: P(k heads in n tosses) = C(n,k) / 2^n.
- Cards without replacement: P(k aces in d cards) = C(4,k) C(48,d-k) / C(52,d). The same counting idea gives P(all d cards of one suit) = 4 C(13,d) / C(52,d).
- Birthday problem: P(shared birthday) = 1 - (365/365)(364/365)...((365-n+1)/365). For 23 people this is about 0.5073, already above one half.
- Interval: the Wilson 95 percent score interval for a proportion, p-hat with z = 1.96. A single 95 percent interval misses the true value about 1 time in 20, so with very few trials you may occasionally see "no". That is the interval doing its job, not a bug.

The exact value is always a Python `Fraction`, so there is no rounding in it. The birthday fraction is very long, so the command line shows only its decimal.

## Install and run
```bash
python -m pip install -e .
python -m pytest
python -m probsim dice-sum 2 7
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
