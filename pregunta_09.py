# PREGUNTA DE NEGOCIO 9
# ¿Cómo influyen la zona (urbana/rural), la jerarquía de la vía y los corredores viales en la
# frecuencia y gravedad de los siniestros, y cómo cambia esa relación a lo largo del día?
#
# Técnicas: comparación urbano/rural (chi-cuadrado, Mann-Whitney, Wilson), gráfico facetado por
# zona y franja horaria, ranking de corredores viales (bubble plot) y heatmap corredor x franja.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from limpieza_datos import FRANJAS, cargar_datos
from utilidades import CMAP_SEC, PALETA, cramers_v, guardar_fig, guardar_tabla, mostrar, seccion, wilson

sin, _ = cargar_datos()

# 1) Urbano vs rural
seccion("1) Zona urbana vs rural")
z = sin.groupby("zona").agg(siniestros=("sid", "size"), fatales=("fatal", "sum"), fallecidos=("fallecidos", "sum"),
                            lesionados=("lesionados", "sum"), victimas_x_sin=("n_victimas", "mean"),
                            hora_mediana=("hora_decimal", "median"))
z["% fatales"] = 100 * z["fatales"] / z["siniestros"]
z["ic_inf"], z["ic_sup"] = wilson(z["fatales"], z["siniestros"])
mostrar(z.round(2))
chi2, p, v = cramers_v(pd.crosstab(sin["zona"], sin["severidad"]))
mw = stats.mannwhitneyu(sin.loc[sin["zona"] == "RURAL", "n_victimas"], sin.loc[sin["zona"] == "URBANA", "n_victimas"])
print(f"Zona x severidad: chi2={chi2:.0f}, p={p:.2e}, V de Cramér={v:.3f}; víctimas por siniestro rural vs urbano (Mann-Whitney) p={mw.pvalue:.2e}")
guardar_tabla(z, "p09_zona")

# 2) Red vial estatal: jerarquía y corredores (E35, E25, ...)
seccion("2) Red vial estatal")
via = sin[sin["via_estatal"]]
print(f"Siniestros en la red vial estatal: {len(via):,} ({100 * len(via) / len(sin):.1f}%); "
      f"% fatales {100 * via['fatal'].mean():.1f}% vs {100 * sin.loc[~sin['via_estatal'], 'fatal'].mean():.1f}% fuera de ella")
j = via.dropna(subset=["jerarquia_via"]).groupby("jerarquia_via").agg(siniestros=("sid", "size"), fatales=("fatal", "sum"))
j["% fatales"] = 100 * j["fatales"] / j["siniestros"]
mostrar(j.round(2))
corr = via.groupby("ubicacion_via").agg(siniestros=("sid", "size"), fatales=("fatal", "sum"), fallecidos=("fallecidos", "sum"))
corr = corr[corr["siniestros"] >= 60].copy()
corr["% fatales"] = 100 * corr["fatales"] / corr["siniestros"]
corr["ic_inf"], corr["ic_sup"] = wilson(corr["fatales"], corr["siniestros"])
corr = corr.sort_values("siniestros", ascending=False)
mostrar(corr.round(1), 15)
guardar_tabla(corr, "p09_corredores")

# 3) Facetas: gravedad por franja horaria, separando zona urbana/rural
seccion("3) Gravedad por franja horaria y zona")
f = sin.groupby(["zona", "franja"], observed=True).agg(n=("sid", "size"), fat=("fatal", "sum")).reset_index()
f["% fatales"] = 100 * f["fat"] / f["n"]
f["ic_inf"], f["ic_sup"] = wilson(f["fat"], f["n"])
mostrar(f.round(1))
fig, ax = plt.subplots(1, 3, figsize=(16, 4.6), gridspec_kw={"width_ratios": [1, 1, 1.4]})
for a, zona, c in zip(ax[:2], ["URBANA", "RURAL"], PALETA):
    d = f[f["zona"] == zona].set_index("franja").reindex(FRANJAS)
    a.bar(range(4), d["% fatales"], yerr=[d["% fatales"] - d["ic_inf"], d["ic_sup"] - d["% fatales"]], color=c,
          error_kw={"ecolor": "#52514e", "capsize": 3})
    a.set_xticks(range(4))
    a.set_xticklabels([x.split(" ")[0] for x in FRANJAS])
    a.set_ylim(0, 24)
    a.set_title(f"Zona {zona.lower()} (n = {int(d['n'].sum()):,})")
    a.set_xlabel("Franja horaria")
    a.set_ylabel("% de siniestros con fallecidos (IC 95%)")
# 4) Bubble: corredores viales
top = corr.head(12)
ax[2].scatter(top["siniestros"], top["% fatales"], s=top["fallecidos"] * 4, color=PALETA[0], alpha=0.75, edgecolor="white")
for n_, r in top.iterrows():
    ax[2].annotate(n_, (r["siniestros"], r["% fatales"]), fontsize=8, xytext=(5, 4), textcoords="offset points")
ax[2].axhline(100 * via["fatal"].mean(), color="#52514e", ls="--", lw=1)
ax[2].set_xlabel("Siniestros en el corredor")
ax[2].set_ylabel("% de siniestros con fallecidos")
ax[2].set_title("Corredores viales (tamaño = fallecidos)")
guardar_fig(fig, "p09_zona_franja_corredores")

# 5) Heatmap corredor x franja (siniestros) para los 10 corredores principales
m = via[via["ubicacion_via"].isin(top.index[:10])].pivot_table(index="ubicacion_via", columns="franja", values="sid",
                                                              aggfunc="count", observed=False).reindex(top.index[:10])
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(m, annot=True, fmt="d", cmap=CMAP_SEC, ax=ax, cbar_kws={"label": "Siniestros"})
ax.set_xlabel("Franja horaria")
ax.set_ylabel("Corredor vial (código de la red estatal)")
ax.set_xticklabels([x.get_text().split(" ")[0] for x in ax.get_xticklabels()], rotation=0)
guardar_fig(fig, "p09_heatmap_corredor_franja")
