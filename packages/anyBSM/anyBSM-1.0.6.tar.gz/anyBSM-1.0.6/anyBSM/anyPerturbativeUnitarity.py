import logging
from tqdm.auto import tqdm
from numpy import pi, sqrt
from numpy.linalg import eig
from itertools import combinations_with_replacement
from anyBSM.anyModel import anyModel

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__doc__ = """
<div class="mermaid">
flowchart RL
    subgraph classes
    anyModel  --> anyPerturbativeUnitarity;
    end
    subgraph methods
    anyPerturbativeUnitarity --> eigSSSS
    end
</div>
"""

class anyPerturbativeUnitarity(anyModel):
    r""" Calculation of unitarity constraints

    Example
    ```python
    from anyBSM import anyPerturbativeUnitarity
    SM = anyPerturbativeUnitarity('SM')
    SM.eigSSSS() # returns largest SS->SS eigenvalue
    ```
    """

    def eigSSSS(self, ignore_scalars: list = [], parameters: dict = {}) -> float:
        """
           Args:
                ignore_scalars: list of scalars to be excluded from the scatter matrix
                parameters: optionally run `anyBSM.anyModel.setparameters(parameters)` so set input parameters
           Return:
               smallest scattering eigenvalue in the s->infinity limit
        """
        if self.evaluation != 'numerical':
            logger.error('Can only compute unitarity constraints in numerical evaluation mode at the moment. (run `set_evaluation_mode("numerical")` or `-e numerical`)')
            return
        if parameters:
            self.setparameters(params=parameters)
        scalars = [s for s in self.particles["S"] if s.color == 1 and s not in ignore_scalars and s.name not in ignore_scalars]
        scatteringpairs = set(combinations_with_replacement(scalars,2))
        logging.debug(f'Found {len(scatteringpairs)} scattering pairs.')
        smatrix = []
        for s1 in tqdm(scatteringpairs, desc = 'Calculating SS->SS scattering matrix in the high-energy limit',  disable = not self.progress, leave = False):
            row = []
            for s2 in tqdm(scatteringpairs, disable = not self.progress, leave = False):
                sym1 = sqrt(2) if s1[0] == s1[1] else 1
                sym2 = sqrt(2) if s2[0] == s2[1] else 1
                coup = self.getcoupling(s1[0],s1[1],s2[0],s2[1])
                coup = complex(0,-1)*coup['c'].nvalue/(sym1*sym2) if coup else 0.0
                coup = coup.real
                row.append(coup)
            smatrix.append(row)
        return max(abs(eig(smatrix)[0]))/(16*pi)
