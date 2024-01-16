#!/usr/bin/env python3

import unittest
import numpy.testing as test
from random import random
from anyBSM import loopfunctions
from itertools import combinations_with_replacement


B0 = loopfunctions.B0_p0 # our own analytical results
C0 = loopfunctions.C0_p0
B00 = loopfunctions.B00_p0
dB0 = loopfunctions.dB0_p0
dB00 = loopfunctions.dB00_p0
cB0 = loopfunctions.pyCollier.b0 # collier
cB00 = loopfunctions.pyCollier.b00 # collier
cC0 = loopfunctions.pyCollier.c0
cdB0 = loopfunctions.pyCollier.db0
cdB00 = loopfunctions.pyCollier.db00

loopfunctions.set_renscale(172.5)

x = random()*1000
y = random()*1000
z = random()*1000

class numericTest(unittest.TestCase):
    """ IR divergent cases are not tested since these are handled differently in COLLIER and in the analytical expresssions """

    # test B0 from COLLIER against analytical B0 implementation
    def test_B0_xy(self):
        test.assert_allclose(B0(x,y), cB0(0,x,y))

    def test_B0_xx(self):
        test.assert_allclose(B0(x,x), cB0(0,x,x))

    def test_B0_x0(self):
        test.assert_allclose(B0(x,0), cB0(0,x,0))

    def test_B0_0y(self):
        test.assert_allclose(B0(0,y), cB0(0,0,y))

    # test dB0 from COLLIER against analytical B0 implementation
    def test_dB0_xy(self):
        test.assert_allclose(dB0(x,y), cdB0(0,x,y))

    def test_dB0_xx(self):
        test.assert_allclose(dB0(x,x), cdB0(0,x,x))

    def test_dB0_x0(self):
        test.assert_allclose(dB0(x,0), cdB0(0,x,0))

    def test_dB0_0y(self):
        test.assert_allclose(dB0(0,y), cdB0(0,0,y))

    # test B00 from COLLIER against analytical B0 implementation
    def test_B00_xy(self):
        test.assert_allclose(B00(x,y), cB00(0,x,y))

    def test_B00_xx(self):
        test.assert_allclose(B00(x,x), cB00(0,x,x))

    def test_B00_x0(self):
        test.assert_allclose(B00(x,0), cB00(0,x,0))

    def test_B00_0y(self):
        test.assert_allclose(B00(0,y), cB00(0,0,y))

    # test dB00 from COLLIER against analytical B0 implementation
    def test_dB00_xy(self):
        test.assert_allclose(dB00(x,y), cdB00(0,x,y))

    def test_dB00_xx(self):
        test.assert_allclose(dB00(x,x), cdB00(0,x,x))

    def test_dB00_x0(self):
        test.assert_allclose(dB00(x,0), cdB00(0,x,0))

    def test_dB00_0y(self):
        test.assert_allclose(dB00(0,y), cdB00(0,0,y))

    # test C0 from COLLIER against analytical C0 implementation
    def test_C0(self):
        for p in combinations_with_replacement([x,y,z,0],3):
            if p[1] != 0 and p[2] != 0:
                test.assert_allclose(C0(*p), cC0(0,0,0,*p))
