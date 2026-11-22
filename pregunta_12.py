# PREGUNTA DE NEGOCIO 12 (adicional)
# ¿Existe correlación entre los tipos de siniestro, las causas y los vehículos involucrados a nivel
# cantonal? ¿Cuáles "se mueven juntos" una vez descontado el tamaño del cantón?
#
# Técnicas: matriz cantón x categoría, coeficiente de correlación (Spearman, por rangos) sobre
# conteos y sobre porcentajes del cantón, heatmaps comparados y diagramas de dispersión (como en el Ejemplo 2).
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import cargar_datos
from utilidades import CMAP_DIV, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
MIN_SIN = 60                                   # solo cantones con al menos 60 siniestros
cant = sin["canton"].value_counts()
cant = cant[cant >= MIN_SIN].index
d = sin[sin["canton"].isin(cant)]
print(f"Cantones analizados: {len(cant)} ({100 * len(d) / len(sin):.1f}% de los siniestros)")

# Matriz cantón x categoría (conteos) y composición porcentual del cantón
tipos = sin["tipo_siniestro"].value_counts().head(7).index
causas = sin["causa_grupo"].value_counts().head(5).index
vehs = ["automovil", "motocicleta", "camioneta", "suv", "camion", "bus"]
cols = {}
for t in tipos:
    cols[f"Tipo: {t.capitalize()}"] = d[d["tipo_siniestro"] == t].groupby("canton").size()
for c in causas:
    cols[f"Causa: {c}"] = d[d["causa_grupo"] == c].groupby("canton").size()
for v in vehs:
    cols[f"Vehículo: {v}"] = d[d[f"n_{v}"] > 0].groupby("canton").size()
cols["Con fallecidos"] = d[d["fatal"]].groupby("canton").size()
X = pd.DataFrame(cols).reindex(cant).fillna(0)
P = X.div(d.groupby("canton").size().reindex(cant), axis=0) * 100          # % del total de siniestros del cantón

seccion("1) Correlación entre categorías")
c_cnt, c_pct = X.corr(method="spearman"), P.corr(method="spearman")
print(f"Correlación media entre pares: conteos = {c_cnt.values[np.triu_indices(len(c_cnt), 1)].mean():.2f} | "
      f"% del cantón = {c_pct.values[np.triu_indices(len(c_pct), 1)].mean():.2f}")
print("Con conteos casi todo se correlaciona con todo porque los cantones grandes tienen más de todo.")

# Pares más correlacionados en composición (se omiten pares de la misma familia, que son casi complementarios)
pares = c_pct.where(np.triu(np.ones(c_pct.shape), 1).astype(bool)).stack().rename("correlación").reset_index()
pares.columns = ["a", "b", "correlación"]
pares = pares[pares["a"].str.split(":").str[0] != pares["b"].str.split(":").str[0]]
pares = pares.reindex(pares["correlación"].abs().sort_values(ascending=False).index)
mostrar(pares.head(12).round(2), 12)
guardar_tabla(pares, "p12_pares_correlacion", indice=False)

# Heatmaps comparados
fig, ax = plt.subplots(1, 2, figsize=(18, 7.5))
for a, c, t in [(ax[0], c_cnt, "Sobre conteos (efecto tamaño)"), (ax[1], c_pct, "Sobre % del cantón")]:
    sns.heatmap(c, cmap=CMAP_DIV, center=0, vmin=-1, vmax=1, ax=a, annot=True, fmt=".1f", annot_kws={"size": 6},
                cbar_kws={"label": "Correlación"}, xticklabels=True, yticklabels=True if a is ax[0] else False)
    a.set_title(t)
guardar_fig(fig, "p12_heatmaps_correlacion")

# Dispersión de los 4 pares más correlacionados en composición
top = pares.head(4)
fig, ax = plt.subplots(1, 4, figsize=(18, 4.2))
for a, (_, r) in zip(ax, top.iterrows()):
    a.scatter(P[r["a"]], P[r["b"]], color=PALETA[0], alpha=0.75, edgecolor="white")
    m, b = np.polyfit(P[r["a"]], P[r["b"]], 1)
    xs = np.linspace(P[r["a"]].min(), P[r["a"]].max(), 50)
    a.plot(xs, m * xs + b, color=PALETA[1], lw=1.5)
    a.set_xlabel(r["a"] + " (% del cantón)", fontsize=8)
    a.set_ylabel(r["b"] + " (% del cantón)", fontsize=8)
    a.set_title(f"correlación = {r['correlación']:.2f}")
guardar_fig(fig, "p12_dispersion_pares_top")
