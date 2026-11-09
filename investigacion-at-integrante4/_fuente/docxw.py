# -*- coding: utf-8 -*-
"""Escritor mínimo de DOCX (WordprocessingML) sin dependencias externas."""
import re
import struct
import zipfile
from xml.sax.saxutils import escape

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"

CM = 567          # twips por cm (aprox.)
EMU_CM = 360000


def esc(t):
    return escape(t, {'"': "&quot;"})


def png_size(path):
    with open(path, "rb") as f:
        d = f.read(24)
    return struct.unpack(">II", d[16:24])


class Doc:
    def __init__(self):
        self.body = []
        self.rels = []           # (id, type, target, external)
        self.media = []          # (zipname, path)
        self.nums = []           # numeración: lista de (numId, abstractId)
        self.cite_order = []
        self.refs = {}
        self.fig_n = 0
        self.tab_n = 0
        self.docpr = 0
        self.hyper = {}
        # página carta, márgenes NTC 1486 (sup 3, inf 2, izq 3, der 2)
        self.portrait = dict(w=12240, h=15840, top=1701, bottom=1134, left=1701, right=1134)
        self.landscape = dict(w=15840, h=12240, top=1021, bottom=1021, left=1134, right=1134, orient="landscape")
        self.cur = self.portrait

    # ------------------------------------------------------------------ util
    def text_width(self):
        return self.cur["w"] - self.cur["left"] - self.cur["right"]

    def rel(self, typ, target, external=False):
        rid = "rId%d" % (len(self.rels) + 10)
        self.rels.append((rid, typ, target, external))
        return rid

    def cite(self, keys):
        nums = []
        for k in keys:
            k = k.strip()
            if k not in self.refs:
                raise KeyError("Referencia no definida: " + k)
            if k not in self.cite_order:
                self.cite_order.append(k)
            nums.append(self.cite_order.index(k) + 1)
        nums = sorted(set(nums))
        out, i = [], 0
        while i < len(nums):
            j = i
            while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                j += 1
            if j - i >= 2:
                out.append("[%d]–[%d]" % (nums[i], nums[j]))
            else:
                out.extend("[%d]" % n for n in nums[i:j + 1])
            i = j + 1
        return ", ".join(out)

    # ------------------------------------------------------------------ runs
    def runs(self, text, size=None, color=None, bold=False, italic=False, font=None):
        """Marcado: **negrita**, //cursiva//, {c:clave1,clave2} cita IEEE, [[url|texto]] enlace."""
        text = re.sub(r"\{c:([^}]+)\}", lambda m: self.cite(m.group(1).split(",")), text)
        out = []
        pos = 0
        token = re.compile(r"(\*\*.+?\*\*|//.+?//|\[\[.+?\]\])")
        for m in token.finditer(text):
            if m.start() > pos:
                out.append(self._run(text[pos:m.start()], size, color, bold, italic, font))
            t = m.group(0)
            if t.startswith("**"):
                out.append(self._run(t[2:-2], size, color, True, italic, font))
            elif t.startswith("//"):
                out.append(self._run(t[2:-2], size, color, bold, True, font))
            else:
                url, _, label = t[2:-2].partition("|")
                rid = self.hyper.get(url)
                if rid is None:
                    rid = self.rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", url, True)
                    self.hyper[url] = rid
                out.append('<w:hyperlink r:id="%s" w:history="1">%s</w:hyperlink>'
                           % (rid, self._run(label or url, size, "0563C1", bold, italic, font, underline=True)))
            pos = m.end()
        if pos < len(text):
            out.append(self._run(text[pos:], size, color, bold, italic, font))
        return "".join(out)

    def _run(self, t, size=None, color=None, bold=False, italic=False, font=None, underline=False):
        rpr = []
        if font:
            rpr.append('<w:rFonts w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>' % (font, font, font))
        if bold:
            rpr.append("<w:b/><w:bCs/>")
        if italic:
            rpr.append("<w:i/><w:iCs/>")
        if color:
            rpr.append('<w:color w:val="%s"/>' % color)
        if size:
            rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size * 2, size * 2))
        if underline:
            rpr.append('<w:u w:val="single"/>')
        rp = "<w:rPr>%s</w:rPr>" % "".join(rpr) if rpr else ""
        parts = t.split("\n")
        xml = []
        for i, p in enumerate(parts):
            if i:
                xml.append("<w:br/>")
            for j, q in enumerate(p.split("\t")):
                if j:
                    xml.append("<w:tab/>")
                if q:
                    xml.append('<w:t xml:space="preserve">%s</w:t>' % esc(q))
        return "<w:r>%s%s</w:r>" % (rp, "".join(xml))

    # ------------------------------------------------------------------ bloques
    def p(self, text="", style=None, align=None, size=None, color=None, bold=False, italic=False,
          before=None, after=None, keep_next=False, num=None, ilvl=0, indent=None, page_break_before=False,
          line=None, ret=False, shade=None):
        ppr = []
        if style:
            ppr.append('<w:pStyle w:val="%s"/>' % style)
        if keep_next:
            ppr.append("<w:keepNext/>")
        if page_break_before:
            ppr.append("<w:pageBreakBefore/>")
        if num is not None:
            ppr.append('<w:numPr><w:ilvl w:val="%d"/><w:numId w:val="%d"/></w:numPr>' % (ilvl, num))
        if shade:
            ppr.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade)
        if before is not None or after is not None or line is not None:
            a = ""
            if before is not None:
                a += ' w:before="%d"' % before
            if after is not None:
                a += ' w:after="%d"' % after
            if line is not None:
                a += ' w:line="%d" w:lineRule="auto"' % line
            ppr.append("<w:spacing%s/>" % a)
        if indent:
            ppr.append('<w:ind w:left="%d" w:hanging="%d"/>' % indent)
        if align:
            ppr.append('<w:jc w:val="%s"/>' % align)
        xml = "<w:p>%s%s</w:p>" % ("<w:pPr>%s</w:pPr>" % "".join(ppr) if ppr else "",
                                   self.runs(text, size, color, bold, italic))
        if ret:
            return xml
        self.body.append(xml)

    def h(self, text, level=1):
        self.p(text, style="Heading%d" % level)

    def new_list(self, kind="bullet"):
        num_id = len(self.nums) + 1
        self.nums.append((num_id, 0 if kind == "bullet" else 1))
        return num_id

    def bullets(self, items, kind="bullet", size=None):
        nid = self.new_list(kind)
        for it in items:
            if isinstance(it, tuple):
                self.p(it[1], style="ListParagraph", num=nid, ilvl=it[0], size=size)
            else:
                self.p(it, style="ListParagraph", num=nid, size=size)

    def page_break(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def _sectpr(self, d):
        orient = ' w:orient="landscape"' if d.get("orient") == "landscape" else ""
        return ('<w:sectPr><w:headerReference w:type="default" r:id="rIdHdr1"/>'
                '<w:footerReference w:type="default" r:id="rIdFtr1"/>'
                '<w:pgSz w:w="%d" w:h="%d"%s/>'
                '<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" w:header="709" w:footer="567" w:gutter="0"/>'
                '<w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>'
                % (d["w"], d["h"], orient, d["top"], d["right"], d["bottom"], d["left"]))

    def section(self, landscape):
        """Cierra la sección actual y abre una nueva con la orientación indicada."""
        self.body.append("<w:p><w:pPr>%s</w:pPr></w:p>" % self._sectpr(self.cur))
        self.cur = self.landscape if landscape else self.portrait

    def caption_fig(self, text):
        self.fig_n += 1
        self.p("**Figura %d.** %s" % (self.fig_n, text), style="Caption", align="center")
        return self.fig_n

    def caption_tab(self, text):
        self.tab_n += 1
        self.p("**Tabla %d.** %s" % (self.tab_n, text), style="Caption", keep_next=True)
        return self.tab_n

    def image(self, path, width_cm, alt=""):
        w, hgt = png_size(path)
        cx = int(width_cm * EMU_CM)
        cy = int(cx * hgt / w)
        name = "media/image%d.png" % (len(self.media) + 1)
        self.media.append(("word/" + name, path))
        rid = self.rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", name)
        self.docpr += 1
        drawing = (
            '<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
            '<wp:extent cx="%d" cy="%d"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
            '<wp:docPr id="%d" name="Imagen %d" descr="%s"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="%s" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic xmlns:a="%s"><a:graphicData uri="%s">'
            '<pic:pic xmlns:pic="%s"><pic:nvPicPr><pic:cNvPr id="%d" name="image%d.png" descr="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing>'
            % (cx, cy, self.docpr, self.docpr, esc(alt), A_NS, A_NS, PIC_NS, PIC_NS, self.docpr, self.docpr, esc(alt),
               rid, cx, cy))
        self.body.append('<w:p><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="60"/><w:jc w:val="center"/></w:pPr>'
                         '<w:r>%s</w:r></w:p>' % drawing)

    def table(self, rows, widths, header_rows=1, size=9, fills=None, col_align=None, bold_first_col=False,
              full_rows=None, repeat_header=True, font_color=None):
        """rows: lista de filas; cada celda es texto (con marcado). full_rows: {indice: (texto, relleno)} filas combinadas."""
        total = sum(widths)
        tw = self.text_width()
        widths = [int(w * tw / total) for w in widths]
        o = ['<w:tbl><w:tblPr><w:tblStyle w:val="TablaInforme"/><w:tblW w:w="%d" w:type="dxa"/>' % sum(widths),
             '<w:tblBorders>'
             '<w:top w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
             '<w:left w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
             '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
             '<w:right w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
             '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
             '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
             '</w:tblBorders><w:tblLayout w:type="fixed"/>'
             '<w:tblCellMar><w:top w:w="28" w:type="dxa"/><w:left w:w="85" w:type="dxa"/>'
             '<w:bottom w:w="28" w:type="dxa"/><w:right w:w="85" w:type="dxa"/></w:tblCellMar>'
             '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
             '</w:tblPr>']
        o.append("<w:tblGrid>%s</w:tblGrid>" % "".join('<w:gridCol w:w="%d"/>' % w for w in widths))
        full_rows = full_rows or {}
        for i, row in enumerate(rows):
            hdr = i < header_rows
            trpr = "<w:cantSplit/>" + ("<w:tblHeader/>" if hdr and repeat_header else "")
            o.append("<w:tr><w:trPr>%s</w:trPr>" % trpr)
            if i in full_rows:
                txt, fill = full_rows[i]
                o.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:gridSpan w:val="%d"/>'
                         '<w:shd w:val="clear" w:color="auto" w:fill="%s"/><w:vAlign w:val="center"/></w:tcPr>%s</w:tc>'
                         % (sum(widths), len(widths), fill,
                            self.p(txt, style="TablaTexto", size=size, bold=True, color="1F3864", ret=True)))
                o.append("</w:tr>")
                continue
            for j, cell in enumerate(row):
                fill = None
                if hdr:
                    fill = "1F3864"
                elif fills and (i, j) in fills:
                    fill = fills[(i, j)]
                elif fills and (i, None) in fills:
                    fill = fills[(i, None)]
                tcpr = '<w:tcW w:w="%d" w:type="dxa"/>' % widths[j]
                if fill:
                    tcpr += '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % fill
                tcpr += '<w:vAlign w:val="%s"/>' % ("center" if hdr else "top")
                align = "center" if hdr else (col_align[j] if col_align else None)
                paras = []
                for k, part in enumerate(str(cell).split("\n\n")):
                    paras.append(self.p(part, style="TablaTexto", size=size, align=align,
                                        bold=hdr or (bold_first_col and j == 0),
                                        color="FFFFFF" if hdr else font_color, ret=True))
                o.append("<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>" % (tcpr, "".join(paras)))
            o.append("</w:tr>")
        o.append("</w:tbl>")
        self.body.append("".join(o))
        self.p("", style="TablaEspacio")

    # ------------------------------------------------------------------ guardado
    def save(self, path, header_text, title, creator):
        rels = list(self.rels)
        body = "".join(self.body) + self._sectpr(self.cur)
        doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<w:document xmlns:w="%s" xmlns:r="%s" xmlns:wp="%s" xmlns:a="%s" xmlns:pic="%s">'
               "<w:body>%s</w:body></w:document>" % (W_NS, R_NS, WP_NS, A_NS, PIC_NS, body))
        styles = STYLES
        numbering = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="%s">' % W_NS,
                     '<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>'
                     '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/>'
                     '<w:pPr><w:ind w:left="567" w:hanging="283"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:hint="default"/></w:rPr></w:lvl>'
                     '<w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="–"/><w:lvlJc w:val="left"/>'
                     '<w:pPr><w:ind w:left="1134" w:hanging="283"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:hint="default"/></w:rPr></w:lvl>'
                     '</w:abstractNum>',
                     '<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="hybridMultilevel"/>'
                     '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/>'
                     '<w:pPr><w:ind w:left="567" w:hanging="340"/></w:pPr></w:lvl>'
                     '<w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="lowerLetter"/><w:lvlText w:val="%2)"/><w:lvlJc w:val="left"/>'
                     '<w:pPr><w:ind w:left="1134" w:hanging="340"/></w:pPr></w:lvl>'
                     '</w:abstractNum>']
        for (nid, aid) in self.nums:
            numbering.append('<w:num w:numId="%d"><w:abstractNumId w:val="%d"/>'
                             '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>' % (nid, aid))
        numbering.append("</w:numbering>")
        header = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr xmlns:w="%s" xmlns:r="%s">'
                  '<w:p><w:pPr><w:pStyle w:val="Encabezado"/><w:jc w:val="right"/></w:pPr>%s</w:p></w:hdr>'
                  % (W_NS, R_NS, self._run(header_text, 8, "7F7F7F")))
        footer = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr xmlns:w="%s" xmlns:r="%s">'
                  '<w:p><w:pPr><w:pStyle w:val="PiePagina"/><w:jc w:val="center"/></w:pPr>'
                  '<w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">Página </w:t></w:r>'
                  '<w:fldSimple w:instr=" PAGE "><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>'
                  '</w:p></w:ftr>' % (W_NS, R_NS))
        settings = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings xmlns:w="%s">'
                    '<w:zoom w:percent="100"/><w:defaultTabStop w:val="709"/><w:hyphenationZone w:val="425"/>'
                    '<w:characterSpacingControl w:val="doNotCompress"/>'
                    '<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>'
                    '<w:decimalSymbol w:val=","/><w:listSeparator w:val=";"/></w:settings>' % W_NS)
        docrels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
                   '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>',
                   '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>',
                   '<Relationship Id="rIdHdr1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>',
                   '<Relationship Id="rIdFtr1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>']
        for (rid, typ, target, ext) in rels:
            docrels.append('<Relationship Id="%s" Type="%s" Target="%s"%s/>' % (
                rid, typ, esc(target), ' TargetMode="External"' if ext else ""))
        docrels.append("</Relationships>")
        ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
              '<Default Extension="xml" ContentType="application/xml"/>'
              '<Default Extension="png" ContentType="image/png"/>'
              '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
              '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
              '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
              '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
              '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
              '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
              '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
              '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
              "</Types>")
        rootrels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                    "</Relationships>")
        core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
                'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                "<dc:title>%s</dc:title><dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>"
                '<dc:language>es-CO</dc:language>'
                '<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-09T12:00:00Z</dcterms:created>'
                '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-11-09T12:00:00Z</dcterms:modified>'
                "</cp:coreProperties>") % (esc(title), esc(creator), esc(creator))
        app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
               "<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity></Properties>")
        parts = {"[Content_Types].xml": ct, "_rels/.rels": rootrels, "word/document.xml": doc,
                 "word/styles.xml": styles, "word/settings.xml": settings, "word/numbering.xml": "".join(numbering),
                 "word/header1.xml": header, "word/footer1.xml": footer, "word/_rels/document.xml.rels": "".join(docrels),
                 "docProps/core.xml": core, "docProps/app.xml": app}
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for name in ["[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/_rels/document.xml.rels",
                         "word/styles.xml", "word/settings.xml", "word/numbering.xml", "word/header1.xml",
                         "word/footer1.xml", "docProps/core.xml", "docProps/app.xml"]:
                z.writestr(name, parts[name])
            for (zname, p) in self.media:
                z.write(p, zname)
        return parts


STYLES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<w:styles xmlns:w="%s">' % W_NS +
          '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:eastAsia="Arial" w:hAnsi="Arial" w:cs="Arial"/>'
          '<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="es-CO" w:eastAsia="en-US" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
          '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>'
          '<w:pPr><w:jc w:val="both"/></w:pPr></w:style>'
          '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>'
          '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/>'
          '<w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
          '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'
          '<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/><w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/></w:style>'
          '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/>'
          '<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/><w:outlineLvl w:val="0"/></w:pPr>'
          '<w:rPr><w:b/><w:bCs/><w:color w:val="1F3864"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>'
          '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/>'
          '<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="100"/><w:jc w:val="left"/><w:outlineLvl w:val="1"/></w:pPr>'
          '<w:rPr><w:b/><w:bCs/><w:color w:val="1F3864"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
          '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/>'
          '<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="200" w:after="80"/><w:jc w:val="left"/><w:outlineLvl w:val="2"/></w:pPr>'
          '<w:rPr><w:b/><w:bCs/><w:color w:val="2F5496"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>'
          '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="10"/><w:qFormat/>'
          '<w:pPr><w:spacing w:before="240" w:after="240"/><w:jc w:val="center"/></w:pPr>'
          '<w:rPr><w:b/><w:bCs/><w:color w:val="1F3864"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>'
          '<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="35"/><w:unhideWhenUsed/><w:qFormat/>'
          '<w:pPr><w:spacing w:before="60" w:after="160" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
          '<w:rPr><w:i/><w:iCs/><w:color w:val="404040"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>'
          '<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:uiPriority w:val="34"/><w:qFormat/>'
          '<w:pPr><w:spacing w:after="60"/><w:ind w:left="720"/><w:contextualSpacing/></w:pPr></w:style>'
          '<w:style w:type="paragraph" w:customStyle="1" w:styleId="TablaTexto"><w:name w:val="Tabla texto"/><w:basedOn w:val="Normal"/><w:qFormat/>'
          '<w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
          '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>'
          '<w:style w:type="paragraph" w:customStyle="1" w:styleId="TablaEspacio"><w:name w:val="Tabla espacio"/><w:basedOn w:val="Normal"/>'
          '<w:pPr><w:spacing w:before="0" w:after="120" w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="12"/><w:szCs w:val="12"/></w:rPr></w:style>'
          '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Referencia"><w:name w:val="Referencia IEEE"/><w:basedOn w:val="Normal"/><w:qFormat/>'
          '<w:pPr><w:spacing w:after="80" w:line="240" w:lineRule="auto"/><w:ind w:left="567" w:hanging="567"/><w:jc w:val="left"/></w:pPr>'
          '<w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>'
          '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Encabezado"><w:name w:val="Encabezado"/><w:basedOn w:val="Normal"/>'
          '<w:pPr><w:spacing w:after="0"/></w:pPr></w:style>'
          '<w:style w:type="paragraph" w:customStyle="1" w:styleId="PiePagina"><w:name w:val="Pie de pagina"/><w:basedOn w:val="Normal"/>'
          '<w:pPr><w:spacing w:after="0"/></w:pPr></w:style>'
          '<w:style w:type="table" w:customStyle="1" w:styleId="TablaInforme"><w:name w:val="Tabla informe"/><w:basedOn w:val="TableNormal"/><w:uiPriority w:val="59"/>'
          '<w:tblPr><w:tblCellMar><w:left w:w="85" w:type="dxa"/><w:right w:w="85" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'
          "</w:styles>")
