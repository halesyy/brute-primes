
import sympy
import math
from time import perf_counter

"""
The encoded equations library part. This handles all the work surrounding
the equation encoded. I believe at the time of writing (2023-04-1) that this
will be one-way, and not equation -> encoded. Still deciding if this takes
a functional approach or object-oriented approach. I'm thinking functional,
so I can utilize JIT (Numba) easier on functional modules.
"""
expression_parts_sympy = [
    "x",
    "log",
    "(",
    ")",
    ",",
    ".",
    "+",
    "-",
    "*",
    "/",
    "**",
    "E",
    "pi",
    "sqrt",
    "cbrt",
    "Abs",
    "exp",
    "ln",
    "log10",
    "log2",
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
    "sinh",
    "cosh",
    "tanh",
    "asinh",
    "acosh",
    "atanh",
    "erf",
    "erfc",
    "gamma",
    "loggamma",
    "digamma",
    "trigamma",
    "zeta",
    "polygamma",
    "beta",
    "betaln",
    "betainc"
]


def evaluate_expression_sympy(expression, x_value):
    x = sympy.Symbol('x')
    parsed_expression = sympy.parse_expr(expression)
    result = parsed_expression.subs(x, x_value).evalf()
    return result

if __name__ == "__main__":
    start = perf_counter()
    for _ in range(10_000):
        v = evaluate_expression_sympy("betainc(x, x, 3, 4)", 2)
    print(v)
    # Evals per second:
    print(f"> {1 / ((perf_counter() - start) / 10_000)} evals per second")
