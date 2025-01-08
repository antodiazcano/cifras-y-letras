"""
Script to define the constants used in the Solver class.
"""

MAX_TIME = 45
FOLLOWED_PARENTHESIS = 1
# This is to bound solutions like "((2 + 3) * 5) + 7" which in some
# cases may be valid, but mostly not.
MAX_PARENTHESIS = 2
# Like the before parameter but regardless of whether they are followed or not
MAX_DEPTH = 5
OPERATIONS = ["+", "-", "*"]  # "/"]
# There are some operations that do not need parenthesis after, for example sum
# and subtraction: "1 + (2 * 3) = 1 + 2 * 3 = 6".
OP_WITH_PARENTHESIS = ["*"]
