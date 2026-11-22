# Pregunta de negocio 11 (adicional): estabilidad y crecimiento por provincia

> **Pregunta:** ¿Qué provincias tienen una siniestralidad estable y cuáles volátil, y cuáles crecieron o decrecieron a lo largo de 2026?

**Técnicas:** coeficiente de variación diario (CV > 1 = volátil), representatividad en el total, variación porcentual entre el primer y el último trimestre disponibles, heatmap provincia × mes y facetas de las provincias principales.
**Verificación:** el script corre sin errores y genera 2 tablas y 2 figuras.

## 1. Qué hace el código

**Bloque 0: serie por provincia.** Matriz día × provincia de siniestros (273 filas, 24 columnas), con ceros en los días sin siniestros.

**Bloque 1: volatilidad.** Para cada provincia calcula el promedio diario, la desviación y el **CV = desviación / promedio**. Se clasifica como "Volátil" si CV > 1 y "Estable" si no, y se agrega su representatividad (% del total). Guarda `p11_volatilidad_provincias.csv`.

**Bloque 2: variación en el año.** Calcula siniestros por día calendario en cada mes y compara el promedio de los 3 primeros meses con el de los 3 últimos (ene-mar vs jul-sep), solo para provincias con 150 o más siniestros. Guarda `p11_variacion_provincias.csv`.

**Bloque 3: gráficos.** (a) Dispersión CV vs representatividad (escala log) y heatmap provincia × mes con el desvío porcentual respecto al promedio de cada provincia. (b) Cuadrícula 2 × 3 con la serie mensual de las 6 provincias principales.

## 2. Resultados

- **13 de 24 provincias son "volátiles"**, pero juntas representan solo el **11.7 %** de los siniestros.
- Estables y grandes: Guayas (CV 0.36), Pichincha (0.34), Santo Domingo (0.59), Manabí (0.60), Tungurahua (0.61).
- Más volátiles: Galápagos (7.33, con solo 5 siniestros), Pastaza (2.55), Orellana (2.06).

**Mayor variación entre los 3 primeros y los 3 últimos meses:**

| Provincia | Promedio inicial (por día) | Promedio final | Variación |
|---|---|---|---|
| Morona Santiago | 0.43 | 1.99 | +362 % |
| Cañar | 0.19 | 0.85 | +338 % |
| Esmeraldas | 0.38 | 0.99 | +163 % |
| Santa Elena | 1.09 | 2.47 | +127 % |
| Guayas | 17.41 | 22.21 | +28 % |
| Pichincha | 12.54 | 13.09 | +4 % |
| Imbabura | 1.14 | 0.91 | -20 % |

## 3. Análisis

1. **Las grandes son estables.** Guayas y Pichincha, que juntas son el 53 % de los siniestros, tienen un CV de apenas 0.3, así que su volumen diario es predecible.
2. **El CV de las provincias pequeñas es mayormente un efecto del tamaño.** Con conteos bajos el CV es alto aunque el proceso no sea inestable: si los siniestros llegaran al azar (distribución de Poisson), el CV esperado es 1/√media. Por ejemplo, Chimborazo tiene un CV de 1.05 frente a 0.91 esperado, y Galápagos 7.33 frente a ~7.4 esperado. En cambio, Guayas tiene 0.36 frente a 0.22 esperado, lo que sí indica una variación real (por día de la semana y feriados). Interpretar "volátil" como "pequeña" es más honesto que como "inestable".
3. **Casi todas crecen.** 15 de 17 provincias aumentan entre el primer y el último trimestre, en línea con el índice mensual nacional de P1.

## 4. Limitaciones y advertencias

- **El crecimiento puede ser cobertura de registro y no siniestralidad real.** En Santa Elena los siniestros pasan de 15 (enero) y 12 (febrero) a 73 en marzo y se mantienen en 71 a 88; todos son del ente CTE, lo que apunta a un cambio de cobertura. En Morona Santiago (19, 10, 10, 6 en enero-abril y 59, 61, 63 en julio-septiembre) y Cañar el salto ocurre en meses concretos y casi todo el registro es de PNE. No se puede separar aumento real de más cobertura con estos datos.
- Esta pregunta se solapa con P3 (ranking provincial) y con la dimensión temporal de P1, por lo que se recomienda dejarla en el apéndice.
- Galápagos (5 siniestros) no debe interpretarse.

## 5. Archivos generados

- Tablas: `p11_volatilidad_provincias.csv`, `p11_variacion_provincias.csv`
- Figuras: `p11_volatilidad_y_variacion.png`, `p11_facetas_provincias_principales.png`

**Cumple de las instrucciones:** gráfico facetado (6.2), heatmap (6.3), medida estadística (CV).
