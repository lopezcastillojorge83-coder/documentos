# Investigación del accidente de trabajo grave del 13/08/2026 (integrante 4)

Seguridad y Salud en el Trabajo, actividad 2 (Universidad Distrital, 2026-3). Este es el componente del integrante 4: metodología OSALAN y formatos legales.

Caso: caída de 4,35 m desde un banco de lavado de aeronaves en la posición Golfo del Aeropuerto El Dorado. El trabajador sufrió un trauma craneoencefálico severo, lo que hace que el accidente sea grave.

## Archivos

| Archivo | Contenido |
|---|---|
| [`../furat.xls`](../furat.xls) | **El mismo formulario original de ARL SURA** (F 2015-PR v3), diligenciado directamente en la raíz. Conserva las 3 hojas, el proyecto VBA, los controles ActiveX, el formato y las imágenes originales. No es una transcripción ni un Excel nuevo. |
| `02_Investigacion_OSALAN_Causas_PlanMejoramiento_Integrante4.docx` | Informe en Word: árbol de causas (método OSALAN) con pasos, hechos e hipótesis; cálculo de caída libre y claridad; formato de investigación de la Res. 1401 de 2007 con causas inmediatas y básicas; plan de mejoramiento; costos ocultos con tres artículos Q1; referencias IEEE. |
| `figuras/` | Secuencia cronológica, árbol de causas y esquema de claridad en PNG. |
| `_fuente/` | Scripts de apoyo. `_fuente/furat_xls/` contiene el diligenciamiento binario reproducible del FURAT original. |

## Estado del FURAT

Se diligenciaron los campos aplicables del caso, incluidas las casillas sombreadas para la entrega académica: códigos EPS, ARL, AFP, actividad económica, centro de trabajo, departamento, municipio y ocupación. Los campos condicionados que no aplican indican `NO APLICA`. Las casillas seleccionadas tienen valor ActiveX y una marca visible estática.

La firma no se falsificó: el campo indica `PENDIENTE DE FIRMA MANUSCRITA`.

Los datos de empresa y contacto son supuestos académicos. Los códigos usados son: EPS SURA `EPS010`; ARL SURA `14-28`; AFP Protección `230201`; Bogotá D.C. `11/11001`; actividad de limpieza industrial y de aeronaves `4812901` (CIIU 8129, clase IV, subactividad 01); ocupación `91120`; centro de trabajo ficticio `001`.

## Pendiente antes de entregar

1. Confirmar que el árbol de causas no fue asignado a otro grupo.
2. Reemplazar, si el docente suministra los datos reales, el nombre y NIT de la empresa, EPS, AFP, salario, responsable del FURAT y peso del trabajador (70 kg).
3. Firmar el FURAT manualmente y completar los nombres del equipo investigador, sus firmas y la copia de la licencia en el informe de investigación.
4. Revisar las inconsistencias de la guía (tabla 2 del Word): fecha del turno, nombre de la clínica, apellidos y norma ANSI.
5. Descargar los PDF de los tres artículos desde la Biblioteca UD, verificar su cuartil en SJR y anexarlos.
6. Abrir el Word y el `furat.xls` en Excel de escritorio; revisar la página horizontal del árbol de causas y la impresión del FURAT.

## Regenerar los archivos

Requiere Python 3. Las figuras requieren además Chrome o Chromium en modo headless.

```bash
CHROME_BIN=/ruta/a/chrome python _fuente/gen_figs.py
python _fuente/gen_doc.py
python _fuente/validate.py 02_Investigacion_OSALAN_Causas_PlanMejoramiento_Integrante4.docx
```

Los datos del FURAT están en `_fuente/furat_xls/targets.py`. El script `fill_furat.py` debe ejecutarse una sola vez sobre una copia limpia del `furat.xls` original; acepta la misma ruta como entrada y salida para diligenciarlo en el mismo archivo:

```bash
python _fuente/furat_xls/fill_furat.py ../furat.xls ../furat.xls
```
