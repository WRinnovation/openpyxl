from __future__ import absolute_import


#Autogenerated schema
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.descriptors import (
    Typed,
    Integer,
    Bool,
    Alias,
    Sequence,
)
from openpyxl.descriptors.excel import ExtensionList
from openpyxl.descriptors.nested import (
    NestedInteger,
    NestedBool,
)

from .axis import AxId
from .shapes import ShapeProperties
from .series import SurfaceSer


class BandFmt(Serialisable):

    idx = NestedInteger()
    spPr = Typed(expected_type=ShapeProperties, allow_none=True)

    __elements__ = ('idx', 'spPr')

    def __init__(self,
                 idx=None,
                 spPr=None,
                ):
        self.idx = idx
        self.spPr = spPr


class BandFmts(Serialisable):

    bandFmt = Typed(expected_type=BandFmt, allow_none=True)

    __elements__ = ('bandFmt',)

    def __init__(self,
                 bandFmt=None,
                ):
        self.bandFmt = bandFmt


class _SurfaceChartBase(Serialisable):

    wireframe = NestedBool(allow_none=True)
    ser = Typed(expected_type=SurfaceSer, allow_none=True)
    bandFmts = Typed(expected_type=BandFmts, allow_none=True)

    __elements__ = ('wireframe', 'ser', 'bandFmts')

    def __init__(self,
                 wireframe=None,
                 ser=None,
                 bandFmts=None,
                ):
        self.wireframe = wireframe
        self.ser = ser
        self.bandFmts = bandFmts


class SurfaceChart(_SurfaceChartBase):

    tagname = "surfaceChart"

    wireframe = _SurfaceChartBase.wireframe
    ser = _SurfaceChartBase.ser
    bandFmts = _SurfaceChartBase.bandFmts

    axId = Sequence(expected_type=AxId) # 2 or 3
    extLst = Typed(expected_type=ExtensionList, allow_none=True)

    __elements__ = _SurfaceChartBase.__elements__ + ('axId',)

    def __init__(self,
                 axId=None,
                 extLst=None,
                 **kw
                ):
        if axId is None:
            axId = [AxId(10), AxId(100)]
        self.axId = axId
        super(SurfaceChart, self).__init__(**kw)


class SurfaceChart3D(SurfaceChart):

    tagname = "surface3DChart"

    wireframe = _SurfaceChartBase.wireframe
    ser = _SurfaceChartBase.ser
    bandFmts = _SurfaceChartBase.bandFmts

    extLst = SurfaceChart.extLst

    axId = Sequence(expected_type=AxId) # must be 3 (cat, val, series)

    def __init__(self, axId, **kw):
        if axId is None:
            axId = [AxId(10), AxId(100), AxId(1000)]
        self.axId = axId
        super(SurfaceChart3D, self).__init__(**kw)
