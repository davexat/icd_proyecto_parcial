# Pregunta de negocio 7: tipo de siniestro y vehículos

> **Pregunta:** ¿Qué tipos de siniestro y qué vehículos involucrados concentran la mayor gravedad, y esa gravedad cambia entre zona urbana y rural?

**Script:** `pregunta_07.py` · **Técnicas:** gravedad por tipo de siniestro, % de fatales con y sin cada vehículo, gráfico facetado urbano vs rural y heatmap tipo × vehículo.

## 1. Qué hace el código

- `gravedad()` por `tipo_siniestro` (13 tipos), ordenado por % con fallecidos.
- Para cada tipo de vehículo (30 o más siniestros) compara el % de fatales *cuando participa* contra *cuando no*, y calcula las "veces más fatales". También mira el % según el número de vehículos.
- Grafica dos paneles (urbana y rural) por tipo con 100 o más casos y un heatmap tipo de siniestro × vehículo 1 (celdas con 30 o más casos).

## 2. Para la exposición (máx. 40 s)

> Cada panel muestra el porcentaje de siniestros con fallecidos por tipo, uno para zona urbana y otro rural, con el mismo eje. Lo más grave son los eventos de un solo actor: atropellos, choques frontales, pérdidas de pista y volcamientos. Lo más frecuente, el choque lateral, es de lo menos letal. Y en todos los tipos la barra rural es más larga: la letalidad casi se duplica. En el heatmap, los siniestros con bus son 1.85 veces más fatales y con moto 1.72 veces. La gravedad depende del tipo, del vehículo y de la zona.

*Figura a mostrar:* `p07_gravedad_tipo_por_zona.png` (apoyo: `p07_heatmap_tipo_vehiculo.png`). 95 palabras, unos 38 s a ritmo normal.

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
- Urbano → rural: atropellos 11.3 → 21.3 %, choque frontal 14.1 → 22.5 %, volcamientos 9.5 → 18.7 %.

## 4. Análisis

1. **Los eventos de un solo actor son los más graves;** lo más frecuente (choque lateral) es lo menos grave.
2. **Bus y moto elevan el riesgo;** es una asociación, no una causa.
3. **La zona rural es más grave en todos los tipos.**

## 5. Limitaciones

- Arrollamientos tiene solo 153 casos y 74 de ellos con vehículo no identificado.
- Las razones comparan con y sin vehículo sin controlar vía, velocidad ni hora; hay un 22 % de siniestros con el vehículo 1 sin identificar.

## 6. Archivos

`p07_gravedad_por_tipo_siniestro.csv`, `p07_gravedad_por_vehiculo.csv` · `p07_gravedad_tipo_por_zona.png`, `p07_heatmap_tipo_vehiculo.png`
