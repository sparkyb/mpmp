#!/usr/bin/env python

"""
**Million Bank Balance Puzzle**

https://www.think-maths.co.uk/BankBalance

What must your initial two deposits be to ensure that you win the million
pounds?

Balance on day n when initial deposits are a and b:
day (n)     balance
-------------------
1           a
2           a  + b
3           2a + b
4           3a + 2b
5           5a + 3b
6           8a + 5b

Looking at just the coefficients of a and b, we can see they're a Fibonacci
sequence off by one. So:

balance(n) = fib(n) * a + fib(n - 1) * b

(where fib(0) = 0, fib(1) = 1, etc.)
"""

import argparse
import functools
import itertools


_fib_cache = [0, 1]
def fib(n):
  """Gets the nth Fibonacci number.

  Where fib(0) == 0 and fib(1) == 1.
  """
  while n >= len(_fib_cache):
    _fib_cache.append(_fib_cache[-2] + _fib_cache[-1])
  return _fib_cache[n]


def balance(a, b, n):
  """Gets the balance on day n if the initial deposits are a and b.

  Where:
    balance(a, b, 0) == 0
    balance(a, b, 1) == a
    balance(a, b, 2) == a + b
  """
  if n < 1:
    return 0
  return fib(n) * a + fib(n - 1) * b


def find_deposits(total):
  """Find the minimum deposit amounts to eventually reach a certain balance.

  Args:
    total: The target balance to eventually reach.
  Returns:
    (a, b, n) where a and b are the day 1 and day 2 deposits (respectively)
    and n is the number of days it will take to reach the total.
  """
  max_n = 0
  while fib(max_n) <= total:
    max_n += 1
  # If fib(x) > total, then fib(x - 1) + fib(x - 2) > total
  # so even if a and b are both 1, then on day x - 1 the balance would be too
  # high so the maximum day would be x - 2.
  max_n -= 2

  for n in range(max_n, 0, -1):
    for b in itertools.count(1):
      a = (total - fib(n - 1) * b) / fib(n)
      if int(a) == a:
        return (int(a), b, n)
      elif a < 1:
        break
  raise ValueError('Not possible')


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('total', type=int, nargs='?', default=1_000_000,
                      help='Target balance')
  args = parser.parse_args()

  try:
    a, b, n = find_deposits(args.total)
  except ValueError as e:
    print(e)
  else:
    bals = [0, a, a + b]
    print('Day\tDeposit\tBalance')
    print('---\t-------\t-------')
    print('1\t{}\t{}'.format(a, bals[1]))
    print('2\t{}\t{}'.format(b, bals[2]))
    for day in range(3, n + 1):
      if day >= len(bals):
        bals.append(bals[-2] + bals[-1])
      print('{}\t\t{:,}'.format(day, bals[day]))
