"""
Main script to solve the problem.
"""

import argparse

from src.solver import Solver


def main() -> None:  # pragma: no cover
    """
    Parse arguments, solve the problem and print the solution.
    """

    parser = argparse.ArgumentParser(
        description="Solve the problem with the given numbers and objective."
    )
    parser.add_argument(
        "--nums",
        type=str,
        required=True,
        help="List of available numbers, separated by commas.",
    )
    parser.add_argument(
        "--obj",
        type=int,
        required=True,
        help="The target number to achieve.",
    )
    args = parser.parse_args()

    available_numbers = list(map(int, args.nums.split(",")))
    objective = args.obj
    solver = Solver(available_numbers, objective)
    print(solver.solve())


if __name__ == "__main__":
    main()
