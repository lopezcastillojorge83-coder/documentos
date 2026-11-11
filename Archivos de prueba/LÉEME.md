# Archivos de prueba — Material nuevo "Inox 304"

Estos archivos `.TXT` simulan un **material nuevo ficticio pero físicamente coherente**
(Acero Inoxidable 304) para probar el libro `Laboratorio Tensión Flexión.xlsx`.
Tienen el **mismo formato exacto** que los archivos reales de la máquina de ensayos
(encabezado, columnas Load/Stroke/Elong/Width, carga en `tf`, decimales con coma).

## Archivos

| Archivo | Carpeta destino | Registros |
|---|---|---|
| `inox304 a tensión.TXT` | `tensión/` | 520 |
| `inox304 a flexión.TXT` | `flexión/` | 1100 |

## Geometría usada

- Tensión: diámetro d₀ = 12,5 mm → A₀ = 122,72 mm²; L₀ = 100 mm
- Flexión: diámetro d = 16 mm; luz L = 200 mm

## Valores que DEBERÍA calcular el Excel (para verificar)

| Propiedad | Valor esperado |
|---|---|
| **Su** (tensión) = Fmax/A₀ | **≈ 580 MPa** |
| Fmax (tensión) | ≈ 71.177 N (7,258 tf) |
| **σf máx** (flexión) = 8·F·L/(π·d³) | **≈ 722 MPa** |
| Fmax (flexión) | ≈ 5.808 N |
| E de referencia (encabezado) | 193 GPa |

> ⚠️ Recuerda: como el ensayo es **sin extensómetro** (Elong = 0), el **módulo E
> medido** saldrá mucho más bajo que 193 GPa (igual que con tus otros materiales).
> Eso es esperado y el libro lo marcará en amarillo/rojo. El valor fiable para
> comparar es **Su** y **σf máx**.

## Cómo probarlo

1. Copia `inox304 a tensión.TXT` en tu carpeta `tensión` y `inox304 a flexión.TXT` en `flexión`.
2. En la hoja **Control** (sección 1), registra el material en una fila libre:
   - Material: `Inox 304`
   - Palabra clave (columna D): `inox304`
3. **Datos → Actualizar todo**.
4. Elige `Inox 304` en la celda **B10** y revisa **Inspección** y **Alertas**.
5. Compara el **Su** y el **σf máx** con la tabla de arriba.
