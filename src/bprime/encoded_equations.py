
# import sympy
import sympy as sp
import numpy as np
from time import perf_counter
import random

"""
The encoded equations library part. This handles all the work surrounding
the equation encoded. I believe at the time of writing (2023-04-1) that this
will be one-way, and not equation -> encoded. Still deciding if this takes
a functional approach or object-oriented approach. I'm thinking functional,
so I can utilize JIT (Numba) easier on functional modules.
"""

# Define all valid Sympy function parts.

# TODO Break up into:
# - Functions (log, abs, betainc, polygamma)
# - Operators (+, -, *, /, **, ^)
# - Numbers (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, .)
# - Variables (x)
# - Constants (E, pi)
# - Parenthesis ((), [])
# - Comma (,)

# Raw expression parts.
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
    "abs",
    "^",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
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

# Define the minimum paramaters to maximum parameters for functions.
functions_info = { 
    "log": (1, 2),
    "abs": (1, 1),
    "betainc": (4, 4),
    "polygamma": (2, 2)
}


# Can resolve the symbols.
def evaluate_expression_sympy(expression, x_value):
    x = sp.Symbol('x')
    parsed_expression = sp.parse_expr(expression)
    lambda_expression = sp.lambdify(x, parsed_expression, modules=["sympy", "numpy"])
    result = parsed_expression.subs(x, x_value).evalf()
    return result, lambda_expression

# Old, but purely symbolic.
def random_equation(length=100, stop_perc=0.05):
    equation = ""
    for _ in range(length):
        if np.random.random() < stop_perc:
            break
        equation += np.random.choice(expression_parts_sympy)
    return equation

# Will generate a random expression, with a much higher
# and quicker success rate per-iteration, but is hard to
# track the expression parts. I will use this to brute force
# as many equations, and see if I can convert it back into the
# desired format.
def expression(n=10, variable="x"):
    expr = sp.sympify(0)
    x = sp.symbols(variable)
    equation_meta = []  # Initialize the list of tokens

    for _ in range(n):
        part = random.choice(expression_parts_sympy)
        if part == variable:
            term = x
            equation_meta.append(part)
        elif part in {"+", "-", "*", "/"}:
            op = part
            term = random.choice([x, random.randint(1, 9)])
            if op == "+":
                expr += term
            elif op == "-":
                expr -= term
            elif op == "*":
                expr *= term
            elif op == "/":
                expr /= term
            equation_meta.append(op)
            continue
        elif part.isdigit():
            term = int(part)
            equation_meta.append(part)
        elif part in {"E", "pi"}:
            term = sp.sympify(part)
            equation_meta.append(part)
        elif part in sp.__dict__:
            if part in functions_info:
                min_args, max_args = functions_info[part]
                num_args = random.randint(min_args, max_args)
                args = [random.choice([x, random.randint(1, 9)])
                        for _ in range(num_args)]
                for arg in args:
                    if isinstance(arg, sp.Symbol):
                        equation_meta.append(variable)
                    else:
                        equation_meta.append(str(arg))
                term = sp.__dict__[part](*args)
            else:
                term = sp.__dict__[part](x)
            equation_meta.append(part)
        else:
            continue
        expr += term

    return expr, equation_meta


if __name__ == "__main__":
    start = perf_counter()
    # Generate 10,000 equations.
    for _ in range(10_000):
        ex, meta = expression(10, "x")
    # Convert ex into lambda.
    ex_lambda = sp.lambdify("x", ex, modules=["sympy", "numpy"])
    ex_number = sp.N(ex_lambda(1))
    # print out the resolved number.    
    print(ex_number)
    # Iterations per second:
    print(f"> {10_000 / (perf_counter() - start):.2f} equations per second")