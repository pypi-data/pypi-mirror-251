
from dataclasses import dataclass
from dataclasses import field

from pyumldiagrams.Common import Common
from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import Position

from pyumldiagrams.Defaults import LEFT_MARGIN
from pyumldiagrams.Defaults import TOP_MARGIN
from pyumldiagrams.Internal import InternalPosition


@dataclass
class Coordinates:
    x: int = 0
    y: int = 0


def createCoordinatesFactory() -> Coordinates:
    return Coordinates()


@dataclass
class Dimensions:
    width:  int = 0
    height: int = 0


def createDimensionsFactory() -> Dimensions:
    return Dimensions()


@dataclass
class PdfShapeDefinition:
    coordinates: Coordinates = field(default_factory=createCoordinatesFactory)
    dimensions:  Dimensions  = field(default_factory=createDimensionsFactory)


class PdfCommon(Common):

    def __init__(self, diagramPadding: DiagramPadding, dpi: int):

        self._diagramPadding: DiagramPadding = diagramPadding
        self._dpi:            int            = dpi

    @classmethod
    def toPdfPoints(cls, pixelNumber: float, dpi: int) -> int:
        """

        points = pixels * 72 / DPI

        Args:
            pixelNumber:  From the display
            dpi:  dots per inch of source display

        Returns:  A pdf point value to use to position on a generated document

        """
        points: int = int((pixelNumber * 72)) // dpi

        return points

    @classmethod
    def convertPosition(cls, pos: Position, dpi: int, verticalGap: int, horizontalGap: int) -> Coordinates:

        x: int = PdfCommon.toPdfPoints(pos.x, dpi) + LEFT_MARGIN + verticalGap
        y: int = PdfCommon.toPdfPoints(pos.y, dpi) + TOP_MARGIN  + horizontalGap

        return Coordinates(x=x, y=y)

    def toInternal(self, position: Position) -> InternalPosition:

        verticalGap:   int = self._diagramPadding.verticalGap
        horizontalGap: int = self._diagramPadding.horizontalGap

        coordinates: Coordinates = PdfCommon.convertPosition(pos=position, dpi=self._dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)

        internalPosition: InternalPosition = InternalPosition(coordinates.x, coordinates.y)

        return internalPosition
