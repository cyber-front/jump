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

# File: enumerations.py
#
# Description: Contains a variety of helper enumeration classes.

import enum


class SearchMethod(enum.Enum):
    """
    This class will be used to specify the search algorithm to use
    to solve the puzzle.
    """

    DEPTH_FIRST = enum.auto()
    BREADTH_FIRST = enum.auto()


class SolutionScope(enum.Enum):
    """
    This class is used to specify the number of results to return.  SINGLE
    specifies returning the first solution detected, while MULTIPLE returns all
    possible solutions.  The MULTIPLE approach can only finde all solutions by
    performing an exhaustive search, so, it's likely to take longer than
    finding only the first one and going home with that.
    """

    SINGLE = enum.auto()
    MULTIPLE = enum.auto()


class CheckerMethod(enum.Enum):
    """
    This class describes how to check for a solution, either by the position of
    the pegs in the board, or by the number of pegs remaining without the
    ability to make any additional moves.
    """

    POSITION = enum.auto()
    COUNT = enum.auto()
