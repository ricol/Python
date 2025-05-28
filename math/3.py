#!/usr/bin/env python
#-*- coding: utf-8 -*-

from functools import reduce
def compute_sum1(n):
    """ computes and returns the sum of 2,4,6, ... , m
	where m is the largest even number smaller than n.
	For example, with n = 7, we compute 0 + 2 + 4 + 6 = 12.
	This implementation uses a variable 'mysum '
	that is
	increased in every iteration of the
	for -loop.
	"""

    mysum = 0
    for i in range(0, n, 2):
        mysum = mysum + i
    return mysum

def compute_sum2(n):
    """ computes and returns ...
	This implementation uses a
	while -loop:
	"""
    counter = 0
    mysum = 0
    while counter < n:
        mysum = mysum + counter
    counter = counter + 2
    return mysum

def compute_sum3(n, startfrom=0):
    """ computes and returns ...
	This is a recursive implementation: """
    if n <= startfrom:
        return 0
    else:
        return startfrom + compute_sum3(n, startfrom + 2)

def compute_sum4a(n):
    """A functional approach ... this seems to be
	the shortest and most concise code.
	"""
    return sum(range(0, n, 2))

def compute_sum4b(n):
    """A functional approach ... not making use of 'sum ' which
	happens to exist and is of course convenient here.
	"""
    return reduce(lambda a, b: a + b, list(range(0, n, 2)))

def compute_sum4c(n):
    """A functional approach ... a bit faster than compute_sum4b
	as we avoid using lambda.
	"""

    import operator
    return reduce(operator.__add__, list(range(0, n, 2)))

def compute_sum4d(n):
    """ Using list comprehension ."""
    return sum([k for k in range(0, n, 2)])

def compute_sum4e(n):
    """ Using another variation of list comprehension ."""
    return sum([k for k in range(0, n) if k % 2 == 0])

def compute_sum5(n):
    """ Using numerical python ( numpy ). This is very fast
	(but would only pay off
	  if n >> 10).
	"""
    import numpy
    return numpy.sum(2 * numpy.arange(0, (n + 1) // 2))

def test_consistency ():
    """ Check that all compute_sum ?? functions in this file produce
	the same answer for all n >=2 and <N.
	"""
    def check_one_n (n):
        """ Compare the output of compute_sum1 with all other functions
		for a given n >=2. Raise AssertionError if outputs disagree ."""
        funcs = [compute_sum1, compute_sum2, compute_sum3,
        compute_sum4a, compute_sum4b, compute_sum4c,
        compute_sum4d, compute_sum4e, compute_sum5]
        ans1 = compute_sum1 (n)
        for f in funcs [1:]:
            assert ans1 == f(n), "%s(n )=% d not the same as %s(n)=% d " \
            % (funcs [0], funcs [0](n), f, f(n))

    # main testing loop in test_consistency function
    for n in range (2, 1000):
        check_one_n (n)

if __name__ == "__main__":
    m = 7
    correct_result = 12
    thisresult = compute_sum1 (m)
    print((" this result is {}, expected to be {}". format(thisresult, correct_result)))
    # compare with correct result
    print("running...")
    assert thisresult == correct_result
    # also check all other methods
    assert compute_sum2 (m) == correct_result
    assert compute_sum3 (m) == correct_result
    assert compute_sum4a (m) == correct_result
    assert compute_sum4b (m) == correct_result
    assert compute_sum4c (m) == correct_result
    assert compute_sum4d (m) == correct_result
    assert compute_sum4e (m) == correct_result
    assert compute_sum5 (m) == correct_result
    # a more systematic check for many values
    print("Testing consistency...")
    test_consistency ()
    print("done")