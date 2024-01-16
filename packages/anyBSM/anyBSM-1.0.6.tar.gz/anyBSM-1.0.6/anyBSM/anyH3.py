from __future__ import division
import logging
from tqdm.auto import tqdm
from os import path
import json
from collections import ChainMap
from hashlib import md5
from typing import Union
import cmath # noqa: F401
from cmath import pi, sin, cos, tan, atan, sqrt, log # noqa: F401
from anyBSM.loopfunctions import lnbar, A0, B0, B00, dB0, dB00, B1, dB1, C0, C1, C2, eps, set_renscale # noqa: F401
from anyBSM.ufo.function_library import complexconjugate, conjugate, Abs, I, Re, Im # noqa: F401
from anyBSM.anyProcess import anyProcess

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__doc__ = """
<div class="mermaid">
flowchart RL
    subgraph classes
    anyModel --> anyProcess --> anyH3;
    end
    subgraph methods
    anyH3 --> lambdahhhCT --> lambdahhh
    end
</div>
"""

class anyH3(anyProcess):
    r""" Calculation of the trilinear Higgs self coupling in OS/$\MS$/user-defined renormalization schemes.

    This class inherits from `anyBSM.anyProcess` which itself inherits from `anyBSM.anyModel`.
    For more information on how to initialize this class, see the documentation of the mother-class `anyBSM.anyModel.anyModel.__init__`  or consult the online documentation.
    The class `anyBSM.anyH3` implements two methods:
      * `anyBSM.anyH3.anyH3.lambdahhh()`: actual computation of the full one-loop corrected trilinear self-coupling (including the renormalization-specific contributions)
      * `anyBSM.anyH3.anyH3.lambdahhhCT()`: automatic caclulation of all renormalization-specific contributions

    It is assumed that a proper renormalization scheme has already been loaded and all SM-like particles/parameters are correctly identified.
    To ensure this `anyBSM.anyModel.anyModel.load_renormalization_scheme()` should be issued beforehand (see example below).

    Example
    ```python
    from anyBSM import anyH3
    SM = anyH3('SM')
    SM.load_renormalization_scheme('OS')
    lam = SM.lambdahhh()
    lamLO = lam[0]
    lamNLO = sum(lam).real
    lamNLO/lamLO
    ```
    """

    def lambdahhh(
        self,
        momenta: list = [0,0,0],
        only_topologies: list = [],
        simplify: bool = False,
        draw: Union[bool, int] = False,
        tadpoles: bool = None,
        wfrs: bool = None,
        exclude_particles: list = [],
        exclude_particles_pdg: list = [],
        parameters = {}
    ) -> dict:
        """ Wrapper around anyBSM.process and anyH3.lambdahhhCT:
            1. Ensures that the SM-like Higgs boson $h$ is correctly
            set/found in the model for the specified parameter set.
            2. Calculates all genuine tree-level and one-loop diagrams
            to $\\lambda_{hhh}$ as well as external-leg-,
            tadpole- and counter-term-contributions.
            3. Returns tuple of individual contributions

            Args:
                momenta: specify external momenta
                    only_topologies: consider only diagrams from specific
                    topologies (see `anyBSM.topologies`)
                simplify: simplify results using sympy
                draw: whether to draw Feynman diagrams using
                    [tikz-feynman](https://arxiv.org/abs/1601.05437). If set to
                    a number !=0 and in evaluation mode 'numerical',
                    this number is used as a cut-off to draw only diagram which
                    contribute with an absolute value larger than the cut-off.
                tadpoles: turn on (`True`) or off (`False`) all tadpole-insertion contributions i.e. all non-PI tadpole diagrams (warning: this is
                    not physically correct and needs to be compensated by using a custom_CT_hhh in the schemes.yml).
                    Can also be controlled from within the schemes.yml using the `tadpole: True/False` statement.
                    Default: `None` (use schemes.yml which defaults to `True`).
                wfrs: turn on (`True`) or off (`False`) all external diagrams with external-leg corrections.
                    Similar to the tadpoles, this can be set in the schemes.yml as well.
                    Default: `None` (uses schemes.yml which defaults to `True`)
                exclude_particles: list of fields (listed by names) to exclude from diagrams -- passed on to anyBSM.process and anyH3.lambdahhhCT.
                exclude_particles_pdg: list of fields (listed by PDG numbers) to exclude from diagrams -- passed on to anyBSM.process and anyH3.lambdahhhCT.
                parameters: optionally run `anyBSM.anyModel.setparameters(parameters)` so set input parameters

            Return:
                dictionary of the individual contributions: total, treelevel, genuine, wfr, tadpoles, massren, vevren, customren
        """
        if parameters:
            self.setparameters(params=parameters)
        if not self.SM_particles['Higgs-Boson']:
            self.find_SM_particles()
        if not self.SM_particles['Higgs-Boson']:
            logger.error("Cannot calculate lambda_hhh without you specifying what h to use!")
            return 0
        h = self.SM_particles['Higgs-Boson']
        if momenta[0] == "auto":
            if self.evaluation == 'numerical':
                momenta = [h.nmass**2, h.nmass**2, h.nmass**2]
            else:
                momenta = ['p12','p22','p32']
        results = self.process(h, h, h,
                               momenta = momenta,
                               only_topologies = only_topologies,
                               tadpoles = tadpoles,
                               wfrs = wfrs,
                               simplify = simplify,
                               draw = draw,
                               exclude_particles = exclude_particles,
                               exclude_particles_pdg = exclude_particles_pdg)

        treelevel = self._eval(f"-({results['ThreePointTree']})")
        genuine = self._eval(f"-({results['ThreePointB']} + {results['ThreePointC']})")
        wfr = self._eval(f"-({results['ThreePointWFRA']} + {results['ThreePointWFRB']})")
        tads = self._eval(f"-({results['ThreePointWFRT']} + {results['ThreePointTA']})")

        CTs = self.lambdahhhCT(
                simplify = simplify,
                draw = draw,
                only_topologies = only_topologies,
                tadpoles = tadpoles,
                exclude_particles = exclude_particles,
                exclude_particles_pdg = exclude_particles_pdg)
        vevren = self._eval(CTs['VEV_CT'])
        massren = self._eval(CTs['mass_CTs'])
        customren = self._eval(CTs['custom_CT_hhh'])

        total = treelevel + genuine + wfr + tads + massren + vevren + customren

        return {
            'total': total,
            'treelevel': treelevel,
            'genuine': genuine,
            'wfr': wfr,
            'tads': tads,
            'massren': massren,
            'vevren': vevren,
            'customren': customren
            }

    def lambdahhhCT(
            self,
            simplify: bool = False,
            only_topologies: list = [],
            draw: Union[bool, int] = False,
            tadpoles: bool = None,
            exclude_particles: list = [],
            exclude_particles_pdg: list = []
    ) -> dict:
        """ Calculates the counter-term contribution to the trilinear
        self-coupling at the one-loop order according to the
        specification of the loaded renormalization scheme (see
        anyBSM.load_renormalization_scheme()).\n
        The calculation involves several steps:
            1. Calculate the tree-level value for $\\lambda_{hhh}$ and
            express it in terms of all external parameters (masses, VEVs):
            $\\lambda_{hhh}(m_{h_1}, m_{h_2}, \\dots, v_{SM},
            v_{i},\\dots$).
            2. If `VEV_counterterm: OS` was specified in the
            renormalization scheme, it calculates
            $$\\delta^{(1)}_{v_{SM}}\\lambda_{hhh} = \\frac{\\partial
            \\lambda_{hhh}}{\\partial v_{SM}}\\delta^{(1)}v_{SM}$$
            with
            $$\\delta^{(1)}v_{SM} = v_{SM}\\left(\\frac{\\delta^{(1)}M_W^2}{M_W^2} - \\frac{\\delta^{(1)}M_Z^2}{2M_Z^2} -\\frac{\\delta^{(1)}e}{e} - \\frac{\\delta^{(1)}M_W^2}{2\\sin^2\\theta_w} + \\frac{\\delta^{(1)}M_Z^2}{2\\sin^2\\theta_w}\\right)$$
            where the OS counter-terms for the W- and Z-boson as well as the
            electric charge are extracted from the transverse parts of the
            W-, Z-,  Photon- and Z-Photon-selfenergies. See [2305.03015](https://arxiv.org/abs/2305.03015) for more details.
            3. For all `'OS'`-entries `mass_counterterms: {'hi': 'OS',
            ...}` the contribution
            $$\\delta^{(1)}_{m_{h_i}}\\lambda_{hhh} = -\\frac{\\partial
            \\lambda_{hhh}}{\\partial m_{h_i}}\\frac{1}{2
            m_{h_i}}\\mathrm{Re}\\Sigma^{(1)}_{h_i}(p^2=m_{h_i}^2)$$
            is calculated.
            4. If `custom_CT_hhh` has been specified in the renormalization
            scheme, the supplied string is being evaluated. For instance
            a valid value could look like:

                 <!-- language: yml -->

                    [...]
                    custom_CT_hhh: |
                            dlamdMh = Derivative(lambdahhh_tree, 'Mh')
                            dMh = Re(Sigma('h'))
                            dZhh = f"-1*({Sigmaprime('h')})"
                            self.custom_CT_hhh = f"3*Mh**2/vvSM*3/2*({dZhh}) + ({dlamdMh})*({dMh})/(2*Mh**2)"

             the value of `self.custom_CT_hhh` **must** be set in order to
            add the contribution to the final result:
            $$\\delta^{(1)}_{\\text{custom}}\\lambda_{hhh} = {\\tt \\text{self.custom_CT_hhh}}$$
            The `custom_CT_hhh` provides access to the full `self` object of
            the model with all its methods such as `anyBSM.Derivative`,
            `anyBSM.Sigma`, `anyBSM.Sigmaprime` or `anyBSM.process. This is
            particularly useful for more complex renormalization schemes. Note that specific choices of momenta, or restrictions on topologies, particles, tadpoles, must be included in the custom_CT_hhh definition.

        Args:
            simplify:  simplify results using sympy
            only_topologies: consider only diagrams from specific
                topologies (see `anyBSM.topologies`)
            draw: whether to draw Feynman diagrams using
                [tikz-feynman](https://arxiv.org/abs/1601.05437). If set to
                a number !=0 and in evaluation mode 'numerical',
                this number is used as a cut-off to draw only diagram which
                contribute with an absolute value larger than the cut-off.
            tadpoles: turn off all tadpole-insertion contributions (warning: this is
                not physically correct unless a custom_CT_hhh with the correct tadpole treatment is added!)
            exclude_particles: list of fields (listed by names) to exclude from diagrams -- passed on to anyBSM.Sigma and anyBSM.Sigmaprime via sigmaargs.
            exclude_particles_pdg: list of fields (listed by PDG numbers) to exclude from diagrams -- passed on to anyBSM.Sigma and anyBSM.Sigmaprime via sigmaargs.

        Returns:
            A dictionary `{`$\\text{'VEV_CT'}:
            \\delta^{(1)}_{v_{SM}}\\lambda_{hhh},\\, \\text{'mass_CTs'}:
            \\sum_{i} \\delta^{(1)}_{m_{h_i}}\\lambda_{hhh},\\,
            \\text{'custom_CT_hhh'}: \\delta^{(1)}_{\\text{custom}}\\lambda_{hhh}$ `}`
        """

        if not self.scheme:
            logger.warn("no renormalization scheme defined. Assuming all input parameters are MSbar values.")
            return {'VEV_CT': '', 'mass_CTs': '', 'custom_CT_hhh': ''}
        h = self.SM_particles['Higgs-Boson']
        argstring = f'Topologies: {only_topologies}; Particle exclusions: {exclude_particles}, {exclude_particles_pdg}; Tadpoles: {tadpoles}'
        argshash = md5(argstring.encode('utf-8')).hexdigest()
        CTfile = path.join(self.cachedir, f'result_{h}{h}{h}CT_{self.scheme_name}_scheme_{argshash}.json')
        if self.caching > 1 and path.isfile(CTfile):
            with open(CTfile, 'r') as f:
                logger.info(f'reading counterterm contributions for "{self.scheme_name}"-scheme from cache ({CTfile})')
                result = json.load(f)
                if self.evaluation == 'numerical':
                    for k,v in result.items():
                        try:
                            result[k] = self._eval(v)
                        except Exception as e:
                            raise Exception(f"There was an error when evaluating the '{k}'-counterterm contribution") from e

                elif self.evaluation == 'analytical':
                    for r in result:
                        for name,c in reversed(self.couplings.items()):
                            result[r] = result[r].replace(name, f'({c.value})')
                return result
        firstrun = self.caching > 1 and self.evaluation != 'abbreviation' and not only_topologies and not draw
        if firstrun:
            evalSAVE = self.evaluation
            logger.info('No CT results found in cache. Calculating in abbreviation-mode to fill cache.')
            self.set_evaluation_mode('abbreviations')

        # options used for calculation of all two-point funtions in the following
        sigmaargs = {
                'momentum': 'auto' if self.OSmomenta else 0,
                'only_topologies': only_topologies,
                'tadpoles': tadpoles,
                'simplify': simplify,
                'draw': draw,
                'exclude_particles': exclude_particles,
                'exclude_particles_pdg': exclude_particles_pdg}

        OSlist = [self.all_particles[k] for k,v in self.scheme['mass_counterterms'].items() if v == 'OS']
        custom_ct_str = self.scheme.get('custom_CT_hhh', None)
        treelevel_needed = OSlist or self.scheme['VEV_counterterm'] == 'OS' or custom_ct_str
        # calculate tree-level analytical (if not already)
        if treelevel_needed and (self.treelevel == '0' or self.evaluation != 'analytical'):
            logger.info('calculate counterterm contributions to lambda_hhh')
            evalSAVE2 = str(self.evaluation)
            self.set_evaluation_mode('analytical') # enforce analytic evaluation to be able to perform derivatives

            logger.info('Calculating tree-level value of lambda_hhh and expressing it in terms of all input parameters.')
            self.treelevel = self.process(h, h, h, momenta = [], only_topologies = ['ThreePointTree'], simplify = simplify)['ThreePointTree']
            self.treelevel = self.treelevel.replace('cmath.','')

            treemasses = [p.mass.name for p in OSlist]

            self.treelevel = -1*self.SolveDependencies(self.treelevel, simplify = simplify, exclude = treemasses+[self.SM_parameters['VEV'].name])
            logger.info(f'lamda_hhh^tree = {self.treelevel}')

            treemasses = [m for m in treemasses if m in str(self.treelevel)]
            logger.info(f"found the following scalar masses appearing at the tree-level: {treemasses}")

            self.set_evaluation_mode(evalSAVE2)

        # contributions from mass renormalization
        OSliststr = [f"{p.name} ({p.mass})" for p in OSlist]
        logger.info(f"the masses of the following particles are renormalized OS: {' '.join(OSliststr) if OSlist else 'none'}")
        massren = self._eval('')
        for p in tqdm(OSlist, leave = False, disable = not self.progress, desc = 'calculate mass CT contributions'):
            logger.info(f'taking derivative of tree-level result w.r.t. {p.mass.name}')
            massderivative = self.Derivative(self.treelevel, p.mass.name, simplify = simplify, dependencies = False)
            if massderivative == '0' or not massderivative:
                logger.warning(f'derivative of lambda_hhh^tree w.r.t {p.mass.name} vanishes!')
                continue
            selfenergy = self.Sigma(p.name, **sigmaargs)
            massren += self._eval(f"-({massderivative})*Re({selfenergy})/(2*{p.mass})")

        # contributions from vev renormalization
        vevren = self._eval('')
        vevderivative = '0'
        if self.scheme['VEV_counterterm'] == 'OS':
            logger.info('calculate CT contribution due to electroweak VEV')
            logger.info(f'taking derivative of tree-level result w.r.t. {self.SM_parameters["VEV"].name}')
            vevderivative = self.Derivative(self.treelevel, self.SM_parameters['VEV'].name, simplify = simplify, dependencies = False)
            if str(vevderivative) == '0':
                logger.warning('derivative of lambda_hhh^tree w.r.t the SM VEV vanishes!')

        if str(vevderivative) != '0':
            # parameters
            MW2 = self.getmass('W-Boson', 2)
            MZ2 = self.getmass('Z-Boson', 2)
            CW = f'sqrt(({MW2})/({MZ2}))'
            SW = f'(sqrt(1-({MW2})/({MZ2})))'
            alphaQEDinverse = f"1/({self.SM_parameters['alphaQEDinverse']})"
            EL = f"(2*sqrt({alphaQEDinverse})*sqrt(pi))"
            VEV = f'2*sqrt(({MW2}*{MZ2}-{MW2}**2)/{MZ2})/{EL}'
            dalpha = self.SM_parameters['Dalpha'].name

            # W/Z selfenergies
            SigmaW = self.Sigma(self.all_particles['W-Boson'], **sigmaargs)
            SigmaZ = self.Sigma(self.all_particles['Z-Boson'], **sigmaargs)

            # Photon(-Z-mixing) selefenergies
            SigmapAnolf = self.Sigmaprime(
                    self.all_particles['Photon'],
                    **ChainMap({'momentum': 0, 'exclude_particles_pdg': list(set(exclude_particles_pdg) | set(self.light_SM_fields))}, sigmaargs))
            SigmaAlf = self.Sigma(
                    self.all_particles['Photon'],
                    **ChainMap({'momentum': MZ2, 'exclude_particles_pdg': list(set(exclude_particles_pdg) | set(self.heavy_fields))}, sigmaargs))
            SigmaAZ = self.Sigma(
                    self.all_particles['Photon'], self.all_particles['Z-Boson'],
                    **ChainMap({'momentum': 0}, sigmaargs))

            # counterterms
            deltaMW = f'Re({SigmaW})/({MW2})'
            deltaMZ = f'Re({SigmaZ})/({MZ2})'
            deltaEL = f'(1/2*(({dalpha}) + Re({SigmapAnolf}) + Re({SigmaAlf})/({MZ2}))\
                    +  SignSinThetaW*({SW}/({CW}*{MZ2}))*Re({SigmaAZ}))'
            vevCT = f'{VEV}*(({deltaMW})/2 - {deltaEL} +\
                    ({CW}**2)/(2*{SW}**2)*(({deltaMZ}) - ({deltaMW})))'

            vevren += self._eval(f'({vevCT})*({vevderivative})')

        customren = self._eval('')
        if custom_ct_str:
            logger.info('calculate custom CT contribution to lambda_hhh')
            # define a few convenient functions which can directly be used in the custom_CT_hhh string
            Tadpole = self.Tadpole           # noqa: F841
            Sigmaprime = self.Sigmaprime     # noqa: F841
            Sigma = self.Sigma               # noqa: F841
            Derivative = self.Derivative     # noqa: F841
            process = self.process           # noqa: F841
            SM_particles = self.SM_particles # noqa: F841
            lambdahhh_tree = self.treelevel  # noqa: F841
            try:
                exec(custom_ct_str)
            except Exception as e:
                raise Exception("CounterTermError", "could not execute your custom counter term due to following error: \n" + str(e))

            if not hasattr(self, 'custom_CT_hhh'):
                logger.error('your custom counter term did not set `self.custom_CT_hhh`')
                self.custom_CT_hhh = self._eval('')
            if self.custom_CT_hhh == 0:  # noqa: F821
                logger.warning('your custom counter term evaluated to zero (0)!')
            try:
                customren = self._eval(self.custom_CT_hhh)  # noqa: F821
            except Exception as e:
                logger.error("could not calculate custom counter term due to following error: \n" + str(e))

        result = {'VEV_CT': vevren, 'mass_CTs': massren, 'custom_CT_hhh': customren}

        if not only_topologies and self.evaluation != 'numerical':
            logger.debug(f'Writing results to cache ({CTfile}).')
            with open(CTfile, 'w') as f:
                json.dump(result, f)
        if firstrun:
            self.set_evaluation_mode(evalSAVE)
            if self.evaluation == 'numerical':
                for k,v in result.items():
                    try:
                        result[k] = self._eval(v)
                    except Exception as e:
                        raise Exception(f"There was an error when evaluating the '{k}'-counterterm contribution") from e

            elif self.evaluation == 'analytical':
                for r in result:
                    for name,c in reversed(self.couplings.items()):
                        result[r] = result[r].replace(name, f'({c.value})')

        return result
