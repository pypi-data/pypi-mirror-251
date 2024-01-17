
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minicompat import NodeList

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from xml.dom.minidom import parseString

from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import DisplayMethodParameters
from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import Parameters
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import UmlLineDefinitions
from pyumldiagrams.Definitions import VisibilityType
from pyumldiagrams.Definitions import createMethodsFactory

from pyumldiagrams.UnsupportedException import UnsupportedException

from pyumldiagrams.xmlsupport.XmlConstants import ATTR_DEFAULT_VALUE
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_DISPLAY_PARAMETERS
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_HEIGHT
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_LINK_DESTINATION_ANCHOR_X
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_LINK_DESTINATION_ANCHOR_Y
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_LINK_SOURCE_ANCHOR_X
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_LINK_SOURCE_ANCHOR_Y
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_NAME
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_SHOW_FIELDS
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_SHOW_METHODS
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_SHOW_STEREOTYPE
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_TYPE
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_WIDTH
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_X
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_Y
from pyumldiagrams.xmlsupport.XmlConstants import ATTR_VISIBILITY
from pyumldiagrams.xmlsupport.XmlConstants import ELEMENT_CONTROL_POINT
from pyumldiagrams.xmlsupport.XmlConstants import ELEMENT_GRAPHIC_CLASS
from pyumldiagrams.xmlsupport.XmlConstants import ELEMENT_GRAPHIC_LINK
from pyumldiagrams.xmlsupport.XmlConstants import ELEMENT_MODEL_CLASS
from pyumldiagrams.xmlsupport.XmlConstants import ELEMENT_MODEL_LINK
from pyumldiagrams.xmlsupport.XmlConstants import ELEMENT_MODEL_METHOD
from pyumldiagrams.xmlsupport.XmlConstants import ELEMENT_MODEL_PARAM
from pyumldiagrams.xmlsupport.XmlConstants import ELEMENT_MODEL_RETURN_TYPE


class ToClassDefinition:

    def __init__(self, fqFileName: str):

        self.logger: Logger = getLogger(__name__)

        self._xmlData:          str      = ''

        self._classDefinitions:   ClassDefinitions   = ClassDefinitions([])
        self._umlLineDefinitions: UmlLineDefinitions = UmlLineDefinitions([])

        self._documentNode: Document = cast(Document, None)
        with open(fqFileName) as xmlFile:
            self._xmlData = xmlFile.read()
            self._documentNode = parseString(self._xmlData)

    def generateClassDefinitions(self):

        graphicClassNodes: NodeList = self._documentNode.getElementsByTagName(ELEMENT_GRAPHIC_CLASS)

        self.logger.debug(f'{graphicClassNodes=}')

        for xmlGraphicClassNode in graphicClassNodes:

            xmlGraphicClass: Element = cast(Element, xmlGraphicClassNode)

            height: int = int(xmlGraphicClass.getAttribute(ATTR_HEIGHT))
            width:  int = int(xmlGraphicClass.getAttribute(ATTR_WIDTH))
            x:      int = int(xmlGraphicClass.getAttribute(ATTR_X))
            y:      int = int(xmlGraphicClass.getAttribute(ATTR_Y))

            xmlClass:  Element = xmlGraphicClass.getElementsByTagName(ELEMENT_MODEL_CLASS)[0]
            className: str     = xmlClass.getAttribute(ATTR_NAME)

            displayMethods:    bool = self._stringToBoolean(xmlClass.getAttribute(ATTR_SHOW_METHODS))
            displayFields:     bool = self._stringToBoolean(xmlClass.getAttribute(ATTR_SHOW_FIELDS))
            displayStereotype: bool = self._stringToBoolean(xmlClass.getAttribute(ATTR_SHOW_STEREOTYPE))

            displayParametersStr: str = xmlClass.getAttribute(ATTR_DISPLAY_PARAMETERS)

            if displayParametersStr is None or displayParametersStr == '':
                displayMethodParameters: DisplayMethodParameters = DisplayMethodParameters.UNSPECIFIED
            else:
                displayMethodParameters = DisplayMethodParameters(displayParametersStr)

            classDef: ClassDefinition = ClassDefinition(name=className)

            classDef.displayMethods    = displayMethods
            classDef.displayFields     = displayFields
            classDef.displayStereotype = displayStereotype
            classDef.displayMethodParameters = displayMethodParameters

            classSize: Size = Size(width=width, height=height)
            classDef.size = classSize

            position: Position = Position(x=x, y=y)
            classDef.position = position

            classDef.methods = self._generateMethods(xmlClass=xmlClass)

            self.logger.debug(f'{classDef=}')
            self._classDefinitions.append(classDef)

    def _generateMethods(self, xmlClass: Element) -> Methods:

        methods: Methods = createMethodsFactory()

        for xmlMethod in xmlClass.getElementsByTagName(ELEMENT_MODEL_METHOD):
            methodName: str = xmlMethod.getAttribute(ATTR_NAME)
            self.logger.debug(f'{methodName=}')

            method: MethodDefinition = MethodDefinition(name=methodName)

            visibilityStr: str = xmlMethod.getAttribute(ATTR_VISIBILITY)
            method.visibility = VisibilityType.toEnum(visibilityStr)

            xmlReturnTypeNodeList: NodeList = xmlMethod.getElementsByTagName(ELEMENT_MODEL_RETURN_TYPE)
            returnNode:            Element  = xmlReturnTypeNodeList[0]
            retType:               str      = returnNode.getAttribute(ATTR_TYPE)
            method.returnType = retType
            method = self._generateMethodParameters(xmlMethod=xmlMethod, methodDef=method)

            methods.append(method)

        return methods

    def generateUmlLineDefinitions(self):

        graphicLinkNodes: NodeList = self._documentNode.getElementsByTagName(ELEMENT_GRAPHIC_LINK)

        for graphicLinkNode in graphicLinkNodes:

            xmlGraphicLink: Element = cast(Element, graphicLinkNode)

            xmlLink:       Element  = xmlGraphicLink.getElementsByTagName(ELEMENT_MODEL_LINK)[0]
            controlPoints: NodeList = xmlGraphicLink.getElementsByTagName(ELEMENT_CONTROL_POINT)

            srcX: int = int(xmlGraphicLink.getAttribute(ATTR_LINK_SOURCE_ANCHOR_X))
            srcY: int = int(xmlGraphicLink.getAttribute(ATTR_LINK_SOURCE_ANCHOR_Y))

            strType:  str      = xmlLink.getAttribute(ATTR_TYPE)
            lineType: LineType = LineType.toEnum(strType)

            srcPosition: Position = Position(x=srcX, y=srcY)
            linePositions: LinePositions = LinePositions([srcPosition])
            umlLineDefinition: UmlLineDefinition = UmlLineDefinition(linePositions=linePositions, lineType=lineType)

            for point in controlPoints:

                controlPoint: Element = cast(Element, point)

                self.logger.debug(f'{controlPoint=}')
                x: int = int(controlPoint.getAttribute(ATTR_X))
                y: int = int(controlPoint.getAttribute(ATTR_Y))
                bendPosition: Position = Position(x=x, y=y)
                linePositions.append(bendPosition)

            destX: int = int(xmlGraphicLink.getAttribute(ATTR_LINK_DESTINATION_ANCHOR_X))
            destY: int = int(xmlGraphicLink.getAttribute(ATTR_LINK_DESTINATION_ANCHOR_Y))

            destPosition: Position = Position(x=destX, y=destY)

            linePositions.append(destPosition)
            self.logger.debug(f'{umlLineDefinition=}')
            self._umlLineDefinitions.append(umlLineDefinition)

    @property
    def classDefinitions(self) -> ClassDefinitions:
        return self._classDefinitions

    @classDefinitions.setter
    def classDefinitions(self, newDefinitions: ClassDefinitions):
        raise UnsupportedException('Class definitions are read-only')

    @property
    def umlLineDefinitions(self) -> UmlLineDefinitions:
        return self._umlLineDefinitions

    @umlLineDefinitions.setter
    def umlLineDefinitions(self, newDefinitions: UmlLineDefinitions):
        raise UnsupportedException('UML Line definitions are read-only')

    def _generateMethodParameters(self, xmlMethod: Element, methodDef: MethodDefinition) -> MethodDefinition:

        parameters: Parameters = Parameters([])
        for xmlParam in xmlMethod.getElementsByTagName(ELEMENT_MODEL_PARAM):
            paramDef: ParameterDefinition = self._getParam(xmlParam=xmlParam)
            parameters.append(paramDef)

        methodDef.parameters = parameters

        return methodDef

    def _getParam(self, xmlParam: Element) -> ParameterDefinition:

        paramName:    str = xmlParam.getAttribute(ATTR_NAME)
        paramType:    str = xmlParam.getAttribute(ATTR_TYPE)
        defaultValue: str = xmlParam.getAttribute(ATTR_DEFAULT_VALUE)
        self.logger.debug(f'{paramName=} {paramType=} {defaultValue=}')

        parameterDefinition: ParameterDefinition = ParameterDefinition(name=paramName,  parameterType=paramType)

        parameterDefinition.defaultValue = defaultValue

        return parameterDefinition

    def _stringToBoolean(self, strBoolValue: str) -> bool:

        self.logger.debug(f'{strBoolValue=}')
        try:
            if strBoolValue is not None:
                if strBoolValue in [True, "True", "true", 1, "1"]:
                    return True
        except (ValueError, Exception) as e:
            self.logger.error(f'_stringToBoolean error: {e}')

        return False
