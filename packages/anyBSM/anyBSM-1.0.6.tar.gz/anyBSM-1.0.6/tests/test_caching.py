#!/usr/bin/env python3

import unittest
import numpy.testing as test
from anyBSM import anyBSM

SM = anyBSM('SM', progress = False, quiet = True)
SM.clear_cache()
SM.set_evaluation_mode('numerical')

""" this plugs numbers directly into generic diagrams """
SM.caching = 0
lam_no_cache = SM.lambdahhh()['total'].real

""" this will first generate the abbreviated/analytical
result, store it in cache and then evaluate the cached
result numerically at each run. Thus, it is expected to
slightly differ from the `lam_no_cache` result."""
SM.caching = 2
lam_cache_1 = SM.lambdahhh()['total'].real
lam_cache_2 = SM.lambdahhh()['total'].real

class numericTest(unittest.TestCase):
    def test_caching_0(self):
        test.assert_allclose(lam_no_cache, lam_cache_1, rtol = 1e-10, atol = 0)

    def test_caching_1(self):
        test.assert_allclose(lam_no_cache, lam_cache_2, rtol = 1e-10, atol = 0)

    def test_caching_2(self):
        test.assert_allclose(lam_cache_1, lam_cache_2, rtol = 1e-15, atol = 0)
