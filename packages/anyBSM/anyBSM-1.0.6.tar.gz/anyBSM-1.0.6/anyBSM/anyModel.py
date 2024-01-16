from __future__ import division
import importlib
import logging
import sys
from tqdm.auto import tqdm
from os import path, mkdir, remove
from shutil import rmtree
import yaml
from glob import glob
from typing import Union
import re
import cmath # noqa: F401
from cmath import pi, sin, cos, tan, atan, asin, acos, sqrt, log # noqa: F401
from anyBSM.loopfunctions import lnbar, A0, B0, B00, dB0, dB00, B1, dB1, C0, C1, C2, eps, set_renscale # noqa: F401
from anyBSM.ufo.function_library import complexconjugate, conjugate, Abs, I, Re, Im # noqa: F401
import anyBSM.ufo.object_library as object_library
from anyBSM.utils import fieldtypes, query_yes_no, import_sympy, LHA, lazy_import
import anyBSM.config as config

sys.setrecursionlimit(100000) # required for models with very large analytic results

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

simple_coup = [
        r'^1$', # SSS, SSSS, SUU
        r'^Metric\(\d,\d\)$', # SSVV, SVV
        r'^P\(\d,\d\)$', # UUV
        ]

class anyModel:
    """UFO Model loader and more.
    This is the main-class which
      * loads the UFO model,
      * loads/defines renormalization schemes
      * loads/defines which particles/parameters belong to the SM particles/parameters
      * converts/resolves UFO parameter relations to/using sympy
      * ...

    Basic Usage
    ```python
    # import the main module and logging
    from anyBSM import anyModel # alternatively: from anyBSM import anyBSM
    import logging
    logging.getLogger('anyBSM').setLevel(logging.DEBUG)

    # initialize the built-in model for the SM in the on-shell renormalization scheme
    SM = anyModel('SM', scheme_name = 'OS', evaluation = 'analytical')

    SM.load_renormalization_scheme('MS') # switch to MS scheme

    SM.getvertex('h','h', 'h') # returns the UFO h-h-h vertex
    SM.getcoupling('Wp','Wpc','Z') # returns the UFO W-W-Z coupling along with the correct sign
    ```
    """

    modeldir: str
    """Absolute path to the UFO model to load"""

    scheme_name: Union[None, str]
    """ The renormalization scheme to load/create from/in the
    `schemes.yml`-file located in the models directory.
    If `scheme_info` is specified as well, `scheme_name` is newly
    created and added to the `schemes.yml`-file of the model (this
    is equivalent to initializing without `scheme_name` and
    executing `anyBSM.add_renormalization_scheme(scheme_name, scheme_info)` later).
    """

    scheme_info: dict
    """ Create a renormalization scheme """

    scheme_load: True
    """ Whether to automatically load a scheme (`True`=yes, default) upon initialization.
    When set to `False`, `anyBSM.load_renormalization_scheme(<scheme_name>)` needs to be invoked manually.
    This allows to use `anyBSM.setparameters()` before loading the scheme for the first time.
    If set to `True` the (default/given) renormalization scheme is loaded using the numerical parameters from the UFO model.
    In this case one can still set the parameters later.
    However, changing input parameters after loading the scheme is not covered by sanity checks of the numerical
    input parameters (unless `anyBSM.find_SM_particles()` and `anyBSM.find_SM_parameters()` are invoked manually)."""

    particles_only: list
    """ Consider only Feynman diagrams that contain particles given in
    this list (specified by their particle name).
    If empty, all diagrams are calculated. Alternatively fill
    `anyBSM.loop_particles` with
    `anyBSM.ufo.object_library.Particle`-objects after the anyBSM-object
    has been created.
    """

    evaluation: str
    """How the result should be represented:
     * `'abbreviations'`: all couplings are represented in terms
     of the UFO couplings (GC_1.name etc)
     * `'analytical'`: the full analytical expression for all
     couplings is used (GC_1.value etc.)
     * `'numerical'` (default): numerical values for all parameters are used
     and a number is returned. See `anyBSM.setparameters()`.
     """

    caching: int
    """Choose which results should be read/stored-to JSON cache files:
      * `2` (default): cache analytic results. Only compatible
      with `anyBSM.evaluation='abbreviations'`
      * `1`: only cache found diagram insertions but calculate
      diagrams from scratch.

    If `caching>1` and `anyBSM.evaluation` is not set to `'abbreviations'`,
    then anyBSM.anyProcess.anyProcess.process switches temporary to
    `'abbreviations'` to fill the cache and then automatically switches
    back to `anyBSM.evaluation` before returning/evaluating results.

    In case of numerical instabilities, it might be desired to run with `caching=1`."""

    progress: bool
    """Whether to show any progress bars (using tqdm).
    Default: `True`."""

    ask: bool
    """ Whether to ask any interactive questions (i.e. issue input
    prompts). Default: True. If set to False, all answers are
    considered to be "yes"."""

    quiet: bool
    """Whether to print anything to stdout. Note that this does
    only affect actual printing not logging. """

    parameters: Union[None, dict, str]
    """ Dictionary of parameter names/values (OR a path to some LHA file) passed to the first
    call of `anyBSM.setparameters()`. If empty, the default values from
    the UFO model are used.\n
    Examples:
      * `parameters = {'Mh1': 125.1, 'Mh2': 350, 'alphaH': 0.1}`
      * `parameters = '/home/user/mssm/slha.in'`"""

    module_dir = path.abspath(path.dirname(__file__))

    models_dir = config.get_config()['models_dir']
    built_in_models = {path.basename(path.dirname(p)): path.dirname(p) for p in sorted(glob(path.join(models_dir,'*','__init__.py')))}

    def __init__(self,
            modeldir: str,
            scheme_name: Union[None, str] = None,
            scheme_info: dict = {},
            scheme_load: bool = True,
            particles_only: list = [],
            evaluation: str = 'numerical',
            caching: int = 2,
            progress: bool = True,
            ask: bool = True,
            quiet: bool = False,
            parameters: Union[None, dict, str] = {}):
        """Initialize a given UFO model for the calculation of $\\kappa_\\lambda$.
        For a detailed description please consult the online documentation."""

        self.modeldir = self.built_in_models.get(modeldir, modeldir)
        if not path.isdir(self.modeldir):
            logger.error(f'Model directory "{self.modeldir}" not found!')
            raise NotADirectoryError(self.modeldir)

        self.cachedir = path.join(self.modeldir, 'cache')
        if not path.isdir(self.cachedir):
            mkdir(self.cachedir)

        self.name = path.basename(self.modeldir)
        sys.path.insert(0, self.modeldir)
        sys.path.insert(0, path.join(self.module_dir, 'ufo')) # ensure to use our UFO objects

        self.progress = progress
        self.quiet = quiet
        self.caching = caching
        self.ask = ask
        self.evaluation = evaluation
        self.parameters = {}
        self.particles_only = particles_only
        self.loop_particles = []

        self.warnSSSS = True
        """ Whether to warn about any quartic scalar coupling being too large """

        self.lorentz = {}
        self.particles = {}
        self.all_particles = {}
        self.couplings = {}
        self.all_parameters = {} # stores numerical value of all couplings/parameters/masses...
        self.symbols_values = {}
        self.texnames = {}
        self.vertices = {} # {'FFS': [V1,V2,...,], 'SSS': [...], ...]
        self.all_vertices = {} # {'V1': V1, ...}
        self.all_vertices_inv = {} # {'h1h1h1': V3, ...} (cache for anyBSM.getvertex() )
        if 'object_library' in sys.modules:  # reset UFO objects
            del sys.modules['object_library']
            importlib.reload(object_library)

        self.default_particle_names = {
                'Higgs-Boson': ['h','hh'],
                'W-Boson': ['W','Wp','W+'],
                'Z-Boson': ['Z'],
                'Photon': ['A'],
                'Top-Quark': ['t', 'u3']
                }
        """ These names are used by anyBSM.find_SM_particles() to
        search for the SM particles in the UFO model"""

        self.default_parameter_names = {
                'VEV': ['v', 'VEV', 'vev', 'vSM', 'vvSM', 'v_SM'],
                'alphaQEDinverse': ['alphaQEDinverse', 'aEWM1'],
                'alphaQCD': ['alphaQCD', 'aS'],
                'GFermi': ['GFermi', 'Gfermi', 'gFermi', 'gF', 'GF', 'Gf'],
                'Dalpha': ['Deltaalpha', 'dalpha', 'Dalpha', 'deltaalpha'],
                }
        """ These names are used by anyBSM.find_SM_parameters() to
        search for the SM parameters in the UFO model"""

        self.SM_particles = { p: None for p in self.default_particle_names.keys()}
        """ Dictionary with SM-like particles. Fill by issueing
        `anyBSM.find_SM_particles()`"""

        self.SM_parameters = { p: None for p in self.default_parameter_names.keys()}
        """ Dictionary with parameters specifying the SM Higgs sector. Fill by issueing
        `anyBSM.find_SM_parameters()`"""

        self.import_parameters()
        self.import_particles(particles_only)
        self.import_lorentz()
        self.import_couplings()
        self.import_vertices()
        self.evalcoups = self._build_evalcoups_func()

        if evaluation == 'numerical':
            self.setparameters(params=parameters)

        self.scheme = {}
        self.scheme_name = scheme_name
        if scheme_info:
            self.add_renormalization_scheme(scheme_name, scheme_info)
        elif scheme_load:
            self.load_renormalization_scheme(scheme_name)

        self.set_evaluation_mode(evaluation)

        self.treelevel = '0'
        """ Cache for the analytic tree-level value of lambda_hhh
        (used for taking derivatives in `anyBSM.lambdahhhCT()`)."""

        self.OSmomenta = True
        """ Whether to calculate all automatically generated mass CTs/selfenergies
        entering in `anyBSM.lambdahhhCT()` at $p^2=m_pole^2$ (`True`)
        or at $p^2=0$ (`False`)
        """

        self.dimensional_reduction = False
        """ Whether to use dimensional reduction rather than minimal substraction
        when applying generic results for Feynman diagrams """

    def _print(self, *args, **kwargs):
        """ Print or not to print """
        if not self.quiet:
            print(*args, **kwargs)

    def _eval(self, n, **kwargs):
        """ Evaluate `n` in the evaluation model `self.evaluation`
        If `self.evaluation` is set to 'numerical'`, `n` will be
        evaluated by using the pre-defined numerical values for all
        model parameters.
        """
        if self.evaluation == 'numerical':
            if not n:
                return 0
            if not self.parameters['SignSinThetaW'].value:
                self.getSignSinThetaW()
            if kwargs:
                paras = dict(self.all_parameters)
                paras.update(kwargs)
            else:
                paras = self.all_parameters
            try:
                return eval(str(n), globals(), paras)
            except Exception as e:
                printparas = {k:v for k,v in paras.items() if k in str(n)}
                raise Exception('EvaluationError', str(e), str(n), printparas) from e
        if not n:
            return '+0'
        return f"+{n}"

    def _import(self, module):
        if module in sys.modules:
            del sys.modules[module]
        return importlib.import_module(module, self.modeldir)

    def clear_cache(self):
        """ Removes all files from the model cache dir """
        for file in glob(path.join(self.cachedir, '*')):
            logger.info(f'Removing {file} from cache.')
            try:
                remove(file)
            except IsADirectoryError:
                rmtree(file)

    def set_evaluation_mode(self,mode):
        """ Sets the evaluation mode to `mode`
            * possible values: 'numerical', 'analytical' or 'abbreviations'.
        """
        allowed = ['numerical', 'analytical', 'abbreviations']
        if mode not in allowed:
            logger.error(f'Evaluation mode "{mode}" not supported (choose either of {allowed})!')
            return
        self.evaluation = mode
        if mode == 'analytical':
            self.sympify_parameters()

    def dump(self, directory: str) -> None:
        """ Dumps the loaded/modified UFO model to a given `directory`. The directory **must not** exist.

        Args:
            directory: directory to dump loaded/modified UFO model (absolute path)
        """
        if path.isdir(directory):
            logger.error(f'Directory {directory} already exists!')
            return
        mkdir(directory)
        header = {
                'particles'  : 'from __future__ import division\nfrom object_library import all_particles,Particle\nimport parameters as P',
                'couplings'  : 'from object_library import all_couplings,Coupling',
                'lorentz'    : 'from object_library import all_lorentz,Lorentz',
                'parameters' : 'from object_library import all_parameters,Parameter',
                'vertices'   : 'from object_library import all_vertices,Vertex\nimport particles as P\nimport couplings as C\nimport lorentz as L'
                }
        for k,v in header.items():
            with open(path.join(directory, f'{k}.py'), 'w') as pf:
                pf.write(v + '\n')
                if k in ['particles', 'lorentz']:
                    attr = 'all_' + k
                else:
                    attr = k
                dumped = []
                for entry in getattr(self, attr).values():
                    if type(entry) is list:
                        for entry2 in entry:
                            pf.write(entry2.dump())
                    else:

                        if entry in dumped:
                            continue
                        dumped.append(entry)
                        pf.write(entry.dump())

    def import_particles(self, particles_only: list = []) -> None:
        """ Import particles from the UFO model and arange them according to their lorentz representation.
        result: `self.particles['S']` contains all scalars of the
        model. Supported are 'S', 'F', 'V' and 'U' (ghosts).
        `self.all_particles` contains all particles.

        Args:
            particles_only: restrict import to this set of particle names.
        """
        particlesimport = self._import('particles')
        self.all_particles = particlesimport.all_particles
        self.loop_particles = []
        for p in self.all_particles.values():
            if p.anti() not in self.loop_particles:
                self.loop_particles.append(p)
        if particles_only:
            noparticles = [p for p in particles_only if p not in self.all_particles.keys()]
            if noparticles:
                logger.warn(f'Particle(s) {noparticles} not defined in model! (You need to provide the particles "name").')
            self.loop_particles = [p for p in self.loop_particles if p.name in particles_only]
            self._print(f'Consider only contributions from {self.loop_particles}')

        # field lists
        self.particles = {}
        self.particles['U'] = [p for p in self.all_particles.values() if p.spin == -1]
        self.particles['S'] = [p for p in self.all_particles.values() if p.spin == 1]
        self.particles['F'] = [p for p in self.all_particles.values() if p.spin == 2]
        self.particles['V'] = [p for p in self.all_particles.values() if p.spin == 3]

        # identify light/heavy particles by PDG
        self.light_SM_fields = [1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16]
        self.heavy_fields = [p.pdg_code for p in self.all_particles.values() if abs(p.pdg_code) not in self.light_SM_fields]

    def import_couplings(self) -> None:
        """ Import couplings from the UFO model """
        couplings = self._import('couplings')
        self.couplings = couplings.all_couplings
        self.couplings['zero'] = object_library.Coupling(name = 'zero', value = '0', nvalue = 0, order = {})

    def import_parameters(self) -> None:
        """ Import parameters from the UFO model and add our custom UFO parameters"""
        parameters = self._import('parameters')
        self.parameters = parameters.all_parameters

        """ Introduce additional parameters """
        # TODO: outsource these thing into a separate UFO file and import it here

        # renormalization scale
        if "Qren" not in self.parameters:
            self.parameters["Qren"] = object_library.Parameter(
                    name = "Qren",
                    nature = "external",
                    texname = "Q_{ren}",
                    type = "real",
                    value = 172.5,
                    lhablock = "SPheno",
                    lhacode = [33]
                    )

        # Fermi constant
        GF = [y for y in [self.parameters.get(x) for x in self.default_parameter_names['GFermi']] if y]
        if GF:
            self.SM_parameters['GFermi'] = GF[0]
        else:
            self.parameters["GFermi"] = self.SM_parameters['GFermi'] = object_library.Parameter(
                    name = "GFermi",
                    nature = 'external',
                    texname = 'G_{F}',
                    type = "real",
                    value = 1.1663787e-05,
                    lhablock = 'SMINPUTS',
                    lhacode = [2]
                    )

        # hadronic and leptonic contribution to photon polarization
        dalpha = [y for y in [self.parameters.get(x) for x in self.default_parameter_names['Dalpha']] if y]
        if dalpha:
            self.SM_parameters['Dalpha'] = dalpha[0]
        else:
            self.parameters["Dalpha"] = self.SM_parameters['Dalpha'] = object_library.Parameter(
                    name = "Dalpha",
                    nature = 'external',
                    texname = '\\Delta \\alpha',
                    type = "real",
                    value = 0.02766 + 0.031497687, # dalpha_had5 + dalpha_lep; taken from  from 2203.15710 Eq. 7
                    lhablock = 'NaN',
                    lhacode = []
                    )

        # sign of weak mixing angle
        if 'SignSinThetaW' not in self.parameters:
            self.parameters['SignSinThetaW'] = object_library.Parameter(
                    name = "SignSinThetaW",
                    nature = 'external',
                    texname = '\\text{sign}(\\sin \\theta_w)',
                    type = 'real',
                    value = None, # this value can only be set later (+1 or -1) after the SM-particles have been identified
                    lhablock = 'NaN',
                    lhacode = []
                    )

        self.internal_parameters = [ e for e in self.parameters.values() if e.nature == 'internal']
        self.external_parameters = [ e for e in self.parameters.values() if e.nature == 'external']

    def import_lorentz(self) -> None:
        """ Import Lorentz structures from the UFO model """
        lorentz = self._import('lorentz')
        self.all_lorentz = lorentz.all_lorentz
        lorentz_types = {
                'FFS': [1, 2, 2],
                'FFV': [2, 2, 3],
                'SSS': [1, 1, 1],
                'SSSS': [1, 1, 1, 1],
                'SVV': [1, 3, 3],
                'SSV': [1, 1, 3],
                'SSVV': [1, 1, 3, 3],
                'SUU': [-1, -1, 1],
                'VVV': [3, 3, 3],
                'VVVV': [3, 3, 3, 3],
                'UUV': [-1, -1, 3]}
        for lorentz_type, spins in lorentz_types.items():
            self.lorentz[lorentz_type] = [lor for lor in self.all_lorentz.values() if sorted(lor.spins) == spins]
            if not self.lorentz[lorentz_type]:
                logger.warning(f"""No lorentz structures of type {lorentz_type} found!
                        Tip: tools like FeynRules and SARAH by
                        default exlucde SSSS and SUU vertices in the
                        generation of UFO files.""")

    def import_vertices(self) -> None:
        """ Import vertices from the UFO model and check if there are any
        un-supported lorentz structures used."""
        vertices = self._import('vertices')
        self.all_vertices = vertices.all_vertices
        self.vertices = {}
        for k,lorentz in self.lorentz.items():
            self.vertices[k] = [v for v in self.all_vertices.values() if len(set(lorentz) & set(v.lorentz)) > 0]
            if not self.vertices[k]:
                logger.warning(f"""No vertices of type {k} found!
                        Tip: tools like FeynRules and SARAH by
                        default exlucde SSSS and SUU vertices in the
                        generation of UFO files.""")

        """ Make sure the couplings are defined according to 1703.09237 (A.1)-(A.7) and save them to v.coupling """
        zero = self.couplings['zero']
        for ctype,verts in self.vertices.items():
            for v in verts:
                if hasattr(v, 'coupling'):
                    continue
                if ctype in ['SSS', 'SSSS', 'SSVV', 'SVV', 'SUU', 'UUV']:
                    if any([re.match(s, v.lorentz[0].structure) for s in simple_coup]):
                        if len(v.lorentz) > 1:
                            if ctype == 'UUV' and len(v.couplings) == 1:
                                v.coupling = list(v.couplings.values())[0]
                                continue
                            logger.error(f'unexpected lorentz structures for vertex {v} ({v.particles})!')
                        try:
                            v.coupling = v.couplings[(0,0)]
                        except:
                            logger.error(f'unexpected lorentz structures for vertex {v} ({v.particles})!')
                            v.coupling = zero
                    else:
                        logger.error(f'unexpected lorentz structures for vertex {v} ({v.particles})!')
                        v.coupling = zero
                elif ctype in ['FFS', 'FFV']:
                    coup = {'L': zero, 'R': zero}
                    for rep, c in v.couplings.items():
                        # color = rep[0]
                        spin = rep[1]
                        structure = v.lorentz[spin].structure
                        if re.match(r"^(Gamma\(\d,\d,-\d\)\*)?ProjP\(-?\d,-?\d\)$", structure):
                            coup.update({'L': c})
                        elif re.match(r"^(Gamma\(\d,\d,-\d\)\*)?ProjM\(-?\d,-?\d\)$", structure):
                            coup.update({'R': c})
                        else:
                            logger.error(f'unexpected lorentz structure for vertex {v} ({v.particles})!')
                    v.coupling = coup
                elif ctype == 'SSV':
                    if len(v.lorentz) == 1 and\
                            v.lorentz[0].spins == [1, 1, 3] and\
                            v.lorentz[0].structure.replace(' ', '') == 'P(3,1)-P(3,2)':
                        v.coupling = v.couplings[(0,0)]
                    else:
                        logger.error(f'unexpected lorentz structure for vertex {v} ({v.particles})!')
                elif ctype == 'VVV':
                    if len(v.lorentz) == 1:
                        v.coupling = v.couplings[(0,0)]
                    else:
                        logger.error(f'unexpected lorentz structure for vertex {v} ({v.particles})!')
                    # TODO: this check is way too dump (idea: expand lorentz.structure at import using sympy (but that's a performance killer) )!
                    # v.lorentz[0].structure == '-Metric(2,3)*P(1,2) + Metric(2,3)*P(1,3) + Metric(1,3)*P(2,1) - Metric(1,3)*P(2,3) + Metric(1,2)*P(3,1) - Metric(1,2)*P(3,2)':
                elif ctype == 'VVVV':
                    coup = {'1': zero, '2': zero, '3': zero}
                    for rep,c in v.couplings.items():
                        # color = rep[0]
                        spin = rep[1]
                        structure = v.lorentz[spin].structure
                        if structure == 'Metric(1,2)*Metric(3,4)':
                            coup.update({'1': c})
                        elif structure == 'Metric(1,3)*Metric(2,4)':
                            coup.update({'2': c})
                        elif structure == 'Metric(1,4)*Metric(2,3)':
                            coup.update({'3': c})
                        else:
                            logger.error(f'unexpected lorentz structure for vertex {v} ({v.particles})!')
                    v.coupling = coup
                else:
                    logger.error(f'vertex {v} not compatible with anyBSM-convention. Please check your modelfile or run `anyBSM_import` to convert it!')

    def _build_evalcoups_func(self):
        """ Constructs a function to evaluate numerical values for couplings to avoid
        calling `eval` multiple times.
        The function is cached into a file `anyModel.cachedir` + `evalcoups.py`.

        Returns:
            evalcoups function which takes internal and external parameters as input and
            returns a dictionary containing numerical values for all couplings.
        """
        coupsfile = path.join(self.cachedir, 'evalcoups.py')
        if path.isfile(coupsfile):
            mod = lazy_import('evalcoups', coupsfile)
            return mod.evalcoups
        # define return evalcoups function
        # args for evalcoups function
        args = ','.join(self.parameters.keys())
        funcstr = 'import cmath\nfrom cmath import *\nfrom anyBSM.ufo.function_library import complexconjugate, conjugate, Abs, I\n\n'
        funcstr += f'def evalcoups({args}, **kwargs):\n'
        # defining string for evalcoups function body
        funcstr += '\n'.join(map(lambda x: f'    {x.name} = {x.value}', self.couplings.values()))
        # return dictionary for evalcoups function
        funcstr += f'\n    return {self.couplings}'
        with open(coupsfile, 'w') as f:
            f.write(funcstr)
        exec(funcstr, globals())
        return globals()['evalcoups']

    def setparameters(self, params: Union[dict, str] = {}) -> None:
        """ Populate numerical values for all internal/external parameters
        (anyBSM.ufo.object_library.Parameter). They are saved to
        `<parameter>.nvalue` and `<particle>.nmass`.

        Args:
            params: overwrite default values defined in the UFO model.
                Can be a dictionary or a path to a LHA spectrum file.\n
                Examples:
                * `somemodel.setparameters(params = {'Mh1': 125.1,'Mh2': 350, 'alphaH': 0.1})`
                * `somemodel.setparameters(params = '/home/user/mssm/slha.in')`"""
        if params is None:
            params = {}
        self.all_parameters = {}
        lha = None
        if type(params) is str:
            logger.info(f'Using parameter definitions from LHA file: {params}.')
            lha = LHA(params)
            params = {}
            for p in self.external_parameters:
                if p.lhablock != 'NaN':
                    p.value = lha.get(p.lhablock, p.lhacode)
                p.nvalue = self.all_parameters[p.name] = p.value
                params[p.name] = p.value
        else:
            logger.info('updating parameters: ' + ', '.join([f'{k}={v}' for k,v in params.items()]))
            for p in self.external_parameters:
                if p.name in params:
                    p.value = params[p.name]
                self.all_parameters[p.name] = p.value
                p.nvalue = eval(str(p.value), globals(), self.all_parameters)
            for p in set(params).difference(self.all_parameters):
                logger.warn(f'parameter "{p}" not found in UFO model. Ignoring it...')
        for p in self.internal_parameters:
            if p.name in params:
                p.value = params[p.name]
            try:
                self.all_parameters[p.name] = eval(str(p.value), globals(), self.all_parameters)
                p.nvalue = self.all_parameters[p.name]
            except Exception as e:
                raise Exception('InitializeParameter', f'{p.name} = eval({p.value}):', e)
        for key, val in self.evalcoups(**{k: v.nvalue for k, v in self.parameters.items()}).items():
            self.all_parameters[key] = val
            self.couplings[key].nvalue = val
        for p in self.all_particles.values():
            p.nmass = abs(eval(str(p.mass), globals(), self.all_parameters))
        set_renscale(self.parameters["Qren"].nvalue)

        if self.warnSSSS:
            self.checkpertubativeSSSS()

    def checkpertubativeSSSS(self):
        """ Check if any quartic scalar coupling $C_{S_1S_2S_3S_4}$ is larger than $8\\pi$.
        Note that this is not the same as calculating/demanding the smallest *eigenvalues* of the 2->2 scattering to be smaller than 1/2.
        Thus, this is not a consistent check for perturbative unitarity but rather to give a conservative warning if sth. went horrible wrong.
        To perform a rigorous check in the high-energy limit please use the eigSSSS() function provided in the `anyBSM.anyPerturbativeUnitarity` module.
        """
        if self.evaluation != 'numerical':
            return
        SSSScoups = [[v.particles, list(v.couplings.values())[0]] for v in self.vertices.get('SSSS', [])]
        tolarge = [c for c in SSSScoups if abs(c[1].nvalue) > 8*pi]
        if self.warnSSSS:
            for c in tolarge:
                logger.warning(fr'Coupling {c[0]} ({c[1].name}={c[1].nvalue} larger than 8\pi. Please check for perturbative unitarity!')
        return [c[1] for c in tolarge]

    def _fieldlist(self, *fieldlist):
        """ Take mixed list of field names/objects and return list of field objects """
        if len(fieldlist) == 1 and type(fieldlist[0]) is list: # legacy
            fieldlist = fieldlist[0]
        fields = []
        for f in fieldlist:
            if f in self.all_particles.keys():
                fields.append(self.all_particles[f])
            elif f in self.all_particles.values():
                fields.append(f)
            else:
                logger.error(f'unkown field: {f}')
        return fields

    def getvertex(self, *fieldlist, names: bool = False) -> object_library.Vertex:
        """ Find vertex for given list of fields.

        Args:
            fieldlist: list of field names or objects
            names: return list of field names rather than the
                vertex.

        Returns:
            Vertex or `None` if the vertex does not exists. Our convention
            assumes only one vertex to be present for each fieldlist.
        """
        fields = self._fieldlist(*fieldlist)
        vname = ''.join(sorted([f.name for f in fields]))
        types = fieldtypes(fields, sort=True)
        if vname in self.all_vertices_inv:
            vert = self.all_vertices_inv[vname]
        else:
            verts = self.vertices.get(types, [])
            vert = [v for v in verts if vname == ''.join(sorted([f.name for f in v.particles]))]
            if len(vert) > 1:
                logger.error(f'More than two tree-level vertices ({vert}) found for {fieldlist}')
                return
            self.all_vertices_inv[vname] = vert
        if not vert:
            return
        vert = vert[0]
        if names:
            vert = vert.name
        return vert

    def getvertexsign(self, *fieldlist) -> int:
        """ Determine the sign of a given vertex specified by a
        fieldlist: SSV and VVV couplings pick-up a sign depending
        on the permutation (momentum-flow) of the fields.

        Args:
            fieldlist: list of field names or objects

        Returns:
            Sign of vertex
        """
        fields = self._fieldlist(*fieldlist)
        vert = self.getvertex(fields)
        if not vert:
            return 0
        types = fieldtypes(fields, sort=True)
        if types == 'SSV':
            fields_model = [f.name for f in vert.particles if f.spin == 1]
            fields_vert = [f.name for f in fields if f.spin == 1]
            if fields_model == fields_vert:
                return -1
        elif types == 'VVV':
            fields_model = [f.name for f in vert.particles]
            fields_vert = [f.name for f in fields]
            perms_even = [fields_model[-i:] + fields_model[:-i] for i in range(len(fields_model))]
            if fields_vert not in perms_even:
                return -1
        return 1

    def getcoupling(self, *fieldlist) -> dict:
        """ Return the coupling(s) of a given vertex specified by a
        fieldlist. Takes into account field permutations.

        Args:
            fieldlist: list of field names or objects

        Returns:
            dictionary `{`'c': coupling, 'sign': sign of vertex`}`
        """
        fields = self._fieldlist(*fieldlist)
        vert = self.getvertex(fields)
        if not vert:
            return
        types = fieldtypes(fields, sort=True)
        if types == "VVVV":
            coupsin = vert.coupling # contains {'c1': GC_X, ...} of the UFO model
            # check permutations and shuffle c's
            fields_ufo = [f.name for f in vert.particles]
            fields_vert = [f.name for f in fields]

            extf1, extf2 = fields_vert[0], fields_vert[-1] # from our vertex, we can pick out which fields are external (they come in first and last position)
            posextf1 = fields_ufo.index(extf1)
            fields_ufo[posextf1] = 'done' # so that the next index search doesn't return the same as posextf1 if extf1 == extf2
            posextf2 = fields_ufo.index(extf2)# next we check at which position the external fields are in the vertex of the UFO file

            if abs(posextf1-posextf2) == 2: # either 1,3 or 2,4
                coupsout = {'1': coupsin['2'], '2': coupsin['1'], '3': coupsin['3']}
            elif [posextf1,posextf2] in [[0,3], [1,2], [2,1], [3,0]]:
                coupsout = {'1': coupsin['3'], '2': coupsin['1'], '3': coupsin['2']}
            else:
                coupsout = coupsin
            return coupsout
        if types in ["FFS", "FFV"]:
            return vert.coupling # {'L': GC_X, 'R': GC_Y}
        return {'c': vert.coupling, 'sign': self.getvertexsign(fields)}

    def getmass(self, particle: Union[str, object_library.Particle], power = 1) -> Union[str, float]:
        """ Get the mass of the `particle`.

        Args:
            particle: particle for which the mass should be returned
            power: exponentiate the mass

        Returns:
            analytical/numerical mass depending on `anyModel.evaluation`
        """
        attr = 'nmass' if self.evaluation == 'numerical' else 'mass'
        if particle in self.all_particles.values():
            mass = getattr(particle, attr)
        elif particle in self.all_particles.keys():
            mass = getattr(self.all_particles[particle], attr)
        else:
            logger.error(f'Particle "{particle}" not part of model "{self.name}"!')
            return
        if power != 1:
            if self.evaluation != 'numerical':
                return f'({mass})**({power})'
            return mass**power
        return mass

    def find_SM_particles(self, names: dict = {}, names2: dict = {}) -> None:
        """ Try to determine the SM-like particles (Higgs boson, top
        quark, ...) based on user-suggestions and/or numerical values
        of masses and/or PDG values. As starting point
        `anyBSM.default_particle_names` is used.

        Args:
            names: first dictionary of suggestions (updates default
                dictionary)
            names2: second dictionary of suggestions
                The suggestions are typically read from the `schemes.yml` of
                in the model directory when issuing
                anyBSM.load_renormalization_scheme().
        """
        self.default_particle_names.update(names)
        self.default_particle_names.update(names2)
        if not self.default_particle_names.get('Higgs-Boson', None):
            higgs_candidates = [p.name for p in self.particles['S'] if p.charge == 0 and p.color == 1 and not p.goldstone]
            self.default_particle_names['Higgs-Boson'] = higgs_candidates

        self.SM_particles['Higgs-Boson'] = self.find_particle('Higgs-Boson', 123, 127, 25, 'S', 1, 0)
        self.SM_particles['Z-Boson'] = self.find_particle('Z-Boson', 90, 92, 23, 'V', 1, 0)
        self.SM_particles['W-Boson'] = self.find_particle('W-Boson', 80, 81, 24, 'V', 1, 1)
        self.SM_particles['Photon'] = self.find_particle('Photon', 0, 0, 22, 'V', 1, 0)
        self.SM_particles['Top-Quark'] = self.find_particle('Top-Quark', 171, 174, 6, 'F', 3, 2/3)
        self.SM_particles['Bottom-Quark'] = self.find_particle('Bottom-Quark', 3, 5, 5, 'F', 3, -1/3)
        self.SM_particles['Charm-Quark'] = self.find_particle('Charm-Quark', 1, 2, 4, 'F', 3, 2/3)
        self.SM_particles['Strange-Quark'] = self.find_particle('Strange-Quark', .1, .2, 3, 'F', 3, -1/3)
        self.SM_particles['Up-Quark'] = self.find_particle('Up-Quark', .001, .005, 2, 'F', 3, 2/3)
        self.SM_particles['Down-Quark'] = self.find_particle('Down-Quark', .003, .005, 1, 'F', 3, -1/3)
        self.SM_particles['Tau-Lepton'] = self.find_particle('Tau-Lepton', 1.5, 2., 15, 'F', 1, -1)
        self.SM_particles['Muon-Lepton'] = self.find_particle('Muon-Lepton', 80e-3, 120e-3, 13, 'F', 1, -1)
        self.SM_particles['Electron-Lepton'] = self.find_particle('Electron-Lepton', 400e-6, 600e-6, 11, 'F', 1, -1)
        self.all_particles.update(self.SM_particles)
        self._print('found the following SM(-like) particles:')
        for k,v in self.SM_particles.items():
            if hasattr(v, 'nmass'):
                self._print('{} ({}): (Mass {} = {})'.format(k, v.name, v.mass, v.nmass))
            else:
                self._print('{} ({}): (Mass {})'.format(k, v.name, v.mass))
        self._print('')

        # now we can determine the sign of the weak mixing angle numerically
        if self.evaluation == 'numerically':
            self.getSignSinThetaW()

    def find_particle(self, name: str, min_mass: float, max_mass: float, pdg_code: int, ftype: str, color: int, charge: float) -> object_library.Particle:
        """ Search a particular particle based on a mass-range,
        PDG-code, field type, color and charge.

        Args:
            name: name of the particle to be searched
            min_mass: minimal mass of the searched particle
            max_mass: maximal mass of the searched particle
            pdg_code: PDG identifier of the searched particle
            ftype: particle type of the searched particle (e.g. S or F)
            color: color quantum number of the searched particle
            charge: electrical charge of the searched particle
        """
        found = False
        candidates = self.default_particle_names.get(name, [name])
        if type(candidates) is str:
            candidates = [candidates]
        # first try the suggested particles
        for c in candidates:
            found = True
            particle = self.all_particles.get(c, None)
            if not particle:
                continue
            logger.debug(f'found particle "{particle.name}" as candidate for the SM-like {name}.')
            if hasattr(particle, 'nmass') and (min_mass > particle.nmass or max_mass < particle.nmass):
                self._print(f'Particle "{particle.name}" outside expected mass range for SM-like {name} ({min_mass}GeV < m < {max_mass}GeV, m={particle.nmass}).')
                found = self.ask and query_yes_no(f"Do you want to use '{particle.name}' as the SM-like {name} (yes) or continue searching (no)?")
                found = found if self.ask else True
            if found and abs(particle.pdg_code) != pdg_code:
                self._print(f'Unusual PDG code ({particle.pdg_code}, {particle.name}) for particle "{name}" (expected: {pdg_code}).')
                found = self.ask and query_yes_no(f"still continue with this ({particle.name}) particle?")
                found = found if self.ask else True
            if found:
                return particle
        # particle not found by user-suggestions: search by attributes
        for particle in self.particles[ftype]:
            if abs(particle.color) != abs(color) or abs(particle.charge) != abs(charge):
                continue
            found = False
            if abs(particle.pdg_code) == pdg_code:
                logger.debug(f'found particle "{particle.name}" as candidate for SM-like {name} with expected PDG code ({pdg_code}).')
                found = True
            if hasattr(particle, 'nmass') and min_mass <= particle.nmass  <= max_mass:
                logger.debug(f'found particle "{particle.name}" as candidate for SM-like {name} with expected mass between {min_mass} and {max_mass}.')
                found = True
            if found:
                return particle
        # particle still not found. ask for more input
        while (not found) and self.ask:
            logger.error(f'found no suitable particle candidate for the SM-like {name}!')
            self.default_particle_names[name] = [input(f'Please enter the name for {name} manually:')]
            return self.find_particle(name,min_mass,max_mass,pdg_code,ftype,color,charge)

    def find_SM_parameters(self,names: dict = {}, names2: dict = {}) -> None:
        """ Same as anyBSM.find_SM_particles() but for the parameters
        of the UFO model """
        self.default_parameter_names.update(names)
        self.default_parameter_names.update(names2)
        self.SM_parameters['VEV'] = self.find_parameter('VEV', 240, 260)
        self.SM_parameters['alphaQEDinverse'] = self.find_parameter('alphaQEDinverse', 130, 140)
        self.SM_parameters['alphaQCD'] = self.find_parameter('alphaQCD', .1, .13)
        self._print('Found the following SM input parameters:')
        for k,v in self.SM_parameters.items():
            if v:
                self._print('{} ({}): {}'.format(k, v.name, v.value))
            else:
                self._print(f'{k}: not found!')
        self._print('')

    def find_parameter(self, name: str, min_val: float, max_val: float) -> object_library.Parameter:
        """ Search for an SM parameter in the UFO model and check if
        its value is within some expected range.

        Args:
            name: name of the searched parameter
            min_val: minimal value
            max_val: maximal value

        Returns:
            searched parameter
        """
        candidates = self.default_parameter_names.get(name, [name])
        if type(candidates) is not list:
            candidates = [candidates]
        found = [p for p in self.parameters.values() if p.name in candidates]
        if len(found) == 1:
            para = found[0]
            if hasattr(para, 'nvalue') and (para.nvalue.real < min_val or para.nvalue.real > max_val):
                logger.error(f'Found parameter "{para.name}" as candidate for "{name}" but its value is outside expeceted range ({min_val},{max_val})')
                found = self.ask and query_yes_no(f"Do you want to use '{para.name}' as the {name} (yes) or enter it manually (no)?")
                found = found if self.ask else True
                if found:
                    return para
                else:
                    self.default_parameter_names[name] = [input(f'Enter name for parameter {name}: ')]
                    return self.find_parameter(name, min_val, max_val)
            return para
        elif len(found) > 1:
            logger.error(f'Found multiple candidates for parameter {name}: {found}.')
        else:
            logger.error(f'Parameter {name} not found.')
        self.default_parameter_names[name] = input(f'Enter name for parameter {name} defined in the model: ')
        return self.find_parameter(name, min_val, max_val)

    def getSignSinThetaW(self) -> int:
        """ Determine sign of weak mixing angle.
        For this, the sign of the coupling between the top quark and the Z-boson is considered.
        Alternatively, one may set a custom UFO parameter "SignSinThetaW" in the UFO models parameters.py.
        If the function sucessully determined the sign, the value is also updated into this UFO parameter.

        Returns:
            sign of weak mixing angle
        """
        if self.parameters['SignSinThetaW'].value is not None:
            return self.parameters['SignSinThetaW'].value
        Z = self.SM_particles['Z-Boson']
        A = self.SM_particles['Photon']
        t = self.SM_particles['Top-Quark']
        if not all((Z,A,t)):
            logger.error("Top quark, Z-boson or photon not known: did you call `load_renormalization_scheme` or `find_SM_particles`?")
            return 'SignSinThetaW'
        if self.evaluation != 'numerical':
            return 'SignSinThetaW'
        try:
            Ztt_coup = self.getvertex(Z,t,t.anti()).coupling['R']
            Att_coup = self.getvertex(A,t,t.anti()).coupling['R']
        except Exception as e:
            logger.exception(f"{Z,A}tt couplings could not be extracted: {e}")
            return 'SignSinThetaW'

        coupr = Ztt_coup.nvalue*Att_coup.nvalue
        sign = -1*coupr/abs(coupr)

        if abs(sign - 1) == 0:
            self.parameters['SignSinThetaW'].value = 1
        elif abs(sign + 1) == 0:
            self.parameters['SignSinThetaW'].value = -1
        else:
            logger.error(f'Error! Right-handed FFV coupling has unexpected form {coupr}')
            return 'SignSinThetaW'
        self.all_parameters['SignSinThetaW'] = self.parameters['SignSinThetaW'].value
        self.parameters['SignSinThetaW'].nvalue = self.all_parameters['SignSinThetaW']
        return self.parameters['SignSinThetaW'].value

    def load_renormalization_scheme(self, scheme_name: Union[None, str] = None) -> dict:
        """ Load a renormalization scheme from the model directories
        `scheme.yml`-file. The file should look like:
        ```yaml
        # default names for SM fields and parameters
        SM_names:
          Top-Quark: u3 # "u3" is the particle name defined in the UFO model
          W-Boson: Wp
          Z-Boson: Z
          Higgs-Boson: h1
          VEV: vvSM

        renormalization_schemes:
          OS1:
            mass_counterterms:
              h1: OS # mass counterterms can be set to OS/MS
              h2: OS
            VEV_counterterm: OS # set to OS/MS
          OS2:
            SM_names:  # overwrite default "SM_names"
              Higgs-Boson: h2
            mass_counterterms:
              h1: OS
              h2: OS
            VEV_counterterm: OS
        ```
        and can be loaded by e.g.
        `somemodel.load_renormalization_scheme('OS1')`.

        Args:
            scheme_name: name of the scheme to be loaded

        Returns:
            dictionary specificing scheme
        """
        schemefile = path.join(self.modeldir, 'schemes.yml')
        if not path.isfile(schemefile):
            logger.warn('No pre-defined renormalization schemes found.')
            if scheme_name:
                self.add_renormalization_scheme(scheme_name)
            return
        with open(schemefile, 'r') as f:
            schemes = yaml.load(f, Loader=yaml.FullLoader)
        if 'SM_names' not in schemes:
            schemes['SM_names'] = {}

        if 'renormalization_schemes' not in schemes:
            logger.error(f'No schemes defined in {schemefile}!')
            return

        scheme_name = schemes.get('default_scheme', None) if not scheme_name else scheme_name
        if not scheme_name:
            logger.warn('No default renormalization scheme defined in schemes.yml!')
            return

        if scheme_name not in schemes['renormalization_schemes']:
            logger.error(f'Scheme with name "{scheme_name}" not found in {schemefile}!')
            return self.add_renormalization_scheme(scheme_name)
        scheme = schemes['renormalization_schemes'][scheme_name]
        if 'SM_names' not in scheme:
            scheme['SM_names'] = {}

        self.find_SM_particles(schemes['SM_names'], scheme['SM_names'])
        self.find_SM_parameters(schemes['SM_names'], scheme['SM_names'])
        if 'mass_counterterms' not in scheme:
            scheme['mass_counterterms'] = []
            logger.error(f'No "mass_counterterms" defined for scheme "{scheme_name}". Assuming all masses MSbar.')
        if 'VEV_counterterm' not in scheme:
            scheme['VEV_counterterm'] = 'MS'
            logger.error(f'No "VEV_counterterm" defined for scheme "{scheme_name}". Assuming MSbar electro-weak sector.')
        self.scheme = scheme
        self.scheme_name = scheme_name
        self.dimensional_reduction = schemes.get('dimensional_reduction', False)
        if not schemes.get('SM_names', None):
            schemes['SM_names'] = {k: v.name for k,v in self.SM_particles.items()}
            schemes['SM_names'].update({k: v.name for k,v in self.SM_parameters.items()})
            with open(schemefile, 'w') as f:
                schemes = yaml.dump(schemes, f)
        return self.scheme

    def add_renormalization_scheme(self, scheme_name: str, scheme_info: dict = {}) -> dict:
        """ Add a renomalization scheme with name `scheme_name` to the
        `schemes.yml` in the model directory. The dictionary
        `scheme_info` must be conform with the scheme specifications
        i.e. at least contain a dictionary `mass_counterterms: {'field1':
            'OS/MS', ...}` and a variable `VEV_counterterm: 'OS/MS'`.
        If it was successful, the scheme is automatically loaded.

        Args:
            scheme_name: name of the new scheme
            scheme_info: scheme specification

        Returns:
            added renormalization scheme
        """
        schemefile = path.join(self.modeldir, 'schemes.yml')
        if scheme_info != {}:
            if 'name' not in scheme_info or \
                    'mass_counterterms' not in scheme_info or \
                    'VEV_counterterm' not in scheme_info:
                logger.error(f'could not generate scheme "{scheme_name}": not all information provided (check built-in models for examples).')
                return
            interactive = False
        else:
            self._print(f'interactively generating new renormalization scheme "{scheme_name}"')
            if not self.ask:
                logger.error('interactive mode disabled')
                return
            interactive = True
        schemes = {}
        if path.isfile(schemefile):
            with open(schemefile, 'r') as f:
                schemes = yaml.load(f, Loader=yaml.FullLoader)
        if 'renormalization_schemes' not in schemes:
            schemes['renormalization_schemes'] = {}
        if 'SM_names' not in schemes:
            schemes['SM_names'] = {}
        if scheme_name in schemes['renormalization_schemes']:
            logger.error(f'scheme with name "{scheme_name}" already exists.')
            if self.ask and not query_yes_no('Overwrite? '):
                return
            else:
                logger.error('overwriting...')
        if interactive:
            scheme_info['SM_names'] = {
                    'Higgs-Boson': input('Enter name of SM-like Higgs boson: ')
                    }
            scheme_info['mass_counterterms'] = {}
            higgs_candidates = [p.name for p in self.particles['S'] if p.charge == 0 and p.color == 1 and not p.goldstone]
            for candidate in higgs_candidates:
                scheme_info['mass_counterterms'][candidate] = 'OS' if query_yes_no(f'do you want to renormalize the mass of the scalar particle "{candidate}" on-shell?') else 'MS'
            scheme_info['VEV_counterterm'] = 'OS' if query_yes_no('shall the SM VEV be renormalized on-shell (via MW, MZ, alphaQEDinverse)?') else 'MS'

        if scheme_info['VEV_counterterm'] == 'OS':
            self.find_SM_parameters(schemes.get('SM_names',{}), scheme_info.get('SM_names', {}))
        schemes['renormalization_schemes'][scheme_name] = scheme_info
        with open(schemefile, 'w') as f:
            yaml.dump(schemes, f)

        return self.load_renormalization_scheme(scheme_name)

    def list_renormalization_schemes(self) -> dict:
        """ Reads the models `scheme,yml` and lists all available schemes
        Returns:
            dictionary with all schemes
        """
        schemefile = path.join(self.modeldir, 'schemes.yml')
        if not path.isfile(schemefile):
            return dict()
        with open(schemefile, 'r') as f:
            schemes = yaml.load(f, Loader=yaml.FullLoader)
        return schemes.get('renormalization_schemes', {})

    def sympify_parameters(self) -> None:
        """ convert the values of parameters in the UFO model to sympy
        expressions """
        if hasattr(self, 'symbols'):
            return
        # import here to avoid sympy import during numerical runs
        from anyBSM.latex.printer import parameter_name
        from anyBSM.latex.printer import anyBSMPrinter

        def latex(expr, **settings):
            sett = {'symbol_names': self.texnames}
            sett.update(settings)
            return anyBSMPrinter(sett).doprint(expr)
        sp = import_sympy()
        sp.init_printing(latex_printer=latex)
        self.symbols = {}
        self.texnames = {}
        for p,v in self.parameters.items():
            real = v.type.lower() == 'real'
            positive = (hasattr(v,'positive') and v.positive) or (real and type(v.value) is float and v.value > 0)
            self.symbols[p] = sp.Symbol(p, real=real, positive=positive)
            self.texnames[self.symbols[p]] = parameter_name(v.texname)
        for c in self.couplings.keys():
            if c in self.symbols:
                logger.error('LaTeX symbol for coupling "{c}" not unique.')
            self.symbols[c] = sp.Symbol(c)
            self.texnames[self.symbols[c]] = parameter_name(c)
        for i,p in enumerate(['PEXT12','PEXT22','PEXT32']):
            self.symbols[p] = sp.Symbol(p, real=True)
            self.texnames[self.symbols[p]] = f'p_{i+1}^2'
        self.symbols['complexconjugate'] = sp.conjugate
        self.symbols['conjugate'] = sp.conjugate
        x,y = sp.symbols('x y')
        self.symbols['complex'] = sp.Lambda((x,y), x+sp.I*y)

    def sympify(self, expr: str, simplify: bool = False, rational: bool = True):
        """ Use sympy.simpify() to convert `expr` to sympy expression.
        Symbols will be associated with the UFO symbols created by `anyModel.sympify_parameters()`.

        Args:
            expr: expression to be converted to sympy expression
            simplify: whether to simplify the result
            ration: whether to convert floats to rationals

        Returns:
            sympy expression
        """
        self.sympify_parameters()
        sp = import_sympy()
        sp_expr = sp.sympify(expr.replace('cmath.', ''), locals=self.symbols, rational= rational)
        if simplify:
            sp_expr = sp.simplify(sp_expr)
        return sp_expr

    def SolveDependencies(self, expression, simplify: bool = False, exclude: list = [], additional: dict = {}):
        """ Replace all internal parameters in `expression` with external ones.

        Args:
            expression: is supposed to be a string/sympy expression while a sympy object is returned.
            simplify: whether to simplify the result
            exclude: list of parameter names/strings which should not be replaced
            additional: dictionary with additional dependencies to
                apply (keys are substituted with values)

        Returns:
            `expression` with all internal parameter replaced by external ones.
        """
        sp = import_sympy()
        self.sympify_parameters()

        expr = expression
        if type(expr) is str:
            expr = sp.sympify(expr.replace('cmath.',''), locals=self.symbols, rational=True)

        # prepare replacement list
        exclude_symbols = []
        for p in self.parameters.values():
            if p.nature != "internal":
                # do not replace input parameters
                continue
            name = self.symbols.get(p.name, sp.Symbol(p.name))
            if name in exclude or p.name in exclude or p in exclude:
                exclude_symbols.append(p.name)
                continue
            if p.name not in self.symbols_values:
                try:
                    self.symbols_values[p.name] = sp.sympify(str(p.value).replace('cmath.', ''), locals=self.symbols, rational=True)
                except Exception as e:
                    logger.error(f'Failed to sympify parameter "{p.name}". Error was: {e}')
                    continue
        exclude_symbols = exclude_symbols + exclude
        replacements = dict(additional)
        replacements.update({self.symbols[p]: self.symbols_values[p] for p in self.symbols_values if p not in exclude_symbols})

        # replace all internal parameters in terms of external parameters
        i = 0
        old = expr
        new = expr
        first = True
        bar = tqdm(
                desc='Resolving parameter dependencies (write interals in terms of external parameters)',
                leave = False,
                disable = not self.progress)
        while old != new or first:
            bar.update(1)
            first = False
            old = new
            new = new.xreplace(replacements)
            i += 1
            if i > 99:
                logger.error('Cannot resolve dependency cycle for internal parameters')
                return new
        bar.close()
        if simplify:
            new = new.simplify()
        return new

    def Derivative(self, expression, symbol, simplify: bool = False, real: bool = True, dependencies: bool = True):
        """ Perform derivative of `expression` w.r.t. `symbol`.

        All input is sympified automatically taking into account the
        definitions obtained with `anyBSM.sympify_parameters()`.

        Args:
            expression: the expression to consider (string or sympy type)
            symbol: the symbol to take the derivative (string or sympy type)
            simplify: whether to simplify result
            real: whether to assume `symbol` to be real-valued
            dependencies: whether to take into
                account all parameter dependencies defined in the model (i.e.
                expresses all internal- through external parameters before
                taking the derivative if `symbol` is not found in `expression`):

        Returns:
            derivative
        """
        sp = import_sympy()
        self.sympify_parameters()
        # sympify `symbol`
        if symbol not in self.symbols:
            sym = sp.Symbol(symbol, real=real)
            self.symbols[symbol] = sym
        else:
            sym  = self.symbols[symbol]
        expr = expression
        if dependencies:
            expr = self.SolveDependencies(expr, simplify = simplify, exclude = [symbol])
        if type(expr) is str:
            expr = sp.sympify(expr, locals=self.symbols, rational=True)

        if simplify and not self.evaluation == 'numerical':
            expr = sp.simplify(expr)
        res = sp.Derivative(expr, sym, evaluate=True).doit()
        if simplify and not self.evaluation == 'numerical':
            res = sp.simplify(res)
        return res
