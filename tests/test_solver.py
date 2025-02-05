"""
This script contains the test for the solver.py.
"""

import re
import time
import pytest

from src.solver import Solver
from src.constants import INVALID_EVAL, MAX_DEPTH, MAX_TIME


@pytest.mark.parametrize(
    "available_numbers, objective, expected",
    [([3, 4, 5], 20, (6, 40)), ([10, 4, 6, 7], 193, (48, 263))],
)
def test_get_bounds(
    available_numbers: list[int], objective: int, expected: tuple[int, int]
) -> None:
    """
    Test for the _get_bounds function.

    Parameters
    ----------
    available_numbers : Parameter for the initialization of the class.
    objective         : Parameter for the initialization of the class.
    expected          : Expected output.
    """

    s = Solver(available_numbers, objective)

    assert s.lower_bound == expected[0] and s.upper_bound == expected[1]


@pytest.mark.parametrize(
    "available_numbers, solution, expected",
    [
        ([3, 4, 5], "4 + (3 * 5", True),
        ([3, 4, 5], "4 + 3 * 5", True),
        ([3, 4, 5], "4 + (3 * 8", False),
        ([3, 4, 5], "4 + (3 * 5))", False),
        ([3, 4, 5], "4 + (3 * 7)", False),
    ],
)
def test_is_valid(available_numbers: list[int], solution: str, expected: bool) -> None:
    """
    Test for the _is_valid function.

    Parameters
    ----------
    available_numbers : Parameter for the initialization of the class.
    solution          : Solution tested.
    expected          : Expected output.
    """

    s = Solver(available_numbers, -1)

    assert s._is_valid(solution) == expected


@pytest.mark.parametrize(
    "solution, value, depth, expected",
    [
        ("1 + 3 * 5", 16, 3, False),
        ("10 + 3 * 5", 25, 3, False),
        ("10 + 3 * 5", 25, 4, True),
        ("((4 + 3)) * 2", 14, 5, False),
        ("(((4 + 3))) * 2", 14, 5, True),
        ("4 - 3 * 1", 1, 10, True),
    ],
)
def test_prune(solution: str, value: int, depth: int, expected: bool) -> None:
    """
    Test for the _is_valid function.

    Parameters
    ----------
    available_numbers : Parameter for the initialization of the class.
    solution          : Solution tested.
    expected          : Expected output.
    """

    s = Solver([1, 2, 3], -1)
    s.lower_bound = 10
    s.upper_bound = 20

    assert s._prune(solution, value, depth) == expected


@pytest.mark.parametrize(
    "available_numbers, solution, expected",
    [
        (
            [1, 2, 3, 4, 5],
            "1 + 2 * (3",
            [
                "1 + 2 * (3 + 4",
                "1 + 2 * (3 - 4",
                "1 + 2 * (3 * 4",
                "1 + 2 * (3 + 5",
                "1 + 2 * (3 - 5",
                "1 + 2 * (3 * 5",
                "1 + 2 * (3 + (4",
                "1 + 2 * (3 - (4",
                "1 + 2 * (3 * (4",
                "1 + 2 * (3 + (5",
                "1 + 2 * (3 - (5",
                "1 + 2 * (3 * (5",
                "1 + 2 * (3 + 4)",
                "1 + 2 * (3 - 4)",
                "1 + 2 * (3 * 4)",
                "1 + 2 * (3 + 5)",
                "1 + 2 * (3 - 5)",
                "1 + 2 * (3 * 5)",
            ],
        ),
        ([1, 2, 3], "1 + 2 * 3", []),
        ([1, 2, 3], "1 + 2 * )3", []),
        ([1, 20_000, 3, 4], "20_000 + 1 * 3", []),
        (
            [1, 2, 3, 4],
            "1 + 2 * 3",
            [
                "1 + 2 * 3 + 4",
                "1 + 2 * 3 - 4",
                "1 + 2 * 3 * 4",
                "1 + 2 * 3 + (4",
                "1 + 2 * 3 - (4",
                "1 + 2 * 3 * (4",
            ],
        ),
    ],
)
def test_select_solutions(
    available_numbers: list[int],
    solution: str,
    expected: list[str],
) -> None:
    """
    Test for the _select_solutions function.

    Parameters
    ----------
    available_numbers : Available numbers.
    solution          : Solution to expand.
    expected          : Expected output.
    """

    s = Solver(available_numbers, 10)
    try:
        value = eval(solution)
    except SyntaxError:
        value = -1
    depth = len(re.findall(r"\d+", solution))
    assert s._select_solutions([], solution, value, depth) == expected


def test_evaluate_solution() -> None:
    """
    Test for evaluate_solution.
    """

    s = Solver([1, 2], 0)
    solutions = ["2 + 2", "2+2", "2+ 2", "2 +"]

    for solution in solutions:
        try:
            assert s.evaluate_solution(solution) == eval(solution)
        except SyntaxError:
            assert s.evaluate_solution(solution) == INVALID_EVAL


def test_update_solutions() -> None:
    """
    Test for the _update_solutions function.
    """

    # Update
    s = Solver([1, 2, 3], 10)
    solution = "5 + 5"
    value = eval(solution)
    s._update_solutions(solution, value)
    assert s.best_solution == solution and s.best_value == abs(s.objective - value)

    # Update and positive difference in available numbers
    s = Solver([1, 2, 3], 10)
    solution = "5 + 7"
    value = eval(solution)
    s._update_solutions(solution, value)
    assert s.best_value == 0

    # Update and negative difference in available numbers
    s = Solver([1, 2, 3], 10)
    solution = "5 + 2"
    value = eval(solution)
    s._update_solutions(solution, value)
    assert s.best_value == 0

    # No update if a better solution was previously found
    s = Solver([1, 2, 3], 10)
    s._update_solutions("5 + 6", 11)
    solution = "5 + 9"
    value = eval(solution)
    s._update_solutions(solution, value)
    assert s.best_solution != solution and s.best_value != abs(s.objective - value)


def test_return_best_solution() -> None:
    """
    Test for return_best_solution.
    """

    s = Solver([2, 3], 10)
    solution = "5 + 4"
    value = eval(solution)
    s._update_solutions(solution, value)
    time = 10
    expected = f"{solution} = {value}. Time elapsed: {time:.2f} s."

    assert s.return_best_solution(time) == expected


def test_expand_current_solution() -> None:
    """
    Test for _expand_current_solution.
    """

    s = Solver([10, 20, 30], 50)
    seen_solutions = [False for _ in range(s.upper_bound)]
    current_depth = MAX_DEPTH - 1
    solution = "20 - 5"
    value = eval(solution)
    current_solutions: list[str] = []

    # Normal case
    new_current_solutions, seen_solutions = s._expand_current_solution(
        solution, seen_solutions, current_depth, current_solutions
    )
    assert (
        new_current_solutions
        == s._select_solutions(current_solutions, solution, value, current_depth)
        and seen_solutions[value]
    )

    # Max depth case
    new_current_solutions_2, seen_solutions_2 = s._expand_current_solution(
        solution, seen_solutions, MAX_DEPTH, current_solutions
    )
    assert (
        new_current_solutions_2 == new_current_solutions
        and seen_solutions_2 == seen_solutions
    )

    # A solution that must not be expanded
    solution = "3 * 5"
    value = eval(solution)
    seen_solutions[value] = True
    current_depth = MAX_DEPTH - 1
    new_current_solutions_3, seen_solutions_3 = s._expand_current_solution(
        solution, seen_solutions, current_depth, current_solutions
    )
    assert (
        new_current_solutions_3 == current_solutions
        and seen_solutions_3 == seen_solutions
    )


def test_expand_last_try() -> None:
    """
    Test for the _expand_last_try function.
    """

    s = Solver([10, 20, 5], 50)
    s.best_solution = "10 + 20"
    s.best_value = 20
    s._expand_last_try()
    assert s.best_solution == "10 + 20 + 5" and s.best_value == 15

    s = Solver([45, 20, 5], 50)
    s.best_solution = "45 + 20"
    s.best_value = 15
    s._expand_last_try()
    assert s.best_solution == "45 + 20 - 5" and s.best_value == 10


def test_solve() -> None:
    """
    Test for the solve function.
    """

    available_numbers = [1, 2, 3, 4, 5]
    objective = 15  # 1 + 2 * (3 + 4)
    s = Solver(available_numbers, objective)
    t0 = time.time()
    s.solve()
    tf = time.time()
    assert eval(s.best_solution) == objective and tf - t0 <= MAX_TIME

    available_numbers = [1, 2, 3, 4, 5]
    objective = 99  # 1 + 2 * (3 + 4)
    s = Solver(available_numbers, objective)
    t0 = time.time()
    s.solve(current_depth=MAX_DEPTH)
    t0 = time.time()
    assert tf - t0 <= MAX_TIME
