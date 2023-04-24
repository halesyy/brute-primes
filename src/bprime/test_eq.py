
import sympy as sp
import matplotlib.pyplot as plt

# Test equation.
# test_ex = "log(x) + acosh(x) + betainc(1, 4, x, 2) + betainc(8, x, x, x) + erf(x) + erfc(x) + 1"
# test_ex = "sinh(x) + cosh(x) + tanh(x) + betainc(1, 6, 2, 7) + erfc(x) + gamma(x) + 2 + pi"
# test_ex = "x*(tanh(x)/7 + acosh(x)/7 + polygamma(1, x)/7 + 6/7) + loggamma(x)"
# test_ex = "erf(x) + erfc(x) - 1"
# test_ex = "x*(log(x) + polygamma(1, x)/4 + 1/2)"
test_ex = "sqrt(x) + x + sin(x) + loggamma(x) + log(3)/log(6)"

# First 100 primes.
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991]


def prime_generator():
    def sieve(n, primes):
        for p in primes:
            if p * p > n:
                return True
            if n % p == 0:
                return False
        return True

    primes = [2]
    yield 2
    n = 3
    while True:
        if sieve(n, primes):
            primes.append(n)
            yield n
        n += 2

# Build lambda for sq.
sq_lambda = sp.lambdify("x", sp.sympify(test_ex), modules=["sympy", "numpy"])

X = []
y_primes = []
y_preds = []


pg = prime_generator()

for i in range(10_000):
    prime = next(pg)
    pred = sp.N(sq_lambda(i + 1), n=1)
    # print(prime, pred)
    X.append(i + 1)
    y_primes.append(prime)
    y_preds.append(pred)

plt.plot(X, y_primes)
plt.plot(X, y_preds)
plt.show()