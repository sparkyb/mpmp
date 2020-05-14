#!/usr/bin/env python

"""
**Steam Train Puzzle**

https://www.think-maths.co.uk/train-puzzle

What is the minimum (optimal) amount of fuel it takes the steam train to travel
800 miles?

Proof:

Define C as the capacity of the train's fuel tank.

Define the start of the track as location 0.
Define the destination (Party Town) as location D.

The least amount of fuel required to from 0 to D is D, as long as D <= C.

If D > C, you will have to make some number of trips, let's call this N, from
the start to drop of fuel along the side to be picked up later. Every trip will
be from 0 to some location and back to 0. Let's define the locations of these
round-trip stops as the sequence S1 to Sn. Don't worry about the order for now.

The most effient use of fuel is that where none is wasted so we reach D we
should have no fuel left in our tank and no fuel left on the side of the
track. As a consequence, our total amount of fuel used will also be equal to
our total distance travelled, D + Sum k=1 to n, 2 * Sk.

Therefore, on our final trip, we must pick up any remaining fuel that was left
beside the track on any previous trip (that wasn't already picked up on a
previous trip). At some point X, we'll pick up our last dropped fuel. At this
point we need to have exactly enough fuel to get to D without any left over,
D - X.

This point X must be exactly the maximum of our stops S1-Sn. It can't be
farther than the maximum because the maximum is the farther out we've
previously been, therefore there can be no fuel to pick up after this. It
also can't be less than the maximum, because then there'd still be fuel to
pick up after X, or else if there was a trip past X but no fuel dropped past
X or all fuel dropped past X already picked up, than it was a waste of a trip
since it doesn't help the final trip. 

Every location up to X must be visited at least 3 times, on the final trip
as well as twice on at least one other trip (out and back), whereas every
location after X will be visited only once, on the final trip. Therefore the
most efficient trip is the one that minimizes X (and maximizes D - X).

The maximum possible D - X is C, so X = D - C.

If we only make two trips (one out-and-back and the final trip), then the
out-and-back will be to X and requires 3X fuel. It costs 2X to get out to X
and back, and since X is the only fuel stop on the final trip and the goal is
to be full to go from X to D, if you're full at the start you'll need to
replace the X used to go from 0 to X on the final trip in order to be full at
X to go from X to D.

If 3X > C, we'll need more than two trips. We can break this up recursively.
If you assume we have a way of reaching X with a full tank (filling up some
amount at X), we can consider X as the starting point and we can think of the
the final trip as being from X to D, a distance of C. Now consider a point
Y < X. If you assume a way of reaching Y with a full tank, we need 3(X-Y) to
to go round-trip from Y to X and back, leaving X - Y there to fill up what we
lost going from Y to X on the final trip. In the same way we reasoned that X
has to be the maximum of all the stops, we can reason that Y must be the next
farthest stop. It must be a stop because in order to be full at Y we must pick
up fuel there. It doesn't make sense to make a trip to anywhere between Y and
X if we're defining Y as the spot from which you can make it to X and back to
drop off the fuel we'll need to get to D. We won't need any fuel between Y and
X.

Now, the space between Y and X we'll visit 3 times, like we've said, to drop
off fuel at X (out-and-back) and again on our final trip. In order to do that
being full at Y, we'll need to take an earlier out-and-back trip to Y to place
fuel we'll need to fill up. This means we have to travel the area between 0
and Y at least 5 times (out-and-back to Y to drop off fuel, out-and-back to X
to drop off fuel at X, picking up fuel at Y alone the way, and on the final
trip). So like before, it is most efficient to minimize Y, maximizing X - Y,
where 3(X - Y) <= C. So Y = X - C/3. Now, we'll be taking 3 trips to Y, two
of which are out-and-back (to Y and to X), which means that our first
out-and-back to Y requires 5Y fuel. 2Y just for that trip itself, and 3Y to
leave at Y to be able to fill up at Y on the way to X and on the way to D,
and to fill up on the way back from from X to get back to 0.

If 5Y > C than we'll need to make another pit stop and this pattern will
continue. We're adding stops in the reverse order that you'll visit them,
each closer to the start. So let's define this point X as S1, Y as S2, etc in
decreasing value until Sn is the closest to the start. Even though this is
backwards from how we're visiting them and sequences normally increase instead
of decreasing, we're adding stops working backwards from our goal, so
it's easier to define the sequence S as decreasing. We can even define S0 = D.

Each stop Sk will need the amount of fuel to get from Sk+1 to Sk (Sk - Sk+1)
times the consecutive odd numbers, because it needs twice that amount just for
the trip to Sk, plus twice that amount of every stop after Sk, Sk-1 down to S1,
plus once that amount for the final trip. So the amount of fuel needed for the
trip Sk is (Sk - Sk+1) * (2k + 1). S0 (the final trip) wil need S0 - S1 which
is D - X which we said before. S1 will need (S1 - S2) * 3 (for itself
plus the final trip) which is the same as 3(X - Y), S2 will need (S2 - S3) * 5,
etc, all of which must be less than or equal to C until Sn needs Sn * (2n + 1).
Since each earlier trip needs an increasing multiple, the most efficient trip
is one which maximized the length of later trips and minimizes earlier ones.
Therefore, each amount of fuel will be exactly C, until the shortest trip
that needs less than C. So, S0 = D, S1 = D - C. S2 = S1 - C/3,
Sk = Sk-1 - C / (2k - 1), until Sn <= C / (2n + 1).

Once we've worked out the number of trips needed and their distances, there are
3 ways to calculate the total amount of fuel needed. One is the way mentioned
above that our fuel required is the total distance traveled,
D + Sum k=1 to n, 2 * Sk. Another is to sum the amount of additional fuel
needed for each trip, (Sum k=0->n-1, (Sk - Sk+1) * (2k + 1)) + Sn * (2n + 1).
sequenced mentioned before and add a full tank for the final trip,
C + Sum k=1->n, (Sk - Sk-1) * (2(n-k) + 3). 
The third way is that all trips will start with a full tank, including the
final trip, except the first trip where the amount needed at Sn might not
require a full tank. Therefore, the total is C * n + Sn * (2n + 1).
"""

import argparse


def fuel_required_rec(d, c, n=0):
  """Calculates the amount of fuel required for a train to a distance.

  This is a recursive version. It is designed to be tail-recurive so that
  stack depth wouldn't be a problem, but unfortunately Python doesn't
  optimize tail recursive calls.

  Args:
    d: Distance to travel.
    c: Capacity of the train's fuel tank.
    n: Number of additional stops after this trip.
  Returns:
    The amount of fuel that will be used by the whole trip.
  """
  if d * (2 * n + 1) <= c:
    return c * n + d * (2 * n + 1)
  else:
    return fuel_required_rec(d - c / (2 * n + 1), c, n + 1)


def fuel_required(d, c, n=0):
  """Calculates the amount of fuel required for a train to a distance.

  This is an iterative version of the above recursive function to get around
  Python's stack depth limit for really large inputs.

  Args:
    d: Distance to travel.
    c: Capacity of the train's fuel tank.
  Returns:
    The amount of fuel that will be used by the whole trip.
  """
  n = 0
  while d * (2 * n + 1) > c:
    d -= c / (2 * n + 1)
    n += 1
  return c * n + d * (2 * n + 1)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-t', '--tank', type=int, default=500,
                      help='Train fuel tank capacity')
  parser.add_argument('distance', type=int, nargs='?', default=800,
                      help='Distance to travel')
  args = parser.parse_args()

  fuel = fuel_required(args.distance, args.tank)
  print('{:.2f}'.format(fuel))
