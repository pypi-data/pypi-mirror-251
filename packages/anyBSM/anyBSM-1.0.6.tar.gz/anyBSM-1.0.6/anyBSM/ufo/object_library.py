import re
import logging

def pythonform(obj):
    """ Returns a string representation of `obj`.
    If `obj` is a list/set/dict, it acts on all elements."""
    if type(obj) == str:
        return f"'{obj}'".replace('\\','\\\\')
    if type(obj).__base__.__name__ == "UFOBaseClass":
        return obj.__class__.__name__[0] + "." + repr(obj)
    if type(obj) == list:
        return str([pythonform(i) for i in obj]).replace("'","")
    if type(obj) == set:
        return str((pythonform(i) for i in obj)).replace("'","")
    if type(obj) == dict:
        return str({pythonform(i) : pythonform(j) for i,j in obj.items()}).replace("'","")
    return obj

class UFOError(Exception):
    """Exception raised if when inconsistencies are detected in the UFO model."""
    pass

class UFOBaseClass(object):
    """The class from which all FeynRules classes are derived."""

    require_args = []

    def __init__(self, *args, **options):
        assert len(self.require_args) == len(args)

        for i, name in enumerate(self.require_args):
            setattr(self, name, args[i])

        for (option, value) in options.items():
            setattr(self, option, value)

    def get(self, name):
        return getattr(self, name)

    def set(self, name, value):
        setattr(self, name, value)

    def get_all(self):
        """Return a dictionary containing all the information of the object"""
        return self.__dict__

    def dump(self):
        res = f'\n{repr(self)} = {self.__class__.__name__}(\n'.replace("'","")
        for k,obj in self.__dict__.items():
            res += f'    {k} = {pythonform(obj)},\n'
        res += ')\n'
        return res

    def __str__(self):
        return self.name

    def nice_string(self):
        """ return string with the full information """
        return '\n'.join(['%s \t: %s' % (name, value) for name, value in self.__dict__.items()])

    def __repr__(self):
        replacements = [
            ('+','__plus__'),
            ('-','__minus__'),
            ('@','__at__'),
            ('!','__exclam__'),
            ('?','__quest__'),
            ('*','__star__'),
            ('~','__tilde__')
            ]
        text = self.name
        for orig,sub in replacements:
            text = text.replace(orig,sub)
        return text

all_particles = {}
class Particle(UFOBaseClass):
    """A standard Particle"""

    require_args = [
            'pdg_code', 'name', 'antiname',
            'spin', 'color', 'mass', 'width',
            'texname', 'antitexname', 'charge'
            ]

    require_args_all = [
            'pdg_code', 'name', 'antiname',
            'spin', 'color', 'mass', 'nmass', 'width',
            'texname', 'antitexname','counterterm',
            'charge', 'line', 'propagating',
            'goldstone', 'propagator', 'OS'
            ]

    def __init__(self, pdg_code, name, antiname, spin, color, mass, width, texname,
                 antitexname, charge , line=None, propagating=True, counterterm=None,
                 goldstone=False, propagator=None, OS=False, **options):

        args = (pdg_code, name, antiname, spin, color, mass,
                width, texname,antitexname, float(charge))

        UFOBaseClass.__init__(self, *args,  **options)

        global all_particles
        if name in all_particles:
            logging.warning(f'Particle name convention for {name} not unique!')
        all_particles[name] = self

        self.propagating = propagating
        self.goldstone = goldstone

        self.selfconjugate = (name == antiname)
        if not line:
            self.line = self.find_line_type()
        else:
            self.line = line

        if hasattr(self.mass, 'value'):
            try:
                self.nmass = float(self.mass.value)
            except:
                pass

        if propagator:
            if isinstance(propagator, dict):
                self.propagator = propagator
            else:
                self.propagator = {0: propagator, 1: propagator}

    def find_line_type(self):
        """ find how we draw a line if not defined
        valid output: dashed/straight/wavy/curly/double/swavy/scurly
        """
        spin = self.spin
        color = self.color

        # use default
        if spin == 1:
            return 'dashed'
        elif spin == 2:
            if not self.selfconjugate:
                return 'straight'
            elif color == 1:
                return 'swavy'
            else:
                return 'scurly'
        elif spin == 3:
            if color == 1:
                return 'wavy'

            else:
                return 'curly'
        elif spin == 5:
            return 'double'
        elif spin == -1:
            return 'dotted'
        else:
            return 'dashed' # not supported yet

    def anti(self):
        global all_particles
        if self.selfconjugate:
            return self
            # raise Exception('%s has no anti particle.' % self.name)
        if self.antiname in all_particles:
            return all_particles[self.antiname]
        outdic = {}
        for k,v in self.__dict__.items():
            if k not in self.require_args_all:
                outdic[k] = -v
        if self.color in [1,8]:
            newcolor = self.color
        else:
            newcolor = -self.color

        return Particle(-self.pdg_code, self.antiname, self.name, self.spin, newcolor, self.mass, self.width,
                        self.antitexname, self.texname, -self.charge, self.line, self.propagating, self.goldstone, **outdic)

all_parameters = {}
class Parameter(UFOBaseClass):

    require_args = ['name', 'nature', 'type', 'value', 'texname']
    require_args_all = ['name', 'nature', 'type', 'value', 'nvalue', 'texname']

    def __init__(self, name, nature, type, value, texname, lhablock=None, lhacode=None, **options):

        args = (name,nature,type,value,texname)

        UFOBaseClass.__init__(self, *args)

        args = (name,nature,type,value,texname)

        global all_parameters
        if name in all_parameters:
            logging.warning(f'Parameter name convention for {name} not unique!')
        all_parameters[name] = self

        if (lhablock is None or lhacode is None) and nature == 'external':
            raise Exception('Need LHA information for external parameter "%s".' % name)
        self.lhablock = lhablock
        self.lhacode = lhacode

all_CTparameters = {}
class CTParameter(UFOBaseClass):

    require_args = ['name', 'type', 'value', 'texname']

    def __init__(self, name, type, value, texname):

        args = (name,type,value,texname)

        UFOBaseClass.__init__(self, *args)

        global all_CTparameters
        if name in all_CTparameters:
            logging.warning(f'CT-parameter name convention for {name} not unique!')
        all_CTparameters[name] = self

    def finite(self):
        try:
            return self.value[0]
        except KeyError:
            return 'ZERO'

    def pole(self, x):
        try:
            return self.value[-x]
        except KeyError:
            return 'ZERO'

all_vertices = {}
class Vertex(UFOBaseClass):

    require_args = ['name', 'particles', 'color', 'lorentz', 'couplings']

    def __init__(self, name, particles, color, lorentz, couplings, **opt):
        global all_vertices
        args = (name, particles, color, lorentz, couplings)
        UFOBaseClass.__init__(self, *args, **opt)
        args = (particles,color,lorentz,couplings)
        if name in all_vertices:
            logging.warning(f'Vertex name convention for {name} not unique!')
        all_vertices[name] = self

all_CTvertices = {}
class CTVertex(UFOBaseClass):

    require_args = ['name', 'particles', 'color', 'lorentz', 'couplings', 'type', 'loop_particles']

    def __init__(self, name, particles, color, lorentz, couplings, type, loop_particles, **opt):

        args = (name, particles, color, lorentz, couplings, type, loop_particles)

        UFOBaseClass.__init__(self, *args, **opt)

        args = (particles,color,lorentz,couplings, type, loop_particles)

        global all_CTvertices
        if name in all_vertices:
            logging.warning(f'Vertex-CT name convention for {name} not unique!')
        all_CTvertices[name] = self

all_couplings = {}
class Coupling(UFOBaseClass):

    require_args = ['name', 'value', 'order']

    require_args_all = ['name', 'value', 'nvalue', 'order', 'loop_particles', 'counterterm']

    def __init__(self, name, value, order, **opt):

        args = (name, value, order)
        UFOBaseClass.__init__(self, *args, **opt)
        global all_couplings
        if name in all_couplings:
            logging.warning(f'Coupling name convention for {name} not unique!')
        all_couplings[name] = self

    def value(self):
        return self.pole(0)

    def pole(self, x):
        """ the self.value attribute can be a dictionary directly specifying the Laurent serie using normal
        parameter or just a string which can possibly contain CTparameter defining the Laurent serie."""

        if isinstance(self.value,dict):
            if -x in self.value.keys():
                return self.value[-x]
            else:
                return 'ZERO'

        CTparam = None
        for param in all_CTparameters:
            pattern = re.compile(r"(?P<first>\A|\*|\+|\-|\()(?P<name>"+param.name+r")(?P<second>\Z|\*|\+|\-|\))")
            numberOfMatches = len(pattern.findall(self.value))
            if numberOfMatches == 1:
                if not CTparam:
                    CTparam = param
                else:
                    raise UFOError("UFO does not support yet more than one occurence of CTParameters in the couplings values.")
            elif numberOfMatches > 1:
                raise UFOError("UFO does not support yet more than one occurence of CTParameters in the couplings values.")

        if not CTparam:
            if x == 0:
                return self.value
            else:
                return 'ZERO'
        else:
            if CTparam.pole(x) == 'ZERO':
                return 'ZERO'
            else:
                def substitution(matchedObj):
                    return matchedObj.group('first')+"("+CTparam.pole(x)+")"+matchedObj.group('second')
                pattern = re.compile(r"(?P<first>\A|\*|\+|\-|\()(?P<name>"+CTparam.name+r")(?P<second>\Z|\*|\+|\-|\))")
                return pattern.sub(substitution,self.value)

all_lorentz = {}
class Lorentz(UFOBaseClass):

    require_args = ['name','spins','structure']

    def __init__(self, name, spins, structure='external', **opt):
        args = (name, spins, structure)
        UFOBaseClass.__init__(self, *args, **opt)

        global all_lorentz
        if name in all_lorentz:
            logging.warning(f'Lorentz name convention for {name} not unique!')
        all_lorentz[name] = self

all_orders = {}
class CouplingOrder(object):

    def __init__(self, name, expansion_order, hierarchy, perturbative_expansion = 0):
        global all_orders
        if name in all_orders:
            logging.warning(f'CouplingOrder name convention for {name} not unique!')
        all_orders[name] = self

        self.name = name
        self.expansion_order = expansion_order
        self.hierarchy = hierarchy
        self.perturbative_expansion = perturbative_expansion

all_decays = {}
class Decay(UFOBaseClass):
    require_args = ['particle','partial_widths']

    def __init__(self, particle, partial_widths, **opt):
        args = (particle, partial_widths)
        UFOBaseClass.__init__(self, *args, **opt)

        global all_decays
        if particle in all_decays:
            logging.warning(f'Decay particle convention for {particle} not unique!')
        all_decays[particle] = self

        # Add the information directly to the particle
        particle.partial_widths = partial_widths

all_form_factors = {}
class FormFactor(UFOBaseClass):
    require_args = ['name','type','value']

    def __init__(self, name, type, value, **opt):
        args = (name, type, value)
        UFOBaseClass.__init__(self, *args, **opt)

        global all_form_factors
        if name in all_form_factors:
            logging.warning(f'FormFactor name convention for {name} not unique!')
        all_form_factors[name] = self

all_propagators = {}
class Propagator(UFOBaseClass):

    require_args = ['name','numerator','denominator']

    def __init__(self, name, numerator, denominator=None, **opt):
        args = (name, numerator, denominator)
        UFOBaseClass.__init__(self, *args, **opt)

        global all_propagators
        if name in all_propagators:
            logging.warning(f'Propagator name convention for {name} not unique!')
        all_propagators[name] = self
