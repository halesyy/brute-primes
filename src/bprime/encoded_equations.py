
# import sympy
import sympy as sp
import numpy as np
from time import perf_counter
import random
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)


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
    # "erf",
    # "erfc",
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

# Randomness of choice.
def roc():
    return random.randint(1, 9)
    # return random.randrange(0, 1_000)

# Will generate a random expression, with a much higher
# and quicker success rate per-iteration, but is hard to
# track the expression parts. I will use this to brute force
# as many equations, and see if I can convert it back into the
# desired format.
def expression(n=50, variable="x", stop_perc=0.05):
    expr = sp.sympify(0)
    x = sp.symbols(variable)
    equation_meta = []  # Initialize the list of tokens

    for _ in range(n):
        part = random.choice(expression_parts_sympy)
        if np.random.random() < stop_perc:
            break
        if part == variable:
            term = x
            equation_meta.append(part)
        elif part in {"+", "-", "*", "/"}:
            op = part

            term = random.choice([x, roc()])
            if op == "+":
                expr += term
            elif op == "-":
                expr -= term
            elif op == "*":
                expr *= term
            elif op == "/":
                expr /= term
            equation_meta.append(op)
            equation_meta.append(str(term))
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
                args = [random.choice([x, roc()])
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

# First 25 primes:
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

test_primes = [
    [1, 2], # 1st prime, 2
    [2, 3],
    [3, 5],
    [4, 7],
    [5, 11],
    [10, 29],
    [100, 541],
    [1000, 7919],
    [10000, 104729],
    # [100000, 1299709]
]

def test_long_error(ex_lambda):
    # print("> Starting to test long error...")
    error = 0
    for i, prime in test_primes:
        pred = sp.N(ex_lambda(i), n=2)
        actu = prime
        diff = abs(pred - actu)
        error += diff
        try:
            error = float(f"{error:.2f}")
        except:
            error = float("inf")
    return error

def find_best():
    # Find the best equation.
    best_error = float("inf")
    iters = 0
    tries = 0
    while True:
        tries += 1
        preds = []
        # Generate a random equation.
        ex, _ = expression(20, "x", 0.05)
        try:
            ex_lambda = sp.lambdify("x", ex, modules=["sympy", "numpy"])
        except:
            continue
        error = 0

        # I vs Prime.
        for i, prime in enumerate(primes):
            try:
                pred = sp.N(ex_lambda(i + 1), n=2)
            except:
                break
            actu = prime
            diff = abs(pred - actu)
            error += diff
            try:
                error = float(f"{error:.2f}")
            except:
                error = float("inf")
                break
            preds.append(pred)

        # Check error not isNaN.
        if str(error) == "nan" or len(preds) != len(primes):
            continue

        # Best error.        
        if error < best_error:
            best_error = error
            long_error = test_long_error(ex_lambda)
            print(f"Best error: {best_error}, Long Error: {long_error}, Ex: {ex}, Preds: {len(preds)}, T={tries} (i={iters})")

        # Iters.
        iters += 1
        if iters % 1000 == 0:
            print(f"Iterations: {iters}")


if __name__ == "__main__":
    find_best()
