#!/usr/bin/env python3
"""Genera la lámina 05: cómo pegar las uniones de la cercha de balso.

Dibuja los tipos de unión, la regla de los ejes, la cartela, el paso a paso
de un nodo y dónde van las cartelas en las opciones 1 y 2. Las fuerzas de las
barras salen del método de nodos de generar_laminas.py.

Uso:
    python3 generar_lamina_uniones.py

Las medidas de la cartela son para barras de 5 × 5 mm: monta 1.5 cm sobre
cada barra (unas 3 veces el ancho de la barra).
"""

import math
import os

from generar_laminas import (
    C,
    CARPETA,
    Lienzo,
    _opciones,
    analizar,
    color_fuerza,
    encabezado,
    envolver,
    leyenda_linea,
)

MADERA = "#efd9b0"
MADERA_BORDE = "#9c7a46"
VETA = "#d4b27c"
PAPEL = "#fbfaf6"
REJILLA = "#ece5d5"
PEGANTE = "#ef6c00"
AMBAR = "#f9a825"
GRIS_CARTELA = "#78909c"

# Detalle de un nodo. Unidad: ancho de la barra.
ANG_DIAG = math.radians(55)
LARGO_DIAG = 7.6
R_CARTELA = 3.5  # 3 anchos de traslapo después de la unión (1.5 cm con barras de 5 mm)

# Cartelas en las caras completas (cm)
R_CARTELA_CM = 2.0
ANCHO_BARRA_CM = 0.5

# ---------------------------------------------------------------------------
# Geometría
# ---------------------------------------------------------------------------


def tira(origen, ang, t0, t1, ancho=1.0):
    """Rectángulo de una barra cuyo eje sale de origen en la dirección ang."""
    dx, dy = math.cos(ang), math.sin(ang)
    nx, ny = -dy, dx
    h = ancho / 2
    ox, oy = origen
    return [
        (ox + dx * t0 + nx * h, oy + dy * t0 + ny * h),
        (ox + dx * t1 + nx * h, oy + dy * t1 + ny * h),
        (ox + dx * t1 - nx * h, oy + dy * t1 - ny * h),
        (ox + dx * t0 - nx * h, oy + dy * t0 - ny * h),
    ]


def recortar(poligono, a, b, c):
    """Deja la parte del polígono donde a·u + b·v + c >= 0."""
    salida = []
    n = len(poligono)
    for i in range(n):
        p, q = poligono[i], poligono[(i + 1) % n]
        fp = a * p[0] + b * p[1] + c
        fq = a * q[0] + b * q[1] + c
        if fp >= -1e-12:
            salida.append(p)
        if (fp >= -1e-12) != (fq >= -1e-12):
            t = fp / (fp - fq)
            salida.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return salida


def casco(puntos):
    """Envolvente convexa (cadena monótona)."""
    pts = sorted({(round(x, 6), round(y, 6)) for x, y in puntos})
    if len(pts) <= 2:
        return pts

    def cruz(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    inf, sup = [], []
    for p in pts:
        while len(inf) >= 2 and cruz(inf[-2], inf[-1], p) <= 0:
            inf.pop()
        inf.append(p)
    for p in reversed(pts):
        while len(sup) >= 2 and cruz(sup[-2], sup[-1], p) <= 0:
            sup.pop()
        sup.append(p)
    return inf[:-1] + sup[:-1]


def geometria_nodo(tipo="tope", e=0.0, desplazar=0.0):
    """Cuerda, montante y diagonal alrededor de un nodo de la cuerda inferior."""
    cuerda = tira((0, 0), 0, -4.6, 5.8)
    if tipo == "traslape":
        montante = tira((0, 0), math.pi / 2, -0.5, 6.4)
        diag = recortar(tira((0, 0), ANG_DIAG, -1.5, LARGO_DIAG), 0, 1, 0.5)
        return cuerda, montante, diag, (0.0, 0.0)
    montante = tira((0, 0), math.pi / 2, 0.5, 6.4)
    diag = recortar(tira((e, 0), ANG_DIAG, 0, LARGO_DIAG), 0, 1, -0.5)
    if e < 1.0:
        diag = recortar(diag, 1, 0, -0.5)
    dx, dy = math.cos(ANG_DIAG) * desplazar, math.sin(ANG_DIAG) * desplazar
    diag = [(u + dx, v + dy) for u, v in diag]
    return cuerda, montante, diag, (e + dx, dy)


def bordes_pegados(poly):
    """Bordes de la diagonal que tocan la cuerda (v = 0.5) o el montante (u = 0.5)."""
    bordes = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        en_cuerda = abs(p[1] - 0.5) < 1e-6 and abs(q[1] - 0.5) < 1e-6
        en_montante = abs(p[0] - 0.5) < 1e-6 and abs(q[0] - 0.5) < 1e-6
        if (en_cuerda or en_montante) and math.dist(p, q) > 1e-6:
            bordes.append((p, q))
    return bordes


def cartela_nodo():
    pts = []
    for ang in (0, math.pi, math.pi / 2, ANG_DIAG):
        pts += tira((0, 0), ang, 0, R_CARTELA)
    return casco(pts)


# ---------------------------------------------------------------------------
# Dibujo
# ---------------------------------------------------------------------------

_clip = [0]


def poligono(lz, pts, relleno="none", borde="none", grosor=1.0, opacidad=1.0, guiones=None,
             op_relleno=None):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    extra = f' stroke-dasharray="{guiones}"' if guiones else ""
    if op_relleno is not None:
        extra += f' fill-opacity="{op_relleno}"'
    lz.partes.append(
        f'<polygon points="{d}" fill="{relleno}" stroke="{borde}" stroke-width="{grosor}" '
        f'opacity="{opacidad}" stroke-linejoin="round"{extra}/>'
    )


class Vista:
    """Convierte coordenadas locales (u, v) en píxeles."""

    def __init__(self, lz, cx, cy, k):
        self.lz, self.cx, self.cy, self.k = lz, cx, cy, k

    def P(self, u, v):
        return self.cx + u * self.k, self.cy - v * self.k

    def linea(self, a, b, color, grosor=2.0, guiones=None, opacidad=1.0, extremo="round"):
        self.lz.linea(*self.P(*a), *self.P(*b), color, grosor, guiones, opacidad, extremo)


def barra(vista, poly, origen, ang, sombra=False):
    lz = vista.lz
    pts = [vista.P(u, v) for u, v in poly]
    if sombra:
        poligono(lz, [(x + 5, y + 6) for x, y in pts], "#000000", opacidad=0.16)
    _clip[0] += 1
    cid = f"veta{_clip[0]}"
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    lz.partes.append(f'<clipPath id="{cid}"><polygon points="{d}"/></clipPath>')
    poligono(lz, pts, MADERA)
    dx, dy = math.cos(ang), math.sin(ang)
    nx, ny = -dy, dx
    lineas = []
    for off in (-0.3, -0.08, 0.17, 0.36):
        x1, y1 = vista.P(origen[0] - 30 * dx + off * nx, origen[1] - 30 * dy + off * ny)
        x2, y2 = vista.P(origen[0] + 30 * dx + off * nx, origen[1] + 30 * dy + off * ny)
        lineas.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{VETA}" stroke-width="1.2"/>'
        )
    lz.partes.append(f'<g clip-path="url(#{cid})">' + "".join(lineas) + "</g>")
    poligono(lz, pts, "none", MADERA_BORDE, 2)


def ejes(vista, e=0.0, color=None, grosor=1.6):
    color = color or C["ink"]
    vista.linea((-4.9, 0), (6.1, 0), color, grosor, "7 5", 0.85)
    vista.linea((0, -1.0), (0, 6.7), color, grosor, "7 5", 0.85)
    dx, dy = math.cos(ANG_DIAG), math.sin(ANG_DIAG)
    vista.linea((e - 1.2 * dx, -1.2 * dy), (e + 8.0 * dx, 8.0 * dy), color, grosor, "7 5", 0.85)


def punto_nodo(vista, u=0.0, v=0.0, color=None, r=5.5):
    vista.lz.circulo(*vista.P(u, v), r, color or C["ink"], "#ffffff", 2)


def alfiler(vista, u, v):
    x, y = vista.P(u, v)
    vista.lz.circulo(x, y, 4.5, "#e53935", "#b71c1c", 1.2)
    vista.lz.circulo(x - 1.4, y - 1.4, 1.3, "#ffcdd2")


def escena(vista, tipo="tope", e=0.0, ejes_on=False, ejes_encima=False, pegante_on=False,
           cartela_on=False, con_barras=True, con_diag=True, desplazar=0.0, pines=False,
           punto=False):
    lz = vista.lz
    cuerda, montante, diag, origen_diag = geometria_nodo(tipo, e, desplazar)
    if ejes_on and not ejes_encima:
        ejes(vista, e, "#8a8f94", 1.4)
    if con_barras:
        barra(vista, cuerda, (0, 0), 0)
        barra(vista, montante, (0, 0), math.pi / 2, sombra=(tipo == "traslape"))
        if con_diag:
            barra(vista, diag, origen_diag, ANG_DIAG, sombra=(tipo == "traslape"))
    if pegante_on:
        vista.linea((-0.5, 0.5), (0.5, 0.5), PEGANTE, 5, opacidad=0.9)
        for p, q in bordes_pegados(diag):
            vista.linea(p, q, PEGANTE, 5, opacidad=0.9)
    if cartela_on:
        pts = [vista.P(u, v) for u, v in cartela_nodo()]
        poligono(lz, pts, C["badge"], C["badge"], 2.2, op_relleno=0.2)
    if pines:
        for u, v in ((-3.3, 1.05), (3.9, 1.05), (-3.3, -1.05), (-1.05, 5.0), (1.05, 3.0)):
            alfiler(vista, u, v)
    if ejes_on and ejes_encima:
        ejes(vista, e)
    if punto:
        punto_nodo(vista)


def papel(lz, x, y, w, h, paso=14):
    lz.rect(x, y, w, h, PAPEL, C["border"], 1.2, radio=6)
    gx = x + paso
    while gx < x + w - 2:
        lz.linea(gx, y + 1, gx, y + h - 1, REJILLA, 1)
        gx += paso
    gy = y + paso
    while gy < y + h - 2:
        lz.linea(x + 1, gy, x + w - 1, gy, REJILLA, 1)
        gy += paso


def pildora(lz, x, y, texto, fondo, color="#ffffff", tam=15):
    w = len(texto) * tam * 0.56 + 26
    lz.rect(x, y, w, 30, fondo, radio=15)
    lz.texto(x + w / 2, y + 20.5, texto, tam, color, "700", "middle")
    return w


def vinetas(lz, x, y, items, ancho, tam=15, paso=21, color=None):
    for item in items:
        lz.circulo(x + 4, y - 5, 4, color or C["badge"])
        for ln in envolver(item, ancho):
            lz.texto(x + 16, y, ln, tam, C["ink"])
            y += paso
        y += 9
    return y


def texto_lineas(lz, x, y, lineas, tam, color, peso="400", ancla="start", paso=None):
    paso = paso or tam + 4
    for ln in lineas:
        lz.texto(x, y, ln, tam, color, peso, ancla)
        y += paso
    return y


def marca_fuerza(lz, x, y, r=8):
    lz.circulo(x, y, r, "#ffffff", C["ink"], 1.8)
    lz.circulo(x, y, 2.6, C["ink"])


# ---------------------------------------------------------------------------
# Bloques de la lámina
# ---------------------------------------------------------------------------


def bloque_tipos(lz, y0):
    w, h, k = 493, 490, 29
    tarjetas = [
        ("A tope (como en tus fotos)", "Sirve si el corte queda justo", AMBAR, "#3e2723", "tope", [
            "Los ejes se cruzan en el nodo.",
            "La cola agarra solo en la punta de las fibras, que pega poco.",
            "Una barra a tensión se puede despegar antes de que falle la barra crítica.",
        ]),
        ("Traslapada", "Evítala", C["comp"], "#ffffff", "traslape", [
            "La diagonal queda en otro plano que la cuerda.",
            "Las fuerzas no pasan por el centro de las barras: la unión se tuerce.",
            "Las barras se pandean antes de lo que calculaste.",
        ]),
        ("A tope con cartelas", "Recomendada", C["badge"], "#ffffff", "cartela", [
            "Los ejes se cruzan en el nodo.",
            "La cartela pega sobre la cara de las fibras: unas 6 veces más área.",
            "Va igual por los dos lados, así que la unión no se tuerce.",
        ]),
    ]
    for i, (titulo, et, fondo, color_et, tipo, items) in enumerate(tarjetas):
        x0 = 40 + i * (w + 20)
        lz.tarjeta(x0, y0, w, h, titulo)
        pildora(lz, x0 + 22, y0 + 52, et, fondo, color_et)
        vista = Vista(lz, x0 + 160, y0 + 300, k)
        if tipo == "traslape":
            escena(vista, "traslape")
            xt, yt = vista.P(-4.5, 5.6)
            texto_lineas(lz, xt, yt, ["Diagonal y", "montante", "encima de", "la cuerda"], 14,
                         C["comp"], "700")
            vista.linea((-2.6, 2.9), (-0.3, 0.15), C["comp"], 1.6)
            punto_nodo(vista, -0.3, 0.15, C["comp"], 3.5)
            # Inset: visto de canto
            cx = x0 + 412
            lz.texto(cx, y0 + 108, "Visto de canto", 14, C["muted"], "700", "middle")
            lado = 34
            xa, ya = cx - lado, y0 + 150
            lz.rect(xa, ya, lado, lado, MADERA, MADERA_BORDE, 2)
            lz.rect(xa + lado, ya - 10, lado, lado, MADERA, MADERA_BORDE, 2)
            marca_fuerza(lz, xa + lado / 2, ya + lado / 2)
            marca_fuerza(lz, xa + 1.5 * lado, ya - 10 + lado / 2)
            lz.texto(xa + lado / 2, ya + lado + 18, "cuerda", 12, C["muted"], "600", "middle")
            lz.texto(xa + 1.5 * lado, ya - 17, "diagonal", 12, C["muted"], "600", "middle")
            yd = ya + lado + 34
            lz.linea(xa + lado / 2, yd, xa + 1.5 * lado, yd, C["comp"], 1.6)
            for xx in (xa + lado / 2, xa + 1.5 * lado):
                lz.linea(xx, yd - 5, xx, yd + 5, C["comp"], 1.6)
            lz.texto(cx, yd + 18, "e", 15, C["comp"], "700", "middle")
            texto_lineas(lz, cx, yd + 42, ["Las fuerzas no", "están en línea:", "la unión se tuerce."],
                         13, C["comp"], "600", "middle", 17)
        elif tipo == "tope":
            escena(vista, "tope", pegante_on=True)
            xt, yt = vista.P(-4.5, 5.6)
            texto_lineas(lz, xt, yt, ["Pegante solo", "en la punta", "de las fibras"], 14,
                         PEGANTE, "700")
            vista.linea((-2.0, 3.6), (-0.45, 0.62), PEGANTE, 1.6)
        else:
            escena(vista, "tope", cartela_on=True)
            xt, yt = vista.P(-4.5, 5.6)
            texto_lineas(lz, xt, yt, ["Cartela", "adelante", "y atrás"], 14, C["badge"], "700")
            vista.linea((-3.2, 4.2), (-2.0, 2.0), C["badge"], 1.6)
        vinetas(lz, x0 + 26, y0 + 355, items, 50)


def bloque_ejes(lz, y0):
    x0, w, h, k = 40, 620, 430, 22
    lz.tarjeta(x0, y0, w, h, "Los ejes se cruzan en el nodo")
    e = 2.6
    escenas = [
        (171, "Bien", C["badge"], 0.0,
         "Los 3 ejes se cruzan en un solo punto. Así trabaja el método de nodos."),
        (440, "Mal", C["comp"], e,
         "La diagonal llega a una distancia e del nodo. La cuerda se dobla y tu cálculo ya no coincide."),
    ]
    for cx, et, col, ee, texto in escenas:
        vista = Vista(lz, cx, y0 + 270, k)
        pildora(lz, cx - 4.6 * k, y0 + 56, et, col)
        escena(vista, "tope", e=ee, ejes_on=True, ejes_encima=True)
        punto_nodo(vista)
        if ee:
            punto_nodo(vista, ee, 0, C["comp"])
            yv = -1.3
            vista.linea((0, yv), (ee, yv), C["comp"], 1.8)
            for uu in (0, ee):
                vista.linea((uu, yv - 0.25), (uu, yv + 0.25), C["comp"], 1.8)
            xe, ye = vista.P(ee / 2, yv - 0.85)
            lz.texto(xe, ye, "e", 16, C["comp"], "700", "middle")
        texto_lineas(lz, cx - 4.6 * k, y0 + 345, envolver(texto, 34), 14, C["ink"], paso=19)
    lz.texto(x0 + 22, y0 + 412, "Una e de hasta medio ancho de barra (2 a 3 mm) es aceptable.", 14,
             C["muted"], "700")


def bloque_cartela(lz, y0):
    x0, w, h, k = 680, 880, 430, 26
    lz.tarjeta(x0, y0, w, h, "La cartela")
    vista = Vista(lz, 830, y0 + 290, k)
    escena(vista, "tope", cartela_on=True)
    # Cota del traslapo sobre la cuerda
    yv = -1.4
    vista.linea((0.5, -0.5), (0.5, yv - 0.3), C["muted"], 1)
    vista.linea((3.5, -0.5), (3.5, yv - 0.3), C["muted"], 1)
    vista.linea((0.5, yv), (3.5, yv), C["muted"], 1.4)
    for uu in (0.5, 3.5):
        vista.linea((uu - 0.15, yv - 0.15), (uu + 0.15, yv + 0.15), C["muted"], 1.8)
    xt, yt = vista.P(2.0, yv - 0.85)
    lz.texto(xt, yt, "1.5 cm", 14, C["muted"], "700", "middle")
    xt, yt = vista.P(-4.5, 5.6)
    texto_lineas(lz, xt, yt, ["Igual en", "cada barra"], 14, C["badge"], "700")

    # Visto de canto
    cx = 1095
    lz.texto(cx, y0 + 72, "Visto de canto", 14, C["muted"], "700", "middle")
    lado, t = 34, 7
    yb = y0 + 250
    lz.rect(cx - lado / 2, y0 + 100, lado, yb - lado - (y0 + 100), "#f6ead3", MADERA_BORDE, 1.5)
    lz.rect(cx - lado / 2, yb - lado, lado, lado, MADERA, MADERA_BORDE, 2)
    for xx in (cx - lado / 2 - t, cx + lado / 2):
        lz.rect(xx, y0 + 112, t, yb - (y0 + 112), "#d7ecd9", C["badge"], 1.8)
    marca_fuerza(lz, cx, yb - lado / 2)
    lz.texto(cx - lado / 2 - t - 8, y0 + 128, "cartela", 13, C["badge"], "700", "end")
    lz.texto(cx - lado / 2 - t - 8, y0 + 145, "1 a 1.5 mm", 12, C["muted"], "600", "end")
    lz.texto(cx + lado / 2 + t + 8, y0 + 128, "cartela", 13, C["badge"], "700")
    lz.texto(cx + lado / 2 + t + 8, y0 + 145, "1 a 1.5 mm", 12, C["muted"], "600")
    lz.texto(cx, yb + 20, "barra", 13, C["muted"], "700", "middle")
    texto_lineas(lz, cx, yb + 50, envolver("Las dos cartelas son iguales: la fuerza pasa por el "
                                           "centro y la unión no se tuerce.", 24),
                 13, C["ink"], "400", "middle", 18)

    vinetas(lz, 1225, y0 + 82, [
        "Monta unos 1.5 cm sobre cada barra, unas 3 veces su ancho.",
        "Hazla de balsa de 1 a 1.5 mm o de cartulina.",
        "Si es de balsa, pon la veta a lo largo de la barra más cargada.",
        "Pon una igual por cada lado de la cara.",
        "Cola blanca en capa delgada. Aprieta un minuto y deja secar.",
    ], 36)


def bloque_pasos(lz, y0):
    lz.tarjeta(40, y0, 1520, 345, "Paso a paso de cada nodo")
    pasos = [
        ("Ejes en el plano", dict(con_barras=False, ejes_on=True, ejes_encima=True, punto=True),
         "Dibuja en el plano 1:1 el eje de cada barra y marca el nodo. Pon plástico encima."),
        ("Cuerda y montante", dict(con_diag=False, ejes_on=True, pines=True),
         "Pega la cuerda y el montante sobre sus ejes. Sujeta con alfileres fuera de la unión."),
        ("Ajusta la diagonal", dict(ejes_on=True, desplazar=1.0),
         "Presenta la diagonal sobre el plano y lija la punta hasta que asiente sin dejar luz."),
        ("Pega la diagonal", dict(pegante_on=True),
         "Cola en la punta, espera 5 minutos, pon otra capa y pega. Limpia el exceso."),
        ("Cartelas (2 por nodo)", dict(cartela_on=True),
         "Pega la cartela de adelante. Cuando seque, voltea la cara y pega la de atrás."),
    ]
    for i, (titulo, opciones, texto) in enumerate(pasos):
        px = 60 + i * 296
        lz.circulo(px + 14, y0 + 66, 13, C["badge"])
        lz.texto(px + 14, y0 + 71.5, str(i + 1), 15, "#ffffff", "700", "middle")
        lz.texto(px + 36, y0 + 72, titulo, 16, C["ink"], "700")
        papel(lz, px, y0 + 86, 280, 180)
        vista = Vista(lz, px + 120, y0 + 244, 23)
        escena(vista, **opciones)
        if i == 0:
            xt, yt = vista.P(0.45, -0.9)
            lz.texto(xt, yt, "nodo", 13, C["ink"], "700")
        if i == 2:
            nx, ny = math.sin(ANG_DIAG), -math.cos(ANG_DIAG)
            dx, dy = math.cos(ANG_DIAG), math.sin(ANG_DIAG)
            a = vista.P(5.0 * dx + 1.25 * nx, 5.0 * dy + 1.25 * ny)
            b = vista.P(2.6 * dx + 1.25 * nx, 2.6 * dy + 1.25 * ny)
            lz.flecha(*a, *b, C["ink"], 2.2, 10)
        texto_lineas(lz, px, y0 + 292, envolver(texto, 36), 14, C["ink"], paso=19)


def cara_cartelas(lz, op, res, ox, oy, s):
    nodos = op["nodos"]

    def P(x, y):
        return ox + x * s, oy - y * s

    tension = set()
    for (a, b, t), f in zip(op["barras"], res["fuerzas"]):
        if f > 1e-9 and t != "inf":
            tension.update((a, b))
    necesarios = set(op["apoyos"]) | tension

    for (a, b, _), f in zip(op["barras"], res["fuerzas"]):
        if abs(f) < 1e-9:
            lz.linea(*P(*nodos[a]), *P(*nodos[b]), C["zero"], 3, guiones="6 5")
        else:
            lz.linea(*P(*nodos[a]), *P(*nodos[b]), color_fuerza(f), 5.5, extremo="butt")

    for n, (x, y) in nodos.items():
        pts = []
        for a, b, _ in op["barras"]:
            if n in (a, b):
                otro = b if a == n else a
                ang = math.atan2(nodos[otro][1] - y, nodos[otro][0] - x)
                pts += tira((x, y), ang, 0, R_CARTELA_CM, ANCHO_BARRA_CM)
        col = C["badge"] if n in necesarios else GRIS_CARTELA
        poligono(lz, [P(u, v) for u, v in casco(pts)], col, col, 1.6, op_relleno=0.3)

    izq, der = op["apoyos"]
    for n in (izq, der):
        x, y = P(*nodos[n])
        base = y + 19
        poligono(lz, [(x, y + 5), (x - 9, base), (x + 9, base)], "#eceff1", C["ink"], 1.5)
        if n == der:
            lz.circulo(x - 4.5, base + 3.5, 3, "#ffffff", C["ink"], 1.2)
            lz.circulo(x + 4.5, base + 3.5, 3, "#ffffff", C["ink"], 1.2)
            base += 7
        lz.linea(x - 14, base + 1, x + 14, base + 1, C["ink"], 1.5)

    for n, (nx, ny) in nodos.items():
        x, y = P(nx, ny)
        lz.circulo(x, y, 3, "#ffffff", C["ink"], 1.5)
        if ny == 0:
            if n == izq:
                lz.texto(x - 14, y + 16, n, 13, C["ink"], "700", "end")
            elif n == der:
                lz.texto(x + 14, y + 16, n, 13, C["ink"], "700")
            else:
                lz.texto(x, y + 24, n, 13, C["ink"], "700", "middle")
        elif ny == 20:
            lz.texto(x - 9, y - 9, n, 13, C["ink"], "700", "end")
        elif nx < 20:
            lz.texto(x - 13, y + 5, n, 13, C["ink"], "700", "end")
        else:
            lz.texto(x + 13, y + 5, n, 13, C["ink"], "700")
    return len(nodos), len(necesarios)


def bloque_donde(lz, y0):
    lz.tarjeta(40, y0, 1520, 420, "Dónde van las cartelas en tus opciones")
    opciones = _opciones()[:2]
    s = 11
    for op, ox in zip(opciones, (100, 610)):
        res = analizar(op)
        lz.texto(ox + 20 * s, y0 + 78, f"Opción {op['num']} · {op['corto']}", 17, C["ink"], "700",
                 "middle")
        n, n_nec = cara_cartelas(lz, op, res, ox, y0 + 335, s)
        lz.texto(ox + 20 * s, y0 + 386, f"Todas: {4 * n} cartelas ({n} nodos × 2 lados × 2 caras)",
                 14, C["ink"], "600", "middle")
        lz.texto(ox + 20 * s, y0 + 405, f"Solo las necesarias: {4 * n_nec} cartelas", 14,
                 C["badge"], "700", "middle")

    x = 1100
    y = y0 + 92
    for col, titulo, texto in (
        (C["badge"], "Necesaria",
         "En los apoyos y en los nodos donde llega una barra a tensión (azul). Ahí la cartela "
         "es la que aguanta la fuerza."),
        (GRIS_CARTELA, "Recomendada",
         "En los demás nodos. La fuerza pasa por contacto, pero la cartela mantiene los ejes "
         "en su sitio."),
    ):
        poligono(lz, [(x, y - 15), (x + 28, y - 15), (x + 28, y + 3), (x, y + 3)], col, col, 1.6,
                 op_relleno=0.3)
        lz.texto(x + 40, y, titulo, 16, C["ink"], "700")
        y = texto_lineas(lz, x, y + 24, envolver(texto, 50), 14, C["ink"], paso=19) + 16
    leyenda_linea(lz, x, y + 6, C["comp"], "Compresión", grosor=5, tam=14, largo=26)
    leyenda_linea(lz, x + 140, y + 6, C["tens"], "Tensión", grosor=5, tam=14, largo=26)
    leyenda_linea(lz, x + 255, y + 6, C["zero"], "Cero", guiones="6 5", grosor=3, tam=14, largo=26)
    texto_lineas(lz, x, y + 44, envolver("Las transversales se pegan en el mismo nodo, sobre la "
                                         "cartela de adentro.", 50), 14, C["muted"], "600", paso=19)


def main():
    W, H = 1600, 2075
    lz = Lienzo(W, H)
    encabezado(
        lz, "Cómo pegar las uniones de tu cercha",
        "Une las barras a tope, como en tus fotos, pero con los ejes cruzándose en el nodo y con "
        "una cartela por cada lado.",
    )
    bloque_tipos(lz, 130)
    bloque_ejes(lz, 640)
    bloque_cartela(lz, 640)
    bloque_pasos(lz, 1090)
    bloque_donde(lz, 1455)

    y = 1895
    lz.rect(40, y, 1520, 112, "#e8f5e9", "#a5d6a7", 1.5, radio=14)
    lz.rect(40, y, 10, 112, C["badge"], radio=4)
    lz.texto(70, y + 36, "Para que tu cálculo coincida con el ensayo", 18, C["badge"], "700")
    lz.texto(70, y + 66, "Con estas uniones se cumplen los supuestos del método de nodos: los ejes se "
             "cruzan en el nodo y cada barra trabaja solo a lo largo de su eje.", 16, C["ink"])
    lz.texto(70, y + 92, "Así la falla debería empezar por pandeo en la barra crítica y no en una unión. "
             "Prueba antes 3 uniones sueltas y deja secar la cercha 24 horas.", 16, C["ink"])
    lz.texto(40, 2040, "Medidas para barras de 5 × 5 mm. Si tus barras son de otra sección, haz que la "
             "cartela monte unas 3 veces el ancho de la barra.", 14, C["muted"])
    lz.texto(40, 2061, "Fuerzas de las opciones 1 y 2 calculadas por el método de nodos con la carga "
             "repartida entre los nodos de arriba.", 14, C["muted"])
    lz.guardar(os.path.join(CARPETA, "05_como_pegar_las_uniones.svg"))


if __name__ == "__main__":
    main()
