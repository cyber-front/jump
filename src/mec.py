# MIT License

# Copyright (c) 2022 Cybernetic Frontiers, LLC

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from dataclasses import dataclass
import functools as ft
import math
import random as rand
import typing


@dataclass
class Point:
    """
    This class defines a 2D point in the plane Z=0

    :param X: X component of the Point instance
    :param Y: Y component of the Point instance
    """

    x: float
    y: float

    @property
    def mag_squared(self) -> float:
        """
        Return the square of the length of the vector connecting the
        location of the point to the origin of the plane.
        """
        return self.x * self.x + self.y * self.y

    @property
    def mag(self) -> float:
        """
        Return the length of the vector connecting the point to the origin

        :return: The length of the vector connecting the point to the origin
        """
        return math.sqrt(self.mag_squared)

    def __add__(self, val: object):
        """
        Return the sum of two points, adding them together in the way
        vectors can be added.

        :param val: Point value to add to this one
        :return: Sum of the two vectors
        """
        return Point(x=self.x + val.x, y=self.y + val.y)

    def __sub__(self, val: object):
        """
        Return the difference between two points.

        :param val: Point to subtract from this ont
        :return: Difference of two vectors
        """
        return Point(x=self.x - val.x, y=self.y - val.y)

    def __mul__(self, scale: float):
        """
        Scale a point by a scaling factor.

        :param scale: Scale factor to multiply the point
        :return: The point scaled by the scaling factor
        """
        return Point(x=self.x * scale, y=self.y * scale)

    def __truediv__(self, scale: float):
        """
        Scale a point by dividing by a scaling factor

        :param scale: Scale factor to divide the point
        :return: The point scaled by the scaling factor
        """
        return Point(x=self.x / scale, y=self.y / scale)

    def __eq__(self, val: object) -> bool:
        """
        Check to see if this point is the same as the one passed.

        :param val: Value to check the equality of this point
        """
        return self.x == val.x and self.y == val.y


def dot(p1: Point, p2: Point) -> float:
    """
    Compute the dot product of the two points given

    :param p1: First of the two points used for computing the dot product
    :param p2: Second of the two points used for computing the dot product
    :return: The dot product of the two given points.
    """
    return p1.x * p2.x + p1.y * p2.y


def det(p1: Point, p2: Point) -> float:
    """
    Compute the determinant of the two given points.

    :param p1: First of the two points to use in computing the determinant
    :param p2: Second of the two points to use in computing the determinant
    :return: The determinant of the two given points
    """
    return p1.x * p2.y - p1.y * p2.x


def dist(p1: Point, p2: Point) -> float:
    """
    Compute the l-2 distance between the two points

    :param p1: First of the two points to use in computing the distance between the two points
    :param p2: Second of the two points to use in computing the distance between the two points
    :return: The distance between the two points
    """
    return (p1 - p2).mag


def dist_squared(p1: Point, p2: Point) -> float:
    """
    Compute the square of the distance between two points.

    :param p1: First of two points to use computing the squared distance between the two points
    :param p2: Second of two points to use computing the squared distance between the two points
    :return: Square of the distance between the two points.
    """
    return (p1 - p2).mag_squared


def mid_point(p1: Point, p2: Point) -> Point:
    """
    Compute the midpoint of the two given points

    :param p1: First of the two points for which to compute the midpoint
    :param p2: Second of the two points for which to compute the midpoint
    :return: Midpoint of the two points
    """
    return (p1 + p2) / 2.0


@dataclass(frozen=True)
class Circle:
    """
    This class defines a circle of a particular radius with its center
    at a certain location.

    :param center: Location of the center of the circle
    :param radius: Length of the radius of the circle
    """

    center: Point
    radius: float

    def contains(self, p: Point) -> bool:
        """
        Given a point, determine if this circle contains it

        :param p: Point to check to see if it's interior to this circle
        :return: True if the point give is interior to the circle
        """
        return (p - self.center).mag_squared <= self.radius_squared

    @property
    def diameter(self) -> float:
        """
        Return the diameter of the circle
        :return: The diameter of the circle
        """
        return 2.0 * self.radius

    @property
    def circumference(self) -> float:
        """
        Return the circumference of the circle

        :return: The circumference of the circle
        """
        return self.diameter * math.pi

    @property
    def radius_squared(self) -> float:
        """
        Return the square of the radius of the circle

        :return: The square of the radius
        """
        return self.radius * self.radius

    @property
    def area(self) -> float:
        """
        Return the area of the circle

        :return: Area of the circle
        """
        return self.radius_squared * math.pi

    def __eq__(self, val: object) -> bool:
        """
        Check to see if this point is the same as the one passed.

        :param val: Value to check the equality of this point
        """
        return self.center == val.center and self.radius == val.radius


def get_circle_from_2_points(p1: Point, p2: Point) -> Circle:
    """
    For two points, the minimal enclosing circle is the circle centered
    at the midpoint of the line segment connecting the two points and
    diameter is the length of the line segment connecting the two points.
    Put another way, the radius is one half the length of the line segment
    connecting the two points.

    :param p1: First of the two points on the circle's boundary
    :param p2: Second of the two points on the circle's oundary
    """
    return Circle(center=mid_point(p1, p2), radius=(p1 - p2).mag / 2.0)


def get_circle_center(b: Point, c: Point) -> Point:
    """
    This finds the center of a circle where two of the points are given, and
    the third is fixed at the origin.

    :param b: Location of the first of the two points away from the origin
    :param c: Location of the second of the two points away from the origin
    """
    B = dot(b, b)
    C = dot(c, c)
    D = det(b, c)
    return Point((c.y * B - b.y * C) / (2 * D), (b.x * C - c.x * B) / (2 * D))


def get_circle_from_3_points(A: Point, B: Point, C: Point) -> Circle:
    """
    This finds the circle defined by the three points given.

    :param A: First of the three points to use in the computations
    :param B: Second of the three points to use in the computation
    :param C: Thirrd of the three points to use in the computation
    :return: Circle defined by the three points
    """

    I = get_circle_center(B - A, C - A) + A
    return Circle(I, dist(I, A))


def is_valid_circle(c: Circle, P: typing.Sequence[Point]) -> bool:
    """
    Given a circle, this will return false if there are any listed points which
    are not inside the circle.

    :param c: Cricle to check for point inclusion
    :param P: List of points to ckeck for inclusion
    :return: True exactly when all points in P are contained in circle c
    """
    return len(list(filter(lambda x: not c.contains(x), P))) == 0


def min_circle_trivial(P: typing.Sequence[Point]) -> Circle:
    """
    This function computes the minimum enclosing circle for cases where there are
    one, two or three points in the given list.

    :param P: List of points for computing the minimum enclosing circle
    :return: Minimum enclosing circle of the one, two or three points given.
    """
    assert len(P) <= 3
    if not P:
        return Circle(Point(0, 0), 0)

    elif len(P) == 1:
        return Circle(P[0], 0)

    elif len(P) == 2:
        return get_circle_from_2_points(P[0], P[1])

    # To check if MEC can be determined
    # by 2 points only
    for i in range(3):
        for j in range(i + 1, 3):

            c = get_circle_from_2_points(P[i], P[j])
            if is_valid_circle(c, P):
                return c

    return get_circle_from_3_points(P[0], P[1], P[2])


def welzl_helper(
    P: typing.Sequence[Point], R: typing.Sequence[Point], np: int
) -> Circle:
    """
    This function recursively computes the minimal enclosing
    circle of the collection of points given to it.  The first np
    points in P are those which have not yet been processed, and R
    contains the points which have been processed.  One point is
    moved from P to R each iteration.

    :param P: Points which have not yet been processed
    :param R: Points which have been processed
    """
    nr = len(R)

    # Base case when all points processed or |R| = 3
    if np == 0 or nr == 3:
        return min_circle_trivial(R)

    # Pick a random point randomly
    idx = rand.randint(0, np - 1)
    p = P[idx]

    # Put the picked point at the end of P
    # since it's more efficient than
    # deleting from the middle of the vector
    P[idx], P[np - 1] = P[np - 1], P[idx]

    # Get the MEC circle d from the
    # set of points P - :p
    d = welzl_helper(P, R.copy(), np - 1)

    # If d contains p, return d
    if d.contains(p):
        return d

    # Otherwise, must be on the boundary of the MEC
    R.append(p)

    # Return the MEC for P - :p and R U :p
    return welzl_helper(P, R.copy(), np - 1)


def welzl(P: typing.Sequence[Point]) -> Circle:
    """
    Main function to compute the minimal enclosing circle of a collection
    of points.

    :param P: List of points for computing the MEC
    :return: Minimal enclosing circle of the points
    """
    P_copy = P.copy()
    rand.shuffle(P_copy)
    return welzl_helper(P_copy, [], len(P_copy))


def bounds(P: typing.Sequence[Point]) -> typing.Tuple[Point, Point]:
    """
    Compute the axially aligned bounding box for the given points.

    :param P: List of points
    :return: Bounding box for the given set of points
    """
    min_val = P[0]
    max_val = P[0]

    for p in P[1:]:
        min_val = Point(x=min(min_val.x, p.x), y=min(min_val.y, p.y))
        max_val = Point(x=min(max_val.x, p.x), y=min(max_val.y, p.y))

    return min_val, max_val
