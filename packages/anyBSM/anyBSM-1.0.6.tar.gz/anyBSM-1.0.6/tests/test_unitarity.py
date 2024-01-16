#!/usr/bin/env python3
import unittest
from anyBSM import anyPerturbativeUnitarity
import numpy.testing as test
import logging
logging.getLogger('anyBSM').setLevel(logging.WARNING)


THDM = anyPerturbativeUnitarity('THDMII', quiet = True, progress = False)

# result obtained with SPheno using the same default input parameters
eigSSSS_SPheno = 0.52212574

class numericTest(unittest.TestCase):

    def test_eigSSSS(self):
        """ compute and compare largest SS->SS scattering eigenvalue """
        eigSSSS_anyBSM = THDM.eigSSSS()
        test.assert_allclose(eigSSSS_SPheno, eigSSSS_anyBSM)
