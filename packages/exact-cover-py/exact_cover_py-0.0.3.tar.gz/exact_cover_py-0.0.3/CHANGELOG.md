# ChangeLog

## 2024 Jan 14 - 0.0.3

* no change but refactor tests towards the potential to split
  tests/problems.py into a separate lib exact-cover-problems
  some day

## 2024 Jan 10 - 0.0.2

* first release
* full Python, using dataclasses with slots
* has the S heurisitic implemented
* one single API endpoint exposed: `exact_covers`
  which returns a generator over all solutions
* tested on a small number of problems
* approx. 20 times slower than the C version
  on finding the first solution
