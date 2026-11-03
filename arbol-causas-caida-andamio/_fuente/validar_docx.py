# -*- coding: utf-8 -*-
"""Validación estructural de un .docx sin Word: XML bien formado, orden de
elementos según el esquema OOXML, relaciones, tipos de contenido y tablas."""
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

ORDEN = {
    "pPr": "pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr "
           "suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap "
           "overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd "
           "snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc "
           "textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr "
           "sectPr pPrChange",
    "rPr": "rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow "
           "emboss imprint noProof snapToGrid vanish webHidden color spacing w kern "
           "position sz szCs highlight u effect bdr shd fitText vertAlign rtl cs em "
           "lang eastAsianLayout specVanish oMath",
    "tblPr": "tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize "
             "tblStyleColBandSize tblW jc tblCellSpacing tblInd tblBorders shd "
             "tblLayout tblCellMar tblLook tblCaption tblDescription",
    "tcPr": "cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar "
            "textDirection tcFitText vAlign hideMark",
    "sectPr": "headerReference footerReference footnotePr endnotePr type pgSz pgMar "
              "paperSrc pgBorders lnNumType pgNumType cols formProt vAlign noEndnote "
              "titlePg textDirection bidi rtlGutter docGrid printerSettings",
    "tblBorders": "top left start bottom right end insideH insideV",
    "tcBorders": "top left start bottom right end insideH insideV tl2br tr2bl",
    "tblCellMar": "top left start bottom right end",
    "pBdr": "top left bottom right between bar",
    "style": "name aliases basedOn next link autoRedefine hidden uiPriority semiHidden "
             "unhideWhenUsed qFormat locked personal personalCompose personalReply rsid "
             "pPr rPr tblPr trPr tcPr tblStylePr",
    "lvl": "start numFmt lvlRestart pStyle isLgl suff lvlText lvlPicBulletId legacy "
           "lvlJc pPr rPr",
}
ORDEN = {k: v.split() for k, v in ORDEN.items()}


def revisar_orden(raiz, parte, errores):
    for el in raiz.iter():
        if not el.tag.startswith(W):
            continue
        nombre = el.tag[len(W):]
        if nombre not in ORDEN:
            continue
        lista, ultimo = ORDEN[nombre], -1
        for hijo in el:
            h = hijo.tag.replace(W, "")
            if h not in lista:
                errores.append(f"{parte}: <{nombre}> contiene <{h}> no permitido")
                continue
            idx = lista.index(h)
            if idx < ultimo:
                errores.append(f"{parte}: <{nombre}> con <{h}> fuera de orden")
            ultimo = max(ultimo, idx)


def revisar_tablas(raiz, errores):
    n = 0
    for tbl in raiz.iter(W + "tbl"):
        n += 1
        cols = len(tbl.find(W + "tblGrid").findall(W + "gridCol"))
        for fila in tbl.findall(W + "tr"):
            celdas = fila.findall(W + "tc")
            if len(celdas) != cols:
                errores.append(f"tabla {n}: fila con {len(celdas)} celdas y {cols} columnas")
            for c in celdas:
                if c[-1].tag != W + "p":
                    errores.append(f"tabla {n}: una celda no termina en <w:p>")
    return n


def validar(ruta):
    errores, info = [], {}
    z = zipfile.ZipFile(ruta)
    nombres = set(z.namelist())
    arboles = {}
    for n in nombres:
        if n.endswith((".xml", ".rels")):
            try:
                arboles[n] = ET.fromstring(z.read(n))
            except ET.ParseError as e:
                errores.append(f"{n}: XML mal formado ({e})")
    for n, raiz in arboles.items():
        revisar_orden(raiz, n, errores)
    # relaciones
    for n, raiz in arboles.items():
        if n.endswith(".rels"):
            base = n.replace("_rels/", "").rsplit(".rels", 1)[0]
            carpeta = base.rsplit("/", 1)[0] + "/" if "/" in base else ""
            for rel in raiz:
                destino = carpeta + rel.get("Target")
                if rel.get("TargetMode") != "External" and destino not in nombres:
                    errores.append(f"{n}: destino inexistente {destino}")
    doc = arboles["word/document.xml"]
    rels = {r.get("Id") for r in arboles["word/_rels/document.xml.rels"]}
    for el in doc.iter():
        for k, v in el.attrib.items():
            if k.startswith(R) and v not in rels:
                errores.append(f"document.xml: relación {v} no definida")
    # tipos de contenido
    ct = arboles["[Content_Types].xml"]
    defaults = {e.get("Extension") for e in ct if e.tag.endswith("Default")}
    overrides = {e.get("PartName") for e in ct if e.tag.endswith("Override")}
    for n in nombres:
        if n != "[Content_Types].xml" and "/" + n not in overrides \
                and n.rsplit(".", 1)[-1] not in defaults:
            errores.append(f"sin tipo de contenido: {n}")
    info["tablas"] = revisar_tablas(doc, errores)
    info["parrafos"] = len(list(doc.iter(W + "p")))
    info["secciones"] = len(list(doc.iter(W + "sectPr")))
    info["imagenes"] = len(list(doc.iter("{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}inline")))
    return errores, info


if __name__ == "__main__":
    errs, inf = validar(sys.argv[1])
    print(inf)
    for e in errs:
        print("ERROR:", e)
    print("VALIDO" if not errs else f"{len(errs)} errores")
    sys.exit(1 if errs else 0)
