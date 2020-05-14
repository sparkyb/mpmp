#!/usr/bin/env python

"""
**Scrabble Puzzle**

https://www.think-maths.co.uk/scrabble-puzzle

How many ways, from the 100 standard scrabble tiles, can you choose seven
which total 46 points?
"""

import argparse
import collections
import functools
import itertools
import operator

try:
  import numpy as np
except ImportError:
  pass


POINTS = {
    'A': 1,
    'B': 3,
    'C': 3,
    'D': 2,
    'E': 1,
    'F': 4,
    'G': 2,
    'H': 4,
    'I': 1,
    'J': 8,
    'K': 5,
    'L': 1,
    'M': 3,
    'N': 1,
    'O': 1,
    'P': 3,
    'Q': 10,
    'R': 1,
    'S': 1,
    'T': 1,
    'U': 1,
    'V': 4,
    'W': 4,
    'X': 8,
    'Y': 4,
    'Z': 10,
    '_': 0,
}


TILES = collections.Counter({
    'A': 9,
    'B': 2,
    'C': 2,
    'D': 4,
    'E': 12,
    'F': 2,
    'G': 3,
    'H': 2,
    'I': 9,
    'J': 1,
    'K': 1,
    'L': 4,
    'M': 2,
    'N': 6,
    'O': 8,
    'P': 2,
    'Q': 1,
    'R': 6,
    'S': 4,
    'T': 6,
    'U': 4,
    'V': 2,
    'W': 2,
    'X': 1,
    'Y': 2,
    'Z': 1,
    '_': 2,
})


def distinct_combinations(values, r):
  """Calculates the number of distinct combinations of a number of items.

  The selection is done without replacement but duplicate items are consindered
  the same.

  Args:
    values: A list of values to select from. Some of these may be duplicates.
    r: The number of items to select.
  Returns:
    The number of distinct ways to select r items from values.
  """
  values = collections.Counter(values)
  p = [1]
  for c in values.values():
    p = np.convolve(p, [1] * (c + 1))
  return p[r]


def value_hands_slow(value, hand_size=7):
  """Calculates the number of Scrabble hands with a given value.

  This is a naive slow algorithm that checks every possible scrabble hand to
  see if it has the target value.

  Args:
    value: The target hand value.
    hand_size: Number of tiles in the hand.
  Returns:
    The number of unique Scrabble hands that have this value.
  """
  count = 0
  # Try each possible hand of the desired size. This ignores limits on number
  # of each letter, so some of these hands will be invalid if they contain more
  # of one letter than is available in a Scrabble set.
  for hand in itertools.combinations_with_replacement(TILES.keys(), hand_size):
    # First check if the value of the hand matches our target value.
    if sum(POINTS[letter] for letter in hand) != value:
      continue
    # If so, rule out any invalid hands by checking whether there are more of
    # each letter in the hand than available in a Scrabble set.
    for letter in hand:
      if hand.count(letter) > TILES[letter]:
        break
    else:
      count += 1
  return count


def value_hands_fast(value, hand_size=7):
  """Calculates the number of Scrabble hands with a given value.

  Start by finding all possibly arrangements of tile values you can have
  in a hand to equal the total value, then figure out how many different
  possible arrangments of letters there are to make hands with those sets of
  values. This is faster than the other approach because there are many fewer
  unique values than there are tiles, so there are fewer combinations of
  values to consider and then that also makes fewer letters to make
  combinations of (removing letters that don't have those values) when we need
  to count all the letters that have those values (which we only do once we
  know the total value is a match).

  Args:
    value: The target hand value.
    hand_size: Number of tiles in the hand.
  Returns:
    The number of unique Scrabble hands that have this value.
  """
  # Group the number of each tile by the unique tile values.
  tiles_with_points = collections.defaultdict(dict)
  for letter, points in POINTS.items():
    tiles_with_points[points][letter] = TILES[letter]

  count = 0
  # Try each possible hand-sized set of point values. This ignores limits on
  # number of tiles of each point value, so some of these combinations will be
  # invalid if they contain more of a value than is available in a Scrabble set.
  for points in itertools.combinations_with_replacement(tiles_with_points.keys(),
                                                        hand_size):
    # First check if the value of the hand matches our target value.
    if sum(points) != value:
      continue
    # Count how many tiles in the hand have each unique point value.
    points = collections.Counter(points)
    for p, c in points.items():
      # Check that the hand doesn't contain more tiles with point value than
      # there are tiles with that value (of any letter) in a Scrabble set.
      if c > sum(tiles_with_points[p].values()):
        break
    else:
      # The number of hands with this set of point values is a the product of
      # the number of distinct combinations of required number of the tiles
      # with each point value.
      count += functools.reduce(operator.mul,
                                (distinct_combinations(tiles_with_points[p], c)
                                 for p, c in points.items()),
                                 1)
  return count


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--hand-size', type=int, default=7,
                      help='Hand size')
  parser.add_argument('value', type=int, nargs='?', default=46,
                      help='Hand point value')
  args = parser.parse_args()

  try:
    num_hands = value_hands_fast(args.value, hand_size=args.hand_size)
  except:
    num_hands = value_hands_slow(args.value, hand_size=args.hand_size)
  print(num_hands)
