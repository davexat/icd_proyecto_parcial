# PREGUNTA DE NEGOCIO 9
# ¿Cómo influyen la zona (urbana o rural), la jerarquía de la vía y los corredores viales en la
# cantidad y gravedad de los siniestros, y cómo cambia eso a lo largo del día?
#
# Técnicas: comparación urbano / rural, ranking de corredores viales, gráfico facetado por zona y
# franja horaria, gráfico de burbujas y heatmap corredor x franja.
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import FRANJAS, cargar_datos
from utilidades import CMAP_SEC, PALETA, gravedad, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()

# 1) Urbano vs rural
seccion("1) Zona urbana vs rural")
z = gravedad(sin, "zona")
z["hora mediana"] = sin.groupby("zona")["hora_decimal"].median()
mostrar(z.round(2))
guardar_tabla(z, "p09_zona")

# 2) Red vial estatal: jerarquía y corredores (E35, E25, ...)
seccion("2) Red vial estatal")
via = sin[sin["via_estatal"]]
print(f"Siniestros en la red vial estatal: {len(via):,} ({100 * len(via) / len(sin):.1f}%); "
      f"% fatales {100 * via['fatal'].mean():.1f}% vs {100 * sin.loc[~sin['via_estatal'], 'fatal'].mean():.1f}% fuera de ella")
mostrar(gravedad(via.dropna(subset=["jerarquia_via"]), "jerarquia_via").round(2))
corr = gravedad(via, "ubicacion_via", minimo=60).sort_values("siniestros", ascending=False)
mostrar(corr.round(1), 15)
guardar_tabla(corr, "p09_corredores")

# 3) Facetas: gravedad por franja horaria, separando zona urbana y rural
seccion("3) Gravedad por franja horaria y zona")
f = gravedad(sin, ["zona", "franja"]).reset_index()
mostrar(f.round(1))
fig, ax = plt.subplots(1, 3, figsize=(16, 4.6), gridspec_kw={"width_ratios": [1, 1, 1.4]})
for a, zona, c in zip(ax[:2], ["URBANA", "RURAL"], PALETA):
    d = f[f["zona"] == zona].set_index("franja").reindex(FRANJAS)
    a.bar(range(4), d["% fatales"], color=c)
    a.set_xticks(range(4))
    a.set_xticklabels([x.split(" ")[0] for x in FRANJAS])
    a.set_ylim(0, 24)
    a.set_title(f"Zona {zona.lower()} (n = {int(d['siniestros'].sum()):,})")
    a.set_xlabel("Franja horaria")
    a.set_ylabel("% de siniestros con fallecidos")
# Burbujas: corredores viales
top = corr.head(12)
ax[2].scatter(top["siniestros"], top["% fatales"], s=top["fallecidos"] * 4, color=PALETA[0], alpha=0.75, edgecolor="white")
for n_, r in top.iterrows():
    ax[2].annotate(n_, (r["siniestros"], r["% fatales"]), fontsize=8, xytext=(5, 4), textcoords="offset points")
ax[2].axhline(100 * via["fatal"].mean(), color="#52514e", ls="--", lw=1)
ax[2].set_xlabel("Siniestros en el corredor")
ax[2].set_ylabel("% de siniestros con fallecidos")
ax[2].set_title("Corredores viales (tamaño = fallecidos)")
guardar_fig(fig, "p09_zona_franja_corredores")

# 4) Heatmap corredor x franja (siniestros) para los 10 corredores principales
m = via[via["ubicacion_via"].isin(top.index[:10])].pivot_table(index="ubicacion_via", columns="franja", values="sid",
                                                              aggfunc="count", observed=False).reindex(top.index[:10])
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(m, annot=True, fmt="d", cmap=CMAP_SEC, ax=ax, cbar_kws={"label": "Siniestros"})
ax.set_xlabel("Franja horaria")
ax.set_ylabel("Corredor vial (código de la red estatal)")
ax.set_xticklabels([x.get_text().split(" ")[0] for x in ax.get_xticklabels()], rotation=0)
guardar_fig(fig, "p09_heatmap_corredor_franja")
