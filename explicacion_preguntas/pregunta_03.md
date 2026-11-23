# Pregunta de negocio 3: provincias y cantones

> **Pregunta:** ¿Qué provincias y cantones concentran la mayor parte de los siniestros y de las muertes, y el ranking cambia si se mide por volumen o por gravedad?

**Script:** `pregunta_03.py` · **Técnicas:** Pareto ABC (80-15-5), Top 5, ranking por volumen y por gravedad, gráfico Pareto y mapa de burbujas con latitud y longitud hecho con Folium.

## 1. Qué hace el código

- `pareto_abc()` (en `utilidades.py`) ordena provincias y cantones, calcula el acumulado y asigna clase A (hasta 80 %), B (hasta 95 %) y C, para siniestros y para fallecidos.
- `gravedad()` da siniestros, fallecidos y % con fallecidos por provincia, con sus rangos por volumen y por gravedad (la tabla impresa filtra provincias con 100 o más siniestros).
- Grafica dos Pareto lado a lado y un mapa de burbujas de Folium (tamaño = volumen, color = % con fallecidos; rotula las 8 provincias con más siniestros y Esmeraldas, Zamora Chinchipe y Cañar). El mapa interactivo es el HTML y el PNG es su captura.

## 2. Para la exposición (máx. 40 s)

> A la izquierda, el Pareto: solo ocho de las 24 provincias reúnen el 80 % de los siniestros, y Guayas y Pichincha suman más de la mitad. A la derecha, el mapa: el tamaño de la burbuja es el volumen y el color es el porcentaje de siniestros con fallecidos. Las burbujas más grandes, Guayas y Pichincha, son claras; las más oscuras, como Esmeraldas, Zamora Chinchipe y Cañar, son pequeñas pero más letales. Por eso el ranking cambia: por volumen mandan dos provincias, por gravedad suben otras.

*Figuras a mostrar:* `p03_pareto_provincias.png` y `p03_mapa_burbujas_provincias.png`. 87 palabras, unos 35 s a ritmo normal.

## 3. Resultados

| Medida | Unidades | Clase A (80 %) | Top 5 |
|---|---|---|---|
| Provincia, siniestros | 24 | 8 (33 %) | 70.3 % |
| Provincia, fallecidos | 24 | 10 (42 %) | 65.5 % |
| Cantón, siniestros | 210 | 35 (17 %) | 51.2 % |
| Cantón, fallecidos | 210 | 52 (25 %) | 39.1 % |

- Volumen: Guayas 5 637 (32.7 %) y Pichincha 3 507 (20.3 %) suman 53 %.
- Gravedad (100 o más siniestros): **Esmeraldas 25.3 %** (16.ª en volumen), **Zamora Chinchipe 23.3 %**, **Cañar 19.5 %**. Promedio nacional: 9.6 %.

## 4. Análisis

1. **El volumen está muy concentrado** y las muertes se reparten más (10 provincias y 52 cantones para el 80 %, frente a 8 y 35 de siniestros).
2. **El ranking cambia con la medida:** por volumen mandan Guayas y Pichincha; por gravedad suben provincias pequeñas.

## 5. Limitaciones

- **Santa Elena** pasa de 12 a 15 siniestros mensuales a ~75 desde marzo, todos del ente CTE: parece un cambio de cobertura y puede inflar su posición (7.º en volumen).
- Los porcentajes de provincias con pocos siniestros son inestables (de ahí el filtro de 100).
- Galápagos (5 siniestros) queda fuera del encuadre. Folium necesita internet para el mapa base y el PNG se captura con Edge o Chrome (si no hay, se captura a mano desde el HTML).

## 6. Archivos

`p03_abc_provincia_siniestros.csv`, `p03_abc_canton_siniestros.csv`, `p03_provincias.csv` · `p03_pareto_provincias.png`, `p03_mapa_burbujas_provincias.png` · `p03_mapa_burbujas_provincias.html`
