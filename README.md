This repo contains a solution for the "Cifras" problem in the Spanish TV show "Cifras y Letras". The problem is the folowing:
- You are given an **objective** number.
- You are given a list of **available numbers** you can combine with the operations $+, -, \cdot$ and $/$.
- You have to obtain the nearest number possible to the objective number within $45$ seconds.

For example, if the objective is $19$ and the available numbers are $[6, 2, 3, 1, 5, 2]$ a possible solution is $6\cdot 3+2=20$ but the best solution would be $5\cdot 2\cdot 2 -1=19$ or $6\cdot 3 + 1=19$.

To run the program execute in command line

    python -m src.main 
