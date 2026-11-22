# Pregunta de negocio 4: puntos críticos

> **Pregunta:** ¿Dónde están los puntos críticos (zonas pequeñas con muchos siniestros) en el país y en las ciudades con más eventos, y coinciden con los lugares donde ocurren las muertes?

**Técnicas:** cuadrícula de ~2 km (agrupar por coordenadas), concentración en pocas celdas, ranking de celdas, mapa de severidad y mapas de densidad (hexbin) facetados por cantón.
**Feature nueva usada:** celda de cuadrícula (Anderson, 2009; Xie y Yan, 2008).
**Verificación:** el script corre sin errores y genera 2 tablas y 2 figuras.

## 1. Qué hace el código

**Bloque 1: concentración nacional.** Agrupa los siniestros por `celda_lat` y `celda_lon`, columnas que creó `limpieza_datos.py` redondeando cada coordenada al múltiplo de 0.02° más cercano (unos 2.2 km en el Ecuador). Por celda cuenta siniestros y fallecidos y toma el cantón más frecuente. Luego calcula el acumulado y responde: ¿cuánto concentra el 1 %, el 5 % y el 10 % de las celdas más activas? Guarda las 50 principales en `p04_top50_celdas.csv`.

**Bloque 2: mapas de densidad facetados.** Toma los tres cantones con más siniestros (Guayaquil, Quito, Santo Domingo). Para cada uno elimina las coordenadas extremas (por debajo del percentil 0.3 y por encima del 99.7) para que un punto lejano no estire el mapa, dibuja un `hexbin` de densidad y encima marca con puntos naranja los siniestros con fallecidos. También mide qué porcentaje de los siniestros del cantón cae en sus 5 celdas principales.

**Bloque 3: mapa nacional por severidad.** Dibuja todos los siniestros en latitud y longitud, con tres capas (sin víctimas, con lesionados, fatales), donde los fatales son más grandes y opacos.

## 2. Resultados

- Celdas con al menos un siniestro: **2 860**.
- El **1 %** de las celdas (29) concentra el **18.9 %** de los siniestros; el **5 %** (143), el **48.8 %**; el **10 %** (286), el **62.7 %**.
- Top 10 de celdas: 7 en Guayaquil, 2 en Santo Domingo y 1 en Quito. La mayor está en Guayaquil (lat -2.20, lon -79.90) con **269 siniestros y 12 fallecidos**.

| Cantón | Siniestros (tras recorte) | Celdas con eventos | % en sus 5 celdas principales |
|---|---|---|---|
| Guayaquil | 3 438 | 106 | 24.8 % |
| Quito | 3 019 | 162 | 17.4 % |
| Santo Domingo | 984 | 107 | **48.2 %** |

## 3. Análisis

1. **Los puntos críticos existen y son muy marcados.** Con el 5 % de las celdas se explica casi la mitad de los siniestros del país.
2. **Cada ciudad tiene un patrón distinto.** Santo Domingo es la más concentrada (casi la mitad en 5 celdas); Quito es la más dispersa (forma una franja norte-sur sin un núcleo único); Guayaquil está en el medio, con un núcleo muy denso alrededor de (-79.9, -2.2) y una cola hacia el oeste.
3. **Volumen y muertes no coinciden del todo.** Las 10 celdas principales suman 1 504 siniestros y 68 fallecidos, es decir, **4.5 fallecidos por cada 100 siniestros**, frente a **10.8** a nivel nacional. Los puntos críticos concentran *cantidad* de eventos, pero no son los más letales: los puntos con fallecidos aparecen también fuera de esos núcleos. Esto responde la segunda parte de la pregunta.

## 4. Limitaciones y advertencias

- La escala de color del hexbin es distinta en cada faceta (llega a ~420 en Guayaquil, ~70 en Quito, ~120 en Santo Domingo); sirve para ver la forma de cada ciudad, no para comparar intensidades entre ellas.
- La cuadrícula depende del tamaño de celda elegido (0.02°); con otro tamaño los números exactos cambiarían, aunque no la idea.
- El cálculo de 4.5 frente a 10.8 es una razón de fallecidos por siniestro hecha a partir de la tabla del Top 10; si se quiere citar en diapositiva, conviene dejarlo documentado.

## 5. Archivos generados

- Tablas: `p04_top50_celdas.csv`, `p04_concentracion_por_canton.csv`
- Figuras: `p04_densidad_facetado.png`, `p04_mapa_nacional_severidad.png`

**Cumple de las instrucciones:** datos espaciales (2.4), feature con referencia (punto 4), gráfico facetado (6.2).
