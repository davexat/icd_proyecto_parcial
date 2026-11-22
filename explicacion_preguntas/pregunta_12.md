# Pregunta de negocio 12 (adicional): correlaciones a nivel cantonal

> **Pregunta:** ¿Existe correlación entre los tipos de siniestro, las causas y los vehículos involucrados a nivel cantonal? ¿Cuáles "se mueven juntos" una vez descontado el tamaño del cantón?

**Técnicas:** matriz cantón × categoría, correlación de Spearman (por rangos) sobre conteos y sobre porcentajes del cantón, heatmaps comparados y diagramas de dispersión.
**Verificación:** el script corre sin errores y genera 1 tabla y 2 figuras.

## 1. Qué hace el código

**Bloque 0: selección.** Se queda con los cantones con al menos 60 siniestros: 44 cantones que reúnen el 83.7 % de los siniestros.

**Bloque 1: matriz cantón × categoría.** Para cada cantón cuenta siniestros por los 7 tipos más frecuentes, los 5 grupos de causa más frecuentes, 6 tipos de vehículo involucrado y los siniestros con fallecidos (19 variables). Luego arma una segunda matriz `P` dividiendo cada fila entre el total del cantón, es decir, la **composición porcentual** del cantón.

**Bloque 2: correlación.** Calcula Spearman sobre conteos (`c_cnt`) y sobre porcentajes (`c_pct`) y compara la correlación media entre pares. Del segundo grupo extrae los pares más correlacionados, omitiendo los pares de la misma familia (por ejemplo, dos tipos de siniestro) porque son casi complementarios. Guarda `p12_pares_correlacion.csv`.

**Bloque 3: gráficos.** Dos heatmaps (conteos y porcentajes) y cuatro dispersiones de los pares más correlacionados, con su recta de ajuste.

## 2. Resultados

- Correlación media entre pares: **0.53 con conteos** y **-0.01 con porcentajes**.

| Par (en % del cantón) | Correlación |
|---|---|
| Causa alcohol / sustancias ↔ vehículo automóvil | **0.70** |
| Causa maniobras y distancia ↔ vehículo motocicleta | 0.63 |
| Causa exceso de velocidad ↔ vehículo automóvil | 0.61 |
| Tipo estrellamientos ↔ vehículo automóvil | 0.60 |
| Vehículo camión ↔ con fallecidos | 0.58 |
| Causa alcohol ↔ vehículo motocicleta | -0.56 |
| Tipo choque frontal ↔ causa distracción | 0.55 |

## 3. Análisis

1. **Con conteos, casi todo se correlaciona con todo (0.53)** porque los cantones grandes tienen más de cada cosa. Es un efecto de tamaño, no información.
2. **Al pasar a porcentajes la correlación media se vuelve 0**, y quedan solo las relaciones de composición. Por eso se usan porcentajes para esta pregunta.
3. **Perfiles cantonales:** los cantones donde el alcohol pesa más también tienen más automóviles involucrados (0.70) y menos motocicletas (-0.56); donde hay más motos, pesan más las maniobras y la distancia (0.63). Son los cantones con un perfil de tránsito "de automóvil" y "de moto". Los camiones se relacionan con mayor proporción de siniestros fatales (0.58).

## 4. Limitaciones y advertencias

- Con 44 cantones y unos 125 pares entre familias distintas, es esperable que algunas correlaciones altas aparezcan por azar; con n = 44, un valor de ~0.30 es el umbral aproximado de significancia al 5 %, pero tantas pruebas simultáneas obligan a ser cautelosos. Son pistas, no hallazgos.
- Es un análisis *ecológico*: que dos categorías se muevan juntas entre cantones no significa que ocurran juntas dentro del mismo siniestro.
- Los porcentajes de una misma familia suman 100 %, por lo que parte de las correlaciones negativas es mecánica.
- Es la pregunta más difícil de explicar en poco tiempo; se recomienda el apéndice.

## 5. Archivos generados

- Tabla: `p12_pares_correlacion.csv`
- Figuras: `p12_heatmaps_correlacion.png`, `p12_dispersion_pares_top.png`

**Cumple de las instrucciones:** medidas estadísticas (punto 5), heatmaps (6.3), datos espaciales agregados por cantón.
