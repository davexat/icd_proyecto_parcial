# Pregunta de negocio 9: zona, jerarquía vial y corredores

> **Pregunta:** ¿Cómo influyen la zona (urbana o rural), la jerarquía de la vía y los corredores viales en la cantidad y gravedad de los siniestros, y cómo cambia eso a lo largo del día?

**Técnicas:** comparación urbano / rural, ranking de corredores viales, gráfico facetado por zona y franja horaria, gráfico de burbujas y heatmap corredor × franja.
**Verificación:** el script corre sin errores y genera 2 tablas y 2 figuras.

## 1. Qué hace el código

**Bloque 1: urbano vs rural.** `gravedad()` por zona, más la hora mediana de ocurrencia. Guarda `p09_zona.csv`.

**Bloque 2: red vial estatal.** Filtra los siniestros con datos de vía (`via_estatal`, un tercio del total; el resto tenía "ND" en los campos viales y se trató como "no aplica"). Compara el % de fatales dentro y fuera de la red, calcula la gravedad por jerarquía (arterial, colectora) y por corredor (códigos E35, E25...) con al menos 60 siniestros. Guarda `p09_corredores.csv`.

**Bloque 3: facetas y burbujas.** Dos paneles de barras con el % de siniestros con fallecidos por franja horaria, uno para zona urbana y otro para rural, con el mismo eje Y (0 a 24 %) para poder compararlos. El tercer panel muestra los 12 corredores principales como burbujas: X = siniestros, Y = % con fallecidos, tamaño = fallecidos.

**Bloque 4: heatmap corredor × franja.** Conteo de siniestros por franja horaria para los 10 corredores con más siniestros.

## 2. Resultados

| Zona | Siniestros | % con fallecidos | Hora mediana |
|---|---|---|---|
| Rural | 6 297 | **13.97** | 14.3 |
| Urbana | 10 939 | 7.09 | 14.0 |

- Red vial estatal: 5 778 siniestros (33.5 %), con **13.7 %** de fatales frente a **7.5 %** fuera de ella.
- Jerarquía: arterial 13.9 % (3 021 siniestros) y colectora 13.5 % (2 745); casi iguales.

**% con fallecidos por zona y franja:**

| Franja | Urbana | Rural |
|---|---|---|
| Madrugada (00-05) | 10.7 | **20.2** |
| Mañana (06-11) | 5.8 | 12.2 |
| Tarde (12-17) | 5.1 | 11.9 |
| Noche (18-23) | 7.7 | 14.0 |

**Corredores principales:**

| Corredor | Siniestros | % con fallecidos | Fallecidos |
|---|---|---|---|
| E40 | 896 | 10.5 | 113 |
| E35 | 722 | 12.3 | 109 |
| E25 | 645 | **17.1** | 125 |
| E20 | 210 | **22.4** | 54 |
| E482 | 107 | 19.6 | 22 |

En el heatmap, en E25, E35 y E40 la franja con más siniestros es la noche (233, 239 y 290) y la madrugada es la de menos volumen (106, 148 y 155).

## 3. Análisis

1. **La zona rural es el doble de grave** (14.0 % vs 7.1 %) aunque tiene menos siniestros que la urbana. Lo mismo ocurre con la red vial estatal frente al resto.
2. **La madrugada es la franja más letal en ambas zonas** y en la rural llega a 1 de cada 5 siniestros (20.2 %), pese a tener el menor volumen de eventos. El patrón es en forma de "U": baja en la mañana y la tarde y sube en la noche y la madrugada. En P5 se vio que de madrugada pesan más la velocidad, el alcohol y la fatiga, lo que es coherente con este resultado.
3. **La jerarquía vial no discrimina** (arterial 13.9 % vs colectora 13.5 %): lo que cambia el riesgo es el corredor, no la categoría.
4. **Volumen y gravedad no coinciden en los corredores.** E40 es el de más siniestros pero con letalidad moderada (10.5 %); E25, E20 y E482 tienen menos eventos pero una proporción mucho mayor de fallecidos, así que son los candidatos a intervención prioritaria.

## 4. Limitaciones y advertencias

- Solo hay datos de vía para un tercio de los siniestros (red estatal), así que los corredores no describen la red municipal ni urbana.
- Algunos corredores tienen pocos casos (E482: 107, E20: 210); sus porcentajes son más variables.
- La línea punteada del panel de burbujas es el promedio de la red estatal (13.7 %) pero no está rotulada; conviene añadir una leyenda antes de proyectarla.

## 5. Archivos generados

- Tablas: `p09_zona.csv`, `p09_corredores.csv`
- Figuras: `p09_zona_franja_corredores.png`, `p09_heatmap_corredor_franja.png`

**Cumple de las instrucciones:** gráfico facetado (6.2), heatmap (6.3), datos espaciales (2.4).
