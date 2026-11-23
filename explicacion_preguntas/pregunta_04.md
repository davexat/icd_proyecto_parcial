# Pregunta de negocio 4: vehículos por provincia

> **Pregunta:** ¿En qué provincias pesan más las motocicletas, los camiones y los buses en los siniestros, y esas provincias son las mismas donde hay más siniestros?

**Script:** `pregunta_04.py` · **Técnicas:** porcentaje de siniestros que involucran cada tipo de vehículo por provincia, ranking por porcentaje y por cantidad, y mapas de burbujas con latitud y longitud, uno por vehículo (mapas facetados con Folium).

## 1. Qué hace el código

- Para cada provincia cuenta los siniestros totales y cuántos involucran al menos una motocicleta, un camión o un bus (`n_motocicleta`, `n_camion`, `n_bus`), y calcula el **porcentaje de los siniestros de la provincia** que incluyen ese vehículo. Solo usa las 20 provincias con 100 o más siniestros (quedan fuera Galápagos, Pastaza, Orellana y Napo, cuyo porcentaje es inestable). Guarda `p04_vehiculos_por_provincia.csv`.
- Dibuja tres mapas de burbujas de Folium lado a lado, uno por vehículo, con una burbuja por provincia en su coordenada promedio: el tamaño es el número de siniestros con ese vehículo y el color es el porcentaje de los siniestros de la provincia. Rotula las 3 provincias de mayor porcentaje y las 2 de mayor cantidad. En el HTML se puede hacer zoom y, al hacer clic en una burbuja, aparecen sus cifras.

## 2. Para la exposición (máx. 40 s)

> Cada mapa muestra un vehículo. El tamaño de la burbuja es cuántos siniestros lo involucran, y el color es el porcentaje de los siniestros de la provincia que lo incluyen. Las motocicletas pesan más en Santo Domingo y Los Ríos, donde participan en torno a la mitad de los siniestros, frente a un tercio en el país. Los camiones destacan en Cotopaxi y Cañar, y los buses en Chimborazo e Imbabura. En cantidad, en cambio, mandan Guayas y Pichincha. Por eso las provincias que destacan cambian según el vehículo.

*Figura a mostrar:* `p04_vehiculos_por_provincia.png`. 88 palabras, unos 35 s a ritmo normal.

## 3. Resultados

Siniestros que involucran cada vehículo (de 17 236): motocicleta 5 647 (**32.8 %**), camión 1 680 (**9.7 %**), bus 862 (**5.0 %**).

| Vehículo | Provincias con mayor porcentaje | Provincias con menor porcentaje | Mayor cantidad |
|---|---|---|---|
| Motocicleta (33 % nacional) | Santo Domingo **50.4 %**, Los Ríos 46.5 %, Esmeraldas 40.4 % | Zamora Chinchipe 17.8 %, Tungurahua 19.6 % | Guayas 1 934, Pichincha 1 015 |
| Camión (10 % nacional) | Cotopaxi **17.4 %**, Cañar 16.6 %, Carchi 16.1 %, Los Ríos 15.8 % | Santa Elena 5.8 %, Pichincha 6.7 % | Guayas 572, Pichincha 235 |
| Bus (5 % nacional) | Chimborazo **8.4 %**, Imbabura 8.3 %, Pichincha 7.2 % | El Oro 2.1 %, Bolívar 3.0 % | Pichincha 254, Guayas 223 |

Guayas y Pichincha concentran el 52.2 % de los siniestros con moto, el 48.0 % de los de camión y el 55.3 % de los de bus. Dentro de sus provincias el porcentaje es: Guayas 34.3 % con moto, 10.1 % con camión y 4.0 % con bus; Pichincha, 28.9 %, 6.7 % y 7.2 %.

## 4. Análisis

1. **Las provincias que destacan cambian según el vehículo:** las motos en Santo Domingo, Los Ríos y Esmeraldas (más del 40 %); los camiones en Cotopaxi, Cañar, Carchi y Los Ríos; los buses en Chimborazo, Imbabura y Pichincha.
2. **Porcentaje y cantidad cuentan historias distintas.** Por cantidad mandan Guayas y Pichincha en los tres vehículos, sobre todo porque tienen más siniestros en total (53.1 % del país); por porcentaje destacan provincias más pequeñas.
3. **Las diferencias son grandes:** la moto pasa de 17.8 % (Zamora Chinchipe) a 50.4 % (Santo Domingo); el camión, de 5.8 % (Santa Elena) a 17.4 % (Cotopaxi), tres veces más; el bus, de 2.1 % (El Oro) a 8.4 % (Chimborazo). Las medidas pueden ajustarse a cada provincia, por ejemplo control a motociclistas en Santo Domingo y Los Ríos y control de transporte de carga en Cotopaxi y Cañar.

## 5. Limitaciones

- **Muestra dónde participa cada vehículo, no cuál es más peligroso.** La gravedad por vehículo se trata en la pregunta 7.
- **No hay datos del parque automotor ni de kilómetros recorridos:** un porcentaje alto puede reflejar que en esa provincia circulan más vehículos de ese tipo, y no que sean más riesgosos.
- Un siniestro puede involucrar varios vehículos, por eso los porcentajes de moto, camión y bus no suman 100 %. "Camión" es solo esa categoría; no incluye camioneta ni furgoneta.
- La escala de color es distinta en cada mapa (moto de 18 a 50 %, camión de 6 a 17 %, bus de 2 a 8 %): sirve para comparar provincias dentro de un mismo vehículo, no entre vehículos.
- Los porcentajes de provincias con pocos casos (Zamora Chinchipe, 129 siniestros; Carchi, 118) son más variables.
- Folium necesita internet para el mapa base y el PNG se captura con Edge o Chrome (si no hay, se captura a mano desde el HTML).

## 6. Archivos

`p04_vehiculos_por_provincia.csv` · `p04_vehiculos_por_provincia.png` · `p04_vehiculos_por_provincia.html`
