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

# File: board.py
#
# Description: Specifies the board topology and manages the solution space search


from dataclasses import dataclass
import typing as ty
import exception as excp
import os.path as osp
import pandas as pd
import math
import step
import enumerations as en
import logging

""" Sequence of states intended to define a solution path from the start to an ending state once discovered """
StepList = ty.List[step.Step]

""" Collection of paths which satisfy the ending condition from the starting state """
PathList = ty.List[StepList]

""" A function for picking the next path to test for being the endstate and the remainng states to check """
Picker = ty.Callable[[PathList], ty.Tuple[StepList, PathList]]

""" A function for checking if the final state in the path satisfies the criteria being searched for """
Checker = ty.Callable[[StepList], bool]


@dataclass(frozen=True, slots=True)
class Board:
    """
    The class describes a board for a jump game.

    :param transitions: Adjacency graph for the board
    :param nodes: Number of nodes on the board
    :param edges: Number of edges connecting nodes on the board.
    :param directions: Maximum number of possible directions to adjacent nodes
    """

    transitions: ty.Dict[int, ty.Dict[int, int]]
    nodes: int
    edges: int
    directions: int

    def transit(self, node: int, direction: int) -> int:
        """
        Given a node and a direction, determine the node which results from the
        transition from the starting node and the direction of travel.

        :param node: Starting node
        :param direction: Direction of travel
        :return: Node arrived at when transiting from starting node and traveling in the given direction
        """
        return self.transitions[node][direction]

    def direction(self, loc_a: int, loc_b: int) -> ty.Union[int, None]:
        """
        Given two nodes, determine the direction needed to travel from the first to the second.  If there
        is no single transit from the first node to the second, return None

        :param loc_a: Starting location
        :param loc_b: Finishing location
        :return: Direction permitting travel from loc_a to loc_b in one jump; None of no solution exists
        """
        for dir in range(self.direction):
            if self.transit(node=loc_a, direction=dir) == loc_b:
                return dir
        return None

    def validate(self, step: step.Step) -> bool:
        """
        Validate a move to ensure it is legal.

        :param step: Move to validate
        :return: True exactly when the move described in the step is valid
        """
        dir = self.direction(loc_a=step.move, loc_b=step.jump)
        if dir is None:
            return False

        jump = self.transit(node=step.move, direction=dir)
        if jump is None:
            return False

        rest = self.transit(node=jump, direction=dir)
        if rest is None:
            return False

        if jump != step.jump or rest != step.land:
            return False

        return step.validate()

    def do_move(
        self, state: step.State, move: int, dir: int, jump: int
    ) -> step.Step | None:
        if jump not in state:
            return None
        transits1 = self.transitions[jump]
        if dir not in transits1:
            return None
        land = transits1[dir]
        if land in state:
            return None

        final_state = state.copy()
        final_state.remove(move)
        final_state.remove(jump)
        final_state.add(land)

        return step.Step(
            start_state=state,
            move=move,
            jump=jump,
            land=land,
            final_state=final_state,
        )

    def moves(self, start_state: step.State) -> StepList:
        """
        Given a board position and topology, computer the list of possible legal
        moves which can be made.  If it returns the empty list, no moves are possible

        :param state: Location of the pegs in the game board
        :param board: Board topology
        :return: List of legal next steps given the board and the current position of the game pieces
        """
        logging.debug(f"Board.moves")
        logging.debug(f"\t start_state: {start_state}")

        move_list = [
            self.do_move(state=start_state, move=move, dir=dir, jump=jump)
            for move in start_state
            for dir, jump in self.transitions[move].items()
        ]

        filtered_moves = list(filter(lambda x: x is not None, move_list))

        logging.debug(f"Board.moves - returning filtered_moves {filtered_moves}")
        return filtered_moves

    def next_paths(self, path: StepList) -> PathList:
        """
        Compute the next set of paths given a starting path and a board.

        :param path: Starting point to get the next set of paths
        :param board: Board topology to use for generating next paths
        :return: Collection of paths subsequent to the given path
        """
        logging.debug(f"Board.next_paths - path: {path}")
        moves = self.moves(start_state=path[-1].final_state)
        paths = [path.copy() + [i] for i in moves]

        logging.debug(f"Board.next_paths - returning paths: {paths}")
        return paths

    def solve(
        self,
        start: step.State,
        picker: Picker,
        checker: Checker,
        scope: en.SolutionScope,
        min_pegs: int,
    ) -> PathList:
        """
        This function finds a path of moves from the start state until the check state is satisfied.

        :param start: Start state to begin search
        :param picker: Function to separate the next path to examine from the list of paths awaiting examination
        :param checker: Function to determine if a path satisfies the endstate condition
        :param scope: Flag used to determine whether to return a single solution or all possible solutions
        :param min_pegs: Minimum number of pegs in the solution; checked to cull branches which cannot possibly satisfy the endstate condition
        :return: List of paths, all of which satisfies the intended criteria
        """

        logging.info("Board.solve")
        candidates = [[x] for x in self.moves(start_state=start)]
        solutions = []
        while len(candidates) > 0:
            logging.debug(f"\t candidates: {candidates}")
            logging.debug(f"\t solutions: {solutions}")

            next, candidates = picker(candidates)
            logging.debug(f"\t next: {next}")

            if len(next[-1].final_state) < min_pegs:
                logging.debug(
                    f"\t too short - min_pegs={min_pegs} / len={len(next[-1].final_state)}"
                )
                continue
            if checker(path=next):
                logging.info(f"found: {next}")
                solutions.append(next)
                if scope == en.SolutionScope.SINGLE:
                    return solutions
            else:
                candidates.extend(self.next_paths(path=next))
        return solutions


def get_transitions(row: pd.Series, nodes: int) -> ty.Dict[int, int]:
    """
    Extract the transitions from a pandas Series

    :param row: Series instance containing the transitions
    :param nodes: Number of nodes used to exclude invalid transitions
    :return: Dict containing the transitions in the row
    """
    transitions = {}
    for direction, destination in row.items():
        if not math.isnan(destination) and int(destination) in range(nodes):
            transitions[direction] = int(destination)
    return transitions


def read_board(board_filename: str) -> Board:
    """
    Read a board from the CSV file containing the transitions

    :param board_filename: Name of the file containing the transitions
    :return: Board object describing the board
    """
    if not isinstance(board_filename, str):
        raise excp.PuzzleException(
            f"Expected the board filename to be a string.  Found {board_filename} / {type(board_filename)}."
        )
    if not osp.exists(path=board_filename):
        raise excp.PuzzleException(f"Board file not found {board_filename}")
    if not osp.isfile(path=board_filename):
        raise excp.PuzzleException(
            f"Given board file name {board_filename} is not a file"
        )

    df = pd.read_csv(board_filename, header=None)
    nodes = df.shape[0]
    directions = df.shape[1]
    edges = 0

    transitions: ty.Dict[int, ty.Dict[int, int]] = {}
    for node, data in df.iterrows():
        transitions[node] = get_transitions(row=data, nodes=nodes)
        edges += len(transitions[node])

    return Board(
        transitions=transitions, nodes=nodes, edges=edges, directions=directions
    )
