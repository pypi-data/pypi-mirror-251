from __future__ import division
import cmath
import logging
import re

logger = logging.getLogger('anyBSM.loopfunctions')
# from functools import lru_cache
try:
    import pyCollier
    collier = True
except Exception as e:
    collier = False
    logger.error(str(e))
    logger.warning("Could not import collier. Evaluation with finite external momentum not possible!")

__doc__ = """ # AnyLoopFunction
A module to store all needed loop functions.\n
For $p^2=0$ we implement the results for the loop functions directly
(see below).
For finite external momentum we rely on
[COLLIER](https://collier.hepforge.org/index.html) [Denner, Dittmaier,
Hofer] via linked [pycollier](https://anybsm.gitlab.io/pycollier/pyCollier.html).
"""

global qren
qren = None
""" The renormalization scale $Q_{ren.}$ (not the squared one!) """

eps = 10**-5
""" When two masses are assumed to be equal """

epszero = 10**-8
""" When masses are assumed to vanish """

def get_UV_part(expr: str):
    """ Replaces all loop functions appearing in  `expr` by their UV-divergent part.

    Args:
        expr: expression to process.

    Returns:
        Expression with loop functions replaced by UV-divergent part.
    """
    repls = [
        (              r"A0\((.*?)\)",                   r"\1"), #          A0(m)_div = m
        (              r"B0\((.*?)\)",                    r"1"), #   B0(p2,m1,m2)_div = 0
        (             r"dB0\((.*?)\)",                    r"0"), #  dB0(p2,m1,m2)_div = 1
        (              r"B1\((.*?)\)",               r"(-1/2)"), #   B1(p2,m1,m2)_div = - 1/2
        (             r"dB1\((.*?)\)",                    r"0"), #  dB1(p2,m1,m2)_div = 0
        ( r"B00\((.*?),(.*?),(.*?)\)",  r"((\2+\3)/4 - \1/12)"), #  B00(p2,m1,m2)_div = (m1 + m2)/4 - p2/12
        (            r"dB00\((.*?)\)",              r"(-1/12)"), # dB00(p2,m1,m2)_div = - 1/12
        (              r"C0\((.*?)\)",                    r"0"), #        C0(...)_div = 0
        (              r"C1\((.*?)\)",                    r"0"), #        C1(...)_div = 0
        (              r"C2\((.*?)\)",                    r"0"), #        C2(...)_div = 0
        ]
    for repl in repls:
        expr = re.sub(repl[0], repl[1], expr)
    return expr

def set_renscale(q):
    """ sets the renormalization scale in pycollier as well as the
    globally used variable `qren`. Note that pycollier's
    set_renscale-function takes the squared value while ours does not."""
    global qren
    qren = q
    if collier:
        pyCollier.set_renscale(qren**2)

def set_delta(delta):
    """ sets the UV regulator in pycollier (delta = 0 by default)."""
    if collier:
        pyCollier.set_delta(delta)

def collerr(p2):
    """ Throws error message if a loop integral with $p^2\\neq0$ was
    issued while COLLIER is not installed/found"""
    if abs(p2) > eps:
        raise ModuleNotFoundError('Evaluation with finite external momentum requires pyCollier!')

def lnbar(x):
    """ $\\overline{\\log}x = \\log \\frac{x}{Q_{ren.}^2}$ """
    return cmath.log(x/qren**2)

# @lru_cache(maxsize=150)
def A0(x):
    """ $A_0(x) = x(1-\\overline{\\log}x$"""
    if abs(x) < epszero:
        return 0
    return x*(1-lnbar(x))

def B0_p0(x,y):
    """ $B_0(p^2=0;x,y)=\\frac{A_0(x)-A_0(y)}{x-y}$ """
    if abs(x) < epszero and abs(y) < epszero:
        return 0
    if abs(x-y)/abs(x+y) < eps:
        return -lnbar(x)
    return (A0(x)-A0(y))/(x-y)

# @lru_cache(maxsize=150)
def B0(p2,x,y):
    """ $B_0(p^2;x,y)$ wrapper for pycollier"""
    if collier and abs(p2) > eps:
        return (pyCollier.b0(p2, x, y))
    collerr(p2)
    return B0_p0(x,y)

def B0p_p0(x,y):
    """ $\\frac{\\partial}{\\partial x}B_0(0;x,y) = -\\frac{1}{x-y}\\left(\\overline{\\log}x + B_0(0;x,y) \\right) $"""
    if abs(x) < epszero:
        if abs(y) < epszero:
            return 0
        logger.error('B0p_p0(0,y) is IR divergent!')
    if abs(y)/abs(x) < epszero:
        return -1/x
    if abs(x-y)/abs(x+y) < eps:
        return -1/(2*x)
    return -(lnbar(x)+B0_p0(x,y))/(x-y)

# @lru_cache(maxsize=150)
def B1(p2,x,y):
    """ $B_1(p^2,x,y)$ wrapper for pycollier """
    return (pyCollier.b1(p2, x, y))

# @lru_cache(maxsize=150)
def dB1(p2,x,y):
    """ $\\dot{B}_1(p^2,x,y)$ wrapper for pycollier """
    return (pyCollier.db1(p2, x, y))

# @lru_cache(maxsize=150)
def B00(p2,x,y):
    """ $B_{00}(p^2,x,y)$ wrapper for pycollier """
    if collier and abs(p2) > eps:
        return (pyCollier.b00(p2, x, y))
    collerr(p2)
    return B00_p0(x,y)

def B00_p0(x,y):
    """ $B_{00}(p^2=0,x,y) = \\frac{1}{4} \\left(x B_0(0;x,y) + A_0(y) + \\frac{x+y}{2}\\right)$ """
    return x*B0_p0(x,y)/4 + A0(y)/4 + (x + y)/8

def dB0_p0(x,y):
    """ $\\frac{\\partial}{\\partial p^2} B_0(p^2;x,y)|_{p^2=0} = \\frac{x^2 + 2 A_0(x) y - y^2 - 2 x A_0(y)}{2 (x-y)^3}$"""
    [x,y] = sorted([abs(x),abs(y)])
    if abs(y) < epszero:
        return 0
    if abs(x-y)/abs(x+y) < eps:
        return 1/(6*x)
    return (x**2+2*A0(x)*y-y**2-2*x*A0(y))/(2*(x-y)**3)

# @lru_cache(maxsize=150)
def dB0(p2,x,y):
    """ $\\dot{B}_0(p^2,x,y)$ wrapper for pycollier """
    if collier and abs(p2) > eps:
        return (pyCollier.db0(p2, x, y))
    collerr(p2)
    return dB0_p0(x,y)

def dB00_p0(x,y):
    """ $\\frac{\\partial}{\\partial p^2} B_{00}(p^2;x,y)|_{p^2=0} =\
        \\frac{-5x^3 + 27x^2y - 27xy^2 + 5y^3 +\
        6(x-y)^3 \\overline{\\log}y + \
        6x^2*(x-3y)\\log\\frac{x}{y}}{72(x-y)^3}\
       \\frac{x^2 + 2 A_0(x) y - y^2 - 2 x A_0(y)}{2 (x-y)^3}$"""
    [x,y] = sorted([abs(x),abs(y)])
    if abs(y) < epszero:
        logger.error('dB00_p0(0,0) is IR divergent!')
        return 0
    if abs(x) < epszero:
        return -(5-6*lnbar(y))/72
    if abs(x-y)/abs(x+y) < eps:
        return lnbar(x)/12
    return (-5*x**3 + 27*x**2*y - 27*x*y**2 + 5*y**3 + 6*(x-y)**3*lnbar(y) + 6*x**2*(x-3*y)*cmath.log(x/y))/(72*(x-y)**3)

# @lru_cache(maxsize=150)
def dB00(p2,x,y):
    """ $\\dot{B}_{00}(p^2;x,y)$ wrapper for pycollier """
    if collier and abs(p2) > eps:
        return (pyCollier.db00(p2, x, y))
    collerr(p2)
    return dB00_p0(x,y)


def C0_p0(x,y,z):
    """ $$C_{0}(p^2=0;x,y,z) = \\frac{B_0(0;y,x)-B_0(0;z,x)}{y-z}$$"""
    if abs(y) < epszero and abs(z) < epszero:
        if abs(x) < epszero:
            return 0
        logger.error('C0_p0(x,0,0) is IR divergent!')
        return 0

    if abs(abs(y)-abs(z))/abs(abs(y)+abs(z)) < eps:
        return B0p_p0(z,x)
    return (B0_p0(y,x)-B0_p0(z,x))/(y-z)

# @lru_cache(maxsize=150)
def C0(p12,p22,p2p3,x,y,z):
    """ $C_{0}(p^2;x,y,z)$ wrapper for pycollier """
    if collier and abs(p12+p22+p2p3) > eps:
        return (pyCollier.c0(p12,p22,p2p3,x,y,z))
    collerr(p12+p22+p2p3)
    return C0_p0(x,y,z)


def C1_p0(x,y,z):
    """ $C_{1}(p^2=0;x,y,z)=0$ """
    return 0

# @lru_cache(maxsize=150)
def C1(p12,p22,p2p3,x,y,z):
    """ $C_{1}(p^2;x,y,z)$ wrapper for pycollier """
    if collier:
        return (pyCollier.c1(p12,p22,p2p3,x,y,z))
    collerr(p12+p22+p2p3)
    return C1_p0(x,y,z)

def C2_p0(x,y,z):
    """ $C_{2}(p^2=0;x,y,z)=0$ """
    return 0

# @lru_cache(maxsize=150)
def C2(p12,p22,p2p3,x,y,z):
    """ $C_{2}(p^2;x,y,z)$ wrapper for pycollier """
    if collier:
        return (pyCollier.c2(p12,p22,p2p3,x,y,z))
    collerr(p12+p22+p2p3)
    return C2_p0(x,y,z)
