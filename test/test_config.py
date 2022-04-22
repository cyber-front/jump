#! /bin/python3

import sys

sys.path.append("../src")

import config
import exception
import unittest


class TestConfig(unittest.TestCase):
    def test_validate_description(self) -> None:
        tc0 = {"description": "test"}
        self.assertEqual(config.validate_description(config=tc0), "test")

        tc1 = {"description": 10.3}
        self.assertRaises(
            exception.PuzzleException, config.validate_description, config=tc1
        )

        tc2 = {"nada": None}
        self.assertEqual(
            config.validate_description(config=tc2), "Generic Jump Puzzle Solution"
        )

    def test_validate_scope(self) -> None:
        tc0 = {"scope": "SINGLE"}
        self.assertEqual(config.validate_scope(config=tc0), config.SolutionScope.SINGLE)

        tc1 = {"scope": "MULTIPLE"}
        self.assertEqual(
            config.validate_scope(config=tc1), config.SolutionScope.MULTIPLE
        )

        tc2 = {"scope": "invalid"}
        self.assertRaises(exception.PuzzleException, config.validate_scope, config=tc2)

        tc3 = {"nada": None}
        self.assertEqual(config.validate_scope(config=tc3), config.SolutionScope.SINGLE)

    def test_validate_method(self) -> None:
        tc0 = {"method": "DEPTH_FIRST"}
        self.assertEqual(
            config.validate_method(config=tc0), config.SearchMethod.DEPTH_FIRST
        )

        tc1 = {"method": "BREADTH_FIRST"}
        self.assertEqual(
            config.validate_method(config=tc1), config.SearchMethod.BREADTH_FIRST
        )

        tc2 = {"method": "invalid"}
        self.assertRaises(exception.PuzzleException, config.validate_method, config=tc2)

        tc3 = {"nada": None}
        self.assertEqual(
            config.validate_method(config=tc3), config.SearchMethod.DEPTH_FIRST
        )

    def test_validate_start(self) -> None:
        tc0 = {"start": [0, 1, 2]}
        self.assertEqual(config.validate_start(config=tc0, node_count=3), {0, 2, 1})
        self.assertRaises(
            exception.PuzzleException, config.validate_start, config=tc0, node_count=2
        )

        tc1 = {"start": {0, 1, 2}}
        self.assertRaises(
            exception.PuzzleException, config.validate_start, config=tc1, node_count=3
        )

        tc2 = {"start": ["0", "1", "2"]}
        self.assertRaises(
            exception.PuzzleException, config.validate_start, config=tc2, node_count=2
        )

        tc3 = {"nada": None}
        self.assertRaises(
            exception.PuzzleException, config.validate_start, config=tc3, node_count=2
        )

        tc4 = {"start": [-1, 1, 2]}
        self.assertRaises(
            exception.PuzzleException, config.validate_start, config=tc4, node_count=3
        )

        tc5 = {"start": [0, 0, 1, 2]}
        self.assertRaises(
            exception.PuzzleException, config.validate_start, config=tc5, node_count=5
        )

    def test_validate_finish(self) -> None:
        tc0 = {"finish": [0, 1, 2]}
        self.assertEqual(config.validate_finish(config=tc0, node_count=3), {0, 2, 1})
        self.assertRaises(
            exception.PuzzleException, config.validate_finish, config=tc0, node_count=2
        )

        tc1 = {"finish": {0, 1, 2}}
        self.assertRaises(
            exception.PuzzleException, config.validate_finish, config=tc1, node_count=3
        )

        tc2 = {"finish": ["0", "1", "2"]}
        self.assertRaises(
            exception.PuzzleException, config.validate_finish, config=tc2, node_count=2
        )

        tc3 = {"nada": None}
        self.assertEqual(config.validate_finish(config=tc3, node_count=2), None)

        tc4 = {"finish": [-1, 1, 2]}
        self.assertRaises(
            exception.PuzzleException, config.validate_finish, config=tc4, node_count=3
        )

        tc5 = {"finish": [0, 0, 1, 2]}
        self.assertRaises(
            exception.PuzzleException, config.validate_finish, config=tc5, node_count=5
        )

    def test_validate_final_count(self) -> None:
        tc0 = {"nada": None}
        self.assertEqual(config.validate_finish(config=tc0, node_count=2), None)

        tc1 = {"final_count": 3}
        self.assertEqual(config.validate_final_count(config=tc1, node_count=10), 3)

        tc2 = {"final_count": 3}
        self.assertRaises(
            exception.PuzzleException,
            config.validate_final_count,
            config=tc2,
            node_count=2,
        )

        tc3 = {"final_count": -1}
        self.assertRaises(
            exception.PuzzleException,
            config.validate_final_count,
            config=tc3,
            node_count=4,
        )

        tc4 = {"final_count": "invalid"}
        self.assertRaises(
            exception.PuzzleException,
            config.validate_final_count,
            config=tc4,
            node_count=4,
        )


if __name__ == "__main__":
    unittest.main()
