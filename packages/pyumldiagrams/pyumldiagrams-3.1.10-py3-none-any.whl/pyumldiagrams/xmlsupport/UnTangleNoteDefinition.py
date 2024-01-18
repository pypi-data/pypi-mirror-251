
from typing import cast

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from untangle import Element

from codeallybasic.Common import XML_END_OF_LINE_MARKER

from pyumldiagrams.Definitions import Contents
from pyumldiagrams.Definitions import NoteDefinition
from pyumldiagrams.xmlsupport import XmlConstants
from pyumldiagrams.xmlsupport.ShapeAttributes import ShapeAttributes


class UnTangleNoteDefinition(ShapeAttributes):

    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def untangle(self, linkElement: Element) -> NoteDefinition:

        pyutNoteElement: Element = linkElement.PyutNote

        noteDefinition: NoteDefinition = NoteDefinition(name='')    # Notes do not have a name

        noteDefinition.size     = self._shapeSize(graphicElement=linkElement)
        noteDefinition.position = self._shapePosition(graphicElement=linkElement)

        # TODO:  Update when code-ally-basic has common code
        rawContent:   str      = pyutNoteElement[XmlConstants.ATTR_CONTENT_V11]
        cleanContent: str      = rawContent.replace(XML_END_OF_LINE_MARKER, osLineSep)
        lineList:     Contents = cast(Contents, cleanContent.split(osLineSep))      # I am coercive

        noteDefinition.content  = Contents(lineList)

        return noteDefinition
