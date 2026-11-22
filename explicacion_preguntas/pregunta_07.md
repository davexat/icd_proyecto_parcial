# Pregunta de negocio 7: tipo de siniestro y vehículos

> **Pregunta:** ¿Qué tipos de siniestro y qué vehículos involucrados concentran la mayor gravedad, y esa gravedad cambia entre zona urbana y rural?

**Script:** `pregunta_07.py`
**Técnicas:** tabla de gravedad por tipo de siniestro, comparación del % de siniestros fatales con y sin cada tipo de vehículo, gráfico facetado urbano vs rural y heatmap tipo de siniestro × vehículo.

## 1. Qué hace el código

**Bloque 1: tipo de siniestro.** `gravedad()` por `tipo_siniestro` (13 tipos), ordenado por % de siniestros con fallecidos. Guarda `p07_gravedad_por_tipo_siniestro.csv`.

**Bloque 2: vehículo involucrado.** Para cada tipo de vehículo (con al menos 30 siniestros) compara el % de siniestros fatales *cuando participa* ese vehículo contra *cuando no participa*, y calcula la razón entre ambos ("veces más fatales"). También mira el % de fatales según el número de vehículos (4 = 4 o más). Guarda `p07_gravedad_por_vehiculo.csv`.

**Bloque 3: facetas urbano vs rural.** Dos paneles de barras horizontales, uno por zona, con los tipos de siniestro con 100 o más casos y el eje compartido. Se omiten las combinaciones con menos de 30 siniestros.

**Bloque 4: heatmap tipo × vehículo 1.** Matriz del % de siniestros con fallecidos por tipo de siniestro y tipo del vehículo 1, omitiendo celdas con menos de 30 casos.

## 2. Para la exposición (máx. 40 s)

> Cada panel muestra el porcentaje de siniestros con fallecidos por tipo, uno para zona urbana y otro rural, con el mismo eje. Lo más grave son los eventos de un solo actor: atropellos, choques frontales, pérdidas de pista y volcamientos. Lo más frecuente, el choque lateral, es de lo menos letal. Y en todos los tipos la barra rural es más larga: la letalidad casi se duplica. En el heatmap, los siniestros con bus son 1.85 veces más fatales y con moto 1.72 veces. La gravedad depende del tipo, del vehículo y de la zona.

*Figura a mostrar:* `p07_gravedad_tipo_por_zona.png` (apoyo: `p07_heatmap_tipo_vehiculo.png`). 95 palabras, unos 38 s a ritmo normal.

## 3. Resultados

**Por tipo de siniestro (% con fallecidos):**

| Tipo | Siniestros | % con fallecidos |
|---|---|---|
| Arrollamientos | 153 | **45.8** |
| Pérdida de pista | 504 | 22.4 |
| Choque frontal | 1 142 | 19.4 |
| Volcamientos | 218 | 15.1 |
| Atropellos | 1 992 | 14.2 |
| Choque lateral | 4 858 | 4.8 |
| Colisión | 482 | 2.9 |

El choque frontal es también el de más víctimas por siniestro (1.37).

**Por vehículo involucrado:**

| Vehículo | Siniestros | % fatales con él | % fatales sin él | Veces más fatales |
|---|---|---|---|---|
| Bus | 862 | 17.1 | 9.2 | **1.85** |
| Motocicleta | 5 647 | 13.4 | 7.8 | **1.72** |
| Camión | 1 680 | 13.3 | 9.2 | 1.44 |
| Camioneta | 2 750 | 6.1 | 10.3 | 0.59 |
| SUV | 2 056 | 5.3 | 10.2 | 0.52 |
| Automóvil | 6 242 | 4.2 | 12.7 | **0.33** |

**Por número de vehículos:** 1 vehículo, 12.3 % fatales; 2 vehículos, 7.2 %; 3, 7.4 %; 4 o más, 4.1 %.

**Urbano vs rural (% con fallecidos, cálculo aparte para los casos principales):**

| Tipo | Urbana | Rural |
|---|---|---|
| Atropellos | 11.3 | 21.3 |
| Choque frontal | 14.1 | 22.5 |
| Pérdida de pista | 18.9 | 24.4 |
| Volcamientos | 9.5 | 18.7 |
| Choque lateral | 3.7 | 8.2 |

## 4. Análisis

1. **Los eventos "de un solo actor" son los más graves.** Arrollamientos, pérdidas de pista y volcamientos tienen una letalidad alta; y los siniestros de un solo vehículo (12.3 %) son más mortales que los de dos (7.2 %).
2. **Lo más frecuente es lo menos grave.** El choque lateral es el tipo más común (4 858) y de los menos letales (4.8 %).
3. **El bus y la moto elevan el riesgo; el automóvil lo reduce.** Los siniestros con bus son 1.85 veces más fatales que los que no lo incluyen; con moto, 1.72. El automóvil aparece con 0.33: los siniestros donde participa un automóvil son bastante menos letales (4.2 % frente a 12.7 %). Es una asociación, no prueba que el automóvil proteja por sí solo.
4. **La zona rural es más grave en todos los tipos.** Casi se duplica la letalidad de atropellos, choques frontales y volcamientos al pasar de urbano a rural.
5. En el heatmap destaca que el arrollamiento tiene un 49 % de fatales cuando el vehículo 1 aparece como "no identificado"; de hecho, 74 de los 153 arrollamientos tienen un vehículo no identificado. Puede sugerir fuga del conductor, pero el dato no lo confirma.

## 5. Limitaciones y advertencias

- Arrollamientos tiene solo 153 casos; es un porcentaje alto, pero con una base pequeña.
- La razón "veces más fatales" compara con y sin el vehículo; no controla otras variables (tipo de vía, velocidad, hora), por lo que no es causal.
- Hay un 22 % de siniestros con el tipo del vehículo 1 sin identificar (parte del ruido global).
- Las etiquetas del heatmap acortan "Vehículo deportivo utilitario" a "Vehículo Depor".

## 6. Archivos generados

- Tablas: `p07_gravedad_por_tipo_siniestro.csv`, `p07_gravedad_por_vehiculo.csv`
- Figuras: `p07_gravedad_tipo_por_zona.png`, `p07_heatmap_tipo_vehiculo.png`
