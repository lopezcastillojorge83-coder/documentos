# -*- coding: utf-8 -*-
"""Escribe un .docx (OOXML) usando solo la biblioteca estándar de Python."""
import os
import re
import struct
import zipfile
from xml.sax.saxutils import escape, quoteattr

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = (f'xmlns:w="{W}" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')
DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

AZUL, AZUL2, GRIS, BORDE = "1F3A5F", "2E6DA4", "475569", "B8C4D6"
FONDO_COL0 = "EAF0F7"
A4_W, A4_H = 11906, 16838
MARG_V, MARG_H = 1418, 850        # márgenes en vertical y en apaisado (twips)
ANCHO_V = A4_W - 2 * MARG_V       # ancho útil en vertical: 9070 twips
CM = 360000                       # EMU por cm

_MARCA = re.compile(r"(\*\*.+?\*\*|\*.+?\*)")


def partes(texto):
    """'a **b** *c*' -> [(texto, negrita, cursiva), ...]"""
    res = []
    for t in _MARCA.split(texto):
        if not t:
            continue
        if t.startswith("**") and t.endswith("**") and len(t) > 4:
            res.append((t[2:-2], True, False))
        elif t.startswith("*") and t.endswith("*") and len(t) > 2:
            res.append((t[1:-1], False, True))
        else:
            res.append((t, False, False))
    return res


def run(txt, b=False, i=False, color=None, sz=None):
    pr = ""
    if b:
        pr += "<w:b/><w:bCs/>"
    if i:
        pr += "<w:i/><w:iCs/>"
    if color:
        pr += f'<w:color w:val="{color}"/>'
    if sz:
        pr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    pr = f"<w:rPr>{pr}</w:rPr>" if pr else ""
    cuerpo = "<w:br/>".join(
        f'<w:t xml:space="preserve">{escape(t)}</w:t>' for t in txt.split("\n"))
    return f"<w:r>{pr}{cuerpo}</w:r>"


def runs(texto, b=False, i=False, color=None, sz=None):
    return "".join(run(t, b or tb, i or ti, color, sz) for t, tb, ti in partes(texto))


def p(texto="", estilo=None, jc=None, antes=None, despues=None, izq=None,
      colg=None, keep=False, num=False, borde_inf=None, sect="", **fmt):
    """Párrafo. El orden de los hijos de w:pPr sigue el esquema OOXML."""
    ppr = ""
    if estilo:
        ppr += f'<w:pStyle w:val="{estilo}"/>'
    if keep:
        ppr += "<w:keepNext/>"
    if num:
        ppr += '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
    if borde_inf:
        ppr += (f'<w:pBdr><w:bottom w:val="single" w:sz="{borde_inf[0]}" '
                f'w:space="6" w:color="{borde_inf[1]}"/></w:pBdr>')
    sp = ""
    if antes is not None:
        sp += f' w:before="{antes}"'
    if despues is not None:
        sp += f' w:after="{despues}"'
    if sp:
        ppr += f"<w:spacing{sp}/>"
    if izq is not None or colg is not None:
        h = f' w:hanging="{colg}"' if colg else ""
        ppr += f'<w:ind w:left="{izq or 0}"{h}/>'
    if jc:
        ppr += f'<w:jc w:val="{jc}"/>'
    ppr += sect
    ppr = f"<w:pPr>{ppr}</w:pPr>" if ppr else ""
    return f"<w:p>{ppr}{runs(texto, **fmt) if texto else ''}</w:p>"


def espaciador(alto=140):
    return ('<w:p><w:pPr><w:spacing w:before="0" w:after="0" '
            f'w:line="{alto}" w:lineRule="exact"/></w:pPr></w:p>')


def celda(contenido, ancho, fill=None, color=None, b=False, sz=20):
    items = contenido if isinstance(contenido, list) else [contenido]
    ps = ""
    for it in items:
        if it.startswith("• "):
            ps += p(it[2:], num=True, izq=284, colg=284, despues=30,
                    sz=sz, color=color, b=b)
        else:
            ps += p(it, despues=40, sz=sz, color=color, b=b)
    tcpr = f'<w:tcW w:w="{ancho}" w:type="dxa"/>'
    if fill:
        tcpr += f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
    return f"<w:tc><w:tcPr>{tcpr}</w:tcPr>{ps}</w:tc>"


def _bordes(ligera):
    v = "nil" if ligera else "single"
    lados = [("top", "single"), ("left", v), ("bottom", "single"),
             ("right", v), ("insideH", "single"), ("insideV", v)]
    return "".join(f'<w:{n} w:val="{val}" w:sz="4" w:space="0" w:color="{BORDE}"/>'
                   for n, val in lados)


def tabla(spec, total=ANCHO_V):
    ws = [round(total * x / 100) for x in spec["anchos"]]
    ws[-1] += total - sum(ws)
    sz = spec.get("sz", 20)
    tblpr = (f'<w:tblW w:w="{total}" w:type="dxa"/>'
             f'<w:tblBorders>{_bordes(spec.get("ligera"))}</w:tblBorders>'
             '<w:tblLayout w:type="fixed"/>'
             '<w:tblCellMar><w:top w:w="70" w:type="dxa"/><w:left w:w="110" w:type="dxa"/>'
             '<w:bottom w:w="50" w:type="dxa"/><w:right w:w="110" w:type="dxa"/></w:tblCellMar>')
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in ws)
    filas = ""
    if spec.get("cab"):
        trpr = "<w:cantSplit/>" + ("<w:tblHeader/>" if spec.get("repetir_cab") else "")
        celdas = "".join(celda(c, w, fill=AZUL, color="FFFFFF", b=True, sz=sz)
                         for c, w in zip(spec["cab"], ws))
        filas += f"<w:tr><w:trPr>{trpr}</w:trPr>{celdas}</w:tr>"
    for fila in spec["filas"]:
        celdas = "".join(
            celda(c, w, fill=FONDO_COL0 if (k == 0 and spec.get("fondo_col0")) else None, sz=sz)
            for k, (c, w) in enumerate(zip(fila, ws)))
        filas += f"<w:tr><w:trPr><w:cantSplit/></w:trPr>{celdas}</w:tr>"
    return f"<w:tbl><w:tblPr>{tblpr}</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{filas}</w:tbl>"


def nota(texto):
    nil = "".join(f'<w:{n} w:val="nil"/>' for n in
                  ("top", "left", "bottom", "right", "insideH", "insideV"))
    cel = (f'<w:tc><w:tcPr><w:tcW w:w="{ANCHO_V}" w:type="dxa"/>'
           '<w:tcBorders><w:left w:val="single" w:sz="24" w:space="0" w:color="E0A100"/></w:tcBorders>'
           '<w:shd w:val="clear" w:color="auto" w:fill="FFF6DB"/></w:tcPr>'
           f'{p(texto, despues=0, sz=20)}</w:tc>')
    return (f'<w:tbl><w:tblPr><w:tblW w:w="{ANCHO_V}" w:type="dxa"/>'
            f'<w:tblBorders>{nil}</w:tblBorders><w:tblLayout w:type="fixed"/>'
            '<w:tblCellMar><w:top w:w="100" w:type="dxa"/><w:left w:w="180" w:type="dxa"/>'
            '<w:bottom w:w="100" w:type="dxa"/><w:right w:w="140" w:type="dxa"/></w:tblCellMar>'
            f'</w:tblPr><w:tblGrid><w:gridCol w:w="{ANCHO_V}"/></w:tblGrid>'
            f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{cel}</w:tr></w:tbl>')


def portada(d):
    x = p("", antes=1500, despues=0)
    x += p(d["titulo"], antes=0, despues=160, b=True, color=AZUL, sz=52)
    x += p(d["subtitulo"], despues=420, color="334155", sz=30, borde_inf=(12, AZUL2))
    x += tabla({"anchos": [24, 76], "ligera": True, "sz": 22,
                "filas": [[f"**{k}**", v] for k, v in d["datos"]]})
    x += p("", antes=360, despues=0)
    x += p("Integrantes", b=True, color=AZUL, sz=26, despues=100, keep=True)
    x += tabla({"anchos": [9, 61, 30], "sz": 22, "cab": ["N.º", "Nombre completo", "Código"],
                "filas": [list(f) for f in d["integrantes"]]})
    return x


def figura(spec, ruta):
    with open(ruta, "rb") as f:
        cab = f.read(24)
    w_px, h_px = struct.unpack(">II", cab[16:24])
    cx = int(spec["ancho_cm"] * CM)
    cy = int(cx * h_px / w_px)
    alt = quoteattr("Árbol de causas de la caída de altura desde un andamio (NTP 274)")
    dibujo = (
        '<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="1" name="Figura 1" descr={alt}/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic><pic:nvPicPr><pic:cNvPr id="1" name="arbol_de_causas.png"/><pic:cNvPicPr/>'
        '</pic:nvPicPr><pic:blipFill><a:blip r:embed="rIdImg"/><a:stretch><a:fillRect/></a:stretch>'
        f'</pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
        '</a:graphicData></a:graphic></wp:inline></w:drawing>')
    img = ('<w:p><w:pPr><w:keepNext/><w:spacing w:before="0" w:after="40" w:line="240" '
           f'w:lineRule="auto"/><w:jc w:val="center"/></w:pPr><w:r>{dibujo}</w:r></w:p>')
    return img + p(spec["pie"], estilo="Caption", jc="center")


def sect(orient, refs=True):
    if orient == "h":
        pg = f'<w:pgSz w:w="{A4_H}" w:h="{A4_W}" w:orient="landscape"/>'
        m = MARG_H
        mar = (f'<w:pgMar w:top="{m}" w:right="{m}" w:bottom="{m}" w:left="{m}" '
               'w:header="340" w:footer="340" w:gutter="0"/>')
    else:
        pg = f'<w:pgSz w:w="{A4_W}" w:h="{A4_H}"/>'
        m = MARG_V
        mar = (f'<w:pgMar w:top="{m}" w:right="{m}" w:bottom="{m}" w:left="{m}" '
               'w:header="709" w:footer="709" w:gutter="0"/>')
    ref = ('<w:headerReference w:type="default" r:id="rIdH"/>'
           '<w:footerReference w:type="default" r:id="rIdF"/>') if refs else ""
    return f"<w:sectPr>{ref}{pg}{mar}</w:sectPr>"


def portador(sectpr):
    """Párrafo mínimo que lleva las propiedades de sección."""
    return ('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="20" '
            f'w:lineRule="exact"/>{sectpr}</w:pPr></w:p>')


def cuerpo(bloques, dir_img):
    x, previo = "", None
    for b in bloques:
        k = b[0]
        if k == "portada":
            x += portada(b[1]) + portador(sect("v", refs=False))
        elif k == "h1":
            # sin espacio superior si abre página (tras portada o salto de sección)
            antes = 0 if previo in ("portada", "seccion") else None
            x += p(b[1], estilo="Heading1", antes=antes)
        elif k == "h2":
            x += p(b[1], estilo="Heading2")
        elif k == "p":
            x += p(b[1])
        elif k == "nota":
            x += nota(b[1]) + espaciador()
        elif k == "bullets":
            x += "".join(p(t, num=True, despues=60) for t in b[1])
        elif k == "tabla":
            x += tabla(b[1]) + espaciador()
        elif k == "figura":
            x += figura(b[1], os.path.join(dir_img, b[1]["archivo"]))
        elif k == "seccion":  # cierra la sección que termina en este punto
            x += portador(sect("v" if b[1] == "horizontal" else "h"))
        else:
            raise ValueError(f"bloque desconocido: {k}")
        previo = k
    return x


def _estilo(tipo, sid, nombre, extra="", ppr="", rpr="", defecto=False):
    d = ' w:default="1"' if defecto else ""
    ppr = f"<w:pPr>{ppr}</w:pPr>" if ppr else ""
    rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return (f'<w:style w:type="{tipo}"{d} w:styleId="{sid}"><w:name w:val="{nombre}"/>'
            f'{extra}{ppr}{rpr}</w:style>')


def estilos_xml():
    base = '<w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
    s = _estilo("paragraph", "Normal", "Normal", "<w:qFormat/>", defecto=True)
    s += _estilo("character", "DefaultParagraphFont", "Default Paragraph Font",
                 '<w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/>', defecto=True)
    s += ('<w:style w:type="table" w:default="1" w:styleId="TableNormal">'
          '<w:name w:val="Normal Table"/><w:uiPriority w:val="99"/><w:semiHidden/>'
          '<w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar>'
          '<w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
          '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/>'
          '</w:tblCellMar></w:tblPr></w:style>')
    s += _estilo("paragraph", "Heading1", "heading 1", base,
                 '<w:keepNext/><w:keepLines/><w:spacing w:before="360" w:after="120"/>'
                 '<w:outlineLvl w:val="0"/>',
                 f'<w:b/><w:bCs/><w:color w:val="{AZUL}"/><w:sz w:val="32"/><w:szCs w:val="32"/>')
    s += _estilo("paragraph", "Heading2", "heading 2", base,
                 '<w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="80"/>'
                 '<w:outlineLvl w:val="1"/>',
                 f'<w:b/><w:bCs/><w:color w:val="{AZUL2}"/><w:sz w:val="26"/><w:szCs w:val="26"/>')
    s += _estilo("paragraph", "Caption", "caption", base,
                 '<w:spacing w:before="60" w:after="120"/>',
                 '<w:i/><w:iCs/><w:color w:val="64748B"/><w:sz w:val="18"/><w:szCs w:val="18"/>')
    return (DECL + f'<w:styles xmlns:w="{W}"><w:docDefaults><w:rPrDefault><w:rPr>'
            '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>'
            '<w:sz w:val="22"/><w:szCs w:val="22"/>'
            '<w:lang w:val="es-ES" w:eastAsia="en-US" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
            '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/>'
            f'</w:pPr></w:pPrDefault></w:docDefaults>{s}</w:styles>')


def numeracion_xml():
    return (DECL + f'<w:numbering xmlns:w="{W}"><w:abstractNum w:abstractNumId="0">'
            '<w:multiLevelType w:val="hybridMultilevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/>'
            '<w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/>'
            '<w:pPr><w:ind w:left="357" w:hanging="357"/></w:pPr>'
            '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri" w:hint="default"/>'
            f'<w:color w:val="{AZUL2}"/></w:rPr></w:lvl></w:abstractNum>'
            '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>')


def encabezado_xml(texto):
    r = run(texto, color="64748B", sz=18)
    return (DECL + f'<w:hdr {NS}><w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="4" '
            f'w:space="4" w:color="{BORDE}"/></w:pBdr><w:spacing w:before="0" w:after="0"/>'
            f'<w:jc w:val="right"/></w:pPr>{r}</w:p></w:hdr>')


def pie_xml():
    rpr = '<w:rPr><w:color w:val="64748B"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
    campo = (f'<w:r>{rpr}<w:fldChar w:fldCharType="begin"/></w:r>'
             f'<w:r>{rpr}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
             f'<w:r>{rpr}<w:fldChar w:fldCharType="separate"/></w:r>'
             f'<w:r>{rpr}<w:t>1</w:t></w:r><w:r>{rpr}<w:fldChar w:fldCharType="end"/></w:r>')
    return (DECL + f'<w:ftr {NS}><w:p><w:pPr><w:spacing w:before="0" w:after="0"/>'
            f'<w:jc w:val="center"/></w:pPr>{run("Página ", color="64748B", sz=18)}{campo}'
            '</w:p></w:ftr>')


REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT_W = "application/vnd.openxmlformats-officedocument.wordprocessingml"


def escribir_docx(bloques, ruta_docx, dir_img, titulo, texto_encabezado):
    doc = (DECL + f'<w:document {NS}><w:body>{cuerpo(bloques, dir_img)}'
           f'{sect("v")}</w:body></w:document>')
    figura_png = next(b[1]["archivo"] for b in bloques if b[0] == "figura")
    ct = (DECL + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="png" ContentType="image/png"/>'
          f'<Override PartName="/word/document.xml" ContentType="{CT_W}.document.main+xml"/>'
          f'<Override PartName="/word/styles.xml" ContentType="{CT_W}.styles+xml"/>'
          f'<Override PartName="/word/settings.xml" ContentType="{CT_W}.settings+xml"/>'
          f'<Override PartName="/word/numbering.xml" ContentType="{CT_W}.numbering+xml"/>'
          f'<Override PartName="/word/header1.xml" ContentType="{CT_W}.header+xml"/>'
          f'<Override PartName="/word/footer1.xml" ContentType="{CT_W}.footer+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
          '</Types>')
    rels = (DECL + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId1" Type="{REL}/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            f'<Relationship Id="rId3" Type="{REL}/extended-properties" Target="docProps/app.xml"/>'
            '</Relationships>')
    drels = (DECL + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             f'<Relationship Id="rIdS" Type="{REL}/styles" Target="styles.xml"/>'
             f'<Relationship Id="rIdT" Type="{REL}/settings" Target="settings.xml"/>'
             f'<Relationship Id="rIdN" Type="{REL}/numbering" Target="numbering.xml"/>'
             f'<Relationship Id="rIdH" Type="{REL}/header" Target="header1.xml"/>'
             f'<Relationship Id="rIdF" Type="{REL}/footer" Target="footer1.xml"/>'
             f'<Relationship Id="rIdImg" Type="{REL}/image" Target="media/{figura_png}"/>'
             '</Relationships>')
    settings = (DECL + f'<w:settings xmlns:w="{W}"><w:zoom w:percent="100"/>'
                '<w:defaultTabStop w:val="708"/><w:characterSpacingControl w:val="doNotCompress"/>'
                '<w:compat><w:compatSetting w:name="compatibilityMode" '
                'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>')
    core = (DECL + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{escape(titulo)}</dc:title><dc:language>es-ES</dc:language>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-03T00:00:00Z</dcterms:created>'
            '</cp:coreProperties>')
    app = (DECL + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           '<Application>Kiro</Application></Properties>')
    with zipfile.ZipFile(ruta_docx, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)
        z.writestr("word/_rels/document.xml.rels", drels)
        z.writestr("word/styles.xml", estilos_xml())
        z.writestr("word/settings.xml", settings)
        z.writestr("word/numbering.xml", numeracion_xml())
        z.writestr("word/header1.xml", encabezado_xml(texto_encabezado))
        z.writestr("word/footer1.xml", pie_xml())
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.write(os.path.join(dir_img, figura_png), f"word/media/{figura_png}")
