import re
from sympy.printing.latex import LatexPrinter
from anyBSM.utils import fieldtypes

function_names = {
        'A0': 'A_0',
        'B0': 'B_0',
        'dB0': r'\dot{B}_0',
        'B00': 'B_{00}',
        'dB00': r'\dot{B}_{00}',
        'C0': 'C_0',
        'C1': 'C_1',
        'C2': 'C_2',
        'lnbar': r'\overline{\ln}',
        }

class anyBSMPrinter(LatexPrinter):
    """ Custom LaTeX printer: defines how certain sympy object are represented in LaTeX output """
    def _print_conjugate(self, expr, exp=None):
        tex = r"{{%s}^*}" % self._print(expr.args[0])

        if exp is not None:
            return r"%s^{%s}" % (tex, exp)
        else:
            return tex

    def _print_Function(self, expr, exp=None):
        func = expr.func.__name__
        if func in function_names.keys():
            args = ','.join([self._print(i) for i in expr.args])
            return f'{function_names[func]}({args})'
        return super()._print_Function(expr, exp=exp)

def latex(expr,**settings):
    """ Executor for custom LaTeX printer `anyBSMPrinter()` """
    return anyBSMPrinter(settings).doprint(expr)

def particle_name(particle):
    """ Tries to convert a particle name into valid LaTeX.
    Takes an `anyBSM.ufo.object_library.Particle()` or a string as input.
    If the input is already latex, it is returned without modification.
    """
    if type(particle) != str and particle.__class__.__name__ == 'Particle':
        texname = particle.texname
    else:
        texname = particle
    if '\\' in texname or '^' in texname or '_' in texname: # is most likely already tex
        return texname
    if len(texname) == 1:
        return texname
    if 'bar' in texname or '~' in texname:
        name = particle_name(texname.replace('bar','').replace('~',''))
        return f'\\tilde{{{name}}}'
    if particle.__class__.__name__ == 'Particle':
        if texname.endswith('p') or texname.endswith('+') and particle.charge > 0:
            name = particle_name(texname[:-1])
            return f'{{{name}}}^+'
        if texname.endswith('m') or texname.endswith('-') and particle.charge < 0:
            name = particle_name(texname[:-1])
            return f'{{{name}}}^-'
    texname = re.sub(r'^([a-zA-Z])(\d)$', r'\1_{\2}', texname)
    texname = re.sub(r'^([a-zA-Z])([A-Za-z])$', r'\1_{\2}', texname)
    return texname

def parameter_name(param):
    """ Same as `particle_name()` but for generic couplings and model parameters """
    texname = param
    if '\\' in texname or '^' in texname or '{' in texname: # is most likely already tex
        return texname
    texname = re.sub(r'GC_(\d+)', r'G_C^{\1}', texname)
    texname = re.sub(r'^([a-zA-Z])_(\d+)$', r'\1_{\2}', texname)
    texname = re.sub(r'^([a-zA-Z])([a-zA-Z])_(\d+)$', r'\1_{\2}^{\3}', texname)
    texname = re.sub(r'^(\w)(\d+)$', r'\1_{\2}', texname)
    return texname

def line(particle):
    """ Guess the propagator line of a `anyBSM.ufo.object_library.Particle()` based on its spin and charge """
    ftype = {-1 : 'ghost', 1: 'scalar', 2: 'fermion', 3: 'boson'}.get(particle.spin, None)
    if not ftype:
        return 'plain'
    if particle.charge != 0 and ftype in ['scalar', 'boson']:
        ftype = 'charged ' + ftype
    if particle.selfconjugate and ftype == 'fermion':
        ftype = 'majorana'
    if particle.pdg_code < 0 and ftype != 'ghost':
        ftype = 'anti ' + ftype
    return ftype

def texname(particle, generic=False, external=False):
    """ Either return particles TeX-name or the generic field type """
    if not generic or external:
        return particle_name(particle.texname)
    ftype = fieldtypes([particle])
    return ftype
