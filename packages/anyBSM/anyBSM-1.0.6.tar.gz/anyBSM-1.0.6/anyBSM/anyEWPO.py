from __future__ import division
import logging
from cmath import pi, sqrt
from anyBSM.Delta_r_SM import Delta_r_SM
import anyBSM.physic_utils as physics_utils
from anyBSM.anyProcess import anyProcess

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__doc__ = """
#  Electroweak precision observables (EWPOs)
<div class="mermaid">
flowchart RL
    subgraph classes
    anyModel --> anyProcess --> anyEWPO
    end
    subgraph methods/EWPOs
    anyEWPO --> Delta_r --> M_W
    anyEWPO --> ...
    end
</div>
"""


class anyEWPO(anyProcess):
    """ A class which collects calculations for electroweak precision observables.
    This class inherits from `anyBSM.anyProcess` which itself inherits from `anyBSM.anyModel`.
    For more information on how to initialize this class, see the documentation of the mother-class `anyBSM.anyModel.anyModel.__init__` or the online documentation.

    The class `anyBSM.anyEWPO` currently implements two methods:
      * `anyBSM.anyEWPO.anyEWPO.Delta_r()`: caclulates $\\Delta r$
      * `anyBSM.anyEWPO.anyEWPO.MW()`: calculates $M_W$

    It is assumed that a proper renormalization scheme has already been loaded and all SM-like particles/parameters are correctly identified.
    To ensure this `anyBSM.anyModel.anyModel.load_renormalization_scheme()` should be issued beforehand (see example below).

    Example:
    ```python
    from anyBSM import anyBSM
    SSM = anyBSM('SSM', scheme_name = 'OS')
    SSM.MW()
    ```
    which calculates $M_W$ in the singlet extended SM at the one-loop order including
    all known higher-order SM-corrections to $\\Delta r$ (see `anyBSM.Delta_r_SM`).
    """

    def Delta_r(self, MWrun: float, MWfw: float, MZrun: float, MZfw: float, incl_SM_ho: bool = True, **kwargs) -> float:
        """ Calculates $\\Delta r$.

        Args:
            MWrun: $M_W$ defined using a running width
            MWfw: $M_W$ defined using a fixed width
            MZrun: $M_Z$ defined using a running width
            MZfw:  $M_Z$ defined using a fixed width
            incl_SM_ho: whether to include higher-order SM corrections
            kwargs: all arguments supported by anyBSM.process
            parameters: optionally run `anyBSM.anyModel.setparameters(parameters)` so set input parameters

        Returns:
            $\\Delta r$
        """

        # set parameters
        MWfw2 = f'({MWfw}**2)'
        MZfw2 = f'({MZfw}**2)'
        CW = self._eval(f'({MWfw}/{MZfw})')
        SW = self._eval(f'sqrt(1-{MWfw2}/{MZfw2})')
        aEW = self._eval(f"1/({self.SM_parameters['alphaQEDinverse'].name})")
        dalpha = self._eval(self.SM_parameters['Dalpha'].name)
        GFermi = self._eval(self.SM_parameters['GFermi'].name)
        asMZ = self._eval(f"{self.SM_parameters['alphaQCD'].name}")

        ZA = f"(SignSinThetaW*({self.Sigma(self.all_particles['Z-Boson'], self.all_particles['Photon'], momentum=0, **kwargs)})/{MZfw2})"

        deltaEL = f"1/2*({dalpha} +\
                ({self.Sigma(self.all_particles['Photon'], momentum = 'MZ**2', exclude_particles_pdg=self.heavy_fields, **kwargs)})/{MZfw2}\
                + {self.Sigmaprime(self.all_particles['Photon'], exclude_particles_pdg=self.light_SM_fields, **kwargs)})\
                + {SW}/({CW})*{ZA}"

        Wselfp0 = f"(({self.Sigma(self.all_particles['W-Boson'], momentum=0, **kwargs)})/{MWfw2})"

        WselfOS = f"(({self.Sigma(self.all_particles['W-Boson'], **kwargs)})/{MWfw2})"
        ZselfOS = f"(({self.Sigma(self.all_particles['Z-Boson'], **kwargs)})/{MZfw2})"
        dSW = f"-{SW}/2*{CW}**2/{SW}**2*({WselfOS} - {ZselfOS})"

        # TODO: implement generic {F,F}->{F,F} at zero external momenta as well as generic fermion selfenergies
        VertexBoxZf = f"-2/({CW}*{SW})*{ZA} \
                + ({aEW})/(4*pi*{SW}**2)*(6+(7-4*{SW}**2)/(2*{SW}**2)*log({CW}**2))"

        dr = self._eval(f"{Wselfp0}-{WselfOS} \
                + 2*({deltaEL}) - 2*({dSW})/{SW} + {VertexBoxZf}")

        if self.evaluation != 'numerical':
            if incl_SM_ho:
                logger.warning("Can't include higher-order SM corrections to $Delta r$ in analytical mode.")
            return dr

        # calculate SM higher-order corrections
        if incl_SM_ho:
            MH = self.getmass('Higgs-Boson')
            MT = self.getmass('Top-Quark')
            MB = self.getmass('Bottom-Quark')
            MC = self.getmass('Charm-Quark')
            MS = self.getmass('Strange-Quark')
            MU = self.getmass('Up-Quark')
            MD = self.getmass('Down-Quark')
            ML = self.getmass('Tau-Lepton')
            MM = self.getmass('Muon-Lepton')
            ME = self.getmass('Electron-Lepton')
            asMT = physics_utils.RunAlfas(MZfw, MT, asMZ)

            _, drSM2Lrem, drSMho = Delta_r_SM(MWrun, MWfw, MZrun, MZfw, MH, MT, MB, aEW, asMT, dalpha, GFermi, ME, MM, ML, MU, MD, MC, MS)

            dr += dalpha**2 + 2*dalpha*(dr - dalpha) + drSM2Lrem + drSMho  # dalpha is contained in dr1L (see also footnote 6 of 1506.07465)

        return dr.real

    def MW(self, MWstart: float = 80.0, precision: int = 8, incl_SM_ho: bool = True, parameters: dict = {}, **kwargs) -> float:
        """ Iteratively calculates $M_W$ from $G_{Fermi}$ and corrections to the muon decay
        (i.e. $\\Delta r$, see anyEWPO.Delta_r).

        Args:
            MWstart: start value of the iteration
            precision: stop iteration if last `precision`-digits do
                not change w.r.t the previous iteration
            incl_SM_ho: whether to include the higher-order
                corrections from the Standard Model (with the one-loop
                result being subtracted)
            kwargs: all arguments supported by anyBSM.process

        Returns:
            $M_W$
        """
        if self.evaluation != 'numerical':
            logger.error('Can only compute MW iteratively in numerical evaluation mode. (run `set_evaluation_mode("numerical")` or `-e numerical`)')
            return
        if parameters:
            self.setparameters(params=parameters)
        if not self.SM_parameters['alphaQEDinverse']:
            self.find_SM_parameters()
        if not self.SM_particles['W-Boson']:
            self.find_SM_particles()
        GFermi = self.SM_parameters['GFermi'].value
        MWsave = self.SM_particles['W-Boson'].nmass
        MWpara = self.SM_particles['W-Boson'].mass.name
        MZrun = self.SM_particles['Z-Boson'].nmass
        MZpara = self.SM_particles['Z-Boson'].mass.name
        aEW = 1/self.SM_parameters['alphaQEDinverse'].value
        asMZ = self._eval(f"{self.SM_parameters['alphaQCD'].name}")
        asMW = physics_utils.RunAlfas(MZrun, MWsave, asMZ)
        cnt = 0
        MWa = MWstart
        MWb = -12345.0

        # ensure that one-loop corrections to Delta_r use fixed-width Z boson mass if higher order corrections are activated
        if incl_SM_ho:
            MZfw = physics_utils.MZfw(MZrun)
            self.setparameters({MZpara: MZfw})
        else:
            MZfw = MZrun

        while abs(MWa - MWb) > 10**(-precision):
            if cnt == 0:
                MWb = MWa
            cnt += 1
            if cnt > 99:
                logger.error(f'MW iteration did not converge in-time.\
                        Last two values: MW = {MWa} GeV and MW = {MWb} GeV.')
                return
            self.setparameters({MWpara: MWb})
            MWrun = physics_utils.MWrun(MWb, asMW, GFermi)
            Deltar = self.Delta_r(MWrun, MWb, MZrun, MZfw, incl_SM_ho=incl_SM_ho, **kwargs)
            MWa = MWb
            MWb = sqrt(MZfw**2*(1/2+sqrt(1/4-pi*aEW/(sqrt(2)*GFermi*MZfw**2)*(1 + Deltar))))
            if abs(MWb.imag) > 1e-6:
                logger.warning(f'MW developed imaginary part: {MWb} GeV')
            logger.info(f'MW iteration {cnt}: MW = {MWb} GeV; Delta_r = {Deltar}.')
            MWb = MWb.real
        if incl_SM_ho:
            MWres = physics_utils.MWrun(MWb, asMW, GFermi)
        else:
            MWres = MWb

        # reset UFO parameter value
        self.setparameters({MWpara: MWsave, MZpara: MZrun})

        return MWres.real
