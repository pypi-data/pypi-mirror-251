
from typing import List
from typing import NewType
from typing import cast

from dataclasses import dataclass
from dataclasses import field

from enum import Enum

from codeallybasic.Position import Position

from codeallyadvanced.ui.AttachmentSide import AttachmentSide

from pyumldiagrams.Defaults import TOP_MARGIN
from pyumldiagrams.Defaults import LEFT_MARGIN
from pyumldiagrams.Defaults import DEFAULT_HORIZONTAL_GAP
from pyumldiagrams.Defaults import DEFAULT_VERTICAL_GAP
from pyumldiagrams.UnsupportedException import UnsupportedException


ClassName = NewType('ClassName', str)


def createPositionFactory() -> Position:
    return Position()


@dataclass
class DiagramPadding:
    """
    todo::  These should move to the Internal package
    """

    topMargin:  int = TOP_MARGIN
    """
    The diagram's observed top margin.  See `pyumldiagrams.Defaults.TOP_MARGIN`
    """
    leftMargin: int = LEFT_MARGIN
    """
    The diagram's observed left margin.  See `pyumldiagrams.Defaults.LEFT_MARGIN`
    """

    horizontalGap: int = DEFAULT_HORIZONTAL_GAP
    """
    The horizontal gap between UML graphics added to the layout in addition to the gap imposed 
    by the actual graphics positions. See `pyumldiagrams.Defaults.DEFAULT_HORIZONTAL_GAP`
    """
    verticalGap:   int = DEFAULT_VERTICAL_GAP
    """
    The vertical gap between UML graphics added to the layout in addition to the gap imposed 
    by the actual graphics positions.  See `pyumldiagrams.Defaults.DEFAULT_VERTICAL_GAP`
    """


@dataclass
class Size:
    """
    Defines the size of the input UML definitions;
    """
    width:  int = 100
    """
    The width of a shape
    """
    height: int = 100
    """
    The height of the shape
    """


def createSizeFactory() -> Size:
    return Size()


class VisibilityType(Enum):
    """
    Defines the visibility of either methods or fields
    """
    Public    = '+'
    Private   = '-'
    Protected = '#'

    @staticmethod
    def toEnum(strValue: str) -> 'VisibilityType':
        """
        Converts the input string to the line type enum
        Args:
            strValue:   The serialized string representation

        Returns:  The line type enumeration
        """
        canonicalStr: str = strValue.lower().strip(' ')
        if canonicalStr == 'public':
            return VisibilityType.Public
        elif canonicalStr == 'private':
            return VisibilityType.Private
        elif canonicalStr == 'protected':
            return VisibilityType.Protected
        else:
            raise UnsupportedException(f'Do not handle VisibilityType {canonicalStr}')


@dataclass
class BaseDefinition:

    __slots__ = ['name']
    name: str
    """
    The name associated with the definition.
    """


@dataclass
class DefaultValueDefinition(BaseDefinition):
    defaultValue:  str = ''
    """
    A string that describes a parameter default value
    """


@dataclass
class ParameterDefinition(DefaultValueDefinition):
    """
    Defines a single parameter for a method
    """
    parameterType: str = ''
    """
    A string that describes the parameter type
    """


Parameters = NewType('Parameters', List[ParameterDefinition])
"""
Syntactic sugar to define a list of parameters.  
"""


class DisplayMethodParameters(Enum):

    DISPLAY        = 'Display'
    DO_NOT_DISPLAY = 'DoNotDisplay'
    UNSPECIFIED    = 'Unspecified'


def createParametersFactory() -> Parameters:
    return Parameters([])


@dataclass
class MethodDefinition(BaseDefinition):
    """
    Defines a single method in a single UML class
    """
    visibility: VisibilityType = VisibilityType.Public
    """
    Defines the method visibility.  See `VisibilityType`
    """
    returnType: str = ''
    """
    Defines the method return type.
    """
    parameters: Parameters = field(default_factory=createParametersFactory)
    """
    Define the parameters for a particular method
    """


Methods = NewType('Methods', List[MethodDefinition])
"""
Syntactic sugar to define a list of methods.
"""


def createMethodsFactory() -> Methods:
    return Methods([])


@dataclass
class FieldDefinition(DefaultValueDefinition):
    """
    Defines a single instance variable
    """
    fieldType: str = ''
    """
    A string that describes the field type
    """
    visibility: VisibilityType = VisibilityType.Public
    """
    Defines the field visibility.  See `VisibilityType`
    """


Fields = NewType('Fields', List[FieldDefinition])


def createFieldsFactory() -> Fields:
    return Fields([])


@dataclass
class ShapeDefinition(BaseDefinition):
    size:     Size     = field(default_factory=createSizeFactory)
    """
    The size of UML class symbol.  See `Size`
    """
    position: Position = field(default_factory=createPositionFactory)
    """
    The position of the UML class symbol.  See `Position`
    """


@dataclass
class ClassDefinition(ShapeDefinition):
    """ The class definition.  Currently, does not support instance properties.
    """
    methods: Methods   = field(default_factory=createMethodsFactory)
    """
    The list of methods this class implements.  
    """
    fields:  Fields    = field(default_factory=createFieldsFactory)
    """
    The list of instance variables this class defines.
    """
    displayStereotype:  bool = True
    """
    If true display the class stereotype when drawing the class diagram
    """
    displayMethods:     bool = True
    """
    If True display the class methods
    """
    displayFields:      bool = True
    """
    If True display the class instance variables
    """
    displayMethodParameters: DisplayMethodParameters = DisplayMethodParameters.UNSPECIFIED
    """
    If True display the method parameters;  If UNSPECIFIED defer to global
    """
    fileName: str = ''
    """
    The file name where the original source code came from (only if reverse engineered)
    """
    description: str = ''
    """
    Text describing the rationale for this class
    """


ClassDefinitions = NewType('ClassDefinitions', List[ClassDefinition])

Content  = NewType('Content', str)
Contents = NewType('Contents', List[Content])


def createContentsFactory() -> Contents:
    return Contents([])


@dataclass
class NoteDefinition(ShapeDefinition):
    content: Contents = field(default_factory=createContentsFactory)
    """
    The note content
    """


UmlNoteDefinitions = NewType('UmlNoteDefinitions', List[NoteDefinition])


class LineType(Enum):
    """
    The type of UML line you wish to draw.  Currently, bare associations are not supported.
    """
    Inheritance     = 0
    Interface       = 1
    Aggregation     = 3
    Composition     = 7
    Association     = 9
    NoteLink        = 11
    Lollipop        = 13

    @staticmethod
    def toEnum(strValue: str) -> 'LineType':
        """
        Converts the input string to the line type enum
        Args:
            strValue:   The serialized string representation

        Returns:  The line type enumeration
        """
        canonicalStr: str = strValue.lower().strip(' ')
        if canonicalStr == 'aggregation':
            return LineType.Aggregation
        elif canonicalStr == 'composition':
            return LineType.Composition
        elif canonicalStr == 'inheritance':
            return LineType.Inheritance
        elif canonicalStr == 'interface':
            return LineType.Interface
        elif canonicalStr == 'association':
            return LineType.Association
        elif canonicalStr == 'notelink':
            return LineType.NoteLink
        elif canonicalStr == 'lollipop':
            return LineType.Lollipop
        else:
            raise UnsupportedException(f'Do not handle LineType {canonicalStr}')


NamedAssociations: List[LineType] = [LineType.Association, LineType.Aggregation, LineType.Composition]


LinePositions = NewType('LinePositions', list[Position])


@dataclass
class LineDefinition:
    """
    Defines a line between many points;  Index 0 the start of the line;  That last point
    is the end of the line
    """
    linePositions: LinePositions


@dataclass
class UmlLineDefinition(LineDefinition):
    """
    A UML Line definition includes its type
    """
    lineType: LineType
    """
    The UML line type  See `LineType`.
    """
    name: str = ''
    """
    Name of composition, aggregation association links
    """
    cardinalitySource:      str = ''
    cardinalityDestination: str = ''
    """
    Cardinality values used for composition, aggregation, and association links
    """
    namePosition:                   Position = field(default_factory=createPositionFactory)
    sourceCardinalityPosition:      Position = field(default_factory=createPositionFactory)
    destinationCardinalityPosition: Position = field(default_factory=createPositionFactory)


UmlLineDefinitions = NewType('UmlLineDefinitions', List[UmlLineDefinition])
"""
Syntactic sugar to define a list of UML Lines.
"""


@dataclass
class UmlLollipopDefinition:
    name: str = ''
    """
    Interface Name 
    """
    attachmentSide: AttachmentSide = cast(AttachmentSide, None)
    position:       Position       = field(default_factory=createPositionFactory)


UmlLollipopDefinitions = NewType('UmlLollipopDefinitions', List[UmlLollipopDefinition])


class RenderStyle(Enum):
    """
    An enumeration that determines how to draw various UML and other graphical elements
    """
    Draw     = 'D'
    """
    Just draw the outline
    """
    Fill     = 'F'
    """
    Just fill in the area associated with the shape
    """
    DrawFill = 'DF'
    """
    Do both when drawing the UML shape or figure
    """


@dataclass
class RectangleDefinition:
    """
    Defines a rectangle
    """

    renderStyle: RenderStyle = RenderStyle.Draw
    """
    How to draw the rectangle.  See `RenderStyle`
    """
    position:    Position    = field(default_factory=createPositionFactory)
    """
    Where to put the rectangle.  See `Position`
    """
    size:        Size        = field(default_factory=createSizeFactory)
    """
    The rectangle size.  See `Size`
    """


@dataclass
class EllipseDefinition(RectangleDefinition):
    """
    This is just typing syntactical sugar on how to define an Ellipse.
    """
    pass
