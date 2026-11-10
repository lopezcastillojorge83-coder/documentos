# -*- coding: utf-8 -*-
"""Valores a escribir directamente en la hoja FORMATO FURAT del furat.xls original.

Los datos de empresa y contacto son supuestos académicos. Los códigos se diligencian para que
la entrega quede completa, aunque las casillas sombreadas las completa la ARL en una radicación real.
"""
TEXT = {
    # Encabezado y afiliaciones
    "I3": "AT-13082026-001",
    "D6": "EPS SURA",
    "X6": "EPS010",
    "AB6": "ARL SURA - SEGUROS DE VIDA SURAMERICANA S.A.",
    "AR6": "14-28",
    "Y8": "PROTECCIÓN S.A.",
    "AN8": "230201",

    # I. Empleador y centro de trabajo
    "P13": "Limpieza industrial y de aeronaves (CIIU 8129)",
    "AO13": "4812901",
    "D16": "LIMPIEZA AERONÁUTICA DEL DORADO S.A.S.",
    "AL16": "901.234.567-8",
    "D19": "Calle 25G No. 100-50, Fontibón",
    "AI19": "601 345 6789",
    "AP19": "NO APLICA",
    "D22": "sst@limpiezaaeronauticadeldorado.com.co",
    "X22": "BOGOTÁ D.C.",
    "AE21": "11",
    "AI22": "BOGOTÁ D.C.",
    "AN21": "11001",
    "AR23": "001",
    "N25": "Limpieza industrial y de aeronaves (CIIU 8129)",
    "AO25": "4812901",
    "D28": "Aeropuerto Internacional El Dorado, Av. Calle 26 No. 103-09 (plataforma)",
    "AI28": "6013456789 ext. 210",
    "AP28": "NO APLICA",
    "D30": "BOGOTÁ D.C.",
    "S29": "11",
    "W30": "BOGOTÁ D.C.",
    "AL29": "11001",

    # II. Persona accidentada
    "AT33": "N/A",
    "D36": "JIMÉNEZ",
    "P36": "JIMÉNEZ PRADO",
    "AB36": "ANDRÉS",
    "AL36": "LEONARDO",
    "R39": "1030612106121",
    "AD39": "0", "AE39": "2", "AG39": "0", "AH39": "4",
    "AJ39": "1", "AK39": "9", "AL39": "8", "AM39": "8",
    "D42": "Carrera 104 No. 23-45, Fontibón",
    "AI42": "310 555 0199",
    "AP42": "NO APLICA",
    "D45": "BOGOTÁ D.C.",
    "L44": "11",
    "P45": "BOGOTÁ D.C.",
    "Y44": "11001",
    "AI45": "Auxiliar de presentación",
    "J47": "ASEO DE AERONAVES",
    "V47": "91120",
    "AQ47": "0", "AR47": "8", "AT47": "2", "AU47": "7",
    "F50": "0", "G50": "5", "I50": "0", "J50": "5",
    "L50": "2", "M50": "0", "N50": "2", "O50": "4",
    "P50": "$ 2.000.000",

    # III. Accidente
    "E55": "1", "F55": "3", "H55": "0", "I55": "8",
    "K55": "2", "L55": "0", "M55": "2", "N55": "6",
    "V55": "0", "W55": "0", "Y55": "3", "Z55": "0",
    "AC58": "NO APLICA",
    "AR58": "N/A",
    "K62": "0", "L62": "3", "N62": "3", "O62": "0",
    "M67": "BOGOTÁ D.C.",
    "V66": "11",
    "Z67": "BOGOTÁ D.C.",
    "AI66": "11001",
    "D84": "NO APLICA",
    "AL84": "NO APLICA",
    "AI102": "NO APLICA",

    # IV. Testigos y responsable
    "X112": "NO APLICA - SIN TESTIGOS",
    "AO113": "NO APLICA",
    "X114": "NO APLICA",
    "X116": "NO APLICA - SIN TESTIGOS",
    "AO117": "NO APLICA",
    "X118": "NO APLICA",
    "X122": "TORRES RUIZ LAURA MARCELA",
    "AO123": "52.987.654",
    "X124": "Responsable del SG-SST (delegada del empleador)",
    "X126": "PENDIENTE DE FIRMA MANUSCRITA",
    "AM127": "1", "AN127": "3", "AP127": "0", "AQ127": "8",
    "AS127": "2", "AT127": "0", "AU127": "2", "AV127": "6",
}

# Casillas ActiveX a marcar con Value=1 y con su imagen estática marcada.
CHECK = [
    "CheckBox2",    # Seguro Social: NO
    "CheckBox1",    # Tipo vinculador: empleador
    "CheckBox6",    # NIT
    "CheckBox11",   # Zona sede: U
    "CheckBox15",   # Datos centro iguales: NO
    "CheckBox16",   # Zona centro: U
    "CheckBox18",   # Vinculación: planta
    "CheckBox23",   # Identificación trabajador: CC
    "CheckBox28",   # Sexo: M
    "CheckBox14",   # Zona residencia: U
    "CheckBox33",   # Jornada habitual: mixta
    "CheckBox53",   # Jornada accidente: normal
    "CheckBox55",   # Labor habitual: sí
    "CheckBox39",   # Propios del trabajo
    "CheckBox41",   # No causó muerte
    "CheckBox42",   # Zona accidente: U
    "CheckBox44",   # Dentro de la empresa
    "CheckBox57",   # Áreas de producción
    "CheckBox72",   # Conmoción o trauma interno
    "CheckBox80",   # Cabeza
    "CheckBox94",   # Aparatos
    "CheckBox102",  # Caída de personas
    "CheckBox111",  # Testigos: NO
    "CheckBox123",  # Responsable: CC
]

DESC = (
    "QUÉ: caída de persona desde un banco-escalera de lavado de aeronaves (plano de trabajo a 4,35 m) "
    "hasta el piso; golpe en la cabeza. "
    "CUÁNDO: jueves 13/08/2026, 00:30. "
    "DÓNDE: posición Golfo, plataforma del Aeropuerto El Dorado. "
    "CÓMO: limpiaba la aeronave sobre el banco, con baranda solo a la derecha; se tropezó y cayó "
    "por un borde sin baranda. Arnés Hawk 412X y eslinga en Y de 1,80 m anclada a 4,15 m, bajo sus pies; "
    "el absorbedor no se activó y el gancho tiene dañado el doble seguro. No firmó el permiso de trabajo; "
    "sin listas de chequeo del equipo. Clínica de Occidente: TCE severo, "
    "incapacidad 15 + 15 días. POR QUÉ (preliminar): bordes sin protección, anclaje bajo y "
    "detención de caídas que no tomó carga. AT GRAVE (Res. 1401/2007)."
)
