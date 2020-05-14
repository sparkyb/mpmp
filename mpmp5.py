#!/usr/bin/env python

"""
**Coin Puzzle**

https://www.think-maths.co.uk/coin-puzzle

What is the minimum number of moves needed to leave just one coin remaining?
"""

import argparse


def coord_to_index(coord):
  """Convert a 2D triangle coordinate to a triangle index.

  Args:
    coord: A (row, column) tuple. If this is not a tuple, it will be passed
        through unchanged.
  Returns:
    A 1-based index where the one item on the first row is 1, the two items on
    the second row are 2 and 3, the third row is 4, 5, 6, etc.
  """
  if not isinstance(coord, (tuple, list)):
    return coord
  y, x = coord
  assert x <= y
  return (y + 1) * y // 2 + x + 1

def index_to_coord(index):
  """Converts a triangle index to a 2D coordinate.

  Args:
    index: The 1-based index of the triangle space where the one item on the
        first row is 1, the two items on the second row are 2 and 3, the third
        row is 4, 5, 6, etc. If this is a tuple, it will be returned as-is.
  Returns:
    A (row, column) tuple.
  """
  if isinstance(index, (tuple, list)):
    return tuple(index)
  assert index > 0
  y = int(pow(.25 + 2 * (index - 1), .5) - .5)
  x = index - 1 - (y + 1) * y // 2
  return (y, x)


class Triangle:
  """A triangle board to represent a state of this game.

  Attributes:
    moves: A list of moves. The first item will be 1 item tuple which indicates
        the index of the first coin to remove. Subsequent items will be
        tuples that represent jumps where the first item in the tuple is the
        index of where the coin started and subsequent entries are the indices
        of places where it landed. In the case of a single jump this will be
        a 2-tuple, but it will be longer for more jumps.
    rows: A list of lists of booleans where each list of booleans is a row
        in the triangle and each boolean indicates if there is still a coin
        in that slot or not.
  """

  def __init__(self, rows=4, src=None, *dests):
    """
    Args:
      rows: Either a number of rows (they will start full), or a previous
          triangle to copy.
      src: The index or coordinate to jump from.
      *dests: A list of locations to jump to. If None, the coin at the source
          will be removed (first move only).
    """
    if isinstance(rows, Triangle):
      self.rows = [list(row) for row in rows.rows]
      self.moves = list(rows.moves)
    else:
      self.rows = [[True] * y for y in range(1, rows + 1)]
      self.moves = []
    if src is not None:
      self.move(src, *dests)
    else:
      assert not dests

  def __len__(self):
    return coord_to_index((len(self.rows), 0))

  def __getitem__(self, index):
    y, x = index_to_coord(index)
    return self.rows[y][x]

  def __setitem__(self, index, value):
    y, x = index_to_coord(index)
    self.rows[y][x] = value

  def move(self, src, *dests):
    """Moves a coin.

    Args:
      src: The index or coordinate to jump from.
      *dests: A list of locations to jump to. If None, the coin at the source
          will be removed (first move only).
    """
    assert self[src]
    if not dests:
      assert len(self.moves) == 0
      self[src] = False
      self.moves.append((coord_to_index(src),))
    else:
      for dest in dests:
        src = index_to_coord(src)
        dest = index_to_coord(dest)
        jumped = ((src[0] + dest[0]) // 2, (src[1] + dest[1]) // 2)
        assert self[src] and self[jumped] and not self[dest]
        self[src] = False
        self[dest] = True
        self[jumped] = False
        src = coord_to_index(src)
        dest = coord_to_index(dest)
        if len(self.moves) > 1 and self.moves[-1][-1] == src:
          self.moves[-1] = self.moves[-1] + (dest,)
        else:
          self.moves.append((src, dest))
        src = dest

  def _moves_from(self, src):
    """Iterates the possible jumps from a given location.

    Assumes there is a coin in that starting location but doesn't check that.
    Tries jumping in all 6 directions and returns only those where there is
    room on the board to move 2 spaces in that direction, there is a coin to
    jump over and remove in the adjacent space, and the following space is
    empty for the coin to land in.

    Args:
      src: The location to jump from (index or coordinate).
    Yields:
      A coordinate (2-tuple) where the coin would land.
    """
    y, x = index_to_coord(src)
    for dest in [(y - 2, x),  # jump up and right
                 (y + 2, x),  # jump down and left
                 (y, x - 2),  # jump left
                 (y, x + 2),  # jump right
                 (y - 2, x - 2),  # jump up and left
                 (y + 2, x + 2),  # jump down and right
                 ]:
      jumped = ((y + dest[0]) // 2, (x + dest[1]) // 2)
      if (0 <= dest[0] < len(self.rows) and
          0 <= dest[1] < dest[0] + 1 and
          self.rows[jumped[0]][jumped[1]] and
          not self.rows[dest[0]][dest[1]]):
        yield dest

  def get_moves(self, ignore_symmetry=True):
    """Iterates all valid moves from this board configuration.

    From the current board position, tries jumping every coin in all possible
    directions.

    Args:
      ignore_symmetry: If True, only unique initial moves will be tried
          ignoring symmetric locations (only cells along first half of the
          the top-left edge of each nested triangle).
    Yields:
      A new Triangle board state for each possible move.
    """
    # Iterate through each possible location on the board.
    for src in range(1, len(self)):
      if not self.moves:
        # If no moves have been made yet, the board is full. The only possible
        # move is to remove that coin.
        if ignore_symmetry:
          y, x = index_to_coord(src)
          if (x > y // 2 or
              y > (len(self.rows) + x - 1) // 2):
            continue
        new_tri = Triangle(self, src)
        yield new_tri
      elif self[src]:
        # Otherwise, if there is a coin in that location, try every possible
        # jump.
        for dest in self._moves_from(src):
          j = coord_to_index(dest)
          new_tri = Triangle(self, src, dest)
          yield new_tri

  def draw(self):
    """Gets an ASCII drawing of the current board as a string."""
    return '\n'.join(' ' * (len(self.rows) - y - 1) +
                        ' '.join('.o'[full] for full in row)
                     for y, row in enumerate(self.rows))

  @property
  def solved(self):
    return sum(full for row in self.rows for full in row) == 1

  def solve(self, ignore_symmetry=True):
    """Find all possible moves that result in a solved board (1 coin left).

    Args:
      ignore_symmetry: If True, only unique initial moves will be tried
          ignoring symmetric locations (only cells along first half of the
          the top-left edge of each nested triangle).
    Returns:
      A list of move lists that result in a solved board. Sorted from shortest
      solution to longest.
    """
    solutions = []
    states = [self]
    while states:
      state = states.pop()
      if state.solved:
        solutions.append(state.moves)
      else:
        states.extend(state.get_moves(ignore_symmetry=ignore_symmetry))
    solutions.sort(key=len)
    return solutions


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--ignore-symmetry', action='store_true',
                      help='Skip symmetric starting locations')
  parser.add_argument('-s', '--start', type=int,
                      help='Starting location')
  parser.add_argument('rows', type=int, nargs='?', default=4,
                      help='Number of rows')
  args = parser.parse_args()

  tri = Triangle(args.rows, src=args.start)
  solutions = tri.solve(ignore_symmetry=args.ignore_symmetry)
  if solutions:
    for moves in solutions:
      print('{} moves: {}'.format(
          len(moves),
          ', '.join('-'.join(map(str, move)) for move in moves)))
  else:
    print('No solutions')
