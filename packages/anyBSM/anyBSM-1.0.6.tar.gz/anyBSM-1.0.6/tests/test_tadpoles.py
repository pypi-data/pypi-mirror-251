#!/usr/bin/env python3
import unittest
from anyBSM import anyBSM
import numpy.testing as test
import logging
logging.getLogger('anyBSM').setLevel(logging.WARNING)

class numericTest(unittest.TestCase):
    """ checks equivalence between FJ and OS treatment of tadpoles in aligned SM and THDM """

    def test_SM(self):
        SM = anyBSM('SM', quiet = True, progress = False)
        SM.clear_cache()
        SM.load_renormalization_scheme('OS')
        lam_FJ = SM.lambdahhh()['total']
        SM.load_renormalization_scheme('OStadpoles')
        lam_tOS = SM.lambdahhh()['total']
        test.assert_allclose(lam_FJ,lam_tOS)

    def test_THDM(self):
        THDM = anyBSM('THDMII', quiet = True, progress = False)
        THDM.clear_cache()
        THDM.setparameters({'SinBmA': 1})
        THDM.load_renormalization_scheme('OSalignment')
        lam_FJ = THDM.lambdahhh()['total']
        THDM.load_renormalization_scheme('OSalignmentadpoles')
        lam_tOS = THDM.lambdahhh()['total']
        test.assert_allclose(lam_FJ,lam_tOS)
