# encoding: utf-8

"""lxml custom element class for CT_GraphicalObjectFrame XML element."""

from pptx.oxml import parse_xml
from pptx.oxml.chart.chart import CT_Chart
from pptx.oxml.ns import nsdecls
from pptx.oxml.shapes.shared import BaseShapeElement
from pptx.oxml.simpletypes import XsdBoolean, XsdString, ST_RelationshipId
from pptx.oxml.table import CT_Table
from pptx.oxml.xmlchemy import (
    BaseOxmlElement,
    OneAndOnlyOne,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrOne,
)
from pptx.spec import (
    GRAPHIC_DATA_URI_CHART,
    GRAPHIC_DATA_URI_OLEOBJ,
    GRAPHIC_DATA_URI_TABLE,
    GRAPHIC_DATA_URI_DRAWING,
)


class CT_GraphicalObject(BaseOxmlElement):
    """
    ``<a:graphic>`` element, which is the container for the reference to or
    definition of the framed graphical object (table, chart, etc.).
    """

    graphicData = OneAndOnlyOne("a:graphicData")

    @property
    def chart(self):
        """
        The ``<c:chart>`` grandchild element, or |None| if not present.
        """
        return self.graphicData.chart

    @property
    def smart_art(self):
        return self.graphicData.diagram


class CT_GraphicalObjectData(BaseShapeElement):
    """
    ``<p:graphicData>`` element, the direct container for a table, a chart,
    or another graphical object.
    """

    chart = ZeroOrOne("c:chart")
    tbl = ZeroOrOne("a:tbl")
    uri = RequiredAttribute("uri", XsdString)
    diagram = ZeroOrOne("dgm:relIds")

    @property
    def blob_rId(self):
        """Optional "r:id" attribute value of `<p:oleObj>` descendent element.

        This value is `None` when this `p:graphicData` element does not enclose an OLE
        object. This value could also be `None` if an enclosed OLE object does not
        specify this attribute (it is specified optional in the schema) but so far, all
        OLE objects we've encountered specify this value.
        """
        return None if self._oleObj is None else self._oleObj.rId

    @property
    def is_embedded_ole_obj(self):
        """Optional boolean indicating an embedded OLE object.

        Returns `None` when this `p:graphicData` element does not enclose an OLE object.
        `True` indicates an embedded OLE object and `False` indicates a linked OLE
        object.
        """
        return None if self._oleObj is None else self._oleObj.is_embedded

    @property
    def progId(self):
        """Optional str value of "progId" attribute of `<p:oleObj>` descendent.

        This value identifies the "type" of the embedded object in terms of the
        application used to open it.

        This value is `None` when this `p:graphicData` element does not enclose an OLE
        object. This could also be `None` if an enclosed OLE object does not specify
        this attribute (it is specified optional in the schema) but so far, all OLE
        objects we've encountered specify this value.
        """
        return None if self._oleObj is None else self._oleObj.progId

    @property
    def showAsIcon(self):
        """Optional value of "showAsIcon" attribute value of `p:oleObj` descendent.

        This value is `None` when this `p:graphicData` element does not enclose an OLE
        object. It is False when the `showAsIcon` attribute is omitted on the `p:oleObj`
        element.
        """
        return None if self._oleObj is None else self._oleObj.showAsIcon

    @property
    def _oleObj(self):
        """Optional `<p:oleObj>` element contained in this `p:graphicData' element.

        Returns `None` when this graphic-data element does not enclose an OLE object.
        Note that this returns the last `p:oleObj` element found. There can be more
        than one `p:oleObj` element because an `<mc.AlternateContent>` element may
        appear as the child of `p:graphicData` and that alternate-content subtree can
        contain multiple compatibility choices. The last one should suit best for
        reading purposes because it contains the lowest common denominator.
        """
        oleObjs = self.xpath(".//p:oleObj")
        return oleObjs[-1] if oleObjs else None


class CT_GraphicalObjectFrame(BaseShapeElement):
    """
    ``<p:graphicFrame>`` element, which is a container for a table, a chart,
    or another graphical object.
    """

    nvGraphicFramePr = OneAndOnlyOne("p:nvGraphicFramePr")
    xfrm = OneAndOnlyOne("p:xfrm")
    graphic = OneAndOnlyOne("a:graphic")

    @property
    def chart(self):
        """
        The ``<c:chart>`` great-grandchild element, or |None| if not present.
        """
        return self.graphic.chart

    @property
    def chart_rId(self):
        """
        The ``rId`` attribute of the ``<c:chart>`` great-grandchild element,
        or |None| if not present.
        """
        chart = self.chart
        if chart is None:
            return None
        return chart.rId

    def get_or_add_xfrm(self):
        """
        Return the required ``<p:xfrm>`` child element. Overrides version on
        BaseShapeElement.
        """
        return self.xfrm

    @property
    def smart_art_data_rId(self):
        """
        The ``r:dm`` attribute of the ``<dgm:relIds>`` great-grandchild element,
        or |None| if not present.
        """
        smart_art = self.smart_art
        if smart_art is None:
            return None
        return smart_art.data_rId

    @property
    def smart_art_style_rId(self):
        """
        The ``r:qs`` attribute of the ``<dgm:relIds>`` great-grandchild element,
        or |None| if not present.
        """
        smart_art = self.smart_art
        if smart_art is None:
            return None
        return smart_art.style_rId

    @property
    def smart_art_layout_rId(self):
        """
        The ``r:lo`` attribute of the ``<dgm:relIds>`` great-grandchild element,
        or |None| if not present.
        """
        smart_art = self.smart_art
        if smart_art is None:
            return None
        return smart_art.layout_rId

    @property
    def smart_art_colors_rId(self):
        """
        The ``r:cs`` attribute of the ``<dgm:relIds>`` great-grandchild element,
        or |None| if not present.
        """
        smart_art = self.smart_art
        if smart_art is None:
            return None
        return smart_art.colors_rId

    @property
    def smart_art(self):
        """
        The ``<dgm:relIds>`` great-grandchild element, or |None| if not present.
        """
        return self.graphic.smart_art


    @property
    def graphicData(self):
        """`<a:graphicData> grandchild of this graphic-frame element."""
        return self.graphic.graphicData

    @property
    def graphicData_uri(self):
        """str value of `uri` attribute of `<a:graphicData> grandchild."""
        return self.graphic.graphicData.uri

    @property
    def has_oleobj(self):
        """True for graphicFrame containing an OLE object, False otherwise."""
        return self.graphicData.uri == GRAPHIC_DATA_URI_OLEOBJ

    @property
    def is_embedded_ole_obj(self):
        """Optional boolean indicating an embedded OLE object.

        Returns `None` when this `p:graphicFrame` element does not enclose an OLE
        object. `True` indicates an embedded OLE object and `False` indicates a linked
        OLE object.
        """
        return self.graphicData.is_embedded_ole_obj

    @classmethod
    def new_chart_graphicFrame(cls, id_, name, rId, x, y, cx, cy):
        """
        Return a ``<p:graphicFrame>`` element tree populated with a chart
        element.
        """
        graphicFrame = CT_GraphicalObjectFrame.new_graphicFrame(id_, name, x, y, cx, cy)
        graphicData = graphicFrame.graphic.graphicData
        graphicData.uri = GRAPHIC_DATA_URI_CHART
        graphicData.append(CT_Chart.new_chart(rId))
        return graphicFrame

    @classmethod
    def new_graphicFrame(cls, id_, name, x, y, cx, cy):
        """
        Return a new ``<p:graphicFrame>`` element tree suitable for
        containing a table or chart. Note that a graphicFrame element is not
        a valid shape until it contains a graphical object such as a table.
        """
        xml = cls._graphicFrame_tmpl() % (id_, name, x, y, cx, cy)
        graphicFrame = parse_xml(xml)
        return graphicFrame

    @classmethod
    def new_ole_object_graphicFrame(
        cls, id_, name, ole_object_rId, progId, icon_rId, x, y, cx, cy, imgW, imgH
    ):
        """Return newly-created `<p:graphicFrame>` for embedded OLE-object.

        `ole_object_rId` identifies the relationship to the OLE-object part.

        `progId` is a str identifying the object-type in terms of the application
        (program) used to open it. This becomes an attribute of the same name in the
        `p:oleObj` element.

        `icon_rId` identifies the relationship to an image part used to display the
        OLE-object as an icon (vs. a preview).
        """
        return parse_xml(
            cls._graphicFrame_xml_for_ole_object(
                id_, name, x, y, cx, cy, ole_object_rId, progId, icon_rId, imgW, imgH
            )
        )

    @classmethod
    def new_smart_art_graphicFrame(
        cls, id_, name, x, y, cx, cy, rId_dm, rId_lo, rId_qs, rId_cs
    ):
        """
        Return a ``<p:graphicFrame>`` element tree populated with a chart
        element.
        """
        graphicFrame = CT_GraphicalObjectFrame.new_graphicFrame(id_, name, x, y, cx, cy)
        graphicData = graphicFrame.graphic.graphicData
        graphicData.uri = GRAPHIC_DATA_URI_DRAWING
        graphicData.append(CT_RelIds.new_diagram(rId_dm, rId_lo, rId_qs, rId_cs))
        return graphicFrame


    @classmethod
    def new_table_graphicFrame(cls, id_, name, rows, cols, x, y, cx, cy):
        """
        Return a ``<p:graphicFrame>`` element tree populated with a table
        element.
        """
        graphicFrame = cls.new_graphicFrame(id_, name, x, y, cx, cy)
        graphicFrame.graphic.graphicData.uri = GRAPHIC_DATA_URI_TABLE
        graphicFrame.graphic.graphicData.append(CT_Table.new_tbl(rows, cols, cx, cy))
        return graphicFrame

    @classmethod
    def _graphicFrame_tmpl(cls):
        return (
            "<p:graphicFrame %s>\n"
            "  <p:nvGraphicFramePr>\n"
            '    <p:cNvPr id="%s" name="%s"/>\n'
            "    <p:cNvGraphicFramePr>\n"
            '      <a:graphicFrameLocks noGrp="1"/>\n'
            "    </p:cNvGraphicFramePr>\n"
            "    <p:nvPr/>\n"
            "  </p:nvGraphicFramePr>\n"
            "  <p:xfrm>\n"
            '    <a:off x="%s" y="%s"/>\n'
            '    <a:ext cx="%s" cy="%s"/>\n'
            "  </p:xfrm>\n"
            "  <a:graphic>\n"
            "    <a:graphicData/>\n"
            "  </a:graphic>\n"
            "</p:graphicFrame>"
            % (nsdecls("a", "p"), "%d", "%s", "%d", "%d", "%d", "%d")
        )

    @classmethod
    def _graphicFrame_xml_for_ole_object(
        cls, id_, name, x, y, cx, cy, ole_object_rId, progId, icon_rId, imgW, imgH
    ):
        """str XML for <a:graphic> element of an embedded OLE-object shape."""
        return (
            "<p:graphicFrame {nsdecls}>\n"
            "  <p:nvGraphicFramePr>\n"
            '    <p:cNvPr id="{id_}" name="{name}"/>\n'
            "    <p:cNvGraphicFramePr>\n"
            '      <a:graphicFrameLocks noGrp="1"/>\n'
            "    </p:cNvGraphicFramePr>\n"
            "    <p:nvPr/>\n"
            "  </p:nvGraphicFramePr>\n"
            "  <p:xfrm>\n"
            '    <a:off x="{x}" y="{y}"/>\n'
            '    <a:ext cx="{cx}" cy="{cy}"/>\n'
            "  </p:xfrm>\n"
            "  <a:graphic>\n"
            "    <a:graphicData"
            '        uri="http://schemas.openxmlformats.org/presentationml/2006/ole">\n'
            '      <p:oleObj showAsIcon="1"'
            '                r:id="{ole_object_rId}"'
            '                imgW="{imgW}"'
            '                imgH="{imgH}"'
            '                progId="{progId}">\n'
            "        <p:embed/>\n"
            "        <p:pic>\n"
            "          <p:nvPicPr>\n"
            '            <p:cNvPr id="0" name=""/>\n'
            "            <p:cNvPicPr/>\n"
            "            <p:nvPr/>\n"
            "          </p:nvPicPr>\n"
            "          <p:blipFill>\n"
            '            <a:blip r:embed="{icon_rId}"/>\n'
            "            <a:stretch>\n"
            "              <a:fillRect/>\n"
            "            </a:stretch>\n"
            "          </p:blipFill>\n"
            "          <p:spPr>\n"
            "            <a:xfrm>\n"
            '              <a:off x="{x}" y="{y}"/>\n'
            '              <a:ext cx="{cx}" cy="{cy}"/>\n'
            "            </a:xfrm>\n"
            '            <a:prstGeom prst="rect">\n'
            "              <a:avLst/>\n"
            "            </a:prstGeom>\n"
            "          </p:spPr>\n"
            "        </p:pic>\n"
            "      </p:oleObj>\n"
            "    </a:graphicData>\n"
            "  </a:graphic>\n"
            "</p:graphicFrame>"
        ).format(
            nsdecls=nsdecls("a", "p", "r"),
            id_=id_,
            name=name,
            x=x,
            y=y,
            cx=cx,
            cy=cy,
            ole_object_rId=ole_object_rId,
            progId=progId,
            icon_rId=icon_rId,
            imgW=imgW,
            imgH=imgH,
        )


class CT_GraphicalObjectFrameNonVisual(BaseOxmlElement):
    """`<p:nvGraphicFramePr>` element.

    This contains the non-visual properties of a graphic frame, such as name, id, etc.
    """

    cNvPr = OneAndOnlyOne("p:cNvPr")
    nvPr = OneAndOnlyOne("p:nvPr")


class CT_OleObject(BaseOxmlElement):
    """`<p:oleObj>` element, container for an OLE object (e.g. Excel file).

    An OLE object can be either linked or embedded (hence the name).
    """

    progId = OptionalAttribute("progId", XsdString)
    rId = OptionalAttribute("r:id", XsdString)
    showAsIcon = OptionalAttribute("showAsIcon", XsdBoolean, default=False)

    @property
    def is_embedded(self):
        """True when this OLE object is embedded, False when it is linked."""
        return True if len(self.xpath("./p:embed")) > 0 else False


class CT_RelIds(BaseOxmlElement):
    """<dgm:relIds> element.  The element that defines a Smart Art Drawing and its relationships"""
    data_rId = RequiredAttribute("r:dm", ST_RelationshipId)
    layout_rId = RequiredAttribute("r:lo", ST_RelationshipId)
    style_rId = RequiredAttribute("r:qs", ST_RelationshipId)
    colors_rId = RequiredAttribute("r:cs", ST_RelationshipId)

    _diagram_tmpl = '<dgm:relIds %s %s r:dm="%%s" r:lo="%%s" r:qs="%%s" r:cs="%%s" />' % (nsdecls("dgm"), nsdecls("r"))

    @staticmethod
    def new_diagram(dm, lo, qs, cs):

        xml = CT_RelIds._diagram_tmpl % (dm, lo, qs, cs)
        diagram = parse_xml(xml)
        return diagram
