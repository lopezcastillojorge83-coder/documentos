# Investigación del accidente de trabajo grave del 13/08/2026 (integrante 4)

Seguridad y Salud en el Trabajo, actividad 2 (Universidad Distrital, 2026-3). Este es el componente del integrante 4: metodología OSALAN y formatos legales.

Caso: caída de 4,35 m desde un banco de lavado de aeronaves en la posición Golfo del Aeropuerto El Dorado. El trabajador sufrió un trauma craneoencefálico severo, lo que hace que el accidente sea grave.

## Archivos

| Archivo | Contenido |
|---|---|
| `01_FURAT_ARL_SURA_AT_13-08-2026_diligenciado.xls` | **El formulario original de ARL SURA** (`furat.xls`, F 2015-PR v3) diligenciado sobre el mismo archivo: mismas hojas, macros, formato y casillas. Solo se llenaron los campos y se marcaron las casillas. |
| `01_FURAT_ARL_SURA_AT_13-08-2026_diligenciado.xlsx` | Versión anterior (reproducción del formato) con la hoja "Notas y supuestos", que indica la fuente de cada dato. |
| `02_Investigacion_OSALAN_Causas_PlanMejoramiento_Integrante4.docx` | Informe en Word: árbol de causas (método OSALAN) con pasos, hechos e hipótesis; cálculo de caída libre y claridad; formato de investigación de la Res. 1401 de 2007 con causas inmediatas y básicas; plan de mejoramiento; costos ocultos con tres artículos Q1; referencias IEEE. |
| `figuras/` | Secuencia cronológica, árbol de causas y esquema de claridad en PNG. |
| `_fuente/` | Scripts en Python que generan el Excel, el Word y las figuras. `_fuente/furat_xls/` llena el `furat.xls` original. |

## Pendiente antes de entregar

1. Confirmar que el árbol de causas no fue asignado a otro grupo.
2. Reemplazar los datos supuestos: nombre y NIT de la empresa, EPS, AFP y sus códigos, salario, responsable del FURAT y peso del trabajador (70 kg).
3. Completar los nombres de los integrantes del equipo investigador, las firmas y la copia de la licencia.
4. Revisar las inconsistencias de la guía (tabla 2 del Word): fecha del turno, nombre de la clínica, apellidos y norma ANSI.
5. Descargar los PDF de los tres artículos desde la Biblioteca UD, verificar su cuartil en SJR y anexarlos.
6. En el FURAT original quedaron en blanco las casillas sombreadas (códigos de EPS, ARL, AFP, actividad, municipio y ocupación), que son de uso de la ARL, y la firma.
7. Abrir el Word y el Excel y revisar la página horizontal del árbol de causas y la impresión del FURAT.

## Regenerar los archivos

Requiere Python 3. Las figuras requieren además Chrome o Chromium en modo headless.

```bash
CHROME_BIN=/ruta/a/chrome python _fuente/gen_figs.py
python _fuente/gen_furat.py
python _fuente/gen_doc.py
python _fuente/validate.py *.xlsx *.docx
# FURAT original: datos en _fuente/furat_xls/targets.py
python _fuente/furat_xls/fill_furat.py ../furat.xls 01_FURAT_ARL_SURA_AT_13-08-2026_diligenciado.xls
python _fuente/furat_xls/validate_xls.py ../furat.xls 01_FURAT_ARL_SURA_AT_13-08-2026_diligenciado.xls
```
