# Brute Primes

Building a clean, step-by-step approach to attempting to brute force an equation to resolve to as little loss on the prime number curve. The goal is to then build a linear regression model on data paramaters which output as an equation.

## The problem

Prime number approximations (n input = nth prime) have existed for a long time, in forms like:

* `p(n) = n * log(n)`

But they are just approximations. What often occurs is when you look at the sequential error rate (the difference between the prediction and the real output), it creates it's own beast of a curve which follows weird curves.

*In the past*, as a bit of a less creative programmer (knew less disciplies), I attempted to do this by brute forcing equations using the raw strings. I'd create a series of tokens (`log,+,-`, etc...) and try to string them together, then attempt to run numbers through them. This worked, but it was grossly inefficient. Although inefficient, it produced the above equation on its own.

## A solution

My plan, this time, is to break the problem down into a more computer-understandable problem, then use a series of paramater optimization algorithms to work out the correct configuration to get the "best" (most fit) equation to fit the given problem (prime numbers). If this works, it's general applicability will also be great to see.

### Steps

* [ ] Create a flat array standard for representing complex equations using floats.
* [ ] (Optional) Algorithmically or manually create a relationship graph which denies certain series of floats from being together (to avoid failed computations). Or a "next word" prediction idea of just having a "next valid word" relationship for each float.
* [ ] Create the prediction series by building the first 1,000,000 primes.
* [ ] Build a large training set of complex equations and their prime fitness.
  (My initial thinking is 0 = perfectly fit, -1 = invalid, > 0 = unfit and errorous.)
  The special part here is not that we're not trying to make a "prime number prediction equation", instead, we're making a "prime number equation prediction equation". To me, this makes more sense and is more scalable since the prime number equation does not follow standard multiplicative features.
* [ ] Run it randomly for a period of time, and see if it comes up with anything special.
* [ ] Pack the training data and the prediction data into a linear regression model to find the most optimal paramaters for the lowest equation.
* [ ] Test other algorithms. Genetic, Bayesian, etc.

### Solution Considerations

| Problem                                                                                                                                     | Proposed Solutions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| How do we encode arbitrary integers and<br />floats into the equations if we're already using<br />them as significant equation references? | 1. Use integers as encoded parts. I.e. encode<br />0, 1, 2 and "." as equation parts. I think this<br />will be the easiest for the models to understand.<br /><br />2. Use bitwise-encoded ceiling ints. I.e. after<br />we've defined all of the equation parts (log,<br />^, +, .,etc), anything above that is treated as a<br />bitwise number pattern. This seems dumb.<br /><br />3. Use ceilings, but any number over that ceiling<br />is the encoded number. If the ceiling is 100, then<br />151.2 = 51.2 in the equation. This seems easiest<br />for a human to read, but I'm not sure if the <br />relationship will be understood by a model. I'll<br />make it easy to test both relationships by <br />keeping this code modular. |
| What models can we utilize which allow us to<br />find or predict the best input to receive the<br />wished-for output?                     | My first thought was linear regression, but<br />instead of using the curve to classify incoming<br />inputs, we train it to work out the curve, then<br />use the curve to distinguish the optimal<br />paramaters to get to a 0.<br /><br />But, will I need to explore this and write in more <br />proposed solutions.                                                                                                                                                                                                                                                                                                                                                                                                                         |
