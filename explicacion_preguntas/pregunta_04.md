# Pregunta de negocio 4: vehículos por provincia

> **Pregunta:** ¿En qué provincias pesan más las motocicletas, los camiones y los buses en los siniestros, y esas provincias son las mismas donde hay más siniestros?

<<<<<<< HEAD
**Script:** `pregunta_04.py` · **Técnicas:** cuadrícula de ~2 km, concentración en pocas celdas, ranking de celdas, mapas de celdas facetados por cantón y mapa de severidad, con Folium · **Feature:** celda de cuadrícula (Anderson, 2009; Xie y Yan, 2008).

## 1. Qué hace el código

- Agrupa los siniestros por `celda_lat` y `celda_lon` (coordenadas redondeadas a 0.02°, unos 2.2 km), cuenta siniestros y fallecidos por celda y calcula cuánto concentran el 1 %, 5 % y 10 % de las celdas más activas. Guarda las 50 principales.
- Para Guayaquil, Quito y Santo Domingo recorta coordenadas extremas, pinta cada celda más oscura mientras más siniestros tiene, marca con puntos naranja los siniestros con fallecidos y une las tres facetas en una página.
- Dibuja un mapa nacional con tres capas activables (sin víctimas, con lesionados, fatales).
=======
**Script:** `pregunta_04.py`
**Técnicas:** porcentaje de siniestros que involucran cada tipo de vehículo por provincia, ranking por porcentaje y por cantidad, y mapas de burbujas con latitud y longitud, uno por vehículo (Folium, mapas facetados).

## 1. Qué hace el código

**Bloque 1: porcentaje por provincia.** Para cada provincia cuenta los siniestros totales y cuántos involucran al menos una motocicleta, un camión o un bus (columnas `n_motocicleta`, `n_camion` y `n_bus`). Con eso calcula el **porcentaje de los siniestros de la provincia** que incluyen ese vehículo. Solo se usan las 20 provincias con 100 o más siniestros, porque con menos casos el porcentaje es inestable (quedan fuera Galápagos, Pastaza, Orellana y Napo). Imprime el ranking y guarda `p04_vehiculos_por_provincia.csv`.

**Bloque 2: mapas de burbujas facetados (Folium).** Tres mapas lado a lado, uno por vehículo, con una burbuja por provincia en su coordenada promedio. El tamaño es el número de siniestros con ese vehículo y el color es el porcentaje de los siniestros de la provincia. Cada mapa rotula las 3 provincias de mayor porcentaje y las 2 de mayor cantidad. En el HTML se puede hacer zoom y, al hacer clic en una burbuja, aparecen sus cifras.
>>>>>>> 4e8875d003616b9cfc0452894587cacd21c5c6c0

## 2. Para la exposición (máx. 40 s)

> Cada mapa muestra un vehículo. El tamaño de la burbuja es cuántos siniestros lo involucran, y el color es el porcentaje de los siniestros de la provincia que lo incluyen. Las motocicletas pesan más en Santo Domingo y Los Ríos, donde participan en torno a la mitad de los siniestros, frente a un tercio en el país. Los camiones destacan en Cotopaxi y Cañar, y los buses en Chimborazo e Imbabura. En cantidad, en cambio, mandan Guayas y Pichincha. Por eso el dónde cambia según el vehículo.

*Figura a mostrar:* `p04_vehiculos_por_provincia.png`. 87 palabras, unos 35 s a ritmo normal.

## 3. Resultados

<<<<<<< HEAD
- 2 860 celdas con siniestros. El **1 %** (29) concentra 18.9 % de los siniestros, el **5 %** (143) el **48.8 %** y el 10 % el 62.7 %.
- Esas mismas celdas concentran menos fallecidos: 8.7 %, **27.4 %** y 38.7 %.
- Top 10: 7 celdas en Guayaquil, 2 en Santo Domingo y 1 en Quito; la mayor, en Guayaquil, con 269 siniestros y 12 fallecidos.
- Las 10 celdas principales: 1 504 siniestros y 68 fallecidos = **4.5 fallecidos por 100 siniestros**, frente a **10.8** nacional.

| Cantón | Siniestros | % en sus 5 celdas principales |
|---|---|---|
| Guayaquil | 3 438 | 24.8 % |
| Quito | 3 019 | 17.4 % |
| Santo Domingo | 984 | **48.2 %** |

## 4. Análisis

1. **Los puntos críticos existen:** con el 5 % de las celdas se explica casi la mitad de los siniestros.
2. **Cada ciudad es distinta:** Santo Domingo la más concentrada; Quito la más dispersa (franja norte-sur); Guayaquil, con un núcleo denso.
3. **Volumen y muertes no coinciden:** los puntos críticos concentran cantidad, no letalidad.
=======
Siniestros que involucran cada vehículo (de 17 236): motocicleta 5 647 (**32.8 %**), camión 1 680 (**9.7 %**), bus 862 (**5.0 %**).

| Vehículo | Provincias con mayor porcentaje | Provincias con menor porcentaje | Mayor cantidad |
|---|---|---|---|
| Motocicleta (33 % nacional) | Santo Domingo **50.4 %**, Los Ríos 46.5 %, Esmeraldas 40.4 % | Zamora Chinchipe 17.8 %, Tungurahua 19.6 % | Guayas 1 934, Pichincha 1 015 |
| Camión (10 % nacional) | Cotopaxi **17.4 %**, Cañar 16.6 %, Carchi 16.1 %, Los Ríos 15.8 % | Santa Elena 5.8 %, Pichincha 6.7 % | Guayas 572, Pichincha 235 |
| Bus (5 % nacional) | Chimborazo **8.4 %**, Imbabura 8.3 %, Pichincha 7.2 % | El Oro 2.1 %, Bolívar 3.0 % | Pichincha 254, Guayas 223 |

Guayas y Pichincha concentran el 52.2 % de los siniestros con moto, el 48.0 % de los de camión y el 55.3 % de los de bus. Su porcentaje dentro de la provincia es: Guayas 34.3 % con moto, 10.1 % con camión y 4.0 % con bus; Pichincha, 28.9 %, 6.7 % y 7.2 %.

## 4. Análisis

1. **El mapa cambia según el vehículo.** Las motocicletas pesan sobre todo en Santo Domingo, Los Ríos y Esmeraldas (más del 40 %); los camiones, en Cotopaxi, Cañar, Carchi y Los Ríos; los buses, en Chimborazo, Imbabura y Pichincha.
2. **Porcentaje y cantidad cuentan historias distintas.** Por cantidad mandan Guayas y Pichincha en los tres vehículos, pero eso se debe sobre todo a que tienen más siniestros en total (53.1 % del país). Por porcentaje, en cambio, destacan provincias más pequeñas.
3. **Las diferencias entre provincias son grandes.** La moto pasa de 17.8 % (Zamora Chinchipe) a 50.4 % (Santo Domingo); el camión, de 5.8 % (Santa Elena) a 17.4 % (Cotopaxi), tres veces más; el bus, de 2.1 % (El Oro) a 8.4 % (Chimborazo).
4. **Implicación:** las medidas pueden ajustarse a cada provincia, por ejemplo controles a motociclistas en Santo Domingo y Los Ríos, y control de transporte de carga en Cotopaxi y Cañar.
>>>>>>> 4e8875d003616b9cfc0452894587cacd21c5c6c0

## 5. Limitaciones

<<<<<<< HEAD
- La escala de color es distinta en cada faceta: sirve para ver la forma de cada ciudad, no para comparar intensidades.
- Las celdas críticas son urbanas y la zona urbana ya es menos letal (7.1 % frente a 14.0 %, pregunta 5), así que parte de la menor letalidad se debe a eso.
- En Guayaquil los puntos con fallecidos se acumulan en el núcleo; lo de «fuera de los núcleos» se ve sobre todo en Quito y Santo Domingo.
- Los puntos críticos describen dónde se concentraron los siniestros registrados entre enero y septiembre; no predicen dónde ocurrirá el próximo.
- La cuadrícula depende del tamaño de celda (0.02°). Folium necesita internet y el PNG se captura con Edge o Chrome.
=======
- **Muestra dónde participa cada vehículo, no cuál es más peligroso.** La gravedad por vehículo se trata en la pregunta 7.
- **No hay datos del parque automotor ni de kilómetros recorridos.** Un porcentaje alto puede reflejar que en esa provincia circulan más vehículos de ese tipo, y no que sean más riesgosos.
- Un siniestro puede involucrar varios vehículos, por eso los porcentajes de moto, camión y bus no suman 100 %.
- "Camión" es solo la categoría camión; no incluye camioneta ni furgoneta.
- La escala de color es distinta en cada mapa (moto de 18 a 50 %, camión de 6 a 17 %, bus de 2 a 8 %); sirve para comparar provincias dentro de un mismo vehículo, no entre vehículos.
- Los porcentajes de las provincias con pocos casos (por ejemplo Zamora Chinchipe con 129 siniestros o Carchi con 118) son más variables.
- Los mapas de Folium necesitan internet para cargar el mapa base. El PNG se genera con una captura automática de Edge o Chrome; si no hay ninguno, se abre el HTML y se toma la captura a mano.
>>>>>>> 4e8875d003616b9cfc0452894587cacd21c5c6c0

## 6. Archivos

<<<<<<< HEAD
`p04_top50_celdas.csv`, `p04_concentracion_por_canton.csv` · `p04_densidad_facetado.png`, `p04_mapa_nacional_severidad.png` · `p04_densidad_facetado.html`, `p04_mapa_nacional_severidad.html`
=======
- Tabla: `p04_vehiculos_por_provincia.csv`
- Figura (captura del mapa): `p04_vehiculos_por_provincia.png`
- Mapa interactivo de Folium: `p04_vehiculos_por_provincia.html`
>>>>>>> 4e8875d003616b9cfc0452894587cacd21c5c6c0
