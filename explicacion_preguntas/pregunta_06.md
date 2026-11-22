# Pregunta de negocio 6: causas y factores

> **Pregunta:** ¿Qué causas probables (y qué factores: humano, vehículo o vía) explican la mayor parte de los siniestros, cuáles se asocian a mayor gravedad y cambia su peso según la hora del día?

**Script:** `pregunta_06.py`
**Técnicas:** Pareto de causas, porcentaje por factor, gravedad por grupo de causa, gráfico de burbujas (frecuencia vs gravedad) y heatmaps causa × franja horaria.
**Features nuevas usadas:** `causa_grupo` y `factor_causal` (Haddon, 1968; Sabey y Taylor, 1980).

## 1. Qué hace el código

**Bloque 1: frecuencia de causas.** Cuenta los siniestros por código de causa (26 códigos), acorta el texto de cada causa para poder mostrarlo y aplica `pareto_abc()`. Después imprime el porcentaje de siniestros por factor causal (humano, vehículo, vía y entorno), una columna que `limpieza_datos.py` deriva agrupando los códigos.

**Bloque 2: gravedad por grupo de causa.** Con `gravedad()` calcula, para cada uno de los 10 grupos de causa, siniestros, fallecidos y % de siniestros con fallecidos. Guarda `p06_gravedad_por_grupo_causa.csv`.

**Bloque 3: gráficos.** Izquierda: barras horizontales con el Top 10 de causas. Derecha: burbujas, donde el eje X es la frecuencia (escala logarítmica, porque hay grupos de 21 y de 4 956 siniestros), el eje Y el % de siniestros con fallecidos y el tamaño de la burbuja el número de fallecidos. El color indica el factor y una línea punteada marca el promedio nacional (9.6 %).

**Bloque 4: heatmaps causa × franja.** Dos mapas con las mismas filas: (a) el peso de cada causa dentro de cada franja horaria (cada columna suma 100 %) y (b) el % de siniestros con fallecidos por causa y franja, omitiendo celdas con menos de 30 siniestros.

## 2. Para la exposición (máx. 40 s)

> En las barras vemos que distracción y velocidad son las dos causas más frecuentes, y que casi todo es factor humano: 94.5 %. En las burbujas, cada una es un grupo de causa; más a la derecha es más frecuente y más arriba es más letal. Distracción y velocidad están arriba de la línea del promedio, mientras el irrespeto de señales es frecuente pero poco letal. Y según el heatmap, de madrugada crecen velocidad, alcohol y fatiga. La prevención debe apuntar al comportamiento del conductor, sobre todo en la noche.

*Figura a mostrar:* `p06_pareto_y_burbujas.png` (apoyo: `p06_heatmaps_causa_franja.png`). 90 palabras, unos 36 s a ritmo normal.

## 3. Resultados

**Top causas** (28.8 %, 19.3 %, 13.5 %, 6.4 %, 5.6 %, 4.3 %, 4.2 % acumulan 82.1 %, clase A):

| Causa | % de siniestros |
|---|---|
| Conducir desatento a las condiciones de tránsito | 28.8 |
| Superar los límites de velocidad | 19.3 |
| No respetar las señales reglamentarias | 13.5 |
| No mantener la distancia prudencial | 6.4 |
| Conducir bajo la influencia de alcohol o sustancias | 5.6 |

**Factor causal:** humano 94.5 %, vía y entorno 4.3 %, vehículo 1.2 %.

**Gravedad por grupo de causa** (promedio nacional 9.6 %):

| Grupo | Siniestros | % con fallecidos |
|---|---|---|
| Vía y entorno | 744 | 12.8 |
| Distracción al conducir | 4 956 | 12.2 |
| Exceso de velocidad | 3 331 | 12.0 |
| Maniobras y distancia | 2 652 | 8.3 |
| Alcohol / sustancias | 1 044 | 5.8 |
| Irrespeto de señales / prioridad | 3 382 | 4.8 |

("Otras infracciones", con 21 siniestros y 14.3 %, no se interpreta por su tamaño.)

**Por franja horaria:** el exceso de velocidad pasa de 16.8 % de los siniestros en la tarde a **26.0 % en la madrugada**; el alcohol, de 3.2 % en la mañana a **10.0 % en la madrugada**; la fatiga, de 0.3 % en la tarde a 2.7 %. El irrespeto de señales cae de 23.0 % en la tarde a 12.2 % en la madrugada. La distracción se mantiene en ~28 a 30 % a toda hora.

## 4. Análisis

1. **Casi todo es factor humano** (94.5 %). Vehículo y vía suman solo 5.5 %, así que cualquier medida de prevención debe apuntar al comportamiento del conductor.
2. **Dos causas explican casi la mitad:** distracción y velocidad (48.1 %). Son también las dos más graves entre las frecuentes (12.2 % y 12.0 % de siniestros con fallecidos, frente al 9.6 % nacional).
3. **Frecuente no es lo mismo que grave.** El irrespeto de señales es la tercera causa en volumen pero una de las menos letales (4.8 %); una hipótesis es que produce sobre todo choques laterales en intersecciones, que suelen ocurrir a menor velocidad (el dataset no lo comprueba).
4. **Cambia con la hora.** De madrugada pesan más la velocidad, el alcohol y la fatiga, justo cuando también aumenta la letalidad (ver pregunta 5). De día pesa más el irrespeto de señales y prioridad (22 a 23 % de los siniestros, frente a 12 % de madrugada). La distracción es la primera causa a toda hora (28 a 30 %).

## 5. Limitaciones y advertencias

- **El alcohol sale con baja letalidad (5.8 %), lo que contradice la intuición.** No debe presentarse como "el alcohol es poco peligroso". Lo más probable es un sesgo de registro: la causa se anota cuando se detecta en un control, y eso ocurre más en siniestros leves. Es una hipótesis, el dataset no permite confirmarla.
- La causa es la *probable* registrada por el ente de control, no una causa verificada.

## 6. Archivos generados

- Tabla: `p06_gravedad_por_grupo_causa.csv`
- Figuras: `p06_pareto_y_burbujas.png`, `p06_heatmaps_causa_franja.png`
