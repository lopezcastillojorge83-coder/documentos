# -*- coding: utf-8 -*-
"""Genera diagrama, DOCX y PDF del informe.

Uso: python3 construir.py [carpeta_salida]
"""
import os
import shutil
import sys

import diagrama
import contenido
import render_docx

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, ".."))
TRABAJO = os.path.join(RAIZ, "_work")
NOMBRE = "Arbol_de_Causas_Caida_Andamio"
ENCABEZADO = "NTP 274 · Árbol de causas · Caída de altura desde andamio"


def main(salida):
    os.makedirs(salida, exist_ok=True)
    os.makedirs(TRABAJO, exist_ok=True)
    html = os.path.join(TRABAJO, "arbol.html")
    png = os.path.join(TRABAJO, contenido.FIGURA)
    diagrama.construir_html(html)
    if not diagrama.renderizar_png(html, png):
        sys.exit("falló el render del diagrama")
    shutil.copy(png, os.path.join(salida, contenido.FIGURA))
    docx = os.path.join(salida, NOMBRE + ".docx")
    render_docx.escribir_docx(contenido.bloques(), docx, TRABAJO,
                              contenido.TITULO, ENCABEZADO)
    print("DOCX:", docx)
    try:
        import render_html
        render_html.escribir_pdf(contenido.bloques(), os.path.join(salida, NOMBRE + ".pdf"),
                                 TRABAJO, ENCABEZADO)
    except ImportError:
        print("(sin render_html todavía: PDF omitido)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else RAIZ)
