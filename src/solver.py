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
    PRUNE_DEPTH,
    OPERATIONS,
    OP_WITH_PARENTHESIS,
    INVALID_EVAL,
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
        lower_bound = self.objective // min(self.available_numbers)
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

        if depth >= PRUNE_DEPTH:
            if (value < self.lower_bound and value != INVALID_EVAL) or (
                value > self.upper_bound
            ):
                return True

        return False

    def _select_solutions(
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
                    if operation not in OP_WITH_PARENTHESIS and "(" not in operation:
                        # "+- (x)" is the same as "+- x" for all x achieved by any
                        # possible combination of operations
                        current_solutions.append(new_solution)
                    elif operation in OP_WITH_PARENTHESIS:
                        current_solutions.append(new_solution)

        return current_solutions

    def evaluate_solution(self, solution: str) -> int:
        """
        Evaluates the value of a solution.

        Parameters
        ----------
        solution : Solution to evaluate.

        Returns
        -------
        Value of the solution (INVALID_EVAL if it is not valid).
        """

        try:
            return eval(solution)
        except SyntaxError:  # in the future it may will be valid
            return INVALID_EVAL

    def _update_solutions(self, current_solution: str, value: int) -> None:
        """
        Updates the best solution and value.

        Parameters
        ----------
        current_solution : Current solution used.
        value            : Value of the current solution.
        """

        diff = value - self.objective
        abs_diff = abs(diff)

        if abs_diff in self.available_numbers and current_solution.count(
            str(abs_diff)
        ) < self.available_numbers.count(abs_diff):
            if diff < 0:
                current_solution += f" + {abs_diff}"
            else:
                current_solution += f" - {abs_diff}"
            abs_diff = 0

        if abs_diff < self.best_value:
            self.best_solution = current_solution
            self.best_value = abs_diff

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
            f"{self.best_solution} = {self.evaluate_solution(self.best_solution)}. "
            f"Time elapsed: {time_elapsed:.2f} s."
        )

    def _expand_current_solution(
        self,
        current_solution: str,
        seen_solutions: list[bool],
        current_depth: int,
        new_current_solutions: list[str],
    ) -> tuple[list[str], list[bool]]:
        """
        Expands all valid and promising solutions from the current one.

        Parameters
        ----------
        current_solution      : Solution we will expand.
        seen_solutions        : Solutions already seen.
        current_depth         : Current depth of the solution.
        new_current_solutions : List to store new solutions for next depth.

        Returns
        -------
        Updated list of new_current_solutions and seen_solutions.
        """

        value = self.evaluate_solution(current_solution)

        if current_depth < MAX_DEPTH:
            if (0 < value < self.upper_bound) and (not seen_solutions[value]):
                seen_solutions[value] = True
                self._update_solutions(current_solution, value)
                new_current_solutions = self._select_solutions(
                    new_current_solutions, current_solution, value, current_depth
                )
            elif value == INVALID_EVAL:
                new_current_solutions = self._select_solutions(
                    new_current_solutions, current_solution, value, current_depth
                )
        else:  # not expand to avoid losing time
            self._update_solutions(current_solution, value)

        return new_current_solutions, seen_solutions

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

        if current_solutions is None:  # initialize possible solutions
            current_solutions = []
            for num in self.available_numbers:
                current_solutions.append(str(num))
                # current_solutions.append(f"({num}")

        if initial_time is None:  # initialize time
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
            new_current_solutions, seen_solutions = self._expand_current_solution(
                current_solution, seen_solutions, current_depth, new_current_solutions
            )

            current_time = time.time() - initial_time
            if self.best_value == 0 or current_time > MAX_TIME:
                return self.return_best_solution(current_time)

        if current_depth == MAX_DEPTH:
            _, _ = self._expand_current_solution(
                self.best_solution, seen_solutions, current_depth, new_current_solutions
            )  # one last try, expand the best solution (only one) found
            return self.return_best_solution(time.time() - initial_time)

        return self.solve(
            new_current_solutions,
            current_depth + 1,
            initial_time,
            verbose,
        )
