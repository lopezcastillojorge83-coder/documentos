# -*- coding: utf-8 -*-
"""Validación estructural de los paquetes OOXML generados."""
import re
import sys
import zipfile
import posixpath
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

ORDER = {
    W + "pPr": ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl", "numPr",
                "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
                "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN", "bidi", "adjustRightInd", "snapToGrid",
                "spacing", "ind", "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc", "textDirection",
                "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr", "pPrChange"],
    W + "rPr": ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike", "outline",
                "shadow", "emboss", "imprint", "noProof", "snapToGrid", "vanish", "webHidden", "color", "spacing", "w",
                "kern", "position", "sz", "szCs", "highlight", "u", "effect", "bdr", "shd", "fitText", "vertAlign",
                "rtl", "cs", "em", "lang", "eastAsianLayout", "specVanish", "oMath"],
    W + "tblPr": ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize", "tblStyleColBandSize",
                  "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout", "tblCellMar", "tblLook"],
    W + "tcPr": ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd", "noWrap", "tcMar",
                 "textDirection", "tcFitText", "vAlign", "hideMark"],
    W + "trPr": ["cnfStyle", "divId", "gridBefore", "gridAfter", "wBefore", "wAfter", "cantSplit", "trHeight",
                 "tblHeader", "tblCellSpacing", "jc", "hidden"],
    W + "sectPr": ["headerReference", "footerReference", "footnotePr", "endnotePr", "type", "pgSz", "pgMar",
                   "paperSrc", "pgBorders", "lnNumType", "pgNumType", "cols", "formProt", "vAlign", "noEndnote",
                   "titlePg", "textDirection", "bidi", "rtlGutter", "docGrid", "printerSettings"],
    S + "worksheet": ["sheetPr", "dimension", "sheetViews", "sheetFormatPr", "cols", "sheetData", "sheetCalcPr",
                      "sheetProtection", "protectedRanges", "scenarios", "autoFilter", "sortState", "dataConsolidate",
                      "customSheetViews", "mergeCells", "phoneticPr", "conditionalFormatting", "dataValidations",
                      "hyperlinks", "printOptions", "pageMargins", "pageSetup", "headerFooter", "rowBreaks", "colBreaks",
                      "customProperties", "cellWatches", "ignoredErrors", "smartTags", "drawing"],
    S + "styleSheet": ["numFmts", "fonts", "fills", "borders", "cellStyleXfs", "cellXfs", "cellStyles", "dxfs",
                       "tableStyles", "colors", "extLst"],
    S + "font": ["b", "i", "strike", "condense", "extend", "outline", "shadow", "u", "vertAlign", "sz", "color",
                 "name", "family", "charset", "scheme"],
}


def local(tag):
    return tag.split("}", 1)[1] if "}" in tag else tag


def check_order(root, errors, part):
    for el in root.iter():
        seq = ORDER.get(el.tag)
        if not seq:
            continue
        idx = []
        for ch in el:
            name = local(ch.tag)
            if name not in seq:
                errors.append("%s: <%s> no esperado dentro de <%s>" % (part, name, local(el.tag)))
                continue
            idx.append(seq.index(name))
        # se permiten repeticiones consecutivas (p. ej. headerReference)
        if idx != sorted(idx):
            errors.append("%s: orden incorrecto en <%s>: %s" % (part, local(el.tag), [local(c.tag) for c in el]))


def validate(path):
    errors = []
    z = zipfile.ZipFile(path)
    names = set(z.namelist())
    ct = ET.fromstring(z.read("[Content_Types].xml"))
    defaults = {e.get("Extension") for e in ct if local(e.tag) == "Default"}
    overrides = {e.get("PartName") for e in ct if local(e.tag) == "Override"}
    for n in names:
        if n.endswith("/") or n == "[Content_Types].xml":
            continue
        ext = n.rsplit(".", 1)[-1]
        if "/" + n not in overrides and ext not in defaults:
            errors.append("Sin tipo de contenido: " + n)
        if n.endswith(".xml") or n.endswith(".rels"):
            try:
                root = ET.fromstring(z.read(n))
            except ET.ParseError as e:
                errors.append("XML mal formado %s: %s" % (n, e))
                continue
            check_order(root, errors, n)
    for o in overrides:
        if o.lstrip("/") not in names:
            errors.append("Override sin parte: " + o)
    # relaciones
    for n in names:
        if not n.endswith(".rels"):
            continue
        base = posixpath.dirname(posixpath.dirname(n))
        root = ET.fromstring(z.read(n))
        ids = set()
        for r in root:
            rid = r.get("Id")
            if rid in ids:
                errors.append("Id de relación duplicado %s en %s" % (rid, n))
            ids.add(rid)
            if r.get("TargetMode") == "External":
                continue
            tgt = posixpath.normpath(posixpath.join(base, r.get("Target")))
            if tgt not in names:
                errors.append("Destino inexistente %s (%s)" % (tgt, n))
    # referencias r:id usadas en el documento
    if "word/document.xml" in names:
        rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        rel_ids = {r.get("Id") for r in rels}
        doc = z.read("word/document.xml").decode("utf-8")
        for rid in set(re.findall(r'r:(?:id|embed)="([^"]+)"', doc)):
            if rid not in rel_ids:
                errors.append("r:id sin relación: " + rid)
        ids = re.findall(r'<wp:docPr id="(\d+)"', doc)
        if len(ids) != len(set(ids)):
            errors.append("docPr id duplicado")
        # tablas: número de celdas coherente con la grilla
        root = ET.fromstring(z.read("word/document.xml"))
        for t_i, tbl in enumerate(root.iter(W + "tbl")):
            ncols = len(tbl.find(W + "tblGrid"))
            for tr in tbl.findall(W + "tr"):
                span = 0
                for tc in tr.findall(W + "tc"):
                    gs = tc.find(W + "tcPr/" + W + "gridSpan")
                    span += int(gs.get(W + "val")) if gs is not None else 1
                if span != ncols:
                    errors.append("Tabla %d: fila con %d columnas (grilla %d)" % (t_i + 1, span, ncols))
    if "xl/workbook.xml" in names:
        for n in sorted(names):
            if not n.startswith("xl/worksheets/sheet"):
                continue
            root = ET.fromstring(z.read(n))
            last_r = 0
            for row in root.iter(S + "row"):
                r = int(row.get("r"))
                if r <= last_r:
                    errors.append("%s: filas fuera de orden en %d" % (n, r))
                last_r = r
                last_c = 0
                for c in row:
                    m = re.match(r"([A-Z]+)(\d+)", c.get("r"))
                    col = 0
                    for ch in m.group(1):
                        col = col * 26 + ord(ch) - 64
                    if int(m.group(2)) != r or col <= last_c:
                        errors.append("%s: celda fuera de orden %s" % (n, c.get("r")))
                    last_c = col
            st = ET.fromstring(z.read("xl/styles.xml"))
            nxf = len(st.find(S + "cellXfs"))
            for c in root.iter(S + "c"):
                if c.get("s") and int(c.get("s")) >= nxf:
                    errors.append("%s: estilo inexistente en %s" % (n, c.get("r")))
    return errors


if __name__ == "__main__":
    ok = True
    for p in sys.argv[1:]:
        errs = validate(p)
        print(("OK  " if not errs else "ERR ") + p)
        for e in errs[:40]:
            print("   -", e)
        ok = ok and not errs
    sys.exit(0 if ok else 1)
