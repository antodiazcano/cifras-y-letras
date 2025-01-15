"""
Script to define the constants used in the Solver class.
"""

MAX_TIME = 45
FOLLOWED_PARENTHESIS = 1
# This is to bound solutions like "((2 + 3) * 5) + 7", that is, with two followed
# parenthesis, which in some cases may be valid, but we have to prune because if not
# the number of solutions grows exponentially.
MAX_PARENTHESIS = 2
# Like the before parameter but regardless of whether they are followed or not
MAX_DEPTH = 5
# Max depth to explore. Note that all solutions until MAX_DEPTH - 1 will be expanded and
# solutions with MAX_DEPTH depth will be explored but not expanded. Therefore, may be it
# is better to keep conservative and for example using MAX_DEPTH = 5 and exploring all
# solutions of depth 5 and none of level 6 than using MAX_DEPTH = 6 because as in level
# 5 they have to be expanded, if MAX_TIME is reached may be all of that level are not
# explored.
PRUNE_DEPTH = 4
# Depth where we start to prune solutions that are not promising.
OPERATIONS = ["+", "-", "*"]  # "/"]
# There are some operations that do not need parenthesis after, for example sum
# and subtraction: "1 + (2 * 3) = 1 + 2 * 3 = 6".
OP_WITH_PARENTHESIS = ["*"]
INVALID_EVAL = -1  # just to denote when "eval" fails


# Notes
# I have noticed empirically is more important to increase the depth than exploring
# all possible solutions of minor depth.
