# -*- coding: utf-8 -*-
"""Datos del árbol de causas (NTP 274): caída de altura desde un andamio
durante trabajos de reparación de fachada.

Tipos de nodo:
  dano   -> daño o lesión (suceso último)
  hecho  -> hecho o condición material
  humano -> factor humano (conducta, conocimiento u omisión de control)
  causa  -> causa primaria (fallo organizativo)
"""

NODOS = {
    "0": ("dano", "ACCIDENTE: politraumatismo grave (fractura de columna "
                  "lumbar y de pelvis) del trabajador al impactar contra el suelo"),
    "1": ("hecho", "El trabajador pierde el equilibrio y cae al vacío desde "
                   "la plataforma del andamio (nivel 3, a 6 m de altura)"),
    "2": ("hecho", "Ningún sistema retiene al trabajador en caso de caída"),
    "1.1": ("humano", "El trabajador retrocede hacia el extremo de la "
                      "plataforma para valorar el paño picado (acto habitual)"),
    "1.2": ("hecho", "Los tablones del extremo están sueltos y basculan "
                     "al pisarlos"),
    "1.3": ("hecho", "El lateral del extremo de la plataforma no tiene "
                     "barandilla ni rodapié"),
    "2.1": ("hecho", "El trabajador no lleva arnés anticaídas"),
    "1.1.1": ("humano", "El trabajador desconoce el riesgo de trabajar junto "
                        "a un borde sin protección (falta de formación)"),
    "1.2.1": ("humano", "Los tablones se colocan sobre los travesaños "
                        "sin sujetarlos"),
    "1.2.2": ("humano", "No se verifica la sujeción de las plataformas "
                        "tras el montaje"),
    "1.3.1": ("humano", "No se comprueba el estado de las protecciones "
                        "del andamio antes de cada jornada"),
    "1.3.2": ("humano", "Se retira la barandilla lateral para pasar "
                        "materiales a la plataforma"),
    "2.1.1": ("hecho", "No hay arneses en la obra ni puntos de anclaje "
                       "en el andamio"),
}

# Causas primarias (fallos organizativos): no precisan una situación anterior
# para ser explicadas (criterio de finalización a) de la NTP 274).
NODOS.update({
    "C1": ("causa", "No se imparte formación ni información sobre riesgos de "
                    "trabajos en altura al personal: fallo de organización"),
    "C2": ("causa", "El montaje se encarga a personal de la obra sin "
                    "cualificación y sin plan de montaje: fallo de planificación"),
    "C3": ("causa", "No existe procedimiento ni responsable designado para "
                    "inspeccionar el andamio: falta de supervisión y control"),
    "C4": ("causa", "Planificación preventiva insuficiente: no se evalúa el "
                    "riesgo de caída ni se prevén medios seguros de elevación "
                    "de materiales ni protección individual anticaídas"),
})

# Antecedentes inmediatos de cada hecho (respuesta a: ¿qué tuvo que ocurrir
# para que este hecho se produjera?)
ANT = {
    "0": ["1", "2"],
    "1": ["1.1", "1.2", "1.3"],
    "1.1": ["1.1.1"],
    "1.1.1": ["C1"],
    "1.2": ["1.2.1", "1.2.2"],
    "1.2.1": ["C2"],
    "1.2.2": ["C3"],
    "1.3": ["1.3.1", "1.3.2"],
    "1.3.1": ["C3"],
    "1.3.2": ["C4"],
    "2": ["2.1"],
    "2.1": ["2.1.1"],
    "2.1.1": ["C4"],
}

# Posición en el dibujo: (columna, nivel). Las columnas admiten decimales.
POS = {
    "0": (4.375, 0),
    "1": (2.75, 1), "2": (6, 1),
    "1.1": (1, 2), "1.2": (2.5, 2), "1.3": (4.5, 2), "2.1": (6, 2),
    "1.1.1": (1, 3), "1.2.1": (2, 3), "1.2.2": (3, 3),
    "1.3.1": (4, 3), "1.3.2": (5, 3), "2.1.1": (6, 3),
    "C1": (1, 4), "C2": (2, 4), "C3": (3.5, 4), "C4": (5.5, 4),
}


def consecuentes(nodo):
    """Hechos de los que `nodo` es antecedente inmediato."""
    return [k for k, v in ANT.items() if nodo in v]


def relacion(hecho):
    """Tipo de relación entre un hecho y sus antecedentes (NTP 274)."""
    ants = ANT[hecho]
    if len(ants) > 1:
        return "Conjunción"
    if len(consecuentes(ants[0])) > 1:
        return "Disyunción"
    return "Cadena"


def grupos_conexion():
    """Grupos (arriba, abajo) que se dibujan con un mismo conector.

    Conjunción o cadena: un hecho arriba y sus antecedentes abajo.
    Disyunción: varios hechos arriba y el antecedente común abajo.
    """
    grupos, vistos = [], set()
    for hecho, ants in ANT.items():
        if len(ants) == 1 and len(consecuentes(ants[0])) > 1:
            if ants[0] in vistos:
                continue
            vistos.add(ants[0])
            grupos.append((consecuentes(ants[0]), ants, "disyuncion"))
        else:
            tipo = "conjuncion" if len(ants) > 1 else "cadena"
            grupos.append(([hecho], ants, tipo))
    return grupos


if __name__ == "__main__":
    # Comprobaciones de coherencia del árbol
    assert set(POS) == set(NODOS), set(POS) ^ set(NODOS)
    for h, ants in ANT.items():
        assert h in NODOS and all(a in NODOS for a in ants), h
    raices = [n for n in NODOS if n not in ANT]
    assert sorted(raices) == ["C1", "C2", "C3", "C4"], raices
    assert all(NODOS[r][0] == "causa" for r in raices)
    for h in ANT:
        print(f"{h:6} {relacion(h):11} <- {ANT[h]}")
    print("grupos:", len(grupos_conexion()))
    print("OK")
