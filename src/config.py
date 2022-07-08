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

# File: config.py
#
# Description: Specifies the features of the jump puzzle to solve including the starting and desired
# final state of the puzzle game board.

from dataclasses import dataclass
import os.path as osp
import typing
import json
import board as pb
import layout as pl
import exception as excp
import enumerations as en


@dataclass(frozen=True, slots=True)
class Config:
    """
    This class specifies the features to solve a particular jump puzzle.  The final
    state to search for is given by either the finish or final_count arguments.  When
    present, the finish parameter defines a specific layout the search algorithm will
    look for.  Alternatively, the final_count parameter can be used to specify the
    number of pegs remaining when no additional moves are possible.  If both are missing,
    the solutions is implicitly the set inversion of the start configuration.

    :param description: Brief description of the puzzle
    :param board: Board layout as a node adjacency graph
    :param layout: Layout of the board for display purposes
    :param start: Starting layout of the board
    :param method: Search method to use to find a solution
    :param scope: Specifies whether to search for a single solution or all possible solutions
    :param finish: When present, specified a specific final configuration
    :param final_count: When present, specifies the number of pegs in the final solution, but
    not in a particular location
    """

    description: str
    board: pb.Board
    layout: pl.Layout
    start: typing.Set[int]
    method: en.SearchMethod = en.SearchMethod.DEPTH_FIRST
    scope: en.SolutionScope = en.SolutionScope.SINGLE
    finish: typing.Optional[typing.Set[int]] = None
    final_count: typing.Optional[int] = None

    @property
    def checker(self) -> en.CheckerMethod:
        """
        This property supplies an enumeration value based on whether the config specifies
        looking for a specific final board layout or a number of pegs remaining without
        the possibility of making any additional moves.
        """
        return (
            en.CheckerMethod.COUNT if self.finish is None else en.CheckerMethod.POSITION
        )


def validate_description(config: dict) -> str:
    """
    Validate the description field and return the validated value to the calling routine.  This will
    raise an exception if a description is given in the config but it's not a string.

    :param config: Dictionary which may or may not contain a description field
    :return: A valid description, which may be a default value if none was present in the given dictionary
    """
    if "description" in config and not isinstance(config["description"], str):
        raise excp.PuzzleException(
            f"Expected optional field 'description' to container a string value if it was present.  Found: {config['description']}"
        )

    return (
        config["description"]
        if "description" in config
        else "Generic Jump Puzzle Solution"
    )


def validate_layout(config: dict, path: str = "./") -> pl.Layout:
    """
    Validate that the layout field in the config exists which is used to
    render the board in a graphical window, is a string, and contains a
    file name which we can resolve.  The filename may either be a fully
    specified path to the file name, or may be relative to the path given.
    If the path isn't given, it's assumed to be the local directory.

    :param config: A dictionary which should contain a string value with the
    file name where the board layout.
    :param path: Path serving as a starting point for a relative path to the
    board file
    :return: A puzzle board as an adjacency graph
    """
    if "layout" not in config:
        raise excp.PuzzleException(
            "File name containing layout configuration is missing."
        )

    if not isinstance(config["layout"], str):
        raise excp.PuzzleException(
            f"Expected file name for layout; value given: {config['layout']}"
        )

    layout_filename = (
        config["layout"] if osp.isfile(config["layout"]) else path + config["layout"]
    )

    if not osp.isfile(layout_filename):
        raise excp.PuzzleException(f"Board file not found: {layout_filename}")

    return pl.read_layout(layout_filename)


def validate_board(config: dict, path: str = "./") -> pb.Board:
    """
    Validate that the board field in the config exists, is a string, and
    contains a file name which we can resolve.  The filename may either be
    a fully specified path to the file name, or may be relative to the path
    given.  If the path isn't given, it's assumed to be the local directory.

    :param config: A dictionary which should contain a string value with the
    file name where the board configuration is given.
    :param path: Path serving as a starting point for a relative path to the
    board file
    :return: A puzzle board as an adjacency graph
    """
    if "board" not in config:
        raise excp.PuzzleException(
            "File name containing board configuration is missing."
        )

    if not isinstance(config["board"], str):
        raise excp.PuzzleException(
            f"Expected file name for board; value given: {config['board']}"
        )

    board_filename = (
        config["board"] if osp.isfile(config["board"]) else path + config["board"]
    )

    if not osp.isfile(board_filename):
        raise excp.PuzzleException(f"Board file not found: {board_filename}")

    return pb.read_board(board_filename)


def validate_scope(config: dict) -> en.SolutionScope:
    """
    This function extracts the solution scope from the configuraiton dict when it's present and returns
    that value to the calling routine.  If the solution scope isn't specified, a default value is returned.

    :param config: Dictionary optionally containing thesolution scope represetned as a string.
    :return: Valid scope which may be a default value if the scope isn't present in the config dictionary
    """
    # Validate the solution scope is either SINGLE or MULTIPLE, and set it to the correct value,
    # using the default value if it's not present in the dict.
    if "scope" in config:
        if not isinstance(config["scope"], str):
            raise excp.PuzzleException(
                f"Expected optional param 'scope' to be a string value.  Found {config['scope']}"
            )
        if config["scope"].upper() not in {"SINGLE", "MULTIPLE"}:
            raise excp.PuzzleException(
                f"Expected optional param 'scope' to be either 'SINGLE' or 'MULTIPLE'.  Found {config['scope']}"
            )

    return (
        en.SolutionScope.SINGLE
        if "scope" not in config
        else en.SolutionScope[config["scope"]]
    )


def validate_method(config: dict) -> en.SearchMethod:
    """
    This function extracts the search method from the configuraiton dict when it's present and returns
    that value to the calling routine.  If the method isn't specified, a default value is returned.

    :param config: Dictionary optionally containing the search method represetned as a string.
    :return: Valid search method which may be a default value if the method isn't present in the
    config dictionary
    """
    # Validate the solution scope is either SINGLE or MULTIPLE, and set it to the correct value,
    # using the default value if it's not present in the dict.
    if "method" in config:
        if not isinstance(config["method"], str):
            raise excp.PuzzleException(
                f"Expected optional param 'method' to be a string value.  Found {config['method']}"
            )
        if config["method"].upper() not in {"DEPTH_FIRST", "BREADTH_FIRST"}:
            raise excp.PuzzleException(
                f"Expected optional param 'method' to be either 'DEPTH_FIRST' or 'BREADTH_FIRST'.  Found {config['method']}"
            )

    return (
        en.SearchMethod.DEPTH_FIRST
        if "method" not in config
        else en.SearchMethod[config["method"].upper()]
    )


def validate_start(config: dict, node_count: int) -> typing.Sequence[int]:
    """
    This function extracts the starting peg layout on the board as a list of indices
    corresponding to the nodes with pegs.  The starting layout is validated to
    ensure it is correcty formatted with the values constrained to be non-negative integers
    between strictly less than the number of nodes.

    :param config: Configuration containing the starting layout information
    :param node_count: Number of nodes in the board used to check the starting locations of the pegs
    are associated with nodes in the puzzle
    :return: Validated list of nodes containing the starting positions of the puzzle pegs.
    """

    if "start" not in config:
        raise excp.PuzzleException("Expected 'start' field in configuration.")

    if not isinstance(config["start"], list):
        raise excp.PuzzleException(f"Expected 'start' to be a list on integer values")

    bad_list = set(
        filter(
            lambda x: not isinstance(x, int) or x < 0 or x >= node_count,
            config["start"],
        )
    )

    if len(bad_list) > 0:
        raise excp.PuzzleException(
            f"Start list should contain only integers between 0 and {node_count-1}.  Found elements {bad_list}"
        )

    if len(config["start"]) != len(set(config["start"])):
        raise excp.PuzzleException(
            f"Multiple values detected in 'start' list: {config['start']}"
        )

    return set(config["start"])


def validate_finish(
    config: dict, node_count: int
) -> typing.Union[typing.Sequence[int], None]:
    """
    This function extracts the desired final peg layout on the board as a list of indices
    corresponding to the nodes with pegs.  The finishing layout is validated to
    ensure it is correcty formatted with the values constrained to be non-negative integers
    between strictly less than the number of nodes.  The finishing layout is an optional field, and
    if it is missing, None is returned.

    :param config: Configuration containing the final layout information, if present
    :param node_count: Number of nodes in the board used to check the starting locations of the pegs
    are associated with nodes in the puzzle
    :return: Validated list of nodes containing the starting positions of the puzzle pegs.
    """

    if "finish" not in config:
        return None

    if not isinstance(config["finish"], list):
        raise excp.PuzzleException(f"Expected 'finish' to be a list on integer values")

    bad_list = list(
        filter(
            lambda x: not isinstance(x, int) or x < 0 or x >= node_count,
            config["finish"],
        )
    )

    if len(bad_list) > 0:
        raise excp.PuzzleException(
            f"Finish list should contain only integers between 0 and {node_count-1}.  Found elements {bad_list}"
        )

    if len(config["finish"]) != len(set(config["finish"])):
        raise excp.PuzzleException(
            f"Multiple values detected in 'start' list: {config['finish']}"
        )

    return set(config["finish"])


def validate_final_count(config: dict, node_count: int) -> typing.Union[int, None]:
    """
    This function validates the final count field if it is present in the configuration dictionary.
    If the field is not present, None is returned to the calling routine.  Otherwise the value
    is checked to ensure it doesn't violate any reasonable constraint and is returned to the calling
    routine.

    :param config: Dictionary which may contain the final count field
    :param node_count: Maximum number of pegs which can be accomodated in the final solution
    :return: number of pegs the final solutoion should hold if specified, or None if not
    """

    if "final_count" not in config:
        return None

    if (
        not isinstance(config["final_count"], int)
        or config["final_count"] < 0
        or config["final_count"] > node_count
    ):
        raise excp.PuzzleException(
            f"Final count should be a positive integer not exceeding {node_count}.  Found {config['final_count']}."
        )

    return config["final_count"]


def from_dict(config: dict, path: str = "./") -> Config:
    """
    Convert a dictionary containing the needed elements of the puzzle configuration to
    a PuzzleConfig.

    :param config: A dictionary containing the configuration information used to
    specify a puzzle along with the scope of the solutions to search for.
    :param path: Relative path used for locating files relative to the puzzle
    :return: Returns the puzzle configuration to the calling routine
    """
    description = validate_description(config=config)
    board = validate_board(config=config, path=path)
    layout = validate_layout(config=config, path=path)
    scope = validate_scope(config=config)
    method = validate_method(config=config)
    start = validate_start(config=config, node_count=board.nodes)
    finish = validate_finish(config=config, node_count=board.nodes)
    final_count = validate_final_count(config=config, node_count=board.nodes)

    if finish is not None and final_count is not None and len(finish) != final_count:
        raise excp.PuzzleException(
            f"Mismach between finish {finish} (having len {len(finish)} and final peg count {final_count}."
        )

    if finish is None and final_count is None:
        finish = set(range(board.nodes)) - start

    if final_count is None:
        final_count = len(finish)

    return Config(
        description=description,
        board=board,
        layout=layout,
        start=start,
        method=method,
        scope=scope,
        finish=finish,
        final_count=final_count,
    )


def config_factory(filename: str) -> Config:
    if not osp.exists(filename):
        raise FileExistsError(f"File {filename} not found.")

    with open(file=filename) as jf:
        config = json.load(jf)

    return from_dict(config=config, path=osp.dirname(filename) + "/")
