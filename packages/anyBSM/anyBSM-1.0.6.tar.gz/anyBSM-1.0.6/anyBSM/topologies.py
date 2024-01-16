#!/bin/python
from __future__ import division
from collections import defaultdict
import logging

logger = logging.getLogger('anyBSM.topologies')

__doc__ = """ # AnyTopology
A module defining all generic topologies.\n
A topology consists of an ordered list of vertices.
Each vertex consists of an ordered list of fields.
Each field is a generic object that can be an internal/external/loop-field as well as a anti-field.\n

The pre-defined topologies are stored in anyBSM.topologies.TOPOLOGIES:
```yml
TOPOLOGIES = {
    <number of external fields> : {
        <topology name> : <topology object>,
        ...
        }
        ...
    }
```
e.g. TOPOLOGIES[2]['TwoPointB'] contains the B0-type self-energy
topology.

The topologies are populated with fields of a given UFO model in
`anyBSM.anyBSM.insert_fields()`.
"""

TOPOLOGIES = defaultdict(dict)
""" Global variable used to store topologies """


class Field():
    """ Representation of generic field """
    def __init__(self, label, insertion = None, anti = False):
        self.label = label
        self.insertion = None
        self.antifield = anti

class InternalField(Field):
    pass

class LoopField(Field):
    pass

class ExternalField(Field):
    pass

class Vertex():
    """ Representation of generic vertex """
    def __init__(self, *fields):
        self.fields = list(fields)

    def setinsertion(self, fields):
        for f in self.fields:
            fieldtoinsert = fields.get(f.label, None)
            if not fieldtoinsert:
                continue
            if fieldtoinsert.__class__.__name__ != 'Particle':
                logger.error('Can only insert `Particle` instances into Topology(), not {} ({})'.format(fieldtoinsert, fieldtoinsert.__class__.__name__))
                return
            f.insertion = fieldtoinsert
            if f.antifield:
                f.insertion = f.insertion.anti()

    def getinsertion(self):
        return [f.insertion for f in self.fields]

class VertexCT(Vertex):
    pass

def isexternal(field):
    return type(field) == ExternalField
def isinternal(field):
    return type(field) in [InternalField, LoopField]
def isloop(field):
    return type(field) == LoopField


class Topology():
    """ Representation of generic one-loop topology """
    def __init__(self, name, *vertices, symmetryfactor = 1, tadpole = False, wfr = False):
        self.vertices = vertices
        self.extfields = {} # OrderedDict()
        self.intfields = {} # OrderedDict()
        self.loopfields = {} # OrderedDict()
        self.Amplitude = name
        self.symmetryfactor = symmetryfactor
        self.tadpole = tadpole
        self.wfr = wfr
        allfields = [field for v in vertices for field in v.fields]
        for field in allfields:
            if isexternal(field):
                self.extfields.update({field.label: field})
            if isinternal(field):
                self.intfields.update({field.label: field})
                if any([ f.label == field.label and f.antifield != field.antifield for f in allfields]):
                    self.loopfields.update({field.label: field})

        self.next = len(self.extfields)
        self.nint = len(self.intfields)
        self.nloop = len(self.loopfields)

        TOPOLOGIES[self.next].update({name : self})

    def getinsertion(self):
        return [v.getinsertion() for v in self.vertices]

    def insertexternal(self, *fields):
        assert len(fields) == self.next
        for v in self.vertices:
            v.setinsertion({label:field for label,field in zip(self.extfields.keys(), fields)})

    def insertinternal(self, *fields):
        assert len(fields) == self.nint
        for v in self.vertices:
            v.setinsertion({label:field for label,field in zip(self.intfields.keys(), fields)})

"""
Define all possible one-loop topologies
"""
# 1-point
Topology(
        'OnePointA',
        Vertex(ExternalField(0),LoopField(1),LoopField(1,anti=True)),
)
# 1-point CT-inserted diagram:
# Tadpoles always MSbar -> no need for tadpole-CT diagrams, but have them here in comments
# Topology(
#         'OnePointCT',
#         VertexCT(LoopField(0)),
# )
# 2-point
Topology(
        'TwoPointA',
        Vertex(ExternalField(0), LoopField(1), LoopField(1,anti=True), ExternalField(2)),
)
Topology(
        'TwoPointB',
        Vertex(ExternalField(0),LoopField(1),LoopField(2,anti=True)),
        Vertex(ExternalField(3,anti=True), LoopField(1),LoopField(2,anti=True)),
)
Topology(
        'TwoPointTA', # tadpole contribution to selfenergy
        Vertex(ExternalField(0),InternalField(1,anti=True),ExternalField(2)),
        Vertex(InternalField(1),LoopField(3,anti=True),LoopField(3)),
        tadpole = 1
)
# 2-point CT-inserted diagrams
# Topology( # mass CT contribution
#         'TwoPointCT',
#         Vertex(ExternalField(0),ExternalField(1,anti=True)),
# )
# Topology(
#         'TwoPointTCT', # tadpole CT contribution
#         Vertex(ExternalField(0),InternalField(1),ExternalField(2)),
#         VertexCT(InternalField(1)),
#         tadpole = 1
# )

# 3-point
Topology(
        'ThreePointTree',
        Vertex(ExternalField(0),ExternalField(1),ExternalField(2)),
)
Topology(
        'ThreePointB', # bubble diagram
        Vertex(ExternalField(0),LoopField(3,anti=True),LoopField(4)),
        Vertex(ExternalField(1),ExternalField(2),LoopField(4,anti=True),LoopField(3)),
)
Topology(
        'ThreePointC', # triangle diagram
        Vertex(ExternalField(0),LoopField(3),LoopField(5, anti=True)),
        Vertex(ExternalField(1),LoopField(4),LoopField(3, anti=True)),
        Vertex(ExternalField(2),LoopField(5),LoopField(4, anti=True)),
)
Topology(
        'ThreePointTA', # 4-point vertex where one leg is a attached to a tadpole
        Vertex(ExternalField(0),InternalField(1,anti=True),ExternalField(2),ExternalField(3)),
        Vertex(InternalField(1),LoopField(4,anti=True),LoopField(4)),
        tadpole = 1
)
Topology(
        'ThreePointWFRA', # external leg with A-bubble
        Vertex(ExternalField(0),InternalField(1,anti=True),ExternalField(2)),
        Vertex(InternalField(1),LoopField(3,anti=True),LoopField(3),ExternalField(4)),
        wfr = True
)
Topology(
        'ThreePointWFRB', # external leg with B-bubble
        Vertex(ExternalField(0),InternalField(1,anti=True),ExternalField(2)),
        Vertex(InternalField(1,anti=True),LoopField(3),LoopField(4,anti=True)),
        Vertex(ExternalField(5),LoopField(3),LoopField(4,anti=True)),
        wfr = True
)
Topology(
        'ThreePointWFRT', # external leg with Tadpole
        Vertex(ExternalField(0),ExternalField(1),InternalField(3,anti=True)),
        Vertex(ExternalField(2),InternalField(3),InternalField(4)),
        Vertex(InternalField(4),LoopField(5),LoopField(5,anti=True)),
        wfr = True,
        tadpole = 4
)
# 3-point CT-inserted diagrams
# Topology(
#         'ThreePointCT', # Vertex CT
#         VertexCT(ExternalField(0),ExternalField(1),ExternalField(2)),
# )
# Topology(
#         'ThreePointMCT', # mass CT on external leg
#         Vertex(ExternalField(0),InternalField(1,anti=True),ExternalField(2)),
#         VertexCT(InternalField(1),ExternalField(3)),
#         wfr = True
# )
# Topology(
#         'ThreePointTCT', # tadpole CT on 4-vertex leg
#         Vertex(ExternalField(0),InternalField(1,anti=True),ExternalField(2),ExternalField(3)),
#         VertexCT(InternalField(1)),
#         tadpole = 1
# )
# Topology(
#         'ThreePointWTCT', # external leg with tadpole CT
#         Vertex(ExternalField(0),InternalField(1,anti=True),ExternalField(2)),
#         Vertex(InternalField(1),InternalField(3, anti=True),ExternalField(4)),
#         VertexCT(InternalField(3)),
#         wfr = True,
#         tadpole = 1
# )
