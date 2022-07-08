#! /bin/python3

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

import sys

sys.path.append("../src")

import config as cfg
import exception as excp
import unittest
import enumerations as en


class TestConfig(unittest.TestCase):
    def test_validate_description(self) -> None:
        tc0 = {"description": "test"}
        self.assertEqual(cfg.validate_description(config=tc0), "test")

        tc1 = {"description": 10.3}
        self.assertRaises(excp.PuzzleException, cfg.validate_description, config=tc1)

        tc2 = {"nada": None}
        self.assertEqual(
            cfg.validate_description(config=tc2), "Generic Jump Puzzle Solution"
        )

    def test_validate_scope(self) -> None:
        tc0 = {"scope": "SINGLE"}
        self.assertEqual(cfg.validate_scope(config=tc0), en.SolutionScope.SINGLE)

        tc1 = {"scope": "MULTIPLE"}
        self.assertEqual(cfg.validate_scope(config=tc1), en.SolutionScope.MULTIPLE)

        tc2 = {"scope": "invalid"}
        self.assertRaises(excp.PuzzleException, cfg.validate_scope, config=tc2)

        tc3 = {"nada": None}
        self.assertEqual(cfg.validate_scope(config=tc3), en.SolutionScope.SINGLE)

    def test_validate_method(self) -> None:
        tc0 = {"method": "DEPTH_FIRST"}
        self.assertEqual(cfg.validate_method(config=tc0), en.SearchMethod.DEPTH_FIRST)

        tc1 = {"method": "BREADTH_FIRST"}
        self.assertEqual(cfg.validate_method(config=tc1), en.SearchMethod.BREADTH_FIRST)

        tc2 = {"method": "invalid"}
        self.assertRaises(excp.PuzzleException, cfg.validate_method, config=tc2)

        tc3 = {"nada": None}
        self.assertEqual(cfg.validate_method(config=tc3), en.SearchMethod.DEPTH_FIRST)

    def test_validate_start(self) -> None:
        tc0 = {"start": [0, 1, 2]}
        self.assertEqual(cfg.validate_start(config=tc0, node_count=3), {0, 2, 1})
        self.assertRaises(
            excp.PuzzleException, cfg.validate_start, config=tc0, node_count=2
        )

        tc1 = {"start": {0, 1, 2}}
        self.assertRaises(
            excp.PuzzleException, cfg.validate_start, config=tc1, node_count=3
        )

        tc2 = {"start": ["0", "1", "2"]}
        self.assertRaises(
            excp.PuzzleException, cfg.validate_start, config=tc2, node_count=2
        )

        tc3 = {"nada": None}
        self.assertRaises(
            excp.PuzzleException, cfg.validate_start, config=tc3, node_count=2
        )

        tc4 = {"start": [-1, 1, 2]}
        self.assertRaises(
            excp.PuzzleException, cfg.validate_start, config=tc4, node_count=3
        )

        tc5 = {"start": [0, 0, 1, 2]}
        self.assertRaises(
            excp.PuzzleException, cfg.validate_start, config=tc5, node_count=5
        )

    def test_validate_finish(self) -> None:
        tc0 = {"finish": [0, 1, 2]}
        self.assertEqual(cfg.validate_finish(config=tc0, node_count=3), {0, 2, 1})
        self.assertRaises(
            excp.PuzzleException, cfg.validate_finish, config=tc0, node_count=2
        )

        tc1 = {"finish": {0, 1, 2}}
        self.assertRaises(
            excp.PuzzleException, cfg.validate_finish, config=tc1, node_count=3
        )

        tc2 = {"finish": ["0", "1", "2"]}
        self.assertRaises(
            excp.PuzzleException, cfg.validate_finish, config=tc2, node_count=2
        )

        tc3 = {"nada": None}
        self.assertEqual(cfg.validate_finish(config=tc3, node_count=2), None)

        tc4 = {"finish": [-1, 1, 2]}
        self.assertRaises(
            excp.PuzzleException, cfg.validate_finish, config=tc4, node_count=3
        )

        tc5 = {"finish": [0, 0, 1, 2]}
        self.assertRaises(
            excp.PuzzleException, cfg.validate_finish, config=tc5, node_count=5
        )

    def test_validate_final_count(self) -> None:
        tc0 = {"nada": None}
        self.assertEqual(cfg.validate_finish(config=tc0, node_count=2), None)

        tc1 = {"final_count": 3}
        self.assertEqual(cfg.validate_final_count(config=tc1, node_count=10), 3)

        tc2 = {"final_count": 3}
        self.assertRaises(
            excp.PuzzleException,
            cfg.validate_final_count,
            config=tc2,
            node_count=2,
        )

        tc3 = {"final_count": -1}
        self.assertRaises(
            excp.PuzzleException,
            cfg.validate_final_count,
            config=tc3,
            node_count=4,
        )

        tc4 = {"final_count": "invalid"}
        self.assertRaises(
            excp.PuzzleException,
            cfg.validate_final_count,
            config=tc4,
            node_count=4,
        )


if __name__ == "__main__":
    unittest.main()
