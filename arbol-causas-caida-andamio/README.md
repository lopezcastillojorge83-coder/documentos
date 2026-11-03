# Árbol de causas — Caída de altura desde un andamio (NTP 274)

Investigación de un accidente de trabajo (caída de altura desde un andamio
durante trabajos de reparación de fachada) aplicando el método del **árbol de
causas** de la **NTP 274** del INSHT.

## Entregables

| Archivo | Descripción |
|---------|-------------|
| `Arbol_de_Causas_Caida_Andamio.docx` | Informe completo (editable). |
| `Arbol_de_Causas_Caida_Andamio.pdf` | Misma versión en PDF (7 páginas). |
| `arbol_de_causas.png` | Solo el diagrama del árbol, para la exposición. |

## Pendiente antes de entregar

1. **Portada:** completar nombre completo y código de cada integrante.
   Revisar también la asignatura («Seguridad (Gr. 23)») y el docente
   («Germán Suárez»).
2. **Hechos del caso:** los hechos concretos (altura, tablones sueltos, falta
   de arnés, etc.) son un **supuesto de trabajo**, indicado como tal en una nota
   del informe. Si existen datos reales del caso, deben sustituirse.
3. **Referencias:** incluye normativa de España y de Colombia; conservar solo
   la aplicable.

## Carpeta `_fuente/` (scripts que generan el informe)

El informe y el diagrama se generan por código, sin dependencias externas de
`pip` (se usan solo la biblioteca estándar de Python y Chromium para el
renderizado).

| Archivo | Función |
|---------|---------|
| `arbol.py` | Datos del árbol: nodos, antecedentes, tipo de relación y posiciones. |
| `contenido.py` | Contenido del informe por secciones (independiente del formato). |
| `diagrama.py` | Construye el diagrama (HTML + SVG) y lo renderiza a PNG. |
| `render_docx.py` | Escribe el `.docx` (OOXML) con la biblioteca estándar. |
| `render_html.py` | Renderiza el informe a HTML y lo imprime a PDF. |
| `render.js` | Renderizado con Chromium (PNG y PDF). |
| `validar_docx.py` | Validación estructural del `.docx` (orden OOXML, relaciones, tablas). |
| `construir.py` | Genera diagrama, DOCX y PDF. Uso: `python3 construir.py [carpeta_salida]`. |

### Regenerar los entregables

```bash
cd _fuente
python3 construir.py ..
```

Requiere Python 3 y un Chromium accesible en `/usr/local/bin/chrome` (ajustar
la ruta en `render.js` si es distinta).
