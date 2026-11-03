# -*- coding: utf-8 -*-
"""Contenido del informe como lista de bloques (independiente del formato)."""
from arbol import NODOS, ANT, relacion, consecuentes

AZUL_CLARO = "EAF0F7"
FIGURA = "arbol_de_causas.png"
TITULO = "Investigación de accidente de trabajo por el método del árbol de causas (NTP 274)"
SUBTITULO = "Caída de altura desde un andamio durante trabajos de reparación de fachada"

CORTO = {
    "1.1.1": "el trabajador desconoce el riesgo",
    "1.2.1": "tablones colocados sin sujeción",
    "1.2.2": "sin verificación tras el montaje",
    "1.3.1": "sin comprobación diaria de protecciones",
    "1.3.2": "barandilla retirada",
    "2.1.1": "sin arneses ni anclajes",
}


def recorrido():
    """Hechos del árbol (sin causas primarias) en profundidad desde el accidente."""
    res = []

    def rec(n):
        if n in res or n not in ANT:
            return
        res.append(n)
        for a in ANT[n]:
            rec(a)
    rec("0")
    return res


CAUSA_CORTA = {  # nombre breve de las causas primarias (texto completo: Figura 1)
    "C1": "No se imparte formación ni información sobre riesgos en altura",
    "C2": "Montaje sin plan de montaje y por personal sin cualificación",
    "C3": "Sin procedimiento ni responsable de inspección del andamio",
    "C4": "Planificación preventiva insuficiente",
}


def fila_construccion(h):
    ants = ANT[h]
    rel = relacion(h)
    textos = [f"**{a}** {CAUSA_CORTA.get(a, NODOS[a][1])}" for a in ants]
    if rel == "Disyunción":
        otros = ", ".join(c for c in consecuentes(ants[0]) if c != h)
        textos[0] += f" *(también origina {otros})*"
    return [f"**{h}** {NODOS[h][1]}", textos, f"**{rel}**"]


def fila_causa(c):
    hechos = [f"**{h}** {CORTO[h]}" for h in consecuentes(c)]
    return [f"**{c}**", NODOS[c][1], hechos]


# ---------------------------------------------------------------- portada
PORTADA = [("portada", {
    "titulo": TITULO,
    "subtitulo": SUBTITULO,
    "datos": [
        ("Asignatura", "Seguridad (Gr. 23)"),
        ("Docente", "Germán Suárez"),
        ("Actividad", "Investigación de accidentes bajo NTP 274 "
                      "(metodología diagrama de árbol)"),
        ("Fecha de entrega", "3 de noviembre de 2026"),
    ],
    "integrantes": [
        ("1", "[Nombre completo del integrante 1]", "[Código]"),
        ("2", "[Nombre completo del integrante 2]", "[Código]"),
        ("3", "[Nombre completo del integrante 3]", "[Código]"),
    ],
})]

# ------------------------------------------------- 1. objetivo y método
SEC1 = [
    ("h1", "1. Objetivo y método"),
    ("p", "Este informe aplica el método del árbol de causas de la NTP 274 "
          "(INSHT) a una caída de altura desde un andamio, ocurrida durante "
          "trabajos de reparación de fachada. El objetivo es reconstruir la "
          "concatenación de hechos que produjo la lesión, llegar a las causas "
          "primarias y proponer medidas para eliminarlas o controlarlas."),
    ("p", "El árbol se construye de arriba hacia abajo. Se parte de la lesión "
          "y, para cada hecho, se responde a la pregunta **«¿qué tuvo que "
          "ocurrir para que este hecho se produjera?»** y después a **«¿tuvo "
          "que ocurrir alguna otra cosa?»**. Se buscan causas y no "
          "responsables, y solo se aceptan hechos probados."),
    ("nota", "**Nota sobre el caso.** Los hechos son un supuesto de trabajo, "
             "construido a partir de las causas más habituales en caídas desde "
             "andamios. En una investigación real, cada caja del árbol debe "
             "respaldarse con hechos comprobados mediante inspección in situ, "
             "entrevistas y documentación."),
]

# ------------------------------------------- 2. descripción del accidente
SEC2 = [
    ("h1", "2. Descripción del accidente"),
    ("h2", "2.1 Datos generales"),
    ("tabla", {"anchos": [27, 73], "fondo_col0": True, "filas": [
        ["**Tipo de accidente**", "Caída de personas a distinto nivel (caída de altura)."],
        ["**Actividad**", "Reparación de la fachada de un edificio de viviendas de "
                          "cinco plantas: picado del revoco desprendido, saneado de "
                          "grietas y aplicación de mortero de reparación."],
        ["**Agente material**", "Andamio tubular de fachada con cuatro niveles de "
                                "trabajo, montado cinco días antes."],
        ["**Lugar**", "Nivel 3 del andamio (6 m sobre el suelo), módulo del extremo lateral."],
        ["**Condiciones**", "Jornada de mañana, tiempo seco y sin viento."],
        ["**Accidentado**", "Oficial de albañilería de 38 años, con 12 años de "
                            "experiencia en el oficio y 8 meses en la empresa. Sin "
                            "formación específica en trabajos en altura."],
        ["**Lesiones**", "Politraumatismo grave (fractura de columna lumbar y de pelvis)."],
    ]}),
    ("h2", "2.2 Relato de los hechos"),
    ("p", "Los trabajos se realizaban desde un andamio tubular de fachada que "
          "habían montado cinco días antes operarios de la propia obra, sin "
          "formación en montaje y sin plan de montaje. Nadie verificó el andamio "
          "tras el montaje, y en la obra no existía un procedimiento de inspección "
          "ni un responsable designado."),
    ("p", "Dos días antes del accidente se había retirado la barandilla del "
          "lateral del extremo del nivel 3 para pasar materiales (cubos de "
          "mortero) a la plataforma, porque no se había previsto otro medio de "
          "elevación. La barandilla no se repuso y nadie comprobó el estado de "
          "las protecciones al reanudar la jornada. En esa plataforma, los "
          "tablones estaban apoyados sobre los travesaños sin ninguna sujeción."),
    ("p", "La mañana del accidente, un oficial de albañilería picaba el revoco "
          "desprendido de un paño de fachada situado en el extremo del andamio. "
          "Para valorar el resultado retrocedió hacia el extremo de la plataforma, "
          "pisó el borde de un tablón suelto y éste basculó. El trabajador perdió "
          "el equilibrio y, al no haber barandilla, cayó al vacío desde unos 6 m "
          "hasta el suelo. No llevaba arnés: en la obra no había arneses ni puntos "
          "de anclaje en el andamio. Al no tener formación específica en trabajos "
          "en altura, no había percibido el riesgo de trabajar junto a un borde "
          "sin protección."),
    ("p", "Los compañeros avisaron a los servicios de emergencia y el trabajador "
          "fue trasladado al hospital con un politraumatismo grave."),
]

# ------------------------------------------------------- 3. toma de datos
SEC3 = [
    ("h1", "3. Toma de datos"),
    ("p", "La NTP 274 pide reconstruir las circunstancias que existían justo "
          "antes del accidente y recoger información de tres ámbitos: las "
          "condiciones materiales, la organización del trabajo y el comportamiento "
          "humano. La calidad del árbol depende de la calidad de estos datos."),
    ("tabla", {"anchos": [24, 76], "fondo_col0": True,
               "cab": ["Ámbito", "Hechos recabados"], "filas": [
        ["**Condiciones materiales**", [
            "• Plataforma del nivel 3 con tablones apoyados sobre los travesaños, sin sujeción.",
            "• Lateral del extremo sin barandilla ni rodapié: se retiró dos días antes "
            "para pasar materiales y no se repuso.",
            "• Sin arneses anticaídas en la obra ni puntos de anclaje en el andamio."]],
        ["**Organización del trabajo**", [
            "• Andamio montado por personal de la obra, sin cualificación y sin plan de montaje.",
            "• Sin procedimiento ni responsable de inspección: nadie verificó el andamio "
            "tras el montaje ni comprobó las protecciones antes de cada jornada.",
            "• Sin evaluación específica del riesgo de caída y sin medio previsto para "
            "elevar materiales.",
            "• Sin formación ni información sobre riesgos de trabajos en altura."]],
        ["**Comportamiento humano**", [
            "• Oficial con experiencia en el oficio, pero sin formación específica en altura.",
            "• Retrocedió hacia el extremo para valorar el paño picado (acto habitual "
            "de trabajo)."]],
    ]}),
    ("p", "*Fuentes consideradas:* inspección in situ, declaración del accidentado y "
          "de los compañeros, entrevista con el encargado y documentación de la obra."),
]

# ---------------------------------------- 4. método de construcción del árbol
SEC4 = [
    ("h1", "4. Método de construcción del árbol"),
    ("p", "Para cada hecho se buscan sus antecedentes inmediatos y se clasifica la "
          "relación entre ellos. La NTP 274 distingue cuatro situaciones, que "
          "aparecen todas en este caso:"),
    ("tabla", {"anchos": [19, 41, 40], "fondo_col0": True,
               "cab": ["Situación", "Qué significa", "En este árbol"], "filas": [
        ["**Cadena**", "Un hecho tiene un solo antecedente y no se habría producido sin él.",
         "1.1.1 origina 1.1; C1 origina 1.1.1; C2 origina 1.2.1; 2.1.1 origina 2.1 y "
         "éste origina 2."],
        ["**Conjunción**", "Un hecho tiene varios antecedentes independientes entre sí "
                           "y hacen falta todos.",
         "1 y 2 originan el accidente; 1.1, 1.2 y 1.3 originan 1; 1.2.1 y 1.2.2 originan "
         "1.2; 1.3.1 y 1.3.2 originan 1.3."],
        ["**Disyunción**", "Un único antecedente da lugar a varios hechos independientes.",
         "C3 origina 1.2.2 y 1.3.1; C4 origina 1.3.2 y 2.1.1."],
        ["**Hechos independientes**", "Hechos sin relación entre sí: en el dibujo no se unen.",
         "La rama de la caída (1) y la de la falta de retención (2) no dependen una de otra."],
    ]}),
]

# ------------------------------------------------ 5. árbol de causas (figura)
SEC5 = [
    ("seccion", "horizontal"),
    ("h1", "5. Árbol de causas"),
    ("figura", {"archivo": FIGURA, "ancho_cm": 24.5,
                "pie": "Figura 1. Árbol de causas de la caída de altura desde un "
                       "andamio durante trabajos de reparación de fachada."}),
    ("seccion", "vertical"),
]

# ------------------------------------------- 6. desarrollo paso a paso
SEC5B = [
    ("h1", "6. Desarrollo del árbol paso a paso"),
    ("p", "Partiendo del accidente, cada fila responde a «¿qué tuvo que ocurrir para "
          "que este hecho se produjera?». El número de cada hecho es el que aparece "
          "en la Figura 1."),
    ("tabla", {"anchos": [35, 51, 14], "repetir_cab": True,
               "cab": ["Hecho", "Antecedentes inmediatos", "Relación"],
               "filas": [fila_construccion(h) for h in recorrido()]}),
    ("p", "**Fin del árbol.** Las ramas terminan en C1, C2, C3 y C4. Son causas "
          "primarias: no necesitan una situación anterior para ser explicadas "
          "(criterio de finalización a) de la NTP 274)."),
]

# --------------------------------------------------- 6. causas primarias
SEC6 = [
    ("h1", "7. Causas primarias"),
    ("tabla", {"anchos": [9, 56, 35], "fondo_col0": True, "repetir_cab": True,
               "cab": ["Código", "Causa primaria (fallo organizativo)",
                       "Hechos que origina"],
               "filas": [fila_causa(c) for c in ("C1", "C2", "C3", "C4")]}),
    ("p", "Las cuatro causas primarias son fallos de organización. Los fallos "
          "técnicos (tablones sueltos, borde sin barandilla, falta de arnés) y el "
          "comportamiento del trabajador aparecen porque la organización no los "
          "previno ni los controló, como señala la NTP 274."),
    ("p", "C3 y C4 son causas comunes de dos hechos cada una (disyunción), de ramas "
          "distintas del árbol. Corregirlas elimina varios hechos a la vez."),
]

# -------------------------------------------------- 7. medidas preventivas
SEC7 = [
    ("h1", "8. Medidas preventivas propuestas"),
    ("tabla", {"anchos": [21, 65, 14], "fondo_col0": True, "repetir_cab": True,
               "cab": ["Actuar sobre", "Medidas", "Hechos que corrige"], "filas": [
        ["**Medidas inmediatas**", [
            "• Paralizar los trabajos en el andamio e inspeccionar todos sus niveles.",
            "• Fijar y trabar las plataformas y reponer barandillas y rodapiés.",
            "• Revisar el resto de andamios de la obra antes de reanudar."], "1.2, 1.3"],
        ["**C1** Formación", [
            "• Formación teórico-práctica en trabajos en altura, uso de andamios y "
            "equipos anticaídas antes de empezar la obra, con registro de asistencia.",
            "• Instrucción de acogida: no trabajar en una plataforma sin protección "
            "completa y derecho a paralizar la tarea."], "1.1.1"],
        ["**C2** Montaje", [
            "• Montaje, modificación y desmontaje a cargo de personal formado y "
            "competente, con plan de montaje, utilización y desmontaje y siguiendo "
            "las instrucciones del fabricante.",
            "• Plataformas completas, con elementos sujetos y trabados, y barandilla "
            "principal, intermedia y rodapié en todo el perímetro (UNE-EN 12811-1)."],
         "1.2.1"],
        ["**C3** Inspección y supervisión", [
            "• Procedimiento escrito de inspección del andamio: tras el montaje, "
            "antes de cada jornada (lista de verificación) y tras cualquier "
            "modificación o inclemencia.",
            "• Persona competente designada, registro de las inspecciones y "
            "señalización del estado del andamio («apto» / «no apto»)."],
         "1.2.2, 1.3.1"],
        ["**C4** Planificación preventiva", [
            "• Evaluación específica del riesgo de caída y plan de trabajo previo al "
            "inicio (secuencia, accesos y medios auxiliares).",
            "• Medio seguro de elevación de materiales (montacargas o polea con "
            "pescante homologado) que evite retirar protecciones colectivas.",
            "• Arneses (UNE-EN 361) y puntos de anclaje (UNE-EN 795) para las tareas "
            "con protección colectiva interrumpida.",
            "• Presencia de un responsable de seguridad durante los trabajos (recurso "
            "preventivo o coordinador de trabajo en alturas, según la normativa "
            "aplicable)."],
         "1.3.2, 2.1.1"],
    ]}),
]

# ------------------------------------------- 8. conclusiones, 9. referencias
SEC8 = [
    ("h1", "9. Conclusiones"),
    ("bullets", [
        "El accidente resulta de la conjunción de dos ramas independientes: la "
        "caída (pérdida de equilibrio sobre un tablón suelto junto a un borde sin "
        "barandilla) y la falta de retención de la caída (sin arnés ni anclajes).",
        "Ambas ramas terminan en cuatro causas primarias de tipo organizativo: "
        "formación (C1), montaje (C2), inspección y supervisión (C3) y planificación "
        "preventiva (C4).",
        "C3 y C4 originan dos hechos cada una, de ramas distintas: corregirlas actúa "
        "sobre varias partes del árbol a la vez, por lo que conviene priorizarlas.",
        "Actuar solo sobre el comportamiento del trabajador no elimina las "
        "condiciones que permitieron el accidente (tablones sueltos, borde abierto, "
        "ausencia de anclajes): otro trabajador habría quedado expuesto igual.",
    ]),
]

SEC9 = [
    ("h1", "10. Referencias"),
    ("bullets", [
        "Piqué Adanuy, T. (1992). *NTP 274: Investigación de accidentes: árbol de "
        "causas.* Instituto Nacional de Seguridad e Higiene en el Trabajo (INSHT), "
        "Centro Nacional de Condiciones de Trabajo.",
        "UNE-EN 12811-1. *Equipamiento para trabajos temporales de obra. Parte 1: "
        "Andamios. Requisitos de comportamiento y diseño general.*",
        "UNE-EN 361. *Equipos de protección individual contra caídas de altura. "
        "Arneses anticaídas.*",
        "UNE-EN 795. *Protección contra caídas de altura. Dispositivos de anclaje.*",
        "España: Real Decreto 1215/1997, anexo II, modificado por el Real Decreto "
        "2177/2004 (trabajos temporales en altura).",
        "Colombia: Resolución 4272 de 2021, Ministerio del Trabajo (requisitos "
        "mínimos de seguridad para el desarrollo de trabajo en alturas).",
    ]),
]


def bloques():
    return (PORTADA + SEC1 + SEC2 + SEC3 + SEC4 + SEC5 + SEC5B + SEC6
            + SEC7 + SEC8 + SEC9)


if __name__ == "__main__":
    bs = bloques()
    print(len(bs), "bloques")
    for b in bs:
        if b[0] in ("h1", "h2"):
            print(b[0], b[1])
