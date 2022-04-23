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
import mec
import exception as excp
import os.path as osp
import pandas as pd


@dataclass(frozen=True)
class Layout:
    points: typing.List[mec.Point]

    @property
    def bounds(self) -> typing.Tuple[mec.Point, mec.Point]:
        """
        Compute and return the bounds of the point list.

        :return: Bounds of the point list
        """
        return mec.bounds(self.points)


def read_layout(layout_filename: str):
    """
    Read a board from the CSV file containing the transitions

    :param layout_filename: Name of the file containing the layout
    :return: Layout object describing the board layout
    """
    if not isinstance(layout_filename, str):
        raise excp.PuzzleException(
            f"Expected the layout filename to be a string.  Found {layout_filename} / {type(layout_filename)}."
        )
    if not osp.exists(path=layout_filename):
        raise excp.PuzzleException(f"Layout file not found {layout_filename}")
    if not osp.isfile(path=layout_filename):
        raise excp.PuzzleException(
            f"Given layout file name {layout_filename} is not a file"
        )

    df = pd.read_csv(layout_filename, header=None)

    points = []

    for _, data in df.iterrows():
        points.append(mec.Point(x=data[0], y=data[1]))

    min_circle = mec.welzl(points)
    points = [(x - min_circle.center) / min_circle.radius for x in points]

    return Layout(points=points)
