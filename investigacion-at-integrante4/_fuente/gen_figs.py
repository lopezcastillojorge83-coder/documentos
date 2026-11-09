# -*- coding: utf-8 -*-
"""Genera las figuras del informe (SVG -> PNG con Chrome headless)."""
import os
import subprocess
from xml.sax.saxutils import escape

BUILD = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(BUILD), "figuras")
os.makedirs(OUT, exist_ok=True)
# Ruta de Chrome/Chromium en modo headless (variable de entorno CHROME_BIN).
CHROME = os.environ.get("CHROME_BIN", "chromium")
FONT = "Noto Sans, Arial, sans-serif"

NAVY = "#1F3864"
INK = "#222222"


def render(name, svg, w, h, scale=1):
    html = os.path.join(BUILD, name + ".html")
    with open(html, "w", encoding="utf-8") as f:
        f.write('<html><head><meta charset="utf-8"></head>'
                '<body style="margin:0;background:#ffffff">' + svg + "</body></html>")
    with open(os.path.join(BUILD, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    png = os.path.join(OUT, name + ".png")
    subprocess.run([CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=%d" % scale,
                    "--window-size=%d,%d" % (w, h), "--screenshot=" + png,
                    "file://" + html], check=True, capture_output=True, timeout=120)
    return png


def text_lines(cx, cy, lines, size, weight="normal", color=INK, lh=None, anchor="middle"):
    lh = lh or size * 1.12
    y0 = cy - (len(lines) - 1) * lh / 2 + size * 0.36
    out = ['<text font-family="%s" font-size="%d" font-weight="%s" fill="%s" text-anchor="%s">'
           % (FONT, size, weight, color, anchor)]
    for i, ln in enumerate(lines):
        out.append('<tspan x="%.1f" y="%.1f">%s</tspan>' % (cx, y0 + i * lh, escape(ln)))
    out.append("</text>")
    return "".join(out)


MARKERS = """<defs>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="#333333"/></marker>
<marker id="arrB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="#1F3864"/></marker>
<marker id="arrR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="#B02A37"/></marker>
<pattern id="hatch" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="14" stroke="#9a9a9a" stroke-width="3"/></pattern>
</defs>"""


# ---------------------------------------------------------------------------
# Figura 2. Árbol de causas (de izquierda: antecedentes, a derecha: lesión)
# ---------------------------------------------------------------------------
def arbol():
    W, H = 2400, 1466
    BW, BH = 290, 130
    colx = [2225 - c * 343 for c in range(7)]
    rowy = [84 + r * 154 for r in range(8)]

    # id: (col, row, kind, lines)  kind: final | var | perm | hip
    N = {
        "A": (0, 4, "final", ["LESIÓN: TCE severo", "con pérdida del", "conocimiento por", "golpe contra el piso"]),
        "B": (1, 4, "var", ["Caída de 4,35 m", "desde el banco al", "plano de referencia"]),
        "D": (2, 1, "var", ["Se tropieza sobre", "el banco y pierde", "el equilibrio", "(versión trabajador)"]),
        "E": (2, 4, "perm", ["Lados izquierdo y", "frontal del banco", "sin baranda"]),
        "F": (2, 6, "var", ["La eslinga no toma", "carga: absorbedor", "sin activar"]),
        "G": (3, 0, "perm", ["Limpieza en húmedo", "sobre el banco a", "4,35 m, turno", "nocturno (00:30)"]),
        "H4": (3, 1, "hip", ["H4: superficie", "húmeda u objetos", "sobre el banco"]),
        "H5": (3, 2, "hip", ["H5: iluminación", "insuficiente en", "posición Golfo"]),
        "I": (3, 3, "perm", ["Banco usado sin", "inspección previa", "(sin lista de", "chequeo)"]),
        "H1": (3, 5, "hip", ["H1: no estaba", "conectado al", "anclaje al caer"]),
        "H2": (3, 7, "hip", ['H2: gancho 1-1/4"', "con doble seguro", "dañado se abre o", "se zafa"]),
        "K": (4, 5, "perm", ["Anclaje a 4,15 m:", "0,20 m por debajo", "del plano de", "trabajo (4,35 m)"]),
        "L": (4, 6, "var", ["Permiso de trabajo", "sin firma del", "trabajador"]),
        "O": (4, 7, "perm", ["Eslinga en uso", "sin inspección", "pre-uso"]),
        "M": (5, 5, "perm", ["Sin cálculo de", "claridad (5,09 m >", "4,15 m) ni anclaje", "elevado"]),
        "N": (5, 6, "var", ["Coordinador TSA", "avala el permiso sin", "verificar firmas ni", "condiciones"]),
        "P": (5, 7, "perm", ["Eslinga fabricada", "en 2013 (12,9 años);", "sin control de", "vida útil"]),
        "J": (6, 4, "perm", ["No existe programa", "de prevención y", "protección contra", "caídas"]),
    }

    def box(nid):
        c, r, k, _ = N[nid]
        cx, cy = colx[c], rowy[r]
        return cx - BW / 2, cy - BH / 2, cx + BW / 2, cy + BH / 2, cx, cy

    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H),
             MARKERS, '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (W, H)]

    edges = []  # (d, dashed, arrow)

    def seg(points, dashed=False, arrow=False):
        d = "M%.1f,%.1f " % points[0] + " ".join("L%.1f,%.1f" % p for p in points[1:])
        edges.append((d, dashed, arrow))

    def join(target, sources, xj=None, dashed_target=False):
        l, t, r, b, cx, cy = box(target)
        xj = xj if xj is not None else l - 26
        any_solid = False
        for s, dashed in sources:
            sl, st, sr, sb, scx, scy = box(s)
            pts = [(sr, scy), (xj, scy)]
            if abs(scy - cy) > 0.5:
                pts.append((xj, cy))
            seg(pts, dashed=dashed)
            any_solid = any_solid or not dashed
        seg([(xj, cy), (l, cy)], dashed=dashed_target or not any_solid, arrow=True)

    join("A", [("B", False)])
    join("B", [("D", False), ("E", False), ("F", False)])
    join("D", [("G", False), ("H4", True), ("H5", True)])
    join("F", [("H1", True), ("H2", True)], dashed_target=True)
    join("H1", [("K", True), ("L", True)], dashed_target=True)
    join("H2", [("O", True)], dashed_target=True)
    join("K", [("M", False)])
    join("L", [("N", False)])
    join("O", [("P", False)])
    # E <- I y J (J por una línea horizontal larga en la fila 4)
    el, et, er, eb, ecx, ecy = box("E")
    il, it, ir, ib, icx, icy = box("I")
    jl, jt, jr, jb, jcx, jcy = box("J")
    xj = el - 26
    seg([(ir, icy), (xj, icy), (xj, ecy)])
    seg([(jr, jcy), (xj, ecy)])
    seg([(xj, ecy), (el, ecy)], arrow=True)
    # I <- J (sube por el hueco entre columnas 6 y 5 y avanza por la fila 3)
    gap = jr + 26
    seg([(jr, jcy - 24), (gap, jcy - 24), (gap, icy), (il, icy)], arrow=True)
    # M <- J
    ml, mt, mr, mb, mcx, mcy = box("M")
    seg([(jr, jcy + 24), (gap, jcy + 24), (gap, mcy), (ml, mcy)], arrow=True)

    for d, dashed, arrow in edges:
        parts.append('<path d="%s" fill="none" stroke="#333333" stroke-width="2.6"%s%s/>'
                     % (d, ' stroke-dasharray="11,7"' if dashed else "",
                        ' marker-end="url(#arr)"' if arrow else ""))

    for nid, (c, r, kind, lines) in N.items():
        l, t, rr, b, cx, cy = box(nid)
        if kind == "final":
            parts.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="#F8D7DA" stroke="#B02A37" stroke-width="3"/>' % (l, t, BW, BH))
            parts.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="none" stroke="#B02A37" stroke-width="2"/>' % (l + 6, t + 6, BW - 12, BH - 12))
            parts.append(text_lines(cx, cy, lines, 23, weight="bold", color="#7A1020", lh=26))
        elif kind == "var":
            parts.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="#FFFFFF" stroke="%s" stroke-width="2.8"/>' % (l, t, BW, BH, NAVY))
            parts.append(text_lines(cx, cy, lines, 24, lh=27))
        elif kind == "perm":
            parts.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="34" ry="34" fill="#E8F0FA" stroke="%s" stroke-width="2.8"/>' % (l, t, BW, BH, NAVY))
            parts.append(text_lines(cx, cy, lines, 24, lh=27))
        else:
            parts.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="10" ry="10" fill="#FFF4CC" stroke="#9A6B00" stroke-width="2.8" stroke-dasharray="12,7"/>' % (l, t, BW, BH))
            parts.append(text_lines(cx, cy, lines, 24, color="#5A3E00", lh=27))
        # etiqueta del nodo
        bx, by = l + 4, t - 2
        lab = nid
        wlab = 30 if len(lab) == 1 else 42
        parts.append('<rect x="%.1f" y="%.1f" width="%d" height="28" rx="6" fill="%s"/>' % (bx, by - 16, wlab, "#B02A37" if kind == "final" else ("#9A6B00" if kind == "hip" else NAVY)))
        parts.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">%s</text>' % (bx + wlab / 2, by + 5, FONT, lab))

    # Leyenda
    ly = 1268
    parts.append('<line x1="20" y1="%d" x2="%d" y2="%d" stroke="#BBBBBB" stroke-width="2"/>' % (ly - 22, W - 20, ly - 22))
    x = 30
    parts.append('<rect x="%d" y="%d" width="70" height="40" fill="#fff" stroke="%s" stroke-width="2.8"/>' % (x, ly, NAVY))
    parts.append(text_lines(x + 82, ly + 20, ["Hecho inhabitual (variación)"], 23, anchor="start"))
    x = 470
    parts.append('<rect x="%d" y="%d" width="70" height="40" rx="20" fill="#E8F0FA" stroke="%s" stroke-width="2.8"/>' % (x, ly, NAVY))
    parts.append(text_lines(x + 82, ly + 20, ["Hecho permanente o habitual"], 23, anchor="start"))
    x = 910
    parts.append('<rect x="%d" y="%d" width="70" height="40" rx="8" fill="#FFF4CC" stroke="#9A6B00" stroke-width="2.8" stroke-dasharray="12,7"/>' % (x, ly))
    parts.append(text_lines(x + 82, ly + 20, ["Hipótesis por verificar"], 23, anchor="start"))
    x = 1290
    parts.append('<rect x="%d" y="%d" width="70" height="40" fill="#F8D7DA" stroke="#B02A37" stroke-width="3"/>' % (x, ly))
    parts.append(text_lines(x + 82, ly + 20, ["Lesión (hecho final)"], 23, anchor="start"))
    x = 1650
    parts.append('<path d="M%d,%d L%d,%d" stroke="#333" stroke-width="2.6" marker-end="url(#arr)"/>' % (x, ly + 20, x + 70, ly + 20))
    parts.append(text_lines(x + 82, ly + 20, ["Relación comprobada"], 23, anchor="start"))
    x = 2010
    parts.append('<path d="M%d,%d L%d,%d" stroke="#333" stroke-width="2.6" stroke-dasharray="11,7" marker-end="url(#arr)"/>' % (x, ly + 20, x + 70, ly + 20))
    parts.append(text_lines(x + 82, ly + 20, ["Relación hipotética"], 23, anchor="start"))
    parts.append(text_lines(30, ly + 82, [
        "Lectura: de izquierda (antecedentes) a derecha (lesión). Las líneas que se unen antes de una flecha indican "
        "conjunción: todos esos antecedentes fueron necesarios. Las letras identifican los nodos citados en el informe."],
        22, anchor="start", color="#444444"))
    parts.append(text_lines(30, ly + 118, [
        "J es una causa común (disyunción): origina E, I y M. H1 y H2 son hipótesis alternativas que explican F: basta con "
        "que una de ellas se confirme."], 22, anchor="start", color="#444444"))
    parts.append(text_lines(30, ly + 154, [
        "Fuente: elaboración propia con el método del árbol de causas (manual OSALAN) a partir de los datos de la guía de laboratorio."],
        22, anchor="start", color="#444444"))
    parts.append("</svg>")
    return render("fig2_arbol_de_causas", "".join(parts), W, H)


# ---------------------------------------------------------------------------
# Figura 1. Secuencia cronológica
# ---------------------------------------------------------------------------
def linea_tiempo():
    W = 1130
    ev = [
        ("12/08/2026", "05:00", "Fin del turno anterior",
         ["Inicia un descanso de 16 horas antes del turno del accidente."], NAVY),
        ("12/08/2026", "21:00", "Ingreso al turno nocturno (jornada mixta, turno rotativo)",
         ["Permiso de trabajo en alturas firmado por el coordinador TSA y los operarios,",
          "sin la firma del accidentado. Sin listas de chequeo de arnés, eslinga ni banco."], NAVY),
        ("21:00 a 00:30", "3 h 30 min", "Limpieza en húmedo de la aeronave sobre el banco a 4,35 m",
         ["Banco con baranda solo en el lado derecho; punto de anclaje a 4,15 m,",
          "0,20 m por debajo del plano de trabajo."], NAVY),
        ("13/08/2026", "00:30", "Tropiezo y caída de 4,35 m (versión del trabajador)",
         ['La eslinga no toma carga (absorbedor sin activar; gancho de 1-1/4" con doble',
          "seguro dañado). La cabeza impacta contra el piso de la plataforma."], "#B02A37"),
        ("13/08/2026", "desde 00:30", "Atención en el sitio y traslado a la Clínica de Occidente",
         ["Diagnóstico de ingreso: trauma craneoencefálico severo con pérdida del",
          "conocimiento. Evento clasificado como accidente grave (Res. 1401 de 2007)."], "#B02A37"),
        ("13/08/2026", "reporte", "FURAT a ARL SURA y EPS; reporte a la Dirección Territorial",
         ["Plazo legal: 2 días hábiles, hasta el martes 18/08/2026 (el lunes 17/08/2026",
          "es festivo). El FURAT se diligencia el mismo 13/08/2026."], NAVY),
        ("hasta 28/08/2026", "15 días", "Investigación del accidente grave y remisión a la ARL",
         ["Equipo investigador con profesional con licencia en SST (Res. 1401 de 2007).",
          "Fecha límite tomada con criterio conservador (días calendario)."], NAVY),
        ("13/08 a 11/09/2026", "30 días", "Incapacidad temporal: 15 + 15 días, prorrogable",
         ["Seguimiento médico y de rehabilitación con la ARL; plan de reintegro."], NAVY),
    ]
    pitch = 118
    top = 60
    H = top + pitch * len(ev) + 75
    xline = 300
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H),
             MARKERS, '<rect width="%d" height="%d" fill="#fff"/>' % (W, H)]
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#8EA9DB" stroke-width="6"/>' % (xline, top - 20, xline, H - 80))
    for i, (d, h, title, det, col) in enumerate(ev):
        y = top + i * pitch + 18
        parts.append(text_lines(xline - 30, y - 12, [d], 24, weight="bold", color=col, anchor="end"))
        parts.append(text_lines(xline - 30, y + 18, [h], 22, color="#444444", anchor="end"))
        parts.append('<circle cx="%d" cy="%d" r="15" fill="%s" stroke="#fff" stroke-width="4"/>' % (xline, y, col))
        parts.append(text_lines(xline + 40, y - 12, [title], 24, weight="bold", color=col, anchor="start"))
        for k, ln in enumerate(det):
            parts.append(text_lines(xline + 40, y + 18 + k * 27, [ln], 21, color="#333333", anchor="start"))
    parts.append(text_lines(20, H - 42, ["Nota: la guía indica que el turno anterior terminó el 13/08 a las 05:00; se ubica el 12/08 para que sea coherente con"], 18, color="#666666", anchor="start"))
    parts.append(text_lines(20, H - 18, ["las 3 h 30 min laboradas antes del accidente de las 00:30 del 13/08/2026 (ver sección 1.2 del informe)."], 18, color="#666666", anchor="start"))
    parts.append("</svg>")
    return render("fig1_secuencia_cronologica", "".join(parts), W, H)


# ---------------------------------------------------------------------------
# Figura 3. Esquema de alturas, caída libre y requerimiento de claridad
# ---------------------------------------------------------------------------
def esquema():
    W, H = 1400, 1010
    g = 940            # y del plano de referencia
    k = 140            # px por metro

    def y(h):
        return g - k * h
    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H),
         MARKERS, '<rect width="%d" height="%d" fill="#fff"/>' % (W, H)]
    # suelo
    p.append('<rect x="40" y="%d" width="720" height="40" fill="url(#hatch)"/>' % g)
    p.append('<line x1="40" y1="%d" x2="760" y2="%d" stroke="#333" stroke-width="4"/>' % (g, g))
    p.append(text_lines(330, g + 56, ["Plano de referencia: piso de la plataforma (0,00 m)"], 21, color="#333", anchor="middle"))
    # escala
    p.append('<line x1="62" y1="%d" x2="62" y2="%d" stroke="#666" stroke-width="2"/>' % (y(0), y(6.2)))
    for m in range(0, 7):
        p.append('<line x1="56" y1="%d" x2="68" y2="%d" stroke="#666" stroke-width="2"/>' % (y(m), y(m)))
        p.append(text_lines(50, y(m), ["%d m" % m], 19, color="#555", anchor="end"))
    # banco: plataforma, patas, escalera con pasamanos
    yp = y(4.35)
    p.append('<rect x="300" y="%.1f" width="230" height="14" fill="#E3B505" stroke="#7A5C00" stroke-width="2"/>' % yp)
    for xl in (320, 510):
        p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%d" stroke="#B08A00" stroke-width="7"/>' % (xl, yp + 14, xl, g))
    p.append('<line x1="300" y1="%.1f" x2="128" y2="%d" stroke="#B08A00" stroke-width="8"/>' % (yp + 8, g))
    steps = 9
    for s in range(1, steps):
        t = s / steps
        xs = 300 - t * 172
        ys = yp + 8 + t * (g - yp - 8)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#7A5C00" stroke-width="4"/>' % (xs - 26, ys, xs + 18, ys))
    p.append('<line x1="300" y1="%.1f" x2="128" y2="%.1f" stroke="#B08A00" stroke-width="5"/>' % (yp - 110, g - 110))
    p.append('<line x1="300" y1="%.1f" x2="300" y2="%.1f" stroke="#B08A00" stroke-width="5"/>' % (yp - 110, yp))
    p.append(text_lines(165, y(5.25), ["Baranda solo", "en un lado"], 19, color="#7A5C00"))
    p.append(text_lines(600, yp - 2, ["Borde sin", "baranda"], 19, color="#B02A37"))
    p.append('<path d="M548,%.1f L532,%.1f" stroke="#B02A37" stroke-width="3" marker-end="url(#arrR)"/>' % (yp - 4, yp + 2))
    # trabajador (1,62 m) parado cerca del borde
    xw = 470
    yh = y(4.35 + 1.62)
    p.append('<circle cx="%d" cy="%.1f" r="20" fill="#F4C7A1" stroke="#333" stroke-width="2.5"/>' % (xw, yh + 20))
    p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#1F3864" stroke-width="10"/>' % (xw, yh + 40, xw, yp - 110))
    p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#1F3864" stroke-width="8"/>' % (xw, yp - 110, xw - 22, yp))
    p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#1F3864" stroke-width="8"/>' % (xw, yp - 110, xw + 20, yp))
    p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#1F3864" stroke-width="7"/>' % (xw, yh + 62, xw + 46, yh + 108))
    p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#1F3864" stroke-width="7"/>' % (xw, yh + 62, xw - 38, yh + 112))
    yd = y(4.35 + 1.35)
    p.append('<circle cx="%d" cy="%.1f" r="8" fill="#B02A37"/>' % (xw - 12, yd))
    # anclaje
    ya = y(4.15)
    p.append('<circle cx="510" cy="%.1f" r="11" fill="none" stroke="#111" stroke-width="4"/>' % ya)
    p.append('<path d="M%d,%.1f C %d,%.1f %d,%.1f 510,%.1f" fill="none" stroke="#2E7D32" stroke-width="4" stroke-dasharray="10,7"/>'
             % (xw - 12, yd, xw - 70, yd + 90, 470, ya - 60, ya - 10))
    # cotas
    p.append('<line x1="548" y1="%.1f" x2="548" y2="%d" stroke="#1F3864" stroke-width="2.5" marker-end="url(#arrB)"/>' % (yp + 10, g - 2))
    p.append('<line x1="548" y1="%d" x2="548" y2="%.1f" stroke="#1F3864" stroke-width="2.5" marker-end="url(#arrB)"/>' % (g - 2, yp + 12))
    p.append(text_lines(556, (yp + g) / 2 - 16, ["4,35 m", "plano de", "trabajo"], 19, weight="bold", color=NAVY, anchor="start"))
    p.append('<line x1="400" y1="%.1f" x2="400" y2="%.1f" stroke="#1F3864" stroke-width="2.5" marker-end="url(#arrB)"/>' % (yp - 4, yh + 6))
    p.append('<line x1="400" y1="%.1f" x2="400" y2="%.1f" stroke="#1F3864" stroke-width="2.5" marker-end="url(#arrB)"/>' % (yh + 6, yp - 4))
    p.append(text_lines(392, (yp + yh) / 2, ["1,62 m"], 20, weight="bold", color=NAVY, anchor="end"))
    p.append(text_lines(415, ya + 50, ["Anclaje", "4,15 m (0,20 m", "bajo los pies)"], 17, weight="bold", color="#111"))
    p.append(text_lines(388, yd, ["Anillo D aprox. 5,70 m"], 17, weight="bold", color="#B02A37", anchor="end"))
    p.append('<line x1="392" y1="%.1f" x2="%d" y2="%.1f" stroke="#B02A37" stroke-width="1.5"/>' % (yd, xw - 22, yd))
    # recorrido teórico del anillo D si estaba conectado
    xb = 660
    seq = [(5.70, 2.35, "#B02A37", ["Caída", "libre", "3,35 m"]),
           (2.35, 1.28, "#E07B00", ["Absorbedor", "1,07 m"]),
           (1.28, -0.07, "#7F7F7F", ["Anillo D", "a pies", "1,35 m"])]
    p.append(text_lines(xb, y(6.12), ["Si hubiera estado", "conectado (teórico)"], 19, weight="bold", color="#333"))
    for top_h, bot_h, col, lab in seq:
        p.append('<rect x="%d" y="%.1f" width="26" height="%.1f" fill="%s"/>' % (xb - 13, y(top_h), y(bot_h) - y(top_h), col))
        p.append(text_lines(xb + 20, (y(top_h) + y(bot_h)) / 2, lab, 18, weight="bold", color=col, anchor="start"))
    p.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#B02A37" stroke-width="3" stroke-dasharray="6,5"/>' % (xb - 40, y(-0.07), xb + 40, y(-0.07)))
    p.append(text_lines(xb - 20, y(-0.07) - 44, ["Pies:", "-0,07 m", "(impacto)"], 17, weight="bold", color="#B02A37", anchor="end"))
    p.append(text_lines(495, yp - 72, ["Eslinga 1,80 m", "(conexión teórica)"], 16, weight="bold", color="#2E7D32", anchor="start"))

    # Panel derecho: cálculos
    x0 = 830
    p.append('<rect x="%d" y="20" width="552" height="975" rx="14" fill="#F7F9FC" stroke="#C9D3E3" stroke-width="2"/>' % x0)
    rows = [
        ("b", "Datos del caso"),
        ("t", "Plano de trabajo 4,35 m; anclaje 4,15 m"),
        ("t", "Estatura 1,62 m; eslinga 1,80 m"),
        ("t", "Elongación máx. del absorbedor 1,07 m"),
        ("s", "Supuestos: masa 70 kg; anillo D a 1,35 m de"),
        ("s", "los pies; factor de seguridad 0,60 m; g = 9,81"),
        ("gap", ""),
        ("b", "1. Caída real (sin detención)"),
        ("t", "t = raíz(2h/g) = raíz(2 · 4,35 / 9,81) = 0,94 s"),
        ("t", "v = raíz(2gh) = 9,24 m/s (33,3 km/h)"),
        ("t", "E = m·g·h = 70 · 9,81 · 4,35 = 2,99 kJ"),
        ("gap", ""),
        ("b", "2. Caída libre si estaba conectado"),
        ("t", "CL = 1,35 + 0,20 + 1,80 = 3,35 m"),
        ("r", "CL > 1,80 m (límite de diseño de la eslinga)"),
        ("t", "Factor de caída = 3,35 / 1,80 = 1,86"),
        ("gap", ""),
        ("b", "3. Requerimiento de claridad (RC)"),
        ("t", "RC = LE + DA + E + FS"),
        ("t", "RC = 1,80 + 1,07 + 1,62 + 0,60 = 5,09 m"),
        ("t", "Disponible bajo el anclaje = 4,15 m"),
        ("r", "Déficit = 0,94 m: la configuración no evitaba"),
        ("r", "el impacto aunque estuviera conectado"),
    ]
    yy = 62
    for kind, txt in rows:
        if kind == "gap":
            yy += 14
            continue
        if kind == "b":
            p.append(text_lines(x0 + 22, yy, [txt], 23, weight="bold", color=NAVY, anchor="start"))
        elif kind == "r":
            p.append(text_lines(x0 + 22, yy, [txt], 21, weight="bold", color="#B02A37", anchor="start"))
        elif kind == "s":
            p.append(text_lines(x0 + 22, yy, [txt], 20, color="#666666", anchor="start"))
        else:
            p.append(text_lines(x0 + 22, yy, [txt], 21, color="#222222", anchor="start"))
        yy += 33
    # barras
    yy += 10
    sc = 100
    p.append(text_lines(x0 + 22, yy, ["Claridad bajo el anclaje (m)"], 21, weight="bold", color=NAVY, anchor="start"))
    yy += 22
    p.append('<rect x="%d" y="%d" width="%d" height="34" fill="#B02A37"/>' % (x0 + 22, yy, 5.09 * sc))
    p.append(text_lines(x0 + 30, yy + 17, ["Requerida 5,09"], 20, weight="bold", color="#fff", anchor="start"))
    yy += 44
    p.append('<rect x="%d" y="%d" width="%d" height="34" fill="#2E7D32"/>' % (x0 + 22, yy, 4.15 * sc))
    p.append(text_lines(x0 + 30, yy + 17, ["Disponible 4,15"], 20, weight="bold", color="#fff", anchor="start"))
    p.append(text_lines(x0 + 22, yy + 70, ["RC: longitud de eslinga (LE) + elongación del absorbedor"], 18, color="#666666", anchor="start"))
    p.append(text_lines(x0 + 22, yy + 94, ["(DA) + estatura (E) + factor de seguridad (FS, mín. 0,60 m)."], 18, color="#666666", anchor="start"))
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#B02A37" stroke-width="3" stroke-dasharray="6,5"/>' % (x0 + 22 + 4.15 * sc, yy - 50, x0 + 22 + 4.15 * sc, yy + 40))
    p.append(text_lines(x0 + 22 + 4.20 * sc, yy + 17, ["-0,94"], 20, weight="bold", color="#B02A37", anchor="start"))
    p.append("</svg>")
    return render("fig3_esquema_claridad", "".join(p), W, H)


if __name__ == "__main__":
    for fn in (linea_tiempo, arbol, esquema):
        print(fn())
