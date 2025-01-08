"""
This script contains the test for the utils.py.
"""

import pytest

from src.utils import list_contained, valid_parenthesis


@pytest.mark.parametrize(
    "list_1, list_2, expected",
    [
        ([1, 2, 3, 3], [1, 2, 3], False),
        ([1, 2, 5], [5, 1, 9, 6], False),
        ([1, 2], [0, 2, 1, 4], True),
        ([], [1, 2, 0], True),
    ],
)
def test_list_contained(list_1: list[int], list_2: list[int], expected: bool) -> None:
    """
    Test for the list_contained function.

    Parameters
    ----------
    list_1   : First parameter for the function.
    list_2   : Second parameter for the function.
    expected : Expected output.
    """

    assert list_contained(list_1, list_2) == expected


@pytest.mark.parametrize(
    "solution, expected",
    [
        ("2 + (2 * 3)", True),
        ("2 + (2 * 3", True),
        ("2 + ((((2 * 3) + (2)))", True),
        ("2 + 2 * 3", True),
        ("2 + 2 * 3)", False),
        ("2 + (2 * 3))", False),
    ],
)
def test_valid_parenthesis(solution: str, expected: bool) -> None:
    """
    Test for the valid_parenthesis function.

    Parameters
    ----------
    solution : Solution to check.
    expected : Expected output.
    """

    assert valid_parenthesis(solution) == expected
