"""
This script contains the test for the solver.py.
"""

import re
import pytest

from src.solver import Solver


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
