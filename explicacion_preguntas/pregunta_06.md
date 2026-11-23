# Pregunta de negocio 6: causas y factores

> **Pregunta:** ¿Qué causas probables (y qué factores: humano, vehículo o vía) explican la mayor parte de los siniestros, cuáles se asocian a mayor gravedad y cambia su peso según la hora del día?

**Script:** `pregunta_06.py` · **Técnicas:** Pareto de causas, % por factor, gravedad por grupo de causa, burbujas (frecuencia vs gravedad) y heatmaps causa × franja · **Features:** `causa_grupo` y `factor_causal` (Haddon, 1968; Sabey y Taylor, 1980).

## 1. Qué hace el código

- Cuenta los siniestros por causa (26 códigos), aplica `pareto_abc()` y calcula el % por factor causal (humano, vehículo, vía y entorno).
- `gravedad()` por cada uno de los 10 grupos de causa: siniestros, fallecidos y % con fallecidos.
- Grafica el Top 10 de causas en barras y un gráfico de burbujas (X = frecuencia en escala log, Y = % fatales, tamaño = fallecidos, color = factor, línea = promedio nacional 9.6 %). Dos heatmaps causa × franja: peso de cada causa y % fatales (celdas con 30 o más siniestros).

## 2. Para la exposición (máx. 40 s)

> En las barras vemos que distracción y velocidad son las dos causas más frecuentes, y que casi todo es factor humano: 94.5 %. En las burbujas, cada una es un grupo de causa; más a la derecha es más frecuente y más arriba es más letal. Distracción y velocidad están arriba de la línea del promedio, mientras el irrespeto de señales es frecuente pero poco letal. Y según el heatmap, de madrugada crecen velocidad, alcohol y fatiga. Las causas registradas son casi todas del comportamiento del conductor.

*Figura a mostrar:* `p06_pareto_y_burbujas.png` (apoyo: `p06_heatmaps_causa_franja.png`). 87 palabras, unos 35 s a ritmo normal.

## 3. Resultados

- Factor causal: **humano 94.5 %**, vía y entorno 4.3 %, vehículo 1.2 %.
- Causas más frecuentes: distracción **28.8 %**, velocidad **19.3 %**, no respetar señales 13.5 %, distancia prudencial 6.4 %, alcohol 5.6 %.

| Grupo (promedio nacional 9.6 %) | Siniestros | % con fallecidos |
|---|---|---|
| Vía y entorno | 744 | 12.8 |
| Distracción al conducir | 4 956 | 12.2 |
| Exceso de velocidad | 3 331 | 12.0 |
| Alcohol / sustancias | 1 044 | 5.8 |
| Irrespeto de señales / prioridad | 3 382 | 4.8 |

- De madrugada: velocidad 26.0 % (16.8 % en la tarde), alcohol 10.0 % (3.2 % en la mañana) y fatiga 2.7 %; el irrespeto de señales cae de 23.0 % a 12.2 %. La distracción se mantiene en 28 a 30 % a toda hora.

## 4. Análisis

1. **Casi todo es factor humano:** las causas registradas son casi todas del comportamiento del conductor, no del vehículo ni de la vía.
2. **Distracción y velocidad explican casi la mitad (48.1 %)** y están entre las más graves; frecuente no es lo mismo que grave (el irrespeto de señales es la tercera causa y de las menos letales).
3. **La madrugada cambia el peso de las causas** justo cuando sube la letalidad (pregunta 5).

## 5. Limitaciones

- **El alcohol sale poco letal (5.8 %), lo que contradice la intuición.** Probable sesgo de registro (la causa se anota en controles, más frecuentes en siniestros leves); es una hipótesis que el dataset no confirma.
- La causa es la *probable* que anota el ente de control, no una causa verificada.

## 6. Archivos

`p06_gravedad_por_grupo_causa.csv` · `p06_pareto_y_burbujas.png`, `p06_heatmaps_causa_franja.png`
