#!/usr/bin/env python3
import unittest
from anyBSM import anyBSM, loopfunctions
import numpy.testing as test
from cmath import pi, sqrt
import logging
logging.getLogger('anyBSM').setLevel(logging.WARNING)

# different particle restrictions
SM = anyBSM('SM', evaluation='numerical', caching = 0, progress = False, quiet = True)
SM.load_renormalization_scheme('MS')
SM.setparameters()
p = SM.all_particles
higgs = p['h']

v = SM.parameters['vvSM'].nvalue
Mt = SM.all_particles['u3'].nmass
Mh = higgs.nmass
MZ = SM.parameters['MZ'].nvalue
MWp = SM.parameters['MWp'].nvalue
Mb = SM.all_particles['d3'].nmass
Md2 = SM.all_particles['d2'].nmass
Md1 = SM.all_particles['d1'].nmass
Mu2 = SM.all_particles['u2'].nmass
Mu1 = SM.all_particles['u1'].nmass
Me3 = SM.all_particles['e3'].nmass
Me2 = SM.all_particles['e2'].nmass
Me1 = SM.all_particles['e1'].nmass

loopfunctions.set_renscale(Mt)

loopfunctions.MSDR = int(not SM.dimensional_reduction) # legacy

SMall = anyBSM('SM', particles_only=['h','Hp','Ah','Hpc','Wp', 'Z', 'A','gWp', 'gWC', 'gZ','gA','u3'], evaluation='numerical', caching = 0, progress = False,scheme_name="OS", quiet = True)
SMall.setparameters()
SMall.setparameters({"Qren":Mt})
pall = SMall.all_particles

SMscalar = anyBSM('SM', particles_only=['h','Ah','Hp','Hpc'],evaluation='numerical', caching = 0, progress = False,scheme_name="OS", quiet = True)
SMscalar.setparameters()
SMscalar.setparameters({"Qren":Mt})
pscalar = SMscalar.all_particles

SMtop = anyBSM('SM', particles_only=['u3'], evaluation='numerical', caching = 0, progress = False,scheme_name="OS", quiet = True)
SMtop.setparameters()
SMtop.setparameters({"Qren":SMtop.all_particles['u3'].mass})
ptop = SMtop.all_particles

SMtb = anyBSM('SM', particles_only=['u3','d3'], evaluation='numerical', caching = 0, progress = False,scheme_name="OS", quiet = True)
SMtb.setparameters()
SMtb.setparameters({"Qren":SMtop.all_particles['u3'].mass})

SMboson = anyBSM('SM', particles_only=['h','Hp','Ah','Hpc','Wp','Z','gWp','gWC', 'gZ'], evaluation='numerical', caching = 0, progress = False,scheme_name="OS", quiet = True)
SMboson.setparameters()
SMboson.setparameters({"Qren":Mt})
pboson = SMboson.all_particles

SMgauge = anyBSM('SM', particles_only=['Wp','Z','A'], evaluation='numerical', caching = 0, progress = False,scheme_name="OS", quiet = True)
SMgauge.setparameters()
SMgauge.setparameters({"Qren":Mt})
pgauge = SMgauge.all_particles

SMgauge2 = anyBSM('SM', particles_only=['Z','Ah'], evaluation='numerical', caching = 0, progress = False,scheme_name="OS", quiet = True)
SMgauge2.setparameters()
SMgauge2.setparameters({"Qren":Mt})

SMghost = anyBSM('SM', particles_only=['gWp','gWC', 'gZ','gA'], evaluation='numerical', caching = 0, progress = False,scheme_name="MS", quiet = True)
SMghost.setparameters()
SMghost.setparameters({"Qren":Mt})
pghost = SMghost.all_particles

SMG0 = anyBSM('SM', particles_only=['Ah'], evaluation='numerical', caching = 0, progress = False,scheme_name="OS", quiet = True)
SMG0.setparameters()
SMG0.setparameters({"Qren":Mt})
pG0 = SMG0.all_particles

SMlf = anyBSM('SM', particles_only=['nu1','nu2','nu3','d1','d2','d3','u1','u2','e1','e2','e3'], evaluation='numerical', caching = 0, progress = False,scheme_name="OS", quiet = True)
SMlf.setparameters()
SMlf.setparameters({"Qren":Mt})
plf = SMlf.all_particles

SMfermion = anyBSM('SM', particles_only=['nu1','nu2','nu3','d1','d2','d3','u1','u2','u3','e1','e2','e3'], evaluation='numerical', caching = 0, progress = False,scheme_name="OS", quiet = True)
SMfermion.setparameters()
SMfermion.setparameters({"Qren":Mt})


alpha = 1/(SMall._eval('aEWM1'))
EL = sqrt(4*pi*alpha)
CW2 = SMall._eval('MWp/MZ')**2
SW2 = 1-CW2

loopfunctions.set_renscale(Mt)
a0mh = loopfunctions.A0(Mh**2)
a0mt = loopfunctions.A0(Mt**2)
a0mb = loopfunctions.A0(Mb**2)
a0mz = loopfunctions.A0(MZ**2)
a0mw = loopfunctions.A0(MWp**2)
b0mh = loopfunctions.B0(Mh**2,Mh**2,Mh**2)
b0mt = loopfunctions.B0(Mh**2,Mt**2,Mt**2)
b0mw = loopfunctions.B0(Mh**2,MWp**2,MWp**2)
b0mz = loopfunctions.B0(Mh**2,MZ**2,MZ**2)

def hhh1LsFC():
    return - alpha*EL*Mh**4/(64*pi*MWp**3*SW2*sqrt(SW2))*( 27*loopfunctions.B0(Mh**2,Mh**2,Mh**2)+6*loopfunctions.B0(Mh**2,MWp**2,MWp**2)+3*loopfunctions.B0(Mh**2,MZ**2,MZ**2)+2*Mh**2*(27*loopfunctions.C0(Mh**2,Mh**2,Mh**2,Mh**2,Mh**2,Mh**2)+2*loopfunctions.C0(Mh**2,Mh**2,Mh**2,MWp**2,MWp**2,MWp**2)+loopfunctions.C0(Mh**2,Mh**2,Mh**2,MZ**2,MZ**2,MZ**2)))

def hhh1LvFC():
    return alpha*EL*MWp/(8*pi*CW2**3*sqrt(SW2)*SW2)*(3*CW2*loopfunctions.MSDR*(1+2*CW2**2)-12*CW2**3*loopfunctions.B0(Mh**2,MWp**2,MWp**2)-6*CW2*loopfunctions.B0(Mh**2,MZ**2,MZ**2)-16*CW2**3*MWp**2*loopfunctions.C0(Mh**2,Mh**2,Mh**2, MWp**2,MWp**2,MWp**2)-8*MWp**2*loopfunctions.C0(Mh**2,Mh**2,Mh**2,MZ**2,MZ**2,MZ**2))

def hhh1LuFC():
    return alpha*EL/(16*pi*CW2*SW2*sqrt(CW2*SW2))*(2*sqrt(CW2)*CW2*MWp**3*loopfunctions.C0(Mh**2,Mh**2,Mh**2,MWp**2,MWp**2,MWp**2)+MZ**3*loopfunctions.C0(Mh**2,Mh**2,Mh**2,MZ**2,MZ**2,MZ**2))

def hhh1LhFC():
    return - 27*alpha*EL*Mh**4/(64*pi*MWp**3*sqrt(SW2)*SW2)*( loopfunctions.B0(Mh**2,Mh**2,Mh**2)+2*Mh**2*loopfunctions.C0(Mh**2,Mh**2,Mh**2,Mh**2,Mh**2,Mh**2))

def hhh1LGZFC():
    return - alpha*EL/(64*pi*MWp**3*sqrt(SW2)*SW2)*(3*(Mh**4-2*Mh**2*MZ**2+12*MZ**4)*loopfunctions.B0(Mh**2,MZ**2,MZ**2)+2*(Mh**6-2*Mh**4*MZ**2-16*Mh**2*MZ**4+26*MZ**6)*loopfunctions.C0(Mh**2,Mh**2,Mh**2,MZ**2,MZ**2,MZ**2)-6*MZ**2*(4*loopfunctions.MSDR*MZ**2+Mh**2*(Mh**2+2*MZ**2)*(loopfunctions.C1(Mh**2,Mh**2,Mh**2,MZ**2,MZ**2,MZ**2)+loopfunctions.C2(Mh**2,Mh**2,Mh**2,MZ**2,MZ**2,MZ**2))))

def hhh1LGpWFC():
    return alpha*EL/(32*pi*MWp**3*sqrt(SW2)*SW2)*(-3*(Mh**4-2*Mh**2*MWp**2+12*MWp**4)*loopfunctions.B0(Mh**2,MWp**2,MWp**2)-2*(Mh**6-2*Mh**4*MWp**2-16*Mh**2*MWp**4+26*MWp**6)*loopfunctions.C0(Mh**2,Mh**2,Mh**2,MWp**2,MWp**2,MWp**2)+6*MWp**2*(4*loopfunctions.MSDR*MWp**2+Mh**2*(Mh**2+2*MWp**2)*( loopfunctions.C1(Mh**2,Mh**2,Mh**2,MWp**2,MWp**2,MWp**2)+loopfunctions.C2(Mh**2,Mh**2,Mh**2,MWp**2,MWp**2,MWp**2) )))

class numericTest(unittest.TestCase):
    """ Test genuine 1L corrections """

    # Eff-Pot approximation (top quark contrib.)
    def test_top(self):
        # Our result
        OurLambda = SMtop.lambdahhh(momenta=[0,0,0])
        # e.q (1) from hep-ph/0211308 :
        LambdaEffective = OurLambda['treelevel']*(1-Mt**4/(pi*v*Mh)**2)
        test.assert_allclose(LambdaEffective, OurLambda['treelevel'] + OurLambda['genuine'])

    # Full external momentum (top quark contrib.)
    def test_top_full_momentum(self):
        # Our result
        OurLambda = SMtop.lambdahhh(momenta=['auto'])
        # analytical result
        p12 = Mh**2
        p22 = Mh**2
        p32 = Mh**2
        p2p3 = (p12 - p22 - p32)/2 # noqa: F841
        loopfunctions.pyCollier.set_renscale(Mt**2) # noqa: F841
        B0 = loopfunctions.pyCollier.b0 # noqa: F841
        C0 = loopfunctions.pyCollier.c0 # noqa: F841
        C1 = loopfunctions.pyCollier.c1 # noqa: F841
        C2 = loopfunctions.pyCollier.c2 # noqa: F841
        nloshiftanalytic = eval("""2*(1/(16*v**3*pi**2))*6*Mt**4*(
            6*B0(p32, Mt**2, Mt**2)
            + (p12 + p22 - p32 + 8*Mt**2)*C0(p22, p32, p12, Mt**2, Mt**2, Mt**2)
            + 2*(p12 + 3*p22 - p32)     *C1(p22, p32, p12, Mt**2, Mt**2, Mt**2)
            + 2*(3*p12 + p22 - p32)     *C2(p22, p32, p12, Mt**2, Mt**2, Mt**2)
        )""")
        test.assert_allclose(nloshiftanalytic, OurLambda['genuine'])

    # Test scalar contributions
    def test_scalar(self):
        hhh1LsanyBSM = SMscalar.lambdahhh(simplify = False, momenta = ['auto'])['genuine']
        test.assert_allclose(hhh1LsanyBSM, hhh1LsFC())

    # Test gauge contributions
    def test_gauge(self):
        hhh1LvanyBSM = SMgauge.lambdahhh(simplify = False, momenta = ['auto'])['genuine']
        test.assert_allclose(hhh1LvanyBSM, hhh1LvFC())

    # Test scalar+gauge contributions
    def test_scalar_gauge(self):
        hhh1LsvanyBSM = SMboson.lambdahhh(simplify = False, momenta = ['auto'])['genuine']
        test.assert_allclose(hhh1LsvanyBSM, hhh1LhFC()+hhh1LGZFC()+hhh1LGpWFC()+hhh1LuFC())

    # Test Goldstone + Z contributions
    def test_GZ(self):
        hhh1LGZanyBSM = SMgauge2.lambdahhh(simplify = False, momenta = ['auto'])['genuine']
        test.assert_allclose(hhh1LGZanyBSM, hhh1LGZFC())

    # Test Ghost contributions
    def test_ghost(self):
        hhh1LuanyBSM = SMghost.lambdahhh(simplify = False, momenta = ['auto'])['genuine']
        test.assert_allclose(hhh1LuanyBSM, hhh1LuFC())

    # Test Goldstone only contributions
    def test_goldstone(self):
        hhh1LGanyBSM = SMG0.lambdahhh(simplify = False, momenta = ['auto'])['genuine']
        hhhGGGFC = alpha*EL*Mh**6*MZ**2/(32*pi*MWp**3*sqrt(SW2)*(MWp**2-MZ**2))*loopfunctions.C0(Mh**2,Mh**2,Mh**2,MZ**2,MZ**2,MZ**2)
        hhhGGFC = - 3*alpha*EL*Mh**4/(64*pi*MWp**3*sqrt(SW2)*SW2)*loopfunctions.B0(Mh**2,MZ**2,MZ**2)
        test.assert_allclose(hhh1LGanyBSM, hhhGGGFC + hhhGGFC)

    # Test tadpole contributions
    def test_tadpole(self):
        hhhTAanyBSM = SMall.lambdahhh(simplify = False, momenta = ['auto'])['tads']
        hhhTAFC = 3*alpha*EL/(64*pi*MWp**3*SW2*sqrt(SW2))*(Mh**2*(3*a0mh+2*a0mw+a0mz)-24*Mt**2*a0mt + 12*MWp**2*a0mw+6*MZ**2*a0mz-4*loopfunctions.MSDR*(2*MWp**4+MZ**4))
        test.assert_allclose(hhhTAanyBSM, hhhTAFC)

    # Test WFR contributions
    # internal cross-check
    def test_wfr_internal(self):
        dZH = sum(SMall.process('h','h',derivative = True, momenta=[Mh**2], simplify = False).values())
        hhhWFRdZ = 3/2*3*Mh**2/v*dZH
        hhhWFRanyBSM = SMall.lambdahhh(simplify = False, momenta = ['auto'])['wfr']
        test.assert_allclose(hhhWFRdZ, hhhWFRanyBSM)

    # external cross-check
    def test_wfr_external(self):
        hhhWFRanyBSM = SMall.lambdahhh(simplify = False, momenta = ['auto'])['wfr']
        hhhWFRsfFC = - 3/2*3*Mh**2/v*alpha/(32*pi*MWp**2*SW2)*(Mh**4*(9*loopfunctions.dB0(Mh**2,Mh**2,Mh**2)+2*loopfunctions.dB0(Mh**2,MWp**2,MWp**2)+loopfunctions.dB0(Mh**2,MZ**2, MZ**2))-24*Mt**2*(-loopfunctions.B0(Mh**2,Mt**2,Mt**2)/2 + 2*Mt**2*loopfunctions.dB0(Mh**2,Mt**2,Mt**2)-Mh**2/2*loopfunctions.dB0(Mh**2,Mt**2,Mt**2)))
        hhhWFRgbFC = 3/2*3*Mh**2/v*alpha/(16*pi*MWp**2*SW2)*(-16*MWp**4*loopfunctions.dB0(Mh**2,MWp**2,MWp**2)-8*MZ**4*loopfunctions.dB0(Mh**2,MZ**2,MZ**2))
        hhhWFRghostFC = 3/2*3*Mh**2/v*alpha/(16*pi*MWp**2*SW2)*(2*MWp**4*loopfunctions.dB0(Mh**2,MWp**2,MWp**2)+MZ**4*loopfunctions.dB0(Mh**2,MZ**2,MZ**2))
        hhhWFRsgbFC = 3/2*3*Mh**2/v*alpha/(16*pi*MWp**2*SW2)*(4*MWp**2*loopfunctions.B0(Mh**2,MWp**2, MWp**2)+2*MZ**2*loopfunctions.B0(Mh**2,MZ**2,MZ**2)+4*Mh**2*MWp**2*loopfunctions.dB0(Mh**2,MWp**2,MWp**2)+2*MWp**4*loopfunctions.dB0(Mh**2,MWp**2,MWp**2)+2*Mh**2*MZ**2*loopfunctions.dB0(Mh**2,MZ**2,MZ**2)+MZ**4*loopfunctions.dB0(Mh**2,MZ**2,MZ**2))
        test.assert_allclose(hhhWFRanyBSM, hhhWFRsfFC + hhhWFRgbFC + hhhWFRghostFC + hhhWFRsgbFC)

    def test_Higgs_mass_ren(self):
        """ test Higgs mass renormalization """
        hhhWFRanyBSM = SMall.lambdahhh(simplify = False, momenta = ['auto'])['massren']
        hhhmassrenbyhand = - 3/v*sum(SMall.process('h','h', momenta=[Mh**2], simplify = False).values())
        test.assert_allclose(hhhWFRanyBSM, hhhmassrenbyhand)

    def test_se_hh_A(self):
        """ test Higgs self-energy """
        PihhAtotanyBSM = sum(SMall.process('h','h',momenta=[Mh**2],only_topologies=['TwoPointA']).values())
        PihhAsFC = - alpha/(32*pi*SW2*MWp**2)*Mh**2*(3*a0mh+2*a0mw+a0mz)
        PihhAvFC = alpha/(8*pi*CW2*SW2)*(loopfunctions.MSDR*(2*CW2*MWp**2+MZ**2)-4*CW2*a0mw - 2*a0mz)
        test.assert_allclose(PihhAtotanyBSM, PihhAsFC + PihhAvFC)

    def test_se_hh_B_scalar(self):
        PihhBsanyBSM = sum(SMscalar.process('h','h',momenta=[Mh**2] , only_topologies=['TwoPointB']).values())
        PihhBsFC  = - alpha*Mh**4/(32*pi*MWp**2*SW2)*(9*b0mh+2*b0mw+b0mz)
        test.assert_allclose(PihhBsanyBSM, PihhBsFC)

    def test_se_hh_B_top(self):
        PihhBtanyBSM = sum(SMtop.process('h','h',momenta=[Mh**2], only_topologies=['TwoPointB']).values())
        PihhBtFC = 12*alpha*Mt**2/(16*pi*MWp**2*SW2)*(a0mt+(2*Mt**2-Mh**2/2)*b0mt)
        test.assert_allclose(PihhBtanyBSM, PihhBtFC)

    def test_se_hh_B_pure_gauge(self):
        PihhBvanyBSM = sum(SMgauge.process('h','h',momenta=[Mh**2], only_topologies=['TwoPointB']).values())
        PihhBvFC = alpha*MWp**2/(4*pi*CW2**2*SW2)*(loopfunctions.MSDR+2*CW2**2*loopfunctions.MSDR - 4*CW2**2*b0mw-2*b0mz)
        test.assert_allclose(PihhBvanyBSM, PihhBvFC)

    def test_se_hh_B_ghost(self):
        PihhBuanyBSM = sum(SMghost.process('h','h',momenta=[Mh**2], only_topologies=['TwoPointB']).values())
        PihhBuFC = alpha/(16*pi*CW2*SW2)*(2*CW2*MWp**2*b0mw+MZ**2*b0mz)
        test.assert_allclose(PihhBuanyBSM, PihhBuFC)

    def test_se_hh_B_total(self):
        PihhBtotanyBSM = sum(SMall.process('h','h',momenta=[Mh**2], only_topologies=['TwoPointB']).values())
        PihhBtFC = 12*alpha*Mt**2/(16*pi*MWp**2*SW2)*(a0mt+(2*Mt**2-Mh**2/2)*b0mt)
        PihhBsFC  = - alpha*Mh**4/(32*pi*MWp**2*SW2)*(9*b0mh+2*b0mw+b0mz)
        PihhBgaugeFC = alpha/(16*pi*CW2**2*SW2)*(4*loopfunctions.MSDR*MWp**2 + 8*CW2**2*loopfunctions.MSDR*MWp**2+2*CW2**2*a0mw+CW2*a0mz+2*CW2**2*Mh**2*b0mw-14*CW2**2*MWp**2*b0mw+CW2*Mh**2*b0mz-8*MWp**2*b0mz+CW2*MZ**2*b0mz + 2*CW2**2*Mh**2*b0mw+CW2*Mh**2*b0mz)
        PihhBuFC = alpha/(16*pi*CW2*SW2)*(2*CW2*MWp**2*b0mw+MZ**2*b0mz)
        test.assert_allclose(PihhBtotanyBSM, PihhBsFC+PihhBtFC+PihhBgaugeFC+PihhBuFC)

    def test_se_hh_tad(self):
        PihhTAtotanyBSM = sum(SMall.process('h','h',momenta=[Mh**2], only_topologies=['TwoPointTA']).values())
        PihhTAsFC  = 3*alpha*Mh**2*(3*a0mh+2*a0mw+a0mz)/(32*pi*MWp**2*SW2)
        PihhTAtFC  = - 36*alpha*Mt**2*a0mt/(16*pi*MWp**2*SW2)
        PihhTAvFC  = - 6*alpha/(16*pi*CW2*SW2)*(loopfunctions.MSDR*(2*CW2*MWp**2+MZ**2)-4*CW2*a0mw-2*a0mz)
        PihhTAuFC  = - 3*alpha/(16*pi*SW2*MWp**2)*(2*MWp**2*a0mw+MZ**2*a0mz)
        test.assert_allclose(PihhTAtotanyBSM, PihhTAsFC+PihhTAtFC+PihhTAvFC+PihhTAuFC)

    def test_se_GG_tot(self):
        """ test Goldstone self-energy """
        PiGGAtotanyBSM = sum(SM.process('Ah','Ah',momenta=[MZ**2], only_topologies=['TwoPointA']).values())
        PiGGAtotFC = alpha/(32*pi*MWp**2*SW2)*(8*loopfunctions.MSDR*MWp**4 + 4*loopfunctions.MSDR*MZ**4-Mh**2*a0mh-2*(Mh**2+8*MWp**2)*a0mw - (3*Mh**2+8*MZ**2)*a0mz)
        test.assert_allclose(PiGGAtotanyBSM, PiGGAtotFC)

    def test_se_GG_scalar(self):
        PiGGBsanyBSM = sum(SMscalar.process('Ah', 'Ah',momenta=[MZ**2] ,only_topologies=['TwoPointB']).values())
        PiGGBsFC = - alpha*Mh**4/(16*pi*MWp**2*SW2)*loopfunctions.B0(MZ**2,Mh**2, MZ**2)
        test.assert_allclose(PiGGBsanyBSM, PiGGBsFC)

    def test_se_GG_scalar_gauge(self):
        PiGGBsvanyBSM = sum(SMboson.process('Ah', 'Ah',momenta=[MZ**2] ,only_topologies=['TwoPointB']).values())
        PiGGBsanyBSM = sum(SMscalar.process('Ah', 'Ah',momenta=[MZ**2] ,only_topologies=['TwoPointB']).values())
        PiGGBuanyBSM = sum(SMghost.process('Ah', 'Ah',momenta=[MZ**2] ,only_topologies=['TwoPointB']).values())
        PiGGBsvFC = alpha/(16*pi*MWp**2*SW2)*(-MZ**2*a0mh+2*MWp**2*a0mw + 2*MZ**2*a0mz + 2*Mh**2*MZ**2*loopfunctions.B0(MZ**2,Mh**2,MZ**2)+MZ**4*loopfunctions.B0(MZ**2,Mh**2,MZ**2)+2*MWp**4*loopfunctions.B0(MZ**2,MWp**2,MWp**2)+4*MWp**2*MZ**2*loopfunctions.B0(MZ**2,MWp**2,MWp**2))
        test.assert_allclose(PiGGBsvanyBSM-PiGGBsanyBSM-PiGGBuanyBSM, PiGGBsvFC)

    def test_se_GG_top(self):
        PiGGBtopanyBSM = sum(SMtop.process('Ah', 'Ah',momenta=[MZ**2] ,only_topologies=['TwoPointB']).values())
        PiGGBtopFC = 12*alpha*Mt**2/(16*pi*MWp**2*SW2)*(a0mt-MZ**2/2*loopfunctions.B0(MZ**2,Mt**2,Mt**2))
        test.assert_allclose(PiGGBtopanyBSM, PiGGBtopFC)

    def test_se_GG_ghost(self):
        PiGGBuanyBSM = sum(SMghost.process('Ah', 'Ah',momenta=[MZ**2] ,only_topologies=['TwoPointB']).values())
        PiGGBuFC = - alpha*MWp**2/(8*pi*SW2)*loopfunctions.B0(MZ**2,MWp**2,MWp**2)
        test.assert_allclose(PiGGBuanyBSM, PiGGBuFC)

    def test_se_GG_tad(self):
        PiGGTAtotanyBSM = sum(SMall.process('Ah','Ah',momenta=[MZ**2], only_topologies=['TwoPointTA']).values())
        PiGGTAtotFC = - alpha/(32*pi*MWp**2*SW2)*(8*loopfunctions.MSDR*MWp**4 + 4*loopfunctions.MSDR*MZ**4-3*Mh**2*a0mh + 24*Mt**2*a0mt-2*(Mh**2+6*MWp**2)*a0mw - (Mh**2+6*MZ**2)*a0mz)
        test.assert_allclose(PiGGTAtotanyBSM, PiGGTAtotFC)

    def test_se_ZZ_A_scalar(self):
        """ test Z self-energy """
        PiZZAsanyBSM = sum(SMscalar.process('Z','Z',momenta=[MZ**2], only_topologies=['TwoPointA']).values())
        PiZZAsFC = alpha/(16*pi*CW2*SW2)*(a0mh+2*(CW2-SW2)**2*a0mw+a0mz)
        test.assert_allclose(PiZZAsanyBSM, PiZZAsFC)

    def test_se_ZZ_A_vector(self):
        PiZZAvanyBSM = sum(SMgauge.process('Z','Z',momenta=[MZ**2], only_topologies=['TwoPointA']).values())
        PiZZAvFC = - alpha*CW2/(2*pi*SW2)*(2*loopfunctions.MSDR*MWp**2-3*a0mw)
        test.assert_allclose(PiZZAvanyBSM, PiZZAvFC)

    def test_se_ZZ_B_scalar(self):
        PiZZBsanyBSM = sum(SMscalar.process('Z','Z',momenta=[MZ**2], only_topologies=['TwoPointB']).values())
        PiZZBsFC = - alpha/(4*pi*CW2*SW2)*(loopfunctions.B00(MZ**2,Mh**2,MZ**2)+(CW2-SW2)**2*loopfunctions.B00(MZ**2,MWp**2,MWp**2))
        test.assert_allclose(PiZZBsanyBSM, PiZZBsFC)

    def test_se_ZZ_B_top(self):
        PiZZBtanyBSM = sum(SMtop.process('Z','Z',momenta=[MZ**2], only_topologies=['TwoPointB']).values())
        PiZZBtFC = - alpha/(24*pi*CW2*SW2)*((9-24*SW2+32*SW2**2)*a0mt + 9*Mt**2*loopfunctions.B0(MZ**2,Mt**2,Mt**2)-(9-24*SW2+32*SW2**2)*(2*loopfunctions.B00(MZ**2,Mt**2,Mt**2)+MZ**2/2*loopfunctions.B0(MZ**2,Mt**2,Mt**2)))
        test.assert_allclose(PiZZBtanyBSM, PiZZBtFC)

    def test_se_ZZ_B_lf(self):
        PiZZBlfanyBSM = sum(SMlf.process('Z','Z',momenta=[MZ**2], only_topologies=['TwoPointB']).values())
        PiZZBbFC = - alpha/(24*pi*CW2*SW2)*((9-12*SW2+8*SW2**2)*loopfunctions.A0(Mb**2)+9*Mb**2*loopfunctions.B0(MZ**2,Mb**2,Mb**2)-2*(9-12*SW2+8*SW2**2)*loopfunctions.B00(MZ**2,Mb**2,Mb**2)+MZ**2*(-1/2*(9-12*SW2+8*SW2**2)*loopfunctions.B0(MZ**2,Mb**2,Mb**2)))
        PiZZBotherlfFC = - alpha/(24*pi*CW2*SW2)*((9-12*SW2+8*SW2**2)*loopfunctions.A0(Md2**2)+9*Md2**2*loopfunctions.B0(MZ**2,Md2**2,Md2**2)-2*(9-12*SW2+8*SW2**2)*loopfunctions.B00(MZ**2,Md2**2,Md2**2)+MZ**2*(-1/2*(9-12*SW2+8*SW2**2)*loopfunctions.B0(MZ**2,Md2**2,Md2**2)))-alpha/(24*pi*CW2*SW2)*((9-12*SW2+8*SW2**2)*loopfunctions.A0(Md1**2)+9*Md1**2*loopfunctions.B0(MZ**2,Md1**2,Md1**2)-2*(9-12*SW2+8*SW2**2)*loopfunctions.B00(MZ**2,Md1**2,Md1**2)+MZ**2*(-1/2*(9-12*SW2+8*SW2**2)*loopfunctions.B0(MZ**2,Md1**2,Md1**2)))-alpha/(24*pi*CW2*SW2)*((9-24*SW2+32*SW2**2)*loopfunctions.A0(Mu2**2)+9*Mu2**2*loopfunctions.B0(MZ**2,Mu2**2,Mu2**2)-(9-24*SW2+32*SW2**2)*(2*loopfunctions.B00(MZ**2,Mu2**2,Mu2**2)+MZ**2/2*loopfunctions.B0(MZ**2,Mu2**2,Mu2**2)))-alpha/(24*pi*CW2*SW2)*((9-24*SW2+32*SW2**2)*loopfunctions.A0(Mu1**2)+9*Mu1**2*loopfunctions.B0(MZ**2,Mu1**2,Mu1**2)-(9-24*SW2+32*SW2**2)*(2*loopfunctions.B00(MZ**2,Mu1**2,Mu1**2)+MZ**2/2*loopfunctions.B0(MZ**2,Mu1**2,Mu1**2)))+6*alpha/(16*pi*CW2*SW2)*(2*loopfunctions.B00(MZ**2,0,0)+MZ**2/2*loopfunctions.B0(MZ**2,0,0))-alpha/(8*pi*CW2*SW2)*((1-4*SW2+8*SW2**2)*loopfunctions.A0(Me3**2)+Me3**2*loopfunctions.B0(MZ**2,Me3**2,Me3**2)-(1-4*SW2+8*SW2**2)*(2*loopfunctions.B00(MZ**2,Me3**2,Me3**2)+MZ**2/2*loopfunctions.B0(MZ**2,Me3**2,Me3**2)))-alpha/(8*pi*CW2*SW2)*((1-4*SW2+8*SW2**2)*loopfunctions.A0(Me2**2)+Me2**2*loopfunctions.B0(MZ**2,Me2**2,Me2**2)-(1-4*SW2+8*SW2**2)*(2*loopfunctions.B00(MZ**2,Me2**2,Me2**2)+MZ**2/2*loopfunctions.B0(MZ**2,Me2**2,Me2**2)))-alpha/(8*pi*CW2*SW2)*((1-4*SW2+8*SW2**2)*loopfunctions.A0(Me1**2)+Me1**2*loopfunctions.B0(MZ**2,Me1**2,Me1**2)-(1-4*SW2+8*SW2**2)*(2*loopfunctions.B00(MZ**2,Me1**2,Me1**2)+MZ**2/2*loopfunctions.B0(MZ**2,Me1**2,Me1**2)))
        test.assert_allclose(PiZZBlfanyBSM, PiZZBbFC+PiZZBotherlfFC)

    def test_se_ZZ_B_gauge(self):
        PiZZBvanyBSM = sum(SMgauge.process('Z','Z',momenta=[MZ**2], only_topologies=['TwoPointB']).values())
        PiZZBvFC = - alpha*CW2/(12*pi*SW2)*(loopfunctions.MSDR*(-12*MWp**2+2*MZ**2)+6*a0mw + 3*(2*MWp**2+5*MZ**2)*loopfunctions.B0(MZ**2,MWp**2,MWp**2)+30*loopfunctions.B00(MZ**2,MWp**2,MWp**2)-3*MZ**2*loopfunctions.B0(MZ**2,MWp**2,MWp**2))
        test.assert_allclose(PiZZBvanyBSM, PiZZBvFC)

    def test_se_ZZ_B_ghost(self):
        PiZZBuanyBSM = sum(SMghost.process('Z','Z',momenta=[MZ**2], only_topologies=['TwoPointB']).values())
        PiZZBuFC = alpha*CW2/(2*pi*SW2)*loopfunctions.B00(MZ**2,MWp**2,MWp**2)
        test.assert_allclose(PiZZBuanyBSM, PiZZBuFC)

    def test_se_ZZ_B_total(self):
        PiZZBtotanyBSM = sum(SM.process('Z','Z',momenta=[MZ**2], only_topologies=['TwoPointB']).values())
        PiZZBsFC = - alpha/(4*pi*CW2*SW2)*(loopfunctions.B00(MZ**2,Mh**2,MZ**2)+(CW2-SW2)**2*loopfunctions.B00(MZ**2,MWp**2,MWp**2))
        PiZZBtFC = - alpha/(24*pi*CW2*SW2)*((9-24*SW2+32*SW2**2)*a0mt + 9*Mt**2*loopfunctions.B0(MZ**2,Mt**2,Mt**2)-(9-24*SW2+32*SW2**2)*(2*loopfunctions.B00(MZ**2,Mt**2,Mt**2)+MZ**2/2*loopfunctions.B0(MZ**2,Mt**2,Mt**2)))
        PiZZBvFC = - alpha*CW2/(12*pi*SW2)*(loopfunctions.MSDR*(-12*MWp**2+2*MZ**2)+6*a0mw + 3*(2*MWp**2+5*MZ**2)*loopfunctions.B0(MZ**2,MWp**2,MWp**2)+30*loopfunctions.B00(MZ**2,MWp**2,MWp**2)-3*MZ**2*loopfunctions.B0(MZ**2,MWp**2,MWp**2))
        PiZZBsvFC = alpha*MWp**2/(4*pi*CW2**2*SW2)*(loopfunctions.B0(MZ**2,Mh**2,MZ**2)+2*CW2*SW2**2*loopfunctions.B0(MZ**2,MWp**2,MWp**2))
        PiZZBuFC = alpha*CW2/(2*pi*SW2)*loopfunctions.B00(MZ**2,MWp**2,MWp**2)
        PiZZBbFC = - alpha/(24*pi*CW2*SW2)*((9-12*SW2+8*SW2**2)*loopfunctions.A0(Mb**2)+9*Mb**2*loopfunctions.B0(MZ**2,Mb**2,Mb**2)-2*(9-12*SW2+8*SW2**2)*loopfunctions.B00(MZ**2,Mb**2,Mb**2)+MZ**2*(-1/2*(9-12*SW2+8*SW2**2)*loopfunctions.B0(MZ**2,Mb**2,Mb**2)))
        PiZZBotherlfFC = - alpha/(24*pi*CW2*SW2)*((9-12*SW2+8*SW2**2)*loopfunctions.A0(Md2**2)+9*Md2**2*loopfunctions.B0(MZ**2,Md2**2,Md2**2)-2*(9-12*SW2+8*SW2**2)*loopfunctions.B00(MZ**2,Md2**2,Md2**2)+MZ**2*(-1/2*(9-12*SW2+8*SW2**2)*loopfunctions.B0(MZ**2,Md2**2,Md2**2)))-alpha/(24*pi*CW2*SW2)*((9-12*SW2+8*SW2**2)*loopfunctions.A0(Md1**2)+9*Md1**2*loopfunctions.B0(MZ**2,Md1**2,Md1**2)-2*(9-12*SW2+8*SW2**2)*loopfunctions.B00(MZ**2,Md1**2,Md1**2)+MZ**2*(-1/2*(9-12*SW2+8*SW2**2)*loopfunctions.B0(MZ**2,Md1**2,Md1**2)))-alpha/(24*pi*CW2*SW2)*((9-24*SW2+32*SW2**2)*loopfunctions.A0(Mu2**2)+9*Mu2**2*loopfunctions.B0(MZ**2,Mu2**2,Mu2**2)-(9-24*SW2+32*SW2**2)*(2*loopfunctions.B00(MZ**2,Mu2**2,Mu2**2)+MZ**2/2*loopfunctions.B0(MZ**2,Mu2**2,Mu2**2)))-alpha/(24*pi*CW2*SW2)*((9-24*SW2+32*SW2**2)*loopfunctions.A0(Mu1**2)+9*Mu1**2*loopfunctions.B0(MZ**2,Mu1**2,Mu1**2)-(9-24*SW2+32*SW2**2)*(2*loopfunctions.B00(MZ**2,Mu1**2,Mu1**2)+MZ**2/2*loopfunctions.B0(MZ**2,Mu1**2,Mu1**2)))+6*alpha/(16*pi*CW2*SW2)*(2*loopfunctions.B00(MZ**2,0,0)+MZ**2/2*loopfunctions.B0(MZ**2,0,0))-alpha/(8*pi*CW2*SW2)*((1-4*SW2+8*SW2**2)*loopfunctions.A0(Me3**2)+Me3**2*loopfunctions.B0(MZ**2,Me3**2,Me3**2)-(1-4*SW2+8*SW2**2)*(2*loopfunctions.B00(MZ**2,Me3**2,Me3**2)+MZ**2/2*loopfunctions.B0(MZ**2,Me3**2,Me3**2)))-alpha/(8*pi*CW2*SW2)*((1-4*SW2+8*SW2**2)*loopfunctions.A0(Me2**2)+Me2**2*loopfunctions.B0(MZ**2,Me2**2,Me2**2)-(1-4*SW2+8*SW2**2)*(2*loopfunctions.B00(MZ**2,Me2**2,Me2**2)+MZ**2/2*loopfunctions.B0(MZ**2,Me2**2,Me2**2)))-alpha/(8*pi*CW2*SW2)*((1-4*SW2+8*SW2**2)*loopfunctions.A0(Me1**2)+Me1**2*loopfunctions.B0(MZ**2,Me1**2,Me1**2)-(1-4*SW2+8*SW2**2)*(2*loopfunctions.B00(MZ**2,Me1**2,Me1**2)+MZ**2/2*loopfunctions.B0(MZ**2,Me1**2,Me1**2)))
        test.assert_allclose(PiZZBtotanyBSM, PiZZBvFC+PiZZBsFC+PiZZBsvFC+PiZZBuFC + PiZZBtFC+PiZZBbFC+PiZZBotherlfFC)

    def test_se_ZZ_tadpole(self):
        PiZZTAtotanyBSM = sum(SMall.process('Z','Z',momenta=[MZ**2], only_topologies=['TwoPointTA']).values())
        PiZZTAtotFC = - alpha/(16*pi*sqrt(CW2)*CW2**2*Mh**2*SW2)*( - 8*sqrt(CW2)*CW2*loopfunctions.MSDR*MWp**4 - 4*sqrt(CW2)*MWp**2*MZ**2+3*sqrt(CW2)*CW2*Mh**2*a0mh - 24*sqrt(CW2)*CW2*Mt**2*a0mt+2*sqrt(CW2)*CW2*Mh**2*a0mw + 12*sqrt(CW2)*CW2*MWp**2*a0mw+sqrt(CW2)*CW2*Mh**2*a0mz + 8*sqrt(CW2)*MWp**2*a0mz-2*CW2*MWp*MZ*a0mz)
        test.assert_allclose(PiZZTAtotanyBSM, PiZZTAtotFC)

    def test_se_WW_A_scalar(self):
        """ test W self-energy """
        PiWWAsanyBSM = sum(SMscalar.process('Wp', 'Wpc',momenta=[MWp**2],only_topologies=["TwoPointA"]).values())
        PiWWAsFC = alpha/(16*pi*SW2)*(a0mh+2*a0mw+a0mz)
        test.assert_allclose(PiWWAsanyBSM, PiWWAsFC)

    def test_se_WW_A_gauge(self):
        PiWWAvanyBSM = sum(SMgauge.process('Wp', 'Wpc',momenta=[MWp**2],only_topologies=["TwoPointA"]).values())
        PiWWAWFC = - alpha/(4*pi*SW2)*(2*loopfunctions.MSDR*(MWp**2)-3*a0mw)
        PiWWAZFC = - alpha/(4*pi*SW2)*(2*loopfunctions.MSDR*(CW2*MZ**2)-3*CW2*a0mz)
        test.assert_allclose(PiWWAvanyBSM, PiWWAZFC+PiWWAWFC)

    def test_se_WW_B_scalar(self):
        PiWWBsanyBSM = sum(SMscalar.process('Wp', 'Wpc',momenta=[MWp**2],only_topologies=["TwoPointB"]).values())
        PiWWBsFC = - alpha/(4*pi*SW2)*(loopfunctions.B00(MWp**2,Mh**2,MWp**2)+loopfunctions.B00(MWp**2,MWp**2,MZ**2))
        test.assert_allclose(PiWWBsanyBSM, PiWWBsFC)

    def test_se_WW_B_topbot(self):
        PiWWBtbanyBSM = sum(SMtb.process('Wp', 'Wpc',momenta=[MWp**2],only_topologies=["TwoPointB"]).values())
        PiWWBtbFC = - 6*alpha/(16*pi*SW2)*(loopfunctions.A0(Mb**2)+a0mt+(Mb**2+Mt**2-MWp**2)*loopfunctions.B0(MWp**2,Mb**2,Mt**2)-4*loopfunctions.B00(MWp**2,Mb**2,Mt**2))
        test.assert_allclose(PiWWBtbanyBSM, PiWWBtbFC)

    def test_se_WW_B_gauge(self):
        PiWWBgbanyBSM = sum(SMgauge.process('Wp', 'Wpc',momenta=[MWp**2],only_topologies=["TwoPointB"]).values())
        PiWWBgbFC = alpha/(12*pi*SW2)*(4*loopfunctions.MSDR*MWp**2+6*CW2*loopfunctions.MSDR*MZ**2-3*a0mw-3*CW2*a0mz-15*SW2*MWp**2*loopfunctions.B0(MWp**2,0,MWp**2)-15*CW2*MWp**2*loopfunctions.B0(MWp**2,MWp**2,MZ**2)-3*CW2*MZ**2*loopfunctions.B0(MWp**2,MWp**2,MZ**2)-30*SW2*loopfunctions.B00(MWp**2,0,MWp**2)-30*CW2*loopfunctions.B00(MWp**2,MWp**2,MZ**2))
        test.assert_allclose(PiWWBgbanyBSM, PiWWBgbFC)

    def test_se_WW_B_ghost(self):
        PiWWBuanyBSM = sum(SMghost.process('Wp', 'Wpc',momenta=[MWp**2],only_topologies=["TwoPointB"]).values())
        PiWWBuFC = alpha/(2*pi)*(loopfunctions.B00(MWp**2,0,MWp**2)+CW2/SW2*loopfunctions.B00(MWp**2,MWp**2,MZ**2))
        test.assert_allclose(PiWWBuanyBSM, PiWWBuFC)

    def test_se_WW_tad(self):
        PiWWTAtotanyBSM = sum(SMall.process('Wp', 'Wpc',momenta=[MWp**2],only_topologies=["TwoPointTA"]).values())
        PiWWTAtotFC = - alpha/(16*pi*sqrt(CW2)*CW2*SW2*Mh**2)*(-8*sqrt(CW2)*CW2*loopfunctions.MSDR*MWp**4-4*sqrt(CW2)*loopfunctions.MSDR*MWp**2*MZ**2+3*sqrt(CW2)*CW2*Mh**2*a0mh-24*sqrt(CW2)*CW2*Mt**2*a0mt+2*sqrt(CW2)*CW2*Mh**2*a0mw+12*sqrt(CW2)*CW2*MWp**2*a0mw+sqrt(CW2)*CW2*Mh**2*a0mz+8*sqrt(CW2)*MWp**2*a0mz-2*CW2*MWp*MZ*a0mz)
        test.assert_allclose(PiWWTAtotanyBSM, PiWWTAtotFC)

    def test_se_AA_A_scalar(self):
        """ test photon self-energy """
        PiAAAsanyBSM = sum(SMscalar.process('A','A',momenta=[0], only_topologies=["TwoPointA"]).values())
        PiAAAsFC = alpha/(2*pi)*a0mw
        test.assert_allclose(PiAAAsanyBSM, PiAAAsFC)

    def test_se_AA_A_gauge(self):
        PiAAAvanyBSM = sum(SMgauge.process('A','A',momenta=[0], only_topologies=["TwoPointA"]).values())
        PiAAAvFC = - alpha/(2*pi)*(2*loopfunctions.MSDR*MWp**2-3*a0mw)
        test.assert_allclose(PiAAAvanyBSM, PiAAAvFC)

    def test_se_AA_B_gauge(self):
        PiAABbosonanyBSM = sum(SMboson.process('A','A',momenta=[0], only_topologies=["TwoPointB"]).values())
        PiAABuFC = alpha/(2*pi)*loopfunctions.B00(0,MWp**2,MWp**2)
        PiAABsFC = - alpha/(pi)*loopfunctions.B00(0,MWp**2,MWp**2)
        PiAABvFC = alpha/(2*pi)*(2*loopfunctions.MSDR*MWp**2-a0mw-MWp**2*loopfunctions.B0(0,MWp**2,MWp**2)-5*loopfunctions.B00(0,MWp**2,MWp**2))
        PiAABsvFC = alpha/(2*pi)*MWp**2*loopfunctions.B0(0,MWp**2,MWp**2)
        test.assert_allclose(PiAABbosonanyBSM, PiAABsFC+PiAABsvFC+PiAABvFC+PiAABuFC)

    def test_se_AA_B_topbot(self):
        PiAABfanyBSM = sum(SMtb.process('A','A',momenta=[0], only_topologies=["TwoPointB"]).values())
        PiAABfFC = - alpha/(3*pi)*(a0mb+4*a0mt-2*(loopfunctions.B00(0,Mb**2,Mb**2)+4*loopfunctions.B00(0,Mt**2,Mt**2)))
        test.assert_allclose(PiAABfanyBSM, PiAABfFC, rtol = 0, atol = 1e-10)

    def test_se_AA_B_ghost(self):
        PiAABuanyBSM = sum(SMghost.process('A','A',momenta=[0], only_topologies=["TwoPointB"]).values())
        PiAABuFC = alpha/(2*pi)*loopfunctions.B00(0,MWp**2,MWp**2)
        test.assert_allclose(PiAABuanyBSM, PiAABuFC)

    def test_se_AA_tad(self):
        PiAATAanyBSM = sum(SMall.process('A','A',momenta=[0], only_topologies=["TwoPointTA"]).values())
        test.assert_allclose(0, PiAATAanyBSM, rtol = 0, atol = 1e-10)

    def test_dse_AA(self):
        dPiAAtotanyBSM = sum(SMall.process('A','A',momenta=[0], derivative = True).values())
        dPiAAtotFC = - alpha/(6*pi)*(loopfunctions.MSDR-4*loopfunctions.B0(0,Mt**2,Mt**2)+6*loopfunctions.B0(0,MWp**2,MWp**2)-16*loopfunctions.dB00(0,Mt**2,Mt**2)+18*loopfunctions.dB00(0,MWp**2,MWp**2))
        test.assert_allclose(dPiAAtotanyBSM,dPiAAtotFC)

    def test_se_AZ_A_scalar(self):
        """ test photon-Z self-energy """
        Zsign = SM.getSignSinThetaW()
        PiAZAsanyBSM = sum(SMscalar.process('A','Z',momenta=[0], only_topologies=["TwoPointA"]).values())
        PiAZAsFC = alpha/(4*pi*sqrt(CW2*SW2))*(CW2-SW2)*a0mw
        test.assert_allclose(Zsign*PiAZAsanyBSM,PiAZAsFC)

    def test_se_AZ_A_gauge(self):
        Zsign = SM.getSignSinThetaW()
        PiAZAvFC = - alpha/(2*pi*sqrt(SW2))*sqrt(CW2)*(2*loopfunctions.MSDR*MWp**2-3*a0mw)
        PiAZAvanyBSM = sum(SMgauge.process('A','Z',momenta=[0], only_topologies=["TwoPointA"]).values())
        test.assert_allclose(Zsign*PiAZAvanyBSM,PiAZAvFC)

    def test_se_AZ_B_scalar_gauge(self):
        Zsign = SM.getSignSinThetaW()
        PiAZBsvanyBSM = sum(SMboson.process('A','Z',momenta=[0], only_topologies=["TwoPointB"]).values())
        PiAZBsvFC = - alpha/(2*pi*sqrt(CW2))*MWp**2*sqrt(SW2)*loopfunctions.B0(0,MWp**2,MWp**2)
        PiAZBvFC = alpha/(2*pi)*sqrt(CW2/SW2)*(2*loopfunctions.MSDR*MWp**2-a0mw-MWp**2*loopfunctions.B0(0,MWp**2,MWp**2)-5*loopfunctions.B00(0,MWp**2,MWp**2))
        PiAZBsFC = - alpha/(2*pi*sqrt(CW2*SW2))*(CW2-SW2)*loopfunctions.B00(0,MWp**2,MWp**2)
        PiAZBuFC = alpha/(2*pi)*sqrt(CW2/SW2)*loopfunctions.B00(0,MWp**2,MWp**2)
        test.assert_allclose(Zsign*PiAZBsvanyBSM,PiAZBsFC+PiAZBvFC+PiAZBsvFC+PiAZBuFC)

    def test_se_AZ_B_top(self):
        Zsign = SM.getSignSinThetaW()
        PiAZBtopanyBSM = sum(SMtop.process('A','Z',momenta=[0], only_topologies=["TwoPointB"]).values())
        PiAZBtopFC = alpha/(6*pi*sqrt(SW2*CW2))*(-3+8*SW2)*(a0mt-2*loopfunctions.B00(0,Mt**2,Mt**2))
        test.assert_allclose(Zsign*PiAZBtopanyBSM,PiAZBtopFC)

    def test_se_AZ_B_ghost(self):
        Zsign = SM.getSignSinThetaW()
        PiAZBuanyBSM = sum(SMghost.process('A','Z',momenta=[0], only_topologies=["TwoPointB"]).values())
        PiAZBuFC = alpha/(2*pi)*sqrt(CW2/SW2)*loopfunctions.B00(0,MWp**2,MWp**2)
        test.assert_allclose(Zsign*PiAZBuanyBSM,PiAZBuFC)

    def test_se_AZ_tad(self):
        PiAZTAanyBSM = sum(SM.process('A','Z',momenta=[0], only_topologies=["TwoPointTA"]).values())
        test.assert_allclose(PiAZTAanyBSM,0, rtol = 0, atol = 1e-10)

    def test_lambdahhh_OS(self):
        """ test whether result for lambdahhh has changed w.r.t. previous versions"""
        SM.load_renormalization_scheme('OS')
        test.assert_allclose(SM.lambdahhh(momenta = ['auto'])['total'].real, 179.367762)

    def test_lambdahhh_MS(self):
        """ test whether result for lambdahhh has changed w.r.t. previous versions"""
        SM.load_renormalization_scheme('MS')
        test.assert_allclose(SM.lambdahhh(momenta = ['auto'])['total'].real, 167.036221)

    def test_MW(self):
        """ test whether result for MW has changed w.r.t. previous versions"""
        SM.load_renormalization_scheme('OS')
        test.assert_allclose(SM.MW(), 80.350091)
