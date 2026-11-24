# REVIEW (CHECKLIST.md, 24 Nov 2026)

1. Maths checked twice: PASS. Exact values come from combinatorics (Fraction). They were checked a second way: brute-force enumeration of all outcomes (3 dice sum 10, 4 rolls with a six = 671/1296, 8 coin tosses with 3 heads), the permutation form 1 - P(365,23)/365^23 for the birthday problem, and sequential probabilities for cards (4/52 x 3/51 for two aces; 12/51 x 11/50 for three of one suit). All agree exactly.
2. Tests pass locally: PASS, 17 passed (`python -m pytest -q`). CI: workflow `.github/workflows/` runs the same command on Python 3.12; it has not run yet because nothing is pushed.
3. No student data, copied board-paper or textbook text, nothing of any other business: PASS (searched; all problems are generic textbook-style classics written fresh).
4. README: PASS. Says what it solves, a real run output, the maths, install and run.
5. MIT licence, copyright MATH and MYTH FZ-LLC: PASS (LICENSE).
6. No em dashes, no "Dubai" alone (none used), no outcome promises: PASS (searched).

Notes: the seeded interval check in the tests uses 20000 trials and fixed seeds, so results are repeatable. At very few trials (10) a 95 percent interval can legitimately miss the exact value; the README says so. Not on GitHub, not pushed.
