
from typing import Tuple

from dataclasses import dataclass

from codeallybasic.Position import Position

from codeallyadvanced.ui.Common import Common
from codeallyadvanced.ui.AttachmentSide import AttachmentSide


@dataclass(eq=True)
class AbsolutePosition:
    """
    """
    x: int = 0
    y: int = 0


class CommonAbsolute:
    """
    This class of computations resides here instead of common because it uses the Position
    class from Definitions and not and InternalPosition class which is relative to the
    particular output type (pdf/image)
    """
    X_FUDGE_FACTOR: int = 9
    Y_FUDGE_FACTOR: int = 9

    @classmethod
    def computeAbsoluteLabelPosition(cls, srcPosition: Position, dstPosition: Position, labelPosition: Position) -> Tuple[int, int]:
        """
        Label  positions are relative to the line they are attached to;

        Args:
            srcPosition:
            dstPosition:
            labelPosition:
        """
        xLength: int = abs(srcPosition.x - dstPosition.x)
        yLength: int = abs(srcPosition.y - dstPosition.y)

        if srcPosition.x < dstPosition.x:
            x: int = srcPosition.x + (xLength // 2) + labelPosition.x
            if cls.doXAdjustment(srcPosition=srcPosition, dstPosition=dstPosition) is True:
                x += CommonAbsolute.X_FUDGE_FACTOR
        else:
            x = dstPosition.x + (xLength // 2) + labelPosition.x
            if cls.doXAdjustment(srcPosition=srcPosition, dstPosition=dstPosition) is True:
                x -= CommonAbsolute.X_FUDGE_FACTOR

        if srcPosition.y < dstPosition.y:
            y: int = srcPosition.y + (yLength // 2) + labelPosition.y
        else:
            y = dstPosition.y + (yLength // 2) + labelPosition.y

        y += CommonAbsolute.Y_FUDGE_FACTOR

        return x, y

    @classmethod
    def doXAdjustment(cls, srcPosition: Position, dstPosition: Position) -> bool:

        ans: bool = True

        placement: AttachmentSide = Common.whereIsDestination(sourcePosition=srcPosition, destinationPosition=dstPosition)

        if placement == AttachmentSide.NORTH or placement == AttachmentSide.SOUTH:
            ans = False

        return ans
