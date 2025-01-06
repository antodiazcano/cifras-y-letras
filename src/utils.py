"""
Script for some utility functions.
"""


def list_contained(list_1: list[int], list_2: list[int]) -> bool:
    """
    Checks if list_1 is contained in list_2 taking into account all numbers with
    repetition. For example, [2, 2, 3] is contained in [1, 2, 5, 2, 3, 1, 0] but not in
    [1, 2, 4, 3, 1, 0].

    Parameters
    ----------
    list_1 : First list.
    list_2 : Second list.

    Returns
    -------
    True if all numbers in list_1.
    """

    copy_list_2 = list_2[:]  # to not modify the original list

    for num in list_1:
        if num in copy_list_2:
            copy_list_2.remove(num)
        else:
            return False

    return True


def valid_parenthesis(solution: str) -> bool:
    """
    Checks if in each moment the number of '(' is greater or equal than the number of
    ')'.

    Parameters
    ----------
    solution : Solution to check.

    Returns
    -------
    True if the number of '(' is greater or equal and False otherwise.
    """

    count = 0

    for character in solution:
        if character == "(":
            count += 1
        elif character == ")":
            count -= 1
        if count < 0:
            return False

    return count >= 0
