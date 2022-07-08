#! /bin/python

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

# File: jump.py
#
# Description: Main executable for the jump program


import argparse as ap
import logging
import config as pc
import solver


def get_arguments() -> ap.Namespace:
    """
    Read and return the CLI arguments

    :return: Command line arguments passed to the running app
    """
    parser = ap.ArgumentParser(
        prog="jump", description="A General Peg Jump Game Solver"
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="JSON formatted file containing the peg jump game configuration",
    )
    return parser.parse_args()


def main() -> None:
    """
    main function
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    args = get_arguments()
    config = pc.config_factory(filename=args.file)
    logging.debug(f"config = {config}")
    solutions = solver.solve(cfg=config)

    for solution in solutions:
        logging.info(solution)

    logging.info(f"Solutions found {len(solutions)}")


if __name__ == "__main__":
    main()
