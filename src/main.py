"""
Main script to solve the problem.
"""

from src.solver import Solver


def main(available_numbers: list[int], objective: int) -> str:
    """
    Obtains the solution for a given problem.

    Parameters
    ----------
    available_numbers : Available numbers for the operations.
    objective         : Objective number.

    Returns
    -------
    Best solution found.
    """

    solver = Solver(available_numbers, objective)
    solver.solve()
    return solver.best_solution


if __name__ == "__main__":  # pragma: no cover
    AVAILABLE_NUMBERS = [3, 25, 9, 8, 6, 7]
    OBJECTIVE = 831

    main(AVAILABLE_NUMBERS, OBJECTIVE)
