#! /bin/python

import argparse as ap
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
    args = get_arguments()
    config = pc.config_factory(filename=args.file)
    print(f"config = {config}")
    solutions = solver.solve(cfg=config)

    for solution in solutions:
        print(solution)

    print(f"Solutions found {len(solutions)}")


if __name__ == "__main__":
    main()
