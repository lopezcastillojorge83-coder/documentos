# Predicción del movimiento del carro

Proyecto de Física I · Avance 2 · Jorge López, Laura Baquero y David Pinilla

## Datos del prototipo

| Símbolo | Magnitud | Valor |
|---|---|---|
| m | Masa del contrapeso | 50 g = 0,050 kg |
| M | Masa del carro | 0,204 kg |
| R | Radio de las ruedas (CD) | 6 cm = 0,06 m |
| r | Radio del carrete | 1 cm = 0,01 m |
| h | Altura de caída del contrapeso | 15 cm = 0,15 m |
| g | Gravedad | 9,81 m/s² |
| μ | Coef. de fricción de rodadura (CD sobre piso) | 0,025 |

## 1. Energía que mueve el carro

El contrapeso, al caer una altura h, pierde energía potencial gravitatoria, la única energía que recibe el carro:

**Ep = m · g · h = 0,050 · 9,81 · 0,15 = 0,074 J**

## 2. Relación entre la rueda y el carrete

El hilo se enrolla en el carrete (radio r) y las ruedas tienen radio R. Por cada vuelta del eje el carro avanza R mientras el hilo solo suelta r:

**k = R / r = 0,06 / 0,01 = 6**

El carro avanza 6 veces lo que baja el contrapeso. Con ruedas grandes de CD, recorre bastante distancia ya durante la caída.

## 3. Distancia que recorre el carro

El carro arranca y termina en reposo, así que toda la energía potencial se gasta en vencer la fricción de rodadura a lo largo del recorrido. La fricción es F = μ·(M + m)·g. Igualando la energía que entra con el trabajo de la fricción:

**m · g · h = μ · (M + m) · g · D**

Despejando la distancia (la g se cancela):

**D = m · h / [ μ · (M + m) ] = (0,050 · 0,15) / (0,025 · 0,254) = 1,18 m**

El carro recorre 1,18 m, cumpliendo el requisito de avanzar un metro o más. La velocidad máxima es de unos 0,4 m/s y el tiempo total de unos 6 s.

## 4. Cómo se mueve en el tiempo

Mientras el contrapeso cae sus 15 cm, el carro avanza d1 = k·h = 6·0,15 = 0,90 m y gana velocidad. Cuando el contrapeso llega al chasis, el hilo se suelta y el carro sigue por inercia unos 0,28 m más, hasta frenarse. La velocidad más alta (unos 0,4 m/s) la alcanza al final de la caída, y se detiene unos 6 s después de soltarlo.

## Conclusión

Con ruedas de CD de 6 cm de radio y un contrapeso de 50 g que cae 15 cm, el carro recorre 1,18 m en línea recta, cumpliendo el requisito de avanzar un metro o más. El valor de la fricción es una estimación, por eso el contrapeso es ajustable: en la prueba real se mide la distancia y, si hace falta, se le agrega o se le quita arena.
