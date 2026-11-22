# PREGUNTA DE NEGOCIO 3
# ¿Qué provincias y cantones concentran la mayor parte de los siniestros y de las muertes, y el
# orden de prioridad cambia si se mide por volumen o por gravedad?
#
# Técnicas: clasificación Pareto ABC (80-15-5), concentración del Top 5, ranking por volumen y por
# gravedad, gráfico Pareto facetado y mapa de burbujas con latitud y longitud.
import pandas as pd
import matplotlib.pyplot as plt

from limpieza_datos import cargar_datos
from utilidades import CMAP_SEC, PALETA, gravedad, guardar_fig, guardar_tabla, mostrar, pareto_abc, seccion

sin, _ = cargar_datos()

# 1) Pareto ABC por provincia y cantón, midiendo siniestros y fallecidos
seccion("1) Clasificación ABC (80-15-5)")
res = {}
for nivel in ["provincia", "canton"]:
    for medida, serie in [("siniestros", sin.groupby(nivel).size()), ("fallecidos", sin.groupby(nivel)["fallecidos"].sum())]:
        abc = pareto_abc(serie)
        res[(nivel, medida)] = abc
        n_a = (abc["clase"] == "A").sum()
        print(f"{nivel:9s} | {medida:10s} | {len(abc)} unidades | clase A: {n_a} ({100 * n_a / len(abc):.0f}% de las unidades) "
              f"= 80% | Top 5 = {abc['%'].head(5).sum():.1f}%")
    guardar_tabla(res[(nivel, "siniestros")], f"p03_abc_{nivel}_siniestros")
print("\nTop 10 provincias por siniestros:")
mostrar(res[("provincia", "siniestros")].round(1), 10)

# 2) Volumen vs gravedad por provincia (% de siniestros con fallecidos)
seccion("2) Volumen vs gravedad por provincia (provincias con 100 o más siniestros)")
prov = gravedad(sin, "provincia")
prov[["lat", "lon"]] = sin.groupby("provincia")[["lat", "lon"]].mean()
prov["rango por volumen"] = prov["siniestros"].rank(ascending=False)
prov["rango por gravedad"] = prov["% fatales"].rank(ascending=False)
mostrar(prov[prov["siniestros"] >= 100].sort_values("% fatales", ascending=False)[
    ["siniestros", "fallecidos", "% fatales", "rango por volumen", "rango por gravedad"]].round(1), 12)
guardar_tabla(prov, "p03_provincias")

# 3) Gráficos: Pareto facetado (siniestros | fallecidos) y mapa de burbujas
fig, ax = plt.subplots(1, 2, figsize=(14, 4.8))
for a, medida, c in zip(ax, ["siniestros", "fallecidos"], PALETA):
    abc = res[("provincia", medida)].head(12)
    a.bar(range(len(abc)), abc["%"], color=c)
    a.plot(range(len(abc)), abc["% acumulado"], color="#52514e", marker="o", ms=4)
    a.axhline(80, color=PALETA[3], ls="--", lw=1)
    a.set_ylim(0, 105)
    a.set_xticks(range(len(abc)))
    a.set_xticklabels([("Santo Domingo" if i.startswith("SANTO DOMINGO") else i.title()[:14]) for i in abc.index],
                      rotation=60, ha="right")
    a.set_ylabel(f"% del total de {medida} (barras) y acumulado (línea)")
    a.set_title(f"Pareto de provincias: {medida}")
guardar_fig(fig, "p03_pareto_provincias")

fig, ax = plt.subplots(figsize=(7.5, 7.5))
cont, prov_c = sin[sin["lon"] > -85], prov[prov["lon"] > -85]     # continente; Galápagos (5 siniestros) queda aparte
ax.scatter(cont["lon"], cont["lat"], s=1, color="#d9d8d3")
sc = ax.scatter(prov_c["lon"], prov_c["lat"], s=prov_c["siniestros"] / 8, c=prov_c["% fatales"], cmap=CMAP_SEC,
                edgecolor="white", linewidth=1, alpha=0.9)
OFF = {"GUAYAS": (-8, -40), "SANTA ELENA": (-10, -26), "PICHINCHA": (10, 18), "SANTO DOMINGO DE LOS TSACHILAS": (-90, 16),
       "ZAMORA CHINCHIPE": (8, -14), "CAÑAR": (-48, 8)}
# Etiquetas: las 8 provincias con más siniestros y las 3 más graves (Esmeraldas, Zamora Chinchipe, Cañar), que cita el guion
rotular = set(prov_c.nlargest(8, "siniestros").index) | {"ESMERALDAS", "ZAMORA CHINCHIPE", "CAÑAR"}
for n, r in prov_c.loc[sorted(rotular)].iterrows():
    ax.annotate("Zamora Chinchipe" if n == "ZAMORA CHINCHIPE" else n.title()[:14], (r["lon"], r["lat"]), fontsize=8,
                xytext=OFF.get(n, (6, 6)), textcoords="offset points",
                arrowprops=dict(arrowstyle="-", color="#8a8a85", lw=0.6) if n in OFF else None)
ax.set_xlabel("Longitud (°)")
ax.set_ylabel("Latitud (°)")
ax.set_title("Siniestros por provincia (continente)\ntamaño = volumen, color = % con fallecidos")
fig.colorbar(sc, ax=ax, label="% de siniestros con fallecidos", shrink=0.7, pad=0.03)
ax.set_aspect("equal")
guardar_fig(fig, "p03_mapa_burbujas_provincias")
