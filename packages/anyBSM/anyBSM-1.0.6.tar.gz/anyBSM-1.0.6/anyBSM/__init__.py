from .anyBSM import anyBSM
from .anyModel import anyModel
from .anyProcess import anyProcess
from .anyEWPO import anyEWPO
from .anyH3 import anyH3
from .anyPerturbativeUnitarity import anyPerturbativeUnitarity

__doc__ = r""" The anyBSM library

This is the anyBSM python package.  
The library is organized in various (sub)modules which define physics obserables (and helper-classes), such as e.g. `anyBSM.anyH3`.
The module `anyBSM.anyBSM` inherits from those modules and makes all observables accessible within one class:
```python
from anyBSM import anyBSM
SM = anyBSM('SM')
# this object can call functions from all sub-modules
SM.lambdahhh() # defined in the `anyBSM.anyH3`-module
SM.eigSSSS() # defined in the `anyBSM.anyPerturbativeUnitarity`-module
SM.getcoupling('h','Z','Z') # defined in the root module `anyBSM.anyModel`
```
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
</div>
"""
