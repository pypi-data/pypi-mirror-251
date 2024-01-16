import cmath

def complexconjugate(z):
    return z.conjugate()

conjugate = complexconjugate

Abs = abs

def Re(z):
    return z.real
re = Re

def Im(z):
    return z.imag
im = Im

I = complex(0,1)

# New functions (trigonometric)

def sec(z):
    return 1./cmath.cos(z.real)

def asec(z):
    return cmath.acos(1./(z.real))

def csc(z):
    return 1./cmath.sin(z.real)

def acsc(z):
    return cmath.asin(1./(z.real))

def cot(z):
    return 1./cmath.tan(z.real)

# Heaviside theta function

def theta_function(x,y,z):
    return y if x else z

# Auxiliary functions for NLO
def cond(cond, exprTrue, exprFalse):
    return exprTrue if cond == 0.0 else exprFalse

def reglog(z):
    return 0.0 if z == 0.0 else cmath.log(z.real)
