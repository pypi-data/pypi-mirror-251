
from typing import Final
from typing import Tuple

from logging import Logger
from logging import getLogger

from fpdf import FPDF

from codeallybasic.Position import Position

from codeallyadvanced.ui.AttachmentSide import AttachmentSide

from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import RenderStyle
from pyumldiagrams.Definitions import UmlLollipopDefinition

from pyumldiagrams.Internal import InternalPosition
from pyumldiagrams.pdf.PdfCommon import PdfCommon

LOLLIPOP_LINE_LENGTH:   Final = 60
LOLLIPOP_CIRCLE_HEIGHT: Final = 8
LOLLIPOP_CIRCLE_WIDTH:  Final = 8

LOLLIPOP_WIDTH_SQUARED: int = (LOLLIPOP_CIRCLE_WIDTH * LOLLIPOP_CIRCLE_WIDTH)
LOLLIPOP_CIRCLE_RADIUS: int = (LOLLIPOP_CIRCLE_HEIGHT // 2) + (LOLLIPOP_WIDTH_SQUARED // (8 * LOLLIPOP_CIRCLE_HEIGHT))

ADJUST_AWAY_FROM_IMPLEMENTOR: Final = 10


class PdfLollipopInterface:

    def __init__(self, pdf: FPDF, dpi: int):

        self.logger: Logger = getLogger(__name__)

        self._pdf: FPDF = pdf
        self._pdfCommon: PdfCommon = PdfCommon(diagramPadding=DiagramPadding(), dpi=dpi)

    def drawLollipopInterface(self, umlLollipopDefinition: UmlLollipopDefinition):

        position: Position = umlLollipopDefinition.position
        xSrc:     int      = position.x
        ySrc:     int      = position.y

        attachmentSide: AttachmentSide = umlLollipopDefinition.attachmentSide

        circleX, circleY, xDest, yDest = self._calculateWhereToDrawLollipop(attachmentSide, xSrc, ySrc)

        self._createTheInterfaceLine(position=position, xDest=xDest, yDest=yDest)
        self._drawTheTootsiePopCircle(attachmentSide=attachmentSide, circleX=circleX, circleY=circleY)
        self._drawInterfaceName(interfaceName=umlLollipopDefinition.name, attachmentSide=attachmentSide, xSrc=xSrc, ySrc=ySrc)

    def _calculateWhereToDrawLollipop(self, attachmentSide: AttachmentSide, xSrc, ySrc):
        """

        Args:
            attachmentSide:
            xSrc:
            ySrc:

        Returns:  A tuple that is the x,y position of the circle and the end
        of the line
        """

        self.logger.debug(f'({xSrc},{ySrc}) {LOLLIPOP_LINE_LENGTH=}')

        if attachmentSide == AttachmentSide.EAST:
            xDest:   int = int(xSrc + LOLLIPOP_LINE_LENGTH)
            yDest:   int = int(ySrc)
            circleX: int = int(xSrc + LOLLIPOP_LINE_LENGTH)
            circleY: int = int(ySrc)
        elif attachmentSide == AttachmentSide.WEST:
            xDest   = int(xSrc - LOLLIPOP_LINE_LENGTH)
            yDest   = int(ySrc)
            circleX = int(xSrc - LOLLIPOP_LINE_LENGTH)
            circleY = int(ySrc)
        elif attachmentSide == AttachmentSide.NORTH:
            xDest   = int(xSrc)
            yDest   = int(ySrc - LOLLIPOP_LINE_LENGTH)
            circleX = int(xSrc)
            circleY = int(ySrc - LOLLIPOP_LINE_LENGTH)
        else:  # it is South
            xDest   = int(xSrc)
            yDest   = int(ySrc + LOLLIPOP_LINE_LENGTH)
            circleX = int(xSrc)
            circleY = int(ySrc + LOLLIPOP_LINE_LENGTH)

        return circleX, circleY, xDest, yDest

    def _createTheInterfaceLine(self, position: Position, xDest: int, yDest: int):

        internalDest: InternalPosition = self._pdfCommon.toInternal(position=Position(x=xDest, y=yDest))
        internalSrc:  InternalPosition = self._pdfCommon.toInternal(position=position)
        self._pdf.line(x1=internalSrc.x, y1=internalSrc.y, x2=internalDest.x, y2=internalDest.y)

    def _drawTheTootsiePopCircle(self, attachmentSide: AttachmentSide, circleX: int, circleY: int):

        adjustedX, adjustedY = self._adjustXYForCircle(attachmentSide=attachmentSide, x=circleX, y=circleY)

        internalAdjusted: InternalPosition = self._pdfCommon.toInternal(Position(x=adjustedX, y=adjustedY))
        self._pdf.ellipse(x=internalAdjusted.x, y=internalAdjusted.y,
                          w=LOLLIPOP_CIRCLE_WIDTH, h=LOLLIPOP_CIRCLE_HEIGHT,
                          style=RenderStyle.Draw.value)

    def _drawInterfaceName(self, interfaceName: str, attachmentSide: AttachmentSide, xSrc: int, ySrc: int):

        textWidth = self._pdf.get_string_width(s=interfaceName)
        pixelSize = self._pdf.font_size_pt

        position = self._determineInterfaceNamePosition(xSrc=xSrc, ySrc=ySrc,
                                                        attachmentSide=attachmentSide,
                                                        pixelSize=(pixelSize, pixelSize),
                                                        textSize=(textWidth, pixelSize))

        textPosition: InternalPosition = self._pdfCommon.toInternal(position=position)

        self._pdf.text(x=textPosition.x, y=textPosition.y, txt=interfaceName)

    def _adjustXYForCircle(self, attachmentSide: AttachmentSide, x: int, y: int) -> Tuple[int, int]:

        adjustedX: int = 0
        adjustedY: int = 0

        if attachmentSide == AttachmentSide.EAST:
            adjustedX = x
            adjustedY = y - (LOLLIPOP_CIRCLE_HEIGHT // 2)
        elif attachmentSide == AttachmentSide.WEST:
            adjustedX = x - LOLLIPOP_CIRCLE_WIDTH
            adjustedY = y - (LOLLIPOP_CIRCLE_HEIGHT // 2)
        elif attachmentSide == AttachmentSide.NORTH:
            adjustedX = x - (LOLLIPOP_CIRCLE_WIDTH // 2)
            adjustedY = y - LOLLIPOP_CIRCLE_HEIGHT
        elif attachmentSide == AttachmentSide.SOUTH:
            adjustedX = x - (LOLLIPOP_CIRCLE_WIDTH // 2)
            adjustedY = y

        return adjustedX, adjustedY

    def _determineInterfaceNamePosition(self, xSrc, ySrc,
                                        attachmentSide: AttachmentSide,
                                        pixelSize: Tuple[int, int],
                                        textSize: Tuple[int, int]) -> Position:

        position: Position = Position()
        x:        int      = xSrc
        y:        int      = ySrc

        fWidth, fHeight = pixelSize
        tWidth, tHeight = textSize

        if attachmentSide == AttachmentSide.NORTH:
            y -= (LOLLIPOP_LINE_LENGTH + (LOLLIPOP_CIRCLE_RADIUS * 2) + ADJUST_AWAY_FROM_IMPLEMENTOR)
            x -= (tWidth // 2)
            position.x = x
            position.y = y

        elif attachmentSide == AttachmentSide.SOUTH:
            y += (LOLLIPOP_LINE_LENGTH + LOLLIPOP_CIRCLE_RADIUS + ADJUST_AWAY_FROM_IMPLEMENTOR)
            x -= (tWidth // 2)
            position.x = x
            position.y = y

        elif attachmentSide == AttachmentSide.WEST:
            y = y - (fHeight * 2)
            originalX: int = x
            x = x - LOLLIPOP_LINE_LENGTH - (tWidth // 2)
            while x + tWidth > originalX:
                x -= ADJUST_AWAY_FROM_IMPLEMENTOR
            position.x = x
            position.y = y

        elif attachmentSide == AttachmentSide.EAST:
            y = y - (fHeight * 2)
            x = x + round(LOLLIPOP_LINE_LENGTH * 0.8)
            position.x = x
            position.y = y
        else:
            self.logger.warning(f'Unknown attachment point: {attachmentSide}')
            assert False, 'Unknown attachment point'

        return position
