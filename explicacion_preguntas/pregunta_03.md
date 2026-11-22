# Pregunta de negocio 3: provincias y cantones

> **Pregunta:** ¿Qué provincias y cantones concentran la mayor parte de los siniestros y de las muertes, y el orden de prioridad cambia si se mide por volumen o por gravedad?

**Técnicas:** clasificación Pareto ABC (80-15-5), concentración del Top 5, ranking por volumen y por gravedad, gráfico Pareto facetado y mapa de burbujas con latitud y longitud.
**Verificación:** el script corre sin errores y genera 3 tablas y 2 figuras.

## 1. Qué hace el código

**Bloque 1: Pareto ABC.** Para provincia y cantón, y para dos medidas (siniestros y fallecidos), llama a `pareto_abc()` de `utilidades.py`. Esa función ordena de mayor a menor, calcula el porcentaje acumulado y asigna clase A (hasta el 80 %), B (hasta el 95 %) y C (el resto). Imprime cuántas unidades forman la clase A y cuánto suma el Top 5.

**Bloque 2: volumen frente a gravedad.** Usa `gravedad()` para obtener, por provincia, siniestros, fallecidos y % de siniestros con fallecidos. Añade la latitud y longitud promedio de cada provincia y dos rangos: por volumen y por gravedad. La tabla impresa se limita a provincias con 100 o más siniestros para no destacar porcentajes de muestras pequeñas.

**Bloque 3: gráficos.** (a) Dos Pareto lado a lado, uno para siniestros y otro para fallecidos, con barras de porcentaje y línea de acumulado, más la línea del 80 %. (b) Un mapa de burbujas: puntos grises con todos los siniestros, y una burbuja por provincia en su coordenada promedio (tamaño = volumen, color = % con fallecidos).

## 2. Resultados

| Medida | Unidades | Clase A (80 %) | Top 5 |
|---|---|---|---|
| Provincia, siniestros | 24 | 8 (33 %) | 70.3 % |
| Provincia, fallecidos | 24 | 10 (42 %) | 65.5 % |
| Cantón, siniestros | 210 | 35 (17 %) | 51.2 % |
| Cantón, fallecidos | 210 | 52 (25 %) | 39.1 % |

Provincias con más siniestros: Guayas 5 637 (32.7 %), Pichincha 3 507 (20.3 %), Santo Domingo 1 044 (6.1 %), Manabí 967, Tungurahua 955.

Provincias con más gravedad (100 o más siniestros): **Esmeraldas 25.3 %** (puesto 16 por volumen y 1 por gravedad), **Zamora Chinchipe 23.3 %**, **Cañar 19.5 %**, Sucumbíos 19.0 %, Los Ríos 17.5 %. Promedio nacional: 9.6 %.

## 3. Análisis

1. **El volumen está muy concentrado.** Un tercio de las provincias reúne el 80 % de los siniestros, y solo Guayas y Pichincha suman más de la mitad (53.1 %).
2. **Las muertes se reparten más que los siniestros.** Hacen falta más unidades para llegar al 80 % de los fallecidos (10 provincias y 52 cantones) que para llegar al 80 % de los siniestros (8 y 35).
3. **El orden de prioridad cambia con la medida.** Por volumen mandan Guayas y Pichincha, pero por gravedad suben provincias pequeñas como Esmeraldas, Zamora Chinchipe y Cañar. La política puede ser distinta según lo que se quiera reducir: eventos o muertes.

## 4. Limitaciones y advertencias

- **Santa Elena.** Sus siniestros pasan de 12 a 15 por mes (enero y febrero) a unos 75 por mes desde marzo, y todos provienen del ente CTE. Parece un cambio de cobertura del registro y puede inflar su posición (7.º en volumen).
- El porcentaje de fatales de provincias con pocos siniestros es inestable; por eso la tabla filtra a 100 o más.

## 5. Corrección recomendada en el mapa de burbujas

En la corrida original el mapa tenía tres problemas: los puntos de Galápagos (longitud cercana a -90) estiraban el eje y dejaban el continente aplastado; la barra de color tapaba el título; y las etiquetas de Guayas/Santa Elena y de Pichincha/Santo Domingo se montaban. Se probó este arreglo (reemplaza el último bloque de `pregunta_03.py`, desde `fig, ax = plt.subplots(figsize=(7.5, 7.5))`) y quedó legible:

```python
fig, ax = plt.subplots(figsize=(7.5, 7.5))
cont, prov_c = sin[sin["lon"] > -85], prov[prov["lon"] > -85]     # continente; Galápagos aparte
ax.scatter(cont["lon"], cont["lat"], s=1, color="#d9d8d3")
sc = ax.scatter(prov_c["lon"], prov_c["lat"], s=prov_c["siniestros"] / 8, c=prov_c["% fatales"], cmap=CMAP_SEC,
                edgecolor="white", linewidth=1, alpha=0.9)
OFF = {"GUAYAS": (-8, -40), "SANTA ELENA": (-10, -26), "PICHINCHA": (10, 18),
       "SANTO DOMINGO DE LOS TSACHILAS": (-90, 16)}
for n, r in prov_c.nlargest(8, "siniestros").iterrows():
    ax.annotate(n.title()[:14], (r["lon"], r["lat"]), fontsize=8, xytext=OFF.get(n, (6, 6)),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="-", color="#8a8a85", lw=0.6) if n in OFF else None)
ax.set_xlabel("Longitud (°)")
ax.set_ylabel("Latitud (°)")
ax.set_title("Siniestros por provincia (continente)\ntamaño = volumen, color = % con fallecidos")
fig.colorbar(sc, ax=ax, label="% de siniestros con fallecidos", shrink=0.7, pad=0.03)
ax.set_aspect("equal")
guardar_fig(fig, "p03_mapa_burbujas_provincias")
```

Galápagos queda fuera del mapa (5 siniestros en total); si se quiere mostrar, puede ir como recuadro aparte.

## 6. Archivos generados

- Tablas: `p03_abc_provincia_siniestros.csv`, `p03_abc_canton_siniestros.csv`, `p03_provincias.csv`
- Figuras: `p03_pareto_provincias.png`, `p03_mapa_burbujas_provincias.png`

**Cumple de las instrucciones:** datos espaciales (2.4), gráfico facetado (6.2) y mapa con latitud y longitud.
