"""
Script to solve the problem of achieving or being near an objective number given a set
of available numbers. You can use the operations '+', '-', '*' and '/'. Each number can
only be used once. For example, if the objective is 19 and the set of numbers is
{2, 4, 4, 5, 3} a possible solution is 2 * (4 + 4) + 3.
"""

import re
import time

from src.utils import list_contained, valid_parenthesis


class Solver:
    """
    Class to do an exhaustive search to find the solution. Solution will be represented
    by strings and in each step an operation is included.
    """

    def __init__(
        self,
        available_numbers: list[int],
        objective: int,
        max_time: float = 45.0,
        n_parenthesis: int = 1,
        max_depth: int = 5,
    ) -> None:
        """
        Constructor of the class.

        Parameters
        ----------
        available_numbers : Numbers we can use.
        objective         : Number we want to obtain.
        max_time          : Maximum time allowed.
        n_parenthesis     : Maximum number of recursive parenthesis allowed.
        max_depth         : Maximum depth of recursion allowed.
        """

        self.available_numbers = available_numbers
        self.objective = objective
        self.max_time = max_time
        self.max_depth = max_depth

        self.best_solution = ""
        self.best_value = objective

        self.possibilities = [str(x) for x in available_numbers]
        for i in range(1, n_parenthesis + 1):
            self.possibilities += [f"{'('*i}{x}" for x in available_numbers]
            self.possibilities += [f"{x}{')'*i}" for x in available_numbers]
        self.operations = ["+", "-", "*"]  # "/"]
        # There are some operations that do not need parenthesis after, for example sum
        # and subtraction: 1 + (2 * 3) = 1 + 2 * 3 = 6.
        self.op_with_parenthesis = ["*"]

    def is_valid(self, solution: str) -> bool:
        """
        Checks if more numbers are used than the available ones.

        Parameters
        ----------
        solution : Solution to check if it is valid.

        Returns
        -------
        True if it is valid, False otherwise.
        """

        used_numbers = [int(x) for x in re.findall(r"\d+", solution)]

        return list_contained(
            used_numbers, self.available_numbers
        ) and valid_parenthesis(solution)

    def expand_solutions(
        self, current_solutions: list[str], solution: str
    ) -> list[str]:
        """
        Expands all possible solutions that came from solution and adds them to
        current_solutions.

        Parameters
        ----------
        current_solutions : List we want to expand.
        solution          : Solution used to expand the list.

        Returns
        -------
        Expanded list of solutions.
        """

        for possibility in self.possibilities:
            for operation in self.operations:
                new_solution = f"{solution} {operation} {possibility}"
                if self.is_valid(new_solution):
                    if operation not in self.op_with_parenthesis:
                        # "+- (x)" is the same as "+- x" for all x achieved by any
                        # possible combination of operations
                        if "(" not in operation:
                            current_solutions.append(new_solution)
                    else:
                        current_solutions.append(new_solution)

        return current_solutions

    def evaluate_solution(self, solution: str) -> tuple[int, bool]:
        """
        Evaluates the value of a solution.

        Parameters
        ----------
        solution : Solution to evaluate.

        Returns
        -------
        Value of the solution (-1) if it is not valid and flag indicating if it is valid
        or not.
        """

        try:
            value = eval(solution)
            return value, True
        except SyntaxError:  # in the future it may will be valid
            return -1, True
        except ZeroDivisionError:
            return -1, False

    def update_solutions(self, current_solution: str, value: int) -> None:
        """
        Updates the best solution and value.

        Parameters
        ----------
        current_solution : Current solution used.
        value            : Value of the current solution.
        """

        diff = abs(value - self.objective)
        if diff < self.best_value:
            self.best_solution = current_solution
            self.best_value = diff

    def return_best_solution(self, time_elapsed: float) -> str:
        """
        Returns the string of the best solution found.

        Parameters
        ----------
        time_elapsed : Time elapsed.

        Returns
        -------
        Solution and time elapsed.
        """

        return (
            f"{self.best_solution} = {eval(self.best_solution)}. "
            f" Time elapsed: {time_elapsed:.2f} s."
        )

    def exhaustive_search(
        self,
        current_solutions: list[str] | None = None,
        current_depth: int = 1,
        initial_time: float | None = None,
        verbose: bool = True,
    ) -> str:
        """
        Performs an exhaustive search to find the best solution.

        Parameters
        ----------
        current_solutions : Solutions in the current level of search.
        current_depth     : Current depth of recursion.
        initial_time      : Initial time when the search started.
        verbose           : To print on screen the iteration where we are or not.

        Returns
        -------
        Best solution found.
        """

        if current_solutions is None:
            current_solutions = []
            for num in self.available_numbers:
                current_solutions.append(str(num))
                # current_solutions.append(f"({num}")

        if initial_time is None:
            initial_time = time.time()

        if verbose:
            print(f"Current depth: {current_depth}")
            print(f"Time elapsed: {time.time() - initial_time:.2f}")
            print(f"Number of solutions: {len(current_solutions)}\n")

        new_current_solutions: list[str] = []
        seen_solutions: list[int] = []

        for current_solution in current_solutions:
            value, expand = self.evaluate_solution(current_solution)

            if current_depth < self.max_depth:
                if value not in seen_solutions or expand:
                    seen_solutions.append(value)
                    self.update_solutions(current_solution, value)
                    new_current_solutions = self.expand_solutions(
                        new_current_solutions, current_solution
                    )
            else:
                self.update_solutions(current_solution, value)

            if self.best_value == 0 or time.time() - initial_time > self.max_time:
                return self.return_best_solution(time.time() - initial_time)

        if current_depth == self.max_depth:
            self.return_best_solution(time.time() - initial_time)

        return self.exhaustive_search(
            new_current_solutions,
            current_depth + 1,
            initial_time,
            verbose,
        )
