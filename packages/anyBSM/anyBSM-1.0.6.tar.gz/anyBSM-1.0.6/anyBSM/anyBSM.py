from __future__ import division
import logging
from anyBSM.anyModel import anyModel
from anyBSM.anyH3 import anyH3
from anyBSM.anyEWPO import anyEWPO
from anyBSM.anyPerturbativeUnitarity import anyPerturbativeUnitarity

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
__doc__ = """
<div class="mermaid">
flowchart RL

  subgraph user[main classes]
    direction TB
    anyModel --> anyProcess
    anyProcess --> anyH3
    anyProcess --> anyEWPO
    anyProcess --> ...
    anyH3 --> anyBSM
    ... --> anyBSM
  end
  subgraph internal[internal modules]
    direction TB
    A[topologies<br>diagrams<br>loopfunctions]
  end
  subgraph external[external optional modules]
    direction TB
    pyCollier
  end
  internal --- user
  external --- user
</div>"""
class anyBSM(anyEWPO, anyH3, anyPerturbativeUnitarity):
    """ Wrapper class which inherits from all available classes that define physics obserables.
    Example:
    ```python
    from anyBSM import anyBSM
    SM = anyBSM('SM', scheme_name = 'OS')
    # all methods from all observables are available such as:
    SM.lambdahhh() # the trilinear coupling (from anyBSM.anyH3)
    SM.MW() # the W-mass (from anyBSM.anyEWPO)
    ```
    For more information on how two initialize a model see anyBSM.anyModel or consult the online documentation.
    """
    def __init__(self, *args, **kwargs):
        """ Takes the same arguments as anyBSM.anyModel.anyModel.__init__ """
        anyModel.__init__(self, *args, **kwargs)
