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
import typing
import board
import config

""" Desciption of the state of a board with elements in the set corresponding to peg locations on the board """
State = typing.Set[int]

""" Sequence of states intended to define a solution path from the start to an ending state once discovered """
Path = typing.List[State]

""" Collection of paths which satisfy the ending condition from the starting state """
PathList = typing.List[Path]

""" A function for picking the next path to test for being the endstate and the remainng states to check """
Picker = typing.Callable[[PathList], typing.Tuple[Path, PathList]]

""" A function for checking if the final state in the path satisfies the criteria being searched for """
Checker = typing.Callable[[Path], bool]


def moves(state: typing.Set[int], board: board.Board) -> Path:
    """
    Given a board position and topology, computer the list of possible legal
    moves which can be made.  If it returns the empty list, no moves are possible

    :param state: Location of the pegs in the game board
    :param board: Board topology
    :return: List of legal next steps given the board and the current position of the game pieces
    """
    move_list = []
    for location in state:
        transits0 = board.transitions[location]
        for dir, node in transits0.items():
            if node not in state:
                continue
            transits1 = board.transitions[node]
            if dir not in transits1:
                continue
            if transits1[dir] in state:
                continue

            next_state = state.copy()
            next_state.remove(location)
            next_state.remove(node)
            next_state.add(transits1[dir])

            if next_state not in move_list:
                move_list.append(next_state)

    return move_list


def pick_next_depth_first(
    candidates: PathList,
) -> typing.Tuple[Path, PathList]:
    """
    Pick the next item to search for in a depth first search and return
    the remaining candidates with the one selected removed.

    :param candidates: List of candidate paths to reference
    :return: Next candidate to use and remaining candidates pending selection
    """
    return candidates[-1], candidates[:-1]


def pick_next_breadth_first(
    candidates: PathList,
) -> typing.Tuple[Path, PathList]:
    """
    Pick the next item to search for in a breadth first search and return
    the remaining candidates with the one selected removed.

    :param candidates: List of candidate paths to reference
    :return: Next candidate to use and remaining candidates pending selection
    """
    return candidates[0], candidates[1:]


def next_paths(path: Path, board: board.Board) -> PathList:
    """
    Compute the next set of paths given a starting path and a board.

    :param path: Starting point to get the next set of paths
    :param board: Board topology to use for generating next paths
    :return: Collection of paths subsequent to the given path
    """
    paths = []
    for next_state in moves(state=path[-1], board=board):
        next_path = path.copy()
        next_path.append(next_state)
        paths.append(next_path)
    return paths


def check_solution_state(path: Path, finish: State) -> bool:
    """
    Check to see if the path concludes at the finish state and return the path, otherwise
    return None.

    :param path: Path, the last state of which is checked to see it satisfies the finished state
    :param finish: Final state to search for and against which to check the given path
    :return: Path if it concludes at the finish state; None otherwise
    """
    return path[-1] == finish


def check_solution_count(path: Path, board: board.Board, final_count: int) -> bool:
    """
    Check to see if the path concludes with the specified number of pieces remaining on
    the board and that there are no additional legal moves which can be made.

    :param path: Path containing the final state to check against the peg count and subsequent moves
    :param board: Board topology to use to find additional steps
    :param final_count: Number of pegs in the target solution without any additional legal moves
    :return: True if the path leads to one of the desired final states
    """
    return len(path[-1]) == final_count and len(moves(state=path[-1], board=board)) == 0


def solve_executive(
    board: board.Board,
    start: State,
    picker: Picker,
    checker: Checker,
    scope: config.SolutionScope,
    min_pegs: int,
) -> PathList:
    """
    This function finds a path of moves from the start state until the check state is satisfied.

    :param board: Board topology to search
    :param start: Start state to begin search
    :param picker: Function to separate the next path to examine from the list of paths awaiting examination
    :param checker: Function to determine if a path satisfies the endstate condition
    :param scope: Flag used to determine whether to return a single solution or all possible solutions
    :param min_pegs: Minimum number of pegs in the solution; checked to cull branches which cannot possibly satisfy the endstate condition
    :return: List of paths, all of which satisfies the intended criteria
    """
    candidates = next_paths(path=[start], board=board)
    solutions = []
    while len(candidates) > 0:
        next, candidates = picker(candidates)
        if len(next[-1]) < min_pegs:
            continue
        if checker(path=next):
            solutions.append(next)
            if scope == config.SolutionScope.SINGLE:
                return solutions
        else:
            candidates.extend(next_paths(path=next, board=board))
    return solutions


def solve(cfg: config.Config) -> PathList:
    """
    Solve a game defined by the elements of the config instance passed

    :param cfg: Configuration of the game to solve
    :return: The list of solutions discovered given the configuration
    """

    # Map from the enum to the function to use to perform the search
    methods = {
        config.SearchMethod.BREADTH_FIRST: pick_next_breadth_first,
        config.SearchMethod.DEPTH_FIRST: pick_next_depth_first,
    }

    # Map from the endstate type, to the partial function to use to
    # check if the desired end state has been reached
    checkers = {
        config.CheckerMethod.COUNT: ft.partial(
            check_solution_count, board=cfg.board, final_count=cfg.final_count
        ),
        config.CheckerMethod.POSITION: ft.partial(
            check_solution_state, finish=cfg.finish
        ),
    }

    # Number of pegs remaining in the solution to limit the scope
    # of the search when the solution has multiple pegs
    min_pegs = (
        len(cfg.finish)
        if cfg.checker == config.CheckerMethod.POSITION
        else cfg.final_count
    )

    # Go solve it
    return solve_executive(
        board=cfg.board,
        start=cfg.start,
        picker=methods[cfg.method],
        checker=checkers[cfg.checker],
        scope=cfg.scope,
        min_pegs=min_pegs,
    )
