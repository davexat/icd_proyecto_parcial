# Pregunta de negocio 1: ¿cuándo ocurren los siniestros?

> **Pregunta:** ¿En qué meses, días de la semana y horas ocurren más siniestros, y ese patrón cambia entre zona urbana y rural?

**Script:** `pregunta_01.py` · **Técnicas:** índices de estacionalidad (valor / promedio) y gráficos de barras y líneas · **Feature:** índice de estacionalidad (Hyndman y Athanasopoulos, 2021).

## 1. Qué hace el código

- Cuenta los días del periodo (273) para que un mes largo no gane solo por tener más días.
- `indices()` calcula los siniestros por día calendario en cada mes y día de la semana, y por hora, y los divide entre su promedio: **1 = promedio, mayor a 1 = temporada alta**. Se aplica a todos los siniestros, a los urbanos y a los rurales (cada zona contra su propio promedio) y guarda `p01_indices.csv`.
- Dibuja una imagen general (mes, día, hora) y una por categoría con urbana (azul) vs rural (naranja).

## 2. Para la exposición (máx. 40 s)

> El índice compara cada mes, día y hora con su promedio: sobre 1 es temporada alta. En el panorama general, los siniestros crecen hasta agosto, se concentran en fin de semana y tienen su pico a las 19 horas. Al separar por zona, el patrón es el mismo, pero la rural es más extrema: el domingo llega a 1,5 contra 1,3 en la urbana, y a las 19 horas, a 1,9 contra 1,4. La urbana es más pareja y tiene más actividad de madrugada.

*Figuras a mostrar:* `p01_indices_general.png`, y como apoyo `p01_indices_hora_zona.png` y `p01_indices_dia_zona.png` (`p01_indices_mes_zona.png` si hay tiempo). 84 palabras, unos 34 s a ritmo normal.

## 3. Resultados

| Índice | General | Urbana | Rural |
|---|---|---|---|
| Domingo | **1.38** | 1.31 | **1.50** |
| 19 h | **1.59** | 1.43 | **1.86** |
| 7 h | 1.20 | 1.15 | 1.30 |
| 0 a 2 h | 0.68 a 0.79 | 0.72 a 0.87 | 0.54 a 0.65 |
| Enero → agosto | 0.82 → 1.15 | 0.83 → 1.13 | 0.78 → 1.17 |

Horas con índice mayor a 1.3 (general): 17, 18, 19 y 20 h. El día más bajo es martes (urbana 0.81) o miércoles (rural 0.75).

## 4. Análisis

1. **El patrón es el mismo en ambas zonas:** fin de semana, tarde-noche (17 a 20 h, máximo a las 19 h) y alza de enero a agosto.
2. **La zona rural es más extrema** (domingo, 19 h y pico matutino de 6 y 7 h); **la urbana es más pareja** y tiene más actividad de madrugada.

## 5. Limitaciones

- Cada zona se compara con su propio promedio: el índice dice *cuándo*, no *cuánto*. La urbana tiene más siniestros (10 939 frente a 6 297).
- Nueve meses no permiten hablar de estacionalidad anual; el alza mensual mezcla estacionalidad y tendencia (posible mayor cobertura del registro, no comprobada).

## 6. Archivos

`p01_indices.csv` · `p01_indices_general.png`, `p01_indices_mes_zona.png`, `p01_indices_dia_zona.png`, `p01_indices_hora_zona.png`
