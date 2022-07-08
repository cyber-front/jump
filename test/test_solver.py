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
import logging
import unittest
import functools as ft
import typing as ty

sys.path.append("../src")

import board
import solver
import enumerations as en


class TestSolver(unittest.TestCase):
    def test_moves_00(self) -> None:
        bd = board.Board(
            transitions={0: {0: 1, 1: 2}, 1: {0: 2, 1: 0}, 2: {0: 0, 1: 1}},
            nodes=3,
            edges=6,
            directions=2,
        )

        next = bd.moves(start_state={0, 1})

        logging.info(f"TestSolver.test_next - next: {next}")

        self.assertEqual(len(next), 2)
        self.assertEqual(len(next[0].final_state), 1)
        self.assertEqual(next[0].final_state, {2})
        self.assertEqual(len(next[1].final_state), 1)
        self.assertEqual(next[1].final_state, {2})

    def test_moves_01(self) -> None:
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        next = bd.moves(start_state={0, 1})

        logging.info(f"TestSolver.test_next - next: {next}")

        self.assertEqual(len(next), 2)
        self.assertEqual(len(next[0].final_state), 1)
        self.assertEqual(len(next[1].final_state), 1)
        self.assertNotEqual(next[0].final_state, next[1].final_state)
        self.assertNotEqual(2 in next[0].final_state, 2 in next[1].final_state)
        self.assertNotEqual(3 in next[0].final_state, 3 in next[1].final_state)

    def test_depth_first(self) -> None:
        path = [{0, 1, 2}, {0, 2, 3}, {4, 5, 6}]
        next, remaining = solver.pick_next_depth_first(path)

        self.assertEqual(len(remaining), len(path) - 1)
        self.assertEqual(next, path[-1])
        for idx in range(len(remaining)):
            self.assertEqual(remaining[idx], path[idx])

    def test_breadth_first(self) -> None:
        path = [{0, 1, 2}, {0, 2, 3}, {4, 5, 6}]
        next, remaining = solver.pick_next_breadth_first(path)

        self.assertEqual(len(remaining), len(path) - 1)
        self.assertEqual(next, path[0])
        for idx in range(len(remaining)):
            self.assertEqual(remaining[idx], path[idx + 1])

    def test_next_paths_00(self) -> None:
        logging.info("TestSolver.test_next_paths_000")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        path_starts = [[x] for x in bd.moves(start_state={0, 1, 2})]
        logging.debug(f"\t path_starts: {path_starts}")

        for start in path_starts:
            logging.debug(f"\t TestSolver.test_next_paths_000 loop start ****")
            logging.debug(f"\t start: {start}")
            moves = bd.next_paths(path=start)
            logging.debug(f"\t moves: {len(moves)} / {moves}")
            logging.debug(f"\t moves[0]: {len(moves[0])} / {moves[0]}")
            logging.debug(f"\t moves[1]: {len(moves[1])} / {moves[1]}")

            self.assertEqual(len(moves), 2)
            self.assertEqual(len(moves[0]), 2)
            fs0 = moves[0][-1].final_state
            fs1 = moves[1][-1].final_state
            self.assertEqual(len(fs0), len(fs1))
            self.assertEqual(len(fs0.intersection(fs1)), 0)

    def test_next_paths_01(self) -> None:
        logging.info("TestSolver.test_next_paths_001")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        path_starts = [[x] for x in bd.moves(start_state={0, 1, 3})]
        logging.debug(f"\t path_starts: {path_starts}")

        for start in path_starts:
            logging.debug(f"\t TestSolver.test_next_paths_001 loop start ****")
            logging.debug(f"\t start: {start}")
            moves = bd.next_paths(path=start)
            logging.debug(f"\t moves: {len(moves)} / {moves}")
            logging.debug(f"\t moves[0]: {len(moves[0])} / {moves[0]}")
            logging.debug(f"\t moves[1]: {len(moves[1])} / {moves[1]}")

            self.assertEqual(len(moves), 2)
            self.assertEqual(len(moves[0]), 2)
            fs0 = moves[0][-1].final_state
            fs1 = moves[1][-1].final_state
            self.assertEqual(len(fs0), len(fs1))
            self.assertEqual(len(fs0.intersection(fs1)), 0)

    def check_counts(
        self, state: board.StepList, bd: board.Board, checks: ty.Dict[int, bool]
    ) -> None:
        for i, exp in checks.items():
            actual = solver.check_solution_count(path=state, board=bd, final_count=i)
            self.assertEqual(actual, exp)

    def test_solution_checkers_00(self) -> None:
        logging.info(f"test_solution_checkers_00")
        bd = board.Board(
            transitions={0: {0: 1, 1: 2}, 1: {0: 2, 1: 0}, 2: {0: 0, 1: 1}},
            nodes=3,
            edges=6,
            directions=2,
        )

        starts = bd.moves(start_state={0, 1})
        logging.debug(f"\t starts: {starts}")

        self.assertEqual(len(starts), 2)

        expectations = {0: False, 1: True, 2: False, 3: False}
        for state in starts:
            self.check_counts(state=[state], bd=bd, checks=expectations)

    def test_solution_checkers_01(self) -> None:
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        starts = bd.moves(start_state={0, 1})
        self.assertEqual(len(starts), 2)
        soln00 = (solver.check_solution_state(path=[starts[0]], finish={2}),)
        soln01 = (solver.check_solution_state(path=[starts[1]], finish={2}),)
        soln10 = (solver.check_solution_state(path=[starts[0]], finish={3}),)
        soln11 = (solver.check_solution_state(path=[starts[1]], finish={3}),)

        self.assertNotEqual(soln00, soln01)
        self.assertNotEqual(soln10, soln11)

        self.assertNotEqual(soln00, soln10)
        self.assertNotEqual(soln01, soln11)

        self.assertEqual(soln00, soln11)
        self.assertEqual(soln01, soln10)

        expectations = {0: False, 1: True, 2: False, 3: False}

        for state in starts:
            self.check_counts(state=[state], bd=bd, checks=expectations)

    def test_solution_checkers_02(self) -> None:
        logging.info("TestSolver.test_solution_checkers_02")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 4},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 4, 1: 2},
                4: {0: 0, 1: 3},
            },
            nodes=5,
            edges=10,
            directions=2,
        )
        logging.debug(f"\t bd: {bd}")

        starts = bd.moves(start_state={0, 1, 3})
        logging.debug(f"\t starts: {starts}")

        moves = bd.next_paths(path=starts)
        logging.debug(f"\t moves: {moves}")

        expectations = {0: False, 1: True, 2: False, 3: False}
        logging.debug(f"\t expectations: {expectations}")

        for state in moves:
            self.check_counts(state=state, bd=bd, checks=expectations)

    def test_solution_checkers_03(self) -> None:
        logging.info("TestSolver.test_solution_checkers_02")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 4},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 4, 1: 2},
                4: {0: 0, 1: 3},
            },
            nodes=5,
            edges=10,
            directions=2,
        )
        logging.debug(f"\t bd: {bd}")

        starts = bd.moves(start_state={0, 1, 2})
        logging.debug(f"\t starts: {starts}")

        expectations = {0: False, 1: False, 2: True, 3: False}
        logging.debug(f"\t expectations: {expectations}")

        for state in starts:
            self.check_counts(state=[state], bd=bd, checks=expectations)

    def test_executive_00(self) -> None:
        logging.info("TestSolver.test_executive_00")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        start = {0, 1, 2}
        test_cases = [
            {"state": {0}, "count": 1},
            {"state": {1}, "count": 2},
            {"state": {2}, "count": 1},
            {"state": {3}, "count": 0},
            {"state": {0, 1}, "count": 0},
            {"state": {0, 2}, "count": 0},
            {"state": {0, 3}, "count": 1},
            {"state": {1, 2}, "count": 0},
            {"state": {1, 3}, "count": 0},
            {"state": {2, 3}, "count": 1},
            {"state": {0, 1, 2}, "count": 0},
            {"state": {0, 1, 3}, "count": 0},
            {"state": {0, 2, 3}, "count": 0},
            {"state": {1, 2, 3}, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")
            checker = ft.partial(solver.check_solution_state, finish=state)
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_breadth_first,
                checker=checker,
                scope=en.SolutionScope.MULTIPLE,
                min_pegs=len(state),
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(solution[-1].final_state, state)

    def test_executive_01(self) -> None:
        logging.info("TestSolver.test_executive_01")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        start = {0, 1, 2}
        test_cases = [
            {"state": {0}, "count": 1},
            {"state": {1}, "count": 1},
            {"state": {2}, "count": 1},
            {"state": {3}, "count": 0},
            {"state": {0, 1}, "count": 0},
            {"state": {0, 2}, "count": 0},
            {"state": {0, 3}, "count": 1},
            {"state": {1, 2}, "count": 0},
            {"state": {1, 3}, "count": 0},
            {"state": {2, 3}, "count": 1},
            {"state": {0, 1, 2}, "count": 0},
            {"state": {0, 1, 3}, "count": 0},
            {"state": {0, 2, 3}, "count": 0},
            {"state": {1, 2, 3}, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")
            checker = ft.partial(solver.check_solution_state, finish=state)
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_breadth_first,
                checker=checker,
                scope=en.SolutionScope.SINGLE,
                min_pegs=len(state),
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(solution[-1].final_state, state)

    def test_executive_02(self) -> None:
        logging.info("TestSolver.test_executive_02")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        start = {0, 1, 2}
        test_cases = [
            {"state": {0}, "count": 1},
            {"state": {1}, "count": 2},
            {"state": {2}, "count": 1},
            {"state": {3}, "count": 0},
            {"state": {0, 1}, "count": 0},
            {"state": {0, 2}, "count": 0},
            {"state": {0, 3}, "count": 1},
            {"state": {1, 2}, "count": 0},
            {"state": {1, 3}, "count": 0},
            {"state": {2, 3}, "count": 1},
            {"state": {0, 1, 2}, "count": 0},
            {"state": {0, 1, 3}, "count": 0},
            {"state": {0, 2, 3}, "count": 0},
            {"state": {1, 2, 3}, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")
            checker = ft.partial(solver.check_solution_state, finish=state)
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_depth_first,
                checker=checker,
                scope=en.SolutionScope.MULTIPLE,
                min_pegs=len(state),
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(solution[-1].final_state, state)

    def test_executive_03(self) -> None:
        logging.info("TestSolver.test_executive_03")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        start = {0, 1, 2}
        test_cases = [
            {"state": {0}, "count": 1},
            {"state": {1}, "count": 1},
            {"state": {2}, "count": 1},
            {"state": {3}, "count": 0},
            {"state": {0, 1}, "count": 0},
            {"state": {0, 2}, "count": 0},
            {"state": {0, 3}, "count": 1},
            {"state": {1, 2}, "count": 0},
            {"state": {1, 3}, "count": 0},
            {"state": {2, 3}, "count": 1},
            {"state": {0, 1, 2}, "count": 0},
            {"state": {0, 1, 3}, "count": 0},
            {"state": {0, 2, 3}, "count": 0},
            {"state": {1, 2, 3}, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")
            checker = ft.partial(solver.check_solution_state, finish=state)
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_depth_first,
                checker=checker,
                scope=en.SolutionScope.SINGLE,
                min_pegs=len(state),
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(solution[-1].final_state, state)

    def test_executive_04(self) -> None:
        logging.info("TestSolver.test_executive_04")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        start = {0, 1, 2}
        test_cases = [
            {"state": 0, "count": 0},
            {"state": 1, "count": 4},
            {"state": 2, "count": 0},
            {"state": 3, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")
            checker = ft.partial(
                solver.check_solution_count, board=bd, final_count=state
            )
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_breadth_first,
                checker=checker,
                scope=en.SolutionScope.MULTIPLE,
                min_pegs=state,
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(len(solution[-1].final_state), state)

    def test_executive_05(self) -> None:
        logging.info("TestSolver.test_executive_05")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        start = {0, 1, 2}
        test_cases = [
            {"state": 0, "count": 0},
            {"state": 1, "count": 1},
            {"state": 2, "count": 0},
            {"state": 3, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")
            checker = ft.partial(
                solver.check_solution_count, board=bd, final_count=state
            )
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_breadth_first,
                checker=checker,
                scope=en.SolutionScope.SINGLE,
                min_pegs=state,
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(len(solution[-1].final_state), state)

    def test_executive_06(self) -> None:
        logging.info("TestSolver.test_executive_06")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        start = {0, 1, 2}
        test_cases = [
            {"state": 0, "count": 0},
            {"state": 1, "count": 4},
            {"state": 2, "count": 0},
            {"state": 3, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")
            checker = ft.partial(
                solver.check_solution_count, board=bd, final_count=state
            )
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_depth_first,
                checker=checker,
                scope=en.SolutionScope.MULTIPLE,
                min_pegs=state,
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(len(solution[-1].final_state), state)

    def test_executive_07(self) -> None:
        logging.info("TestSolver.test_executive_07")
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 3},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 0, 1: 2},
            },
            nodes=4,
            edges=8,
            directions=2,
        )

        start = {0, 1, 2}
        test_cases = [
            {"state": 0, "count": 0},
            {"state": 1, "count": 1},
            {"state": 2, "count": 0},
            {"state": 3, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")
            checker = ft.partial(
                solver.check_solution_count, board=bd, final_count=state
            )
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_depth_first,
                checker=checker,
                scope=en.SolutionScope.SINGLE,
                min_pegs=state,
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(len(solution[-1].final_state), state)

    def test_executive_10(self) -> None:
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 4},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 4, 1: 2},
                4: {0: 0, 1: 3},
            },
            nodes=5,
            edges=10,
            directions=2,
        )

        start = {0, 1, 3}
        test_cases = [
            {"state": {0}, "count": 1},
            {"state": {1}, "count": 1},
            {"state": {2}, "count": 1},
            {"state": {3}, "count": 0},
            {"state": {4}, "count": 1},
            {"state": {0, 1}, "count": 0},
            {"state": {0, 2}, "count": 0},
            {"state": {0, 3}, "count": 0},
            {"state": {0, 4}, "count": 0},
            {"state": {1, 2}, "count": 0},
            {"state": {1, 3}, "count": 0},
            {"state": {1, 4}, "count": 0},
            {"state": {2, 3}, "count": 1},
            {"state": {2, 4}, "count": 0},
            {"state": {3, 4}, "count": 1},
            {"state": {0, 1, 2}, "count": 0},
            {"state": {0, 1, 3}, "count": 0},
            {"state": {0, 1, 4}, "count": 0},
            {"state": {0, 2, 3}, "count": 0},
            {"state": {0, 2, 4}, "count": 0},
            {"state": {1, 2, 3}, "count": 0},
            {"state": {1, 2, 4}, "count": 0},
            {"state": {2, 3, 4}, "count": 0},
            {"state": {0, 1, 2, 3}, "count": 0},
            {"state": {0, 1, 2, 4}, "count": 0},
            {"state": {0, 1, 3, 4}, "count": 0},
            {"state": {0, 2, 3, 4}, "count": 0},
            {"state": {1, 2, 3, 4}, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")

            checker = ft.partial(solver.check_solution_state, finish=state)
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_breadth_first,
                checker=checker,
                scope=en.SolutionScope.MULTIPLE,
                min_pegs=len(state),
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(solution[-1].final_state, state)

    def test_executive_11(self) -> None:
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 4},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 4, 1: 2},
                4: {0: 0, 1: 3},
            },
            nodes=5,
            edges=10,
            directions=2,
        )

        start = {0, 1, 3}
        test_cases = [
            {"state": {0}, "count": 1},
            {"state": {1}, "count": 1},
            {"state": {2}, "count": 1},
            {"state": {3}, "count": 0},
            {"state": {4}, "count": 1},
            {"state": {0, 1}, "count": 0},
            {"state": {0, 2}, "count": 0},
            {"state": {0, 3}, "count": 0},
            {"state": {0, 4}, "count": 0},
            {"state": {1, 2}, "count": 0},
            {"state": {1, 3}, "count": 0},
            {"state": {1, 4}, "count": 0},
            {"state": {2, 3}, "count": 1},
            {"state": {2, 4}, "count": 0},
            {"state": {3, 4}, "count": 1},
            {"state": {0, 1, 2}, "count": 0},
            {"state": {0, 1, 3}, "count": 0},
            {"state": {0, 1, 4}, "count": 0},
            {"state": {0, 2, 3}, "count": 0},
            {"state": {0, 2, 4}, "count": 0},
            {"state": {1, 2, 3}, "count": 0},
            {"state": {1, 2, 4}, "count": 0},
            {"state": {2, 3, 4}, "count": 0},
            {"state": {0, 1, 2, 3}, "count": 0},
            {"state": {0, 1, 2, 4}, "count": 0},
            {"state": {0, 1, 3, 4}, "count": 0},
            {"state": {0, 2, 3, 4}, "count": 0},
            {"state": {1, 2, 3, 4}, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")

            checker = ft.partial(solver.check_solution_state, finish=state)
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_breadth_first,
                checker=checker,
                scope=en.SolutionScope.SINGLE,
                min_pegs=len(state),
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(solution[-1].final_state, state)

    def test_executive_12(self) -> None:
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 4},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 4, 1: 2},
                4: {0: 0, 1: 3},
            },
            nodes=5,
            edges=10,
            directions=2,
        )

        start = {0, 1, 3}
        test_cases = [
            {"state": {0}, "count": 1},
            {"state": {1}, "count": 1},
            {"state": {2}, "count": 1},
            {"state": {3}, "count": 0},
            {"state": {4}, "count": 1},
            {"state": {0, 1}, "count": 0},
            {"state": {0, 2}, "count": 0},
            {"state": {0, 3}, "count": 0},
            {"state": {0, 4}, "count": 0},
            {"state": {1, 2}, "count": 0},
            {"state": {1, 3}, "count": 0},
            {"state": {1, 4}, "count": 0},
            {"state": {2, 3}, "count": 1},
            {"state": {2, 4}, "count": 0},
            {"state": {3, 4}, "count": 1},
            {"state": {0, 1, 2}, "count": 0},
            {"state": {0, 1, 3}, "count": 0},
            {"state": {0, 1, 4}, "count": 0},
            {"state": {0, 2, 3}, "count": 0},
            {"state": {0, 2, 4}, "count": 0},
            {"state": {1, 2, 3}, "count": 0},
            {"state": {1, 2, 4}, "count": 0},
            {"state": {2, 3, 4}, "count": 0},
            {"state": {0, 1, 2, 3}, "count": 0},
            {"state": {0, 1, 2, 4}, "count": 0},
            {"state": {0, 1, 3, 4}, "count": 0},
            {"state": {0, 2, 3, 4}, "count": 0},
            {"state": {1, 2, 3, 4}, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")

            checker = ft.partial(solver.check_solution_state, finish=state)
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_depth_first,
                checker=checker,
                scope=en.SolutionScope.MULTIPLE,
                min_pegs=len(state),
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(solution[-1].final_state, state)

    def test_executive_13(self) -> None:
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 4},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 4, 1: 2},
                4: {0: 0, 1: 3},
            },
            nodes=5,
            edges=10,
            directions=2,
        )

        start = {0, 1, 3}
        test_cases = [
            {"state": {0}, "count": 1},
            {"state": {1}, "count": 1},
            {"state": {2}, "count": 1},
            {"state": {3}, "count": 0},
            {"state": {4}, "count": 1},
            {"state": {0, 1}, "count": 0},
            {"state": {0, 2}, "count": 0},
            {"state": {0, 3}, "count": 0},
            {"state": {0, 4}, "count": 0},
            {"state": {1, 2}, "count": 0},
            {"state": {1, 3}, "count": 0},
            {"state": {1, 4}, "count": 0},
            {"state": {2, 3}, "count": 1},
            {"state": {2, 4}, "count": 0},
            {"state": {3, 4}, "count": 1},
            {"state": {0, 1, 2}, "count": 0},
            {"state": {0, 1, 3}, "count": 0},
            {"state": {0, 1, 4}, "count": 0},
            {"state": {0, 2, 3}, "count": 0},
            {"state": {0, 2, 4}, "count": 0},
            {"state": {1, 2, 3}, "count": 0},
            {"state": {1, 2, 4}, "count": 0},
            {"state": {2, 3, 4}, "count": 0},
            {"state": {0, 1, 2, 3}, "count": 0},
            {"state": {0, 1, 2, 4}, "count": 0},
            {"state": {0, 1, 3, 4}, "count": 0},
            {"state": {0, 2, 3, 4}, "count": 0},
            {"state": {1, 2, 3, 4}, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")

            checker = ft.partial(solver.check_solution_state, finish=state)
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_depth_first,
                checker=checker,
                scope=en.SolutionScope.SINGLE,
                min_pegs=len(state),
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(solution[-1].final_state, state)

    def test_executive_14(self) -> None:
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 4},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 4, 1: 2},
                4: {0: 0, 1: 3},
            },
            nodes=5,
            edges=10,
            directions=2,
        )

        start = {0, 1, 3}
        test_cases = [
            {"state": 0, "count": 0},
            {"state": 1, "count": 4},
            {"state": 2, "count": 0},
            {"state": 3, "count": 0},
            {"state": 4, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")

            checker = ft.partial(
                solver.check_solution_count, board=bd, final_count=state
            )

            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_breadth_first,
                checker=checker,
                scope=en.SolutionScope.MULTIPLE,
                min_pegs=state,
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(len(solution[-1].final_state), state)

    def test_executive_15(self) -> None:
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 4},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 4, 1: 2},
                4: {0: 0, 1: 3},
            },
            nodes=5,
            edges=10,
            directions=2,
        )

        start = {0, 1, 3}
        test_cases = [
            {"state": 0, "count": 0},
            {"state": 1, "count": 1},
            {"state": 2, "count": 0},
            {"state": 3, "count": 0},
            {"state": 4, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")

            checker = ft.partial(
                solver.check_solution_count, board=bd, final_count=state
            )
            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_breadth_first,
                checker=checker,
                scope=en.SolutionScope.SINGLE,
                min_pegs=state,
            )

            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(len(solution[-1].final_state), state)

    def test_executive_16(self) -> None:
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 4},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 4, 1: 2},
                4: {0: 0, 1: 3},
            },
            nodes=5,
            edges=10,
            directions=2,
        )

        start = {0, 1, 3}
        test_cases = [
            {"state": 0, "count": 0},
            {"state": 1, "count": 4},
            {"state": 2, "count": 0},
            {"state": 3, "count": 0},
            {"state": 4, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")

            checker = ft.partial(
                solver.check_solution_count, board=bd, final_count=state
            )

            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_depth_first,
                checker=checker,
                scope=en.SolutionScope.MULTIPLE,
                min_pegs=state,
            )
            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(len(solution[-1].final_state), state)

    def test_executive_16(self) -> None:
        bd = board.Board(
            transitions={
                0: {0: 1, 1: 4},
                1: {0: 2, 1: 0},
                2: {0: 3, 1: 1},
                3: {0: 4, 1: 2},
                4: {0: 0, 1: 3},
            },
            nodes=5,
            edges=10,
            directions=2,
        )

        start = {0, 1, 3}
        test_cases = [
            {"state": 0, "count": 0},
            {"state": 1, "count": 1},
            {"state": 2, "count": 0},
            {"state": 3, "count": 0},
            {"state": 4, "count": 0},
        ]

        logging.debug(f"\t bd: {bd}")
        logging.debug(f"\t start: {start}")
        logging.debug(f"\t test_cases: {test_cases}")

        for test_case in test_cases:
            state = test_case["state"]
            count = test_case["count"]
            logging.debug(f"\t desired: {state}")
            logging.debug(f"\t solutiosn: {count}")

            checker = ft.partial(
                solver.check_solution_count, board=bd, final_count=state
            )

            solutions = bd.solve(
                start=start,
                picker=solver.pick_next_depth_first,
                checker=checker,
                scope=en.SolutionScope.SINGLE,
                min_pegs=state,
            )
            logging.debug(f"\t solutions: {len(solutions)} / {solutions}")

            self.assertEqual(len(solutions), count)
            for solution in solutions:
                self.assertEqual(len(solution[-1].final_state), state)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARN,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    unittest.main()
