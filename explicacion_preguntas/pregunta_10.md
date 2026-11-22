# Pregunta de negocio 10: días críticos

> **Pregunta:** ¿Qué días tuvieron muchos más siniestros o fallecidos de lo habitual y qué tienen en común (día de la semana, feriado, mes, causa dominante)?

**Técnicas:** valores estandarizados (z-score) de la serie diaria, correlación entre siniestros y fallecidos, composición de causas, serie diaria y calendario heatmap.
**Verificación:** el script corre sin errores y genera 1 tabla y 2 figuras.

## 1. Qué hace el código

**Bloque 0: serie diaria.** Siniestros y fallecidos por día (incluye los días con 0), con marcas de día de la semana, fin de semana y feriado.

**Bloque 1: z-score.** Cada día se compara contra el promedio y la desviación estándar *de su mismo día de la semana*: `z = (valor - media del día de la semana) / desviación del día de la semana`. Así un domingo no se marca como crítico solo por ser domingo (los domingos ya son más altos, ver P1). Imprime la correlación entre siniestros y fallecidos y cuántos días tienen z > 2.

**Bloque 2: días críticos.** Un día es crítico si z > 2 en siniestros *o* en fallecidos. Para cada uno muestra día, valores, z, si fue feriado y la causa dominante. Mide el % de críticos entre fines de semana y feriados frente al resto, los críticos por mes, y compara la composición de causas de los días críticos con la del resto. Guarda `p10_dias_criticos.csv`.

**Bloque 3: gráficos.** (a) Dos series (siniestros y fallecidos) con media móvil de 7 días y los días críticos en rojo. (b) Dos calendarios heatmap (semana ISO × día de la semana) coloreados por el z-score.

## 2. Resultados

- Correlación diaria entre siniestros y fallecidos: **0.64**.
- Días con z > 2: 6 en siniestros y 10 en fallecidos; en total **13 días críticos de 273 (4.8 %)**.

| Fecha | Día | Siniestros | Fallecidos | z sin. | z fall. | Feriado | Causa dominante |
|---|---|---|---|---|---|---|---|
| **2026-01-01** | Jueves | **123** | **21** | **4.23** | **3.72** | Sí | Distracción |
| 2026-06-15 | Lunes | 78 | 12 | 2.44 | 2.33 | No | Velocidad |
| 2026-06-21 | Domingo | 125 | 20 | 2.09 | 2.12 | No | Distracción |
| 2026-08-04 | Martes | 50 | 12 | 0.00 | 3.16 | No | Distracción |
| 2026-09-05 | Sábado | 104 | 19 | 1.74 | 2.73 | No | Distracción |

(La tabla completa tiene los 13 días en `p10_dias_criticos.csv`.)

- % de críticos entre los feriados: **16.7 %** vs 3.9 % en el resto. Entre fines de semana: 2.6 % vs 5.6 % en los otros días.
- Críticos por mes: enero 1, mayo 1, junio 3, julio 2, agosto 4, septiembre 2.
- Causa dominante: distracción en 10 de los 13 días y exceso de velocidad en 3.
- Composición de causas (críticos frente al resto): distracción +4.0 puntos, alcohol +2.1, velocidad +1.1; irrespeto de señales -5.3.

## 3. Análisis

1. **Son pocos días y son extremos.** El 1 de enero de 2026 es el caso más fuerte (z de 4.2 en siniestros y 3.7 en fallecidos), consistente con las celebraciones de fin de año.
2. **El feriado es lo que más se repite**: 1 de cada 6 feriados es crítico, frente a 1 de cada 26 de los demás días. En cambio, el *fin de semana* no es más crítico, justamente porque el z-score ya descuenta su efecto: los fines de semana son altos, pero son "normalmente altos".
3. **Siniestros y fallecidos no siempre suben juntos** (correlación 0.64): el 4 de agosto tiene 50 siniestros (z = 0.0) pero 12 fallecidos (z = 3.2), mientras que el 17 de agosto tiene un exceso de siniestros (z = 2.1) con solo 3 fallecidos. Por eso se evalúan ambas series.
4. **Hay concentración en el segundo semestre:** 11 de los 13 críticos están entre junio y septiembre, lo que coincide con el aumento del volumen visto en P1.
5. **Causa dominante:** en los días críticos pesan algo más la distracción y el alcohol, y menos el irrespeto de señales.

## 4. Limitaciones y advertencias

- Con solo 13 casos, los porcentajes por mes o por tipo de día son frágiles.
- El calendario heatmap tiene 39 filas (semanas) y es difícil de leer proyectado; para la diapositiva conviene usar la serie diaria con críticos marcados y dejar el calendario como apoyo.
- Parte del aumento en el segundo semestre puede reflejar mayor cobertura del registro (ver P1).

## 5. Archivos generados

- Tabla: `p10_dias_criticos.csv`
- Figuras: `p10_serie_diaria_criticos.png`, `p10_calendario_heatmap.png`

**Cumple de las instrucciones:** analítica con medidas estadísticas (punto 5), heatmap (6.3), datos temporales (2.1).
