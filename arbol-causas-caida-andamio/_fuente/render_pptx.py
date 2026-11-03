# -*- coding: utf-8 -*-
"""Escribe un .pptx (PresentationML) con la biblioteca estándar de Python.

Cada diapositiva es una imagen a pantalla completa, más cuadros de texto
editables opcionales y notas del orador.
"""
import os
import subprocess
import zipfile
from xml.sax.saxutils import escape, quoteattr

DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS = f'xmlns:a="{A}" xmlns:r="{R}" xmlns:p="{P}"'
REL = R
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "application/vnd.openxmlformats-officedocument.presentationml"
SX, SY = 12192000, 6858000          # 16:9 (13,333 x 7,5 in)
EMU_PX = SX // 1920                 # 6350 EMU por píxel del lienzo


def rels(lista):
    cuerpo = "".join(f'<Relationship Id="{i}" Type="{t}" Target="{d}"/>' for i, t, d in lista)
    return DECL + f'<Relationships xmlns="{PKG}">{cuerpo}</Relationships>'


GRUPO = ('<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
         '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/>'
         '<a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')
CLRMAP = ('<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
          'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" '
          'folHlink="folHlink"/>')


def tema(nombre):
    colores = [("dk1", '<a:sysClr val="windowText" lastClr="000000"/>'),
               ("lt1", '<a:sysClr val="window" lastClr="FFFFFF"/>'),
               ("dk2", '<a:srgbClr val="1F3A5F"/>'), ("lt2", '<a:srgbClr val="E7EEF6"/>'),
               ("accent1", '<a:srgbClr val="2E6DA4"/>'), ("accent2", '<a:srgbClr val="2E7D32"/>'),
               ("accent3", '<a:srgbClr val="B58900"/>'), ("accent4", '<a:srgbClr val="8E2A2A"/>'),
               ("accent5", '<a:srgbClr val="475569"/>'), ("accent6", '<a:srgbClr val="9CC3E6"/>'),
               ("hlink", '<a:srgbClr val="2E6DA4"/>'), ("folHlink", '<a:srgbClr val="6B4E9B"/>')]
    clr = "".join(f"<a:{n}>{v}</a:{n}>" for n, v in colores)
    fuente = '<a:latin typeface="{}"/><a:ea typeface=""/><a:cs typeface=""/>'
    relleno = '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    linea = f'<a:ln w="6350">{relleno}</a:ln>'
    efecto = "<a:effectStyle><a:effectLst/></a:effectStyle>"
    return (DECL + f'<a:theme xmlns:a="{A}" name="{nombre}"><a:themeElements>'
            f'<a:clrScheme name="Arbol">{clr}</a:clrScheme>'
            f'<a:fontScheme name="Arbol"><a:majorFont>{fuente.format("Calibri")}</a:majorFont>'
            f'<a:minorFont>{fuente.format("Calibri")}</a:minorFont></a:fontScheme>'
            f'<a:fmtScheme name="Arbol"><a:fillStyleLst>{relleno * 3}</a:fillStyleLst>'
            f'<a:lnStyleLst>{linea * 3}</a:lnStyleLst><a:effectStyleLst>{efecto * 3}'
            f'</a:effectStyleLst><a:bgFillStyleLst>{relleno * 3}</a:bgFillStyleLst></a:fmtScheme>'
            '</a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>')


def master():
    estilo = '<a:lvl1pPr><a:defRPr sz="1800"/></a:lvl1pPr>'
    return (DECL + f'<p:sldMaster {NS}><p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/>'
            f'</p:bgRef></p:bg><p:spTree>{GRUPO}</p:spTree></p:cSld>{CLRMAP}'
            '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
            f'<p:txStyles><p:titleStyle>{estilo}</p:titleStyle><p:bodyStyle>{estilo}</p:bodyStyle>'
            f'<p:otherStyle>{estilo}</p:otherStyle></p:txStyles></p:sldMaster>')


def layout():
    return (DECL + f'<p:sldLayout {NS} type="blank" preserve="1"><p:cSld name="En blanco">'
            f'<p:spTree>{GRUPO}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/>'
            '</p:clrMapOvr></p:sldLayout>')


def notes_master():
    def ph(i, nombre, tipo, x, y, cx, cy, extra=""):
        return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{nombre}"/><p:cNvSpPr>'
                f'<a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="{tipo}"{extra}/></p:nvPr>'
                f'</p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/>'
                '</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
                + ('<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="es-ES"/></a:p>'
                   '</p:txBody>' if tipo == "body" else "") + '</p:sp>')
    arbol = (GRUPO + ph(2, "Imagen de diapositiva", "sldImg", 381000, 685800, 6096000, 3429000)
             + ph(3, "Notas", "body", 685800, 4343400, 5486400, 4114800, ' idx="1"'))
    estilo = '<a:lvl1pPr><a:defRPr sz="1200"/></a:lvl1pPr>'
    return (DECL + f'<p:notesMaster {NS}><p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr '
            f'val="bg1"/></p:bgRef></p:bg><p:spTree>{arbol}</p:spTree></p:cSld>{CLRMAP}'
            f'<p:notesStyle>{estilo}</p:notesStyle></p:notesMaster>')


def _xfrm(x, y, w, h):
    return (f'<a:xfrm><a:off x="{x * EMU_PX}" y="{y * EMU_PX}"/>'
            f'<a:ext cx="{w * EMU_PX}" cy="{h * EMU_PX}"/></a:xfrm>')


def cuadro_texto(i, c):
    rpr = (f'<a:rPr lang="es-ES" sz="{int(c["pt"] * 100)}" dirty="0"><a:solidFill>'
           f'<a:srgbClr val="{c["color"]}"/></a:solidFill><a:latin typeface="Calibri"/></a:rPr>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name={quoteattr(c["nombre"])}/>'
            f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>'
            f'{_xfrm(c["x"], c["y"], c["w"], c["h"])}<a:prstGeom prst="rect"><a:avLst/>'
            f'</a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" '
            f'tIns="0" rIns="0" bIns="0" anchor="ctr"><a:normAutofit/></a:bodyPr><a:lstStyle/>'
            f'<a:p><a:r>{rpr}<a:t>{escape(c["texto"])}</a:t></a:r></a:p></p:txBody></p:sp>')


def diapositiva(n, d):
    pic = (f'<p:pic><p:nvPicPr><p:cNvPr id="2" name="Diapositiva {n}" '
           f'descr={quoteattr("Diapositiva " + str(n))}/><p:cNvPicPr><a:picLocks '
           f'noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill>'
           f'<a:blip r:embed="rIdImg"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
           f'<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{SX}" cy="{SY}"/></a:xfrm>'
           f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
    textos = "".join(cuadro_texto(i, c) for i, c in enumerate(d.get("nativos", []), 3))
    return (DECL + f'<p:sld {NS}><p:cSld><p:spTree>{GRUPO}{pic}{textos}</p:spTree></p:cSld>'
            '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')


def notas(texto):
    parrafos = "".join(f'<a:p><a:r><a:rPr lang="es-ES" dirty="0"/><a:t>{escape(t)}</a:t></a:r>'
                       f'</a:p>' for t in texto.split("\n") if t.strip())
    return (DECL + f'<p:notes {NS}><p:cSld><p:spTree>{GRUPO}'
            '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Imagen de diapositiva"/><p:cNvSpPr>'
            '<a:spLocks noGrp="1" noRot="1" noChangeAspect="1"/></p:cNvSpPr><p:nvPr>'
            '<p:ph type="sldImg"/></p:nvPr></p:nvSpPr><p:spPr/></p:sp>'
            '<p:sp><p:nvSpPr><p:cNvPr id="3" name="Notas"/><p:cNvSpPr><a:spLocks noGrp="1"/>'
            '</p:cNvSpPr><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/>'
            f'<p:txBody><a:bodyPr/><a:lstStyle/>{parrafos}</p:txBody></p:sp>'
            '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>')


def escribir_pptx(diapos, ruta):
    n = len(diapos)
    ids = "".join(f'<p:sldId id="{256 + i}" r:id="rIdS{i}"/>' for i in range(1, n + 1))
    pres = (DECL + f'<p:presentation {NS} saveSubsetFonts="1"><p:sldMasterIdLst>'
            '<p:sldMasterId id="2147483648" r:id="rIdM"/></p:sldMasterIdLst><p:notesMasterIdLst>'
            f'<p:notesMasterId r:id="rIdNM"/></p:notesMasterIdLst><p:sldIdLst>{ids}</p:sldIdLst>'
            f'<p:sldSz cx="{SX}" cy="{SY}"/><p:notesSz cx="6858000" cy="9144000"/>'
            '</p:presentation>')
    pres_rels = [("rIdM", f"{REL}/slideMaster", "slideMasters/slideMaster1.xml"),
                 ("rIdNM", f"{REL}/notesMaster", "notesMasters/notesMaster1.xml"),
                 ("rIdT", f"{REL}/theme", "theme/theme1.xml"),
                 ("rIdPP", f"{REL}/presProps", "presProps.xml"),
                 ("rIdVP", f"{REL}/viewProps", "viewProps.xml"),
                 ("rIdTS", f"{REL}/tableStyles", "tableStyles.xml")]
    pres_rels += [(f"rIdS{i}", f"{REL}/slide", f"slides/slide{i}.xml") for i in range(1, n + 1)]
    ov = [("/ppt/presentation.xml", f"{CT}.presentation.main+xml"),
          ("/ppt/slideMasters/slideMaster1.xml", f"{CT}.slideMaster+xml"),
          ("/ppt/slideLayouts/slideLayout1.xml", f"{CT}.slideLayout+xml"),
          ("/ppt/notesMasters/notesMaster1.xml", f"{CT}.notesMaster+xml"),
          ("/ppt/theme/theme1.xml", "application/vnd.openxmlformats-officedocument.theme+xml"),
          ("/ppt/theme/theme2.xml", "application/vnd.openxmlformats-officedocument.theme+xml"),
          ("/ppt/presProps.xml", f"{CT}.presProps+xml"),
          ("/ppt/viewProps.xml", f"{CT}.viewProps+xml"),
          ("/ppt/tableStyles.xml", f"{CT}.tableStyles+xml"),
          ("/docProps/core.xml", "application/vnd.openxmlformats-package.core-properties+xml"),
          ("/docProps/app.xml",
           "application/vnd.openxmlformats-officedocument.extended-properties+xml")]
    for i in range(1, n + 1):
        ov += [(f"/ppt/slides/slide{i}.xml", f"{CT}.slide+xml"),
               (f"/ppt/notesSlides/notesSlide{i}.xml", f"{CT}.notesSlide+xml")]
    ct = (DECL + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.'
          'relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="png" ContentType="image/png"/>'
          + "".join(f'<Override PartName="{p}" ContentType="{c}"/>' for p, c in ov) + '</Types>')
    core = (DECL + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/'
            'metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>Árbol de causas: caída de altura desde andamio (NTP 274)</dc:title>'
            '<dc:language>es-ES</dc:language><dcterms:created xsi:type="dcterms:W3CDTF">'
            '2026-11-03T00:00:00Z</dcterms:created></cp:coreProperties>')
    app = (DECL + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/'
           f'extended-properties"><Application>Kiro</Application><Slides>{n}</Slides>'
           f'<Notes>{n}</Notes></Properties>')
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels([
            ("rId1", f"{REL}/officeDocument", "ppt/presentation.xml"),
            ("rId2", f"{PKG}/metadata/core-properties", "docProps/core.xml"),
            ("rId3", f"{REL}/extended-properties", "docProps/app.xml")]))
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("ppt/presentation.xml", pres)
        z.writestr("ppt/_rels/presentation.xml.rels", rels(pres_rels))
        z.writestr("ppt/presProps.xml", DECL + f'<p:presentationPr {NS}/>')
        z.writestr("ppt/viewProps.xml", DECL + f'<p:viewPr {NS}><p:normalViewPr>'
                   '<p:restoredLeft sz="15620"/><p:restoredTop sz="94660"/></p:normalViewPr>'
                   '</p:viewPr>')
        z.writestr("ppt/tableStyles.xml", DECL + f'<a:tblStyleLst xmlns:a="{A}" '
                   'def="{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"/>')
        z.writestr("ppt/theme/theme1.xml", tema("Arbol de causas"))
        z.writestr("ppt/theme/theme2.xml", tema("Notas"))
        z.writestr("ppt/slideMasters/slideMaster1.xml", master())
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels([
            ("rId1", f"{REL}/slideLayout", "../slideLayouts/slideLayout1.xml"),
            ("rId2", f"{REL}/theme", "../theme/theme1.xml")]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", layout())
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels([
            ("rId1", f"{REL}/slideMaster", "../slideMasters/slideMaster1.xml")]))
        z.writestr("ppt/notesMasters/notesMaster1.xml", notes_master())
        z.writestr("ppt/notesMasters/_rels/notesMaster1.xml.rels", rels([
            ("rId1", f"{REL}/theme", "../theme/theme2.xml")]))
        for i, d in enumerate(diapos, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", diapositiva(i, d))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels([
                ("rIdL", f"{REL}/slideLayout", "../slideLayouts/slideLayout1.xml"),
                ("rIdImg", f"{REL}/image", f"../media/diapo{i:02d}.png"),
                ("rIdN", f"{REL}/notesSlide", f"../notesSlides/notesSlide{i}.xml")]))
            z.writestr(f"ppt/notesSlides/notesSlide{i}.xml", notas(d["notas"]))
            z.writestr(f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels", rels([
                ("rId1", f"{REL}/notesMaster", "../notesMasters/notesMaster1.xml"),
                ("rId2", f"{REL}/slide", f"../slides/slide{i}.xml")]))
            z.write(d["png"], f"ppt/media/diapo{i:02d}.png")


def escribir_pdf(diapos, ruta_pdf, trabajo):
    """PDF de revisión: una página 16:9 por diapositiva."""
    paginas = "".join(f'<img src="{os.path.basename(d["png"])}">' for d in diapos)
    doc = ('<!doctype html><html><head><meta charset="utf-8"><style>@page{size:338.67mm 190.5mm;'
           'margin:0}*{margin:0;padding:0}img{display:block;width:338.67mm;height:190.5mm;'
           f'break-after:page}}</style></head><body>{paginas}</body></html>')
    html = os.path.join(trabajo, "presentacion_pdf.html")
    with open(html, "w", encoding="utf-8") as f:
        f.write(doc)
    js = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.js")
    r = subprocess.run(["node", js, "pdf", html, ruta_pdf], capture_output=True, text=True,
                       timeout=300)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-400:])
