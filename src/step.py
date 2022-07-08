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
import typing

State = typing.Set[int]


@dataclass(frozen=True, slots=True)
class Step:
    """
    This class defines a transition from one state to another.

    :param start_state: Starting state of the transition
    :param move: Location of the peg moving
    :param jump: Location of the peg being jumped
    :param land: Final location of the peg being moved
    :param final_state: Final state after completing the transition
    """

    start_state: State
    move: int
    jump: int
    land: int
    final_state: State

    def validate(self) -> bool:
        start_valid = (
            self.move in self.start_state
            and self.jump in self.start_state
            and self.land not in self.start_state
        )
        final_valid = (
            self.move not in self.final_state
            and self.jump not in self.final_state
            and self.land in self.final_state
        )

        return start_valid and final_valid
