# -*- coding: utf-8 -*-
"""Escritor mínimo de XLSX (SpreadsheetML) sin dependencias externas."""
import copy
import zipfile
from xml.sax.saxutils import escape

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def col_letter(c):
    s = ""
    while c:
        c, rem = divmod(c - 1, 26)
        s = chr(65 + rem) + s
    return s


def ref(r, c):
    return "%s%d" % (col_letter(c), r)


BASE = {
    "font": ("Arial", 8, False, False, "000000"),
    "fill": None,
    "border": {"l": None, "r": None, "t": None, "b": None},
    "h": "left", "v": "center", "wrap": True, "indent": 0,
}


def style(**kw):
    st = copy.deepcopy(BASE)
    for k, v in kw.items():
        if k == "border":
            st["border"].update(v)
        else:
            st[k] = v
    return st


class Sheet:
    def __init__(self, name):
        self.name = name
        self.cells = {}
        self.merges = []
        self.row_heights = {}
        self.col_widths = {}
        self.row_breaks = []
        self.print_area = None
        self.print_titles = None
        self.orientation = "portrait"
        self.fit_width = True
        self.footer = None
        self.show_grid = False
        self.zoom = 100
        self.freeze = None

    # ---- celdas ----
    def set(self, r, c, value=None, st=None):
        cell = self.cells.setdefault((r, c), {"v": None, "st": copy.deepcopy(BASE)})
        if value is not None:
            cell["v"] = value
        if st is not None:
            cell["st"] = copy.deepcopy(st)
        return cell

    def area(self, r1, c1, r2, c2, value, st):
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                self.set(r, c, None, st)
        if value is not None:
            self.cells[(r1, c1)]["v"] = value
        if (r1, c1) != (r2, c2):
            for (a, b, cc, d) in self.merges:
                if not (r2 < a or r1 > cc or c2 < b or c1 > d):
                    raise ValueError("Combinación superpuesta %s con %s" % (
                        ref(r1, c1) + ":" + ref(r2, c2), ref(a, b) + ":" + ref(cc, d)))
            self.merges.append((r1, c1, r2, c2))

    def outline(self, r1, c1, r2, c2, kind="thin", color="000000"):
        side = (kind, color)
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                cell = self.set(r, c)
                b = cell["st"]["border"]
                if r == r1:
                    b["t"] = side
                if r == r2:
                    b["b"] = side
                if c == c1:
                    b["l"] = side
                if c == c2:
                    b["r"] = side


class Styles:
    def __init__(self):
        self.fonts, self.fills, self.borders, self.xfs = [], [None, "gray125"], [], []
        self.fid, self.flid, self.bid, self.xid = {}, {}, {}, {}
        self.xf(copy.deepcopy(BASE))

    def _font(self, f):
        if f not in self.fid:
            self.fid[f] = len(self.fonts)
            self.fonts.append(f)
        return self.fid[f]

    def _fill(self, color):
        if color is None:
            return 0
        if color not in self.flid:
            self.flid[color] = len(self.fills)
            self.fills.append(color)
        return self.flid[color]

    def _border(self, b):
        key = (b["l"], b["r"], b["t"], b["b"])
        if key not in self.bid:
            self.bid[key] = len(self.borders)
            self.borders.append(key)
        return self.bid[key]

    def xf(self, st):
        key = (self._font(tuple(st["font"])), self._fill(st["fill"]), self._border(st["border"]),
               st["h"], st["v"], bool(st["wrap"]), st["indent"])
        if key not in self.xid:
            self.xid[key] = len(self.xfs)
            self.xfs.append(key)
        return self.xid[key]

    def xml(self):
        o = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
             '<styleSheet xmlns="%s">' % NS_MAIN]
        o.append('<fonts count="%d">' % len(self.fonts))
        for (name, size, bold, italic, color) in self.fonts:
            o.append("<font>%s%s<sz val=\"%s\"/><color rgb=\"FF%s\"/><name val=\"%s\"/><family val=\"2\"/></font>"
                     % ("<b/>" if bold else "", "<i/>" if italic else "", size, color, name))
        o.append("</fonts>")
        o.append('<fills count="%d">' % len(self.fills))
        for f in self.fills:
            if f is None:
                o.append('<fill><patternFill patternType="none"/></fill>')
            elif f == "gray125":
                o.append('<fill><patternFill patternType="gray125"/></fill>')
            else:
                o.append('<fill><patternFill patternType="solid"><fgColor rgb="FF%s"/><bgColor indexed="64"/></patternFill></fill>' % f)
        o.append("</fills>")
        o.append('<borders count="%d">' % len(self.borders))
        for (l, r, t, b) in self.borders:
            s = ["<border>"]
            for tag, v in (("left", l), ("right", r), ("top", t), ("bottom", b)):
                if v:
                    s.append('<%s style="%s"><color rgb="FF%s"/></%s>' % (tag, v[0], v[1], tag))
                else:
                    s.append("<%s/>" % tag)
            s.append("<diagonal/></border>")
            o.append("".join(s))
        o.append("</borders>")
        o.append('<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>')
        o.append('<cellXfs count="%d">' % len(self.xfs))
        for (fo, fi, bo, h, v, wrap, ind) in self.xfs:
            al = '<alignment horizontal="%s" vertical="%s"%s%s/>' % (
                h, v, ' wrapText="1"' if wrap else "", (' indent="%d"' % ind) if ind else "")
            o.append('<xf numFmtId="49" fontId="%d" fillId="%d" borderId="%d" xfId="0" applyNumberFormat="1" '
                     'applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">%s</xf>' % (fo, fi, bo, al))
        o.append("</cellXfs>")
        o.append('<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>')
        o.append('<dxfs count="0"/><tableStyles count="0" defaultTableStyle="TableStyleMedium2" defaultPivotStyle="PivotStyleLight16"/>')
        o.append("</styleSheet>")
        return "".join(o)


def sheet_xml(sh, styles):
    rows = sorted(set(r for r, c in sh.cells))
    maxr = max(rows) if rows else 1
    maxc = max(c for r, c in sh.cells) if sh.cells else 1
    o = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
         '<worksheet xmlns="%s" xmlns:r="%s">' % (NS_MAIN, NS_R)]
    o.append('<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>' if sh.fit_width else "<sheetPr/>")
    o.append('<dimension ref="A1:%s"/>' % ref(maxr, maxc))
    o.append('<sheetViews><sheetView %sworkbookViewId="0" zoomScale="%d" zoomScaleNormal="%d">'
             % ('showGridLines="0" ' if not sh.show_grid else "", sh.zoom, sh.zoom))
    if sh.freeze:
        fr, fc = sh.freeze
        o.append('<pane ySplit="%d" topLeftCell="%s" activePane="bottomLeft" state="frozen"/>' % (fr - 1, ref(fr, fc)))
        o.append('<selection pane="bottomLeft" activeCell="%s" sqref="%s"/>' % (ref(fr, fc), ref(fr, fc)))
    else:
        o.append('<selection activeCell="A1" sqref="A1"/>')
    o.append("</sheetView></sheetViews>")
    o.append('<sheetFormatPr defaultRowHeight="12.75"/>')
    if sh.col_widths:
        o.append("<cols>")
        for c in sorted(sh.col_widths):
            o.append('<col min="%d" max="%d" width="%s" customWidth="1"/>' % (c, c, sh.col_widths[c]))
        o.append("</cols>")
    o.append("<sheetData>")
    for r in range(1, maxr + 1):
        cols = sorted(c for rr, c in sh.cells if rr == r)
        attrs = ' r="%d"' % r
        if r in sh.row_heights:
            attrs += ' ht="%s" customHeight="1"' % sh.row_heights[r]
        if not cols:
            if r in sh.row_heights:
                o.append("<row%s/>" % attrs)
            continue
        o.append("<row%s>" % attrs)
        for c in cols:
            cell = sh.cells[(r, c)]
            s = styles.xf(cell["st"])
            v = cell["v"]
            if v is None or v == "":
                o.append('<c r="%s" s="%d"/>' % (ref(r, c), s))
            else:
                o.append('<c r="%s" s="%d" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>'
                         % (ref(r, c), s, escape(str(v))))
        o.append("</row>")
    o.append("</sheetData>")
    if sh.merges:
        o.append('<mergeCells count="%d">' % len(sh.merges))
        for (r1, c1, r2, c2) in sh.merges:
            o.append('<mergeCell ref="%s:%s"/>' % (ref(r1, c1), ref(r2, c2)))
        o.append("</mergeCells>")
    o.append('<printOptions horizontalCentered="1"/>')
    o.append('<pageMargins left="0.35" right="0.35" top="0.45" bottom="0.5" header="0.2" footer="0.25"/>')
    o.append('<pageSetup paperSize="1" orientation="%s"%s/>' % (
        sh.orientation, ' fitToWidth="1" fitToHeight="0"' if sh.fit_width else ""))
    if sh.footer:
        o.append("<headerFooter><oddFooter>%s</oddFooter></headerFooter>" % escape(sh.footer))
    if sh.row_breaks:
        o.append('<rowBreaks count="%d" manualBreakCount="%d">' % (len(sh.row_breaks), len(sh.row_breaks)))
        for b in sh.row_breaks:
            o.append('<brk id="%d" max="16383" man="1"/>' % b)
        o.append("</rowBreaks>")
    o.append('<ignoredErrors><ignoredError sqref="A1:%s" numberStoredAsText="1"/></ignoredErrors>' % ref(maxr + 5, max(maxc, 5)))
    o.append("</worksheet>")
    return "".join(o)


def save(path, sheets, title="", creator=""):
    styles = Styles()
    sheet_parts = [sheet_xml(sh, styles) for sh in sheets]
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
          '<Default Extension="xml" ContentType="application/xml"/>',
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>']
    for i in range(len(sheets)):
        ct.append('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % (i + 1))
    ct += ['<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
           '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
           '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
           "</Types>"]
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
            "</Relationships>")
    wb = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<workbook xmlns="%s" xmlns:r="%s">' % (NS_MAIN, NS_R),
          '<workbookPr/>',
          '<bookViews><workbookView xWindow="0" yWindow="0" windowWidth="28800" windowHeight="15000" activeTab="0"/></bookViews>',
          "<sheets>"]
    for i, sh in enumerate(sheets):
        wb.append('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (escape(sh.name), i + 1, i + 1))
    wb.append("</sheets>")
    dn = []
    for i, sh in enumerate(sheets):
        qn = "'%s'" % sh.name.replace("'", "''")
        if sh.print_area:
            dn.append('<definedName name="_xlnm.Print_Area" localSheetId="%d">%s!%s</definedName>' % (i, escape(qn), sh.print_area))
        if sh.print_titles:
            dn.append('<definedName name="_xlnm.Print_Titles" localSheetId="%d">%s!%s</definedName>' % (i, escape(qn), sh.print_titles))
    if dn:
        wb.append("<definedNames>%s</definedNames>" % "".join(dn))
    wb.append('<calcPr calcId="191029"/></workbook>')
    wbrels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
              '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for i in range(len(sheets)):
        wbrels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet%d.xml"/>' % (i + 1, i + 1))
    wbrels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' % (len(sheets) + 1))
    wbrels.append("</Relationships>")
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            "<dc:title>%s</dc:title><dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>"
            '<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-09T12:00:00Z</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-11-09T12:00:00Z</dcterms:modified>'
            "</cp:coreProperties>") % (escape(title), escape(creator), escape(creator))
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           "<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>"
           "</Properties>")
    styles_xml = styles.xml()
    parts = {"[Content_Types].xml": "".join(ct), "_rels/.rels": rels, "xl/workbook.xml": "".join(wb),
             "xl/_rels/workbook.xml.rels": "".join(wbrels), "xl/styles.xml": styles_xml,
             "docProps/core.xml": core, "docProps/app.xml": app}
    for i, sp in enumerate(sheet_parts):
        parts["xl/worksheets/sheet%d.xml" % (i + 1)] = sp
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ["[Content_Types].xml", "_rels/.rels", "docProps/core.xml", "docProps/app.xml",
                     "xl/workbook.xml", "xl/_rels/workbook.xml.rels", "xl/styles.xml"] + \
                    ["xl/worksheets/sheet%d.xml" % (i + 1) for i in range(len(sheets))]:
            z.writestr(name, parts[name])
    return parts


def html_preview(sh, px_per_width=7.0, pt_to_px=1.333, zoom=1.0):
    """Vista previa aproximada en HTML para revisar el diseño."""
    maxr = max(r for r, c in sh.cells)
    maxc = max(c for r, c in sh.cells)
    covered = {}
    for (r1, c1, r2, c2) in sh.merges:
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                covered[(r, c)] = (r1, c1, r2, c2)
    o = ['<html><head><meta charset="utf-8"><style>td{overflow:hidden;padding:0 2px;font-family:Arial}</style></head>'
         '<body style="margin:8px;background:#fff;zoom:%s"><table' % zoom + ' style="border-collapse:collapse;table-layout:fixed">']
    o.append("<colgroup>%s</colgroup>" % "".join(
        '<col style="width:%dpx">' % int(float(sh.col_widths.get(c, 8.43)) * px_per_width + 5) for c in range(1, maxc + 1)))
    for r in range(1, maxr + 1):
        h = float(sh.row_heights.get(r, 12.75)) * pt_to_px
        o.append('<tr style="height:%dpx">' % h)
        for c in range(1, maxc + 1):
            m = covered.get((r, c))
            if m and (m[0], m[1]) != (r, c):
                continue
            cell = sh.cells.get((r, c), {"v": None, "st": BASE})
            st = cell["st"]
            span = ""
            bst = st
            if m:
                span = ' rowspan="%d" colspan="%d"' % (m[2] - m[0] + 1, m[3] - m[1] + 1)
                br = sh.cells.get((m[2], m[3]), cell)["st"]["border"]
                bl = sh.cells.get((m[2], m[1]), cell)["st"]["border"]
                tr_ = sh.cells.get((m[0], m[3]), cell)["st"]["border"]
                bdr = {"t": st["border"]["t"], "l": st["border"]["l"], "r": tr_["r"], "b": bl["b"]}
            else:
                bdr = st["border"]
            css = []
            for k, side in (("t", "top"), ("b", "bottom"), ("l", "left"), ("r", "right")):
                v = bdr.get(k)
                if v:
                    css.append("border-%s:%s solid #%s" % (side, "2px" if v[0] == "medium" else "1px", v[1]))
            f = st["font"]
            css.append("font-size:%.1fpx" % (f[1] * pt_to_px))
            if f[2]:
                css.append("font-weight:bold")
            if f[3]:
                css.append("font-style:italic")
            css.append("color:#%s" % f[4])
            if st["fill"]:
                css.append("background:#%s" % st["fill"])
            css.append("text-align:%s" % st["h"])
            css.append("vertical-align:%s" % {"center": "middle", "top": "top", "bottom": "bottom"}[st["v"]])
            css.append("white-space:%s" % ("pre-wrap" if st["wrap"] else "pre"))
            v = cell["v"] or ""
            o.append('<td%s style="%s">%s</td>' % (span, ";".join(css), escape(str(v))))
        o.append("</tr>")
    o.append("</table></body></html>")
    return "".join(o)
