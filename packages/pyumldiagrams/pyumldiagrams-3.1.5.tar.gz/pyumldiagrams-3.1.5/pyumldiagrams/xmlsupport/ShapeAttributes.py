
from logging import Logger
from logging import getLogger

from untangle import Element

from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size
from pyumldiagrams.xmlsupport import XmlConstants
from pyumldiagrams.xmlsupport.SafeConversions import SafeConversions


class ShapeAttributes(SafeConversions):
    def __init__(self):
        super().__init__()
        self.shapeLogger: Logger = getLogger(__name__)

    def _shapeSize(self, graphicElement: Element) -> Size:

        width:  int = self._stringToInteger(graphicElement[XmlConstants.ATTR_WIDTH_V11])
        height: int = self._stringToInteger(graphicElement[XmlConstants.ATTR_HEIGHT_V11])

        size: Size = Size(width=width, height=height)

        return size

    def _shapePosition(self, graphicElement: Element) -> Position:

        x: int = self._stringToInteger(graphicElement[XmlConstants.ATTR_X_V11])
        y: int = self._stringToInteger(graphicElement[XmlConstants.ATTR_Y_V11])

        position: Position = Position(x=x, y=y)

        return position
