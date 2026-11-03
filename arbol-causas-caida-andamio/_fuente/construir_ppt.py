# -*- coding: utf-8 -*-
"""Genera la presentación: diapositivas PNG, .pptx (con notas) y PDF.

Uso: python3 construir_ppt.py [carpeta_salida]
"""
import json
import os
import shutil
import subprocess
import sys

import presentacion

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, ".."))
TRABAJO = os.path.join(RAIZ, "_work", "ppt")
NOMBRE = "Presentacion_Arbol_de_Causas"
PNG_ARBOL = "arbol_de_causas.png"
ESCALA = 1.5   # 2880x1620 px por diapositiva


def renderizar():
    """Escribe el HTML de cada diapositiva y lo captura como PNG."""
    os.makedirs(TRABAJO, exist_ok=True)
    shutil.copy(os.path.join(RAIZ, PNG_ARBOL), os.path.join(TRABAJO, PNG_ARBOL))
    diapos = presentacion.diapositivas(PNG_ARBOL)
    htmls = []
    for n, d in enumerate(diapos, 1):
        ruta = os.path.join(TRABAJO, f"diapo{n:02d}.html")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(d["html"])
        htmls.append(ruta)
    r = subprocess.run(["node", os.path.join(AQUI, "render_slides.js"), str(ESCALA)] + htmls,
                       capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        sys.exit("falló el render: " + r.stderr[-500:])
    informe = json.loads(r.stdout.strip().splitlines()[-1])
    problemas = {k: v for k, v in informe.items() if v}
    for k, v in problemas.items():
        print("DESBORDE", k, v)
    for d, h in zip(diapos, htmls):
        d["png"] = h.replace(".html", ".png")
    return diapos, problemas


if __name__ == "__main__":
    salida = sys.argv[1] if len(sys.argv) > 1 else RAIZ
    diapos, problemas = renderizar()
    print(len(diapos), "diapositivas;", "sin desbordes" if not problemas else "HAY DESBORDES")
    try:
        import render_pptx
        render_pptx.escribir_pptx(diapos, os.path.join(salida, NOMBRE + ".pptx"))
        print("PPTX:", os.path.join(salida, NOMBRE + ".pptx"))
        render_pptx.escribir_pdf(diapos, os.path.join(salida, NOMBRE + ".pdf"), TRABAJO)
        print("PDF:", os.path.join(salida, NOMBRE + ".pdf"))
    except ImportError:
        print("(render_pptx todavía no existe)")
