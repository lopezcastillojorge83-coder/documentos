# -*- coding: utf-8 -*-
"""Renderiza los mismos bloques del informe a HTML y lo imprime a PDF."""
import html
import os
import subprocess

from render_docx import partes

CSS = """
@page { size: A4; margin: 22mm 24mm 20mm 24mm;
  @top-right { content: "%(enc)s"; font: 8.5pt 'Noto Sans', sans-serif; color: #64748b; }
  @bottom-center { content: "Página " counter(page); font: 8.5pt 'Noto Sans', sans-serif;
                   color: #64748b; } }
@page portada { margin: 24mm; @top-right { content: none }
                @bottom-center { content: none } }
@page figura { size: A4 landscape; margin: 14mm 14mm 12mm 14mm; }
* { box-sizing: border-box; }
body { font-family: 'Noto Sans', 'Liberation Sans', Arial, sans-serif; font-size: 9.6pt;
       line-height: 1.36; color: #111827; margin: 0; }
p { margin: 0 0 5pt; }
h1 { font-size: 15.5pt; color: #1f3a5f; margin: 16pt 0 5pt; break-after: avoid; line-height: 1.2; }
h2 { font-size: 12pt; color: #2e6da4; margin: 11pt 0 4pt; break-after: avoid; }
ul { margin: 0 0 6pt; padding-left: 17pt; }
li { margin: 0 0 3pt; padding-left: 2pt; }
li::marker { color: #2e6da4; }
table { width: 100%%; border-collapse: collapse; table-layout: fixed; font-size: 8.7pt;
        margin: 0 0 8pt; line-height: 1.3; }
th { background: #1f3a5f; color: #fff; text-align: left; font-weight: 700; }
th, td { border: 0.6pt solid #b8c4d6; padding: 3pt 6pt; vertical-align: top; }
td p { margin: 0 0 2.5pt; } td ul { margin: 0; padding-left: 12pt; } td li { margin: 0 0 2pt; }
td.c0 { background: #eaf0f7; }
tr { break-inside: avoid; }
table.ligera { font-size: 10.5pt; }
table.ligera td { border-width: 0.6pt 0; padding: 5pt 6pt; }
.portada { page: portada; padding-top: 28mm; }
.portada .tit { font-size: 25pt; font-weight: 700; color: #1f3a5f; line-height: 1.15;
                margin: 0 0 8pt; }
.portada .sub { font-size: 15pt; color: #334155; margin: 0 0 22pt; padding-bottom: 8pt;
                border-bottom: 1.5pt solid #2e6da4; }
.portada h3 { font-size: 13pt; color: #1f3a5f; margin: 22pt 0 5pt; }
.portada table { font-size: 10.5pt; }
.nota { background: #fff6db; border-left: 3pt solid #e0a100; padding: 7pt 10pt;
        margin: 0 0 10pt; font-size: 9.5pt; break-inside: avoid; }
.figura { page: figura; }
.figura h1 { margin-top: 0; }
.figura img { display: block; margin: 0 auto; width: 250mm; }
.pie { text-align: center; font-style: italic; color: #64748b; font-size: 8.5pt;
       margin-top: 3pt; }
"""


def inline(texto):
    out = ""
    for t, b, i in partes(texto):
        t = html.escape(t).replace("\n", "<br>")
        if b:
            t = f"<strong>{t}</strong>"
        if i:
            t = f"<em>{t}</em>"
        out += t
    return out


def contenido_celda(c):
    items = c if isinstance(c, list) else [c]
    out, lista = "", []
    for it in items + [None]:
        if it is not None and it.startswith("• "):
            lista.append(f"<li>{inline(it[2:])}</li>")
            continue
        if lista:
            out += "<ul>" + "".join(lista) + "</ul>"
            lista = []
        if it is not None:
            out += f"<p>{inline(it)}</p>"
    return out


def tabla(spec, clase=""):
    cols = "".join(f'<col style="width:{w}%">' for w in spec["anchos"])
    cab = ""
    if spec.get("cab"):
        cab = "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in spec["cab"]) + "</tr></thead>"
    filas = ""
    for f in spec["filas"]:
        celdas = ""
        for k, c in enumerate(f):
            cl = ' class="c0"' if (k == 0 and spec.get("fondo_col0")) else ""
            celdas += f"<td{cl}>{contenido_celda(c)}</td>"
        filas += f"<tr>{celdas}</tr>"
    clase = ' class="ligera"' if spec.get("ligera") else ""
    return f"<table{clase}><colgroup>{cols}</colgroup>{cab}<tbody>{filas}</tbody></table>"


def portada(d):
    t = tabla({"anchos": [24, 76], "ligera": True,
               "filas": [[f"**{k}**", v] for k, v in d["datos"]]})
    m = tabla({"anchos": [9, 61, 30], "cab": ["N.º", "Nombre completo", "Código"],
               "filas": [list(f) for f in d["integrantes"]]})
    return (f'<section class="portada"><p class="tit">{html.escape(d["titulo"])}</p>'
            f'<p class="sub">{html.escape(d["subtitulo"])}</p>{t}<h3>Integrantes</h3>{m}</section>')


def cuerpo(bloques):
    x, previo = "", None
    for b in bloques:
        k = b[0]
        if k == "portada":
            x += portada(b[1])
        elif k == "h1":
            est = ' style="margin-top:0"' if previo in ("portada", "seccion") else ""
            x += f"<h1{est}>{inline(b[1])}</h1>"
        elif k == "h2":
            x += f"<h2>{inline(b[1])}</h2>"
        elif k == "p":
            x += f"<p>{inline(b[1])}</p>"
        elif k == "nota":
            x += f'<div class="nota">{inline(b[1])}</div>'
        elif k == "bullets":
            x += "<ul>" + "".join(f"<li>{inline(t)}</li>" for t in b[1]) + "</ul>"
        elif k == "tabla":
            x += tabla(b[1])
        elif k == "figura":
            x += (f'<img src="{b[1]["archivo"]}" alt="Árbol de causas">'
                  f'<p class="pie">{inline(b[1]["pie"])}</p>')
        elif k == "seccion":
            x += '<section class="figura">' if b[1] == "horizontal" else "</section>"
        else:
            raise ValueError(k)
        previo = k
    return x


def escribir_pdf(bloques, ruta_pdf, dir_trabajo, encabezado):
    css = CSS % {"enc": encabezado.replace('"', "'")}
    doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Árbol de '
           f'causas</title><style>{css}</style></head><body>{cuerpo(bloques)}</body></html>')
    ruta_html = os.path.join(dir_trabajo, "informe.html")
    with open(ruta_html, "w", encoding="utf-8") as f:
        f.write(doc)
    js = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.js")
    r = subprocess.run(["node", js, "pdf", ruta_html, ruta_pdf], capture_output=True,
                       text=True, timeout=240)
    print("PDF:", ruta_pdf, r.stdout.strip(), r.stderr.strip()[-300:])
    return r.returncode == 0
