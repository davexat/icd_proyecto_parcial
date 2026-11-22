# PREGUNTA DE NEGOCIO 3
# ¿Cómo se concentran geográficamente los siniestros y las muertes (provincias y cantones), y el
# orden de prioridad territorial cambia según se mida por volumen de siniestros o por letalidad?
#
# Técnicas: clasificación Pareto ABC (80-15-5), curva de Lorenz e índice de Gini, concentración del
# Top-5, correlación de rangos de Spearman, intervalos de Wilson y mapa de burbujas.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

from limpieza_datos import cargar_datos
from utilidades import CMAP_SEC, PALETA, gini, guardar_fig, guardar_tabla, lorenz, mostrar, pareto_abc, seccion, wilson

sin, _ = cargar_datos()

# 1) Pareto ABC por provincia y cantón, midiendo siniestros y fallecidos
seccion("1) Clasificación ABC (80-15-5) y concentración")
res = {}
for nivel in ["provincia", "canton"]:
    for medida, serie in [("siniestros", sin.groupby(nivel).size()), ("fallecidos", sin.groupby(nivel)["fallecidos"].sum())]:
        abc = pareto_abc(serie)
        res[(nivel, medida)] = abc
        n_a = (abc["clase"] == "A").sum()
        print(f"{nivel:9s} | {medida:10s} | {len(abc)} unidades | clase A: {n_a} ({100 * n_a / len(abc):.0f}% de las unidades) "
              f"= 80% | Top-5 = {abc['%'].head(5).sum():.1f}% | Gini = {gini(serie):.3f}")
    guardar_tabla(res[(nivel, "siniestros")], f"p03_abc_{nivel}_siniestros")
print("\nTop 10 provincias por siniestros:")
mostrar(res[("provincia", "siniestros")].round(2), 10)

# 2) Ranking: volumen vs letalidad (fallecidos por 100 siniestros) con IC
seccion("2) Volumen vs letalidad por provincia")
prov = sin.groupby("provincia").agg(siniestros=("sid", "size"), fatales=("fatal", "sum"), fallecidos=("fallecidos", "sum"),
                                    lat=("lat", "mean"), lon=("lon", "mean"))
prov["fallecidos_x100"] = 100 * prov["fallecidos"] / prov["siniestros"]
prov["%_fatales"] = 100 * prov["fatales"] / prov["siniestros"]
prov["ic_inf"], prov["ic_sup"] = wilson(prov["fatales"], prov["siniestros"])
prov["rango_volumen"] = prov["siniestros"].rank(ascending=False)
prov["rango_letalidad"] = prov["%_fatales"].rank(ascending=False)
rho, p = stats.spearmanr(prov["siniestros"], prov["%_fatales"])
print(f"Spearman entre volumen y % de siniestros fatales (24 provincias): rho={rho:.2f}, p={p:.3f}")
sig = prov[prov["siniestros"] >= 100].sort_values("%_fatales", ascending=False)
mostrar(sig[["siniestros", "fallecidos", "%_fatales", "ic_inf", "ic_sup", "rango_volumen", "rango_letalidad"]].round(1), 12)
guardar_tabla(prov, "p03_provincias")

# 3) Gráficos: Pareto facetado (siniestros | fallecidos), Lorenz y mapa de burbujas
fig, ax = plt.subplots(1, 3, figsize=(17, 4.8))
for a, medida, c in zip(ax[:2], ["siniestros", "fallecidos"], PALETA):
    abc = res[("provincia", medida)].head(12)
    a.bar(range(len(abc)), abc["%"], color=c)
    a.plot(range(len(abc)), abc["% acumulado"], color="#52514e", marker="o", ms=4, label="% acumulado")
    a.axhline(80, color=PALETA[3], ls="--", lw=1)
    a.set_ylim(0, 105)
    a.set_xticks(range(len(abc)))
    a.set_xticklabels([i.title()[:12] for i in abc.index], rotation=60, ha="right")
    a.set_ylabel(f"% del total de {medida} (barras) y acumulado (línea)")
    a.set_title(f"Pareto de provincias: {medida}")
for nivel, c in [("provincia", PALETA[0]), ("canton", PALETA[1])]:
    y, x = lorenz(sin.groupby(nivel).size().values)
    ax[2].plot(x, y, color=c, label=f"{nivel.title()} (Gini {gini(sin.groupby(nivel).size()):.2f})")
ax[2].plot([0, 1], [0, 1], color=PALETA[3], ls="--", label="Igualdad perfecta")
ax[2].set_xlabel("Proporción acumulada de unidades (de menos a más siniestros)")
ax[2].set_ylabel("Proporción acumulada de siniestros")
ax[2].set_title("Curva de Lorenz")
ax[2].legend(frameon=False)
guardar_fig(fig, "p03_pareto_y_lorenz")

fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.scatter(sin["lon"], sin["lat"], s=1, color="#d9d8d3")
sc = ax.scatter(prov["lon"], prov["lat"], s=prov["siniestros"] / 8, c=prov["%_fatales"], cmap=CMAP_SEC,
                edgecolor="white", linewidth=1, alpha=0.9)
for n, r in prov.nlargest(8, "siniestros").iterrows():
    ax.annotate(n.title()[:14], (r["lon"], r["lat"]), fontsize=8, xytext=(6, 6), textcoords="offset points")
ax.set_xlabel("Longitud (°)")
ax.set_ylabel("Latitud (°)")
ax.set_title("Siniestros por provincia: tamaño = volumen, color = % con fallecidos")
fig.colorbar(sc, ax=ax, label="% de siniestros con fallecidos", shrink=0.7)
ax.set_aspect("equal")
guardar_fig(fig, "p03_mapa_burbujas_provincias")
