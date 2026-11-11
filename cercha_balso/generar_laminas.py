#!/usr/bin/env python3
"""Genera las láminas SVG de las opciones de cercha de balso.

Calcula la fuerza de cada barra por el método de nodos (ΣFx = 0 y ΣFy = 0
en cada nodo, resuelto como un sistema de ecuaciones) y dibuja:
  - una lámina por opción: vista frontal con fuerzas, vista 3D con las
    barras de soporte, tabla de fuerzas, lista de corte y notas
  - una lámina comparativa de las tres opciones

Uso:
    python3 generar_laminas.py        # separación entre caras b = 10 cm
    python3 generar_laminas.py 12     # separación entre caras b = 12 cm

Convención: P es la carga que recibe UNA cara (la mitad de la carga de la
máquina), repartida por igual entre los nodos de arriba. Fuerza positiva =
tensión, negativa = compresión.

Conteo de barras: la cuerda inferior de cada cara es UNA sola barra de 40 cm
(se calcula por tramos entre nodos, pero se cuenta y se corta como una pieza).
Las demás barras cuentan una por tramo entre nodos, más una transversal por
nodo y las diagonales de soporte.
"""

import math
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

B = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
CARPETA = os.path.dirname(os.path.abspath(__file__))

FONT = "Noto Sans, DejaVu Sans, Arial, sans-serif"
C = {
    "bg": "#f3efe6",
    "card": "#ffffff",
    "border": "#e2d9c6",
    "ink": "#263238",
    "muted": "#5f6b73",
    "comp": "#c62828",
    "tens": "#1565c0",
    "zero": "#9e9e9e",
    "crit": "#ffd54f",
    "trans": "#2e7d32",
    "sup": "#ef6c00",
    "portal": "#7b1fa2",
    "inf": "#00838f",
    "wood": "#d9b98a",
    "wood_dark": "#8d6e3f",
    "badge": "#2e7d32",
}

TIPOS = {
    "inf": "Cuerda inferior",
    "sup": "Cuerda superior",
    "incl": "Inclinadas de los extremos",
    "mont": "Montantes",
    "diag": "Diagonales",
    "riostra": "Riostras de las inclinadas",
}

# ---------------------------------------------------------------------------
# Definición de las opciones (una cara, medidas en cm)
# ---------------------------------------------------------------------------


def _opciones():
    # Opción 1: Warren en W, 3 nodos arriba, inclinadas partidas en M y N
    n1 = {
        "A": (0, 0), "B": (15, 0), "C": (25, 0), "D": (40, 0),
        "E": (5, 20), "F": (20, 20), "G": (35, 20),
        "M": (2.5, 10), "N": (37.5, 10),
    }
    b1 = [
        ("A", "B", "inf"), ("B", "C", "inf"), ("C", "D", "inf"),
        ("E", "F", "sup"), ("F", "G", "sup"),
        ("E", "B", "diag"), ("B", "F", "diag"), ("F", "C", "diag"), ("C", "G", "diag"),
        ("A", "M", "incl"), ("M", "E", "incl"), ("D", "N", "incl"), ("N", "G", "incl"),
        ("M", "B", "riostra"), ("N", "C", "riostra"),
    ]

    # Opción 2: Pratt de 4 paneles, inclinadas partidas en M y N
    n2 = {
        "A": (0, 0), "B": (10, 0), "C": (20, 0), "D": (30, 0), "E": (40, 0),
        "F": (10, 20), "G": (20, 20), "H": (30, 20),
        "M": (5, 10), "N": (35, 10),
    }
    b2 = [
        ("A", "B", "inf"), ("B", "C", "inf"), ("C", "D", "inf"), ("D", "E", "inf"),
        ("F", "G", "sup"), ("G", "H", "sup"),
        ("B", "F", "mont"), ("C", "G", "mont"), ("D", "H", "mont"),
        ("F", "C", "diag"), ("H", "C", "diag"),
        ("A", "M", "incl"), ("M", "F", "incl"), ("E", "N", "incl"), ("N", "H", "incl"),
        ("M", "B", "riostra"), ("N", "D", "riostra"),
    ]

    # Opción 3: Warren de 4 nodos arriba, inclinadas partidas en M y N
    n3 = {
        "A": (0, 0), "B": (10, 0), "C": (20, 0), "D": (30, 0), "E": (40, 0),
        "F": (5, 20), "G": (15, 20), "H": (25, 20), "I": (35, 20),
        "M": (2.5, 10), "N": (37.5, 10),
    }
    b3 = [
        ("A", "B", "inf"), ("B", "C", "inf"), ("C", "D", "inf"), ("D", "E", "inf"),
        ("F", "G", "sup"), ("G", "H", "sup"), ("H", "I", "sup"),
        ("F", "B", "diag"), ("B", "G", "diag"), ("G", "C", "diag"),
        ("C", "H", "diag"), ("H", "D", "diag"), ("D", "I", "diag"),
        ("A", "M", "incl"), ("M", "F", "incl"), ("E", "N", "incl"), ("N", "I", "incl"),
        ("M", "B", "riostra"), ("N", "D", "riostra"),
    ]

    return [
        dict(
            num=1,
            archivo="01_opcion1_warren_w_41barras",
            titulo="Opción 1 · Warren en W con inclinadas arriostradas",
            corto="Warren en W",
            nodos=n1, barras=b1, arriba=["E", "F", "G"], apoyos=("A", "D"),
            # Diagonales de soporte: (nodo de la cara delantera, nodo de la cara trasera)
            sup=[("E", "F"), ("G", "F")],
            portal=[("A", "M"), ("M", "E"), ("D", "N"), ("N", "G")],
            inf=[],
            notas=[
                "La cuerda inferior A–D es una sola barra de 40 cm. Marca en ella "
                "los nodos B (a 15 cm) y C (a 25 cm).",
                "B–F y F–C se reparten la carga del centro y son las críticas. "
                "Usa ahí tus palitos más rectos y densos.",
                "M–B y N–C tienen fuerza cero, pero parten cada inclinada en dos "
                "tramos de 10.3 cm.",
            ],
            pros="La más resistente y con menos barras.",
            contras="Paneles de arriba de 15 cm: se doblan más si el cabezal "
                    "apoya entre nodos.",
        ),
        dict(
            num=2,
            archivo="02_opcion2_pratt_arriostrada_44barras",
            titulo="Opción 2 · Pratt con inclinadas arriostradas",
            corto="Pratt arriostrada",
            nodos=n2, barras=b2, arriba=["F", "G", "H"], apoyos=("A", "E"),
            sup=[("F", "G"), ("H", "G")],
            portal=[("A", "M"), ("M", "F"), ("E", "N"), ("N", "H")],
            inf=[],
            notas=[
                "La cuerda inferior A–E es una sola barra de 40 cm, con nodos "
                "cada 10 cm.",
                "M–B y N–D tienen fuerza cero, pero parten cada inclinada en dos "
                "tramos de 11.2 cm.",
                "B–F y D–H tienen fuerza cero, pero sostienen la cuerda inferior. "
                "No las quites.",
            ],
            pros="Las diagonales largas trabajan a tensión.",
            contras="Todo el centro descansa en un solo montante, C–G.",
        ),
        dict(
            num=3,
            archivo="03_opcion3_warren_arriostrada_50barras",
            titulo="Opción 3 · Warren de 4 nodos con inclinadas arriostradas",
            corto="Warren de 4 nodos",
            nodos=n3, barras=b3, arriba=["F", "G", "H", "I"], apoyos=("A", "E"),
            sup=[("F", "G"), ("G", "H"), ("I", "H")],
            portal=[("A", "M"), ("M", "F"), ("E", "N"), ("N", "I")],
            inf=[],
            notas=[
                "La cuerda inferior A–E es una sola barra de 40 cm, con nodos "
                "cada 10 cm.",
                "M–B y N–D parten cada inclinada en dos tramos de 10.3 cm.",
                "B–G y D–H son las críticas. G–C y C–H tienen fuerza cero con "
                "carga simétrica.",
                "No hay nodo arriba en el centro. Si el cabezal es angosto, "
                "apoya en la mitad de G–H y la dobla.",
            ],
            pros="Paneles de arriba más cortos (10 cm).",
            contras="Usa 50 barras y no tiene nodo arriba en el centro.",
        ),
    ]


# ---------------------------------------------------------------------------
# Método de nodos
# ---------------------------------------------------------------------------


def _gauss(a, b):
    n = len(b)
    m = [fila[:] + [b[i]] for i, fila in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            raise ValueError("La cercha no se puede resolver (es un mecanismo).")
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r != col:
                k = m[r][col] / m[col][col]
                for c in range(col, n + 1):
                    m[r][c] -= k * m[col][c]
    return [m[i][n] / m[i][i] for i in range(n)]


def resolver_nodos(nodos, barras, cargas, apoyos):
    """Plantea ΣFx = 0 y ΣFy = 0 en cada nodo y resuelve todas las barras.

    Cada barra se supone a tensión (su fuerza sale del nodo), así que un
    resultado negativo significa compresión.
    """
    nombres = list(nodos)
    idx = {n: i for i, n in enumerate(nombres)}
    n_inc = len(barras) + len(apoyos)
    if n_inc != 2 * len(nombres):
        raise ValueError("La cercha no es isostática (m + r != 2j).")
    a = [[0.0] * n_inc for _ in range(2 * len(nombres))]
    rhs = [0.0] * (2 * len(nombres))
    for k, (n1, n2) in enumerate(barras):
        (x1, y1), (x2, y2) = nodos[n1], nodos[n2]
        largo = math.hypot(x2 - x1, y2 - y1)
        cx, cy = (x2 - x1) / largo, (y2 - y1) / largo
        a[2 * idx[n1]][k] += cx
        a[2 * idx[n1] + 1][k] += cy
        a[2 * idx[n2]][k] -= cx
        a[2 * idx[n2] + 1][k] -= cy
    for r, (n, d) in enumerate(apoyos):
        a[2 * idx[n] + (0 if d == "x" else 1)][len(barras) + r] = 1.0
    for n, (fx, fy) in cargas.items():
        rhs[2 * idx[n]] -= fx
        rhs[2 * idx[n] + 1] -= fy
    sol = _gauss(a, rhs)
    # Comprobación: el residuo de cada ecuación debe ser cero
    for i, fila in enumerate(a):
        residuo = sum(c * s for c, s in zip(fila, sol)) - rhs[i]
        assert abs(residuo) < 1e-9, "El equilibrio de nodos no cierra."
    return sol[: len(barras)], sol[len(barras):]


def _caso_carga(op, cargas):
    nodos, barras = op["nodos"], op["barras"]
    izq, der = op["apoyos"]
    fuerzas, reacciones = resolver_nodos(
        nodos, [(a, b) for a, b, _ in barras], cargas, [(izq, "x"), (izq, "y"), (der, "y")]
    )
    largos = [dist(nodos[a], nodos[b]) for a, b, _ in barras]
    # Índice de pandeo |F|·L²: con la misma sección y E en todas las barras,
    # la barra comprimida con el mayor índice es la que se pandea primero.
    indices = [(-f) * L * L if f < -1e-9 else 0.0 for f, L in zip(fuerzas, largos)]
    imax = max(indices)
    criticas = [k for k, v in enumerate(indices) if v > 0.99 * imax]
    return fuerzas, reacciones, largos, imax, criticas


def analizar(op):
    nodos, barras = op["nodos"], op["barras"]
    m, j = len(barras), len(nodos)
    assert m == 2 * j - 3, f"Opción {op['num']}: m = {m}, 2j - 3 = {2 * j - 3}"
    q = -1.0 / len(op["arriba"])
    fuerzas, reacciones, largos, imax, criticas = _caso_carga(
        op, {n: (0.0, q) for n in op["arriba"]}
    )

    # Caso de cabezal angosto: toda la carga P en el nodo de arriba del centro
    centro = None
    nodo_c = [n for n in op["arriba"] if abs(nodos[n][0] - 20) < 1e-9]
    if nodo_c:
        fc, _, _, _, crit_c = _caso_carga(op, {nodo_c[0]: (0.0, -1.0)})
        centro = dict(nodo=nodo_c[0], criticas=crit_c, fuerza=fc[crit_c[0]])

    # La cuerda inferior se calcula por tramos, pero es una sola barra por cara
    tramos_inf = sum(1 for _, _, t in barras if t == "inf")
    por_cara = m - tramos_inf + 1
    total = 2 * por_cara + j + len(op["sup"]) + len(op["portal"]) + len(op["inf"])
    return dict(
        fuerzas=fuerzas, reacciones=reacciones, largos=largos, indice=imax,
        criticas=criticas, m=m, j=j, por_cara=por_cara, total=total, carga=q,
        centro=centro,
    )


def nota_cabezal(op, res):
    c = res["centro"]
    if c is None:
        return None
    nombres = [nombre_barra(*op["barras"][k][:2]) for k in c["criticas"]]
    if len(nombres) == 1:
        sujeto = f"la barra crítica es {nombres[0]}"
    else:
        sujeto = f"las barras críticas son {' y '.join(nombres)}"
    return (f"Si el cabezal es angosto y solo toca {c['nodo']}, {sujeto} "
            f"({fmt_fuerza(c['fuerza'])}).")


def dist(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def largo_soporte(op, n_del, n_tras):
    (x1, y1), (x2, y2) = op["nodos"][n_del], op["nodos"][n_tras]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + B**2)


# ---------------------------------------------------------------------------
# Utilidades de formato y dibujo
# ---------------------------------------------------------------------------


def redondear(v, dec="0.01"):
    return Decimal(str(round(v, 9))).quantize(Decimal(dec), rounding=ROUND_HALF_UP)


def fmt_fuerza(f):
    if abs(f) < 1e-9:
        return "0"
    return ("−" if f < 0 else "+") + f"{redondear(abs(f))}P"


def fmt_cm(v):
    return f"{redondear(v, '0.1')} cm"


def fmt_b():
    return f"{redondear(B, '0.1')}".rstrip("0").rstrip(".")


def color_fuerza(f):
    if abs(f) < 1e-9:
        return C["zero"]
    return C["comp"] if f < 0 else C["tens"]


def trabajo(f):
    if abs(f) < 1e-9:
        return "Cero"
    return "Compresión" if f < 0 else "Tensión"


def nombre_barra(a, b):
    return f"{a}–{b}"


def envolver(texto, max_chars):
    lineas, actual = [], ""
    for p in texto.split():
        prueba = (actual + " " + p).strip()
        if len(prueba) > max_chars and actual:
            lineas.append(actual)
            actual = p
        else:
            actual = prueba
    if actual:
        lineas.append(actual)
    return lineas


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Lienzo:
    def __init__(self, ancho, alto):
        self.ancho, self.alto, self.partes = ancho, alto, []

    def linea(self, x1, y1, x2, y2, color, grosor=2.0, guiones=None, opacidad=1.0, extremo="round"):
        d = f' stroke-dasharray="{guiones}"' if guiones else ""
        self.partes.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
            f'stroke-width="{grosor:.1f}" stroke-linecap="{extremo}" opacity="{opacidad}"{d}/>'
        )

    def rect(self, x, y, w, h, relleno, borde="none", grosor=1.0, radio=0, opacidad=1.0):
        self.partes.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{radio}" '
            f'fill="{relleno}" stroke="{borde}" stroke-width="{grosor}" opacity="{opacidad}"/>'
        )

    def circulo(self, cx, cy, r, relleno, borde="none", grosor=1.0):
        self.partes.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{relleno}" '
            f'stroke="{borde}" stroke-width="{grosor}"/>'
        )

    def poligono(self, puntos, relleno, borde="none", grosor=1.0, opacidad=1.0):
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in puntos)
        self.partes.append(
            f'<polygon points="{pts}" fill="{relleno}" stroke="{borde}" '
            f'stroke-width="{grosor}" opacity="{opacidad}" stroke-linejoin="round"/>'
        )

    def texto(self, x, y, t, tam=16, color=None, peso="400", ancla="start", rot=None):
        color = color or C["ink"]
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
        self.partes.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{tam}" fill="{color}" '
            f'font-weight="{peso}" text-anchor="{ancla}"{tr}>{esc(t)}</text>'
        )

    def flecha(self, x1, y1, x2, y2, color, grosor=2.5, punta=11):
        ang = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - punta * math.cos(ang), y2 - punta * math.sin(ang)
        self.linea(x1, y1, bx, by, color, grosor, extremo="butt")
        px, py = -math.sin(ang), math.cos(ang)
        w = punta * 0.5
        self.poligono([(x2, y2), (bx + px * w, by + py * w), (bx - px * w, by - py * w)], color)

    def tarjeta(self, x, y, w, h, titulo=None):
        self.rect(x, y, w, h, C["card"], C["border"], 1.5, radio=14)
        if titulo:
            self.texto(x + 22, y + 36, titulo, 20, C["ink"], "700")

    def guardar(self, ruta):
        cab = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.ancho}" height="{self.alto}" '
            f'viewBox="0 0 {self.ancho} {self.alto}" font-family="{FONT}">\n'
            f'<rect width="{self.ancho}" height="{self.alto}" fill="{C["bg"]}"/>\n'
        )
        with open(ruta, "w", encoding="utf-8") as fh:
            fh.write(cab + "\n".join(self.partes) + "\n</svg>\n")


def etiqueta(lz, x, y, t, color, tam=14):
    w = len(t) * tam * 0.6 + 12
    h = tam + 9
    lz.rect(x - w / 2, y - h / 2, w, h, "#ffffff", color, 1.6, radio=h / 2)
    lz.texto(x, y + tam * 0.36, t, tam, color, "700", "middle")


def leyenda_linea(lz, x, y, color, texto, guiones=None, grosor=6, tam=15, largo=34):
    lz.linea(x, y, x + largo, y, color, grosor, guiones=guiones)
    lz.texto(x + largo + 10, y + 5, texto, tam, C["ink"])


def cota_h(lz, x1, x2, y, texto, tam=14, arriba=True):
    lz.linea(x1, y, x2, y, C["muted"], 1.3)
    for x in (x1, x2):
        lz.linea(x - 4, y + 4, x + 4, y - 4, C["muted"], 1.6)
    lz.texto((x1 + x2) / 2, y - 6 if arriba else y + 18, texto, tam, C["muted"], "600", "middle")


# ---------------------------------------------------------------------------
# Vista frontal
# ---------------------------------------------------------------------------


def dibujar_frontal(lz, op, res, ox, oy, s, compacto=False):
    nodos = op["nodos"]

    def P(n):
        return ox + nodos[n][0] * s, oy - nodos[n][1] * s

    fmax = max(abs(f) for f in res["fuerzas"])
    ytop = oy - 20 * s

    for k in res["criticas"]:
        a, b, _ = op["barras"][k]
        lz.linea(*P(a), *P(b), C["crit"], 18 if compacto else 26, opacidad=0.95)

    for k, (a, b, _) in enumerate(op["barras"]):
        f = res["fuerzas"][k]
        if abs(f) < 1e-9:
            lz.linea(*P(a), *P(b), C["zero"], 2.5 if compacto else 3, guiones="7 6")
        else:
            g = (2.5 + 4.5 * abs(f) / fmax) if compacto else (3 + 7 * abs(f) / fmax)
            lz.linea(*P(a), *P(b), color_fuerza(f), g)

    # Cargas en los nodos de arriba
    n_arriba = len(op["arriba"])
    largo_f = 34 if compacto else 48
    for n in op["arriba"]:
        x, y = P(n)
        lz.flecha(x, y - largo_f - 8, x, y - 8, C["ink"], 2 if compacto else 2.5, 9 if compacto else 11)
        if not compacto:
            lz.texto(x, y - largo_f - 14, f"P/{n_arriba}", 15, C["ink"], "700", "middle")

    # Apoyos
    izq, der = op["apoyos"]
    for n, rodillo in ((izq, False), (der, True)):
        x, y = P(n)
        h = 15 if compacto else 20
        w = 10 if compacto else 13
        base = y + 6 + h
        lz.poligono([(x, y + 6), (x - w, base), (x + w, base)], "#eceff1", C["ink"], 1.8)
        if rodillo:
            r = 3 if compacto else 4
            lz.circulo(x - w / 2, base + r + 1, r, "#ffffff", C["ink"], 1.5)
            lz.circulo(x + w / 2, base + r + 1, r, "#ffffff", C["ink"], 1.5)
            base += 2 * r + 2
        lz.linea(x - w - 6, base + 1, x + w + 6, base + 1, C["ink"], 1.8)
        if not compacto:
            lz.texto(x, base + 20, "R = P/2", 14, C["ink"], "700", "middle")

    # Nodos
    for n in nodos:
        x, y = P(n)
        lz.circulo(x, y, 4 if compacto else 6, "#ffffff", C["ink"], 2)

    # Letras de los nodos
    tam_n = 12 if compacto else 16
    for n, (nx, ny) in nodos.items():
        x, y = P(n)
        if ny == 0:
            if n == izq:
                lz.texto(x - 14, y + 18, n, tam_n, C["ink"], "700", "end")
            elif n == der:
                lz.texto(x + 14, y + 18, n, tam_n, C["ink"], "700", "start")
            else:
                lz.texto(x, y + (18 if compacto else 25), n, tam_n, C["ink"], "700", "middle")
        elif ny == 20:
            lz.texto(x - 10, y - 9, n, tam_n, C["ink"], "700", "end")
        else:
            izquierda = nx < 20
            lz.texto(x + (-12 if izquierda else 12), y + 5, n, tam_n, C["ink"], "700",
                     "end" if izquierda else "start")

    # Etiquetas de fuerza (en compacto solo las críticas, sin que se encimen)
    puestas = []
    for k, (a, b, _) in enumerate(op["barras"]):
        if compacto and k not in res["criticas"]:
            continue
        (x1, y1), (x2, y2) = P(a), P(b)
        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
        if compacto and any(math.hypot(xm - px, ym - py) < 75 for px, py in puestas):
            continue
        puestas.append((xm, ym))
        f = res["fuerzas"][k]
        etiqueta(lz, (x1 + x2) / 2, (y1 + y2) / 2, fmt_fuerza(f), color_fuerza(f), 12 if compacto else 14)

    if compacto:
        lz.texto(ox + 20 * s, oy + 40, "Cuerda inferior: una sola barra", 13, C["tens"], "700", "middle")
        return

    # Cotas
    xs_inf = sorted({nodos[n][0] for n in nodos if nodos[n][1] == 0})
    xs_sup = sorted({nodos[n][0] for n in nodos if nodos[n][1] == 20})
    y_pan, y_tot = oy + 74, oy + 104
    for x in xs_inf:
        X = ox + x * s
        lz.linea(X, oy + 62, X, y_pan + 6, C["muted"], 1)
    for x in (xs_inf[0], xs_inf[-1]):
        X = ox + x * s
        lz.linea(X, y_pan + 6, X, y_tot + 6, C["muted"], 1)
    for x1, x2 in zip(xs_inf, xs_inf[1:]):
        cota_h(lz, ox + x1 * s, ox + x2 * s, y_pan, f"{x2 - x1:g} cm", 13)
    cota_h(lz, ox + xs_inf[0] * s, ox + xs_inf[-1] * s, y_tot,
           f"{xs_inf[-1] - xs_inf[0]:g} cm · cuerda inferior de una sola barra", 15)

    y_sup = ytop - 96
    for x in (xs_sup[0], xs_sup[-1]):
        X = ox + x * s
        lz.linea(X, y_sup - 6, X, y_sup + 12, C["muted"], 1)
    cota_h(lz, ox + xs_sup[0] * s, ox + xs_sup[-1] * s, y_sup, f"{xs_sup[-1] - xs_sup[0]:g} cm", 15)

    xh = ox - 58
    lz.linea(ox - 30, oy, xh - 6, oy, C["muted"], 1, guiones="3 3")
    lz.linea(ox + xs_sup[0] * s - 14, ytop, xh - 6, ytop, C["muted"], 1, guiones="3 3")
    lz.linea(xh, oy, xh, ytop, C["muted"], 1.3)
    for y in (oy, ytop):
        lz.linea(xh - 4, y + 4, xh + 4, y - 4, C["muted"], 1.6)
    lz.texto(xh - 8, (oy + ytop) / 2, "20 cm", 15, C["muted"], "600", "middle", rot=-90)


# ---------------------------------------------------------------------------
# Vista 3D
# ---------------------------------------------------------------------------


def proyectar(x, y, z, th=math.radians(32), ph=math.radians(24)):
    xc = x - 20
    sx = xc * math.cos(th) + z * math.sin(th)
    prof = -xc * math.sin(th) + z * math.cos(th)
    sy = y * math.cos(ph) + prof * math.sin(ph)
    return sx, sy


def dibujar_3d(lz, op, res, caja):
    x0, y0, x1, y1 = caja
    nodos = op["nodos"]
    puntos = []
    for (nx, ny) in nodos.values():
        for z in (0, B):
            puntos.append(proyectar(nx, ny, z))
    puntos += [proyectar(0, -1.5, -2.5), proyectar(40, -1.5, B + 2.5), proyectar(20, 31, B / 2)]
    mnx, mxx = min(p[0] for p in puntos), max(p[0] for p in puntos)
    mny, mxy = min(p[1] for p in puntos), max(p[1] for p in puntos)
    k = min((x1 - x0) / (mxx - mnx), (y1 - y0) / (mxy - mny))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    mx, my = (mnx + mxx) / 2, (mny + mxy) / 2

    def S(x, y, z):
        sx, sy = proyectar(x, y, z)
        return cx + (sx - mx) * k, cy - (sy - my) * k

    def N(n, z):
        return S(*nodos[n], z)

    # Rodillos de apoyo
    for xr in (0, 40):
        lz.linea(*S(xr, -1.2, -2.5), *S(xr, -1.2, B + 2.5), "#b0bec5", 12)
        lz.linea(*S(xr, -1.2, -2.5), *S(xr, -1.2, B + 2.5), "#78909c", 2)

    # Cara trasera
    for a, b, _ in op["barras"]:
        lz.linea(*N(a, B), *N(b, B), C["wood"], 4.5)

    # Barras de soporte
    for n in nodos:
        lz.linea(*N(n, 0), *N(n, B), C["trans"], 3.5)
    for clave in ("inf", "sup", "portal"):
        for a, b in op[clave]:
            lz.linea(*N(a, 0), *N(b, B), C[clave], 3.5)

    # Cara delantera
    for a, b, _ in op["barras"]:
        lz.linea(*N(a, 0), *N(b, 0), C["wood_dark"], 6)

    for n in nodos:
        lz.circulo(*N(n, B), 3, "#ffffff", C["wood"], 1.5)
        lz.circulo(*N(n, 0), 3.5, "#ffffff", C["wood_dark"], 1.8)

    # Carga de la máquina
    xa, ya = S(20, 30, B / 2)
    xb, yb = S(20, 21.2, B / 2)
    lz.flecha(xa, ya, xb, yb, C["ink"], 4, 16)
    lz.texto(xa + 12, ya + 6, "Carga de la máquina = 2P", 16, C["ink"], "700")

    # Rótulos
    xl, yl = N("C", 0)
    lz.texto(xl - 40, yl + 34, "Cara delantera", 15, C["wood_dark"], "700", "middle")
    top = op["arriba"]
    xt, yt = N(top[-1], B)
    lz.texto(xt + 18, yt - 6, "Cara trasera", 15, C["wood_dark"], "700", "start")
    der = op["apoyos"][1]
    xe, ye = N(der, 0)
    xe2, ye2 = N(der, B)
    lz.texto((xe + xe2) / 2 + 16, (ye + ye2) / 2 + 20, f"b = {fmt_b()} cm", 15, C["trans"], "700")
    xr, yr = S(0, -1.2, -2.5)
    lz.texto(xr - 8, yr + 22, "Rodillos de apoyo", 13, C["muted"], "600", "middle")


# ---------------------------------------------------------------------------
# Lámina de cada opción
# ---------------------------------------------------------------------------


def encabezado(lz, titulo, subtitulo, insignia=None):
    lz.texto(40, 62, titulo, 34, C["ink"], "700")
    lz.texto(40, 96, subtitulo, 18, C["muted"])
    if insignia:
        w = 220
        lz.rect(lz.ancho - 40 - w, 30, w, 62, C["badge"], radio=31)
        lz.texto(lz.ancho - 40 - w / 2, 72, insignia, 28, "#ffffff", "700", "middle")


def lamina_opcion(op, res, rel, num_base):
    W, H = 1600, 1244
    lz = Lienzo(W, H)
    encabezado(
        lz, op["titulo"],
        f"Proyecto final de Ingeniería de los Materiales · balso · base 40 cm · alto 20 cm · "
        f"b = {fmt_b()} cm · cuerda inferior de una sola barra",
        f"{res['total']} barras",
    )

    # Vista frontal
    lz.tarjeta(40, 130, 780, 590, "Vista frontal (una cara)")
    lx = 335
    leyenda_linea(lz, lx, 160, C["comp"], "Compresión", largo=26)
    leyenda_linea(lz, lx + 150, 160, C["tens"], "Tensión", largo=26)
    leyenda_linea(lz, lx + 262, 160, C["zero"], "Cero", guiones="6 5", grosor=3, largo=26)
    lz.linea(lx + 350, 160, lx + 376, 160, C["crit"], 14)
    lz.texto(lx + 386, 165, "Crítica", 15, C["ink"])
    dibujar_frontal(lz, op, res, 130, 598, 15)

    # Vista 3D
    lz.tarjeta(850, 130, 710, 590, "Vista 3D: caras y barras de soporte")
    dibujar_3d(lz, op, res, (885, 190, 1525, 585))
    filas = [
        (C["wood_dark"], f"Caras: 2 × {res['por_cara']} = {2 * res['por_cara']}"),
        (C["trans"], f"Transversales (una por nodo): {res['j']}"),
        (C["sup"], f"Diagonales superiores: {len(op['sup'])}"),
        (C["portal"], f"Diagonales de portal: {len(op['portal'])}"),
    ]
    if op["inf"]:
        filas.append((C["inf"], f"Diagonales inferiores: {len(op['inf'])}"))
    for i, (col, t) in enumerate(filas):
        fx = 875 + (i % 2) * 345
        fy = 628 + (i // 2) * 28
        leyenda_linea(lz, fx, fy, col, t, grosor=5, tam=15, largo=28)
    lz.texto(1535, 628 + 2 * 28 + 5, f"Total: {res['total']} barras", 17, C["ink"], "700", "end")

    # Tabla de fuerzas
    lz.tarjeta(40, 745, 670, 425, "Fuerza en cada barra (una cara)")
    barras = op["barras"]
    mitad = (len(barras) + 1) // 2
    paso_t = 33 if mitad <= 9 else 29
    for g, grupo in enumerate((range(0, mitad), range(mitad, len(barras)))):
        gx = 62 + g * 325
        y = 806
        for cx, t, an in ((0, "Barra", "start"), (128, "Fuerza", "end"), (232, "Trabajo", "end"),
                          (305, "Largo", "end")):
            lz.texto(gx + cx, y, t, 14, C["muted"], "700", an)
        lz.linea(gx, y + 9, gx + 305, y + 9, C["border"], 1.5)
        for i, k in enumerate(grupo):
            a, b, tipo = barras[k]
            f = res["fuerzas"][k]
            ry = y + 34 + i * paso_t
            if k in res["criticas"]:
                lz.rect(gx - 8, ry - 21, 321, 30, C["crit"], radio=6, opacidad=0.55)
            nombre = nombre_barra(a, b) + ("*" if tipo == "inf" else "")
            lz.texto(gx, ry, nombre, 16, C["ink"], "700")
            lz.texto(gx + 128, ry, fmt_fuerza(f), 16, color_fuerza(f), "700", "end")
            lz.texto(gx + 232, ry, trabajo(f), 15, color_fuerza(f), "600", "end")
            lz.texto(gx + 305, ry, fmt_cm(res["largos"][k]), 15, C["ink"], "400", "end")
    lz.texto(62, 1132, "* Tramo de la cuerda inferior, que es una sola barra.", 13, C["muted"])
    lz.texto(62, 1150, "Fondo amarillo: barra crítica (la comprimida con mayor |F|·L², se pandea primero).",
             13, C["muted"])

    # Lista de corte
    lz.tarjeta(735, 745, 420, 425, "Lista de corte")
    xs_inf = [op["nodos"][n][0] for n in op["nodos"] if op["nodos"][n][1] == 0]
    filas = [("Cuerda inferior completa", 2, fmt_cm(max(xs_inf) - min(xs_inf)))]
    grupos = {}
    for (a, b, t), L in zip(barras, res["largos"]):
        if t == "inf":
            continue
        clave = (TIPOS[t], str(redondear(L, "0.1")))
        grupos[clave] = grupos.get(clave, 0) + 2
    filas += [(n, q, f"{L} cm") for (n, L), q in grupos.items()]
    n_cara = len(filas)
    sop = {"Transversales": [B] * res["j"]}
    for clave, nombre in (("sup", "Diagonales superiores"), ("portal", "Diagonales de portal"),
                          ("inf", "Diagonales inferiores")):
        for a, b in op[clave]:
            sop.setdefault(nombre, []).append(largo_soporte(op, a, b))
    for nombre, largos in sop.items():
        por_largo = {}
        for L in largos:
            por_largo[str(redondear(L, "0.1"))] = por_largo.get(str(redondear(L, "0.1")), 0) + 1
        for L, q in por_largo.items():
            filas.append((nombre, q, f"{L} cm"))
    y = 806
    lz.texto(757, y, "Pieza", 14, C["muted"], "700")
    lz.texto(1032, y, "Cant.", 14, C["muted"], "700", "end")
    lz.texto(1133, y, "Largo", 14, C["muted"], "700", "end")
    lz.linea(757, y + 9, 1133, y + 9, C["border"], 1.5)
    paso = 25
    for i, (n, q, L) in enumerate(filas):
        ry = y + 31 + i * paso
        es_soporte = i >= n_cara
        lz.texto(757, ry, n, 15, C["trans"] if es_soporte else C["ink"], "700" if i == 0 else "400")
        lz.texto(1032, ry, str(q), 15, C["ink"], "700", "end")
        lz.texto(1133, ry, L, 15, C["ink"], "700" if i == 0 else "400", "end")
    ry = y + 31 + len(filas) * paso - 8
    lz.linea(757, ry, 1133, ry, C["border"], 1.5)
    total_piezas = sum(q for _, q, _ in filas)
    assert total_piezas == res["total"], (total_piezas, res["total"])
    lz.texto(757, ry + 22, "Total", 15, C["ink"], "700")
    lz.texto(1032, ry + 22, str(total_piezas), 15, C["ink"], "700", "end")
    lz.texto(757, 1132, "Medidas de centro a centro de nodo. Al cortar, réstale", 13, C["muted"])
    lz.texto(757, 1150, "el grosor de las barras con las que choca.", 13, C["muted"])

    # Notas
    lz.tarjeta(1180, 745, 380, 425, "Para tener en cuenta")
    notas = list(op["notas"])
    extra = nota_cabezal(op, res)
    if extra:
        notas.append(extra)
    y = 800
    for nota in notas:
        lz.circulo(1205, y - 5, 4, C["badge"])
        for ln in envolver(nota, 40):
            lz.texto(1218, y, ln, 15, C["ink"])
            y += 21
        y += 10
    assert y < 1140, f"Notas demasiado largas en la opción {op['num']}"
    if op["num"] == num_base:
        texto_rel = "Resistencia al pandeo: la menor de las tres (1.0×)"
    else:
        texto_rel = f"Resistencia al pandeo: {redondear(rel, '0.1')}× la de la opción {num_base}"
    lz.texto(1202, 1150, texto_rel, 14, C["badge"], "700")

    lz.texto(
        40, 1205,
        "Supuestos: P es la carga en una cara (la mitad de la carga de la máquina), repartida por igual "
        "entre los nodos de arriba. Nodos articulados.",
        14, C["muted"],
    )
    lz.texto(40, 1226, "Signo: + tensión, − compresión. Fuerzas calculadas por el método de nodos "
             "(ΣFx = 0 y ΣFy = 0 en cada nodo).", 14, C["muted"])
    lz.guardar(os.path.join(CARPETA, op["archivo"] + ".svg"))


# ---------------------------------------------------------------------------
# Lámina comparativa
# ---------------------------------------------------------------------------


def lamina_comparacion(opciones, resultados, rels, num_base):
    W, H = 1600, 1140
    lz = Lienzo(W, H)
    encabezado(
        lz, "Comparación de las opciones de cercha",
        "Balso · base 40 cm · alto 20 cm · cuerda inferior de una sola barra · "
        f"misma sección en todas las barras · b = {fmt_b()} cm",
    )
    rel_max = max(rels)
    for i, (op, res, rel) in enumerate(zip(opciones, resultados, rels)):
        x0 = 40 + i * 515
        w = 490
        lz.tarjeta(x0, 130, w, 810)
        lz.texto(x0 + 24, 170, f"Opción {op['num']}", 16, C["muted"], "700")
        lz.texto(x0 + 24, 202, op["corto"], 25, C["ink"], "700")
        lz.rect(x0 + w - 24 - 132, 152, 132, 44, C["badge"], radio=22)
        lz.texto(x0 + w - 24 - 66, 182, f"{res['total']} barras", 19, "#ffffff", "700", "middle")

        dibujar_frontal(lz, op, res, x0 + 45, 470, 10, compacto=True)

        crit = res["criticas"]
        nombres = " y ".join(nombre_barra(*op["barras"][k][:2]) for k in crit)
        f = res["fuerzas"][crit[0]]
        L = res["largos"][crit[0]]
        y = 560
        lz.texto(x0 + 24, y, "Barra crítica", 14, C["muted"], "700")
        lz.texto(x0 + 24, y + 28, nombres, 22, C["ink"], "700")
        lz.texto(x0 + 24, y + 62, "Fuerza y largo", 14, C["muted"], "700")
        lz.texto(x0 + 24, y + 90, f"{fmt_fuerza(f)}  ·  {fmt_cm(L)}", 22, C["comp"], "700")
        lz.texto(x0 + 24, y + 124, f"Resistencia al pandeo (relativa a la opción {num_base})",
                 14, C["muted"], "700")
        bw = 330 * rel / rel_max
        lz.rect(x0 + 24, y + 138, 330, 26, "#eceff1", radio=13)
        lz.rect(x0 + 24, y + 138, bw, 26, C["badge"], radio=13)
        lz.texto(x0 + 24 + 330 + 14, y + 158, f"{redondear(rel, '0.1')}×", 22, C["badge"], "700")

        y = 760
        lz.texto(x0 + 24, y, "Si el cabezal solo toca el centro", 14, C["muted"], "700")
        c = res["centro"]
        if c:
            nc = " y ".join(nombre_barra(*op["barras"][k][:2]) for k in c["criticas"])
            lz.texto(x0 + 24, y + 26, f"{nc}: {fmt_fuerza(c['fuerza'])}", 18, C["ink"], "700")
        else:
            lz.texto(x0 + 24, y + 26, "Apoya en la mitad de una barra y la dobla", 18, C["ink"], "700")

        y = 830
        for signo, color, texto in (("+", C["badge"], op["pros"]), ("−", C["comp"], op["contras"])):
            lz.circulo(x0 + 34, y - 6, 11, color)
            lz.texto(x0 + 34, y - 0.5, signo, 18, "#ffffff", "700", "middle")
            for ln in envolver(texto, 42):
                lz.texto(x0 + 54, y, ln, 16, C["ink"])
                y += 22
            y += 14
        assert y < 945, f"Texto demasiado largo en la tarjeta de la opción {op['num']}"

    mejor = max(range(len(rels)), key=lambda k: rels[k])
    menos_barras = min(range(len(resultados)), key=lambda k: resultados[k]["total"])
    assert mejor == menos_barras == 0, "Revisa el texto de la recomendación"
    lz.rect(40, 960, 1520, 112, "#e8f5e9", "#a5d6a7", 1.5, radio=14)
    lz.rect(40, 960, 10, 112, C["badge"], radio=4)
    lz.texto(70, 996, "Recomendación", 18, C["badge"], "700")
    lz.texto(70, 1027,
             f"Opción 1: es la más resistente y la que usa menos barras ({resultados[0]['total']}).",
             18, C["ink"], "700")
    lz.texto(70, 1055,
             "Las opciones 2 y 3 usan más barras y resisten menos: manda la barra comprimida más cargada "
             "y más larga, no la cantidad de barras.", 17, C["ink"])
    lz.texto(40, 1102,
             f"Resistencia relativa: |F|·L² de la barra crítica de la opción {num_base} dividido entre el "
             "de cada opción (misma sección y mismo E en todas las barras).", 14, C["muted"])
    lz.texto(40, 1124,
             "P es la carga en una cara, repartida por igual entre los nodos de arriba. La cuerda inferior "
             "de cada cara cuenta como una sola barra.", 14, C["muted"])
    lz.guardar(os.path.join(CARPETA, "04_comparacion_opciones.svg"))


def main():
    opciones = _opciones()
    resultados = [analizar(op) for op in opciones]
    # Base de comparación: la opción menos resistente (mayor índice |F|·L²)
    k_base = max(range(len(resultados)), key=lambda k: resultados[k]["indice"])
    num_base = opciones[k_base]["num"]
    base = resultados[k_base]["indice"]
    rels = [base / r["indice"] for r in resultados]
    for op, res, rel in zip(opciones, resultados, rels):
        lamina_opcion(op, res, rel, num_base)
        print(f"\nOpción {op['num']} ({op['corto']}): {res['total']} barras "
              f"({res['por_cara']} por cara), m = {res['m']}, j = {res['j']}, "
              f"resistencia relativa {rel:.2f}")
        for (a, b, _), f, L in zip(op["barras"], res["fuerzas"], res["largos"]):
            print(f"  {a}-{b}: {f:+.4f} P   L = {L:.2f} cm")
    lamina_comparacion(opciones, resultados, rels, num_base)


if __name__ == "__main__":
    main()
