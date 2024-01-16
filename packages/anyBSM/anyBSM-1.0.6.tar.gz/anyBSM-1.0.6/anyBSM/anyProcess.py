from __future__ import division
import logging
from tqdm.auto import tqdm
from math import factorial
from os import path
import json
from collections import defaultdict, OrderedDict
from itertools import permutations, combinations_with_replacement
from hashlib import md5
from typing import Union
import cmath # noqa: F401
from cmath import pi, sin, cos, tan, atan, sqrt, log # noqa: F401
from anyBSM.loopfunctions import lnbar, A0, B0, B00, dB0, dB00, B1, dB1, C0, C1, C2, eps, set_renscale # noqa: F401
from anyBSM.ufo.function_library import complexconjugate, conjugate, Abs, I, Re, Im # noqa: F401
from anyBSM.topologies import TOPOLOGIES
from anyBSM.diagrams import GenericDiagrams
from anyBSM.utils import fieldtypes
from anyBSM.anyModel import anyModel

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
__doc__ = """
<div class="mermaid">
flowchart RL
    subgraph classes
    anyModel --> anyProcess;
    end
    subgraph methods
    anyProcess --> insert_fields --> process
    end
    subgraph wrappers/helpers
    process --> Sigma
    process --> Sigmaprime
    process --> Tadpole
    end
</div>
"""

class anyProcess(anyModel):
    """ Class for the generation and caclulation of all Feynman diagrams for a given set of external fields.
    This class inherits from `anyBSM.anyModel`.
    For more information on how to initialize this class, see the documentation of the mother-class `anyBSM.anyModel.anyModel.__init__`  or consult the online documentation.
    """

    def process(
            self,
            *externalfields,
            momenta: list = [],
            derivative: bool = False,
            only_topologies: list = [],
            tadpoles: bool = None,
            wfrs: bool = None,
            simplify: bool = False,
            draw: Union[bool, int] = False,
            export: str = '',
            exclude_particles: list = [],
            exclude_particles_pdg: list = []
    ) -> defaultdict:
        """ For given external fields `externalfields` calculate all possible one-loop diagrams.

        The procedure is roughly as follows:
          * find all possible insertions for all possible topologies using `anyProcess.insert_fields`
          * iterate over the resulting diagram insertions
          * extract the appropriate couplings and masses specified in the UFO for the calculation of the diagrams
          * use generic results for those diagrams; apply color factors if necessary

        Args:
            externalfields: list of field names or objects
            momenta: **squared** momenta
            derivative: whether to calculate the derivate w.r.t
                squared external momentum (only for two-point functions)
            only_topologies: list of specific topologies of
                diagrams to restrict to
            tadpoles: turn on (`True`) or off (`False`) all tadpole-insertion contributions i.e. all non-PI tadpole diagrams.
                Can also be controlled from within the schemes.yml using the `tadpole: True/False` statement.
                Default: `None` (use schemes.yml which defaults to `True`).
                Note that `only_topologies` is superior to `tadpoles` and `tadpoles` is superior to the value in the schemes.yml.
            wfrs: turn on (`True`) or off (`False`) all external diagrams with external-leg corrections.
                Similar to the tadpoles, this can be set in the schemes.yml as well.
                Default: `None` (uses schemes.yml which defaults to `True`)
                Note that `only_topologies` is superior to `wfrs` and `wfrs` is superior to the value in the schemes.yml.
            simplify: whether to simplify results using sympy
            export: save results to a file (absolute path). If the
                file exists, the result is appended to that file.
            draw: whether to draw Feynman diagrams using
                [tikz-feynman](https://arxiv.org/abs/1601.05437). If set to
                a number !=0 and in evaluation mode 'numerical',
                this number is used as a cut-off to draw only diagram which
                contribute with an absolute value larger than the cut-off.
            exclude_particles: list of fields to exclude from diagrams (listed by names).
            exclude_particles_pdg: list of fields to exclude from diagrams (listed by PDG numbers).

        Returns:
            analytical/numerical/abbreviated result depending on the evaluation mode
            `anyModel.evaluation`.
        """
        externalfields = self._fieldlist(*externalfields)
        extfields = ''.join([f.name for f in externalfields])
        nextfields = len(externalfields)
        momenta = [0 for i in range(nextfields)] if not momenta else momenta
        momenta_placeholder = [f'PEXT{i+1}2' for i in range(nextfields)]
        derivative_str = '' if not derivative else '_derivative'
        wfrs_str = (wfrs is not None and wfrs is False) or not self.scheme.get('wfrs', True)
        tadpoles_str = (tadpoles is not None and wfrs is False) or not self.scheme.get('tadpoles', True)
        argstring = f'Topologies: {only_topologies}; Particle exclusions: {exclude_particles}, {exclude_particles_pdg}; Simplify: {simplify}; WFRs: {wfrs_str}; Tadpoles: {tadpoles_str}'
        # TODO: write argstring as comment to the json file
        argshash = md5(argstring.encode('utf-8')).hexdigest()
        cachefile = path.join(self.cachedir, f'result_{extfields}{derivative_str}_{argshash}.json')
        loop_particles = [p for p in self.loop_particles if (p.name not in exclude_particles and abs(p.pdg_code) not in exclude_particles_pdg)]
        loop_particles = loop_particles + [p.anti() for p in loop_particles if p != p.anti()]
        zero = self._eval('')
        if path.isfile(cachefile) and self.caching > 1 and not draw:
            logger.info(f'reading results for {extfields}-amplitude from cache ({cachefile}).')
            with open(cachefile, 'r') as f:
                result = defaultdict(lambda *x: zero)
                result.update(json.load(f))
        else:
            firstrun = self.caching > 1 and self.evaluation != 'abbreviation' and not draw
            if firstrun:
                evalSAVE = self.evaluation
                logger.info('No results found in cache. Calculating in abbreviation-mode to fill cache.')
                self.set_evaluation_mode('abbreviations')
                zero = self._eval('')
            if draw:
                from anyBSM.latex.drawer import DrawProcess # import here to avoid sympy import in numerical runs
                drawer = DrawProcess(self, externalfields, simplify, draw)
            all_insertions = OrderedDict()
            if only_topologies:
                for topo in only_topologies:
                    all_insertions. update(self.insert_fields(*externalfields,  only_topology=topo, wfrs = wfrs, tadpoles = tadpoles, exclude_particles = exclude_particles, exclude_particles_pdg = exclude_particles_pdg))
            else:
                all_insertions. update(self.insert_fields(*externalfields, wfrs = wfrs, tadpoles = tadpoles, exclude_particles = exclude_particles, exclude_particles_pdg = exclude_particles_pdg))
            diagramtype = fieldtypes(list(externalfields))
            result = defaultdict(lambda *x: zero)
            genericdiags  = GenericDiagrams(evaluation = self.evaluation, MSDR = int(not self.dimensional_reduction))
            if self.evaluation == 'numerical':
                momenta_in = [self._eval(m) for m in momenta]
            else:
                momenta_in = momenta_placeholder
            desc = f'Calculate all diagrams for {extfields}-amplitude'
            logger.info(desc)
            bar = tqdm(all_insertions.items(), disable = not self.progress, desc = desc, leave = False, total = len(all_insertions))
            for topo, insertions in bar:
                bar.set_description(f'{desc} ({topo})')
                if topo not in TOPOLOGIES[nextfields]:
                    # result[topo] = zero
                    continue
                topology = TOPOLOGIES[nextfields][topo]
                if not hasattr(genericdiags, topology.Amplitude):
                    logger.error(f'Topology {topology.Amplitude} not found')
                    continue
                genamp = genericdiags.__getattribute__(topology.Amplitude)
                if genamp is None:
                    logger.error(f'Generic amplitude not implemented for topology {topo} for external fields = {diagramtype}')
                    continue
                i = 0
                bar2 = tqdm(insertions, leave=False, disable = not self.progress, total = len(insertions), desc = 'diagrams: ')
                for particles_s, couplings_s in bar2:
                    i += 1
                    particles = [self.all_particles[p] for p in particles_s]
                    couplings = [{k : self.couplings.get(v,v) for k,v in c.items()} for c in couplings_s]
                    if any([p not in loop_particles and p.antiname not in loop_particles for p in particles]):
                        continue

                    chargefac = 1 # instead, we sum over all (anti)-particles
                    colorfac = self.ColorFactor(externalfields, particles, topo)
                    fac = self._eval(f'{colorfac}*{chargefac}*{topology.symmetryfactor}/(16*pi**2)')
                    ampargs = {
                            'external': externalfields,
                            'internal': particles,
                            'coupling_objects': couplings,
                            'derivative': derivative,
                            'factor': fac
                            }
                    tmp = genamp(momenta = momenta_in, **ampargs)
                    if 'WFR' in topo or topo == 'ThreePointB' and tmp:
                        if momenta_in[0] == momenta_in[1] == momenta_in[2]: # all momenta 0
                            tmp = self._eval(f'3*({tmp})') if tmp else self._eval('')
                        else:
                            tmp2 = genamp(momenta = [momenta_in[2], momenta_in[0], momenta_in[1]], **ampargs)
                            tmp3 = genamp(momenta = [momenta_in[1], momenta_in[2], momenta_in[0]], **ampargs)
                            tmp = self._eval(f'{tmp}+{tmp2}+{tmp3}')

                    if tmp and simplify and self.evaluation != 'numerical':
                        try:
                            bar2.set_postfix_str('(simplifying...)')
                            tmp = self.sympify(str(tmp)+'+0', simplify = simplify)
                            bar2.set_postfix_str('')
                        except Exception as e:
                            bar2.set_postfix_str('')
                            logger.exception('Not able to simplify analytical results: ' + str(e))
                            logger.error('Continuing with un-simplified result.')
                    result[topo] += self._eval(str(tmp) + '+0')
                    if draw:
                        drawer.add_diagram(topo,particles,tmp)

                # if not result[topo]:
                #     result[topo] = "0"
            try:
                bar.close()
                bar2.close()
            except UnboundLocalError:
                pass
            if draw:
                drawer.write(result)

            if self.evaluation == 'abbreviations':
                logger.debug(f'Writing results to cache ({cachefile}).')
                with open(cachefile, 'w') as f:
                    json.dump(result,f)
            if firstrun:
                self.set_evaluation_mode(evalSAVE)

        momenta_d = {f'PEXT{i+1}2' : m for i,m in enumerate(momenta)}
        if self.evaluation == 'numerical':
            momenta_d = {k: self._eval(v) for k,v, in momenta_d.items()}
            result.update({k: self._eval(v, **momenta_d) for k,v in result.items()})
        else:
            for r in result:
                for m,md in momenta_d.items():
                    result[r] = result[r].replace(m, str(md))
                if self.evaluation == 'analytical':
                    for name,c in reversed(self.couplings.items()):
                        result[r] = result[r].replace(name, f'({c.value})')

        if export:
            export = path.abspath(export)
            if not path.isdir(path.dirname(export)):
                logger.error(f'{export}: not a directory')
                return result
            with open(export, 'w') as e:
                self._print(f'Saving results to {export}.')
                json.dump(result, e)
        return result

    def Sigma(self, f1, f2="", momentum: Union[str, float] = 'auto', signconvention = 1, **kwargs):
        """ Calculates the self-energy for field with name `f1`.
        This is a wrapper around `anyProcess.process()`.

        Args:
            f1: field name or object
            f2: field name or object (default: `f2=f1`)
            momentum: external momentum **squared**. 'auto' uses
                geometric mean of the squared masses of the particles.
            signconvention: flag allowing to switch between overall sign convention for self-energies. The default value, 1, corresponds to the convention employed in SARAH and many works on generic calculations, where mass counterterms are equal to *minus* the self-energy. Setting this flag to 0 changes to the convention used e.g. in FeynHiggs, with mass counterterms equal to the self-energy with a *plus*.
            **kwargs: additional keyword arguments passed to `self.process`

        Returns:
            analytical/numerical/abbreviated result depending on the evaluation mode
            `anyModel.evaluation`.
        """
        if not f2:
            f2 = f1
        p1 = self.all_particles.get(f1, f1)
        p2 = self.all_particles.get(f2, f2)
        p2 = p2.anti()
        if not (p1 and p2):
            logger.error(f"invalid input for Sigma({f1},{f2}): field name(s) not found.")
            return 0
        if momentum == 'auto':
            if self.evaluation == 'numerical':
                s = (p1.nmass**2 + p2.nmass**2)/2
            elif p1.mass == p2.mass:
                s = f'{p1.mass.name}**2'
            else:
                s = f'({p1.mass.name}**2 + {p2.mass.name}**2)/2'
        else:
            s = momentum
        sigma = self.process(p1, p2, momenta = [s], **kwargs)
        sigma = self._eval('+'.join([str(r) for r in sigma.values()]))
        if not sigma:
            return 0
        else:
            if signconvention:
                return sigma
            else:
                return -sigma

    def Sigmaprime(self, *args, **kwargs):
        """ Passes all its arguments to `anyProcess.Sigma()` with
        `derivative=True` i.e. calculates the derivate of the
        two-point function w.r.t. the squared external momentum

        Returns:
            analytical/numerical/abbreviated result depending on the evaluation mode
            `anyModel.evaluation`.
        """
        return self.Sigma(*args, derivative = True, **kwargs)

    def Tadpole(self, f, **kwargs):
        """ Calculates the (scalar) tadpole diaram for field with name `f`.
        This is a wrapper around `anyProcess.process()`.

        Args:
            f1: field name (str) or UFO object
            **kwargs: additional keyword arguments passed to `self.process`

        Returns:
            analytical/numerical/abbreviated result depending on the evaluation mode
            `anyModel.evaluation`.
        """
        p = self.all_particles.get(f, f)
        if not p:
            logger.error(f"invalid input for Tadpole({f}): field not found.")
            return 0
        tad = self.process(p, **kwargs)
        return self._eval('+'.join([str(r) for r in tad.values()]))

    def insert_fields(
            self,
            *externalfields,
            only_topology: Union[None, str] = None,
            wfrs: bool = None,
            tadpoles: bool = None,
            exclude_particles: list = [],
            exclude_particles_pdg: list = []
    ) -> OrderedDict:
        """ Insert all possible field permuations for given process
        with `externalfields` into `anyBSM.topologies.TOPOLOGIES`.
        The insertions are carried out using a brute-force method which inserts
        all possible field combinations into all possible topologies and checks
        whether the resulting couplings are all existing in the UFO model.

        Args:
            externalfields: field names or objects
            only_topology: consider only this specific topology rather
                than all possible ones (see `anyBSM.topologies`).
            tadpoles: turn on (`True`) or off (`False`) all tadpole insertions i.e. all non-PI tadpole diagrams.
                Can also be controlled from within the schemes.yml using the `tadpole: True/False` statement.
                Default: `None` (use schemes.yml which defaults to `True`).
                Note that `only_topologies` is superior to `tadpoles` and `tadpoles` is superior to the value in the schemes.yml.
            wfrs: turn on (`True`) or off (`False`) all external diagrams with external-leg corrections.
                Similar to the tadpoles, this can be set in the schemes.yml as well.
                Default: `None` (uses schemes.yml which defaults to `True`)
                Note that `only_topologies` is superior to `wfrs` and `wfrs` is superior to the value in the schemes.yml.
            exclude_particles: list of fields to exclude from diagrams (listed by names).
            exclude_particles_pdg: list of fields to exclude from diagrams (listed by PDG numbers).

        Returns:
            `OrderedDict` of insertions.
        """
        topologies = TOPOLOGIES[len(externalfields)]
        if not only_topology:
            if (tadpoles is not None and tadpoles is False) or not self.scheme.get('tadpoles', True):
                topologies = {k:v for k,v in topologies.items() if v.tadpole is False}
                tadpoles = False
                logger.info('Ignoring non-1PI tadpole diagrams.')
            else:
                tadpoles = True
            if (wfrs is not None and wfrs is False) or not self.scheme.get('wfrs', True):
                topologies = {k:v for k,v in topologies.items() if v.wfr is False}
                logger.info('Ignoring non-1PI WFR diagrams.')
                wfrs = False
            else:
                wfrs = True

        insertions = OrderedDict()
        extfields = ''.join([f.name for f in externalfields])

        argstring = f'Topologies: {only_topology or "all"}; Particle exclusions: {exclude_particles}, {exclude_particles_pdg}; WFRs: {wfrs}; Tadpoles: {tadpoles}'
        # TODO: write argstring as comment to the json file
        argshash = md5(argstring.encode('utf-8')).hexdigest()
        cachefile = path.join(self.cachedir, f'insertions_{extfields}_{argshash}.json')

        loop_particles = [p for p in self.loop_particles if (p.name not in exclude_particles and abs(p.pdg_code) not in exclude_particles_pdg)]
        loop_particles = loop_particles + [p.anti() for p in loop_particles if p != p.anti()]
        if not loop_particles:
            return insertions
        caching = self.caching > 0
        if path.isfile(cachefile) and caching:
            logger.info(f'Using insertions for {extfields} from cache ({cachefile}).')
            with open(cachefile, 'r') as f:
                return json.load(f)
        if not only_topology:
            desc = f'determine all insertions for {extfields}-amplitude for all topologies.'
        else:
            desc = f'determine all insertions for {extfields}-amplitude for the {only_topology} toplogy.'
        logger.info(desc)
        if only_topology and only_topology in topologies:
            topologies = {only_topology: topologies[only_topology]}

        for t, topo in tqdm(topologies.items(), disable = not self.progress, desc = desc, leave = False):
            insertions[t] = []
            topo.insertexternal(*externalfields)
            # TODO: this could be optimized further. For now it works and is nor urgent (due to caching)
            num = int(factorial(len(loop_particles)+topo.nint-1)/factorial(topo.nint)/factorial(len(loop_particles)-1))
            for particles in tqdm(combinations_with_replacement(loop_particles, topo.nint), total = num, leave = False, desc = t, disable = not self.progress):
                perms = set(permutations(particles))
                for p in perms:
                    topo.insertinternal(*p)
                    if topo.tadpole is not False and topo.intfields[topo.tadpole].insertion.spin != 1:
                        # only scalar tadpoles
                        continue
                    insertion = topo.getinsertion()
                    couplings = [self.getcoupling(ins) for ins in insertion]
                    if all(couplings):
                        insertions[t].append([[k.name for k in p], couplings])
            logger.debug(f'Found insertions for topology {t}: {[i[0] for i in insertions[t]]}')
        logger.info(f'{sum(len(i) for i in insertions.values())} (potentially) non-zero diagrams to calculate found.')
        if caching:
            with open(cachefile, 'w') as f:
                json.dump(insertions, f, default = lambda x: x.name, indent = None)
        return insertions

    def ColorFactor(self, externalfields: list, particles: list, topo: str):
        """ hard-coded color factors for various topologies

        Args:
            externalfields: list of field names or objects
            particles: list of particles inserted into the topology
            topo: name of topology to be considered

        Returns:
            color factor
        """

        colors = [p.color for p in particles] if particles else [0]
        extcolors = [p.color for p in externalfields]
        if topo in ['TwoPointTA','ThreePointTA','ThreePointWFRA','ThreePointWFRB']:
            colors = colors[1:]
        if topo  == 'ThreePointWFRT':
            colors = colors[2:]
        colors = tuple(sorted(colors))

        if all(c == 1 for c in extcolors):
            colorfac = {
                    (0,): 1,
                    (1,): 1,
                    (3,): 3,
                    (-3,): 3,
                    (8,): 8,
                    (1,1): 1,
                    (3,3): 3,
                    (-3,-3): 3,
                    (8,8): 8,
                    (1,1,1): 1,
                    (3,3,3): 3,
                    (-3,-3,-3): 3,
                    (8,8,8): 8
                    }.get(colors, 0)

        if extcolors in [[3,-3],[-3,3]]:
            colorfac = {
                    (0,): 1,
                    (1,): 1,
                    (3,): 3,
                    (-3,): 3,
                    (8,): 8,
                    (1,1): 1,
                    (-3,1): 1,
                    (1,3): 1,
                    (3,8): '4/3',
                    (-3,8): '4/3'
                    }.get(colors, 0)

        if colorfac == 0:
            colorfac = 1
            # TODO caclulate color factor using UFO couplings
            logger.error(f'Color structure "{colors}" not supported in diagram {topo}[{particles}]!')
        return colorfac
