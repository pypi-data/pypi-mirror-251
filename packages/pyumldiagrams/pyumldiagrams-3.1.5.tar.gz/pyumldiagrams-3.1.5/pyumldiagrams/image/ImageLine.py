
from typing import Any
from typing import List
from typing import NewType
from typing import Tuple
from typing import Union
from typing import Final

from logging import Logger
from logging import getLogger

from os import sep as osSep

from PIL import ImageDraw
from PIL import ImageFont

from codeallybasic.ResourceManager import ResourceManager

from pyumldiagrams.BaseDiagram import BaseDiagram
from pyumldiagrams.Common import Common
from pyumldiagrams.CommonAbsolute import CommonAbsolute
from pyumldiagrams.IDiagramLine import IDiagramLine
from pyumldiagrams.UnsupportedException import UnsupportedException

from pyumldiagrams.image.ImageCommon import ImageCommon

from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import LinePositions

from pyumldiagrams.Internal import ArrowPoints
from pyumldiagrams.Internal import DiamondPoints
from pyumldiagrams.Internal import InternalPosition

PILPoints     = NewType('PILPoints',     List[int])         # Maybe these go
PolygonPoints = NewType('PolygonPoints', List[int])         # in Internal


class ImageLine(IDiagramLine):

    DEFAULT_LINE_COLOR: Final = 'Black'
    DEFAULT_TEXT_COLOR: Final = 'Black'

    LINE_WIDTH:         Final = 1

    RESOURCES_PACKAGE_NAME: Final = 'pyumldiagrams.image.resources'
    RESOURCES_PATH:         Final = f'pyumldiagrams{osSep}image{osSep}resources'

    def __init__(self, docWriter: Any, diagramPadding: DiagramPadding):

        super().__init__(docMaker=docWriter, diagramPadding=diagramPadding, dpi=0)

        self.logger: Logger = getLogger(__name__)

        self._imgDraw: ImageDraw = docWriter

        # noinspection SpellCheckingInspection
        fqPath:     str       = self._retrieveResourcePath('MonoFonto.ttf')
        self._font: ImageFont = ImageFont.truetype(font=fqPath, size=BaseDiagram.DEFAULT_FONT_SIZE)

    def draw(self, lineDefinition: UmlLineDefinition):
        """
        Draw the line described by the input parameter

        Args:
            lineDefinition:  Describes the line to draw
        """
        linePositions: LinePositions = lineDefinition.linePositions
        lineType:      LineType      = lineDefinition.lineType

        if lineType == LineType.Inheritance:
            self._drawInheritance(linePositions=linePositions)
        elif lineType == LineType.Composition:
            self._drawCompositeAggregation(lineDefinition=lineDefinition)
        elif lineType == LineType.Aggregation:
            self._drawSharedAggregation(lineDefinition=lineDefinition)
        elif lineType == LineType.Association:
            self._drawAssociation(lineDefinition=lineDefinition)
        elif lineType == LineType.Interface:
            pass        # TODO
        elif lineType == LineType.NoteLink:
            pass        # TODO
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def _drawInheritance(self, linePositions: LinePositions):
        """
        Must account for the margins and gaps between drawn shapes
        Must convert from screen coordinates to point coordinates
        Draw the arrow first
        Compute the mid-point of the bottom line of the arrow
        That is where the line ends

        Args:
            linePositions  The points that describe the line
        """
        internalPosition0:  InternalPosition = self._toInternal(linePositions[-1])
        internalPosition1:  InternalPosition = self._toInternal(linePositions[-2])

        points:  ArrowPoints   = Common.computeTheArrowVertices(position0=internalPosition0, position1=internalPosition1)
        polygon: PolygonPoints = self._toPolygonPoints(points)

        self._imgDraw.polygon(xy=polygon, outline=ImageLine.DEFAULT_LINE_COLOR)

        newEndPoint: InternalPosition = Common.computeMidPointOfBottomLine(points[0], points[2])

        xy: PILPoints = PILPoints([])

        adjustedPositions: LinePositions = LinePositions(linePositions[:-1])
        for externalPosition in adjustedPositions:
            internalPosition: InternalPosition = self._toInternal(externalPosition)
            xy.append(internalPosition.x)
            xy.append(internalPosition.y)
        xy.append(newEndPoint.x)
        xy.append(newEndPoint.y)

        self._imgDraw.line(xy=xy, fill=ImageLine.DEFAULT_LINE_COLOR, width=ImageLine.LINE_WIDTH)

    def _drawCompositeAggregation(self, lineDefinition: UmlLineDefinition):
        """
        Composition
        Draws both the line and the solid diamond

        Args:
            lineDefinition:   The line definition
        """
        self._drawAggregation(lineDefinition=lineDefinition, isComposite=True)

    def _drawSharedAggregation(self, lineDefinition: UmlLineDefinition):
        """
        Aggregation
        Draws both the line and the hollow diamond

        Args:
            lineDefinition:   The line definition
        """
        self._drawAggregation(lineDefinition=lineDefinition, isComposite=False)

    def _drawAggregation(self, lineDefinition: UmlLineDefinition, isComposite: bool):
        """

        Args:
            lineDefinition: The UML line definitions
            isComposite:    'True' draws solid composition diamond;  'False' draws hollow aggregation diamond
        """
        linePositions: LinePositions = lineDefinition.linePositions

        internalPosition0:  InternalPosition = self._toInternal(linePositions[0])
        internalPosition1:  InternalPosition = self._toInternal(linePositions[1])

        points:  DiamondPoints = Common.computeDiamondVertices(position1=internalPosition1, position0=internalPosition0)
        polygon: PolygonPoints = self._toPolygonPoints(points)

        if isComposite is True:
            self._imgDraw.polygon(xy=polygon, outline=ImageLine.DEFAULT_LINE_COLOR, fill='black')
        else:
            self._imgDraw.polygon(xy=polygon, outline=ImageLine.DEFAULT_LINE_COLOR)

        newStartPoint: InternalPosition = points[3]
        xy:            PILPoints        = self._toPILPoints(linePositions=linePositions, newStartPoint=newStartPoint)

        self._imgDraw.line(xy=xy, fill=ImageLine.DEFAULT_LINE_COLOR, width=ImageLine.LINE_WIDTH)

        self._drawAssociationName(lineDefinition=lineDefinition)
        self._drawSourceCardinality(lineDefinition=lineDefinition)
        self._drawDestinationCardinality(lineDefinition=lineDefinition)

    def _drawAssociation(self, lineDefinition: UmlLineDefinition):

        linePositions: LinePositions = lineDefinition.linePositions
        xy:            PILPoints     = PILPoints([])

        for externalPosition in linePositions:
            internalPosition: InternalPosition = self._toInternal(externalPosition)
            xy.append(internalPosition.x)
            xy.append(internalPosition.y)

        self._imgDraw.line(xy=xy, fill=ImageLine.DEFAULT_LINE_COLOR, width=ImageLine.LINE_WIDTH)

        self._drawAssociationName(lineDefinition=lineDefinition)
        self._drawSourceCardinality(lineDefinition=lineDefinition)
        self._drawDestinationCardinality(lineDefinition=lineDefinition)

    def _drawAssociationName(self, lineDefinition: UmlLineDefinition):

        iPos: InternalPosition = self._computeTextPosition(lineDefinition=lineDefinition, labelPosition=lineDefinition.namePosition)

        self._imgDraw.text(xy=(iPos.x, iPos.y), fill=ImageLine.DEFAULT_TEXT_COLOR, font=self._font, text=lineDefinition.name)

    def _drawSourceCardinality(self, lineDefinition: UmlLineDefinition):

        iPos: InternalPosition = self._computeTextPosition(lineDefinition=lineDefinition, labelPosition=lineDefinition.sourceCardinalityPosition)

        self._imgDraw.text(xy=(iPos.x, iPos.y), fill=ImageLine.DEFAULT_TEXT_COLOR, font=self._font, text=lineDefinition.cardinalitySource)

    def _drawDestinationCardinality(self, lineDefinition: UmlLineDefinition):

        iPos: InternalPosition = self._computeTextPosition(lineDefinition=lineDefinition, labelPosition=lineDefinition.destinationCardinalityPosition)

        self._imgDraw.text(xy=(iPos.x, iPos.y), fill=ImageLine.DEFAULT_TEXT_COLOR, font=self._font, text=lineDefinition.cardinalityDestination)

    def _computeTextPosition(self, lineDefinition: UmlLineDefinition, labelPosition: Position) -> InternalPosition:

        xy: Tuple[int, int] = CommonAbsolute.computeAbsoluteLabelPosition(srcPosition=lineDefinition.linePositions[0],
                                                                          dstPosition=lineDefinition.linePositions[-1],
                                                                          labelPosition=labelPosition)

        iPos: InternalPosition = self._toInternal(position=Position(x=xy[0], y=xy[1]))

        return iPos

    def _retrieveResourcePath(self, bareFileName: str) -> str:

        fqFileName: str = ResourceManager.retrieveResourcePath(bareFileName=bareFileName,
                                                               resourcePath=ImageLine.RESOURCES_PATH,
                                                               packageName=ImageLine.RESOURCES_PACKAGE_NAME)

        return fqFileName

    def _toInternal(self, position: Position) -> InternalPosition:

        verticalGap:   int = self._diagramPadding.verticalGap
        horizontalGap: int = self._diagramPadding.horizontalGap

        iPos: InternalPosition = ImageCommon.toInternal(position, verticalGap=verticalGap, horizontalGap=horizontalGap)

        return iPos

    def _toPolygonPoints(self, points: Union[ArrowPoints, DiamondPoints]) -> PolygonPoints:

        polygon: PolygonPoints = PolygonPoints([])

        for point in points:
            polygon.append(int(point.x))
            polygon.append(int(point.y))

        return polygon

    def _toPILPoints(self, linePositions: LinePositions, newStartPoint: InternalPosition) -> PILPoints:

        linePositionsCopy: LinePositions = LinePositions(linePositions[1:])  # Makes a copy; remove old start point

        xy: PILPoints = PILPoints([])

        xy.append(newStartPoint.x)
        xy.append(newStartPoint.y)
        for externalPosition in linePositionsCopy:
            internalPosition: InternalPosition = self._toInternal(externalPosition)
            xy.append(internalPosition.x)
            xy.append(internalPosition.y)

        return xy
