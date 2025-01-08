"""
Script to solve the problem of achieving or being near an objective number given a set
of available numbers. You can use the operations '+', '-', '*' and '/'. Each number can
only be used once. For example, if the objective is 19 and the set of numbers is
{2, 4, 4, 5, 3} a possible solution is 2 * (4 + 4) + 3.
"""

import re
import time

from src.utils import list_contained, valid_parenthesis
from src.constants import (
    MAX_TIME,
    FOLLOWED_PARENTHESIS,
    MAX_PARENTHESIS,
    MAX_DEPTH,
    OPERATIONS,
    OP_WITH_PARENTHESIS,
)


class Solver:
    """
    Class to do an exhaustive search to find the solution. Solution will be represented
    by strings and in each step an operation is included.
    """

    def __init__(
        self,
        available_numbers: list[int],
        objective: int,
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

        self.best_solution = ""
        self.best_value = objective

        self.possibilities = [str(x) for x in available_numbers]
        for i in range(1, FOLLOWED_PARENTHESIS + 1):
            self.possibilities += [f"{'('*i}{x}" for x in available_numbers]
            self.possibilities += [f"{x}{')'*i}" for x in available_numbers]

        self.lower_bound, self.upper_bound = self._get_bounds()

    def _get_bounds(self) -> tuple[int, int]:
        """
        Obtains an upper bound to bound solutions.

        Returns
        -------
        Upper and lower bounds.
        """

        max_elements = sorted(self.available_numbers, reverse=True)[:2]
        lower_bound = self.objective // max_elements[0]
        upper_bound = self.objective + max_elements[0] * max_elements[1]

        return lower_bound, upper_bound

    def _is_valid(self, solution: str) -> bool:
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

    def _prune(self, solution: str, value: int, depth: int) -> bool:
        """
        Prunes the solution if its expected value is not promising.

        Parameters
        ----------
        solution : Solution.
        value    : Value of the solution.
        depth    : Current depth of the solution.

        Returns
        -------
        True if we have to bound and False otherwise.
        """

        if solution.count("(") > MAX_PARENTHESIS:
            return True

        if depth >= 4:
            if (value < self.lower_bound and value != -1) or (value > self.upper_bound):
                return True

        return False

    def _expand_solutions(
        self, current_solutions: list[str], solution: str, value: int, depth: int
    ) -> list[str]:
        """
        Expands all possible solutions that came from solution and adds them to
        current_solutions.

        Parameters
        ----------
        current_solutions : List we want to expand.
        solution          : Solution used to expand the list.
        value             : Value of the solution.
        depth             : Depth of the solutions.

        Returns
        -------
        Expanded list of solutions.
        """

        for possibility in self.possibilities:
            for operation in OPERATIONS:
                new_solution = f"{solution} {operation} {possibility}"
                if self._is_valid(new_solution) and not self._prune(
                    solution, value, depth
                ):
                    if operation not in OP_WITH_PARENTHESIS:
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

    def _update_solutions(self, current_solution: str, value: int) -> None:
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

    def solve(
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
                current_solutions.append(f"({num}")

        if initial_time is None:
            initial_time = time.time()

        if verbose:
            print(f"Current depth: {current_depth}")
            print(f"Time elapsed: {time.time() - initial_time:.2f} s")
            print(f"Number of solutions: {len(current_solutions)}\n")

        new_current_solutions: list[str] = []
        seen_solutions = [
            False for _ in range(self.upper_bound)
        ]  # to not repeat equivalent solutions

        for current_solution in current_solutions:
            value, expand = self.evaluate_solution(current_solution)

            if current_depth < MAX_DEPTH:
                try:
                    if not seen_solutions[value] or expand:
                        seen_solutions[value] = True
                        self._update_solutions(current_solution, value)
                except IndexError:
                    self._update_solutions(current_solution, value)
                new_current_solutions = self._expand_solutions(
                    new_current_solutions, current_solution, value, current_depth
                )
            else:
                self._update_solutions(current_solution, value)

            current_time = time.time() - initial_time
            if self.best_value == 0 or current_time > MAX_TIME:
                return self.return_best_solution(current_time)

        if current_depth == MAX_DEPTH:
            self.return_best_solution(time.time() - initial_time)

        return self.solve(
            new_current_solutions,
            current_depth + 1,
            initial_time,
            verbose,
        )
