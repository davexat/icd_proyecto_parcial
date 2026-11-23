# Pregunta de negocio 2: días críticos

> **Pregunta:** ¿Qué días tuvieron muchos más siniestros o fallecidos de lo habitual y qué tienen en común (día de la semana, feriado, mes, causa dominante)?

**Script:** `pregunta_02.py` · **Técnicas:** z-score de la serie diaria, correlación, y comparación de los días críticos con todos los días en gráficos facetados.

## 1. Qué hace el código

- Arma la serie diaria de siniestros y fallecidos (con los días en 0) y marca el día de la semana, el fin de semana y el feriado.
- Mide **cuántas desviaciones estándar se aparta cada día de lo habitual**, donde «habitual» es el promedio de su mismo día de la semana (así no se marca como crítico cada domingo solo por ser domingo). Cero es un día normal; un día es **crítico** si pasa de 2 en siniestros o en fallecidos. Guarda `p02_dias_criticos.csv`.
- Grafica cada día como un punto (rojo si es crítico, con su fecha) y luego compara, en cuatro paneles, cómo se reparten los días críticos y **todos** los días según día de la semana, mes, feriado y causa dominante.

## 2. Para la exposición (máx. 40 s)

> Cada punto es un día; cero es un día normal para su día de la semana y los rojos son los críticos, los que pasan de dos desviaciones: 13 de 273. El más extremo es el 1 de enero. Si los comparamos con todos los días, vemos qué tienen en común: 11 de los 13 caen entre junio y septiembre, casi uno de cada cuatro es feriado, frente a uno de cada quince en general, y la distracción es la causa dominante en 77 %, contra 58 %. El día de la semana no los distingue.

*Figuras a mostrar:* primero `p02_dias_criticos_z.png` (qué días) y, al decir «Si los comparamos…», `p02_que_tienen_en_comun.png` (qué tienen en común). 96 palabras, unos 38 s a ritmo normal.

## 3. Resultados

- **13 días críticos de 273 (4.8 %)**: 6 por siniestros, 10 por fallecidos y 3 por ambos (1 de enero, 15 y 21 de junio). Correlación diaria entre siniestros y fallecidos: **0.64**.
- Peor día: **1 de enero** (123 siniestros y 21 fallecidos; 4.2 y 3.7 desviaciones). Le siguen el 15 de junio, el 21 de junio y el 5 de septiembre.
- Comparación de los 13 días críticos con los 273 días:

| Característica | Días críticos | Todos los días |
|---|---|---|
| Entre junio y septiembre | **85 %** (11 de 13) | 45 % |
| Feriado | **23 %** (3 de 13) | 6.6 % (18 de 273) |
| Causa dominante: distracción | **77 %** | 57.5 % |
| Causa dominante: velocidad | 23 % | 19.4 % |
| Causa dominante: irrespeto de señales | **0 %** | 18.7 % |
| Lunes o viernes | 46 % (6 de 13) | 29 % |

## 4. Análisis

1. **Qué días:** son pocos (4.8 %) y extremos; el 1 de enero es el más marcado en ambos criterios.
2. **Qué tienen en común:** caen sobre todo entre junio y septiembre, hay más feriados de los esperados y la causa dominante es más a menudo la distracción, mientras que el irrespeto de señales casi no aparece. El **día de la semana no los distingue** (se reparten entre los siete días).
3. **Siniestros y fallecidos no siempre suben juntos:** el 4 de agosto tuvo 50 siniestros (en el promedio) pero 12 fallecidos (3.2 desviaciones).

## 5. Limitaciones

- Con 13 casos, los porcentajes son frágiles; el feriado son solo 3 días.
- **El nivel diario sube durante el año** (de 52 siniestros por día en enero a 72 en agosto) y «habitual» se calcula con el promedio de todo el período, así que los meses de más actividad quedan por encima casi por construcción.
- La distracción es la causa dominante en 57.5 % de **todos** los días, por eso se compara contra ese total y no contra cero.

## 6. Archivos

`p02_dias_criticos.csv` · `p02_dias_criticos_z.png`, `p02_que_tienen_en_comun.png`
