
from logging import Logger
from logging import getLogger

from abc import abstractmethod
from abc import ABCMeta

from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import UmlLineDefinitions

from pyumldiagrams.xmlsupport.ShapeAttributes import ShapeAttributes


class MyMetaAbstractToClassDefinition(ABCMeta, type(ShapeAttributes)):        # type: ignore
    """
    I have know idea why this works:
    https://stackoverflow.com/questions/66591752/metaclass-conflict-when-trying-to-create-a-python-abstract-class-that-also-subcl
    """
    pass


class AbstractToClassDefinition(ShapeAttributes):
    __metaclass__ = MyMetaAbstractToClassDefinition

    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._classDefinitions:   ClassDefinitions   = ClassDefinitions([])
        self._umlLineDefinitions: UmlLineDefinitions = UmlLineDefinitions([])

    @abstractmethod
    def generateClassDefinitions(self):
        pass

    @abstractmethod
    def generateUmlLineDefinitions(self):
        pass

    @property
    @abstractmethod
    def classDefinitions(self) -> ClassDefinitions:
        pass

    @property
    @abstractmethod
    def umlLineDefinitions(self) -> UmlLineDefinitions:
        pass
