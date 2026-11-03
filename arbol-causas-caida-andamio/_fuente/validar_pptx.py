# -*- coding: utf-8 -*-
"""Validación estructural de un .pptx sin PowerPoint."""
import posixpath
import sys
import zipfile
import xml.etree.ElementTree as ET

P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

ORDEN = {  # elemento: hijos permitidos en orden
    P + "presentation": [P + x for x in "sldMasterIdLst notesMasterIdLst handoutMasterIdLst "
                         "sldIdLst sldSz notesSz smartTags embeddedFontLst custShowLst photoAlbum "
                         "custDataLst kinsoku defaultTextStyle modifyVerifier extLst".split()],
    P + "sp": [P + x for x in "nvSpPr spPr style txBody extLst".split()],
    P + "pic": [P + x for x in "nvPicPr blipFill spPr style extLst".split()],
    P + "sld": [P + x for x in "cSld clrMapOvr transition timing extLst".split()],
    P + "notes": [P + x for x in "cSld clrMapOvr extLst".split()],
    P + "sldMaster": [P + x for x in "cSld clrMap sldLayoutIdLst transition timing hf "
                      "txStyles extLst".split()],
    P + "notesMaster": [P + x for x in "cSld clrMap hf notesStyle extLst".split()],
    A + "rPr": [A + x for x in "ln noFill solidFill gradFill blipFill pattFill grpFill effectLst "
                "effectDag highlight uLnTx uLn uFillTx uFill latin ea cs sym hlinkClick "
                "hlinkMouseOver rtl extLst".split()],
    P + "spPr": [], A + "bodyPr": [],
}


def validar(ruta):
    err = []
    z = zipfile.ZipFile(ruta)
    nombres = set(z.namelist())
    arboles = {}
    for n in nombres:
        if n.endswith((".xml", ".rels")):
            try:
                arboles[n] = ET.fromstring(z.read(n))
            except ET.ParseError as e:
                err.append(f"{n}: XML mal formado ({e})")
    for n, raiz in arboles.items():
        for el in raiz.iter():
            lista = ORDEN.get(el.tag)
            if not lista:
                continue
            ultimo = -1
            for h in el:
                if h.tag not in lista:
                    err.append(f"{n}: <{el.tag.split('}')[1]}> con hijo no permitido "
                               f"<{h.tag.split('}')[1]}>")
                    continue
                k = lista.index(h.tag)
                if k < ultimo:
                    err.append(f"{n}: <{el.tag.split('}')[1]}> hijo <{h.tag.split('}')[1]}> "
                               "fuera de orden")
                ultimo = max(ultimo, k)
    # relaciones: destinos existen y cada r:id usado está definido
    for n, raiz in arboles.items():
        if not n.endswith(".rels"):
            continue
        parte = n.replace("_rels/", "")[:-5]
        base = posixpath.dirname(parte)
        ids = set()
        for rel in raiz:
            ids.add(rel.get("Id"))
            destino = posixpath.normpath(posixpath.join(base, rel.get("Target")))
            if destino not in nombres:
                err.append(f"{n}: destino inexistente {destino}")
        if parte in arboles:
            for el in arboles[parte].iter():
                for k, v in el.attrib.items():
                    if k.startswith(R) and v not in ids:
                        err.append(f"{parte}: r:id {v} no definido")
    ct = arboles["[Content_Types].xml"]
    defaults = {e.get("Extension") for e in ct if e.tag.endswith("Default")}
    overrides = {e.get("PartName") for e in ct if e.tag.endswith("Override")}
    for n in nombres:
        if n != "[Content_Types].xml" and "/" + n not in overrides \
                and n.rsplit(".", 1)[-1] not in defaults:
            err.append(f"sin tipo de contenido: {n}")
    for o in overrides:
        if o[1:] not in nombres:
            err.append(f"override sin parte: {o}")
    pres = arboles["ppt/presentation.xml"]
    info = {"diapositivas": len(pres.find(P + "sldIdLst")),
            "notas": len([n for n in nombres if n.startswith("ppt/notesSlides/notesSlide")]),
            "imagenes": len([n for n in nombres if n.startswith("ppt/media/")]),
            "textos_editables": sum(len(arboles[n].findall(f".//{P}sp")) for n in arboles
                                    if n.startswith("ppt/slides/slide"))}
    return err, info


if __name__ == "__main__":
    e, i = validar(sys.argv[1])
    print(i)
    for x in e:
        print("ERROR:", x)
    print("VALIDO" if not e else f"{len(e)} errores")
    sys.exit(1 if e else 0)
