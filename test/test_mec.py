#! /bin/python3

import sys

sys.path.append("../src")

import unittest
import mec
import math


class TestMinimumEnclosingCircle(unittest.TestCase):
    def test_point(self) -> None:
        x = mec.Point(x=1.0, y=0.5)
        y = mec.Point(x=2.0, y=1.0)
        z = mec.Point(x=3.0, y=1.5)

        self.assertEqual((x + y), z)
        self.assertEqual((z - x), y)
        self.assertEqual((x * 2), y)
        self.assertEqual((z / 3), x)
        self.assertEqual((y / 2), x)

        self.assertEqual(mec.dot(x, y), 2.5)
        self.assertEqual(mec.det(x, y), 0.0)
        self.assertEqual(mec.dist(x, y), x.mag)
        self.assertEqual(mec.mid_point(x, z), y)

    def test_circle(self) -> None:
        x = mec.Circle(mec.Point(0, 0), 1.0)
        y = mec.Circle(mec.Point(1, 1), 1.0)
        z = mec.Circle(mec.Point(1, 2), 2.0)

        self.assertTrue(x.contains(mec.Point(0.5, 0.5)))
        self.assertTrue(y.contains(mec.Point(0.5, 0.5)))
        self.assertTrue(z.contains(mec.Point(0.5, 0.5)))

        self.assertEqual(x.diameter, 2.0)
        self.assertEqual(y.diameter, 2.0)
        self.assertEqual(z.diameter, 4.0)

        self.assertEqual(x.circumference, x.diameter * math.pi)
        self.assertEqual(y.circumference, y.diameter * math.pi)
        self.assertEqual(z.circumference, z.diameter * math.pi)

        self.assertEqual(x.radius_squared, 1.0)
        self.assertEqual(y.radius_squared, 1.0)
        self.assertEqual(z.radius_squared, 4.0)

        self.assertEqual(x.area, x.radius_squared * math.pi)
        self.assertEqual(y.area, y.radius_squared * math.pi)
        self.assertEqual(z.area, z.radius_squared * math.pi)

    def test_trivial_mec(self) -> None:
        w = mec.Point(-1, 0)
        x = mec.Point(1, 0)
        y = mec.Point(0, 1)
        z = mec.Point(0, 0)

        unit_circle = mec.Circle(z, 1)

        self.assertEqual(mec.min_circle_trivial([w]), mec.Circle(w, 0))
        self.assertEqual(mec.min_circle_trivial([x]), mec.Circle(x, 0))
        self.assertEqual(mec.min_circle_trivial([y]), mec.Circle(y, 0))
        self.assertEqual(mec.min_circle_trivial([z]), mec.Circle(z, 0))

        self.assertEqual(mec.min_circle_trivial([w, x]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([x, w]), unit_circle)

        self.assertEqual(mec.min_circle_trivial([w, x, y]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([w, y, x]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([x, w, y]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([x, y, w]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([y, w, x]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([y, x, w]), unit_circle)

        self.assertEqual(mec.min_circle_trivial([w, x, z]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([w, z, x]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([x, w, z]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([x, z, w]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([z, x, w]), unit_circle)
        self.assertEqual(mec.min_circle_trivial([z, w, x]), unit_circle)

    def test_nontrivial_mec(self) -> None:
        w = mec.Point(-1, 0)
        x = mec.Point(1, 0)
        y = mec.Point(0, 1)
        z = mec.Point(0, 0)

        unit_circle = mec.Circle(z, 1)
        self.assertEqual(mec.welzl([w, x, y, z]), unit_circle)

        soln0 = mec.Circle(mec.Point(0.5, 0.5), math.sqrt(2.0) / 2.0)
        self.assertEqual(mec.welzl([x, y, z]), soln0)

        p0 = mec.Point(5, -2)
        p1 = mec.Point(-3, -2)
        p2 = mec.Point(-2, 5)
        p3 = mec.Point(1, 6)
        p4 = mec.Point(0, 2)
        soln1 = mec.Circle(mec.Point(1, 1), 5)

        self.assertEqual(mec.welzl([p0, p1, p2, p3, p4]), soln1)


if __name__ == "__main__":
    unittest.main()
