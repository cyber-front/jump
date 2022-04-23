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
import typing as ty
import exception as excp
import os.path as osp
import pandas as pd
import math


@dataclass(frozen=True)
class Board:
    """
    The class describes a board for a jump game
    """

    transitions: ty.Dict[int, ty.Dict[int, int]]
    nodes: int
    edges: int
    directions: int

    def transit(self, node: int, direction: int) -> int:
        return self.transitions[node][direction]


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
