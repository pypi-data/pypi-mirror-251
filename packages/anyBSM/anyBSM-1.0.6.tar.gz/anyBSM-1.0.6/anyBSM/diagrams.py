#!/bin/python
from __future__ import division
from anyBSM.utils import fieldtypes
from anyBSM.loopfunctions import A0, B0, B00, dB0, dB00, B1, dB1, C0, C1, C2, eps # noqa: F401
from anyBSM.ufo.function_library import complexconjugate, I # noqa: F401
import logging
import functools

__doc__ = """ # AnyDiagram
A module to store the analytic results of Feynman diagrams populated
with fields that couple with the most general Lorentz structure
without assuming any relations between the field masses and
couplings.\n

The analytic results are expressed in terms of the generic couplings,
masses and Passarino Veltman functions.
"""

logger = logging.getLogger('anyBSM.diagrams')

def multIply(coup, fac = 1):
    """ Multiply Feynman rule (UFO coupling) with -I to receive the
    parameter from the Lagrangian """
    try:
        return -I*fac*coup # numerical mode
    except:
        return f'-I*({fac})*({coup})' # analytical mode

def getCouplingNum(coupling, attribute = 'nvalue'):
    """ Get the (numerical) coupling from the `anyBSM.getcoupling()`-result"""
    coup = {i : multIply(c.get(attribute), coupling.get('sign', 1)) for i,c in coupling.items() if i != 'sign'}
    return coup.get('c',coup)

def iszero(CLR):
    """ check if a vertex (i.e. all its couplings) `CLR` is numerically negligible """
    if type(CLR) == dict:
        return all([abs(c) < eps for c in CLR.values()])
    return abs(CLR) < eps

def conj(CLR):
    """ Take the complex conjugate of a vertex (in case of a
    non-scalar vertex, all couplings are conjugated) """
    if type(CLR) == dict:
        return {k: conj(v) for k,v in CLR.items()}
    if type(CLR) == str:
        return f'complexconjugate({CLR})'
    return CLR.conjugate()

def diagram(Next=0,Nint=0,Nvert=0):
    """ Decorator for the actual generic diagrams. It ensures that the
    diagram with `Next`/`Nint` external/internal fields and `Nvert`
    vertices receives the correct inputs (number of couplings, masses
    etc) and prepares all information ready to be used in the generic
    analytic expressions.

    @diagram passes a dictionary of the form:
    ```python
    d = {
        'external' : [ externalfield1, ... ],
        'momenta'  : [ p12, p22, ...],
        'couplings' : [ CSSS, {'L': CFFSL, 'R': CFFSR}, ... ],
        'internal' : [ internalfield1, ... ],
        'masses' : [ MassOfinternalfield1, ... ],
        'factor' : symmetryfactor*colorfactor*loopfactor
    }
    ```
    to the actual generic diagram.
    """
    def wrapper2(diag):
        @functools.wraps(diag, updated=())
        def wrapper(self,**kwargs):
            all_args = ['external', 'factor', 'coupling_objects', 'internal', 'momenta']
            for arg in all_args:
                assert arg in kwargs , f"{diag.__name__}: missing argument {arg})"
            assert Next == len(kwargs['external']), f"{diag.__name__}"
            assert Nint == len(kwargs['internal']), f'{diag.__name__}'
            assert Nvert == len(kwargs['coupling_objects']), f'{diag.__name__}'
            couplings_num = [getCouplingNum(c, self.coupling_values) for c in kwargs['coupling_objects']]
            if self.anyzero(*couplings_num):
                return self.zero
            inttype = fieldtypes(kwargs['internal'])
            exttype = fieldtypes(kwargs['external'])
            masses = [p.get(self.mass_values) for p in kwargs['internal']]
            if 'derivative' not in kwargs:
                kwargs['derivative'] = False
            result = diag(self,**kwargs, couplings = couplings_num, inttype = inttype, exttype = exttype, masses = masses)
            if result is None:
                logger.error(f"{diag.__name__} with external={exttype} and internal={inttype} not (correctly) implemented!")
                return self.zero
            if not result:
                result = self.zero
            else:
                if self.evaluation == 'numerical' and type(result) == str:
                    result  = eval(result)
                elif not (result.startswith('+') or result.startswith('-')):
                    result = '+' + result
            logger.debug(f"{diag.__name__}({list(kwargs['internal'])}) = {result}")
            return result
        return wrapper
    return wrapper2

class GenericDiagrams():
    """
        Defines results for all generic amplitudes.
        Each class method with the @`diagram()` decorator is supposed
        to return a string with the masses and couplings inserted into
        the generic diagram it represents.\n
        Example:
        ```python
        GenericDiagrams.OnePointA(
            momenta = [],
            external = [h1],
            internal = [u3],
            coupling_objects = [{"L": GC_79, "R": GC_80}],
            derivative = False,
            factor = '1/(16*pi**2)')
        ```
        calculates the top quark contribution to the Higgs boson
        tadpole.
    """

    def __init__(self, evaluation = 'abbreviations', MSDR = 1):
        """
            * `evaluation`: evaluation mode as in anyBSM.anyBSM
            * `MSDR`: whether to work in $\\overline{\\text{MS}}$ (1) or
            $\\overline{\\text{DR}}$ (0).
        """
        self.evaluation = evaluation
        evaluation_methods = {
                'numerical': { 'couplings': 'nvalue', 'masses': 'nmass' },
                'analytical': { 'couplings': 'value', 'masses': 'mass' },
                'abbreviations': { 'couplings': 'name', 'masses': 'mass' }
                }
        self.coupling_values = evaluation_methods[evaluation]['couplings']
        self.mass_values = evaluation_methods[evaluation]['masses']
        self.zero = 0 if self.evaluation == 'numerical' else ''
        self.MSDR = MSDR

    def anyzero(self, *coups):
        """ Check if any of the vertices is numerically negligible
        i.e. whether the diagram is (numerically) zero """
        if self.evaluation in ['analytical', 'abbreviations']:
            return False
        return any([iszero(c) for c in coups])

    # 1L tadpoles
    @diagram(Next=1,Nint=1,Nvert=1)
    def OnePointA(self, **d):
        """ One-loop tadpole diagram
            * zero for everything but scalars
            * in the loop: $S=0,1/2,1$
        """
        if d['exttype'] != 'S':
            return
        fac = f"-1*({d['factor']})"
        m = d['masses'][0]
        c = d['couplings'][0]
        if d['inttype'] == 'F':
            return f"-1*{fac}*(({c['L']} + {c['R']})*({m})*A0({m}**2))"
        if d['inttype'] == 'V':
            return f"{fac}*({c})*({self.MSDR}*{m}**2-2*A0({m}**2))"
        if d['inttype'] in ['S', 'U']:
            fac = f'{fac}/2'
            fac = f'-1*{fac}' if d['inttype'] == 'U' else fac
            return f'+{fac}*({c})*A0({m}**2)'

    # 1L selfenergies
    @diagram(Next=2,Nint=1,Nvert=1)
    def TwoPointA(self, **d):
        """ One-loop selfenergy diagram with one four-point
        interaction.\n
         * internal: $S=0,1$
         * external: $S=0,1$
        """
        c = d['couplings'][0]
        m = d['masses'][0]
        fac = f"1/2*({d['factor']})"
        if d['derivative']:
            return self.zero

        if d['exttype'] == 'SS': # scalar selfenergy
            if d['inttype'] == 'S':
                return f'+({fac})*({c})*A0({m}**2)'
            if d['inttype'] == 'V':
                return f'-({fac})*({c})*4*(A0({m}**2)-{self.MSDR}*{m}**2/2)'

        if d['exttype'] == 'VV': # transverse part of vector boson selfenergy
            if d['inttype'] == 'S':
                return f'+({fac})*({c})*A0({m}**2)'
            if d['inttype'] == 'V':
                return f"-({fac})*((4*{c['1']}+{c['2']}+{c['3']})*A0({m}**2) - 2*{self.MSDR}*{m}**2*{c['1']})"

    @diagram(Next=2,Nint=2,Nvert=2)
    def TwoPointB(self, **d):
        """ One-loop selfenergy diagram with two three-point
        interactions as well as its derivative w.r.t the external
        momentum.\n
         * internal: all possible combinations of $S=0,1/2,1$
         * external: $S=0,1/2,(1$ not yet checked$)$"""
        m1,m2 = d['masses']
        c1,c2 = d['couplings']
        c2 = conj(c2)
        if d['inttype'] == 'FF' or d['exttype'] == 'FF':
            c1L, c1R, c2L, c2R = c1['L'], c1['R'], c2['L'], c2['R']
        s = d['momenta'][0]
        fac = f"1/2*({d['factor']})"
        if d['exttype'] == 'SS': # scalar selfenergy
            fac = f"4*{fac}" if d['inttype'] == 'VV' else fac
            fac = f"-1*{fac}" if d['inttype'] == 'UU' else fac

            if d['derivative']:  # derivative w.r.t s
                if d['inttype'] == 'SV':# if d['inttype'] in ['SV', 'VS']:
                    dF0 = f'-2*B0({s},{m1}**2,{m2}**2)-(2*{s} + 2*{m1}**2-{m2}**2)*dB0({s},{m1}**2,{m2}**2)'
                    return f'-2*{fac}*({c1})*({c2})*({dF0})'
                if d['inttype'] == 'VS':
                    return self.zero
                if d['inttype'] == 'FF':
                    dG0 = f'({s}-{m1}**2-{m2}**2)*dB0({s},{m1}**2,{m2}**2) + B0({s},{m1}**2,{m2}**2)'
                    return f'-({fac})*(({c1L}*{c2L} + {c1R}*{c2R})*({dG0})-2*({c1L}*{c2R} + {c1R}*{c2L})*({m1})*({m2})*dB0({s},{m1}**2,{m2}**2))'
                if d['inttype'] in ['SS', 'VV', 'UU']:
                    if d['inttype'] == 'UU':
                        c2 = conj(c2)
                    return f'-{fac}*({c1})*({c2})*dB0({s},{m1}**2,{m2}**2)'

            if d['inttype'] == 'SV': # if d['inttype'] in ['SV', 'VS']:
                F0 = f'A0({m1}**2)-2*A0({m2}**2)-(2*{s} + 2*{m1}**2-{m2}**2)*B0({s},{m1}**2,{m2}**2)'
                return f'-2*{fac}*({c1})*({c2})*({F0})'
            if d['inttype'] == 'VS':  # set to 0 to avoid double counting
                # F0 = f'A0({m2}**2)-2*A0({m1}**2)-(2*{s} + 2*{m2}**2-{m1}**2)*B0({s},{m2}**2,{m1}**2)'
                return self.zero # f'+2*{fac}*({c1})*({c2})*({F0})'
            if d['inttype'] == 'VV':
                return f'-{fac}*({c1})*({c2})*(B0({s},{m1}**2,{m2}**2)-{self.MSDR}/2)'
            if d['inttype'] in ['SS', 'UU']:
                if d['inttype'] == 'UU':
                    c2 = conj(c2)
                return f'-{fac}*({c1})*({c2})*B0({s},{m1}**2,{m2}**2)'
            if d['inttype'] == 'FF':
                G0 = f'(({s}-{m1}**2-{m2}**2)*B0({s},{m1}**2,{m2}**2) - A0({m1}**2) - A0({m2}**2))'
                return f'-({fac})*((({c1L})*({c2L}) + ({c1R})*({c2R}))*({G0}) - 2*(({c1L})*({c2R}) + ({c1R})*({c2L}))*({m1})*({m2})*B0(({s}),({m1})**2,({m2})**2))'

        if d['exttype'] == 'VV': # transverse part of vector selfenergy
            if d['derivative']: # derivative w.r.t. s
                dB0012 = f'dB00({s},{m1}**2,{m2}**2)'
                dB012 = f'dB0({s},{m1}**2,{m2}**2)'
                if d['inttype'] == 'SS':
                    return f'-4*{fac}*({c1})*({c2})*{dB0012}'
                if d['inttype'] == 'VV':
                    return f'-1*{fac}*({c1})*({c2})*(10*({dB0012}) + ({m2}**2 + {m1}**2 + 4*{s})*({dB012}) + 4*B0({s},{m1}**2,{m2}**2)+2/3*{self.MSDR})'
                if d['inttype'] == 'UU':
                    return f'{fac}*{c1}*{c2}*{dB0012}'
                if d['inttype'] == 'SV': # if d['inttype'] in ['SV', 'VS']:
                    return f'+2*({fac})*({c1})*({c2})*{dB012}'
                if d['inttype'] == 'VS':
                    return self.zero
                if d['inttype'] == 'FF':
                    db0 = f'dB0({s},{m1}**2,{m2}**2)'
                    b0 = f'B0({s},{m1}**2,{m2}**2)'
                    dH0 = f'4*dB00({s},{m1}**2,{m2}**2) + ({s} - {m1}**2 - {m2}**2)*{db0} + {b0}'
                    return f'{fac}*((({c1L})*({c2L}) + ({c1R})*({c2R}))*({dH0}) + 2*(({c1L})*({c2R}) + ({c1R})*({c2L}))*({m1})*({m2})*{db0})'

            B0012 = f'B00({s},{m1}**2,{m2}**2)'
            B012 = f'B0({s},{m1}**2,{m2}**2)'
            if d['inttype'] == 'SS':
                return f'-4*{fac}*({c1})*({c2})*{B0012}'
            if d['inttype'] == 'VV':
                return f'-1*{fac}*({c1})*({c2})*(10*{B0012} + ({m2}**2 + {m1}**2 + 4*{s})*{B012} + A0({m1}**2) + A0({m2}**2) - 2*{self.MSDR}*({m1}**2+{m2}**2-{s}/3))'
            if d['inttype'] == 'UU':
                return f'{fac}*{c1}*{c2}*{B0012}'
            if d['inttype'] in ['SV', 'VS']:
                return f'+({fac})*({c1})*({c2})*{B012}'
            # if d['inttype'] == 'VS':
            #     return self.zero
            if d['inttype'] == 'FF':
                b0 = f'B0({s},{m1}**2,{m2}**2)'
                H0 = f'4*B00({s},{m1}**2,{m2}**2)-A0({m1}**2)-A0({m2}**2) + ({s} - {m1}**2 - {m2}**2)*{b0}'
                return f'{fac}*((({c1L})*({c2L}) + ({c1R})*({c2R}))*({H0}) + 2*(({c1L})*({c2R}) + ({c1R})*({c2L}))*({m1})*({m2})*({b0}))'

        if d['exttype'] == 'FF': # fermion selfenergy
            if d['inttype'] not in ['FV', 'FS']:
                return 0
            if d['external'][0] != d['external'][1].anti():
                # external states are in the mass basis -> no mixing
                mfext = 0
            else:
                mfext = d['external'][0].get(self.mass_values)
            if d['derivative']:
                b0 = f'dB0({s},{m1}**2,{m2}**2)'
                b1 = f'dB1({s},{m1}**2,{m2}**2)'
            else:
                if d['inttype'] == 'FV':
                    b0 = f'(B0({s},{m1}**2,{m2}**2) - 1/2*{self.MSDR})'
                    b1 = f'(B1({s},{m1}**2,{m2}**2) + 1/2*{self.MSDR})'
                elif d['inttype'] == 'FS':
                    b0 = f'B0({s},{m1}**2,{m2}**2)'
                    b1 = f'B1({s},{m1}**2,{m2}**2)'

            SigSL = f'2*{m1}*({c1R})*({c2L})*{b0}'
            SigSR = f'2*{m1}*({c1L})*({c2R})*{b0}'
            SigVL = f'-2*({c1L})*({c2L})*{b1}'
            SigVR = f'-2*({c1R})*({c2R})*{b1}'
            if d['inttype'] == 'FV':
                SigSL = f'-4*({SigSL})'
                SigSR = f'-4*({SigSR})'
                SigVL = f'2*({SigVL})'
                SigVR = f'2*({SigVR})'
            return f'+({fac})*(({SigSL}+{SigSR})/2 + ({mfext})*({SigVL} + {SigVR})/2)'

        return

    @diagram(Next=2,Nint=2,Nvert=2)
    def TwoPointTA(self, **d):
        """ One-loop tadpole attached to a tree-level propagator, i.e.
        tadpole correction to a selfenergy.\n
         * internal: $S=0,1/2,1$
         * external: $S=0,1$ (1/2 not yet implemented)
        """
        m1,m2 = d['masses']
        c1,c2 = d['couplings']
        fac = f"1/2*({d['factor']})"

        if d['derivative'] or not d['inttype'].startswith('S'):
            return self.zero

        if d['exttype'] == 'SS': # scalar self-energy with tadpole insertion
            if d['inttype'] == 'SS':
                return f"+({fac})*({c1})*({c2})*A0({m2}**2)/({m1}**2)"
            if d['inttype'] == 'SF':
                c2L,c2R = c2['L'],c2['R']
                return f"-2*({fac})*({c1})*(({c2L})+({c2R}))*{m2}*A0({m2}**2)/({m1}**2)"
            if d['inttype'] == 'SV':
                return f"+2*({fac})*({c1})*({c2})*(({self.MSDR})*({m2}**2)-2*A0({m2}**2))/({m1}**2)"
            if d['inttype'] == 'SU':
                return f"-({fac})*({c1})*({c2})*A0({m2}**2)/({m1}**2)"

        if d['exttype'] == 'VV': # vector self-energy with tadpole insertion
            if d['inttype'] == 'SS':
                return f"+({fac})*({c1})*({c2})*A0({m2}**2)/({m1}**2)"
            if d['inttype'] == 'SF':
                c2L,c2R = c2['L'],c2['R']
                return f"-2*({fac})*({c1})*(({c2L})+({c2R}))*{m2}*A0({m2}**2)/({m1}**2)"
            if d['inttype'] == 'SV':
                return f"+2*({fac})*({c1})*({c2})*(({self.MSDR})*({m2}**2)-2*A0({m2}**2))/({m1}**2)"
            if d['inttype'] == 'SU':
                return f"-({fac})*({c1})*({c2})*A0({m2}**2)/({m1}**2)"

        if d['exttype'] == 'FF': # fermion selfenergy with tadpole insertion
            mS,mX = d['masses']
            cL, cR = d['couplings'][0]['L'], d['couplings'][0]['R']

            Stad = self.OnePointA(
                external = [d['internal'][0]],
                internal = [d['internal'][1]],
                coupling_objects = [d['coupling_objects'][1]],
                factor = d['factor'],
                momenta = []
                )

            return f'1/({mS})**2*({Stad})*({cL} + {cR})/2'

    # Three point functions
    @diagram(Next=3,Nint=0,Nvert=1)
    def ThreePointTree(self, **d):
        """ Tree-level S->SS diagram """
        try:
            return f"{d['couplings'][0]}"
        except IndexError:
            return ''

    @diagram(Next=3,Nint=2,Nvert=2)
    def ThreePointB(self, **d):
        """ One-loop correction to three-point functions with one
        quartic and one trilinear coupling.\n
         * internal: all possible combinations of $S=0,1/2,1$
         * external: only $S=1/2$"""
        if d['exttype'] != 'SSS':
            return
        fac = d['factor']
        c1,c2 = d['couplings']
        m1,m2 = d['masses']
        s = d['momenta'][0]
        if d['inttype'] == 'SS':
            return f'+({fac})*({c1})*({c2})*B0({s},{m1}**2,{m2}**2)/2'
        if d['inttype'] == 'VV':
            return f'+({fac})*({c1})*({c2})*(2*B0({s},{m1}**2,{m2}**2)-{self.MSDR})'

    @diagram(Next=3,Nint=3,Nvert=3)
    def ThreePointC(self, **d):
        """ One-loop correction to three-point functions with three
        trilinear couplings.\n
         * internal: all possible combinations of $S=0,1/2,1$
         * external: only $S=0$"""

        if d['exttype'] != 'SSS':
            return
        m1,m2,m3 = d['masses']
        fac = d['factor']
        c1, c2, c3 = d['couplings']
        p12,p22,p32 = d['momenta']
        if d['inttype'] in ['SSS', 'UUU', 'VVV']:
            fac = f'-1*{fac}' if d['inttype'] == 'UUU' else fac
            fac = f'-4*{fac}' if d['inttype'] == 'VVV' else fac
            return f'-1*{fac}*({c1})*({c2})*({c3})*C0({p12},{p32},{p22},{m1}**2,{m2}**2,{m3}**2)'
        if d['inttype'] == 'FFF':
            c1L,c1R = c1['L'],c1['R']
            c2L,c2R = c2['L'],c2['R']
            c3L,c3R = c3['L'],c3['R']
            return (
                    f'+({fac})* ('
                    f'2*B0({p32},{m2}**2, {m3}**2)* ({c1L}* ({c2L}* {c3R}* {m1} + {c2R}*{c3L}*{m2} + {c2R}*{c3R}*{m3})+ {c1R}*({c2R}*{c3L}*{m1} + {c2L}*{c3R}*{m2} + {c2L}*{c3L}*{m3}))'
                    f'+ {m1}*C0({p12}, {p32}, {p22}, {m1}**2, {m2}**2, {m3}**2)* (({c1R}*{c2R}*{c3L} + {c1L}*{c2L}*{c3R})* ({p12} + {p22} - {p32}) +2*{m2}*{m3}*({c1L}*{c2L}*{c3L} + {c1R}*{c2R}*{c3R}) +2*{m1}*({c1R}* ({c2R}*{c3L}*{m1} + {c2L}*{c3R}*{m2} + {c2L}*{c3L}*{m3}) + {c1L}*({c2L}*{c3R}*{m1} + {c2R}*{c3L}*{m2} + {c2R}*{c3R}*{m3})))'
                    f'+C1({p12}, {p32}, {p22}, {m1}**2, {m2}**2, {m3}**2)*(({p12}+{p22}-{p32})*(({c1R}*{c2R}*{c3L} + {c1L}*{c2L}*{c3R})*{m1} + ({c1L}*{c2R}*{c3L} + {c1R}*{c2L}*{c3R})*{m2}) +2*{p12}*({c1R}*{c3L}*({c2R}*{m1}+ {c2L}*{m3}) + {c1L}*{c3R}*({c2L}*{m1} + {c2R}*{m3})))'
                    f'+C2({p12}, {p32}, {p22}, {m1}**2, {m2}**2, {m3}**2)*(2*{p22}*({c1R}*{c2R}*{c3L}*{m1} + {c1L}*{c2L}*{c3R}*{m1} + {c1L}*{c2R}*{c3L}*{m2} + {c1R}*{c2L}*{c3R}*{m2})+ ({p12}+{p22}-{p32})*({c1R}*{c3L}*({c2R}*{m1} + {c2L}*{m3}) + {c1L}*{c3R}*({c2L}*{m1} + {c2R}*{m3})))'
                    f')'
                    )
        if d['inttype'] == 'SSV':
            return (
                    f'-1*({fac})*({c1})*({c2})*({c3})*(B0({p32}, {m2}**2, {m3}**2) - (({p12})-({p32})-({m1})**2)*C0({p12}, {p32}, {p22}, {m1}**2, {m2}**2, {m3}**2) + ({p12}-{p22}+{p32})*C1({p12}, {p32}, {p22}, {m1}**2, {m2}**2, {m3}**2) + ({p12}-{p22}-{p32})*C2({p12}, {p32}, {p22}, {m1}**2, {m2}**2, {m3}**2))'
                    )
        if d['inttype'] == 'SVS':
            return (
                    f'-1*({fac})*({c1})*({c2})*({c3})*(B0({p32}, {m2}**2, {m3}**2) - ({p22}-{p32}-{m1}**2)*C0({p22}, {p32}, {p12}, {m1}**2, {m3}**2, {m2}**2) - ({p12}-{p22}-{p32})*C1({p22}, {p32}, {p12}, {m1}**2, {m3}**2, {m2}**2) - ({p12}-{p22}+{p32})*C2({p22}, {p32}, {p12}, {m1}**2, {m3}**2, {m2}**2))'
                    )
        if d['inttype'] == 'VSS':
            return (
                    f'-1*({fac})*({c1})*({c2})*({c3})*(B0({p32}, {m2}**2, {m3}**2) -({p12}-{p22}+{p32}-{m1}**2)*C0({p32}, {p22}, {p12}, {m2}**2, {m3}**2, {m1}**2) - 2*({p12} -{p22})*C1({p32}, {p22}, {p12}, {m2}**2, {m3}**2, {m1}**2) -(3*{p12}+{p22}-{p32})*C2({p32}, {p22}, {p12}, {m2}**2, {m3}**2, {m1}**2))'
                    )
        if d['inttype'] == 'SVV':
            return (
                    f'+({fac})*({c1})*({c2})*({c3})*(2*B0({p32}, {m2}**2, {m3}**2) + ({p12}+{p22}-{p32}+2*{m1}**2)*C0({p12}, {p32}, {p22}, {m1}**2, {m2}**2, {m3}**2) - (3*{p12}+{p22}-{p32})*C1({p12}, {p32}, {p22}, {m1}**2, {m2}**2, {m3}**2) - ({p12}+3*{p22}-{p32})*C2({p12}, {p32}, {p22}, {m1}**2, {m2}**2, {m3}**2))/2'
                    )
        if d['inttype'] == 'VSV':
            return (
                    f'+({fac})*({c1})*({c2})*({c3})*(2*B0({p32}, {m2}**2, {m3}**2) - ({p12}+{p22}-{p32}-2*{m1}**2)*C0({p12}, {p22}, {p32}, {m2}**2, {m1}**2, {m3}**2) - (7*{p12}-{p22}+{p32})*C1({p12}, {p22}, {p32}, {m2}**2, {m1}**2, {m3}**2) - (3*{p12}-3*{p22}+5*{p32})*C2({p12}, {p22}, {p32}, {m2}**2, {m1}**2, {m3}**2))/2'
                    )
        if d['inttype'] == 'VVS':
            return (
                    f'+({fac})*({c1})*({c2})*({c3})*(2*B0({p32}, {m2}**2, {m3}**2) - ({p12}+{p22}-{p32}-2*{m1}**2)*C0({p22}, {p12}, {p32}, {m3}**2, {m1}**2, {m2}**2) + ({p12}-7*{p22}-{p32})*C1({p22}, {p12}, {p32}, {m3}**2, {m1}**2, {m2}**2) + (3*{p12}-3*{p22}-5*{p32})*C2({p22}, {p12}, {p32}, {m3}**2, {m1}**2, {m2}**2))/2'
                    )

    @diagram(Next=3,Nint=2,Nvert=2)
    def ThreePointTA(self, **d):
        """ One-loop tadpole attached to one of the external legs of a
        tree-level four point interaction.\n
         * internal: all possible combinations of $S=0,1/2,1$
         * external: only $S=0$"""

        if d['exttype'] != 'SSS':
            return

        m1, m2 = d['masses']
        c1, c2 = d['couplings']
        fac = f"1/2*({d['factor']})"

        if d['inttype'] == 'SS':
            return f"-({fac})*({c1})*({c2})*A0({m2}**2)/({m1}**2)"
        if d['inttype'] == 'SF':
            c2L, c2R = c2['L'], c2['R']
            return f"+2*({fac})*({c1})*(({c2L})+({c2R}))*({m2})*A0({m2}**2)/({m1}**2)"
        if d['inttype'] == 'SV':
            return f"-2*({fac})*({c1})*({c2})*(({self.MSDR})*({m2}**2)-2*A0({m2}**2))/({m1}**2)"
        if d['inttype'] == 'SU':
            return f"+({fac})*({c1})*({c2})*A0({m2}**2)/({m1}**2)"

    @diagram(Next=3,Nint=3,Nvert=3)
    def ThreePointWFRT(self, **d):
        """ External leg correction to the three-point function with a
        tadpole insertion.\n
         * internal: all possible combinations of $S=0,1/2,1$
         * external: only $S=0$"""
        if d['internal'][0].name == d['external'][-1].name: # diagonal WFR
            return self.zero
        SSs_coupling = d['couplings'][0]
        sS_selfenergyTA = self.TwoPointTA(
                external = [d['internal'][0], d['external'][-1]],
                internal = [d['internal'][1], d['internal'][2]],
                coupling_objects = [d['coupling_objects'][1], d['coupling_objects'][2]],
                factor = d['factor'],
                momenta = []
                )
        if not (SSs_coupling and sS_selfenergyTA):
            return self.zero
        mprop = d['masses'][0]
        return f'-1/({mprop}**2-({d["momenta"][1]}))*({SSs_coupling})*({sS_selfenergyTA})'

    @diagram(Next=3,Nint=2,Nvert=2)
    def ThreePointWFRA(self, **d):
        """ External leg correction to the three-point function with
        an A0-integral insertion.\n
         * internal: all possible combinations of $S=0,1$
         * external: only $S=0$"""

        if d['internal'][0].name == d['external'][-1].name: # diagonal WFR
            return self.zero
        SSs_coupling = d['couplings'][0]
        sS_selfenergyA = self.TwoPointA(
                external = [d['internal'][0], d['external'][-1]],
                internal = [d['internal'][1]],
                coupling_objects = [d['coupling_objects'][1]],
                factor = d['factor'],
                momenta = []
                )
        if not (SSs_coupling and sS_selfenergyA):
            return self.zero
        mprop = d['masses'][0]
        return f'-1/({mprop}**2-({d["momenta"][1]}))*({SSs_coupling})*({sS_selfenergyA})'

    @diagram(Next=3,Nint=3,Nvert=3)
    def ThreePointWFRB(self, **d):
        """ External leg correction to the three-point function with
        an B0-integral insertion.\n
         * internal: all possible combinations of $S=0,1/2,1$
         * external: only $S=0$"""

        diagonal = d['internal'][0].name == d['external'][-1].name
        SSs_coupling = d['couplings'][0]
        sS_selfenergyB = self.TwoPointB(
                external = [d['internal'][0], d['external'][-1]],
                internal = [d['internal'][1], d['internal'][2]],
                coupling_objects = [d['coupling_objects'][1], d['coupling_objects'][2]],
                factor = d['factor'],
                momenta = [d['momenta'][1], d['momenta'][1]],
                derivative = diagonal
                )
        if not (SSs_coupling and sS_selfenergyB):
            return self.zero
        if diagonal:
            return f'1/2*({SSs_coupling})*({sS_selfenergyB})'
        mprop = d['masses'][0]
        return f'-1/({mprop}**2-({d["momenta"][1]}))*({SSs_coupling})*({sS_selfenergyB})'
