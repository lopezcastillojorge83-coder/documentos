# -*- coding: utf-8 -*-
"""Genera el diagrama del árbol de causas (HTML + SVG) y lo renderiza a PNG."""
import html
import os
import subprocess
import sys

from arbol import NODOS, POS, grupos_conexion

AQUI = os.path.dirname(os.path.abspath(__file__))
PASO = 255          # separación entre columnas (px)
X0 = 144            # centro de la columna 1
MARGEN = 30
NIVEL_TOP = [24, 148, 296, 480, 664]
NIVEL_ALTO = [80, 92, 128, 124, 140]
ANCHO_BASE = 228
ANCHO = {"0": 640, "1": 410, "1.2": 400, "1.3": 400, "C3": 420, "C4": 450}
ALTO_LEYENDA = 96
ANCHO_LIENZO = 1570
ALTO_LIENZO = NIVEL_TOP[4] + NIVEL_ALTO[4] + 36 + ALTO_LEYENDA + 24

ESTILO = {  # tipo: (fondo, borde, texto)
    "dano": ("#8E2A2A", "#5E1A1A", "#FFFFFF"),
    "hecho": ("#D6EAF8", "#2E6DA4", "#0F2A44"),
    "humano": ("#FFF1BF", "#B58900", "#3B2F00"),
    "causa": ("#C8EBC0", "#2E7D32", "#0F3A12"),
}
LINEA = "#334155"


def geometria():
    """id -> (x_centro, y_arriba, ancho, alto)."""
    g = {}
    for nid, (col, niv) in POS.items():
        w = ANCHO.get(nid, ANCHO_BASE)
        g[nid] = (X0 + (col - 1) * PASO, NIVEL_TOP[niv], w, NIVEL_ALTO[niv])
    return g


def caja(nid, geo):
    tipo, txt = NODOS[nid]
    x, y, w, h = geo[nid]
    fondo, borde, color = ESTILO[tipo]
    peso = 700 if tipo in ("dano", "causa") else 400
    ins = "" if nid == "0" else f'<b class="id">{nid}</b>'
    return (f'<div class="n" id="n{nid}" style="left:{x - w / 2:.1f}px;top:{y}px;'
            f'width:{w}px;height:{h}px;background:{fondo};border-color:{borde};'
            f'color:{color};font-weight:{peso}">{ins}<span>{html.escape(txt)}</span></div>')


def conectores(geo):
    """Devuelve el SVG con líneas, flechas y etiquetas de relación."""
    out = []

    def linea(x1, y1, x2, y2):
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')

    def flecha(x, y):  # punta hacia arriba, tocando el borde inferior del hecho
        out.append(f'<polygon class="fl" points="{x - 6:.1f},{y + 12:.1f} '
                   f'{x + 6:.1f},{y + 12:.1f} {x:.1f},{y + 1:.1f}"/>')

    for arriba, abajo, tipo in grupos_conexion():
        y_a = max(geo[n][1] + geo[n][3] for n in arriba)
        y_b = min(geo[n][1] for n in abajo)
        y_bus = (y_a + y_b) / 2
        xs = [geo[n][0] for n in arriba + abajo]
        for n in arriba:
            x, yt, _, h = geo[n]
            linea(x, yt + h + 10, x, y_bus)
            flecha(x, yt + h)
        for n in abajo:
            linea(geo[n][0], geo[n][1], geo[n][0], y_bus)
        if max(xs) - min(xs) > 0.5:
            linea(min(xs), y_bus, max(xs), y_bus)
        if tipo == "conjuncion":
            out.append(f'<text x="{geo[arriba[0]][0] + 9:.1f}" y="{y_bus - 6:.1f}">Conjunción</text>')
        elif tipo == "disyuncion":
            out.append(f'<text x="{geo[abajo[0]][0] + 9:.1f}" y="{y_bus + 17:.1f}">Disyunción</text>')
    return "\n".join(out)


def leyenda(y):
    items = [("dano", "Daño o lesión"),
             ("hecho", "Hecho o condición material"),
             ("humano", "Factor humano (conducta, desconocimiento u omisión de control)"),
             ("causa", "Causa primaria (fallo organizativo)")]
    chips = "".join(
        f'<span class="chip"><i style="background:{ESTILO[t][0]};border-color:{ESTILO[t][1]}">'
        f'</i>{html.escape(txt)}</span>' for t, txt in items)
    notas = ("<b>Cadena:</b> un solo antecedente &nbsp;·&nbsp; "
             "<b>Conjunción:</b> todos los antecedentes son necesarios y entre sí independientes "
             "&nbsp;·&nbsp; <b>Disyunción:</b> un mismo antecedente origina varios hechos "
             "&nbsp;·&nbsp; <b>Lectura:</b> de abajo hacia arriba (cada flecha va de la causa a su "
             "consecuencia); cada caja responde a «¿qué tuvo que ocurrir para que se produjera el "
             "hecho de arriba?».")
    return (f'<div class="ley" style="top:{y}px;height:{ALTO_LEYENDA}px">'
            f'<div class="chips">{chips}</div><div class="notas">{notas}</div></div>')


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fff;font-family:"Noto Sans","Liberation Sans",Arial,sans-serif}
#lienzo{position:relative;width:%(w)spx;height:%(h)spx;background:#fff;overflow:hidden}
svg{position:absolute;left:0;top:0}
svg line{stroke:%(l)s;stroke-width:2;stroke-linecap:square}
svg .fl{fill:%(l)s}
svg text{font-size:13px;font-style:italic;fill:#64748b;font-family:inherit}
.n{position:absolute;display:flex;align-items:center;justify-content:center;
text-align:center;padding:9px 11px;border:2px solid;border-radius:9px;
font-size:16px;line-height:1.24;z-index:2}
.n span{display:block}
.n .id{position:absolute;left:8px;top:-11px;background:#334155;color:#fff;
font-size:11.5px;font-weight:700;line-height:1;padding:3px 7px;border-radius:9px}
.tit{position:absolute;left:30px;top:22px;width:610px;z-index:2}
.tit h1{font-size:25px;color:#1f3a5f;line-height:1.15}
.tit p{font-size:14px;color:#475569;margin-top:6px;line-height:1.35}
.ley{position:absolute;left:30px;width:%(lw)spx;border-top:2px solid #cbd5e1;
padding-top:10px;z-index:2}
.chips{display:flex;flex-wrap:wrap;gap:6px 26px;font-size:14px;color:#1e293b}
.chip{display:inline-flex;align-items:center;gap:8px}
.chip i{display:inline-block;width:20px;height:14px;border:2px solid;border-radius:4px}
.notas{font-size:13px;color:#334155;line-height:1.4;margin-top:8px}
""" % {"w": ANCHO_LIENZO, "h": ALTO_LIENZO, "l": LINEA, "lw": ANCHO_LIENZO - 60}


JS = """
window.__report = function () {
  const mal = [];
  document.querySelectorAll('.n').forEach(function (n) {
    const s = n.querySelector('span');
    if (s.getBoundingClientRect().height > n.clientHeight - 14 ||
        s.scrollWidth > n.clientWidth - 8) mal.push(n.id);
  });
  return { desbordadas: mal };
};
"""


def construir_html(ruta_html):
    geo = geometria()
    cajas = "\n".join(caja(n, geo) for n in NODOS)
    y_ley = NIVEL_TOP[4] + NIVEL_ALTO[4] + 36
    titulo = ('<div class="tit"><h1>Árbol de causas</h1><p>Caída de altura desde un '
              'andamio durante trabajos de reparación de fachada.<br>Método: NTP 274 '
              '(INSHT), investigación de accidentes.</p></div>')
    doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
           f'<title>Árbol de causas</title><style>{CSS}</style></head><body>'
           f'<div id="lienzo"><svg width="{ANCHO_LIENZO}" height="{ALTO_LIENZO}">'
           f'{conectores(geo)}</svg>{titulo}{cajas}{leyenda(y_ley)}</div>'
           f'<script>{JS}</script></body></html>')
    with open(ruta_html, "w", encoding="utf-8") as f:
        f.write(doc)


def renderizar_png(ruta_html, ruta_png, escala=2.5):
    js = os.path.join(AQUI, "render.js")
    r = subprocess.run(["node", js, "png", ruta_html, ruta_png, str(escala)],
                       capture_output=True, text=True, timeout=240)
    print(r.stdout.strip(), r.stderr.strip()[-400:])
    return r.returncode == 0


if __name__ == "__main__":
    destino = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "..", "_work")
    os.makedirs(destino, exist_ok=True)
    h = os.path.join(destino, "arbol.html")
    construir_html(h)
    ok = renderizar_png(h, os.path.join(destino, "arbol_de_causas.png"))
    sys.exit(0 if ok else 1)
