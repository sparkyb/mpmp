#!/usr/bin/env python

"""
**Card Puzzle**

https://www.think-maths.co.uk/card-puzzle

Submit an optimal set of flips (a solution that uses the minimum number of
flips) that guarantees all four cards will eventually be face down given any
starting position.
"""

import argparse


def cards_to_state(flipped):
  """Converts a list of flipped cards into a card state bitfield.

  Args:
    flipped: A list of cards that are flipped from their initial state
        (numbered starting at 1).
  Returns:
    A card state bitfield where bit i (where the low-order bit is 0) indicates
    that card i+1 has been flipped from its initial state.
  """
  return sum(1 << (card - 1) for card in flipped)


def state_to_cards(state):
  """Converts a card state bitfield to a list of flipped cards.

  Args:
    state: A card state bitfield.
  Returns:
    A list of cards that have been flipped (numbered starting at 1).
  """
  flipped = []
  card = 1
  while state:
    if state & 1:
      flipped.append(card)
    card += 1
    state >>= 1
  return flipped


def do_flips(flips, start_state=0):
  """Performs a series of card flips.

  Args:
    flips: A list of cards to flip in order (numbered starting at 1).
    start_state: Initial state of cards as a bitfield (or a list of cards
        to start "flipped").
  Yields:
    The state of the cards after each flip, starting with the initial state.
  """
  if isinstance(start_state, (list, tuple)):
    state = cards_to_state(start_state)
  else:
    state = start_state
  yield state
  for card in flips:
    state ^= 1 << (card - 1)
    yield state


def print_state(state, cards=4, flipped=''):
  """Prints a state of the cards.

  Args:
    state: The card state bitfield (or a list of flipped cards).
    cards: The total number of cards.
    flipped: The card flipped to make this state.
  """
  if isinstance(state, (list, tuple)):
    state = cards_to_state(state)
  print('{}\t{}\t{:0{}b}\t{}'.format(flipped,
                                     ''.join(map(str, state_to_cards(state))),
                                     state, cards,
                                      state))


def test_flips(flips, cards=4, up_or_down=False):
  """Tests whether a series of card flips is guaranteed to win.

  Args:
    flips: A list of cards to flip in order (numbered starting at 1).
    cards: The total number of cards.
    up_or_down: If True, you win if it flips them either all up or down,
        if False, they must flip all up.
  """
  # Starting with the initial state, all states must be tried.
  all_states = frozenset(range(1 << cards))

  flips = list(flips)
  states = list(do_flips(flips))

  print('Flip\tFlipped\tBits\tDecimal')
  print('----\t-------\t----\t-------')
  for flipped, state in zip([''] + flips, states):
    print_state(state, cards, flipped)

  states = set(states)
  if up_or_down:
    # You only need to generate half the states, because they're the inverse
    # of the other half, so if all face up is in one half all face down is
    # in the other. Therefore, treat each state you generate as itself and
    # its inverse
    states |= set(state ^ ((1 << cards) - 1) for state in states)
  if states == all_states:
    print('Success')
  else:
    print('Failure')



def graycode(digits):
  """Counts in graycode.

  Args:
    digits: The number of bits of graycode to use. Will count from 0 to (2^n)-1.
  Yields:
    The numbers of the bits you need to flip (1-based).
  """
  if digits == 0:
    return
  yield from graycode(digits - 1)
  yield digits
  yield from graycode(digits - 1)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--up-or-down', action='store_true',
                      help='Face up or down')
  parser.add_argument('cards', type=int, nargs='?', default=4,
                      help='Number of cards')
  args = parser.parse_args()

  test_flips(graycode(args.cards - args.up_or_down),
             cards=args.cards,
             up_or_down=args.up_or_down)
