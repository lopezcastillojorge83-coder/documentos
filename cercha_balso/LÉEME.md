# Cercha de balso: opciones de 40 a 50 barras

Láminas con tres ideas de cercha para el proyecto final de Ingeniería de los Materiales. Todas mantienen las medidas del prototipo: 40 cm de base y 20 cm de alto, con dos caras iguales unidas por barras de soporte. La cuerda inferior de cada cara es una sola barra de 40 cm.

| Opción | Barras | Barra crítica | Resistencia al pandeo (relativa a la opción 2) |
|---|---|---|---|
| 1 · Warren en W | 41 | B–F y F–C (−0.17P, 20.6 cm) | 1.8× |
| 2 · Pratt arriostrada | 44 | C–G (−0.33P, 20.0 cm) | 1.0× |
| 3 · Warren de 4 nodos | 50 | B–G y H–D (−0.26P, 20.6 cm) | 1.2× |

La opción 1 es la recomendada: es la más resistente y la que usa menos barras.

## Láminas

![Comparación](04_comparacion_opciones.png)
![Opción 1](01_opcion1_warren_w_41barras.png)
![Opción 2](02_opcion2_pratt_arriostrada_44barras.png)
![Opción 3](03_opcion3_warren_arriostrada_50barras.png)

Cada lámina trae la vista frontal con la fuerza de cada barra, una vista 3D con las barras de soporte (transversales, diagonales superiores y de portal), la tabla de fuerzas, la lista de corte y notas.

## Cómo se cuentan las barras

- La cuerda inferior de cada cara es una sola barra de 40 cm. Para el cálculo se divide en tramos entre nodos, pero se corta y se cuenta como una pieza. Las demás barras se pegan sobre ella en los nodos marcados.
- Las demás barras cuentan una por tramo entre nodos.
- Hay una transversal en cada nodo, uniendo la cara de adelante con la de atrás.
- Las diagonales superiores arriostran la parte de arriba. Las diagonales de portal arriostran los planos inclinados de los extremos.

## Supuestos

- P es la carga que recibe una cara, es decir, la mitad de la carga de la máquina. Se reparte por igual entre los nodos de arriba.
- Nodos articulados. Signo: + tensión, − compresión.
- La barra crítica es la comprimida con mayor |F|·L², que es la que se pandea primero si todas las barras tienen la misma sección.
- Separación entre caras b = 10 cm. Cámbiala por tu medida real.

## Volver a generar las láminas

```bash
python3 generar_laminas.py        # b = 10 cm
python3 generar_laminas.py 12     # b = 12 cm
```

El script solo usa Python estándar. Calcula las fuerzas por el método de nodos y escribe los archivos `.svg`. Los `.png` se exportaron desde los `.svg` con un navegador.
