#!/usr/bin/env python

"""
**Unique Distancing Puzzle**

https://www.think-maths.co.uk/uniquedistance

 Can you place 6 counters on a 6x6 grid such that the distance between each
 counter is different?
 """

import argparse
import collections.abc


def dist(p1, p2):
  """Gets the distance between two counters.

  Args:
    p1: A (row, col) tuple of the location of one counter.
    p2: A (row, col) tuple of the location of the other counter.
  Returns:
    The distance between the counters squared. I return squared distance
    because all we care about is uniqueness, not actual distance, and this
    saves us doing a square root and also makes all the numbers integers.
  """
  return pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2)


class Grid(collections.abc.Sequence):
  """A NxN grid with some number of counters on."""

  def __init__(self, n, pieces=(), distances=None):
    """
    Args:
      n: The side length, N.
      pieces: A list of (rol, col) tuples that are occupied by counters.
      distances: A set of the unique distances between the counters. If None,
          this will be calculated on demand.
    """
    self.n = n
    self._pieces = sorted(pieces)
    self._distances = distances

  def __getitem__(self, index):
    return self._pieces[index]

  def __len__(self):
    return len(self._pieces)

  def __eq__(self, other):
    return self._pieces == other._pieces

  @property
  def distances(self):
    """Gets the unique distances between all counters.

    Returns:
      A set of unique distances.
    """
    if self._distances is None:
      self._distances = set()
      for i, p1 in enumerate(self):
        for p2 in self[i + 1:]:
          self._distances.add(dist(p1, p2))
    return self._distances

  def reset_distances(self):
    """Clears the cached distances.

    The next time distances are requested they will be recalculated.
    """
    self._distances = None

  def flip(self, axis):
    """Mirrors the grid across one of the axes.

    Args:
      axis: The axis to flip across (0 or 1).
    Returns:
      A new flipped grid.
    """
    pieces = [tuple(self.n - c - 1 if i == axis else c
                    for i, c in enumerate(piece))
              for piece in self._pieces]
    return Grid(self.n, pieces, self.distances)

  def rotate(self, n=1):
    """Rotates the grid.

    Args:
      n: Number of quarter turns to rotate.
    Returns:
      A new rotated grid.
    """
    pieces = self._pieces
    for i in range(n % 4):
      pieces = [(self.n - x - 1, y) for y, x in pieces]
    return Grid(self.n, pieces, self.distances)

  def symmetrical(self, other):
    """Checks if this grid is symmetrical to another.

    Args:
      other: The other grid to check for symmetry.
    Returns:
      True if the grids have the same distances.
    """
    return self.distances == other.distances
    ## if self.distances != other.distances:
      ## return False
    ## return (any(self.rotate(i) == other for i in range(1, 4)) or
            ## any(self.flip(0).rotate(i) == other for i in range(0, 4)))

  def calc_distances(self, piece):
    """Gets the new distances after adding a counter.

    Args:
      piece: A (row, col) tuple of where to add the piece.
    Returns:
      A new set of distances between all current pieces and between all current
      pieces and the new piece.
    Raises:
      AssertionError: If the new piece isn't after all current pieces or if
          any of the new distances are non-unique.
    """
    distances = set(self.distances)
    for p2 in self:
      assert piece > p2, 'Can\'t add earlier piece'
      d = dist(piece, p2)
      assert (d not in distances), 'Non-unique distance'
      distances.add(d)
    return distances

  def moves(self):
    """Gets all the possible places to put a counter with unique distancing.

    Yields:
      New grids with an extra counter placed.
    """
    for y in range(self.n):
      for x in range(self.n):
        try:
          new_distances = self.calc_distances((y, x))
        except:
          pass
        else:
          yield Grid(self.n, self._pieces + [(y, x)], new_distances)

  def solve(self):
    """Gets all grids with N counters with unique distances.

    Yields:
      New grids with N counters.
    """
    if len(self) == self.n:
      yield self
      return
    for grid in self.moves():
      yield from grid.solve()

  def draw(self):
    """Prints a text image of this board."""
    sep = '+-' * self.n + '+'
    print(sep)
    for y in range(self.n):
      print('|' +  '|'.join(' O'[(y, x) in self] for x in range(self.n)) + '|')
      print(sep)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('n', type=int, nargs='?', default=6,
                      help='Size of grid and number of counters')
  args = parser.parse_args()

  solutions = []
  grid = Grid(args.n)
  for solution in grid.solve():
    if any(s.symmetrical(solution) for s in solutions):
      continue
    solutions.append(solution)
    solution.draw()
    distances = solution.distances
    solution.reset_distances()
    assert(distances == solution.distances)
    assert(len(distances) == args.n * (args.n - 1) / 2)
    print(sorted(distances))
    print()
    ## break
  print('{} unique solutions'.format(len(solutions)))
