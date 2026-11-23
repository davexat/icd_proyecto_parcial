# Pregunta de negocio 7: tipo de siniestro y vehículos

> **Pregunta:** ¿Qué tipos de siniestro y qué vehículos involucrados concentran la mayor gravedad, y esa gravedad cambia entre zona urbana y rural?

**Script:** `pregunta_07.py` · **Técnicas:** gravedad por tipo de siniestro, % de fatales con y sin cada vehículo, barras agrupadas urbano vs rural y heatmap tipo × vehículo.

## 1. Qué hace el código

- `gravedad()` por `tipo_siniestro` (13 tipos), ordenado por % con fallecidos.
- Para cada tipo de vehículo (30 o más siniestros) compara el % de fatales *cuando participa* contra *cuando no*, y calcula las "veces más fatales". También mira el % según el número de vehículos.
- Grafica en una sola figura dos paneles: a la izquierda, barras agrupadas urbana / rural por tipo (100 o más casos, con el número de siniestros entre paréntesis y la línea del promedio nacional); a la derecha, barras con y sin cada vehículo con las veces más fatales. Aparte, un heatmap tipo de siniestro × vehículo 1 (celdas con 30 o más casos) para el apéndice.

## 2. Para la exposición (máx. 40 s)

> A la izquierda, el porcentaje de siniestros con fallecidos por tipo, en ciudad y campo, con el mismo eje. Los arrollamientos son los más graves, con 37 % en la ciudad y 59 % en el campo; el choque lateral es el más frecuente, pero de los menos graves. En casi todos los tipos la barra rural es más larga. A la derecha, cada vehículo con y sin él: con un bus el siniestro es 1.85 veces más fatal, y con una moto, 1.72.

*Figura a mostrar:* `p07_gravedad_tipo_y_vehiculo.png` (apoyo: `p07_heatmap_tipo_vehiculo.png`). 84 palabras, unos 37 s a ritmo normal.

## 3. Resultados

| Tipo | Siniestros | % con fallecidos |
|---|---|---|
| Arrollamientos | 153 | **45.8** |
| Pérdida de pista | 504 | 22.4 |
| Choque frontal | 1 142 | 19.4 |
| Atropellos | 1 992 | 14.2 |
| Choque lateral | 4 858 | 4.8 |

- Veces más fatales con el vehículo: **bus 1.85**, **moto 1.72**, camión 1.44, automóvil 0.33.
- Por número de vehículos: 1 vehículo 12.3 % fatales, 2 vehículos 7.2 %.
- Urbano → rural: arrollamientos 37 → 59 %, atropellos 11 → 21 %, choque frontal 14 → 23 %, volcamientos 10 → 19 %. Solo «Otros» es más grave en la ciudad (9 % contra 7 %).

## 4. Análisis

1. **Los eventos de un solo actor son los más graves;** lo más frecuente (choque lateral) es lo menos grave.
2. **Bus y moto elevan el riesgo;** es una asociación, no una causa.
3. **La zona rural es más grave en casi todos los tipos** (la excepción es «Otros»).

## 5. Limitaciones

- Arrollamientos tiene solo 153 casos y 74 de ellos con vehículo no identificado. Bicicleta (100) y scooter (90) tienen pocos casos.
- Las razones comparan con y sin vehículo sin controlar vía, velocidad ni hora; hay un 22 % de siniestros con el vehículo 1 sin identificar.

## 6. Archivos

`p07_gravedad_por_tipo_siniestro.csv`, `p07_gravedad_por_vehiculo.csv` · `p07_gravedad_tipo_y_vehiculo.png`, `p07_heatmap_tipo_vehiculo.png`
