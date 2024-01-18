
from typing import Final
from typing import List
from typing import NewType
from typing import Tuple

from logging import Logger
from logging import getLogger
from typing import cast

from fpdf import FPDF

from pyumldiagrams.Common import Common

from pyumldiagrams.CommonAbsolute import CommonAbsolute

from pyumldiagrams.IDiagramLine import IDiagramLine

from pyumldiagrams.UnsupportedException import UnsupportedException

from pyumldiagrams.Internal import ArrowPoints
from pyumldiagrams.Internal import DiamondPoints
from pyumldiagrams.Internal import PolygonPoints
from pyumldiagrams.Internal import InternalPosition

from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import Position

from pyumldiagrams.Definitions import UmlLollipopDefinition


from pyumldiagrams.pdf.PdfCommon import PdfCommon
from pyumldiagrams.pdf.PdfLollipopInterface import PdfLollipopInterface


PDFCoordinate  = NewType('PDFCoordinate',  Tuple[int, int])
PDFCoordinates = NewType('PDFCoordinates', List[PDFCoordinate])


PolyPoint  = NewType('PolyPoint',  Tuple[int, int])
PolyPoints = NewType('PolyPoints', List[PolyPoint])


class PdfLine(IDiagramLine):
    """
    This class takes responsibility for drawing the various types of lines within the
    described UML classes.  End users generally do not directly use this class.
    It is split off as part of the separation of responsibility principle.
    """
    INHERITANCE_ARROW_HEIGHT: Final = 10
    DIAMOND_HEIGHT:           Final = 8

    DASH_LENGTH:     Final = 5.0
    DASH_GAP_LENGTH: Final = 7.0

    def __init__(self, pdf: FPDF, diagramPadding: DiagramPadding, dpi: int):

        super().__init__(docMaker=pdf, diagramPadding=diagramPadding, dpi=dpi)
        self.logger: Logger = getLogger(__name__)

        self._pdfLollipopInterface: PdfLollipopInterface = PdfLollipopInterface(pdf=pdf, dpi=dpi)
        self._pdfCommon:            PdfCommon            = PdfCommon(diagramPadding=diagramPadding,  dpi=dpi)

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
            self._drawInterface(lineDefinition=lineDefinition)
        elif lineType == LineType.NoteLink:
            self._drawNoteLink(lineDefinition=lineDefinition)
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def drawLollipopInterface(self, umlLollipopDefinition: UmlLollipopDefinition):

        self._pdfLollipopInterface.drawLollipopInterface(umlLollipopDefinition=umlLollipopDefinition)

    def _drawInheritance(self, linePositions: LinePositions):
        """
        Must account for the margins and gaps between drawn shapes
        Must convert to from screen noteCoordinates to point noteCoordinates
        Draw the arrow first
        Compute the mid-point of the bottom line of the arrow
        That is where the line ends

        Args:
            linePositions - The points that describe the line
        """
        points:  ArrowPoints = self._drawArrowAtDestination(linePositions)

        self._drawLineSourceToDestination(linePositions, points)

    def _drawInterface(self, lineDefinition: UmlLineDefinition):

        points:  ArrowPoints = self._drawArrowAtDestination(lineDefinition.linePositions)

        self._drawLineSourceToDestination(lineDefinition.linePositions, points, dashedLine=True)

    def _drawCompositeAggregation(self, lineDefinition: UmlLineDefinition):
        """
        Composition

        Args:
            lineDefinition:
        """
        self._drawAggregation(lineDefinition=lineDefinition, isComposite=True)

    def _drawSharedAggregation(self, lineDefinition: UmlLineDefinition):
        """
        Aggregation

        Args:
            lineDefinition:
        """
        self._drawAggregation(lineDefinition=lineDefinition, isComposite=False)

    def _drawAssociation(self, lineDefinition: UmlLineDefinition):

        pdf:           FPDF          = self._docMaker
        linePositions: LinePositions = lineDefinition.linePositions

        polyPoints: PolyPoints = self._toPolyPoints(linePositions=linePositions)

        pdf.polyline(polyPoints, style='D')

        self._drawAssociationName(lineDefinition=lineDefinition)
        self._drawSourceCardinality(lineDefinition=lineDefinition)
        self._drawDestinationCardinality(lineDefinition=lineDefinition)

    def _drawNoteLink(self, lineDefinition: UmlLineDefinition):

        pdf:           FPDF          = self._docMaker
        linePositions: LinePositions = lineDefinition.linePositions
        polyPoints:    PolyPoints = self._toPolyPoints(linePositions=linePositions)

        with pdf.local_context():
            pdf.set_dash_pattern(dash=PdfLine.DASH_LENGTH, gap=PdfLine.DASH_GAP_LENGTH)
            pdf.polyline(polyPoints, style='D')

    def _drawAggregation(self, lineDefinition: UmlLineDefinition, isComposite: bool):

        linePositions: LinePositions = lineDefinition.linePositions

        startPoints: Tuple[InternalPosition, InternalPosition] = self._convertPoints(linePositions[0], linePositions[1])

        convertedSrc: InternalPosition = startPoints[0]
        convertedDst: InternalPosition = startPoints[1]

        points: DiamondPoints = Common.computeDiamondVertices(position0=convertedSrc, position1=convertedDst)
        self._drawDiamond(diamondPoints=points, isComposite=isComposite)

        newEndStartPoint: InternalPosition = points[3]

        self._finishDrawingLine(linePositions=linePositions, newStartPoint=newEndStartPoint)

        self._drawAssociationName(lineDefinition=lineDefinition)
        self._drawSourceCardinality(lineDefinition=lineDefinition)
        self._drawDestinationCardinality(lineDefinition=lineDefinition)

    def _drawDiamond(self, diamondPoints: DiamondPoints, isComposite: bool):

        pdfCoordinates: PDFCoordinates = self._toPDFCoordinates(polygonPoints=diamondPoints)
        pdf:            FPDF           = self._docMaker

        if isComposite is True:
            pdf.polygon(pdfCoordinates, style='DF')
        else:
            pdf.polygon(pdfCoordinates, style='D')

    def _drawAssociationName(self, lineDefinition: UmlLineDefinition):

        pdf: FPDF = self._docMaker

        iPos: InternalPosition = self._computeTextPosition(lineDefinition=lineDefinition, labelPosition=lineDefinition.namePosition)
        pdf.text(x=iPos.x, y=iPos.y, txt=lineDefinition.name)

    def _drawSourceCardinality(self, lineDefinition: UmlLineDefinition):

        pdf: FPDF = self._docMaker

        iPos: InternalPosition = self._computeTextPosition(lineDefinition=lineDefinition, labelPosition=lineDefinition.sourceCardinalityPosition)

        pdf.text(x=iPos.x, y=iPos.y, txt=lineDefinition.cardinalitySource)

    def _drawDestinationCardinality(self, lineDefinition: UmlLineDefinition):

        pdf: FPDF = self._docMaker

        iPos: InternalPosition = self._computeTextPosition(lineDefinition=lineDefinition, labelPosition=lineDefinition.destinationCardinalityPosition)

        pdf.text(x=iPos.x, y=iPos.y, txt=lineDefinition.cardinalityDestination)

    def _drawLineSourceToDestination(self, linePositions: LinePositions, points: ArrowPoints, dashedLine: bool = False):

        pdf: FPDF = self._docMaker

        newEndPosition:    InternalPosition = Common.computeMidPointOfBottomLine(points[0], points[2])
        adjustedPositions: LinePositions    = LinePositions(linePositions[:-1])

        with pdf.local_context():
            if dashedLine is True:
                pdf.set_dash_pattern(dash=PdfLine.DASH_LENGTH, gap=PdfLine.DASH_GAP_LENGTH)

            polyPoints:   PolyPoints = self._toPolyPoints(linePositions=adjustedPositions)
            endPolyPoint: PolyPoint  = PolyPoint((newEndPosition.x, newEndPosition.y))

            polyPoints.append(endPolyPoint)

            pdf.polyline(polyPoints, style='D')

    def _drawArrowAtDestination(self, linePositions: LinePositions) -> ArrowPoints:
        """

        Args:
            linePositions:  The line positions

        Returns:    The points used to draw the arrow
        """

        internalPosition0: InternalPosition = self._pdfCommon.toInternal(linePositions[-1])  # last position
        internalPosition1: InternalPosition = self._pdfCommon.toInternal(linePositions[-2])  # next to last position

        points:         ArrowPoints    = Common.computeTheArrowVertices(position0=internalPosition0, position1=internalPosition1)
        pdfCoordinates: PDFCoordinates = self._toPDFCoordinates(polygonPoints=points)

        self._docMaker.polygon(pdfCoordinates, style='D')

        return points

    def _computeTextPosition(self, lineDefinition: UmlLineDefinition, labelPosition: Position) -> InternalPosition:

        xy: Tuple[int, int] = CommonAbsolute.computeAbsoluteLabelPosition(srcPosition=lineDefinition.linePositions[0],
                                                                          dstPosition=lineDefinition.linePositions[-1],
                                                                          labelPosition=labelPosition)

        iPos: InternalPosition = self._pdfCommon.toInternal(position=Position(x=xy[0], y=xy[1]))

        return iPos

    def _toPDFCoordinates(self, polygonPoints: PolygonPoints) -> PDFCoordinates:

        pdfCoordinates: PDFCoordinates = PDFCoordinates([])

        for dPoint in polygonPoints:
            diamondPoint: InternalPosition = cast(InternalPosition, dPoint)
            pdfTuple:     PDFCoordinate    = PDFCoordinate((diamondPoint.x, diamondPoint.y))
            pdfCoordinates.append(pdfTuple)

        return pdfCoordinates

    def _finishDrawingLine(self, linePositions: LinePositions, newStartPoint: InternalPosition):
        """
        Finishes drawing the line for aggregation/composition where the diamond is at the source;  Thus,
        the new start position at a diamond tip

        Args:
            linePositions:
            newStartPoint:
        """

        linePositionsCopy: LinePositions = LinePositions(linePositions[1:])    # Makes a copy; remove first one
        pdf:               FPDF          = self._docMaker

        currentPos:          Position         = linePositionsCopy[0]
        convertedCurrentPos: InternalPosition = self._pdfCommon.toInternal(position=currentPos)
        pdf.line(x1=newStartPoint.x, y1=newStartPoint.y, x2=convertedCurrentPos.x, y2=convertedCurrentPos.y)

        polyPoints: PolyPoints = self._toPolyPoints(linePositions=linePositionsCopy)
        pdf.polyline(polyPoints, style='D')

    def _convertPoints(self, src: Position, dst: Position) -> Tuple[InternalPosition, InternalPosition]:

        convertedSrc: InternalPosition = self._pdfCommon.toInternal(position=src)
        convertedDst: InternalPosition = self._pdfCommon.toInternal(position=dst)

        return convertedSrc, convertedDst

    def _toPolyPoints(self, linePositions: LinePositions) -> PolyPoints:
        """
        Takes the raw positions and creates the poly points associated with our adjusted internal positions.
        Args:
            linePositions:

        Returns:  PDF style internal points
        """

        polyPoints: PolyPoints = PolyPoints([])

        for position in linePositions:
            lastInternal: InternalPosition = self._pdfCommon.toInternal(position)

            polyPoint: PolyPoint = PolyPoint((lastInternal.x, lastInternal.y))
            polyPoints.append(polyPoint)

        return polyPoints
