"""
Test for main.py
"""

import time

from src.main import main
from src.constants import MAX_TIME


def test_main() -> None:
    """
    Checks the correct work of the main.py function.
    """

    available_numbers = [1, 2, 3, 4, 5]
    objective = 15  # 1 + 2 * (3 + 4)
    t0 = time.time()
    solution = main(available_numbers, objective)
    tf = time.time()
    assert eval(solution) == objective and tf - t0 <= MAX_TIME
