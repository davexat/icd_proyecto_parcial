# Pregunta de negocio 5: zona, jerarquía vial y corredores

> **Pregunta:** ¿Cómo influyen la zona (urbana o rural), la jerarquía de la vía y los corredores viales en la cantidad y gravedad de los siniestros, y cómo cambia eso a lo largo del día?

**Script:** `pregunta_05.py`
**Técnicas:** comparación urbano / rural, ranking de corredores viales, gráfico facetado por zona y franja horaria, gráfico de burbujas y heatmap corredor × franja.

## 1. Qué hace el código

**Bloque 1: urbano vs rural.** `gravedad()` por zona, más la hora mediana de ocurrencia. Guarda `p05_zona.csv`.

**Bloque 2: red vial estatal.** Filtra los siniestros con datos de vía (`via_estatal`, un tercio del total; el resto tenía "ND" en los campos viales y se trató como "no aplica"). Compara el % de fatales dentro y fuera de la red, calcula la gravedad por jerarquía (arterial, colectora) y por corredor (códigos E35, E25...) con al menos 60 siniestros. Guarda `p05_corredores.csv`.

**Bloque 3: facetas y burbujas.** Dos paneles de barras con el % de siniestros con fallecidos por franja horaria, uno para zona urbana y otro para rural, con el mismo eje Y (0 a 24 %) para poder compararlos. El tercer panel muestra los 12 corredores principales como burbujas: X = siniestros, Y = % con fallecidos, tamaño = fallecidos, con una línea punteada en el promedio de la red estatal.

**Bloque 4: heatmap corredor × franja.** Conteo de siniestros por franja horaria para los 10 corredores con más siniestros.

## 2. Para la exposición (máx. 40 s)

> Los dos primeros paneles comparten eje: muestran el porcentaje de siniestros con fallecidos por franja horaria. La zona rural, en naranja, es el doble de grave que la urbana, y en ambas la madrugada es la peor franja; en la rural llega a uno de cada cinco. A la derecha, cada burbuja es un corredor: E40 tiene más siniestros pero está bajo el promedio, mientras E25, E20 y E482 tienen menos eventos y más muertes por siniestro. Esos son los candidatos a intervención prioritaria.

*Figura a mostrar:* `p05_zona_franja_corredores.png` (apoyo: `p05_heatmap_corredor_franja.png`). 84 palabras, unos 34 s a ritmo normal.

## 3. Resultados

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

## 4. Análisis

1. **La zona rural es el doble de grave** (14.0 % vs 7.1 %) aunque tiene menos siniestros que la urbana. La red vial estatal también es más grave que el resto (13.7 % frente a 7.5 %), pero no es una evidencia independiente: el 69 % de sus siniestros son rurales (dentro de la red, rural 14.7 % y urbana 11.6 %; fuera de ella, 12.8 % y 6.2 %).
2. **La madrugada es la franja más letal en ambas zonas** y en la rural llega a 1 de cada 5 siniestros (20.2 %), pese a tener el menor volumen de eventos. El patrón es en forma de "U": baja en la mañana y la tarde y sube en la noche y la madrugada. En la pregunta 6 se ve que de madrugada pesan más la velocidad, el alcohol y la fatiga, lo que es coherente con este resultado.
3. **La jerarquía vial no discrimina** (arterial 13.9 % vs colectora 13.5 %): lo que cambia el riesgo es el corredor, no la categoría.
4. **Volumen y gravedad no coinciden en los corredores.** E40 es el de más siniestros pero con letalidad moderada (10.5 %); E25, E20 y E482 tienen menos eventos pero una proporción mucho mayor de fallecidos, así que son los candidatos a intervención prioritaria.

## 5. Limitaciones y advertencias

- Solo hay datos de vía para un tercio de los siniestros (red estatal), así que los corredores no describen la red municipal ni urbana.
- Otros corredores también superan el promedio de la red estatal (13.7 %), como E45 (17.2 %, 198 siniestros) y E48 (15.0 %, 253); aparecen en el gráfico de burbujas. Se destacan E25, E20 y E482 por combinar más letalidad con volumen relevante (E25 es el corredor con más fallecidos: 125).
- Algunos corredores tienen pocos casos (E482: 107, E20: 210); sus porcentajes son más variables.

## 6. Archivos generados

- Tablas: `p05_zona.csv`, `p05_corredores.csv`
- Figuras: `p05_zona_franja_corredores.png`, `p05_heatmap_corredor_franja.png`
