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

import functools
import sys

sys.path.append("../src")

import unittest
import solver
import board
import functools as ft
import config


class TestSolver(unittest.TestCase):
    def test_next(self) -> None:
        board0 = board.Board(
            transitions={0: {0: 1, 1: 2}, 1: {0: 2, 1: 0}, 2: {0: 0, 1: 1}},
            nodes=3,
            edges=6,
            directions=2,
        )

        locations = {0, 1}

        next = solver.moves(state=locations, board=board0)

        self.assertEqual(len(next), 1)
        self.assertEqual(len(next[0]), 1)
        self.assertEqual(next[0], {2})

        board1 = board.Board(
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

        locations = {0, 1}

        next = solver.moves(state=locations, board=board1)

        self.assertEqual(len(next), 2)
        self.assertEqual(len(next[0]), 1)
        self.assertEqual(len(next[1]), 1)
        self.assertNotEqual(next[0], next[1])
        self.assertNotEqual(2 in next[0], 2 in next[1])
        self.assertNotEqual(3 in next[0], 3 in next[1])

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

    def test_next_paths(self) -> None:
        board0 = board.Board(
            transitions={0: {0: 1, 1: 2}, 1: {0: 2, 1: 0}, 2: {0: 0, 1: 1}},
            nodes=3,
            edges=6,
            directions=2,
        )

        locations = {0, 1}

        moves0 = solver.next_paths(path=[locations], board=board0)
        self.assertEqual(len(moves0), 1)
        self.assertEqual(len(moves0[0]), 2)
        self.assertEqual(moves0[0][0], {0, 1})
        self.assertEqual(moves0[0][1], {2})

        board1 = board.Board(
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

        moves1 = solver.next_paths(path=[locations], board=board1)
        self.assertEqual(len(moves1), 2)

        results = {2, 3}

        for move in moves1:
            self.assertEqual(len(move), 2)
            self.assertEqual(move[0], {0, 1})
            self.assertEqual(len(move[1]), 1)
            val = list(move[1])[0]
            self.assertTrue(val in results)
            results.remove(val)

    def test_solution_checkers(self) -> None:
        board0 = board.Board(
            transitions={0: {0: 1, 1: 2}, 1: {0: 2, 1: 0}, 2: {0: 0, 1: 1}},
            nodes=3,
            edges=6,
            directions=2,
        )

        state0 = {0, 1}
        finish0 = {2}

        moves0 = solver.next_paths(path=[state0], board=board0)
        self.assertTrue(solver.check_solution_state(path=moves0[0], finish=finish0))

        board1 = board.Board(
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

        state1 = {0, 1}
        finish1 = {2}
        moves1 = solver.next_paths(path=[state1], board=board1)
        self.assertNotEqual(
            solver.check_solution_state(path=moves1[0], finish=finish1),
            solver.check_solution_state(path=moves1[1], finish=finish1),
        )

        board2 = board.Board(
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

        state2 = {0, 1, 3}
        moves2 = solver.next_paths(path=[state2], board=board2)
        self.assertFalse(
            solver.check_solution_count(path=moves2[0], board=board2, final_count=2)
        )
        self.assertFalse(
            solver.check_solution_count(path=moves2[0], board=board2, final_count=3)
        )
        self.assertFalse(
            solver.check_solution_count(path=moves1[0], board=board1, final_count=2)
        )
        self.assertTrue(
            solver.check_solution_count(path=moves1[0], board=board1, final_count=1)
        )

    def test_executive_0(self) -> None:
        brd = board.Board(
            transitions={0: {0: 1, 1: 2}, 1: {0: 2, 1: 0}, 2: {0: 0, 1: 1}},
            nodes=3,
            edges=6,
            directions=2,
        )

        start = {0, 1}
        finish = {2}

        checker_a = ft.partial(solver.check_solution_state, finish=finish)
        solutions_a_bf_mul = solver.solve_executive(
            board=brd,
            start=start,
            picker=solver.pick_next_breadth_first,
            checker=checker_a,
            scope=config.SolutionScope.MULTIPLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_a_bf_mul), 1)
        self.assertEqual(solutions_a_bf_mul[0][-1], finish)

        solutions_a_bf_sing = solver.solve_executive(
            board=brd,
            start=start,
            picker=solver.pick_next_breadth_first,
            checker=checker_a,
            scope=config.SolutionScope.SINGLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_a_bf_sing), 1)
        self.assertEqual(solutions_a_bf_sing[0][-1], finish)

        solutions_a_df_mul = solver.solve_executive(
            board=brd,
            start=start,
            picker=solver.pick_next_depth_first,
            checker=checker_a,
            scope=config.SolutionScope.MULTIPLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_a_df_mul), 1)
        self.assertEqual(solutions_a_df_mul[0][-1], finish)

        solutions_a_df_sing = solver.solve_executive(
            board=brd,
            start=start,
            picker=solver.pick_next_depth_first,
            checker=checker_a,
            scope=config.SolutionScope.SINGLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_a_df_sing), 1)
        self.assertEqual(solutions_a_df_sing[0][-1], finish)

        checker_b = ft.partial(
            solver.check_solution_count, board=brd, final_count=len(finish)
        )

        solutions_b_bf_mul = solver.solve_executive(
            board=brd,
            start=start,
            picker=solver.pick_next_breadth_first,
            checker=checker_b,
            scope=config.SolutionScope.MULTIPLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_b_bf_mul), 1)
        self.assertEqual(solutions_b_bf_mul[0][-1], finish)

        solutions_b_bf_sing = solver.solve_executive(
            board=brd,
            start=start,
            picker=solver.pick_next_breadth_first,
            checker=checker_b,
            scope=config.SolutionScope.SINGLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_b_bf_sing), 1)
        self.assertEqual(solutions_b_bf_sing[0][-1], finish)

        solutions_b_df_mul = solver.solve_executive(
            board=brd,
            start=start,
            picker=solver.pick_next_depth_first,
            checker=checker_b,
            scope=config.SolutionScope.MULTIPLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_b_df_mul), 1)
        self.assertEqual(solutions_b_df_mul[0][-1], finish)

        solutions_b_df_sing = solver.solve_executive(
            board=brd,
            start=start,
            picker=solver.pick_next_depth_first,
            checker=checker_b,
            scope=config.SolutionScope.SINGLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_b_df_sing), 1)
        self.assertEqual(solutions_b_df_sing[0][-1], finish)

    def test_executive_1(self) -> None:
        brd = board.Board(
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

        state = {0, 1, 3}
        finish = {1}

        checker_a = ft.partial(solver.check_solution_state, finish=finish)
        solutions_a_bf_mul = solver.solve_executive(
            board=brd,
            start=state,
            picker=solver.pick_next_breadth_first,
            checker=checker_a,
            scope=config.SolutionScope.MULTIPLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_a_bf_mul), 1)
        self.assertEqual(solutions_a_bf_mul[0][-1], finish)

        solutions_a_bf_sing = solver.solve_executive(
            board=brd,
            start=state,
            picker=solver.pick_next_breadth_first,
            checker=checker_a,
            scope=config.SolutionScope.SINGLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_a_bf_sing), 1)
        self.assertEqual(solutions_a_bf_sing[0][-1], finish)

        solutions_a_df_mul = solver.solve_executive(
            board=brd,
            start=state,
            picker=solver.pick_next_depth_first,
            checker=checker_a,
            scope=config.SolutionScope.MULTIPLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_a_df_mul), 1)
        self.assertEqual(solutions_a_df_mul[0][-1], finish)

        solutions_a_df_sing = solver.solve_executive(
            board=brd,
            start=state,
            picker=solver.pick_next_depth_first,
            checker=checker_a,
            scope=config.SolutionScope.SINGLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_a_df_sing), 1)
        self.assertEqual(solutions_a_df_sing[0][-1], finish)

        checker_b = ft.partial(
            solver.check_solution_count, board=brd, final_count=len(finish)
        )

        solutions_b_bf_mul = solver.solve_executive(
            board=brd,
            start=state,
            picker=solver.pick_next_breadth_first,
            checker=checker_b,
            scope=config.SolutionScope.MULTIPLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_b_bf_mul), 4)
        for solution in solutions_b_bf_mul:
            self.assertEqual(len(solution), 3)
            self.assertEqual(len(solution[2]), 1)
            self.assertTrue(list(solution[2])[0] in {0, 1, 3})

        solutions_b_bf_sing = solver.solve_executive(
            board=brd,
            start=state,
            picker=solver.pick_next_breadth_first,
            checker=checker_b,
            scope=config.SolutionScope.SINGLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_b_bf_sing), 1)
        self.assertEqual(len(solutions_b_bf_sing[0]), 3)
        self.assertEqual(len(solutions_b_bf_sing[0][2]), 1)
        self.assertTrue(list(solutions_b_bf_sing[0][2])[0] in {0, 1, 3})

        solutions_b_df_mul = solver.solve_executive(
            board=brd,
            start=state,
            picker=solver.pick_next_depth_first,
            checker=checker_b,
            scope=config.SolutionScope.MULTIPLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_b_df_mul), 4)
        for solution in solutions_b_df_mul:
            self.assertEqual(len(solution), 3)
            self.assertEqual(len(solution[2]), 1)
            self.assertTrue(list(solution[2])[0] in {0, 1, 3})

        solutions_b_df_sing = solver.solve_executive(
            board=brd,
            start=state,
            picker=solver.pick_next_depth_first,
            checker=checker_b,
            scope=config.SolutionScope.SINGLE,
            min_pegs=len(finish),
        )
        self.assertTrue(len(solutions_b_df_sing), 1)
        self.assertEqual(len(solutions_b_df_sing[0]), 3)
        self.assertEqual(len(solutions_b_df_sing[0][2]), 1)
        self.assertTrue(list(solutions_b_df_sing[0][2])[0] in {0, 1, 3})


if __name__ == "__main__":
    unittest.main()
