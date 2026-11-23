# Pregunta de negocio 2: días críticos

> **Pregunta:** ¿Qué días tuvieron muchos más siniestros o fallecidos de lo habitual y qué tienen en común (día de la semana, feriado, mes, causa dominante)?

**Script:** `pregunta_02.py` · **Técnicas:** z-score de la serie diaria, correlación, composición de causas, serie diaria y calendario heatmap.

## 1. Qué hace el código

- Arma la serie diaria de siniestros y fallecidos (con los días en 0) y marca día de la semana, fin de semana y feriado.
- Calcula el z-score de cada día **contra su mismo día de la semana**, para no marcar los domingos como críticos solo por ser domingo. Un día es crítico si z > 2 en siniestros o en fallecidos; guarda `p02_dias_criticos.csv`.
- Mide el % de críticos en feriados y fines de semana, por mes y la composición de causas frente al resto. Grafica la serie con media móvil de 7 días y un calendario heatmap.

## 2. Para la exposición (máx. 40 s)

> Aquí vemos la serie diaria de siniestros y fallecidos con su media móvil de 7 días; los puntos rojos son los días críticos, es decir, los que superan dos desviaciones respecto a su mismo día de la semana. Son solo 13 de 273 días. El pico más alto es el 1 de enero, y 11 de los 13 caen entre junio y septiembre. Además, uno de cada seis feriados es crítico frente a uno de cada 26 días normales. Los días extremos son pocos y se repiten sobre todo en feriados.

*Figura a mostrar:* `p02_serie_diaria_criticos.png` (el calendario heatmap queda como apoyo). 91 palabras, unos 36 s a ritmo normal.

## 3. Resultados

- **13 días críticos de 273 (4.8 %)**; correlación diaria siniestros-fallecidos: **0.64**.
- Peor día: **1 de enero** (123 siniestros, 21 fallecidos, z = 4.23 y 3.72). Le siguen el 15 de junio (z 2.44), el 21 de junio y el 5 de septiembre.
- Feriados críticos: **16.7 %** frente a 3.9 % en los demás días. Fines de semana: 2.6 % frente a 5.6 %.
- Por mes: junio 3, julio 2, agosto 4, septiembre 2 (11 de 13), más enero 1 y mayo 1.
- Causa dominante: distracción en 10 de los 13 días y velocidad en 3.

## 4. Análisis

1. **Son pocos días y extremos;** el feriado es lo que más se repite. El fin de semana no es crítico porque el z-score ya descuenta su efecto.
2. **Siniestros y fallecidos no siempre suben juntos:** el 4 de agosto tiene 50 siniestros (z = 0.0) pero 12 fallecidos (z = 3.2).

## 5. Limitaciones

- Con 13 casos, los porcentajes por mes o tipo de día son frágiles.
- El calendario heatmap (39 semanas) es denso para proyectar; usar la serie diaria.

## 6. Archivos

`p02_dias_criticos.csv` · `p02_serie_diaria_criticos.png`, `p02_calendario_heatmap.png`
