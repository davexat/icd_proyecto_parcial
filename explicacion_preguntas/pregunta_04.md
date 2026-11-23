# Pregunta de negocio 4: puntos críticos

> **Pregunta:** ¿Dónde están los puntos críticos (zonas pequeñas con muchos siniestros) en el país y en las ciudades con más eventos, y coinciden con los lugares donde ocurren las muertes?

**Script:** `pregunta_04.py` · **Técnicas:** cuadrícula de ~2 km, concentración en pocas celdas, ranking de celdas, mapas de celdas facetados por cantón y mapa de severidad, con Folium · **Feature:** celda de cuadrícula (Anderson, 2009; Xie y Yan, 2008).

## 1. Qué hace el código

- Agrupa los siniestros por `celda_lat` y `celda_lon` (coordenadas redondeadas a 0.02°, unos 2.2 km), cuenta siniestros y fallecidos por celda y calcula cuánto concentran el 1 %, 5 % y 10 % de las celdas más activas. Guarda las 50 principales.
- Para Guayaquil, Quito y Santo Domingo recorta coordenadas extremas, pinta cada celda más oscura mientras más siniestros tiene, marca con puntos naranja los siniestros con fallecidos y une las tres facetas en una página.
- Dibuja un mapa nacional con tres capas activables (sin víctimas, con lesionados, fatales).

## 2. Para la exposición (máx. 40 s)

> Dividimos el país en cuadrículas de unos dos kilómetros. El 5 % de las celdas concentra casi la mitad de los siniestros: esos son los puntos críticos. En los mapas de las tres ciudades principales, las celdas más oscuras marcan el núcleo; Santo Domingo está muy concentrado y Quito, disperso. Los puntos naranja son siniestros con fallecidos y aparecen también fuera de los núcleos. Respuesta: los puntos críticos existen y son claros, pero concentran cantidad, no letalidad, porque los fallecidos están más repartidos.

*Figura a mostrar:* `p04_densidad_facetado.png` (apoyo: `p04_mapa_nacional_severidad.png`). 84 palabras, unos 34 s a ritmo normal.

## 3. Resultados

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

## 5. Limitaciones

- La escala de color es distinta en cada faceta: sirve para ver la forma de cada ciudad, no para comparar intensidades.
- Las celdas críticas son urbanas y la zona urbana ya es menos letal (7.1 % frente a 14.0 %, pregunta 5), así que parte de la menor letalidad se debe a eso.
- En Guayaquil los puntos con fallecidos se acumulan en el núcleo; lo de «fuera de los núcleos» se ve sobre todo en Quito y Santo Domingo.
- Los puntos críticos describen dónde se concentraron los siniestros registrados entre enero y septiembre; no predicen dónde ocurrirá el próximo.
- La cuadrícula depende del tamaño de celda (0.02°). Folium necesita internet y el PNG se captura con Edge o Chrome.

## 6. Archivos

`p04_top50_celdas.csv`, `p04_concentracion_por_canton.csv` · `p04_densidad_facetado.png`, `p04_mapa_nacional_severidad.png` · `p04_densidad_facetado.html`, `p04_mapa_nacional_severidad.html`
