# Pregunta de negocio 5: zona, jerarquía vial y corredores

> **Pregunta:** ¿Cómo influyen la zona (urbana o rural), la jerarquía de la vía y los corredores viales en la cantidad y gravedad de los siniestros, y cómo cambia eso a lo largo del día?

**Script:** `pregunta_05.py` · **Técnicas:** comparación urbano / rural, ranking de corredores, gráfico facetado por zona y franja horaria, burbujas y heatmap corredor × franja.

## 1. Qué hace el código

- `gravedad()` por zona y por red vial: compara el % de fatales dentro y fuera de la red estatal (un tercio de los siniestros; el resto tiene "no aplica" en los campos viales) y por jerarquía y corredor (mínimo 60 siniestros).
- Dos paneles con el % de fatales por franja horaria, urbana y rural, con el mismo eje Y, y un tercero con los 12 corredores principales en burbujas (X = siniestros, Y = % fatales, tamaño = fallecidos, línea punteada = promedio de la red estatal).
- Un heatmap corredor × franja con los 10 corredores de más siniestros.

## 2. Para la exposición (máx. 40 s)

> Los dos primeros paneles comparten eje: muestran el porcentaje de siniestros con fallecidos por franja horaria. La zona rural, en naranja, es el doble de grave que la urbana, y en ambas la madrugada es la peor franja; en la rural llega a uno de cada cinco. A la derecha, cada burbuja es un corredor: E40 tiene más siniestros pero está bajo el promedio, mientras E25, E20 y E482 tienen menos eventos y más muertes por siniestro. Volumen y gravedad no coinciden en los corredores.

*Figura a mostrar:* `p05_zona_franja_corredores.png` (apoyo: `p05_heatmap_corredor_franja.png`). 85 palabras, unos 34 s a ritmo normal.

## 3. Resultados

| | Urbana | Rural |
|---|---|---|
| Siniestros | 10 939 | 6 297 |
| % con fallecidos | 7.09 | **13.97** |
| Madrugada (00-05) | 10.7 | **20.2** |
| Mañana / Tarde / Noche | 5.8 / 5.1 / 7.7 | 12.2 / 11.9 / 14.0 |

- Red estatal: **13.7 %** de fatales frente a 7.5 % fuera de ella. Arterial 13.9 % y colectora 13.5 %: casi iguales.
- Corredores (siniestros, % fatales): E40 896, 10.5 · E35 722, 12.3 · **E25** 645, **17.1** (125 fallecidos, el que más) · **E20** 210, **22.4** · E482 107, 19.6.

## 4. Análisis

1. **La zona rural es el doble de grave** aunque tiene menos siniestros. La red estatal también, pero no es evidencia independiente: el 69 % de sus siniestros son rurales (dentro de la red, rural 14.7 % y urbana 11.6 %).
2. **La madrugada es la franja más letal** en ambas zonas, pese a tener el menor volumen (de madrugada pesan más velocidad, alcohol y fatiga, pregunta 6).
3. **Volumen y gravedad no coinciden en los corredores:** E40 tiene más siniestros pero menos letalidad que E25, E20 y E482.

## 5. Limitaciones

- Solo hay datos de vía para un tercio de los siniestros; los corredores no describen la red urbana ni municipal.
- Otros corredores también superan el promedio estatal (E45 17.2 % con 198 siniestros, E48 15.0 % con 253); se destacan E25, E20 y E482 por combinar letalidad y volumen. E482 y E20 tienen pocos casos y sus porcentajes son variables.

## 6. Archivos

`p05_zona.csv`, `p05_corredores.csv` · `p05_zona_franja_corredores.png`, `p05_heatmap_corredor_franja.png`
