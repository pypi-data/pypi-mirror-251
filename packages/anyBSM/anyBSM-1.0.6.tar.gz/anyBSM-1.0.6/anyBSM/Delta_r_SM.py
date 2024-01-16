# expression adapted from FeynHiggs-2.18.1 (src/EWPO/Deltar.F)

import logging
import numpy as np
import cmath
from typing import Tuple
from anyBSM.loopfunctions import A0, B0, B00, B1

def Delta_r_SM(
        MWrun: float, MWfw: float, MZrun: float, MZfw: float,
        MHSM: float, MT: float, MB: float,
        Alfa0: float, AlfasMT: float, DeltaAlfa: float, GF: float,
        ME: float, MM: float, ML: float, MU: float, MD: float, MC: float, MS: float,
        CKM: np.array = np.array([[1,0,0],[0,1,0],[0,0,1]]),
        calc_1L: bool = False
        ) -> Tuple[float, float, float]:
    """ Calculates $\\Delta r_\\text{SM}$ at 1L, 2L, and beyond.

    Args:
       MWrun: $M_W$ using running width definition
       MWfw: $M_W$ using fixed width definition
       MZrun: $M_Z$ using running width definition
       MZfw: $M_Z$ using fixed width definition
       MHSM: SM Higgs boson mass
       MT: Top-quark mass
       MB: Bottom-quark mass
       Alfa0: fine-structure constant
       AlfasMT: stronge gauge coupling at the top-quark mass scale, $\\alpha_s(M_t)$
       DeltaAlfa: running contribution to the electromagnetic coupling, $\\Delta\\alpha = \\Delta\\alpha_\\text{had}^{(5)}(M_Z) + \\Delta\\alpha_\\text{lept}$
       GF: Fermi constant, $G_F$
       ME: electron mass
       MM: muon mass
       ML: tau mass
       MU: up-quark mass
       MD: down-quark mass
       MC: charm-quark mass
       MS: strange-quark mass
       CKM: CKM matrix
       calc_1L: whether 1L correction to $\\Delta r_\\text{SM}$ is evaluated (zero is returned for $\\Delta r_\\text{SM}^{(1)}$ if false)

    Returns:
       $\\Delta r_\\text{SM}^{(1)}$, $\\Delta r_\\text{SM}^{(2),\\text{rem}}$, $\\Delta r_\\text{SM}^{(>2)}$
    """

    # numerical constants

    pi = np.pi
    zeta2 = pi**2/6
    sqrt2 = np.sqrt(2)

    # function defintions

    def log(x):
        return cmath.log(x)

    def sqrt(x):
        return cmath.sqrt(x)

    def Re(x):
        return np.real(x)

    def KniehlX1(x, b0, b1, c0, c1, c2, c3, c4):
        return zeta2*(b0 + b1*x**2)*log(2*x) + \
              c0 + x*(c1 + x*(c2 + x*(c3 + x*c4)))

    def KniehlV1(x):
        return KniehlX1(sqrt(1 - .25*x), -12, 20, 1.0829, 8*pi, 8.4465, -66.3923, 22.6086)

    def KniehlA1(x):
        return KniehlX1(sqrt(1 - .25*x), 0, 8, -.6043, 0, -9.7824, -6.5179, .8861)

    def KniehlF1(x):
        return (1 - x)**2*log(1 - x) * \
              (3/8*log(1 - x) - 1.6449340668 - 9/8) - \
              1.1881 + x*(-2.0979 + x*(4.1157
                  + x*(-2.2082 + x*(3.6968 - 2.1815*x))))

    # parameter definitions

    CKM2 = CKM*np.conjugate(CKM)
    # pad CKM2 matrix with zeros in first column/row resulting in CKM[i,j] -> CKM[i+i,j+i]
    # matching Fortran array indexing
    CKM2 = np.hstack((np.zeros((3,1)), CKM2))
    CKM2 = np.vstack((np.zeros((1,4)), CKM2))

    ME2 = ME**2
    MM2 = MM**2
    ML2 = ML**2
    MU2 = MU**2
    MD2 = MD**2
    MC2 = MC**2
    MS2 = MS**2
    MT2 = MT**2
    MB2 = MB**2

    MWfw2 = MWfw**2
    MZfw2 = MZfw**2

    MH = MHSM
    MH2 = MHSM**2

    CW = MWfw/MZfw
    CW2 = CW**2
    SW2 = 1 - CW2
    CTW2 = CW2/SW2

    Qu = 2/3
    Qd = -1/3

    asDr = AlfasMT/pi
    aDr = Alfa0/pi

    # 1L corrections
    if calc_1L:

        DrSM1Lferm0 = \
            -((aDr*(1/8.*(((1 + (2 - 4*SW2)*SW2)
                    * (Re(A0(ME2)) + Re(A0(ML2)) + Re(A0(MM2))))
                     / MWfw2 + ((3 + 4*SW2)*Re(A0(MS2)))/MZfw2)
                 + 3/16.*Re(B0(MZfw2,0.,0.))
                 + 1/144.*(108 *
                      (SW2 *
                       (MT2*Re(B0(0.,MB2,MT2))
                           + MC2*Re(B0(0.,MC2,MS2))
                           + MU2*Re(B0(0.,MD2,MU2)))
                       + (CW2 - SW2)
                       * ((MT2 - MWfw2)*Re(B0(MWfw2,MB2,MT2))
                           + MC2*Re(B0(MWfw2,MC2,MS2))
                           + (MU2 - MWfw2)*Re(B0(MWfw2,MD2,MU2))))
                     - SW2*(9*(ME2 + ML2 + MM2) - 64*MWfw2*SW2
                        + 216
                         * (Re(B00(0.,MB2,MT2))
                          + Re(B00(0.,MC2,MS2)) + Re(B00(0.,MD2,MU2))
                            )) -
                     72*(CW2 - SW2)
                * (Re(B00(MWfw2,0.,ME2)) +
                   Re(B00(MWfw2,0.,ML2))
                   + Re(B00(MWfw2,0.,MM2))
                   + 3*(Re(B00(MWfw2,MB2,MT2))
                        + Re(B00(MWfw2,MC2,MS2))
                        + Re(B00(MWfw2,MD2,MU2)))))/MWfw2
                 - (1/72.*((32*MZfw2*SW2**2 +
                          3*MT2*(9 - (24 - 32*SW2)*SW2)) *
                        Re(A0(MT2)))/MT2
                  + 1/8.*(-((3 + 4*SW2)*Re(A0(MB2))) +
                       3*Re(A0(MC2)) - 3*Re(A0(MD2))
                       + 3*Re(A0(MU2))
                       - SW2
                        * (8*Re(A0(MC2)) + 4*Re(A0(MD2))
                          + 8*Re(A0(MU2))))
                    + 1/48.*((18*MT2
                         - MZfw2*(9 - (24 - 32*SW2)*SW2)) *
                       Re(B0(MZfw2,MT2,MT2)))
                  + 1/16.*((6*MB2 - MZfw2*(3 - 4*SW2)) *
                        Re(B0(MZfw2,MB2,MB2))
                       + (6*MC2 - MZfw2*(3 - 8*SW2))
                        * Re(B0(MZfw2,MC2,MC2))
                       + (6*MD2 - MZfw2*(3 - 4*SW2))
                        * Re(B0(MZfw2,MD2,MD2))
                       + (2*ME2 - MZfw2*(1 - 4*SW2))
                        * Re(B0(MZfw2,ME2,ME2))
                       + (2*ML2 - MZfw2*(1 - 4*SW2))
                        * Re(B0(MZfw2,ML2,ML2))
                       + (2*MM2 - MZfw2*(1 - 4*SW2))
                        * Re(B0(MZfw2,MM2,MM2))
                       + (6*MS2 - MZfw2*(3 - 4*SW2))
                        * Re(B0(MZfw2,MS2,MS2))
                       + (6*MU2 - MZfw2*(3 - 8*SW2))
                        * Re(B0(MZfw2,MU2,MU2)))
                    - 3/4.*Re(B00(MZfw2,0.,0.))
                  + 1/4.*(-((3 - 4*SW2)*Re(B00(MZfw2,MB2,MB2))) -
                       (3 - 8*SW2)*Re(B00(MZfw2,MC2,MC2))
                       - (3 - 4*SW2)*Re(B00(MZfw2,MD2,MD2))
                       - (1 - 4*SW2)*(Re(B00(MZfw2,ME2,ME2))
                       + Re(B00(MZfw2,ML2,ML2))
                       + Re(B00(MZfw2,MM2,MM2))) -
                    (3 - 4*SW2)*Re(B00(MZfw2,MS2,MS2)))
                    - 1/12.*((9 - (24 - 32*SW2)*SW2)
                       * Re(B00(MZfw2,MT2,MT2)))
                    - 1/4.*((3 - 8*SW2)*Re(B00(MZfw2,MU2,MU2))))/MZfw2
                 + 1/4.*((CW2 - SW2) *
                    (Re(B1(MWfw2,0.,ME2)) + Re(B1(MWfw2,0.,ML2)) +
                        Re(B1(MWfw2,0.,MM2))
                     - 3*(Re(B1(MWfw2,MB2,MT2)) -
                         Re(B1(MWfw2,MC2,MS2)) + Re(B1(MWfw2,MD2,MU2))
                          )))))/SW2**2)

        DrSM1LfermCKM = aDr*(((3/4.*(MT2*(1 - CKM2[3,3])*Re(B0(0.,MB2,MT2)) +
                      MC2*(1 - CKM2[2,2])*Re(B0(0.,MC2,MS2))
                      + MU2*(1 - CKM2[1,1])*Re(B0(0.,MD2,MU2)))
                   - 3/4.*(MC2 *
                       (CKM2[2,3]*Re(B0(0.,MB2,MC2))
                        + CKM2[2,1]*Re(B0(0.,MC2,MD2)))
                      + MT2*(CKM2[3,1]*Re(B0(0.,MD2,MT2))
                         + CKM2[3,2]*Re(B0(0.,MS2,MT2)))
                      + MU2*(CKM2[1,3]*Re(B0(0.,MB2,MU2))
                         + CKM2[1,2]*Re(B0(0.,MS2,MU2)))) -
                   3/2.*((1 - CKM2[3,3])*Re(B00(0.,MB2,MT2))
                      + (1 - CKM2[2,2])*Re(B00(0.,MC2,MS2))
                      + (1 - CKM2[1,1])*Re(B00(0.,MD2,MU2)))
                   + 3/2.*(CKM2[2,3]*Re(B00(0.,MB2,MC2)) +
                      CKM2[1,3]*Re(B00(0.,MB2,MU2))
                      + CKM2[2,1]*Re(B00(0.,MC2,MD2))
                      + CKM2[3,1]*Re(B00(0.,MD2,MT2))
                      + CKM2[3,2]*Re(B00(0.,MS2,MT2))
                      + CKM2[1,2]*Re(B00(0.,MS2,MU2))))/SW2 +
                ((CW2 - SW2) *
                 (3/4.*((MT2 - MWfw2)*(1 - CKM2[3,3]) *
                        Re(B0(MWfw2,MB2,MT2))
                        + MC2*(1 - CKM2[2,2])*Re(B0(MWfw2,MC2,MS2))
                        + (MU2 - MWfw2)*(1 - CKM2[1,1])
                        * Re(B0(MWfw2,MD2,MU2)))
                    - 3/4.*((MC2 - MWfw2)*CKM2[2,3] *
                         Re(B0(MWfw2,MB2,MC2))
                        + MC2*CKM2[2,1]*Re(B0(MWfw2,MC2,MD2))
                        + (MT2 - MWfw2)
                         * (CKM2[3,1]*Re(B0(MWfw2,MD2,MT2))
                           + CKM2[3,2]*Re(B0(MWfw2,MS2,MT2)))
                        + (MU2 - MWfw2)
                         * (CKM2[1,3]*Re(B0(MWfw2,MB2,MU2))
                          + CKM2[1,2]*Re(B0(MWfw2,MS2,MU2)))) -
                     3/2.*((1 - CKM2[3,3])
                         * Re(B00(MWfw2,MB2,MT2))
                        + (1 - CKM2[2,2])*Re(B00(MWfw2,MC2,MS2))
                        + (1 - CKM2[1,1])*Re(B00(MWfw2,MD2,MU2)))
                    + 3/2.*(CKM2[2,3]*Re(B00(MWfw2,MB2,MC2)) +
                        CKM2[1,3]*Re(B00(MWfw2,MB2,MU2))
                        + CKM2[2,1]*Re(B00(MWfw2,MC2,MD2))
                        + CKM2[3,1]*Re(B00(MWfw2,MD2,MT2))
                        + CKM2[3,2]*Re(B00(MWfw2,MS2,MT2))
                        + CKM2[1,2]*Re(B00(MWfw2,MS2,MU2)))))/SW2**2) /
              MWfw2 + 3/4.*((CW2 - SW2) *
                 (CKM2[2,3]*Re(B1(MWfw2,MB2,MC2)) -
                  (1 - CKM2[3,3])*Re(B1(MWfw2,MB2,MT2))
                  + CKM2[1,3]*Re(B1(MWfw2,MB2,MU2))
                  - CKM2[2,1]*Re(B1(MWfw2,MC2,MD2))
                  + (1 - CKM2[2,2])*Re(B1(MWfw2,MC2,MS2))
                  + CKM2[3,1]*Re(B1(MWfw2,MD2,MT2))
                  - (1 - CKM2[1,1])*Re(B1(MWfw2,MD2,MU2))
                  + CKM2[3,2]*Re(B1(MWfw2,MS2,MT2))
                  + CKM2[1,2]*Re(B1(MWfw2,MS2,MU2))))/SW2**2)

        DrSM1Lbos = -(aDr *
             (1/4.*((1 - 2*CW2)*Re(B0(MWfw2,MH2,MWfw2)) +
                   (MZfw2*((5 - SW2*(18 - (18 - 4*SW2)*SW2)) *
                         Re(B0(MWfw2,MWfw2,MZfw2))
                        + CW2*Re(B0(MZfw2,MH2,MZfw2))))/MWfw2)/SW2**2
                 + (1/4.*((8*MWfw2 + MZfw2)*Re(B00(0.,MWfw2,MZfw2)) +
                      MZfw2*(Re(B00(0.,MH2,MWfw2)) +
                         (8 - 16*SW2)*Re(B00(MWfw2,0.,MWfw2))))
                    / (MZfw2*SW2)
                  + (1/8.*((13 - 4*SW2*(10 - (8 - 3*SW2)*SW2)) *
                         Re(A0(MWfw2))
                        - (1 + (14 - 2*CW2)*CW2**2)*Re(A0(MZfw2))
                        - 4*CW2**2*MZfw2*(3 - 4*SW2)
                         * Re(B0(MZfw2,MWfw2,MWfw2))
                        - 2*(((1 - 2*CW2) *
                            (8*MWfw2*Re(B00(MWfw2,MWfw2,MZfw2)) +
                              MZfw2
                              * (Re(B00(MWfw2,MH2,MWfw2)) +
                              Re(B00(MWfw2,MWfw2,MZfw2)))))/MZfw2 +
                           CW2
                            * (Re(B00(MZfw2,MH2,MZfw2))
                              + (1 + CW2*(8 - 12*SW2))
                              * Re(B00(MZfw2,MWfw2,MWfw2)))))
                     - 1/16.*(MZfw2 *
                        (SW2 *
                         (5 - 2*(8 - 5*SW2)*SW2 +
                             ((1 - 2*CW2*SW2)
                              * (MZfw2 - 2*Re(A0(MZfw2))))/MZfw2
                          - CW2
                            * (8 *
                              (1/2.
                              * (-1/2.
                              + ((2 - 2*CW2)*Re(A0(MWfw2)))/MWfw2)
                              + ((2 - 4*SW2)*(MWfw2 + Re(A0(MWfw2))))
                              / MWfw2)
                              - 4
                              * ((SW2 *
                              (9*(MWfw2 - Re(A0(MWfw2))) +
                              Re(A0(MWfw2))))/MWfw2 +
                              Re(B0(0.,MH2,MWfw2)))) -
                          4*(2 - SW2*(2 + SW2))
                            * Re(B0(0.,MWfw2,MZfw2))) -
                         8*(1 - 2*CW2)*CW2**2
                         * Re(B1(MWfw2,MWfw2,MZfw2)))))/SW2**2)/MWfw2))

        DrSM1L = DeltaAlfa + DrSM1Lferm0 + DrSM1LfermCKM + DrSM1Lbos
    else:
        DrSM1L = 0.

    # >= 2L corrections

    dW = MWrun/80.404 - 1
    dZZ = MZrun/91.1876 - 1
    dH = MH/100
    lH = log(dH)
    dT = MT/178
    dT = (dT - 1)*(dT + 1)

    DrSM2Lrem = .003354 + \
    (-2.09e-4 + (2.54e-5 - 7.85e-6*lH**2)*lH)*lH - \
    2.33e-6*(dH - 1)*(dH + 1) + \
    (7.83e-3 - 9.89e-6*lH + 3.38e-3*dT)*dT + \
    (.0939 + .204*dT)*dW - \
    .103*dZZ

    w = MWfw2/MT2
    z = MZfw2/MT2
    l = log(z)
    DrSM2LQCD = 1/pi * sqrt2/pi*GF*MWfw2*SW2 * asDr*(
                 -.25/(SW2**2*z)*(
                 (1 - 8/3*SW2)**2*KniehlV1(z) + KniehlA1(z)
                 - .25*(1 + (1 - 4/3*SW2)**2)*z*l ) +
                 1/(SW2**2*w)*((CW2 - SW2)*KniehlF1(w) + SW2*KniehlF1(0.))
                 - 1/(SW2**2)*(CW2 - SW2)*log(CW)
                 + 2*Qu**2*(2.404114 - 5/12) - Qd**2*l )

    DrSM3LtbQCD = -3*CTW2*MT2 * GF/(8*sqrt2*pi**2) * asDr**2*(
                     -14.594 + (-17.224 +
                     (.08829 + .4722*l)*l
                     + (22.6367 + (1.2527 - .8519*l)*l)*SW2
                     + (-7.7781 + (-.07226 + .004938*l)*l +
                         SW2*(21.497 - 21.0799*SW2 +
                         (.05794 - .006584*l)*l))*z)*z )

    x = MH/MT - 1
    if x <= 1.4:
        DrhoSM3LGF3MT6 = 95.92 + (-111.98 + (8.099
                    + (9.36 + (7.27 - 15.6*x)*x)*x)*x)*x
        DrhoSM3LasGF2MT4 = 157.295 + (112 + (-24.73
                        + (7.39 + (-3.52 + 2.06*x)*x)*x)*x)*x
    else:
        x = 4*MT2/MH2
        l = log(x)
        DrhoSM3LGF3MT6 = (-3.17 - 83.25*l)/x - \
        189.93 + (-231.48 + (-142.06 + 2.75*l)*l)*l + \
        ( -332.34 + (77.71 + (-68.67 + 51.79*l)*l)*l +
          ( 227.55 + (-510.55 + (87.77 + 6.41*l)*l)*l +
            ( -58.4 + (-329.18 + (20.42 + 14.54*l)*l)*l +
              ( -36.14 + (-381.88 + (18.63 + 15.04*l)*l)*l +
                ( -39.08 + (-416.36 + (13.76 + 17.19*l)*l)*l
                  )*x )*x )*x )*x )*x
        DrhoSM3LasGF2MT4 = 79.73 + (-47.77 + (42.07 + 9*l)*l)*l + \
        ( 225.16 + (-179.74 + (70.22 - 19.22*l)*l)*l +
          ( -76.07 + (25.33 + (-9.17 - 5.57*l)*l)*l +
            ( -10.1 + (-24.69 + (-.3 - 5.46*l)*l)*l +
              ( -4.52 + (-32.85 + (.72 - 5.25*l)*l)*l +
                ( -2.55 + (-36.61 + (1.06 - 5.14*l)*l)*l
                  )*x )*x )*x )*x )*x

    Xt = GF*MT2/(8*sqrt2*pi**2)
    DrSMGFMT = -CTW2*Xt**2*(Xt*DrhoSM3LGF3MT6 + asDr*DrhoSM3LasGF2MT4)

    DrSM34L = -CTW2*3*Xt*(7.9326 - 101.0827)*asDr**3

    DrSMho = DrSM2LQCD + DrSM3LtbQCD + DrSMGFMT + DrSM34L

    logging.debug("DrSM1L", DrSM1L)
    logging.debug("DrSM2Lrem", DrSM2Lrem)
    logging.debug("DrSMho", DrSMho)

    return DrSM1L, DrSM2Lrem, DrSMho
