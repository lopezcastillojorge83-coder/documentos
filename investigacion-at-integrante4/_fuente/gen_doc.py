# -*- coding: utf-8 -*-
"""Informe Word del Integrante 4: OSALAN, formatos legales, causas, plan de mejoramiento y costos ocultos."""
import os
import docxw

BUILD = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(BUILD)
FIG = os.path.join(OUT, "figuras")
DOCX = os.path.join(OUT, "02_Investigacion_OSALAN_Causas_PlanMejoramiento_Integrante4.docx")

d = docxw.Doc()
d.refs = {
    "guia": 'Universidad Distrital Francisco José de Caldas, "Guía de laboratorio: Seguridad y Salud en el Trabajo, actividad número 2," Proyecto Curricular de Ingeniería Industrial, Bogotá, Colombia, 2026.',
    "furat": 'ARL SURA, "Informe de accidente de trabajo del empleador o contratante (F 2015-PR, versión 3) e instructivo de diligenciamiento," Seguros de Vida Suramericana S.A., Colombia, s.f.',
    "dl1295": 'Presidencia de la República de Colombia, Decreto Ley 1295 de 1994, "por el cual se determinan la organización y administración del Sistema General de Riesgos Profesionales," Bogotá, Colombia, jun. 1994.',
    "res156": 'Ministerio de la Protección Social, Resolución 156 de 2005, "por la cual se adoptan los formatos de informe de accidente de trabajo y de enfermedad profesional y se dictan otras disposiciones," Bogotá, Colombia, ene. 2005.',
    "res2851": 'Ministerio del Trabajo, Resolución 2851 de 2015, "por la cual se modifica el artículo 3° de la Resolución 156 de 2005," Bogotá, Colombia, 2015.',
    "d1072": 'Ministerio del Trabajo, Decreto 1072 de 2015, "por medio del cual se expide el Decreto Único Reglamentario del Sector Trabajo," Bogotá, Colombia, may. 2015.',
    "res1401": 'Ministerio de la Protección Social, Resolución 1401 de 2007, "por la cual se reglamenta la investigación de incidentes y accidentes de trabajo," Diario Oficial 46.638, Bogotá, Colombia, may. 2007.',
    "res4272": 'Ministerio del Trabajo, Resolución 4272 de 2021, "por la cual se establecen los requisitos mínimos de seguridad para el desarrollo de trabajo en alturas," Bogotá, Colombia, dic. 2021.',
    "res0312": 'Ministerio del Trabajo, Resolución 0312 de 2019, "por la cual se definen los Estándares Mínimos del Sistema de Gestión de la Seguridad y Salud en el Trabajo SG-SST," Bogotá, Colombia, feb. 2019.',
    "ley1562": 'Congreso de la República de Colombia, Ley 1562 de 2012, "por la cual se modifica el Sistema de Riesgos Laborales y se dictan otras disposiciones en materia de salud ocupacional," Bogotá, Colombia, jul. 2012.',
    "cst": 'República de Colombia, Código Sustantivo del Trabajo (Decreto 2663 de 1950), art. 216, "Culpa del empleador," Bogotá, Colombia.',
    "ley776": 'Congreso de la República de Colombia, Ley 776 de 2002, "por la cual se dictan normas sobre la organización, administración y prestaciones del Sistema General de Riesgos Profesionales," Bogotá, Colombia, dic. 2002.',
    "osalan": "I. M. Azkoaga Bengoetxea, I. Olaciregui Garbizu y M. Silva Casal, //Manual para la investigación de accidentes laborales//, 2.ª ed. Barakaldo, España: OSALAN - Instituto Vasco de Seguridad y Salud Laborales, 2005.",
    "ntp274": "Instituto Nacional de Seguridad e Higiene en el Trabajo, //NTP 274: Investigación de accidentes: árbol de causas//. Madrid, España: INSHT, 1991.",
    "rikh": 'P. M. Rikhardsson y M. Impgaard, "Corporate cost of occupational accidents: an activity-based analysis," //Accident Analysis & Prevention//, vol. 36, no. 2, pp. 173-182, 2004, doi: 10.1016/S0001-4575(02)00147-1.',
    "jallon": 'R. Jallon, D. Imbeau y N. de Marcellis-Warin, "Development of an indirect-cost calculation model suitable for workplace use," //Journal of Safety Research//, vol. 42, no. 3, pp. 149-164, 2011.',
    "feng": 'Y. Feng, S. Zhang y P. Wu, "Factors influencing workplace accident costs of building projects," //Safety Science//, vol. 72, pp. 97-104, 2015.',
    "battaglia": 'M. Battaglia, M. Frey y E. Passetti, "Accidents at work and costs analysis: a field study in a large Italian company," //Industrial Health//, vol. 52, no. 4, pp. 354-366, 2014.',
    "heinrich": "H. W. Heinrich, //Industrial Accident Prevention: A Scientific Approach//. New York, NY, EE. UU.: McGraw-Hill, 1931.",
    "bird": "F. E. Bird y G. L. Germain, //Practical Loss Control Leadership//. Loganville, GA, EE. UU.: International Loss Control Institute, 1985.",
}

FILL_SUP = "FFF2CC"     # supuestos / hipótesis
FILL_OK = "E2EFDA"
FILL_SUB = "DDEBF7"

# ============================================================================ portada
d.p("UNIVERSIDAD DISTRITAL FRANCISCO JOSÉ DE CALDAS", align="center", bold=True, size=12, after=0)
d.p("Facultad de Ingeniería - Proyecto Curricular de Ingeniería Industrial", align="center", size=11, after=0)
d.p("Seguridad y Salud en el Trabajo - Prácticas de laboratorio 2026-3 - Actividad número 2", align="center", size=11, after=360)
d.p("Investigación del accidente de trabajo grave del 13 de agosto de 2026", style="Title", after=120)
d.p("Componente del integrante 4: metodología OSALAN (árbol de causas), formatos legales (FURAT y formato de investigación), "
    "análisis de causas, plan de mejoramiento y costos ocultos", align="center", size=12, color="1F3864", after=360)
d.p("Elaborado por: [nombre y código del integrante 4]", align="center", after=0)
d.p("Grupo: [__]   Equipo de trabajo: [__]", align="center", after=0)
d.p("Profesor: MSc., Ing. Julio Fernando Ochoa Rodriguez", align="center", after=0)
d.p("Bogotá D.C., 2026", align="center", after=360)
d.caption_tab("Ficha del evento investigado.")
d.table([
    ["Campo", "Información"],
    ["Empresa (nombre supuesto)", "LIMPIEZA AERONÁUTICA DEL DORADO S.A.S. - mantenimiento de aeronaves (lavado en seco y presentación), clase de riesgo V, 26 trabajadores en promedio, tres turnos, contratista de una gran empresa"],
    ["Trabajador", "Andrés Leonardo Jiménez Jiménez Prado, CC 1030612106121, 38 años, auxiliar de presentación, ingreso el 05/05/2024"],
    ["Fecha, hora y lugar", "Jueves 13/08/2026, 00:30 h - posición Golfo, plataforma del Aeropuerto Internacional El Dorado, Bogotá D.C."],
    ["Evento", "Caída de persona desde 4,35 m (banco-escalera/plataforma de lavado de aeronaves) con trauma craneoencefálico severo y pérdida del conocimiento"],
    ["Clasificación", "Accidente de trabajo grave (Res. 1401 de 2007, art. 3) - tarea de alto riesgo: trabajo en alturas (Res. 4272 de 2021)"],
    ["Incapacidad", "15 días iniciales + 15 días de prórroga, con posibilidad de nueva prórroga"],
    ["ARL", "ARL SURA"],
], [28, 72], bold_first_col=True)
d.p("Los nombres de la empresa, del responsable del reporte y de los integrantes del equipo investigador son supuestos del juego de "
    "roles; deben reemplazarse por los que defina el grupo para que coincidan con la cotización y con los demás numerales del informe.",
    size=9, italic=True, color="595959")

# ============================================================================ 1
d.section(False)   # mantiene vertical; separa la portada como sección propia
d.h("1. Alcance, fuentes y verificación de los datos del caso", 1)
d.h("1.1 Alcance", 2)
d.p("Este documento desarrolla los cinco entregables asignados al integrante 4 dentro de la actividad 2 {c:guia}:")
d.bullets([
    "FURAT de ARL SURA diligenciado con los datos del accidente del 13/08/2026 a las 00:30 {c:furat} (Anexo A, archivo Excel).",
    "Investigación con una metodología del manual de OSALAN {c:osalan}: método del árbol de causas, con diagramas, pasos e hipótesis (sección 4).",
    "Identificación y clasificación de las causas inmediatas y básicas dentro del formato de investigación exigido por la Resolución 1401 de 2007 {c:res1401} (sección 5).",
    "Plan de mejoramiento con las medidas correctivas y preventivas (sección 6).",
    "Tres artículos científicos Q1 que definen los costos ocultos de los accidentes de trabajo, con su aplicación al caso (sección 7 y Anexo B).",
], kind="number")
d.p("Fuentes de información: la guía de laboratorio (datos del trabajador y del accidente, fichas técnicas del arnés y de la eslinga, "
    "registro fotográfico del banco, la eslinga, el gancho y la atención en el sitio), el formato FURAT de ARL SURA y su instructivo, "
    "y la normatividad citada. Se aplica el criterio que pide la guía: tener claros los hechos antes que hacer suposiciones. Por eso, "
    "todo lo que no está comprobado se presenta como hipótesis y se indica cómo verificarlo.")

d.h("1.2 Verificación de consistencia de los datos del caso", 2)
d.p("Antes de diligenciar los formatos se revisó la coherencia de los datos de la guía. La Tabla 2 resume las inconsistencias "
    "encontradas y el tratamiento dado. El grupo debe usar el mismo tratamiento en todos los numerales del informe.")
d.caption_tab("Inconsistencias o vacíos de información en los datos del caso y tratamiento aplicado.")
d.table([
    ["Dato", "Lo que indica la guía", "Inconsistencia o vacío", "Tratamiento en este documento"],
    ["Turno del accidente", "Salió a las 05:00 del 13/08 y volvió a las 21:00 del 13/08; accidente a las 00:30 del 13/08 con 3 h 30 min laboradas.",
     "Si el turno empezó el 13/08 a las 21:00, el accidente habría ocurrido el 14/08 a las 00:30.",
     "Se conserva la fecha oficial del accidente (13/08/2026, 00:30) y se ubica el turno anterior el 12/08 (05:00) y el ingreso el 12/08 a las 21:00. Confirmar con control de acceso o nómina."],
    ["Clínica", "Campo: Clínica de Occidente. Nota: Clínica de Oriente.", "Dos nombres distintos.", "Se usa Clínica de Occidente; confirmar con la historia clínica."],
    ["Nombre", "Andrés Leonardo Jiménez Jiménez Prado.", "Aparecen tres apellidos.", "Se transcribe completo (primer apellido Jiménez, segundo apellido Jiménez Prado); verificar con la cédula."],
    ["Proceso", "Actividad de la empresa: lavado en seco. Tarea: limpieza en húmedo.", "La tarea difiere del proceso registrado.", "Se registra como hecho y se plantea la hipótesis H4 (superficie húmeda u objetos sobre el banco)."],
    ["Norma del equipo", "ANSI 3359.1.", "Referencia inexistente; probablemente ANSI Z359.1.", "Solicitar los certificados del fabricante del arnés y de la eslinga."],
    ["Peso del trabajador", "No se indica.", "Se requiere para el cálculo de energía.", "Se asume 70 kg; ajustar al valor que defina el grupo."],
    ["Tiempo de ocupación", "Aparece como \"¿?\".", "Debe calcularse.", "Del 05/05/2024 al 13/08/2026: 2 años, 3 meses y 8 días (27 meses y 8 días; 830 días)."],
    ["Licencia para investigar", "La empresa \"no tiene persona con licencia\", pero el responsable del SG-SST tiene licencia en salud ocupacional.",
     "El responsable del SG-SST es también el coordinador TSA que firmó el permiso de trabajo.",
     "Por independencia, la investigación la lidera el profesional externo con licencia (consultoría); el responsable del SG-SST participa como integrante e informante."],
], [15, 27, 25, 33], size=8)

# ============================================================================ 2
d.h("2. Marco legal aplicado en este componente", 1)
d.caption_tab("Requisitos legales que se aplican al reporte, la investigación y las medidas.")
d.table([
    ["Norma", "Requisito", "Aplicación en el caso"],
    ["Decreto Ley 1295 de 1994, art. 62 {c:dl1295}; Res. 156 de 2005 {c:res156}, modificada por la Res. 2851 de 2015 {c:res2851}",
     "Reportar el accidente a la ARL y a la EPS en el FURAT dentro de los 2 días hábiles siguientes y entregar copia al trabajador.",
     "FURAT diligenciado el 13/08/2026 (Anexo A). Plazo máximo: martes 18/08/2026, porque el lunes 17/08/2026 es festivo."],
    ["Decreto 1072 de 2015, art. 2.2.4.1.7 {c:d1072}",
     "Reportar los accidentes graves y mortales a la Dirección Territorial del Ministerio del Trabajo dentro de los 2 días hábiles siguientes.",
     "Aplica: el trauma craneoencefálico hace que el accidente sea grave. Mismo plazo (18/08/2026)."],
    ["Res. 1401 de 2007, art. 3 {c:res1401}",
     "Definiciones de accidente grave (incluye trauma craneoencefálico), causas inmediatas y causas básicas.",
     "Clasifica el evento como grave y orienta el análisis causal de la sección 5."],
    ["Res. 1401 de 2007, art. 4",
     "Investigar todos los incidentes y accidentes dentro de los 15 días siguientes; remitir a la ARL la investigación de los accidentes graves y mortales; adoptar metodología y formato; implementar las medidas.",
     "Fecha límite tomada con criterio conservador: 28/08/2026 (15 días calendario)."],
    ["Res. 1401 de 2007, art. 7",
     "Conformación del equipo investigador. En accidentes graves debe participar un profesional con licencia en salud ocupacional, propio o contratado, y personal de diseño o mantenimiento.",
     "Equipo con consultor externo con licencia (juego de roles, sección 5.2)."],
    ["Res. 1401 de 2007, arts. 10 a 13",
     "Contenido del informe: descripción del accidente, causas y compromiso de adopción de medidas de intervención.",
     "Secciones 5 y 6."],
    ["Decreto 1072 de 2015, arts. 2.2.4.6.32 y 2.2.4.6.33",
     "Investigación de incidentes, accidentes y enfermedades laborales dentro del SG-SST; acciones preventivas y correctivas.",
     "Plan de mejoramiento con responsables, fechas y verificación de eficacia."],
    ["Decreto 1072 de 2015, art. 2.2.4.6.24",
     "Jerarquía de controles: eliminación, sustitución, controles de ingeniería, controles administrativos y elementos de protección personal.",
     "Orden de prioridad de las medidas de la sección 6."],
    ["Res. 4272 de 2021 {c:res4272}",
     "Requisitos mínimos para trabajo en alturas (riesgo de caída mayor a 2,0 m): programa de prevención y protección contra caídas, permiso de trabajo, roles (coordinador, persona calificada), anclajes de al menos 5.000 lb (22,2 kN) por trabajador, inspección de equipos y requerimiento de claridad.",
     "Referencia técnica de las causas y de las medidas (secciones 4 a 6)."],
    ["Res. 0312 de 2019, estándar 3.2.2 {c:res0312}",
     "Investigación de incidentes, accidentes de trabajo y enfermedades laborales como estándar mínimo del SG-SST.",
     "Evidencia de cumplimiento del estándar."],
    ["Ley 1562 de 2012, art. 13 {c:ley1562}; Código Sustantivo del Trabajo, art. 216 {c:cst}",
     "Sanciones por incumplimiento de las normas de SST; indemnización plena de perjuicios cuando se compruebe culpa del empleador.",
     "Riesgo legal y costos ocultos (sección 7)."],
], [26, 42, 32], size=8)

# ============================================================================ 3
d.h("3. FURAT diligenciado (formato ARL SURA)", 1)
d.p("El FURAT completo está en el archivo **01_FURAT_ARL_SURA_AT_13-08-2026_diligenciado.xlsx** (Anexo A). La hoja \"FURAT\" "
    "reproduce el formato F 2015-PR versión 3 de ARL SURA {c:furat} con todas sus secciones: afiliación (EPS, ARL, AFP), I. identificación "
    "del empleador, II. información de la persona accidentada, III. información sobre el accidente y IV. descripción del accidente. "
    "La hoja \"Notas y supuestos\" documenta la fuente de cada dato. Las casillas sombreadas se dejaron en blanco porque son de uso "
    "exclusivo de la ARL. La Tabla 4 resume las decisiones de clasificación que requieren justificación.")
d.caption_tab("Clasificaciones del FURAT y su justificación según el instructivo de ARL SURA.")
d.table([
    ["Campo del FURAT", "Registro", "Justificación"],
    ["Tipo de vinculador / vinculación", "(1) Empleador / (1) Planta", "Trabajador directo de la empresa contratista."],
    ["Día de la semana", "JU (jueves)", "El 13/08/2026 fue jueves."],
    ["Jornada habitual / jornada en que sucede", "(3) Mixto / (1) Normal", "La guía indica jornada mixta con turno rotativo; el evento ocurrió dentro del turno, tras 3 h 30 min laboradas."],
    ["Tiempo de ocupación habitual", "27 meses y 8 días", "Calculado desde el ingreso (05/05/2024); se asume igual a la experiencia en el oficio."],
    ["Tipo de accidente", "(5) Propios del trabajo", "Ejecutaba sus funciones; no hubo vehículo en movimiento, violencia ni actividad deportiva o recreativa."],
    ["Lugar y sitio", "(1) Dentro de la empresa / (2) Áreas de producción", "Ocurrió en el centro de trabajo donde la empresa presta su servicio. El instructivo incluye en áreas de producción las instalaciones al aire libre, los andamios y el área de producción de servicios."],
    ["Tipo de lesión", "(30) Conmoción o trauma interno", "Historia clínica de ingreso: trauma craneoencefálico severo con pérdida del conocimiento."],
    ["Parte del cuerpo", "(1) Cabeza", "Dato del caso."],
    ["Agente", "(3) Aparatos", "El instructivo ubica las escaleras móviles, rampas móviles y andamios en \"Aparatos\" y los excluye de \"Ambiente de trabajo\". El banco-plataforma de lavado es un equipo de acceso móvil."],
    ["Mecanismo", "(1) Caída de personas", "Caída a diferente nivel desde 4,35 m."],
    ["Testigos", "No", "La indagación preliminar solo registra la versión del trabajador; si se identifican testigos, se actualiza el reporte."],
    ["Fecha de diligenciamiento", "13/08/2026", "Dentro de las 48 horas que pide la guía y de los 2 días hábiles legales."],
], [26, 26, 48], size=8.5, bold_first_col=True)

# ============================================================================ 4
d.h("4. Investigación con la metodología OSALAN: método del árbol de causas", 1)
d.h("4.1 Selección y justificación del método", 2)
d.p("El //Manual para la investigación de accidentes laborales// de OSALAN (2.ª ed., 2005) {c:osalan} plantea una investigación basada "
    "en hechos objetivos, orientada a encontrar causas y no culpables, y actualizada con las variables del Sistema Europeo de Estadísticas "
    "de Accidentes de Trabajo (ESAW). De las metodologías del manual se seleccionó el **método del árbol de causas** {c:osalan,ntp274}, por "
    "cuatro razones:")
d.bullets([
    "Representa gráficamente la cadena de hechos que produjo el accidente y muestra su carácter multicausal.",
    "Obliga a separar los hechos comprobados de las hipótesis, que es lo que pide la guía.",
    "Permite remontarse desde la lesión hasta las causas de gestión (programa de protección contra caídas, supervisión, compras), que corresponden a las causas básicas de la Res. 1401 de 2007 {c:res1401}.",
    "Cada causa identificada se traduce en una medida concreta del plan de mejoramiento.",
])
d.h("4.2 Pasos aplicados", 2)
d.caption_tab("Pasos del método del árbol de causas aplicados al caso.")
d.table([
    ["Paso", "Qué se hace", "Aplicación y producto"],
    ["1. Toma de datos", "Recoger la información lo antes posible y en el lugar del accidente, sin buscar culpables: inspección, fotografías, entrevistas individuales y documentos.",
     "Fuentes usadas: descripción del caso, fichas técnicas, registro fotográfico, permiso de trabajo e historia clínica. Pendientes: entrevista al trabajador cuando su estado lo permita, entrevistas a los operarios del turno y al coordinador TSA, video del CCTV del operador aeroportuario, medición de iluminancia e inspección del banco."],
    ["2. Lista de hechos", "Redactar hechos concretos y verificables, sin juicios, por componente de la situación de trabajo: individuo (I), tarea (T), material (M) y medio de trabajo (MT); marcar si son habituales o inhabituales.",
     "Tabla 6 (17 hechos)."],
    ["3. Construcción del árbol", "Partir de la lesión y retroceder preguntando para cada hecho: ¿qué tuvo que ocurrir para que se produjera?, ¿fue necesario?, ¿fue suficiente? Las respuestas dan relaciones de encadenamiento, conjunción, disyunción o independencia.",
     "Figura 2 (18 nodos)."],
    ["4. Hipótesis", "Cuando un antecedente necesario no está comprobado, se formula como hipótesis, se dibuja con borde discontinuo y se define cómo verificarla o descartarla.",
     "Tabla 7 (seis hipótesis) y cálculo de verificación (Tabla 8, Figura 3)."],
    ["5. Identificación y selección de causas", "Clasificar los antecedentes del árbol como causas inmediatas (actos y condiciones subestándar) y causas básicas (factores personales y del trabajo); seleccionar como principales las que, eliminadas, habrían evitado el accidente.",
     "Sección 4.8 y formato de investigación (sección 5.4)."],
    ["6. Medidas y seguimiento", "Proponer al menos una medida por causa principal, priorizada con la jerarquía de controles, con responsable, fecha e indicador.",
     "Plan de mejoramiento (sección 6)."],
], [19, 41, 40], size=8.5, bold_first_col=True)

d.h("4.3 Secuencia cronológica del evento", 2)
d.p("La Figura 1 ordena los hechos en el tiempo, desde el turno anterior hasta los plazos legales de reporte e investigación.")
d.image(os.path.join(FIG, "fig1_secuencia_cronologica.png"), 14.5, "Secuencia cronológica del accidente")
d.caption_fig("Secuencia cronológica del accidente del 13/08/2026. Fuente: elaboración propia con datos de la guía {c:guia}.")

d.h("4.4 Lista de hechos", 2)
d.caption_tab("Lista de hechos del accidente (I: individuo, T: tarea, M: material, MT: medio de trabajo).")
d.table([
    ["N.º", "Hecho", "Comp.", "Tipo", "Fuente"],
    ["F01", "Trabajador de 38 años, auxiliar de presentación, con 2 años, 3 meses y 8 días en la empresa.", "I", "Habitual", "Datos del trabajador"],
    ["F02", "Certificación vigente en trabajo seguro en alturas nivel avanzado y concepto médico ocupacional de aptitud.", "I", "Habitual", "Guía"],
    ["F03", "Turno iniciado a las 21:00; 3 h 30 min laboradas al momento del evento; descanso previo de 16 h.", "T", "Habitual", "Datos del accidente"],
    ["F04", "Realizaba limpieza en húmedo de una aeronave a 4,35 m sobre el plano de referencia (la actividad registrada de la empresa es lavado en seco).", "T", "Por verificar", "Descripción del caso"],
    ["F05", "Posición Golfo, plataforma del Aeropuerto Internacional El Dorado, en horario nocturno (00:30) con iluminación artificial.", "MT", "Habitual", "Guía y fotografías"],
    ["F06", "El banco-escalera/plataforma tiene baranda solo en el lado derecho; los lados izquierdo y frontal no tienen baranda.", "M", "Habitual", "Guía y fotografías"],
    ["F07", "El punto de anclaje está a 4,15 m, 0,20 m por debajo del plano de trabajo (4,35 m).", "M", "Habitual", "Guía"],
    ["F08", "Arnés de cuerpo entero Hawk 412X, serie 4123640140102712, fabricado el 13/01/2014, capacidad 140 kg: cumple requisitos.", "M", "Habitual", "Ficha técnica"],
    ["F09", "Eslinga en Y Hawk 412X de 1,80 m con absorbedor (1,07 m), serie 6710180130904536, fabricada el 23/09/2013 y adquirida el 22/04/2023: el absorbedor no se activó y el gancho de 1-1/4\" tiene dañado el mecanismo de doble seguro.", "M", "Inhabitual", "Ficha técnica y fotografía"],
    ["F10", "El permiso de trabajo está firmado por el coordinador TSA y por los demás operarios del turno, pero no por el accidentado.", "T", "Inhabitual", "Guía"],
    ["F11", "No se evidencia lista de chequeo (inspección pre-uso) del arnés, la eslinga ni el banco.", "T", "Habitual", "Guía"],
    ["F12", "La empresa tiene programa de SST y responsable del SG-SST con licencia, curso de 50 h y curso de coordinador TSA de 80 h.", "MT", "Habitual", "Guía"],
    ["F13", "Hay procedimientos de limpieza, pero no existe programa de prevención y protección contra caídas de personas y objetos.", "MT", "Habitual", "Guía"],
    ["F14", "Según la versión del trabajador, se tropezó sobre el banco y cayó.", "I", "Inhabitual", "Indagación preliminar"],
    ["F15", "Cayó desde 4,35 m hasta el piso de la plataforma y recibió atención en el sitio.", "I", "Inhabitual", "Guía y fotografía"],
    ["F16", "Diagnóstico de ingreso: trauma craneoencefálico severo con pérdida del conocimiento; incapacidad de 15 + 15 días, prorrogable.", "I", "Inhabitual", "Historia clínica"],
    ["F17", "Empresa de 26 trabajadores, tres turnos, clase de riesgo V y contratista de una gran empresa.", "MT", "Habitual", "Guía"],
], [7, 59, 7, 11, 16], size=8, col_align=["center", None, "center", "center", None])

# ---------------------------------------------------------------- árbol (horizontal)
d.section(True)
d.h("4.5 Árbol de causas", 2)
d.image(os.path.join(FIG, "fig2_arbol_de_causas.png"), 23.8, "Árbol de causas del accidente")
d.caption_fig("Árbol de causas del accidente de trabajo del 13/08/2026 (método OSALAN). Fuente: elaboración propia {c:osalan,ntp274}.")
d.section(False)

d.p("**Lectura del árbol.** El árbol se lee de izquierda (antecedentes) a derecha (lesión). La caída de 4,35 m (B) requirió la "
    "conjunción de tres hechos: el tropiezo sobre el banco (D), los lados izquierdo y frontal del banco sin baranda (E) y la falla del "
    "sistema de detención, que se evidencia porque el absorbedor no se activó (F). Si cualquiera de los tres no hubiera existido, el "
    "accidente no se habría producido o no habría tenido esta gravedad.")
d.p("El hecho F tiene dos explicaciones posibles que se mantienen como hipótesis: el trabajador no estaba conectado (H1) o el gancho "
    "con el doble seguro dañado se abrió o se zafó (H2). Las dos ramas llegan a causas de gestión comunes: no existe programa de "
    "prevención y protección contra caídas (J), el permiso se avaló sin verificar firmas ni condiciones (N) y no hay inspección pre-uso "
    "ni control de vida útil de los equipos (I, O, P). Además, aunque el trabajador hubiera estado bien conectado, el anclaje ubicado "
    "0,20 m por debajo de sus pies (K) y la falta de claridad (M) no habrían evitado el impacto contra el piso (sección 4.6).")

d.h("4.6 Formulación y verificación de hipótesis", 2)
d.caption_tab("Hipótesis del árbol de causas, evidencias y forma de verificación.")
d.table([
    ["Hipótesis", "Evidencia a favor", "Evidencia en contra", "Cómo verificarla", "Estado"],
    ["H1. El trabajador no estaba conectado al punto de anclaje en el momento de la caída.",
     "El absorbedor no se activó (F09); permiso sin su firma (F10); sin inspección pre-uso (F11); el anclaje bajo los pies (F07) hace poco útil la conexión.",
     "No hay evidencia directa.",
     "Entrevista al trabajador cuando su estado lo permita y a los operarios del turno; posición en que quedaron la eslinga y los ganchos; video CCTV de la plataforma; marcas en el anclaje.",
     "Probable, por confirmar"],
    ["H2. Estaba conectado, pero el gancho de 1-1/4\" con el doble seguro dañado se abrió o se zafó durante la caída.",
     "Daño documentado del gancho (F09); el absorbedor no tomó carga.",
     "No se sabe si el daño era previo o se produjo en la caída.",
     "Inspección del gancho por persona calificada o por el fabricante; análisis de marcas y deformaciones; entrevistas.",
     "Posible, por confirmar"],
    ["H3. El sistema de detención actuó, pero por falta de claridad el trabajador impactó el piso.",
     "Claridad requerida 5,09 m frente a 4,15 m disponibles; factor de caída 1,86 (Tabla 8).",
     "Si la eslinga hubiera tomado carga, el absorbedor se habría desplegado.",
     "Inspección del absorbedor por persona calificada.",
     "Descartada como mecanismo; confirmada como condición latente (K, M)"],
    ["H4. Superficie del banco húmeda o con mangueras e insumos que provocaron el tropiezo.",
     "Limpieza en húmedo (F04); versión de tropiezo (F14).",
     "No se registró el estado de la superficie después del evento.",
     "Inspección del banco (superficie antideslizante, peldaños, rejilla); revisión del procedimiento de limpieza; entrevistas.",
     "Posible, por verificar"],
    ["H5. Iluminación insuficiente en la posición Golfo durante el turno nocturno.",
     "Evento a las 00:30 con iluminación artificial (F05).",
     "El registro fotográfico muestra el banco iluminado.",
     "Medición de iluminancia con luxómetro en la posición y a la misma hora.",
     "Por verificar"],
    ["H6. Fatiga o somnolencia por el trabajo nocturno.",
     "Hora del evento (00:30) y turnos rotativos.",
     "Descanso previo de 16 h, 3 h 30 min laboradas y concepto médico de aptitud.",
     "Entrevista sobre el sueño previo y revisión de la programación de turnos.",
     "Poco probable (no se incluye en el árbol)"],
], [21, 22, 17, 25, 15], size=7.5, fills={(3, 4): FILL_OK, (6, 4): "EDEDED"})
d.p("**Cálculo de verificación de H3.** Se calcularon la caída real (sin detención) y el comportamiento teórico del sistema si el "
    "trabajador hubiera estado conectado al anclaje existente. La Resolución 4272 de 2021 exige determinar el requerimiento de "
    "claridad antes de la tarea {c:res4272}; para calcularlo se usa la fórmula habitual en la formación en alturas, medida desde el "
    "punto de anclaje: longitud de la eslinga (LE) + elongación del absorbedor (DA) + estatura del trabajador (E) + factor de "
    "seguridad (FS, mínimo 0,60 m).")
d.caption_tab("Datos, supuestos y resultados del cálculo de caída libre y requerimiento de claridad.")
d.table([
    ["Concepto", "Cálculo", "Resultado"],
    ["Datos del caso", "Plano de trabajo 4,35 m; anclaje 4,15 m; estatura 1,62 m; eslinga 1,80 m; elongación máxima del absorbedor 1,07 m", "-"],
    ["Supuestos", "Masa 70 kg; altura del anillo D sobre los pies de aproximadamente 1,35 m (0,83 × estatura); FS = 0,60 m; g = 9,81 m/s²", "-"],
    ["Caída real: tiempo", "t = √(2h/g) = √(2 × 4,35 / 9,81)", "0,94 s"],
    ["Caída real: velocidad al impacto", "v = √(2gh) = √(2 × 9,81 × 4,35)", "9,24 m/s (33,3 km/h)"],
    ["Caída real: energía al impacto", "E = m·g·h = 70 × 9,81 × 4,35", "2,99 kJ"],
    ["Caída libre potencial si estaba conectado", "CL = altura anillo D + desnivel anclaje-pies + LE = 1,35 + 0,20 + 1,80", "3,35 m (mayor que el máximo de 1,80 m para el que está diseñada la eslinga con absorbedor)"],
    ["Factor de caída", "FC = CL / LE = 3,35 / 1,80", "1,86"],
    ["Requerimiento de claridad bajo el anclaje", "RC = LE + DA + E + FS = 1,80 + 1,07 + 1,62 + 0,60", "5,09 m"],
    ["Claridad disponible bajo el anclaje", "Altura del anclaje sobre el piso", "4,15 m: déficit de 0,94 m"],
    ["Posición final teórica de los pies", "4,15 - 1,80 - 1,07 - 1,35", "-0,07 m (por debajo del piso: habría impacto)"],
], [27, 43, 30], size=8, bold_first_col=True, fills={(9, 2): "FCE4D6", (10, 2): "FCE4D6", (6, 2): "FCE4D6"})
d.image(os.path.join(FIG, "fig3_esquema_claridad.png"), 16.2, "Esquema de alturas y requerimiento de claridad")
d.caption_fig("Esquema de alturas, caída libre y requerimiento de claridad. Fuente: elaboración propia con datos de la guía {c:guia}.")
d.p("**Conclusión del cálculo.** La configuración del sistema no protegía al trabajador aunque estuviera conectado: la caída libre "
    "potencial (3,35 m) supera el límite de diseño de la eslinga y la claridad disponible es 0,94 m menor que la requerida. Esto confirma "
    "una condición subestándar latente (K, M), independiente de la hipótesis que explique por qué la eslinga no tomó carga. Si el grupo "
    "desarrolla el cálculo de caída libre en otro numeral, debe unificar la masa y la altura del anillo D con estos valores.")

d.h("4.7 Variables del sistema europeo ESAW incorporadas en el manual OSALAN", 2)
d.caption_tab("Codificación descriptiva del accidente según las variables ESAW.")
d.table([
    ["Variable", "Registro para este accidente"],
    ["Tipo de lugar y de trabajo", "Plataforma aeroportuaria (exterior); limpieza de aeronaves en turno nocturno"],
    ["Actividad física específica", "Trabajar y desplazarse a pie sobre un banco-plataforma a 4,35 m"],
    ["Desviación", "Tropiezo y pérdida de equilibrio que termina en la caída de la persona desde altura"],
    ["Forma de contacto (modalidad de la lesión)", "Golpe de la cabeza contra el piso al final de la caída (choque contra un objeto inmóvil)"],
    ["Agente material de la desviación", "Banco-escalera/plataforma móvil para lavado de aeronaves"],
    ["Agente material del contacto", "Superficie de la plataforma (piso)"],
], [35, 65], size=8.5, bold_first_col=True)

d.h("4.8 Causas principales seleccionadas", 2)
d.p("Se seleccionaron como causas principales las que, eliminadas, habrían evitado el accidente o reducido su gravedad, y que pueden "
    "originar otros accidentes en la operación:")
d.bullets([
    "**Ausencia del programa de prevención y protección contra caídas (J):** no se identificaron ni controlaron los bordes abiertos, la ubicación del anclaje ni la claridad.",
    "**Equipo de acceso sin protección colectiva en dos lados (E).**",
    "**Sistema de detención mal configurado:** anclaje por debajo del plano de trabajo y claridad insuficiente (K, M).",
    "**Control deficiente del permiso de trabajo y de la supervisión (L, N).**",
    "**Ausencia de inspección pre-uso y de control de vida útil de los equipos (I, O, P).**",
], kind="number")

# ============================================================================ 5
d.h("5. Formato de investigación del accidente de trabajo (Resolución 1401 de 2007)", 1)
d.p("Este formato contiene los elementos mínimos que exige la Resolución 1401 de 2007 {c:res1401}: datos generales, equipo "
    "investigador, descripción del accidente, análisis de causas inmediatas y básicas y compromiso de medidas de intervención.")
d.h("5.1 Datos generales", 2)
d.caption_tab("Formato de investigación - datos generales.")
d.table([
    ["Campo", "Información"],
    ["Empresa (supuesta)", "LIMPIEZA AERONÁUTICA DEL DORADO S.A.S. - NIT 901.234.567-8 - ARL SURA"],
    ["Actividad y clase de riesgo", "Mantenimiento de aeronaves (lavado en seco y presentación) - clase V; 26 trabajadores; tres turnos"],
    ["Centro de trabajo", "Operación en plataforma, Aeropuerto Internacional El Dorado, Bogotá D.C. (contratista de una gran empresa)"],
    ["Trabajador", "Andrés Leonardo Jiménez Jiménez Prado - CC 1030612106121 - 38 años"],
    ["Cargo y funciones", "Auxiliar de presentación: limpieza y aseo de aeronaves según el procedimiento de cada servicio"],
    ["Antigüedad", "Ingreso el 05/05/2024: 2 años, 3 meses y 8 días al momento del accidente"],
    ["Formación en alturas y aptitud", "Certificación vigente nivel avanzado; concepto médico ocupacional apto"],
    ["Fecha, hora y lugar", "Jueves 13/08/2026, 00:30 h - posición Golfo, plataforma del Aeropuerto Internacional El Dorado"],
    ["Jornada", "Turno nocturno iniciado a las 21:00 (3 h 30 min laboradas); descanso previo de 16 h"],
    ["Lesión", "Trauma craneoencefálico severo con pérdida del conocimiento (Clínica de Occidente); incapacidad 15 + 15 días, prorrogable"],
    ["Clasificación", "Accidente de trabajo grave (Res. 1401 de 2007, art. 3)"],
    ["Reportes", "FURAT a ARL y EPS: 13/08/2026 (plazo 18/08/2026). Dirección Territorial del Ministerio del Trabajo: plazo 18/08/2026"],
    ["Plazo de investigación y remisión a la ARL", "15 días desde el evento: 28/08/2026 (criterio conservador)"],
], [30, 70], size=8.5, bold_first_col=True)

d.h("5.2 Equipo investigador", 2)
d.p("Como el accidente es grave, el equipo incluye un profesional con licencia en SST y personal de diseño o mantenimiento "
    "(Res. 1401 de 2007, art. 7). Los nombres corresponden al juego de roles del grupo.")
d.caption_tab("Equipo investigador (juego de roles).")
d.table([
    ["Rol (Res. 1401 de 2007, art. 7)", "Cargo", "Nombre", "Licencia SST", "Firma"],
    ["Profesional con licencia en SST, líder de la investigación (externo)", "Consultor externo", "[Integrante __]", "N.º [__]", ""],
    ["Jefe inmediato o supervisor del trabajador", "Supervisor de operaciones del turno nocturno", "[Integrante __]", "No aplica", ""],
    ["Representante del COPASST", "Representante de los trabajadores", "[Integrante __]", "No aplica", ""],
    ["Responsable del SG-SST (participa e informa; firmó el permiso como coordinador TSA)", "Responsable del SG-SST y coordinador TSA", "[Integrante __]", "N.º [__]", ""],
    ["Personal de diseño o mantenimiento", "Jefe de mantenimiento de equipos de acceso o persona calificada del proveedor de equipos", "[Por designar]", "No aplica", ""],
], [30, 25, 17, 13, 15], size=8)
d.p("Anexar al informe final la copia de la licencia en SST del profesional que lidera la investigación (juego de roles).",
    size=9, italic=True, color="595959")

d.h("5.3 Descripción detallada del accidente", 2)
d.p("**¿Qué pasó?** Caída de persona desde un banco-escalera/plataforma de lavado de aeronaves, desde 4,35 m hasta el plano de "
    "referencia, con golpe de la cabeza contra el piso.")
d.p("**¿Cuándo?** Jueves 13/08/2026, aproximadamente a las 00:30, tras 3 h 30 min de un turno iniciado a las 21:00.")
d.p("**¿Dónde?** Posición Golfo, plataforma del Aeropuerto Internacional El Dorado (Bogotá D.C.), en horario nocturno con "
    "iluminación artificial.")
d.p("**¿Cómo?** El trabajador realizaba limpieza en húmedo de una aeronave sobre el banco, que tenía baranda solo en el lado derecho. "
    "Según su versión, se tropezó y cayó. Portaba arnés de cuerpo entero y eslinga en Y con absorbedor de 1,80 m; el punto de anclaje "
    "estaba a 4,15 m, por debajo del plano de trabajo. El absorbedor no se activó y el gancho de 1-1/4\" presentaba dañado el mecanismo "
    "de doble seguro. El permiso de trabajo no tenía su firma y no hubo inspección pre-uso de los equipos. Recibió atención en el sitio "
    "y fue trasladado a la Clínica de Occidente, donde se diagnosticó trauma craneoencefálico severo con pérdida del conocimiento.")
d.p("**¿Por qué?** El banco no tenía protección colectiva en los lados por donde era posible caer; el sistema de detención no tomó "
    "carga, por no estar conectado o porque el gancho se abrió (hipótesis en verificación); y, aun conectado, el anclaje bajo los pies "
    "y la falta de claridad no habrían evitado el impacto. Estas condiciones se originan en la ausencia del programa de prevención y "
    "protección contra caídas, en un control deficiente del permiso de trabajo y en la falta de inspección de los equipos.")

d.h("5.4 Análisis de causas", 2)
d.p("Las causas se clasifican según las definiciones del artículo 3 de la Resolución 1401 de 2007 {c:res1401}: las causas "
    "inmediatas son los actos y condiciones subestándar que se presentan justo antes del contacto; las causas básicas son los factores "
    "personales y del trabajo que explican por qué existieron esos actos y condiciones. Cada causa se relaciona con los nodos del "
    "árbol (Figura 2). Las filas sombreadas son hipótesis por confirmar.")
d.caption_tab("Causas inmediatas.")
d.table([
    ["N.º", "Causa", "Categoría", "Evidencia / nodo", "Estado"],
    ["", "ACTOS SUBESTÁNDAR", "", "", ""],
    ["AS1", "Iniciar el trabajo en alturas sin firmar el permiso de trabajo (no participó en la verificación de peligros y controles).", "Operar sin autorización; no seguir el procedimiento", "F10 / L", "Comprobada"],
    ["AS2", "Usar el arnés, la eslinga y el banco sin inspección pre-uso.", "Usar equipo sin verificar su estado", "F11, F09 / I, O", "Comprobada"],
    ["AS3", "No permanecer conectado al punto de anclaje mientras trabajaba sobre el banco.", "Uso inadecuado del equipo de protección personal", "F09 / H1", "Hipótesis"],
    ["AS4", "Desplazarse cerca de un borde sin baranda sobre una superficie posiblemente húmeda u obstruida.", "Adoptar una posición o ubicación insegura", "F04, F06, F14 / D, E, H4", "Hipótesis parcial"],
    ["AS5", "Avalar el permiso sin verificar la firma de todos los ejecutantes ni las condiciones del sitio (anclaje, claridad, barandas) - acto del supervisor.", "No asegurar ni advertir", "F10 / N", "Comprobada"],
    ["", "CONDICIONES SUBESTÁNDAR", "", "", ""],
    ["CS1", "Banco-plataforma con baranda solo en el lado derecho; bordes izquierdo y frontal abiertos a 4,35 m.", "Protecciones o barreras inadecuadas", "F06 / E", "Comprobada"],
    ["CS2", "Anclaje a 4,15 m, 0,20 m por debajo del plano de trabajo: caída libre potencial de 3,35 m (factor 1,86) y claridad requerida de 5,09 m frente a 4,15 m disponibles.", "Sistema de protección contra caídas inadecuado", "F07 + Tabla 8 / K, M", "Comprobada"],
    ["CS3", "Eslinga con el gancho de 1-1/4\" con doble seguro dañado y absorbedor sin activación; fabricada en 2013.", "Equipo de protección defectuoso", "F09 / H2, O, P", "Comprobada (momento del daño por verificar)"],
    ["CS4", "Superficie del banco húmeda u obstruida por la limpieza en húmedo.", "Superficie resbaladiza; orden y aseo deficientes", "F04 / H4", "Hipótesis"],
    ["CS5", "Posible iluminación insuficiente en el turno nocturno.", "Iluminación deficiente", "F05 / H5", "Hipótesis"],
], [7, 42, 21, 15, 15], size=8, full_rows={1: ("Actos subestándar (actos inseguros)", FILL_SUB), 7: ("Condiciones subestándar (condiciones inseguras)", FILL_SUB)},
    fills={(4, None): FILL_SUP, (5, None): FILL_SUP, (11, None): FILL_SUP, (12, None): FILL_SUP},
    col_align=["center", None, None, None, None])
d.caption_tab("Causas básicas.")
d.table([
    ["N.º", "Causa", "Categoría", "Evidencia / nodo", "Estado"],
    ["", "FACTORES PERSONALES", "", "", ""],
    ["FP1", "Omitir controles (permiso, inspección pre-uso, conexión) a pesar de contar con certificación avanzada vigente; posible exceso de confianza o costumbre tolerada.", "Motivación incorrecta", "F02, F10, F11", "Hipótesis (confirmar en entrevista)"],
    ["FP2", "Falta de habilidad práctica para mantener la conexión al 100 % con eslinga en Y al desplazarse sobre el banco.", "Falta de habilidad", "H1", "Hipótesis"],
    ["FP3", "Posible presión de tiempo para entregar la aeronave lista en el turno nocturno.", "Tensión mental por demandas de producción", "Entrevistas", "Hipótesis"],
    ["", "FACTORES DEL TRABAJO", "", "", ""],
    ["FT1", "No existe programa de prevención y protección contra caídas ni procedimiento para la limpieza de aeronaves en alturas (ubicación de anclajes, claridad, uso del banco, rescate).", "Estándares de trabajo inadecuados", "F13 / J", "Comprobada"],
    ["FT2", "El coordinador TSA avaló el permiso sin verificar firmas ni condiciones en el sitio; no se verificó el uso de los equipos durante el turno.", "Liderazgo y supervisión deficientes", "F10 / N", "Comprobada"],
    ["FT3", "Banco sin barandas perimetrales y punto de anclaje no diseñado para quedar por encima del anillo D.", "Ingeniería inadecuada", "F06, F07 / E, K, M", "Comprobada"],
    ["FT4", "Sin listas de chequeo pre-uso; registros de inspección semestral (frecuencia del fabricante) no evidenciados.", "Mantenimiento e inspección inadecuados", "F08, F09, F11 / I, O", "Comprobada (registros por verificar)"],
    ["FT5", "Eslinga comprada en 2023 con fecha de fabricación de 2013, sin criterio de vida útil ni verificación de la certificación (Decreto 1072 de 2015, art. 2.2.4.6.27).", "Adquisiciones inadecuadas", "F09 / P", "Comprobada"],
    ["FT6", "Tarea de limpieza en húmedo, distinta del lavado en seco registrado, sin análisis de riesgos específico.", "Planificación y gestión del cambio inadecuadas", "F04", "Hipótesis"],
    ["FT7", "No se evidencia verificación de la empresa contratante sobre las condiciones de trabajo en alturas del contratista (Decreto 1072 de 2015, art. 2.2.4.6.28).", "Gestión de contratistas deficiente", "F17", "Hipótesis"],
], [7, 42, 21, 15, 15], size=8, full_rows={1: ("Factores personales", FILL_SUB), 5: ("Factores del trabajo (del sistema de gestión)", FILL_SUB)},
    fills={(2, None): FILL_SUP, (3, None): FILL_SUP, (4, None): FILL_SUP, (11, None): FILL_SUP, (12, None): FILL_SUP},
    col_align=["center", None, None, None, None])
d.p("La fatiga (hipótesis H6) se descarta como causa: el trabajador tuvo 16 h de descanso, llevaba 3 h 30 min de turno y tenía "
    "concepto médico de aptitud.")
d.h("5.5 Conclusión del análisis", 2)
d.p("El accidente es multicausal. Las causas inmediatas comprobadas son físicas y de procedimiento: un equipo de acceso sin "
    "protección colectiva, un sistema de detención mal configurado y defectuoso, un permiso de trabajo incompleto y equipos sin "
    "inspección. Todas convergen en una causa básica de gestión: la empresa no tiene el programa de prevención y protección contra "
    "caídas que exige la Resolución 4272 de 2021 {c:res4272}, y los controles que sí existían en el papel (permiso, coordinador TSA, "
    "certificación del trabajador) no se verificaron en el sitio. La certificación vigente del trabajador muestra que la formación, por "
    "sí sola, no compensa la falta de controles de ingeniería y de supervisión.")
d.h("5.6 Compromiso de la empresa y firmas", 2)
d.p("La empresa se compromete a implementar las medidas del plan de mejoramiento (sección 6) en los plazos establecidos, a "
    "informar los avances al COPASST y a la ARL y a conservar este informe con sus anexos (Res. 1401 de 2007, art. 13; Decreto 1072 de "
    "2015, art. 2.2.4.6.33).")
d.table([
    ["Representante legal o delegado", "Profesional con licencia en SST (líder)", "Representante del COPASST"],
    ["\n\n\nFirma: ____________________\nNombre: [__]\nCC: [__]", "\n\n\nFirma: ____________________\nNombre: [Integrante __]\nLicencia N.º [__]",
     "\n\n\nFirma: ____________________\nNombre: [Integrante __]\nCC: [__]"],
], [34, 33, 33], size=8.5, repeat_header=False)
d.p("Fecha de elaboración del informe: [dd/mm/2026, a más tardar el 28/08/2026].", size=9.5)

# ============================================================================ 6
d.h("6. Plan de mejoramiento", 1)
d.p("Las medidas siguen la jerarquía de controles del Decreto 1072 de 2015 (art. 2.2.4.6.24) {c:d1072}: primero se elimina o se "
    "controla el peligro en la fuente y en el medio, y después se actúa sobre el trabajador. Cada medida indica la causa que elimina "
    "(códigos de las Tablas 12 y 13), el responsable, la fecha límite y el indicador para verificar su cumplimiento.")
d.h("6.1 Medidas inmediatas (contención)", 2)
d.caption_tab("Medidas inmediatas tomadas tras el accidente.")
d.table([
    ["N.º", "Medida", "Responsable", "Fecha"],
    ["MI1", "Retirar de servicio y conservar como evidencia el arnés (serie 4123640140102712) y la eslinga (serie 6710180130904536); enviarlos a evaluación por persona calificada o por el fabricante.", "Coordinador TSA", "13/08/2026"],
    ["MI2", "Bloquear y etiquetar el banco involucrado y los de diseño similar hasta instalar barandas en todos los lados abiertos.", "Jefe de operaciones", "13/08/2026"],
    ["MI3", "Inspección extraordinaria del 100 % de arneses, eslingas, conectores y bancos; retirar los defectuosos o sin trazabilidad.", "Coordinador TSA y persona calificada", "15/08/2026"],
    ["MI4", "Mientras se implementan los controles: no trabajar sobre bancos sin baranda perimetral y no iniciar trabajos en alturas sin permiso firmado por todos los ejecutantes y verificado en el sitio por el coordinador.", "Gerencia", "13/08/2026"],
    ["MI5", "Charla de lecciones aprendidas en los tres turnos.", "Responsable del SG-SST", "20/08/2026"],
    ["MI6", "Seguimiento médico y apoyo al trabajador y su familia; coordinación con la ARL para rehabilitación y reintegro.", "Talento humano y SG-SST", "Permanente"],
], [8, 62, 18, 12], size=8, col_align=["center", None, None, "center"])
d.h("6.2 Medidas correctivas y preventivas", 2)
d.caption_tab("Plan de mejoramiento: medidas correctivas y preventivas.")
d.table([
    ["N.º", "Medida", "Causa que elimina", "Nivel de control", "Responsable", "Fecha límite", "Indicador / evidencia"],
    ["M1", "Rediseñar o reemplazar los bancos por plataformas de mantenimiento de aeronaves con barandas en todos los lados abiertos (baranda superior, intermedia y rodapié), acceso con cierre automático y superficie antideslizante.", "CS1, FT3 (E)", "Ingeniería / sustitución - fuente", "Gerencia y jefe de mantenimiento", "30/09/2026", "Bancos con protección perimetral / bancos en uso = 100 %"],
    ["M2", "Diseñar, instalar y certificar con persona calificada puntos de anclaje por encima del anillo D o líneas de vida sobre el área de trabajo, de al menos 5.000 lb (22,2 kN) por trabajador; preferir sistemas de restricción que impidan llegar al borde.", "CS2, FT3 (K, M)", "Ingeniería - medio", "Coordinador TSA y persona calificada", "30/09/2026", "Anclajes certificados / anclajes requeridos = 100 %"],
    ["M3", "Calcular y registrar el requerimiento de claridad en el permiso de cada tarea; prohibir configuraciones con caída libre mayor de 1,80 m o claridad insuficiente.", "CS2 (M)", "Administrativo", "Coordinador TSA", "31/08/2026", "Permisos con cálculo de claridad / permisos emitidos = 100 %"],
    ["M4", "Elaborar e implementar el programa de prevención y protección contra caídas (Res. 4272 de 2021): inventario de tareas y anclajes, procedimiento de limpieza de aeronaves en alturas (seco y húmedo), plan de emergencias y rescate, roles e inspecciones.", "FT1 (J)", "Administrativo", "Responsable del SG-SST", "30/09/2026", "Programa aprobado y divulgado al 100 % del personal"],
    ["M5", "Fortalecer el permiso de trabajo: firma de cada ejecutante antes de iniciar, verificación en el sitio por el coordinador TSA con lista (anclaje, claridad, barandas, equipos, iluminación, superficie) y cierre al final del turno; auditoría semanal aleatoria.", "AS1, AS5, FT2 (L, N)", "Administrativo", "Coordinador TSA", "31/08/2026", "Permisos completos / permisos auditados = 100 %"],
    ["M6", "Inspección pre-uso diaria por el trabajador (lista de chequeo) e inspección periódica por persona calificada con la frecuencia del fabricante (semestral); hoja de vida y etiqueta para cada equipo.", "AS2, CS3, FT4 (I, O)", "Administrativo - EPP", "Coordinador TSA", "31/08/2026", "Equipos con hoja de vida e inspección vigente = 100 %"],
    ["M7", "Reemplazar eslingas y conectores sin trazabilidad o fuera de vida útil; fijar en compras requisitos de certificación, antigüedad máxima de fabricación al recibir y vida útil según el fabricante.", "CS3, FT5 (P)", "EPP - administrativo", "Compras y SG-SST", "15/09/2026", "Equipos que cumplen los criterios de compra = 100 %"],
    ["M8", "Procedimiento de orden y aseo para la limpieza en húmedo sobre bancos: recoger mangueras e insumos, secar la superficie, calzado antideslizante y análisis de riesgos cuando cambie el método de lavado.", "CS4, FT6 (H4)", "Administrativo - EPP", "Jefe de operaciones", "31/08/2026", "Inspecciones planeadas con cumplimiento de al menos 95 %"],
    ["M9", "Medir la iluminancia en las posiciones de trabajo nocturno y complementar con iluminación portátil donde no se cumpla el nivel requerido para la tarea.", "CS5 (H5)", "Ingeniería - medio", "Responsable del SG-SST", "15/09/2026", "Posiciones medidas que cumplen / posiciones medidas"],
    ["M10", "Reentrenamiento práctico de trabajadores y coordinador: conexión al 100 % con eslinga en Y, inspección pre-uso, factor de caída y claridad; evaluación práctica y observación de comportamientos en campo.", "AS3, FP1, FP2 (H1)", "Administrativo - trabajador", "SG-SST y centro de entrenamiento", "30/09/2026", "Personal aprobado en evaluación práctica = 100 %; observaciones seguras / observaciones"],
    ["M11", "Asignar ayudante de seguridad o supervisor en el sitio durante los trabajos en alturas del turno nocturno y revisar con la empresa contratante los tiempos de entrega de las aeronaves.", "FT2, FP3", "Administrativo", "Jefe de operaciones", "31/08/2026", "Turnos con supervisor asignado / turnos con trabajo en alturas = 100 %"],
    ["M12", "Coordinar con la empresa contratante la verificación de requisitos de SST para tareas de alto riesgo (Decreto 1072 de 2015, art. 2.2.4.6.28) y actualizar la matriz de peligros de la operación.", "FT7", "Administrativo", "Gerencia y SG-SST", "30/09/2026", "Acta de coordinación y matriz actualizada"],
    ["M13", "Divulgar los resultados de la investigación al COPASST y a los trabajadores, e incluir las acciones en el plan anual de trabajo del SG-SST (Decreto 1072 de 2015, art. 2.2.4.6.32).", "Todas", "Administrativo", "Responsable del SG-SST", "31/08/2026", "Acta de divulgación firmada"],
], [6, 31, 11, 13, 13, 11, 15], size=7.5, col_align=["center", None, None, None, None, "center", None])
d.h("6.3 Seguimiento y verificación de eficacia", 2)
d.bullets([
    "El COPASST revisa mensualmente el avance del plan y deja acta; el responsable del SG-SST reporta los avances a la ARL junto con las evidencias.",
    "Verificación de eficacia al 30/11/2026: cero trabajos en alturas sin permiso completo en las auditorías, 100 % de equipos con inspección vigente, 100 % de bancos con barandas y cero incidentes por caída de altura.",
    "Si un indicador no se cumple, se analiza la causa y se reprograma la medida con un nuevo responsable y una nueva fecha (Decreto 1072 de 2015, art. 2.2.4.6.33).",
])

# ============================================================================ 7
d.h("7. Costos ocultos del accidente de trabajo", 1)
d.h("7.1 Concepto", 2)
d.p("Los costos de un accidente se dividen en dos grupos. Los costos directos o asegurados son las prestaciones asistenciales y "
    "económicas que cubre el Sistema General de Riesgos Laborales: atención médica, rehabilitación y subsidio por incapacidad temporal "
    "{c:ley776}. Los costos indirectos u ocultos son los que asume la empresa y casi nunca aparecen como costo del accidente en la "
    "contabilidad: tiempo perdido del trabajador, de los compañeros y de los supervisores, interrupción de la operación, reemplazo y "
    "entrenamiento, daño de equipos, investigación, sanciones, demandas y pérdida de imagen ante el cliente.")
d.p("Heinrich planteó que los costos indirectos podían ser del orden de cuatro veces los directos {c:heinrich}, y Bird y Germain "
    "representaron esta relación con la figura del iceberg, en la que la parte visible es mucho menor que la oculta {c:bird}. Los estudios "
    "recientes muestran que la proporción varía según el sector y el método de cálculo, por lo que debe estimarse caso a caso "
    "{c:rikh,jallon,feng}.")
d.h("7.2 Artículos científicos que definen los costos ocultos", 2)
d.caption_tab("Artículos Q1 sobre costos ocultos del accidente de trabajo (y un complementario de acceso abierto).")
d.table([
    ["Artículo", "Revista y cuartil", "Qué aporta sobre los costos ocultos", "Uso en este caso"],
    ["Rikhardsson e Impgaard (2004) {c:rikh}", "//Accident Analysis & Prevention//. Q1 (SJR, Safety, Risk, Reliability and Quality)",
     "Aplican costeo basado en actividades en empresas danesas: identifican las actividades que dispara un accidente y encuentran que cerca de dos tercios del costo era visible en la contabilidad y un tercio permanecía oculto para la gerencia.",
     "Listar las actividades que dispara este accidente (atención, traslado, reportes, investigación, reemplazo) y asignarles costo."],
    ["Jallon, Imbeau y de Marcellis-Warin (2011) {c:jallon}", "//Journal of Safety Research//. Q1 (SJR)",
     "Revisan los métodos de cálculo de costos indirectos (enfoques de arriba hacia abajo, de abajo hacia arriba y local) y concluyen que el enfoque local, calculado dentro de la empresa, es el más adecuado; proponen criterios para un modelo práctico.",
     "Calcular los costos indirectos del caso con datos propios de la empresa, no con una razón genérica."],
    ["Feng, Zhang y Wu (2015) {c:feng}", "//Safety Science//. Q1 (SJR)",
     "En proyectos de edificación en Singapur separan costos directos e indirectos de los accidentes (en promedio 0,165 % y 0,086 % del valor del contrato; 0,25 % en total) e identifican los factores que los aumentan.",
     "Mostrar que la relación entre costos directos e indirectos no es fija y que debe medirse."],
    ["Battaglia, Frey y Passetti (2014) {c:battaglia} - complementario", "//Industrial Health// (acceso abierto; verificar cuartil del año de consulta)",
     "Estudio de campo en una gran empresa italiana que implementó una herramienta de análisis de costos de accidentes: la dimensión económica resultó sustancial y su uso exige compromiso de la organización.",
     "Referencia para incorporar el registro de costos de accidentes al SG-SST."],
], [20, 18, 37, 25], size=8)
d.p("El cuartil corresponde a la clasificación de Scimago Journal Rank (SJR). Como el cuartil cambia cada año, al descargar los "
    "artículos conviene verificarlo y guardar una captura de la página de la revista en SJR o en Journal Citation Reports como evidencia.", size=9, italic=True, color="595959")
d.h("7.3 Aplicación al caso", 2)
d.caption_tab("Costos directos y ocultos del accidente del 13/08/2026.")
d.table([
    ["Tipo", "Costo", "Quién lo asume / observación"],
    ["Directo (asegurado)", "Atención prehospitalaria, hospitalaria y rehabilitación del trauma craneoencefálico", "ARL SURA"],
    ["Directo (asegurado)", "Subsidio por incapacidad temporal (30 días o más) {c:ley776}", "ARL SURA"],
    ["Directo (asegurado), eventual", "Indemnización por incapacidad permanente parcial o pensión de invalidez si quedan secuelas", "ARL SURA, previa calificación"],
    ["Oculto", "Tiempo de los compañeros que atendieron la emergencia y suspensión del lavado de la aeronave en la posición Golfo", "Empresa"],
    ["Oculto", "Posible demora en la entrega de la aeronave y penalidades contractuales con la empresa contratante", "Empresa"],
    ["Oculto", "Tiempo de directivos y supervisores en reportes (FURAT, Ministerio del Trabajo), reuniones con la ARL y el cliente e investigación, incluida la consultoría externa cotizada por el grupo", "Empresa"],
    ["Oculto", "Reemplazo del trabajador durante la incapacidad: horas extra o contratación temporal, inducción, certificación en alturas y menor productividad inicial", "Empresa"],
    ["Oculto", "Reposición del arnés y la eslinga en cuarentena y adecuación urgente de los bancos", "Empresa (parte se convierte en inversión preventiva)"],
    ["Oculto", "Posible demanda por culpa patronal (indemnización plena de perjuicios) {c:cst}, ya anticipada en el caso, y costos de defensa jurídica", "Empresa"],
    ["Oculto", "Multas del Ministerio del Trabajo por incumplimiento de normas de SST {c:ley1562}", "Empresa"],
    ["Oculto", "Pérdida de confianza o del contrato con la empresa contratante; efecto en futuras licitaciones", "Empresa"],
    ["Oculto", "Deterioro del clima laboral: temor, ausentismo y rotación en el equipo de lavado", "Empresa"],
    ["Oculto", "Posible aumento de la tarifa de cotización a la ARL dentro del rango de la clase de riesgo, según la siniestralidad", "Empresa"],
], [22, 56, 22], size=8, fills={(1, None): FILL_OK, (2, None): FILL_OK, (3, None): FILL_OK})
d.p("Con el enfoque local que recomiendan Jallon y colaboradores {c:jallon}, la empresa puede valorar cada fila con sus propios "
    "registros (horas pagadas, facturas, penalidades) y comparar el total con la inversión del plan de mejoramiento.")

# ============================================================================ referencias
d.h("Referencias", 1)
for i, k in enumerate(d.cite_order, 1):
    d.p("[%d]\t%s" % (i, d.refs[k]), style="Referencia")
unused = [k for k in d.refs if k not in d.cite_order]
assert not unused, unused

# ============================================================================ anexos
d.h("Anexos", 1)
d.h("Anexo A. FURAT diligenciado", 2)
d.p("Archivo **01_FURAT_ARL_SURA_AT_13-08-2026_diligenciado.xlsx**, hojas \"FURAT\" (formato listo para imprimir en dos páginas "
    "tamaño carta) y \"Notas y supuestos\" (origen de cada dato).")
d.h("Anexo B. Artículos sobre costos ocultos", 2)
d.p("Descargar los PDF con la cuenta institucional desde las bases de datos de la Biblioteca de la Universidad Distrital (Scopus, Web "
    "of Science o ScienceDirect) y anexarlos al informe final:")
d.bullets([
    "Rikhardsson e Impgaard (2004): buscar por DOI 10.1016/S0001-4575(02)00147-1.",
    "Jallon, Imbeau y de Marcellis-Warin (2011): buscar por título en ScienceDirect o Scopus (Journal of Safety Research, vol. 42, no. 3).",
    "Feng, Zhang y Wu (2015): buscar por título en ScienceDirect o Scopus (Safety Science, vol. 72).",
    "Complementario de acceso abierto: Battaglia, Frey y Passetti (2014), disponible en [[https://pmc.ncbi.nlm.nih.gov/articles/PMC4243021/|PubMed Central (PMC4243021)]].",
])
d.h("Anexo C. Registro fotográfico", 2)
d.p("Insertar las fotografías de la guía: banco-escalera de lavado junto a la aeronave, eslinga en Y, detalle del gancho de 1-1/4\", "
    "arnés de cuerpo entero, plataforma del banco y atención del trabajador en el sitio.")

d.save(DOCX, "Investigación AT grave del 13/08/2026 · Componente del integrante 4 (OSALAN y formatos legales)",
       "Investigación AT grave 13/08/2026 - Integrante 4", "Integrante 4")
print("DOCX:", DOCX)
print("Referencias:", len(d.cite_order), "Figuras:", d.fig_n, "Tablas:", d.tab_n)
