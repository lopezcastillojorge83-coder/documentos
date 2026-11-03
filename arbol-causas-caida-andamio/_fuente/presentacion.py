# -*- coding: utf-8 -*-
"""Diapositivas de la presentación (HTML 1920x1080) y notas del orador.

Cada diapositiva es un dict: {"html": ..., "notas": ..., "nativos": [...]}.
"nativos" son cuadros de texto editables que se colocan sobre la imagen en
el .pptx (en píxeles del lienzo de 1920x1080).
"""
import html as H

PIE = "NTP 274 · Árbol de causas · Caída de altura desde andamio"
TIPO = {  # fondo, borde, texto
    "dano": ("#8E2A2A", "#5E1A1A", "#FFFFFF"),
    "hecho": ("#D6EAF8", "#2E6DA4", "#0F2A44"),
    "humano": ("#FFF1BF", "#B58900", "#3B2F00"),
    "causa": ("#C8EBC0", "#2E7D32", "#0F3A12"),
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1920px;height:1080px;background:#fff}
body{font-family:"Noto Sans",sans-serif;color:#1e293b}
#lienzo{position:relative;width:1920px;height:1080px;overflow:hidden;background:#fff}
.top{position:absolute;left:0;top:0;width:1920px;height:156px;background:#1F3A5F;padding:28px 96px 0}
.top .k{font-size:22px;letter-spacing:4px;text-transform:uppercase;color:#9CC3E6;font-weight:700}
.top h1{font-size:52px;line-height:1.15;color:#fff;font-weight:700;margin-top:6px}
.body{position:absolute;left:96px;right:96px;top:196px;bottom:100px}
.foot{position:absolute;left:96px;right:96px;bottom:26px;height:46px;border-top:2px solid #E2E8F0;
 display:flex;justify-content:space-between;align-items:flex-end;font-size:20px;color:#64748B}
p{font-size:32px;line-height:1.4}
b,strong{font-weight:700}
.card{border-radius:18px;padding:26px 30px;background:#F1F5F9;border:2px solid #E2E8F0;overflow:hidden}
.card h3{font-size:31px;color:#1F3A5F;margin-bottom:10px;line-height:1.2}
.card p,.card li{font-size:26px;line-height:1.38}
ul.l{list-style:none}
ul.l li{position:relative;padding-left:30px;margin-bottom:9px}
ul.l li:before{content:"";position:absolute;left:3px;top:.52em;width:13px;height:13px;border-radius:3px;background:#2E6DA4}
.chip{display:inline-block;font-weight:700;font-size:21px;line-height:1;padding:7px 14px;border-radius:999px;background:#334155;color:#fff}
.tag{display:inline-block;font-weight:700;font-size:21px;padding:6px 14px;border-radius:8px;background:#E0ECF8;color:#1F3A5F}
.grid{display:grid;gap:26px}
.num{display:flex;align-items:center;justify-content:center;width:64px;height:64px;border-radius:50%;
 background:#2E6DA4;color:#fff;font-size:32px;font-weight:700;flex:none}
"""

JS = """
window.__report=function(){const mal=[];
document.querySelectorAll('.body,.card,.fit').forEach(function(e,i){
 if(e.scrollHeight>e.clientHeight+2||e.scrollWidth>e.clientWidth+2)
  mal.push('desborda '+e.className+': '+(e.textContent||'').trim().slice(0,50));});
const b=document.querySelector('.body');
if(b){const r=b.getBoundingClientRect();
 b.querySelectorAll('*').forEach(function(e){const q=e.getBoundingClientRect();
  if(q.width&&(q.bottom>r.bottom+2||q.right>r.right+2))
   mal.push('fuera: '+(e.textContent||'').trim().slice(0,50));});}
return {desbordadas:mal.slice(0,6)};};
"""


def esc(t):
    """Escapa texto y convierte **negrita**."""
    partes = H.escape(t).split("**")
    return "".join(f"<b>{x}</b>" if i % 2 else x for i, x in enumerate(partes))


def documento(cuerpo):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}'
            f'</style></head><body>{cuerpo}<script>{JS}</script></body></html>')


def marco(kicker, titulo, cuerpo):
    """Diapositiva estándar: barra de título, cuerpo y pie con numeración."""
    return documento(
        f'<div id="lienzo"><div class="top"><div class="k">{esc(kicker)}</div>'
        f'<h1>{esc(titulo)}</h1></div><div class="body">{cuerpo}</div>'
        f'<div class="foot"><span>{PIE}</span><span>{{N}} / {{TOTAL}}</span></div></div>')


def lista(items, size=None):
    st = f' style="font-size:{size}px"' if size else ""
    return '<ul class="l">' + "".join(f"<li{st}>{esc(i)}</li>" for i in items) + "</ul>"


def arbol_decorativo():
    """Pequeño árbol estilizado para la portada (solo decoración)."""
    cajas = [  # x, y, w, h, tipo
        (150, 0, 220, 70, "dano"),
        (40, 140, 200, 64, "hecho"), (300, 140, 200, 64, "hecho"),
        (0, 280, 150, 60, "humano"), (180, 280, 150, 60, "hecho"),
        (360, 280, 150, 60, "humano"),
        (20, 420, 200, 70, "causa"), (290, 420, 200, 70, "causa"),
    ]
    lineas = [(260, 70, 260, 105), (140, 105, 400, 105), (140, 105, 140, 140),
              (400, 105, 400, 140), (140, 204, 140, 242), (75, 242, 255, 242),
              (75, 242, 75, 280), (255, 242, 255, 280), (400, 204, 400, 280),
              (75, 340, 75, 380), (435, 340, 435, 380), (75, 380, 435, 380),
              (120, 380, 120, 420), (390, 380, 390, 420), (255, 340, 255, 380)]
    svg = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>' for a, b, c, d in lineas)
    div = "".join(
        f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
        f'background:{TIPO[t][0]};border:3px solid {TIPO[t][1]};border-radius:12px"></div>'
        for x, y, w, h, t in cajas)
    return (f'<div style="position:absolute;left:1330px;top:250px;width:520px;height:500px;'
            f'opacity:.92"><svg width="520" height="500" style="position:absolute;left:0;top:0">'
            f'<g stroke="#9CC3E6" stroke-width="4">{svg}</g></svg>{div}</div>')


# Geometría del panel de integrantes (px). Se usa también para los textos nativos.
PANEL = {"x": 96, "y": 636, "w": 1140, "h": 348}
FILAS_Y = [752, 822, 892]
FILA_H = 62
COL_NOMBRE = (190, 640)   # x, ancho
COL_CODIGO = (890, 316)


def portada():
    px, py, pw, ph = PANEL["x"], PANEL["y"], PANEL["w"], PANEL["h"]
    filas = ""
    for i, y in enumerate(FILAS_Y, 1):
        filas += (f'<div style="position:absolute;left:{px + 30}px;top:{y}px;width:{pw - 60}px;'
                  f'height:{FILA_H}px;border-bottom:2px solid #CBD5E1"></div>'
                  f'<div class="num" style="position:absolute;left:{px + 34}px;top:{y + 11}px;'
                  f'width:40px;height:40px;font-size:22px">{i}</div>')
    panel = (f'<div style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;'
             f'background:#fff;border-radius:22px"></div>'
             f'<div style="position:absolute;left:{px + 34}px;top:{py + 26}px;font-size:30px;'
             f'font-weight:700;color:#1F3A5F">Integrantes</div>'
             f'<div style="position:absolute;left:{COL_NOMBRE[0]}px;top:{py + 80}px;font-size:20px;'
             f'color:#64748B;font-weight:700;letter-spacing:1px">NOMBRE COMPLETO</div>'
             f'<div style="position:absolute;left:{COL_CODIGO[0]}px;top:{py + 80}px;font-size:20px;'
             f'color:#64748B;font-weight:700;letter-spacing:1px">CÓDIGO</div>{filas}')
    cuerpo = (
        '<div id="lienzo" style="background:linear-gradient(135deg,#1F3A5F 0%,#2B5583 100%)">'
        '<div style="position:absolute;left:96px;top:92px;width:1180px">'
        '<div style="font-size:24px;letter-spacing:5px;color:#9CC3E6;font-weight:700;'
        'text-transform:uppercase">Investigación de accidentes · NTP 274</div>'
        '<div style="font-size:84px;line-height:1.05;color:#fff;font-weight:700;margin-top:20px">'
        'Árbol de causas</div>'
        '<div style="font-size:40px;line-height:1.3;color:#DCE8F5;margin-top:18px">Caída de altura '
        'desde un andamio durante trabajos de reparación de fachada</div>'
        '<div style="font-size:27px;color:#9CC3E6;margin-top:26px">Seguridad (Gr. 23) · Docente: '
        'Germán Suárez · 3 de noviembre de 2026</div></div>'
        f'{panel}{arbol_decorativo()}</div>')
    nativos = []
    for i, y in enumerate(FILAS_Y, 1):
        nativos.append({"x": COL_NOMBRE[0], "y": y, "w": COL_NOMBRE[1], "h": FILA_H,
                        "texto": f"[Nombre completo del integrante {i}]",
                        "pt": 16, "color": "1E293B", "nombre": f"Integrante {i}"})
        nativos.append({"x": COL_CODIGO[0], "y": y, "w": COL_CODIGO[1], "h": FILA_H,
                        "texto": "[Código]", "pt": 16, "color": "1E293B",
                        "nombre": f"Código {i}"})
    notas = ("Presentación del grupo. Decir el nombre de cada integrante. "
             "Tema: investigamos una caída de altura desde un andamio durante la reparación "
             "de una fachada, aplicando el método del árbol de causas de la NTP 274 del INSHT. "
             "Objetivo: encontrar las causas de origen del accidente y proponer medidas para "
             "que no se repita.")
    return {"html": documento(cuerpo), "notas": notas, "nativos": nativos}


def s_contenido():
    items = [("El método", "La NTP 274 y sus reglas básicas"),
             ("El caso", "Datos generales y relato del accidente"),
             ("Toma de datos", "Hechos recogidos en tres ámbitos"),
             ("Construcción del árbol", "Pregunta a pregunta, desde la lesión"),
             ("Causas primarias", "Los fallos de organización de origen"),
             ("Medidas y conclusiones", "Cómo evitar que se repita")]
    cards = "".join(
        f'<div class="card" style="display:flex;gap:26px;align-items:center">'
        f'<div class="num" style="width:84px;height:84px;font-size:40px">{i}</div>'
        f'<div><h3 style="margin-bottom:6px">{esc(t)}</h3><p>{esc(d)}</p></div></div>'
        for i, (t, d) in enumerate(items, 1))
    cuerpo = (f'<div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:'
              f'repeat(3,1fr);height:100%">{cards}</div>')
    notas = ("La exposición tiene seis partes. Primero explicamos el método de la NTP 274. "
             "Después presentamos el caso y los datos recogidos. Luego construimos el árbol paso "
             "a paso, identificamos las causas primarias y cerramos con las medidas preventivas "
             "y las conclusiones.")
    return {"html": marco("Contenido", "Qué vamos a presentar", cuerpo), "notas": notas}


def s_que_es():
    principios = [
        ("Causas, no culpables", "Se buscan las causas del accidente, no a los responsables."),
        ("Solo hechos probados", "Hechos concretos y objetivos, no opiniones ni juicios de valor."),
        ("Hasta el origen", "El análisis llega a los fallos de organización que lo permitieron."),
    ]
    tarjetas = "".join(
        f'<div class="card" style="border-left:10px solid #2E6DA4"><h3>{esc(t)}</h3>'
        f'<p>{esc(d)}</p></div>' for t, d in principios)
    cuerpo = (
        '<div style="display:flex;gap:56px;height:100%">'
        '<div style="flex:1.05;display:flex;flex-direction:column;gap:28px">'
        '<p>Método de investigación de accidentes de la <b>NTP 274</b> del INSHT. Representa '
        'gráficamente la cadena de hechos que produjo un accidente real, desde la lesión hasta '
        'sus causas de origen.</p>'
        '<p>Su objetivo es identificar las <b>causas primarias</b> para eliminarlas o '
        'controlarlas, de forma que el accidente no vuelva a ocurrir.</p>'
        '<div class="card" style="background:#1F3A5F;border-color:#1F3A5F;margin-top:auto">'
        '<p style="color:#9CC3E6;font-size:24px;font-weight:700;letter-spacing:2px">'
        'LA PREGUNTA QUE GUÍA EL MÉTODO</p>'
        '<p style="color:#fff;font-size:40px;font-weight:700;line-height:1.25;margin-top:8px">'
        '¿Qué tuvo que ocurrir para que este hecho se produjera?</p></div></div>'
        f'<div style="flex:1;display:flex;flex-direction:column;gap:24px;justify-content:center">'
        f'{tarjetas}</div></div>')
    notas = ("El árbol de causas es el método que propone la NTP 274 para investigar accidentes. "
             "Parte de un accidente que ya ocurrió y dibuja la concatenación de hechos que lo "
             "produjo. Tiene tres reglas: se buscan causas y no culpables, solo se aceptan hechos "
             "probados, y hay que llegar hasta las causas primarias, que suelen ser fallos de "
             "organización. Todo el método se apoya en una pregunta: ¿qué tuvo que ocurrir para "
             "que este hecho se produjera?")
    return {"html": marco("1 · El método", "¿Qué es el árbol de causas?", cuerpo), "notas": notas}


def s_como():
    pasos = [
        ("Toma de datos", ["Investigar lo antes posible", "Reconstruir el accidente in situ",
                           "Entrevistar al accidentado, testigos y mando directo",
                           "Condiciones materiales, organización y conducta"]),
        ("Organización de los datos", ["Partir de la lesión (suceso último)",
                                       "Preguntar «¿qué tuvo que ocurrir?» y «¿algo más?»",
                                       "Clasificar la relación entre los hechos"]),
        ("Árbol y medidas", ["Dibujar el árbol completo", "Identificar las causas primarias",
                             "Proponer medidas para cada causa"]),
    ]
    cols = ""
    for i, (t, items) in enumerate(pasos, 1):
        if i > 1:
            cols += ('<svg width="56" height="60" style="flex:none;align-self:center">'
                     '<path d="M4 30 H40" stroke="#2E6DA4" stroke-width="6"/>'
                     '<path d="M36 14 L54 30 L36 46 Z" fill="#2E6DA4"/></svg>')
        cols += (f'<div class="card" style="flex:1;background:#fff;border-top:10px solid #2E6DA4">'
                 f'<div style="display:flex;gap:18px;align-items:center;margin-bottom:16px">'
                 f'<div class="num">{i}</div><h3 style="margin:0">{esc(t)}</h3></div>'
                 f'{lista(items, 30)}</div>')
    fin = ('<div class="card" style="background:#FFF6DB;border-color:#E0A100;margin-top:26px">'
           '<p style="font-size:27px"><b>El árbol termina cuando:</b> a) se llega a causas '
           'primarias, que no necesitan una situación anterior para explicarse; o b) faltan '
           'datos para seguir remontando.</p></div>')
    cuerpo = (f'<div style="display:flex;flex-direction:column;height:100%">'
              f'<div style="display:flex;gap:10px;flex:1">{cols}</div>{fin}</div>')
    notas = ("El método tiene tres fases. Primero la toma de datos: ir al lugar cuanto antes, "
             "reconstruir el accidente y hablar con el accidentado, los testigos y el encargado. "
             "Segundo, organizar los datos: se parte de la lesión y, hecho por hecho, se pregunta "
             "qué tuvo que ocurrir y si hizo falta algo más. Tercero, se dibuja el árbol, se "
             "identifican las causas primarias y se proponen medidas. El árbol termina al llegar "
             "a causas primarias o cuando faltan datos.")
    return {"html": marco("1 · El método", "Cómo se aplica", cuerpo), "notas": notas}


def mini(cajas, segmentos, flechas):
    """Esquema pequeño estilo NTP 274 (se lee de izquierda a derecha)."""
    s = ""
    for x1, y1, x2, y2 in segmentos:
        s += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
    for x1, y, x2 in flechas:
        s += (f'<line x1="{x1}" y1="{y}" x2="{x2 - 12}" y2="{y}"/>'
              f'<polygon points="{x2 - 15},{y - 9} {x2},{y} {x2 - 15},{y + 9}" '
              f'fill="#334155" stroke="none"/>')
    for x, y, t in cajas:
        s += (f'<rect x="{x}" y="{y}" width="96" height="48" rx="9" fill="#D6EAF8" '
              f'stroke="#2E6DA4" stroke-width="3"/><text x="{x + 48}" y="{y + 32}" '
              f'text-anchor="middle" font-size="22" font-weight="700" fill="#0F2A44" '
              f'stroke="none">{t}</text>')
    return (f'<svg width="330" height="170" style="flex:none"><g stroke="#334155" '
            f'stroke-width="3" fill="none">{s}</g></svg>')


def s_relaciones():
    rel = [
        ("Cadena", "Un hecho tiene un único antecedente: sin (y) no se produce (x).",
         "C1 origina 1.1.1: sin formación, el trabajador desconoce el riesgo.",
         mini([(20, 61, "y"), (214, 61, "x")], [], [(116, 85, 214)])),
        ("Conjunción", "Hacen falta dos o más antecedentes independientes a la vez.",
         "1.1 + 1.2 + 1.3 producen la caída (1).",
         mini([(20, 15, "y"), (20, 107, "z"), (214, 61, "x")],
              [(116, 39, 160, 39), (116, 131, 160, 131), (160, 39, 160, 131)],
              [(160, 85, 214)])),
        ("Disyunción", "Un mismo antecedente origina varios hechos independientes.",
         "C3 origina 1.2.2 y 1.3.1; C4 origina 1.3.2 y 2.1.1.",
         mini([(20, 61, "y"), (214, 15, "x1"), (214, 107, "x2")],
              [(116, 85, 165, 85), (165, 39, 165, 131)],
              [(165, 39, 214), (165, 131, 214)])),
        ("Hechos independientes", "Hechos sin relación entre sí: no se unen en el dibujo.",
         "La caída (1) y la falta de retención (2) no dependen una de otra.",
         mini([(20, 61, "y"), (214, 61, "x")], [], [])),
    ]
    cards = "".join(
        f'<div class="card" style="display:flex;gap:28px;align-items:center;background:#fff">'
        f'{svg}<div><h3>{esc(t)}</h3><p>{esc(d)}</p>'
        f'<p style="margin-top:12px;color:#2E6DA4;font-size:24px"><b>En el caso:</b> {esc(e)}</p>'
        f'</div></div>' for t, d, e, svg in rel)
    cuerpo = (f'<div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;'
              f'height:100%">{cards}</div>')
    notas = ("Al buscar los antecedentes de cada hecho aparecen cuatro situaciones. Cadena: un "
             "hecho tiene un solo antecedente. Conjunción: hacen falta varios antecedentes a la "
             "vez; por ejemplo, la caída necesitó que el trabajador retrocediera, que el tablón "
             "basculara y que no hubiera barandilla. Disyunción: un mismo antecedente produce "
             "varios hechos, como la falta de inspección. Y hechos independientes, que no se "
             "relacionan entre sí. En nuestro árbol aparecen las cuatro.")
    return {"html": marco("1 · El método", "Las cuatro relaciones entre hechos", cuerpo),
            "notas": notas}


def s_datos():
    datos = [
        ("Tipo de accidente", "Caída de personas a distinto nivel (caída de altura).", False),
        ("Actividad", "Reparación de fachada en un edificio de 5 plantas: picado de revoco, "
                      "saneado de grietas y mortero.", False),
        ("Agente material", "Andamio tubular de fachada de 4 niveles, montado 5 días antes.",
         False),
        ("Lugar", "Nivel 3 del andamio, a 6 m de altura, en el módulo del extremo lateral.",
         False),
        ("Accidentado", "Oficial de albañilería, 38 años, 12 años de oficio, sin formación "
                        "en trabajos en altura.", False),
        ("Lesión", "Politraumatismo grave: fractura de columna lumbar y de pelvis.", True),
    ]
    cards = ""
    for t, d, rojo in datos:
        est = ' style="background:#FBEAEA;border-color:#8E2A2A"' if rojo else ""
        col = "#8E2A2A" if rojo else "#1F3A5F"
        cards += (f'<div class="card"{est}><h3 style="color:{col};font-size:35px">{esc(t)}</h3>'
                  f'<p style="font-size:32px">{esc(d)}</p></div>')
    cuerpo = (f'<div style="display:flex;flex-direction:column;height:100%">'
              f'<div class="grid" style="grid-template-columns:repeat(3,1fr);'
              f'grid-template-rows:1fr 1fr;flex:1">{cards}</div>'
              f'<p style="font-size:22px;color:#64748B;margin-top:18px">Caso planteado como '
              f'supuesto de trabajo, con las causas más habituales de las caídas desde '
              f'andamios.</p></div>')
    notas = ("Presentamos el caso. Es una caída a distinto nivel durante la reparación de la "
             "fachada de un edificio de cinco plantas. El trabajador, un oficial de albañilería "
             "con experiencia pero sin formación en altura, estaba en el nivel 3 de un andamio "
             "tubular, a 6 metros. La lesión fue un politraumatismo grave con fractura de "
             "columna lumbar y de pelvis.")
    return {"html": marco("2 · El caso", "Datos generales del accidente", cuerpo),
            "notas": notas}


def s_relato():
    hitos = [
        ("5 días antes", "Operarios de la obra, sin formación ni plan de montaje, montan el "
                         "andamio. Los tablones quedan apoyados sin sujeción y nadie revisa "
                         "el montaje."),
        ("2 días antes", "Se retira la barandilla lateral del nivel 3 para subir cubos de "
                         "mortero, porque no hay un medio de elevación previsto. No se repone "
                         "ni se revisa."),
        ("Día del accidente", "El oficial retrocede hacia el extremo para valorar el paño "
                              "picado. Pisa un tablón suelto que bascula, pierde el equilibrio "
                              "y cae: no hay barandilla y no lleva arnés."),
    ]
    cols = ""
    for i, (t, d) in enumerate(hitos):
        color = "#8E2A2A" if i == 2 else "#2E6DA4"
        cols += (f'<div style="flex:1;display:flex;flex-direction:column;align-items:center">'
                 f'<div style="width:38px;height:38px;border-radius:50%;background:{color};'
                 f'border:6px solid #fff;box-shadow:0 0 0 4px {color};position:relative;'
                 f'z-index:2"></div>'
                 f'<div style="font-size:30px;font-weight:700;color:{color};margin:20px 0 16px">'
                 f'{esc(t)}</div><div class="card" style="background:#fff;flex:1;width:100%;'
                 f'border-top:8px solid {color}"><p style="font-size:33px">{esc(d)}</p></div>'
                 f'</div>')
    cuerpo = (
        '<div style="display:flex;flex-direction:column;height:100%">'
        '<div style="position:relative;display:flex;gap:40px;flex:1">'
        '<div style="position:absolute;left:16%;right:16%;top:17px;height:6px;'
        'background:#CBD5E1"></div>' + cols + '</div>'
        '<div class="card" style="background:#8E2A2A;border-color:#8E2A2A;margin-top:26px">'
        '<p style="color:#fff;font-size:30px"><b>Resultado:</b> caída de 6 m hasta el suelo y '
        'politraumatismo grave (fractura de columna lumbar y de pelvis).</p></div></div>')
    notas = ("Así ocurrieron los hechos. Cinco días antes, personal de la obra sin formación "
             "montó el andamio sin plan de montaje; los tablones quedaron sueltos y nadie lo "
             "revisó. Dos días antes se quitó la barandilla del extremo para subir materiales y "
             "no se volvió a poner. El día del accidente el oficial retrocedió para mirar su "
             "trabajo, pisó un tablón suelto, perdió el equilibrio y cayó: no había barandilla "
             "ni llevaba arnés.")
    return {"html": marco("2 · El caso", "Relato de los hechos", cuerpo), "notas": notas}


def s_toma():
    cols = [
        ("Condiciones materiales", "#2E6DA4",
         ["Tablones del nivel 3 apoyados sin sujeción",
          "Lateral del extremo sin barandilla ni rodapié",
          "Sin arneses en la obra ni anclajes en el andamio"]),
        ("Organización del trabajo", "#2E7D32",
         ["Montaje por personal no cualificado y sin plan",
          "Sin procedimiento ni responsable de inspección",
          "Sin evaluación del riesgo de caída ni medio para subir materiales",
          "Sin formación sobre trabajos en altura"]),
        ("Comportamiento humano", "#B58900",
         ["Oficial con experiencia, sin formación en altura",
          "Retrocede hacia el extremo para valorar el paño (acto habitual)"]),
    ]
    cards = "".join(
        f'<div class="card" style="background:#fff;border-top:10px solid {c}">'
        f'<h3 style="color:{c};font-size:34px">{esc(t)}</h3>{lista(items, 30)}</div>' for t, c, items in cols)
    cuerpo = (f'<div style="display:flex;flex-direction:column;height:100%">'
              f'<div class="grid" style="grid-template-columns:repeat(3,1fr);flex:1">{cards}</div>'
              f'<div class="card" style="margin-top:24px"><p style="font-size:25px">'
              f'<b>Fuentes:</b> inspección in situ · declaraciones del accidentado y los '
              f'compañeros · entrevista al encargado · documentación de la obra</p></div></div>')
    notas = ("La NTP pide recoger datos de tres ámbitos. En las condiciones materiales: tablones "
             "sin sujetar, el lateral sin barandilla y la falta de arneses y anclajes. En la "
             "organización: un montaje sin plan ni personal cualificado, nadie encargado de "
             "inspeccionar, sin evaluación del riesgo y sin formación. En el comportamiento: el "
             "trabajador hizo un gesto habitual, retroceder para mirar su trabajo.")
    return {"html": marco("3 · Toma de datos", "Hechos recogidos en tres ámbitos", cuerpo),
            "notas": notas}


def caja(x, y, w, h, tipo, ident, texto, fs=21):
    f, b, c = TIPO[tipo]
    chip = (f'<span style="display:inline-block;background:#334155;color:#fff;font-size:16px;'
            f'font-weight:700;padding:3px 9px;border-radius:9px;margin-bottom:4px">{ident}</span><br>'
            if ident else "")
    return (f'<div class="fit" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
            f'height:{h}px;background:{f};border:3px solid {b};color:{c};border-radius:12px;'
            f'display:flex;align-items:center;justify-content:center;text-align:center;'
            f'padding:8px 10px;font-size:{fs}px;line-height:1.22;overflow:hidden">'
            f'<div>{chip}{esc(texto)}</div></div>')


def s_construccion_1():
    qa = [
        ("P", "¿Qué tuvo que ocurrir para que el trabajador sufriera el politraumatismo?", None),
        ("R", "Que cayera al vacío desde la plataforma, a 6 m **(1)**.", None),
        ("P", "¿Tuvo que ocurrir algo más?", None),
        ("R", "Que ningún sistema lo retuviera en la caída **(2)**.", "Conjunción"),
        ("P", "¿Qué tuvo que ocurrir para que cayera?", None),
        ("R", "Que retrocediera hacia el extremo **(1.1)**, que los tablones basculasen "
              "**(1.2)** y que el lateral no tuviera barandilla **(1.3)**.", "Conjunción"),
    ]
    filas = ""
    for k, t, tag in qa:
        bg = "#1F3A5F" if k == "P" else "#2E7D32"
        estilo = "color:#475569" if k == "P" else "color:#0F172A"
        extra = f' <span class="tag" style="margin-left:8px">{tag}</span>' if tag else ""
        filas += (f'<div style="display:flex;gap:18px;align-items:flex-start;margin-bottom:16px">'
                  f'<div style="flex:none;width:46px;height:46px;border-radius:10px;background:{bg};'
                  f'color:#fff;font-weight:700;font-size:26px;display:flex;align-items:center;'
                  f'justify-content:center">{k}</div><p style="font-size:27px;{estilo}">'
                  f'{esc(t)}{extra}</p></div>')
    lineas = [(350, 108, 350, 150), (230, 150, 585, 150), (230, 150, 230, 200),
              (585, 150, 585, 200), (230, 302, 230, 360), (75, 360, 405, 360),
              (75, 360, 75, 420), (240, 360, 240, 420), (405, 360, 405, 420)]
    svg = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>' for a, b, c, d in lineas)
    puntas = "".join(f'<polygon points="{x - 9},{y + 14} {x + 9},{y + 14} {x},{y}" '
                     f'fill="#334155"/>' for x, y in [(350, 96), (230, 290)])
    arbol = (
        '<div style="position:relative;width:700px;height:560px;flex:none">'
        f'<svg width="700" height="560" style="position:absolute;left:0;top:0">'
        f'<g stroke="#334155" stroke-width="3">{svg}</g>{puntas}'
        '<text x="362" y="142" font-size="18" font-style="italic" fill="#64748B">Conjunción</text>'
        '<text x="242" y="352" font-size="18" font-style="italic" fill="#64748B">Conjunción</text>'
        '</svg>'
        + caja(150, 0, 400, 96, "dano", "", "Politraumatismo grave del trabajador", 22)
        + caja(30, 200, 400, 90, "hecho", "1", "Cae al vacío desde 6 m")
        + caja(470, 200, 230, 90, "hecho", "2", "Nada retiene la caída", 18)
        + caja(0, 420, 150, 140, "humano", "1.1", "Retrocede hacia el borde", 19)
        + caja(165, 420, 150, 140, "hecho", "1.2", "Los tablones basculan", 19)
        + caja(330, 420, 150, 140, "hecho", "1.3", "Lateral sin barandilla", 19)
        + '</div>')
    cuerpo = (f'<div style="display:flex;gap:40px;height:100%;align-items:center">'
              f'<div style="flex:1">{filas}</div>{arbol}</div>')
    notas = ("Empezamos por la lesión y hacemos la pregunta clave. Para que hubiera "
             "politraumatismo, el trabajador tuvo que caer desde 6 metros. ¿Hizo falta algo más? "
             "Sí: que nada lo retuviera. Como hacen falta los dos hechos a la vez, es una "
             "conjunción. Seguimos con la caída: tuvo que retroceder hacia el borde, los tablones "
             "tuvieron que bascular y el lateral tenía que estar sin barandilla. Es otra "
             "conjunción de tres hechos.")
    return {"html": marco("4 · Construcción del árbol", "Paso 1: desde la lesión", cuerpo),
            "notas": notas}


CH_W, CH_H = 290, 84
FLECHA = ('<svg width="52" height="30" style="flex:none"><path d="M2 15 H36" stroke="#334155" '
          'stroke-width="4"/><path d="M34 4 L50 15 L34 26 Z" fill="#334155"/></svg>')


def chip(tipo, ident, texto):
    f, b, c = TIPO[tipo]
    return (f'<div class="fit" style="flex:none;width:{CH_W}px;height:{CH_H}px;background:{f};'
            f'border:3px solid {b};color:{c};border-radius:12px;display:flex;align-items:center;'
            f'gap:12px;padding:0 14px;overflow:hidden"><span style="flex:none;background:#334155;'
            f'color:#fff;font-size:17px;font-weight:700;padding:4px 9px;border-radius:9px">'
            f'{ident}</span><span style="font-size:21px;line-height:1.2;font-weight:600">'
            f'{esc(texto)}</span></div>')


def cadena(items):
    partes = [chip(*it) for it in items]
    return '<div style="display:flex;align-items:center">' + FLECHA.join(partes) + "</div>"


def conjuncion(rama_a, rama_b, resultado):
    h = CH_H * 2 + 16
    a, b = CH_H // 2, CH_H + 16 + CH_H // 2
    llave = (f'<svg width="70" height="{h}" style="flex:none"><g stroke="#334155" '
             f'stroke-width="4" fill="none"><path d="M0 {a} H30 V{b} H0"/><path d="M30 {h // 2} '
             f'H54"/></g><path d="M52 {h // 2 - 11} L68 {h // 2} L52 {h // 2 + 11} Z" '
             f'fill="#334155"/></svg>')
    return (f'<div style="display:flex;align-items:center"><div style="display:flex;'
            f'flex-direction:column;gap:16px">{cadena(rama_a)}{cadena(rama_b)}</div>{llave}'
            f'{chip(*resultado)}</div>')


def s_construccion_2():
    C1 = ("causa", "C1", "Sin formación en altura")
    C2 = ("causa", "C2", "Montaje sin plan ni cualificación")
    C3 = ("causa", "C3", "Sin inspección del andamio")
    C4 = ("causa", "C4", "Planificación insuficiente")
    filas = [
        ("Rama 1.1", "Cadena", cadena([C1, ("humano", "1.1.1", "Desconoce el riesgo"),
                                       ("humano", "1.1", "Retrocede hacia el borde")])),
        ("Rama 1.2", "Conjunción", conjuncion(
            [C2, ("humano", "1.2.1", "Tablones sin sujetar")],
            [C3, ("humano", "1.2.2", "No se verifica el montaje")],
            ("hecho", "1.2", "Los tablones basculan"))),
        ("Rama 1.3", "Conjunción", conjuncion(
            [C3, ("humano", "1.3.1", "No se revisan las protecciones")],
            [C4, ("humano", "1.3.2", "Se retira la barandilla")],
            ("hecho", "1.3", "Lateral sin barandilla"))),
        ("Rama 2", "Cadena", cadena([C4, ("hecho", "2.1.1", "Sin arneses ni anclajes"),
                                     ("hecho", "2.1", "No lleva arnés"),
                                     ("hecho", "2", "Nada retiene la caída")])),
    ]
    html_filas = ""
    for i, (rama, rel, flujo) in enumerate(filas):
        borde = "border-top:2px solid #E2E8F0;" if i else ""
        html_filas += (f'<div style="display:flex;align-items:center;gap:30px;{borde}'
                       f'padding:11px 0"><div style="width:210px;flex:none">'
                       f'<div style="font-size:30px;font-weight:700;color:#1F3A5F">{rama}</div>'
                       f'<span class="tag" style="margin-top:8px">{rel}</span></div>{flujo}</div>')
    cuerpo = (f'<div style="display:flex;flex-direction:column;height:100%">'
              f'<div style="flex:1">{html_filas}</div>'
              f'<p style="font-size:24px;color:#475569"><b>C3 y C4 aparecen en dos ramas cada '
              f'una:</b> son disyunciones. Cada flecha va de la causa a su consecuencia.</p></div>')
    notas = ("Repetimos la pregunta en cada rama hasta llegar al origen. La rama 1.1 es una "
             "cadena: el trabajador retrocede porque desconoce el riesgo, y lo desconoce porque "
             "no recibió formación. La 1.2 es una conjunción: los tablones basculan porque se "
             "colocaron sin sujetar y porque nadie verificó el montaje. La 1.3 también: falta la "
             "barandilla porque se retiró para subir material y nadie revisó las protecciones. "
             "La rama 2 llega a la falta de arneses y anclajes. Fíjense que C3 y C4 aparecen dos "
             "veces: son disyunciones.")
    return {"html": marco("4 · Construcción del árbol", "Paso 2: hasta las causas primarias",
                          cuerpo), "notas": notas}


def s_arbol(png):
    cuerpo = (f'<div id="lienzo" style="background:#fff">'
              f'<img src="{png}" style="position:absolute;left:50%;top:14px;height:1052px;'
              f'transform:translateX(-50%)"></div>')
    notas = ("Este es el árbol completo. Arriba está la lesión y se lee de abajo hacia arriba: "
             "cada flecha va de una causa a su consecuencia. Los colores indican el tipo de "
             "hecho: azul para condiciones materiales, amarillo para factores humanos y verde "
             "para las causas primarias. Todas las ramas terminan en cuatro cajas verdes, que son "
             "fallos de organización.")
    return {"html": documento(cuerpo), "notas": notas}


def s_causas():
    causas = [
        ("C1", "Formación", "No se imparte formación ni información sobre riesgos de trabajos "
                            "en altura.", "1.1.1", False),
        ("C2", "Montaje", "El montaje se encarga a personal sin cualificación y sin plan de "
                          "montaje.", "1.2.1", False),
        ("C3", "Inspección y supervisión", "No hay procedimiento ni responsable designado para "
                                           "inspeccionar el andamio.", "1.2.2 y 1.3.1", True),
        ("C4", "Planificación preventiva", "No se evalúa el riesgo de caída ni se prevén medios "
                                           "seguros para subir materiales ni arneses.",
         "1.3.2 y 2.1.1", True),
    ]
    cards = ""
    for c, t, d, orig, dis in causas:
        badge = ('<span class="tag" style="background:#2E7D32;color:#fff;margin-left:auto">'
                 'Disyunción · 2 hechos</span>' if dis else "")
        cards += (f'<div class="card" style="background:#EAF6E6;border:3px solid #2E7D32">'
                  f'<div style="display:flex;align-items:center;gap:16px;margin-bottom:12px">'
                  f'<span class="chip" style="font-size:24px">{c}</span>'
                  f'<h3 style="margin:0;color:#0F3A12">{esc(t)}</h3>{badge}</div>'
                  f'<p style="font-size:31px">{esc(d)}</p><p style="margin-top:14px;font-size:28px;color:#2E7D32">'
                  f'<b>Origina:</b> {orig}</p></div>')
    cuerpo = (f'<div style="display:flex;flex-direction:column;height:100%">'
              f'<div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;'
              f'flex:1">{cards}</div>'
              f'<div class="card" style="background:#1F3A5F;border-color:#1F3A5F;margin-top:24px">'
              f'<p style="color:#fff;font-size:28px">Las cuatro son <b>fallos de organización</b>: '
              f'permitieron que los fallos técnicos y la conducta del trabajador quedaran sin '
              f'controlar.</p></div></div>')
    notas = ("Llegamos a cuatro causas primarias. C1, falta de formación. C2, un montaje sin "
             "plan y sin personal cualificado. C3, nadie inspecciona el andamio. C4, una "
             "planificación preventiva insuficiente. C3 y C4 originan dos hechos cada una, en "
             "ramas distintas. Como dice la NTP 274, las causas primarias son fallos de "
             "organización: son los que permiten que los fallos técnicos y humanos no se "
             "controlen.")
    return {"html": marco("5 · Causas primarias", "Los fallos de organización de origen", cuerpo),
            "notas": notas}


def s_medidas():
    medidas = [
        ("C1", "Formación", ["Formación en altura, andamios y anticaídas antes de empezar",
                             "Instrucción: no trabajar sin protección completa"], "1.1.1"),
        ("C2", "Montaje", ["Montaje por personal competente y con plan de montaje",
                           "Plataformas sujetas, barandilla completa y rodapié"], "1.2.1"),
        ("C3", "Inspección", ["Revisión tras el montaje, cada jornada y tras cambios",
                              "Responsable designado y registro «apto / no apto»"],
         "1.2.2 y 1.3.1"),
        ("C4", "Planificación", ["Evaluar el riesgo y prever un medio para subir materiales",
                                 "Arneses, puntos de anclaje y responsable de seguridad"],
         "1.3.2 y 2.1.1"),
    ]
    cards = "".join(
        f'<div class="card" style="background:#fff;border-top:8px solid #2E7D32">'
        f'<div style="display:flex;align-items:center;gap:14px;margin-bottom:12px">'
        f'<span class="chip" style="background:#2E7D32">{c}</span><h3 style="margin:0">{esc(t)}'
        f'</h3><span style="margin-left:auto;font-size:21px;color:#64748B">Corrige {cor}</span>'
        f'</div>{lista(items, 30)}</div>' for c, t, items, cor in medidas)
    inmediatas = ('<div class="card" style="background:#FBEAEA;border-color:#8E2A2A;'
                  'display:flex;align-items:center;gap:26px;margin-bottom:24px">'
                  '<h3 style="margin:0;color:#8E2A2A;flex:none">Inmediatas</h3>'
                  '<p style="font-size:25px">Paralizar e inspeccionar el andamio · fijar las '
                  'plataformas y reponer barandillas · revisar los demás andamios</p></div>')
    cuerpo = (f'<div style="display:flex;flex-direction:column;height:100%">{inmediatas}'
              f'<div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;'
              f'flex:1">{cards}</div></div>')
    notas = ("Proponemos una medida para cada causa primaria. Primero, medidas inmediatas: parar "
             "y revisar el andamio. Para C1, formación en altura antes de empezar. Para C2, que "
             "monte personal competente con plan de montaje y plataformas bien sujetas. Para C3, "
             "un procedimiento de inspección con responsable y registro. Para C4, evaluar el "
             "riesgo, prever cómo subir materiales sin quitar barandillas y disponer de arneses "
             "y anclajes.")
    return {"html": marco("6 · Medidas", "Medidas preventivas propuestas", cuerpo),
            "notas": notas}


def s_conclusiones():
    ideas = [
        "El accidente necesitó **dos ramas a la vez**: la caída y la falta de un sistema que la "
        "detuviera.",
        "Todas las ramas terminan en **cuatro causas primarias de organización**: formación, "
        "montaje, inspección y planificación.",
        "**C3 y C4 actúan en varias ramas**: corregirlas primero tiene más efecto.",
        "Culpar al trabajador no basta: con tablones sueltos, borde abierto y sin anclajes, "
        "**cualquier otro habría estado expuesto**.",
    ]
    filas = "".join(
        f'<div class="card" style="display:flex;gap:28px;align-items:center;background:#fff">'
        f'<div class="num" style="width:74px;height:74px;font-size:36px">{i}</div>'
        f'<p style="font-size:31px">{esc(t)}</p></div>' for i, t in enumerate(ideas, 1))
    cuerpo = (f'<div class="grid" style="grid-template-rows:repeat(4,1fr);height:100%">'
              f'{filas}</div>')
    notas = ("Para cerrar, cuatro ideas. El accidente necesitó dos cosas a la vez: caer y que "
             "nada lo detuviera. Todas las ramas llevan a cuatro fallos de organización. C3 y C4 "
             "aparecen en varias ramas, así que son las primeras que conviene corregir. Y lo más "
             "importante: culpar al trabajador no soluciona nada, porque las condiciones que "
             "permitieron el accidente seguirían ahí para cualquier otro.")
    return {"html": marco("6 · Conclusiones", "Conclusiones", cuerpo), "notas": notas}


def s_cierre():
    refs = ["Piqué Adanuy, T. (1992). NTP 274: Investigación de accidentes: árbol de causas. INSHT.",
            "UNE-EN 12811-1: Andamios. Requisitos de comportamiento y diseño.",
            "UNE-EN 361: Arneses anticaídas. · UNE-EN 795: Dispositivos de anclaje.",
            "España: RD 1215/1997, modificado por el RD 2177/2004.",
            "Colombia: Resolución 4272 de 2021 (trabajo en alturas)."]
    cuerpo = (
        '<div id="lienzo" style="background:linear-gradient(135deg,#1F3A5F 0%,#2B5583 100%)">'
        '<div style="position:absolute;left:96px;top:300px;width:760px">'
        '<div style="font-size:112px;font-weight:700;color:#fff;line-height:1">¿Preguntas?</div>'
        '<div style="font-size:44px;color:#9CC3E6;margin-top:30px">Gracias por su atención</div>'
        '</div><div class="card" style="position:absolute;left:960px;top:200px;width:864px;'
        'height:auto;background:#fff;border:0"><h3 style="font-size:36px;margin-bottom:24px">'
        'Referencias</h3>' + lista(refs, 29) + '</div></div>')
    notas = ("Cerramos la presentación y quedamos atentos a sus preguntas. Las referencias "
             "principales son la NTP 274 del INSHT y la normativa sobre andamios y trabajo en "
             "altura.")
    return {"html": documento(cuerpo), "notas": notas}


def diapositivas(png_arbol):
    lista_s = [portada(), s_contenido(), s_que_es(), s_como(), s_relaciones(), s_datos(),
               s_relato(), s_toma(), s_construccion_1(), s_construccion_2(), s_arbol(png_arbol),
               s_causas(), s_medidas(), s_conclusiones(), s_cierre()]
    total = len(lista_s)
    for n, s in enumerate(lista_s, 1):
        s["html"] = s["html"].replace("{N}", str(n)).replace("{TOTAL}", str(total))
    return lista_s
