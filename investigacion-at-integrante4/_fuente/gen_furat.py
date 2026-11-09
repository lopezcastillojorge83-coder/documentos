# -*- coding: utf-8 -*-
"""FURAT ARL SURA (F 2015-PR v3) diligenciado - Accidente del 13/08/2026."""
import os
import xlsxw
from xlsxw import Sheet, style

BUILD = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.dirname(BUILD)
XLSX = os.path.join(OUTDIR, "01_FURAT_ARL_SURA_AT_13-08-2026_diligenciado.xlsx")

NAVY = "1F3864"
BLUE = "0B3D91"     # color de los datos diligenciados
GRAY = "D9D9D9"     # casillas sombreadas (uso exclusivo ARL)
LIGHT = "DDEBF7"
LABELF = "F2F2F2"

S_LABEL = style(font=("Arial", 7, True, False, "000000"), fill=LABELF, v="center")
S_LABEL_ARL = style(font=("Arial", 7, True, False, "000000"), fill=GRAY, v="center")
S_VAL = style(font=("Arial", 9, False, False, BLUE), v="center")
S_VALC = style(font=("Arial", 9, False, False, BLUE), h="center", v="center")
S_VALB = style(font=("Arial", 9, True, False, BLUE), v="center")
S_ARL = style(font=("Arial", 6.5, False, True, "595959"), fill=GRAY, h="center", v="center")
S_OPT = style(font=("Arial", 7, False, False, "000000"), v="center")
S_OPTSEL = style(font=("Arial", 7, True, False, BLUE), v="center")
S_BOX = style(font=("Arial", 9, True, False, BLUE), h="center", v="center",
              border={"l": ("thin", "000000"), "r": ("thin", "000000"), "t": ("thin", "000000"), "b": ("thin", "000000")})
S_SEC = style(font=("Arial", 8.5, True, False, "FFFFFF"), fill=NAVY, v="center", indent=1)
S_SUB = style(font=("Arial", 7, True, False, NAVY), fill=LIGHT, v="center", indent=1)
S_NOTE = style(font=("Arial", 7, False, True, "404040"), v="center")
S_DESC = style(font=("Arial", 8, False, False, BLUE), v="top")

sh = Sheet("FURAT")
for c in range(1, 41):
    sh.col_widths[c] = 2.86
NCOL = 40
LH, VH, OH = 10.5, 15, 13.5   # alturas: etiqueta, valor, opción


def field(r, c1, c2, label, value, arl=False, h="left", vrows=1, bold=False):
    sh.area(r, c1, r, c2, label, S_LABEL_ARL if arl else S_LABEL)
    if arl:
        sh.area(r + 1, c1, r + vrows, c2, value if value else "Uso ARL", S_ARL)
    else:
        st = S_VALB if bold else (S_VALC if h == "center" else S_VAL)
        sh.area(r + 1, c1, r + vrows, c2, value, st)
    sh.outline(r, c1, r + vrows, c2)


def multi(r, c1, c2, label, parts):
    """Campo con varias casillas de valor (p. ej. D / M / A). parts=[(c1,c2,valor)]."""
    sh.area(r, c1, r, c2, label, S_LABEL)
    for (a, b, v) in parts:
        sh.area(r + 1, a, r + 1, b, v, S_VALC)
        sh.outline(r + 1, a, r + 1, b)
    sh.outline(r, c1, r + 1, c2)


def options(r, c1, c2, label, items, label_arl=False):
    """items = [(col_casilla, c_texto1, c_texto2, texto, marcado)]"""
    if label is not None:
        sh.area(r, c1, r, c2, label, S_LABEL_ARL if label_arl else S_LABEL)
        ro = r + 1
    else:
        ro = r
    used = set()
    for (bc, t1, t2, txt, chk) in items:
        sh.area(ro, bc, ro, bc, "X" if chk else "", S_BOX)
        sh.area(ro, t1, ro, t2, txt, S_OPTSEL if chk else S_OPT)
        used.update(range(bc, bc + 1))
        used.update(range(t1, t2 + 1))
    for c in range(c1, c2 + 1):
        if c not in used:
            sh.set(ro, c, None, S_OPT)
    sh.outline(r, c1, ro, c2)
    return ro


def grid(r, c1, c2, label, rows, colspec):
    """Lista de opciones en varias filas/columnas. colspec=[(col_casilla, t1, t2), ...]"""
    sh.area(r, c1, r, c2, label, S_LABEL)
    sh.row_heights[r] = LH
    rr = r
    for row in rows:
        rr += 1
        used = set()
        for (spec, item) in zip(colspec, row):
            if item is None:
                continue
            bc, t1, t2 = spec
            txt, chk = item[0], item[1]
            sh.area(rr, bc, rr, bc, "X" if chk else "", S_BOX)
            if len(item) > 2:          # opción con casilla de especificación
                split = item[2]
                sh.area(rr, t1, rr, split - 1, txt, S_OPTSEL if chk else S_OPT)
                sh.area(rr, split, rr, t2, item[3], S_VAL)
                sh.outline(rr, split, rr, t2)
            else:
                sh.area(rr, t1, rr, t2, txt, S_OPTSEL if chk else S_OPT)
            used.update(range(bc, t2 + 1))
        for c in range(c1, c2 + 1):
            if c not in used:
                sh.set(rr, c, None, S_OPT)
        sh.row_heights.setdefault(rr, OH)
    sh.outline(r, c1, rr, c2)
    return rr


def sec(r, text, h=15):
    sh.area(r, 1, r, NCOL, text, S_SEC)
    sh.outline(r, 1, r, NCOL)
    sh.row_heights[r] = h


def sub(r, c1, c2, text):
    sh.area(r, c1, r, c2, text, S_SUB)
    sh.outline(r, c1, r, c2)


def two(r, lh=LH, vh=VH):
    sh.row_heights[r] = lh
    sh.row_heights[r + 1] = vh


# --------------------------------------------------------------------- encabezado
sh.area(1, 1, 4, 8, "ARL SURA\nRiesgos Laborales", style(font=("Arial", 12, True, False, "0033A0"), h="center", v="center"))
sh.outline(1, 1, 4, 8)
sh.area(1, 9, 2, 32, "INFORME ACCIDENTE DE TRABAJO DEL EMPLEADOR O CONTRATANTE",
        style(font=("Arial", 11, True, False, "000000"), h="center", v="center"))
sh.area(3, 9, 3, 32, "FURAT - Formato Único de Reporte de Accidente de Trabajo (Res. 156 de 2005, modificada por la Res. 2851 de 2015)",
        style(font=("Arial", 7, False, False, "000000"), h="center", v="center"))
sh.area(4, 9, 4, 32, "Responda cada pregunta con letra imprenta clara. NOTA: no llene los espacios sombreados; son de uso exclusivo de la ARL.",
        style(font=("Arial", 6.5, False, True, "404040"), h="center", v="center"))
sh.outline(1, 9, 4, 32)
sh.area(1, 33, 2, 40, "GERENCIA TÉCNICA", style(font=("Arial", 7.5, True, False, "000000"), h="center", v="center"))
sh.area(3, 33, 4, 40, "F 2015 - PR\nVERSIÓN 3", style(font=("Arial", 7.5, False, False, "000000"), h="center", v="center"))
sh.outline(1, 33, 2, 40)
sh.outline(3, 33, 4, 40)
for r in range(1, 5):
    sh.row_heights[r] = 13.5
sh.row_heights[5] = 4

# --------------------------------------------------------------------- afiliación
r = 6
two(r)
field(r, 1, 12, "EPS A LA QUE ESTÁ AFILIADO", "EPS SURA")
field(r, 13, 17, "CÓDIGO EPS", "EPS010", h="center")
field(r, 18, 33, "ARL A LA QUE ESTÁ AFILIADO", "ARL SURA - Seguros de Vida Suramericana S.A.")
field(r, 34, 40, "CÓDIGO ARL", "14-28", h="center")
r = 8
two(r, vh=OH)
options(r, 1, 12, "AFP A LA QUE ESTÁ AFILIADO - ¿SEGURO SOCIAL?",
        [(1, 2, 4, "SI", False), (6, 7, 9, "NO", True)])
field(r, 13, 33, "CUÁL", "Protección S.A. (fondo de pensiones obligatorias)")
field(r, 34, 40, "CÓDIGO AFP O SEGURO SOCIAL", "230201", h="center")

# --------------------------------------------------------------------- sección I
sec(10, "I. IDENTIFICACIÓN GENERAL DEL EMPLEADOR, CONTRATANTE O COOPERATIVA")
r = 11
two(r, vh=OH)
options(r, 1, 40, "TIPO DE VINCULADOR LABORAL",
        [(1, 2, 8, "(1) EMPLEADOR", True), (10, 11, 17, "(2) CONTRATANTE", False),
         (19, 20, 31, "(3) COOPERATIVA DE TRABAJO ASOCIADO", False)])
sub(13, 1, 40, "SEDE PRINCIPAL")
sh.row_heights[13] = 11.5
r = 14
two(r)
field(r, 1, 33, "NOMBRE DE LA ACTIVIDAD ECONÓMICA",
      "Mantenimiento de aeronaves: lavado en seco y presentación (limpieza) de aeronaves - clase de riesgo V")
field(r, 34, 40, "CÓDIGO", "", arl=True)
r = 16
two(r)
field(r, 1, 19, "NOMBRE O RAZÓN SOCIAL", "LIMPIEZA AERONÁUTICA DEL DORADO S.A.S.", bold=True)
options(r, 20, 31, "TIPO DE IDENTIFICACIÓN",
        [(20, 21, 21, "NI", True), (22, 23, 23, "CC", False), (24, 25, 25, "CE", False),
         (26, 27, 27, "NU", False), (28, 29, 29, "PA", False)])
field(r, 32, 40, "NÚMERO", "901.234.567-8", h="center")
r = 18
two(r)
field(r, 1, 14, "DIRECCIÓN", "Calle 25G No. 100-50, Fontibón")
field(r, 15, 21, "TELÉFONO", "601 345 6789", h="center")
field(r, 22, 26, "FAX", "No aplica", h="center")
field(r, 27, 40, "CORREO ELECTRÓNICO", "sst@limpiezaaeronauticadeldorado.com.co")
r = 20
two(r, vh=OH)
field(r, 1, 10, "DEPARTAMENTO", "Bogotá D.C.")
field(r, 11, 13, "CÓDIGO", "", arl=True)
field(r, 14, 23, "MUNICIPIO", "Bogotá D.C.")
field(r, 24, 26, "CÓDIGO", "", arl=True)
options(r, 27, 40, "ZONA", [(27, 28, 31, "U (urbana)", True), (33, 34, 37, "R (rural)", False)])

r = 22
sh.row_heights[22] = 11.5
sh.row_heights[23] = OH
sub(22, 1, 33, "CENTRO DE TRABAJO DONDE LABORA EL TRABAJADOR")
sh.area(23, 1, 23, 25, "¿SON LOS DATOS DEL CENTRO DE TRABAJO LOS MISMOS DE LA SEDE PRINCIPAL?", S_OPT)
options(23, 26, 33, None, [(26, 27, 28, "SI", False), (30, 31, 32, "NO", True)])
sh.outline(22, 1, 23, 33)
field(22, 34, 40, "CÓDIGO", "", arl=True)
sh.area(24, 1, 24, 40, "SÓLO EN CASO NEGATIVO DILIGENCIAR LAS SIGUIENTES CASILLAS SOBRE CENTRO DE TRABAJO:", S_NOTE)
sh.row_heights[24] = 10.5
r = 25
two(r)
field(r, 1, 30, "NOMBRE DE LA ACTIVIDAD ECONÓMICA DEL CENTRO DE TRABAJO",
      "Lavado y limpieza de aeronaves en plataforma (incluye trabajo en alturas)")
field(r, 31, 40, "CÓDIGO DE LA ACTIVIDAD ECONÓMICA DEL CENTRO DE TRABAJO", "", arl=True)
sh.row_heights[25] = 17
r = 27
two(r)
field(r, 1, 22, "DIRECCIÓN", "Aeropuerto Internacional El Dorado, Av. Calle 26 No. 103-09 (plataforma)")
field(r, 23, 31, "TELÉFONO", "601 345 6789 ext. 210", h="center")
field(r, 32, 40, "FAX", "No aplica", h="center")
r = 29
two(r, vh=OH)
field(r, 1, 10, "DEPARTAMENTO", "Bogotá D.C.")
field(r, 11, 13, "CÓDIGO", "", arl=True)
field(r, 14, 23, "MUNICIPIO", "Bogotá D.C.")
field(r, 24, 26, "CÓDIGO", "", arl=True)
options(r, 27, 40, "ZONA", [(27, 28, 31, "U (urbana)", True), (33, 34, 37, "R (rural)", False)])

# --------------------------------------------------------------------- sección II
sec(31, "II. INFORMACIÓN DE LA PERSONA QUE SE ACCIDENTÓ")
r = 32
two(r, vh=OH)
options(r, 1, 33, "TIPO DE VINCULACIÓN",
        [(1, 2, 5, "(1) PLANTA", True), (6, 7, 10, "(2) MISIÓN", False), (11, 12, 16, "(3) COOPERADO", False),
         (17, 18, 25, "(4) ESTUDIANTE O APRENDIZ", False), (26, 27, 33, "(5) INDEPENDIENTE", False)])
field(r, 34, 40, "CÓDIGO (5)", "", arl=True)
r = 34
two(r)
field(r, 1, 10, "PRIMER APELLIDO", "JIMÉNEZ", bold=True)
field(r, 11, 20, "SEGUNDO APELLIDO", "JIMÉNEZ PRADO", bold=True)
field(r, 21, 30, "PRIMER NOMBRE", "ANDRÉS", bold=True)
field(r, 31, 40, "SEGUNDO NOMBRE", "LEONARDO", bold=True)
r = 36
two(r, vh=OH)
options(r, 1, 11, "TIPO DE IDENTIFICACIÓN",
        [(1, 2, 2, "CC", True), (3, 4, 4, "CE", False), (5, 6, 6, "NU", False), (7, 8, 8, "TI", False), (9, 10, 10, "PA", False)])
field(r, 12, 21, "No.", "1030612106121", h="center", bold=True)
multi(r, 22, 33, "FECHA DE NACIMIENTO (D / M / A)", [(22, 25, "02"), (26, 29, "04"), (30, 33, "1988")])
options(r, 34, 40, "SEXO", [(34, 35, 36, "M", True), (37, 38, 40, "F", False)])
r = 38
two(r, vh=OH)
field(r, 1, 18, "DIRECCIÓN", "Carrera 104 No. 23-45, Fontibón")
field(r, 19, 27, "TELÉFONO", "310 555 0199", h="center")
field(r, 28, 33, "FAX", "No aplica", h="center")
options(r, 34, 40, "ZONA", [(34, 35, 36, "U", True), (38, 39, 40, "R", False)])
r = 40
two(r)
field(r, 1, 10, "DEPARTAMENTO", "Bogotá D.C.")
field(r, 11, 13, "CÓDIGO", "", arl=True)
field(r, 14, 23, "MUNICIPIO", "Bogotá D.C.")
field(r, 24, 26, "CÓDIGO", "", arl=True)
field(r, 27, 40, "CARGO", "Auxiliar de presentación", bold=True)
r = 42
two(r)
field(r, 1, 26, "OCUPACIÓN HABITUAL", "Auxiliar de limpieza y presentación de aeronaves")
field(r, 27, 33, "CÓDIGO OCUPACIÓN HABITUAL", "", arl=True)
field(r, 34, 40, "SALARIO U HONORARIOS (MENSUAL)", "$ 2.000.000", h="center")
sh.row_heights[42] = 17
r = 44
two(r, lh=17, vh=OH)
multi(r, 1, 14, "TIEMPO DE OCUPACIÓN HABITUAL AL MOMENTO DEL ACCIDENTE (en meses y días)",
      [(1, 7, "27 meses"), (8, 14, "8 días")])
multi(r, 15, 25, "FECHA DE INGRESO A LA EMPRESA (D / M / A)", [(15, 17, "05"), (18, 20, "05"), (21, 25, "2024")])
options(r, 26, 40, "JORNADA DE TRABAJO HABITUAL",
        [(26, 27, 29, "(1) DIURNA", False), (30, 31, 33, "(2) NOCTURNA", False),
         (34, 35, 36, "(3) MIXTO", True), (37, 38, 40, "(4) TURNOS", False)])
sh.row_breaks.append(45)

# --------------------------------------------------------------------- sección III
sec(46, "III. INFORMACIÓN SOBRE EL ACCIDENTE")
r = 47
two(r, lh=17, vh=OH)
multi(r, 1, 9, "FECHA DEL ACCIDENTE (D / M / A)", [(1, 3, "13"), (4, 6, "08"), (7, 9, "2026")])
multi(r, 10, 15, "HORA DEL ACCIDENTE (0-23 HRS) H / M", [(10, 12, "00"), (13, 15, "30")])
dias = ["LU", "MA", "MI", "JU", "VI", "SA", "DO"]
options(r, 16, 30, "DÍA DE LA SEMANA EN EL QUE OCURRIÓ EL ACCIDENTE",
        [(16 + 2 * i, 17 + 2 * i, 17 + 2 * i, d, d == "JU") for i, d in enumerate(dias)])
options(r, 31, 40, "JORNADA EN QUE SUCEDE",
        [(31, 32, 35, "(1) NORMAL", True), (36, 37, 40, "(2) EXTRA", False)])
r = 49
two(r, lh=17, vh=OH)
options(r, 1, 8, "¿ESTABA REALIZANDO SU LABOR HABITUAL?",
        [(1, 2, 3, "SI", True), (5, 6, 7, "NO", False)])
field(r, 9, 26, "¿CUÁL? (Diligenciar sólo en caso negativo)", "No aplica")
field(r, 27, 31, "CÓDIGO", "", arl=True)
multi(r, 32, 40, "TOTAL TIEMPO LABORADO PREVIO AL ACCIDENTE (H / M)", [(32, 35, "03 h"), (36, 40, "30 min")])
r = 51
two(r, vh=OH)
options(r, 1, 33, "TIPO DE ACCIDENTE",
        [(1, 2, 5, "(1) VIOLENCIA", False), (6, 7, 10, "(2) TRÁNSITO", False), (11, 12, 15, "(3) DEPORTIVO", False),
         (16, 17, 23, "(4) RECREATIVO O CULTURAL", False), (24, 25, 33, "(5) PROPIOS DEL TRABAJO", True)])
options(r, 34, 40, "¿CAUSÓ LA MUERTE AL TRABAJADOR?",
        [(34, 35, 36, "SI", False), (37, 38, 40, "NO", True)])
r = 53
two(r, vh=OH)
field(r, 1, 10, "DEPARTAMENTO DEL ACCIDENTE", "Bogotá D.C.")
field(r, 11, 13, "CÓDIGO", "", arl=True)
field(r, 14, 23, "MUNICIPIO DEL ACCIDENTE", "Bogotá D.C.")
field(r, 24, 26, "CÓDIGO", "", arl=True)
options(r, 27, 40, "ZONA DONDE OCURRIÓ EL ACCIDENTE", [(27, 28, 31, "U (urbana)", True), (33, 34, 37, "R (rural)", False)])
r = 55
two(r, vh=OH)
options(r, 1, 40, "LUGAR DONDE OCURRIÓ EL ACCIDENTE",
        [(1, 2, 12, "(1) DENTRO DE LA EMPRESA", True), (14, 15, 25, "(2) FUERA DE LA EMPRESA", False),
         (27, 28, 36, "(3) TRABAJO EN CASA", False)])
r = 57
cs3 = [(1, 2, 13), (14, 15, 26), (27, 28, 40)]
r = grid(r, 1, 40, "INDIQUE CUÁL SITIO (Indique dónde ocurrió)", [
    [("(1) ALMACENES O DEPÓSITOS", False), ("(2) ÁREAS DE PRODUCCIÓN", True), ("(3) ÁREAS RECREATIVAS O DEPORTIVAS", False)],
    [("(4) CORREDORES O PASILLOS", False), ("(5) ESCALERAS", False), ("(6) PARQUEADEROS O ÁREAS DE CIRCULACIÓN VEHICULAR", False)],
    [("(7) OFICINAS", False), ("(8) OTRAS ÁREAS COMUNES", False), ("(9) OTRO (Especifique)", False, 34, "No aplica")],
], cs3)
r += 1
cs2 = [(1, 2, 20), (21, 22, 40)]
r = grid(r, 1, 40, "TIPO DE LESIÓN (MARQUE CON UNA X CUÁL O CUÁLES)", [
    [("(10) FRACTURA", False), ("(70) ENVENENAMIENTO O INTOXICACIÓN AGUDA O ALERGIA", False)],
    [("(20) LUXACIÓN", False), ("(80) EFECTO DEL TIEMPO, DEL CLIMA U OTRO RELACIONADO CON EL AMBIENTE", False)],
    [("(25) TORCEDURA, ESGUINCE, DESGARRO MUSCULAR, HERNIA O LACERACIÓN DE MÚSCULO O TENDÓN SIN HERIDA", False), ("(81) ASFIXIA", False)],
    [("(30) CONMOCIÓN O TRAUMA INTERNO", True), ("(82) EFECTO DE LA ELECTRICIDAD", False)],
    [("(40) AMPUTACIÓN O ENUCLEACIÓN (Exclusión o pérdida del ojo)", False), ("(83) EFECTO NOCIVO DE LA RADIACIÓN", False)],
    [("(41) HERIDA", False), ("(90) LESIONES MÚLTIPLES", False)],
    [("(50) TRAUMA SUPERFICIAL (Incluye rasguño, punción o pinchazo y lesión en ojo por cuerpo extraño)", False),
     ("(99) OTRO (Especifique)", False, 31, "No aplica")],
    [("(55) GOLPE, CONTUSIÓN O APLASTAMIENTO", False), None],
    [("(60) QUEMADURA", False), None],
], cs2)
for rr in (r - 6, r - 2):        # filas con textos largos
    sh.row_heights[rr] = 18
r += 1
r = grid(r, 1, 40, "PARTE DEL CUERPO APARENTEMENTE AFECTADO", [
    [("(1) CABEZA", True), ("(1.12) OJO", False), ("(2) CUELLO", False)],
    [("(3) TRONCO (Incluye espalda, columna vertebral, médula espinal, pelvis)", False), ("(3.32) TÓRAX", False), ("(3.33) ABDOMEN", False)],
    [("(4) MIEMBROS SUPERIORES", False), ("(4.46) MANOS", False), ("(5) MIEMBROS INFERIORES", False)],
    [("(5.56) PIES", False), ("(6) UBICACIONES MÚLTIPLES", False), ("(7) LESIONES GENERALES U OTRAS", False)],
], cs3)
sh.row_heights[r - 2] = 18
r += 1
agentes = [
    ("(1) MÁQUINAS Y/O EQUIPOS", False), ("(2) MEDIOS DE TRANSPORTE", False), ("(3) APARATOS", True),
    ("(3.36) HERRAMIENTAS, IMPLEMENTOS O UTENSILIOS", False), ("(4) MATERIALES O SUSTANCIAS", False),
    ("(4.4) RADIACIONES", False),
    ("(5) AMBIENTE DE TRABAJO (Incluye superficies de tránsito y de trabajo, muebles, tejados, en el exterior, interior o subterráneos)", False),
    ("(6) OTROS AGENTES NO CLASIFICADOS", False), ("(6.61) ANIMALES (Vivos o productos animales)", False),
    ("(7) AGENTES NO CLASIFICADOS POR FALTA DE DATOS", False)]
mecan = [
    ("(1) CAÍDA DE PERSONAS", True), ("(2) CAÍDA DE OBJETOS", False), ("(3) PISADAS, CHOQUES O GOLPES", False),
    ("(4) ATRAPAMIENTOS", False), ("(5) SOBREESFUERZO, ESFUERZO EXCESIVO O FALSO MOVIMIENTO", False),
    ("(6) EXPOSICIÓN O CONTACTO CON TEMPERATURA EXTREMA", False), ("(7) EXPOSICIÓN O CONTACTO CON LA ELECTRICIDAD", False),
    ("(8) EXPOSICIÓN O CONTACTO CON SUSTANCIAS NOCIVAS, RADIACIONES O SALPICADURAS", False),
    ("(9) OTRO (Especifique)", False, 31, "No aplica"), None]
top = r
sh.area(top, 1, top, 20, "AGENTE DEL ACCIDENTE: (CON QUÉ SE LESIONÓ EL TRABAJADOR)", S_LABEL)
sh.area(top, 21, top, 40, "MECANISMO O FORMA DEL ACCIDENTE", S_LABEL)
sh.row_heights[top] = LH
for i in range(10):
    rr = top + 1 + i
    a = agentes[i]
    sh.area(rr, 1, rr, 1, "X" if a[1] else "", S_BOX)
    sh.area(rr, 2, rr, 20, a[0], S_OPTSEL if a[1] else S_OPT)
    m = mecan[i]
    if m is None:
        for c in range(21, 41):
            sh.set(rr, c, None, S_OPT)
    else:
        sh.area(rr, 21, rr, 21, "X" if m[1] else "", S_BOX)
        if len(m) > 2:
            sh.area(rr, 22, rr, m[2] - 1, m[0], S_OPT)
            sh.area(rr, m[2], rr, 40, m[3], S_VAL)
            sh.outline(rr, m[2], rr, 40)
        else:
            sh.area(rr, 22, rr, 40, m[0], S_OPTSEL if m[1] else S_OPT)
    sh.row_heights[rr] = OH
sh.row_heights[top + 7] = 18
sh.row_heights[top + 8] = 18
sh.outline(top, 1, top + 10, 20)
sh.outline(top, 21, top + 10, 40)
r = top + 11

# --------------------------------------------------------------------- sección IV
sec(r, "IV. DESCRIPCIÓN DEL ACCIDENTE")
r += 1
sh.area(r, 1, r, 40, "DESCRIBA DETALLADAMENTE EL ACCIDENTE. QUÉ LO ORIGINÓ O CAUSÓ (Responda a las preguntas qué pasó, cuándo, dónde, cómo y por qué)", S_LABEL)
sh.row_heights[r] = LH
DESC = (
    "QUÉ: caída de persona desde un banco-escalera/plataforma de lavado de aeronaves, desde 4,35 m sobre el plano de referencia "
    "hasta el piso de la plataforma, con golpe en la cabeza. "
    "CUÁNDO: jueves 13/08/2026, aproximadamente a las 00:30, después de 3 h 30 min de un turno nocturno iniciado a las 21:00. "
    "DÓNDE: posición Golfo, plataforma del Aeropuerto Internacional El Dorado, Bogotá D.C.\n"
    "CÓMO: el trabajador, auxiliar de presentación con certificación vigente en trabajo seguro en alturas nivel avanzado y concepto "
    "médico de aptitud, realizaba limpieza en húmedo de una aeronave sobre el banco, que tenía baranda solo en el lado derecho "
    "(lados izquierdo y frontal sin baranda). Según su versión, se tropezó y cayó. Portaba arnés de cuerpo entero Hawk 412X y eslinga "
    "en Y con absorbedor de 1,80 m; el punto de anclaje estaba a 4,15 m, por debajo del plano de trabajo. El absorbedor no se activó y el "
    "gancho de 1-1/4\" de la eslinga presenta dañado el mecanismo de cierre de doble seguro. El permiso de trabajo estaba firmado por "
    "el coordinador de trabajo seguro en alturas y por los demás operarios del turno, pero no por el accidentado; no se evidencian listas "
    "de chequeo del arnés, la eslinga ni el banco. Recibió atención en el sitio y fue trasladado a la Clínica de Occidente. Diagnóstico "
    "de ingreso: trauma craneoencefálico severo con pérdida del conocimiento; incapacidad inicial de 15 días, prorrogada 15 días.\n"
    "POR QUÉ (preliminar, en investigación): bordes del banco sin protección colectiva, sistema de detención de caídas que no tomó "
    "carga y anclaje ubicado por debajo de los pies, sin programa de prevención y protección contra caídas. Accidente GRAVE "
    "(Res. 1401 de 2007, art. 3): se reporta a la Dirección Territorial del Ministerio del Trabajo y se investigará dentro de los 15 días."
)
sh.area(r + 1, 1, r + 9, 40, DESC, S_DESC)
sh.outline(r, 1, r + 9, 40)
for rr in range(r + 1, r + 10):
    sh.row_heights[rr] = 15.75
r += 10
sub(r, 1, 40, "PERSONAS QUE PRESENCIARON EL ACCIDENTE")
sh.row_heights[r] = 11.5
r += 1
sh.area(r, 1, r, 19, "¿HUBO PERSONAS QUE PRESENCIARON EL ACCIDENTE?", S_OPT)
sh.area(r, 20, r, 20, "", S_BOX)
sh.area(r, 21, r, 22, "SI", S_OPT)
sh.area(r, 23, r, 23, "X", S_BOX)
sh.area(r, 24, r, 25, "NO", S_OPTSEL)
sh.area(r, 26, r, 40, "EN CASO AFIRMATIVO, DILIGENCIAR LA SIGUIENTE INFORMACIÓN:", S_NOTE)
sh.outline(r, 1, r, 40)
sh.row_heights[r] = OH
r += 1
sh.area(r, 1, r, 20, "APELLIDOS Y NOMBRES COMPLETOS", S_LABEL)
sh.area(r, 21, r, 30, "DOCUMENTO DE IDENTIDAD (tipo y número)", S_LABEL)
sh.area(r, 31, r, 40, "CARGO", S_LABEL)
for (a, b) in ((1, 20), (21, 30), (31, 40)):
    sh.outline(r, a, r, b)
sh.row_heights[r] = LH
r += 1
sh.area(r, 1, r, 40, "No aplica: en la indagación preliminar no se identificaron testigos presenciales directos; la versión inicial "
        "es la del trabajador. Si se identifican testigos entre los operarios del turno, se actualiza este informe.", S_VAL)
sh.outline(r, 1, r, 40)
sh.row_heights[r] = 22
r += 1
sub(r, 1, 40, "PERSONA RESPONSABLE DEL INFORME (Representante o Delegado)")
sh.row_heights[r] = 11.5
r += 1
two(r, vh=26)
field(r, 1, 16, "APELLIDOS Y NOMBRES COMPLETOS", "TORRES RUIZ LAURA MARCELA", bold=True)
field(r, 17, 23, "DOCUMENTO DE IDENTIDAD", "CC 52.987.654", h="center")
field(r, 24, 33, "CARGO", "Responsable del SG-SST (delegada del empleador)")
field(r, 34, 40, "FIRMA", "")
r += 2
two(r, lh=17, vh=OH)
multi(r, 1, 16, "FECHA DE DILIGENCIAMIENTO DEL INFORME DEL ACCIDENTE (D / M / A)", [(1, 5, "13"), (6, 10, "08"), (11, 16, "2026")])
field(r, 17, 40, "USO EXCLUSIVO DE LA ARL: número de radicado y fecha de recibo", "", arl=True)
r += 2
sh.area(r, 1, r + 1, 40,
        "Reproducción del formato ARL SURA F 2015-PR versión 3 diligenciada con fines académicos (Universidad Distrital, SST 2026-3). "
        "Los datos de la empresa, la EPS, la AFP, el salario y los datos de contacto son supuestos: ver la hoja \"Notas y supuestos\". "
        "Entregar copia al trabajador y radicar ante la ARL y la EPS dentro de los 2 días hábiles siguientes al accidente.", S_NOTE)
sh.row_heights[r] = 12
sh.row_heights[r + 1] = 12
last = r + 1
sh.print_area = "$A$1:$AN$%d" % last
sh.footer = "&L&7FURAT - AT del 13/08/2026 (ejercicio académico)&R&7Página &P de &N"

# --------------------------------------------------------------------- hoja de notas
nt = Sheet("Notas y supuestos")
nt.col_widths = {1: 5, 2: 26, 3: 38, 4: 74, 5: 17, 6: 9}
nt.fit_width = True
nt.orientation = "landscape"
nt.print_titles = "$3:$3"
nt.freeze = (4, 1)
H_ST = style(font=("Arial", 9, True, False, "FFFFFF"), fill=NAVY, h="center", v="center")
T_ST = style(font=("Arial", 9, False, False, "000000"), v="top")
TB_ST = style(font=("Arial", 9, True, False, "000000"), v="top")
nt.area(1, 1, 1, 6, "FURAT del accidente del 13/08/2026: origen de cada dato, cálculos y criterios de diligenciamiento",
        style(font=("Arial", 12, True, False, NAVY), v="center"))
nt.row_heights[1] = 22
nt.area(2, 1, 2, 6, "Tipo de dato: Caso = dato de la guía de laboratorio; Calculado = obtenido a partir de datos de la guía; "
        "Supuesto = no lo da la guía, reemplazar si el grupo definió otro valor; Criterio = decisión de clasificación según el instructivo del FURAT.",
        style(font=("Arial", 8.5, False, True, "404040"), v="center"))
nt.row_heights[2] = 26
for i, h in enumerate(["N.º", "Campo del FURAT", "Valor registrado", "Fuente o justificación", "Tipo de dato", "Ref. (IEEE)"]):
    nt.area(3, i + 1, 3, i + 1, h, H_ST)
    nt.outline(3, i + 1, 3, i + 1, color="FFFFFF")
nt.row_heights[3] = 18
NOTAS = [
    ("EPS y código", "EPS SURA - EPS010", "La guía no indica la EPS. Código de la tabla de administradoras de la PILA; verificar en la planilla de aportes de la empresa.", "Supuesto"),
    ("ARL y código", "ARL SURA (Seguros de Vida Suramericana S.A.) - 14-28", "El formato usado es el de ARL SURA. Verificar el código de la administradora en la PILA.", "Supuesto"),
    ("AFP y código", "Seguro Social: NO. Protección S.A. - 230201", "La guía no indica la AFP. El ISS (Seguro Social) fue reemplazado por Colpensiones. Verificar el código en la PILA.", "Supuesto"),
    ("Tipo de vinculador laboral", "(1) Empleador", "La empresa contrata directamente al trabajador (es contratista de una gran empresa, pero es su empleador).", "Criterio"),
    ("Razón social, NIT, dirección, teléfono, correo", "LIMPIEZA AERONÁUTICA DEL DORADO S.A.S., NIT 901.234.567-8, Calle 25G No. 100-50, 601 345 6789", "Datos ficticios. Reemplazar por los que use el grupo en la cotización y en el informe final.", "Supuesto"),
    ("Actividad económica y clase de riesgo", "Mantenimiento de aeronaves (lavado en seco y presentación) - clase V", "Guía: actividad de la empresa y \"la empresa es riesgo V\". Los códigos de actividad los asigna la ARL (casillas sombreadas).", "Caso"),
    ("Centro de trabajo", "NO coincide con la sede principal: operación en plataforma del Aeropuerto Internacional El Dorado, Av. Calle 26 No. 103-09", "Lugar donde el trabajador presta el servicio en los tres turnos.", "Criterio"),
    ("Tipo de vinculación", "(1) Planta", "Trabajador directo con fecha de ingreso 05/05/2024.", "Criterio"),
    ("Apellidos y nombres", "JIMÉNEZ / JIMÉNEZ PRADO / ANDRÉS / LEONARDO", "Guía: \"Andrés Leonardo Jiménez Jiménez Prado\". Se transcribe completo; verificar contra la cédula (puede ser una repetición del apellido).", "Caso"),
    ("Identificación", "CC 1030612106121", "Guía.", "Caso"),
    ("Fecha de nacimiento y edad", "02/04/1988 - 38 años al accidente", "Guía; la edad se calcula al 13/08/2026.", "Caso / calculado"),
    ("Sexo", "M", "Nombre masculino y registro fotográfico de la guía.", "Criterio"),
    ("Dirección y teléfono del trabajador", "Carrera 104 No. 23-45, Fontibón; 310 555 0199", "Datos ficticios.", "Supuesto"),
    ("Cargo y ocupación habitual", "Auxiliar de presentación / Auxiliar de limpieza y presentación de aeronaves", "Guía: cargo y funciones (limpieza y aseo de aeronaves según el procedimiento de cada servicio).", "Caso"),
    ("Tiempo de ocupación habitual", "27 meses y 8 días", "Del 05/05/2024 al 13/08/2026 = 2 años, 3 meses y 8 días (830 días). Se asume que la experiencia en el oficio es igual a la antigüedad en la empresa.", "Calculado"),
    ("Salario", "$ 2.000.000", "La guía no lo indica. Valor supuesto superior al SMMLV 2026 ($ 1.750.905).", "Supuesto"),
    ("Jornada de trabajo habitual", "(3) Mixto", "Guía: \"Mixto, turno rotativo\". Si el grupo prefiere resaltar la rotación, el instructivo admite (4) Turnos; marcar solo una.", "Caso"),
    ("Fecha y hora del accidente", "13/08/2026 - 00:30", "Guía.", "Caso"),
    ("Día de la semana", "JU (jueves)", "Calendario 2026: el 13/08/2026 es jueves.", "Calculado"),
    ("Inicio del turno", "21:00 del 12/08/2026", "La guía dice que el turno anterior terminó a las 05:00 del 13/08 y que regresó a las 21:00 del 13/08; eso no cuadra con un accidente a las 00:30 del 13/08 con 3 h 30 min laboradas. Se conserva la fecha oficial del accidente y se ubica el turno el 12/08. Confirmar con control de acceso o nómina.", "Criterio (inconsistencia)"),
    ("Jornada en que sucede", "(1) Normal", "El accidente ocurrió dentro del turno ordinario (3 h 30 min laboradas).", "Criterio"),
    ("¿Labor habitual?", "SI", "Guía: \"Estaba realizando las funciones asignadas: SI\".", "Caso"),
    ("Tiempo laborado previo", "3 h 30 min", "Guía.", "Caso"),
    ("Tipo de accidente", "(5) Propios del trabajo", "Ocurrió ejecutando la labor; no hubo vehículo en movimiento, violencia ni actividad deportiva o recreativa.", "Criterio"),
    ("¿Causó la muerte?", "NO", "Guía: incapacidad de 15 + 15 días.", "Caso"),
    ("Departamento, municipio y zona", "Bogotá D.C. - urbana", "Aeropuerto Internacional El Dorado, Bogotá D.C. Los códigos DIVIPOLA los registra la ARL.", "Caso"),
    ("Lugar", "(1) Dentro de la empresa", "Ocurrió en el centro de trabajo donde la empresa presta su servicio (plataforma, posición Golfo) y durante la labor habitual. Si el grupo considera la plataforma como instalación del cliente, marcar (2) Fuera de la empresa: el instructivo permite conservar el sitio (2) Áreas de producción.", "Criterio"),
    ("Sitio", "(2) Áreas de producción", "El instructivo incluye en esta opción las instalaciones al aire libre, los andamios y el área de producción de servicios.", "Criterio"),
    ("Tipo de lesión", "(30) Conmoción o trauma interno", "Historia clínica de ingreso: trauma craneoencefálico severo con pérdida del conocimiento.", "Caso"),
    ("Parte del cuerpo", "(1) Cabeza", "Guía.", "Caso"),
    ("Agente del accidente", "(3) Aparatos", "El instructivo ubica las escaleras móviles, rampas móviles y andamios en \"Aparatos\" y los excluye de \"Ambiente de trabajo\". El banco-plataforma de lavado es un equipo de acceso móvil. Lectura alternativa: (5) Ambiente de trabajo, si se toma la superficie contra la que se golpeó.", "Criterio"),
    ("Mecanismo", "(1) Caída de personas", "Guía: caída de diferente nivel desde 4,35 m.", "Caso"),
    ("Clínica", "Clínica de Occidente", "La guía nombra la Clínica de Occidente en el campo y la Clínica de Oriente en la nota; confirmar con la historia clínica.", "Caso (inconsistencia)"),
    ("Testigos", "NO", "La indagación preliminar solo recoge la versión del trabajador. Si se identifican testigos entre los operarios del turno, actualizar el FURAT y la investigación.", "Criterio"),
    ("Responsable del informe", "TORRES RUIZ LAURA MARCELA - CC 52.987.654 - Responsable del SG-SST", "Nombre ficticio. Según la guía, el responsable del SG-SST también es el coordinador de trabajo seguro en alturas. Reemplazar por el integrante que asuma el rol.", "Supuesto"),
    ("Fecha de diligenciamiento", "13/08/2026", "Dentro de las 48 horas de la guía y de los 2 días hábiles legales (Decreto Ley 1295 de 1994, art. 62; Res. 156 de 2005 mod. Res. 2851 de 2015). Plazo máximo: martes 18/08/2026, porque el lunes 17/08/2026 es festivo.", "Criterio"),
    ("Reporte a la Dirección Territorial", "Plazo: 18/08/2026", "Accidente grave (trauma craneoencefálico): reporte directo al Ministerio del Trabajo dentro de los 2 días hábiles (Decreto 1072 de 2015, art. 2.2.4.1.7).", "Requisito legal"),
    ("Casillas sombreadas", "En blanco (\"Uso ARL\")", "Según el formato, solo las diligencia la ARL (códigos de actividad, ocupación, DIVIPOLA y radicado).", "Instrucción del formato"),
]
REFS = ['[2]', '[2]', '[2]', '[2]', '-', '[1], [2]', '[1], [2]', '[1], [2]', '[1]', '[1]', '[1]', '[1]', '-', '[1]', '[1], [2]', '-', '[1], [2]', '[1]', '[1]', '[1]', '[1], [2]', '[1]', '[1]', '[2]', '[1]', '[1], [2]', '[2]', '[2]', '[1], [2]', '[1]', '[2]', '[1], [2]', '[1]', '[1], [2]', '[1]', '[3]-[5]', '[6], [7]', '[2]']
assert len(REFS) == len(NOTAS), (len(REFS), len(NOTAS))
rr = 4
for i, (campo, valor, fuente, tipo) in enumerate(NOTAS, 1):
    nt.area(rr, 1, rr, 1, str(i), style(font=("Arial", 9, False, False, "000000"), h="center", v="top"))
    nt.area(rr, 2, rr, 2, campo, TB_ST)
    nt.area(rr, 3, rr, 3, valor, style(font=("Arial", 9, False, False, BLUE), v="top"))
    nt.area(rr, 4, rr, 4, fuente, T_ST)
    fill = {"Supuesto": "FFF2CC"}.get(tipo, None)
    if "inconsistencia" in tipo:
        fill = "FCE4D6"
    nt.area(rr, 5, rr, 5, tipo, style(font=("Arial", 9, False, False, "000000"), fill=fill, h="center", v="top"))
    nt.area(rr, 6, rr, 6, REFS[i - 1], style(font=("Arial", 9, False, False, "000000"), h="center", v="top"))
    for c in range(1, 7):
        nt.outline(rr, c, rr, c, color="A6A6A6")
    lines = max(len(fuente) / 72.0, len(valor) / 36.0, len(campo) / 25.0)
    nt.row_heights[rr] = max(15, 12.5 * (int(lines) + 1) + 2)
    rr += 1
rr += 1
nt.area(rr, 1, rr, 6, "Referencias (formato IEEE)", style(font=("Arial", 10, True, False, NAVY), v="center"))
nt.row_heights[rr] = 18
REF_TXT = [
    '[1] Universidad Distrital Francisco José de Caldas, "Guía de laboratorio: Seguridad y Salud en el Trabajo, actividad número 2," Proyecto Curricular de Ingeniería Industrial, Bogotá, Colombia, 2026.',
    '[2] ARL SURA, "Informe de accidente de trabajo del empleador o contratante (F 2015-PR, versión 3) e instructivo de diligenciamiento," Seguros de Vida Suramericana S.A., Colombia, s.f.',
    '[3] Presidencia de la República de Colombia, Decreto Ley 1295 de 1994, "por el cual se determinan la organización y administración del Sistema General de Riesgos Profesionales," Bogotá, Colombia, jun. 1994.',
    '[4] Ministerio de la Protección Social, Resolución 156 de 2005, "por la cual se adoptan los formatos de informe de accidente de trabajo y de enfermedad profesional y se dictan otras disposiciones," Bogotá, Colombia, ene. 2005.',
    '[5] Ministerio del Trabajo, Resolución 2851 de 2015, "por la cual se modifica el artículo 3° de la Resolución 156 de 2005," Bogotá, Colombia, 2015.',
    '[6] Ministerio del Trabajo, Decreto 1072 de 2015, "por medio del cual se expide el Decreto Único Reglamentario del Sector Trabajo," Bogotá, Colombia, may. 2015.',
    '[7] Ministerio de la Protección Social, Resolución 1401 de 2007, "por la cual se reglamenta la investigación de incidentes y accidentes de trabajo," Diario Oficial 46.638, Bogotá, Colombia, may. 2007.',
]
for t in REF_TXT:
    rr += 1
    nt.area(rr, 1, rr, 6, t, style(font=("Arial", 9, False, False, "000000"), v="top"))
    nt.row_heights[rr] = 15 if len(t) < 230 else 27
nt.print_area = "$A$1:$F$%d" % rr
nt.footer = "&L&7FURAT - Notas y supuestos&R&7Página &P de &N"

os.makedirs(OUTDIR, exist_ok=True)
xlsxw.save(XLSX, [sh, nt], title="FURAT diligenciado - AT 13/08/2026", creator="Integrante 4")
print("XLSX:", XLSX, "filas FURAT:", last)
