# PREGUNTA DE NEGOCIO 5
# ¿Qué causas probables (y qué factores humano / vehículo / vía) explican la mayor parte de los
# siniestros, y cuáles se asocian a mayor gravedad? ¿Cambia el peso de las causas según la hora?
#
# Técnicas: Pareto de causas, severidad por causa con intervalos de Wilson, chi-cuadrado y V de
# Cramér (causa x severidad), Kruskal-Wallis sobre víctimas por siniestro, gráfico de burbujas
# (frecuencia vs gravedad) y heatmap causa x franja horaria.
import textwrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from limpieza_datos import cargar_datos, FRANJAS
from utilidades import CMAP_SEC, PALETA, cramers_v, guardar_fig, guardar_tabla, mostrar, pareto_abc, seccion, wilson

sin, _ = cargar_datos()

# 1) Pareto de causas probables (26 códigos) y factor contribuyente
seccion("1) Frecuencia de causas")
corto = sin.groupby("cod_causa")["causa_probable"].agg(lambda s: textwrap.shorten(s.iloc[0].split("(")[0].strip().rstrip(".").capitalize(), 58, placeholder="…"))
abc = pareto_abc(sin.groupby("cod_causa").size())
abc["causa"] = abc.index.map(corto)
mostrar(abc[["causa", "valor", "%", "% acumulado", "clase"]].round(1), 12)
print("\nSiniestros por factor causal (modelo humano-vehículo-vía):")
print((sin["factor_causal"].value_counts(normalize=True) * 100).round(1).to_string())

# 2) Gravedad por grupo de causa
seccion("2) Gravedad por grupo de causa")
g = sin.groupby("causa_grupo").agg(siniestros=("sid", "size"), fatales=("fatal", "sum"), fallecidos=("fallecidos", "sum"),
                                   victimas=("n_victimas", "sum"), ponderada=("severidad_ponderada", "mean"))
g["% fatales"] = 100 * g["fatales"] / g["siniestros"]
g["ic_inf"], g["ic_sup"] = wilson(g["fatales"], g["siniestros"])
g["victimas_x_siniestro"] = g["victimas"] / g["siniestros"]
g = g.sort_values("% fatales", ascending=False)
mostrar(g.round(2), 12)
guardar_tabla(g, "p05_gravedad_por_grupo_causa")
chi2, p, v = cramers_v(pd.crosstab(sin["causa_grupo"], sin["severidad"]))
kw = stats.kruskal(*[x["n_victimas"].values for _, x in sin.groupby("causa_grupo")])
print(f"\nChi-cuadrado causa x severidad: chi2={chi2:.0f}, p={p:.2e}, V de Cramér={v:.3f}")
print(f"Kruskal-Wallis víctimas por siniestro entre grupos de causa: H={kw.statistic:.1f}, p={kw.pvalue:.2e}")

# 3) Gráficos: Pareto horizontal y burbujas frecuencia vs gravedad
fig, ax = plt.subplots(1, 2, figsize=(16, 6.5), gridspec_kw={"width_ratios": [1, 1.15]})
top = abc.head(10).iloc[::-1]
ax[0].barh(top["causa"], top["%"], color=PALETA[0])
for y, (v_, c_) in enumerate(zip(top["%"], top["% acumulado"])):
    ax[0].text(v_ + 0.3, y, f"{v_:.1f}%", va="center", fontsize=8)
ax[0].set_xlabel("% de siniestros")
ax[0].set_title("Top 10 causas probables")
col = {"Humano": PALETA[0], "Vehículo": PALETA[2], "Vía y entorno": PALETA[3]}
fac = sin.groupby("causa_grupo")["factor_causal"].first()
for gname, r in g.iterrows():
    ax[1].scatter(r["siniestros"], r["% fatales"], s=r["fallecidos"] * 3 + 20, color=col[fac[gname]], alpha=0.8,
                  edgecolor="white")
    ax[1].annotate(gname, (r["siniestros"], r["% fatales"]), fontsize=8, textcoords="offset points",
                   xytext={"Vehículo / carga": (6, -13), "Distracción al conducir": (-110, 12)}.get(gname, (6, 4)))
ax[1].axhline(100 * sin["fatal"].mean(), color="#52514e", ls="--", lw=1, label="Promedio nacional")
ax[1].set_xscale("log")
ax[1].set_xlabel("Siniestros (escala logarítmica)")
ax[1].set_ylabel("% de siniestros con fallecidos")
ax[1].set_title("Frecuencia vs gravedad (tamaño = fallecidos)")
for k, c in col.items():
    ax[1].scatter([], [], color=c, label=k)
ax[1].legend(title="Factor", frameon=False, loc="lower left")
guardar_fig(fig, "p05_pareto_y_burbujas")

# 4) Heatmaps: peso de cada causa por franja horaria y % fatal (celdas con n < 30 enmascaradas)
n = pd.crosstab(sin["causa_grupo"], sin["franja"])
share = n.div(n.sum(axis=0), axis=1) * 100
fat = sin.pivot_table(index="causa_grupo", columns="franja", values="fatal", aggfunc="mean", observed=False) * 100
fat = fat.where(n >= 30)
orden = g.index
fig, ax = plt.subplots(1, 2, figsize=(15, 5.5), sharey=True)
sns.heatmap(share.loc[orden], annot=True, fmt=".0f", cmap=CMAP_SEC, ax=ax[0], cbar_kws={"label": "% de los siniestros de la franja"})
ax[0].set_title("Peso de cada causa dentro de la franja horaria")
sns.heatmap(fat.loc[orden], annot=True, fmt=".0f", cmap=CMAP_SEC, ax=ax[1], cbar_kws={"label": "% de siniestros con fallecidos"})
ax[1].set_title("Gravedad por causa y franja (n ≥ 30)")
for a in ax:
    a.set_xlabel("Franja horaria")
    a.set_ylabel("")
    a.set_xticklabels([t.get_text().split(" ")[0] for t in a.get_xticklabels()], rotation=0)
guardar_fig(fig, "p05_heatmaps_causa_franja")
