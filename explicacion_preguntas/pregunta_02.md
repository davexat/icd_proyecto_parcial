# Pregunta de negocio 2: días críticos

> **Pregunta:** ¿Qué días tuvieron muchos más siniestros o fallecidos de lo habitual y qué tienen en común (día de la semana, feriado, mes, causa dominante)?

**Script:** `pregunta_02.py`
**Técnicas:** valores estandarizados (z-score) de la serie diaria, correlación entre siniestros y fallecidos, composición de causas, serie diaria y calendario heatmap.

## 1. Qué hace el código

**Bloque 0: serie diaria.** Siniestros y fallecidos por día (incluye los días con 0), con marcas de día de la semana, fin de semana y feriado.

**Bloque 1: z-score.** Cada día se compara contra el promedio y la desviación estándar *de su mismo día de la semana*: `z = (valor - media del día de la semana) / desviación del día de la semana`. Así un domingo no se marca como crítico solo por ser domingo (los domingos ya son más altos, ver pregunta 1). Imprime la correlación entre siniestros y fallecidos y cuántos días tienen z > 2.

**Bloque 2: días críticos.** Un día es crítico si z > 2 en siniestros *o* en fallecidos. Para cada uno muestra día, valores, z, si fue feriado y la causa dominante. Mide el % de críticos entre fines de semana y feriados frente al resto, los críticos por mes, y compara la composición de causas de los días críticos con la del resto. Guarda `p02_dias_criticos.csv`.

**Bloque 3: gráficos.** (a) Dos series (siniestros y fallecidos) con media móvil de 7 días y los días críticos en rojo. (b) Dos calendarios heatmap (semana ISO × día de la semana) coloreados por el z-score.

## 2. Para la exposición (máx. 40 s)

> Aquí vemos la serie diaria de siniestros y fallecidos con su media móvil de 7 días; los puntos rojos son los días críticos, es decir, los que superan dos desviaciones respecto a su mismo día de la semana. Son solo 13 de 273 días. El pico más alto es el 1 de enero, y 11 de los 13 caen entre junio y septiembre. Además, uno de cada seis feriados es crítico frente a uno de cada 26 días normales. Los días extremos son pocos y se repiten sobre todo en feriados.

*Figura a mostrar:* `p02_serie_diaria_criticos.png` (el calendario heatmap queda como apoyo). 91 palabras, unos 36 s a ritmo normal.

## 3. Resultados

- Correlación diaria entre siniestros y fallecidos: **0.64**.
- Días con z > 2: 6 en siniestros y 10 en fallecidos; en total **13 días críticos de 273 (4.8 %)**.

| Fecha | Día | Siniestros | Fallecidos | z sin. | z fall. | Feriado | Causa dominante |
|---|---|---|---|---|---|---|---|
| **2026-01-01** | Jueves | **123** | **21** | **4.23** | **3.72** | Sí | Distracción |
| 2026-06-15 | Lunes | 78 | 12 | 2.44 | 2.33 | No | Velocidad |
| 2026-06-21 | Domingo | 125 | 20 | 2.09 | 2.12 | No | Distracción |
| 2026-08-04 | Martes | 50 | 12 | 0.00 | 3.16 | No | Distracción |
| 2026-09-05 | Sábado | 104 | 19 | 1.74 | 2.73 | No | Distracción |

(La tabla completa, con los 13 días, está en `p02_dias_criticos.csv`.)

- % de críticos entre los feriados: **16.7 %** vs 3.9 % en el resto. Entre fines de semana: 2.6 % vs 5.6 % en los otros días.
- Críticos por mes: enero 1, mayo 1, junio 3, julio 2, agosto 4, septiembre 2.
- Causa dominante: distracción en 10 de los 13 días y exceso de velocidad en 3.
- Composición de causas (críticos frente al resto): distracción +4.0 puntos, alcohol +2.1, velocidad +1.1; irrespeto de señales -5.3.

## 4. Análisis

1. **Son pocos días y son extremos.** El 1 de enero de 2026 es el caso más fuerte (z de 4.2 en siniestros y 3.7 en fallecidos), consistente con las celebraciones de fin de año.
2. **El feriado es lo que más se repite**: 1 de cada 6 feriados es crítico, frente a 1 de cada 26 de los demás días. En cambio, el *fin de semana* no es más crítico, justamente porque el z-score ya descuenta su efecto: los fines de semana son altos, pero son "normalmente altos".
3. **Siniestros y fallecidos no siempre suben juntos** (correlación 0.64): el 4 de agosto tiene 50 siniestros (z = 0.0) pero 12 fallecidos (z = 3.2), mientras que el 17 de agosto tiene un exceso de siniestros (z = 2.1) con solo 3 fallecidos. Por eso se evalúan ambas series.
4. **Hay concentración en el segundo semestre:** 11 de los 13 críticos están entre junio y septiembre, lo que coincide con el aumento del volumen visto en la pregunta 1.
5. **Causa dominante:** en los días críticos pesan algo más la distracción y el alcohol, y menos el irrespeto de señales.

## 5. Limitaciones y advertencias

- Con solo 13 casos, los porcentajes por mes o por tipo de día son frágiles.
- El calendario heatmap tiene 39 filas (semanas) y es difícil de leer proyectado; para la diapositiva conviene usar la serie diaria con críticos marcados y dejar el calendario como apoyo.
- Parte del aumento en el segundo semestre puede reflejar mayor cobertura del registro (ver pregunta 1).

## 6. Archivos generados

- Tabla: `p02_dias_criticos.csv`
- Figuras: `p02_serie_diaria_criticos.png`, `p02_calendario_heatmap.png`
