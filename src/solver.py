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

import functools as ft
import logging
import typing
import board
import config
import step
import enumerations as en


def pick_next_depth_first(
    candidates: board.PathList,
) -> typing.Tuple[board.StepList, board.PathList]:
    """
    Pick the next item to search for in a depth first search and return
    the remaining candidates with the one selected removed.

    :param candidates: List of candidate paths to reference
    :return: Next candidate to use and remaining candidates pending selection
    """
    return candidates[-1], candidates[:-1]


def pick_next_breadth_first(
    candidates: board.PathList,
) -> typing.Tuple[board.StepList, board.PathList]:
    """
    Pick the next item to search for in a breadth first search and return
    the remaining candidates with the one selected removed.

    :param candidates: List of candidate paths to reference
    :return: Next candidate to use and remaining candidates pending selection
    """
    return candidates[0], candidates[1:]


def check_solution_state(path: board.StepList, finish: step.State) -> bool:
    """
    Check to see if the path concludes at the finish state and return the path, otherwise
    return None.

    :param path: Path, the last state of which is checked to see it satisfies the finished state
    :param finish: Final state to search for and against which to check the given path
    :return: Path if it concludes at the finish state; None otherwise
    """
    logging.debug(f"check_solution_state")
    logging.debug(f"\t path: {path}")
    logging.debug(f"\t finish: {finish}")
    logging.debug(f"\t final_state: {path[-1].final_state}")

    return path[-1].final_state == finish


def check_solution_count(
    path: board.StepList, board: board.Board, final_count: int
) -> bool:
    """
    Check to see if the path concludes with the specified number of pieces remaining on
    the board and that there are no additional legal moves which can be made.

    :param path: Path containing the final state to check against the peg count and subsequent moves
    :param board: Board topology to use to find additional steps
    :param final_count: Number of pegs in the target solution without any additional legal moves
    :return: True if the path leads to one of the desired final states
    """
    final_state = path[-1].final_state
    subsequent_moves = board.moves(start_state=final_state)
    logging.debug(f"check_solution_count")
    logging.debug(f"\t path: {path}")
    logging.debug(f"\t board: {board}")
    logging.debug(f"\t final_count: {final_count}")
    logging.debug(f"\t final_state: {len(final_state)} / {final_state}")
    logging.debug(f"\t subsequent_moves: {subsequent_moves}")

    return len(final_state) == final_count and len(subsequent_moves) == 0


def solve(cfg: config.Config) -> board.PathList:
    """
    Solve a game defined by the elements of the config instance passed

    :param cfg: Configuration of the game to solve
    :return: The list of solutions discovered given the configuration
    """

    # Map from the enum to the function to use to perform the search
    methods = {
        en.SearchMethod.BREADTH_FIRST: pick_next_breadth_first,
        en.SearchMethod.DEPTH_FIRST: pick_next_depth_first,
    }

    # Map from the endstate type, to the partial function to use to
    # check if the desired end state has been reached
    checkers = {
        en.CheckerMethod.COUNT: ft.partial(
            check_solution_count, board=cfg.board, final_count=cfg.final_count
        ),
        en.CheckerMethod.POSITION: ft.partial(check_solution_state, finish=cfg.finish),
    }

    # Number of pegs remaining in the solution to limit the scope
    # of the search when the solution has multiple pegs
    min_pegs = (
        len(cfg.finish) if cfg.checker == en.CheckerMethod.POSITION else cfg.final_count
    )

    # Go solve it
    return cfg.board.solve(
        start=cfg.start,
        picker=methods[cfg.method],
        checker=checkers[cfg.checker],
        scope=cfg.scope,
        min_pegs=min_pegs,
    )
