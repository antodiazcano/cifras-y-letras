"""
Main script to solve the problem.
"""

from src.solver import Solver

if __name__ == "__main__":
    AVAILABLE_NUMBERS = [3, 25, 9, 8, 6, 7]
    OBJECTIVE = 831

    SOLVER = Solver(AVAILABLE_NUMBERS, OBJECTIVE)
    print(SOLVER.exhaustive_search())
