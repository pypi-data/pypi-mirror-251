
from logging import Logger
from logging import getLogger
from typing import cast

from untangle import Element

from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import NamedAssociations
from pyumldiagrams.Internal import Elements

from pyumldiagrams.xmlsupport import XmlConstants

from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.xmlsupport.SafeConversions import SafeConversions


class UnTangleLineDefinition(SafeConversions):
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def untangle(self, linkElement: Element) -> UmlLineDefinition:

        linePositions: LinePositions = self._getLinePositions(linkElement=linkElement)

        pyutLinkElement: Element  = linkElement.PyutLink
        strType:         str      = pyutLinkElement[XmlConstants.ATTR_TYPE_V11]
        lineType:        LineType = LineType.toEnum(strType)

        umlLineDefinition: UmlLineDefinition = UmlLineDefinition(linePositions=linePositions, lineType=lineType)

        if lineType in NamedAssociations:

            nameStr: str = pyutLinkElement[XmlConstants.ATTR_NAME_V11]
            umlLineDefinition.name = nameStr

            umlLineDefinition.cardinalitySource      = pyutLinkElement[XmlConstants.ATTR_CARDINALITY_SOURCE_V11]
            umlLineDefinition.cardinalityDestination = pyutLinkElement[XmlConstants.ATTR_CARDINALITY_DESTINATION_V11]

            umlLineDefinition.namePosition                   = self._getNamePosition(linkElement=linkElement)
            umlLineDefinition.sourceCardinalityPosition      = self._getSourcePosition(linkElement=linkElement)
            umlLineDefinition.destinationCardinalityPosition = self._getDestinationPosition(linkElement=linkElement)

        elif lineType == LineType.NoteLink or lineType == LineType.Interface:
            nameStr = pyutLinkElement[XmlConstants.ATTR_NAME_V11]
            umlLineDefinition.name = nameStr

        return umlLineDefinition

    def _getLinePositions(self, linkElement: Element) -> LinePositions:

        srcPosition: Position = self._getStartPosition(linkElement=linkElement)

        linePositions:     LinePositions     = LinePositions([srcPosition])

        # Intermediate points
        controlPoints: Elements = linkElement.get_elements(XmlConstants.ELEMENT_CONTROL_POINT_V11)
        for point in controlPoints:
            controlPointElement: Element = cast(Element, point)

            self.logger.debug(f'{controlPointElement=}')
            x: int = self._stringToInteger(controlPointElement[XmlConstants.ATTR_X_V11])
            y: int = self._stringToInteger(controlPointElement[XmlConstants.ATTR_Y_V11])
            bendPosition: Position = Position(x=x, y=y)
            linePositions.append(bendPosition)

        # end of line
        destX: int = self._stringToInteger(linkElement[XmlConstants.ATTR_LINK_DESTINATION_ANCHOR_X_V11])
        destY: int = self._stringToInteger(linkElement[XmlConstants.ATTR_LINK_DESTINATION_ANCHOR_Y_V11])

        destPosition: Position = Position(x=destX, y=destY)

        linePositions.append(destPosition)

        return linePositions

    def _getStartPosition(self, linkElement: Element) -> Position:

        srcX: int = self._stringToInteger(linkElement[XmlConstants.ATTR_LINK_SOURCE_ANCHOR_X_V11])
        srcY: int = self._stringToInteger(linkElement[XmlConstants.ATTR_LINK_SOURCE_ANCHOR_Y_V11])

        srcPosition: Position = Position(x=srcX, y=srcY)

        return srcPosition

    def _getNamePosition(self, linkElement: Element) -> Position:
        return self._getLabelPosition(linkElement=linkElement, elementName=XmlConstants.ELEMENT_LABEL_CENTER_V11)

    def _getSourcePosition(self, linkElement: Element) -> Position:
        return self._getLabelPosition(linkElement=linkElement, elementName=XmlConstants.ELEMENT_LABEL_SOURCE_V11)

    def _getDestinationPosition(self, linkElement: Element) -> Position:
        return self._getLabelPosition(linkElement=linkElement, elementName=XmlConstants.ELEMENT_LABEL_DESTINATION_V11)

    def _getLabelPosition(self, linkElement: Element, elementName: str) -> Position:

        positionElements: Elements = linkElement.get_elements(elementName)

        assert len(positionElements) == 1, f'There can only be one ....  position element -- {elementName}'

        positionElement: Element = positionElements[0]

        x: int = self._stringToInteger(positionElement[XmlConstants.ATTR_X_V11])
        y: int = self._stringToInteger(positionElement[XmlConstants.ATTR_Y_V11])

        position: Position = Position(x=x, y=y)

        return position
