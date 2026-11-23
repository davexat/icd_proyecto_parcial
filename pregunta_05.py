# PREGUNTA DE NEGOCIO 5
# ¿Cómo influyen la zona (urbana o rural), la jerarquía de la vía y los corredores viales en la
# cantidad y gravedad de los siniestros, y cómo cambia eso a lo largo del día?
#
# Técnicas: comparación urbano / rural, ranking de corredores viales, barras agrupadas por franja
# horaria y zona, gráfico de burbujas y heatmap corredor x franja.
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
guardar_tabla(z, "p05_zona")

# 2) Red vial estatal: jerarquía y corredores (E35, E25, ...)
seccion("2) Red vial estatal")
via = sin[sin["via_estatal"]]
print(f"Siniestros en la red vial estatal: {len(via):,} ({100 * len(via) / len(sin):.1f}%); "
      f"% fatales {100 * via['fatal'].mean():.1f}% vs {100 * sin.loc[~sin['via_estatal'], 'fatal'].mean():.1f}% fuera de ella")
mostrar(gravedad(via.dropna(subset=["jerarquia_via"]), "jerarquia_via").round(2))
corr = gravedad(via, "ubicacion_via", minimo=60).sort_values("siniestros", ascending=False)
mostrar(corr.round(1), 15)
guardar_tabla(corr, "p05_corredores")

# 3) Barras agrupadas: gravedad por franja horaria, con la zona urbana junto a la rural, y burbujas de corredores
seccion("3) Gravedad por franja horaria y zona")
f = gravedad(sin, ["zona", "franja"]).reset_index()
mostrar(f.round(1))
fig, ax = plt.subplots(1, 2, figsize=(14, 4.8), gridspec_kw={"width_ratios": [1, 1.2]})
for desp, zona, c in [(-0.2, "URBANA", PALETA[0]), (0.2, "RURAL", PALETA[1])]:
    d = f[f["zona"] == zona].set_index("franja").reindex(FRANJAS)
    barras = ax[0].bar([i + desp for i in range(4)], d["% fatales"], 0.4, color=c,
                       label=f"Zona {zona.lower()} (n = {int(d['siniestros'].sum()):,})")
    ax[0].bar_label(barras, fmt="%.1f", fontsize=8, padding=2)
ax[0].set_xticks(range(4))
ax[0].set_xticklabels([x.split(" ")[0] for x in FRANJAS])
ax[0].set_ylim(0, 24)
ax[0].set_xlabel("Franja horaria")
ax[0].set_ylabel("% de siniestros con fallecidos")
ax[0].set_title("Gravedad por franja horaria: urbana vs rural")
ax[0].legend(frameon=False, loc="upper right")
# Burbujas: corredores viales
top = corr.head(12)
ax[1].scatter(top["siniestros"], top["% fatales"], s=top["fallecidos"] * 4, color=PALETA[0], alpha=0.75, edgecolor="white")
for n_, r in top.iterrows():
    ax[1].annotate(n_, (r["siniestros"], r["% fatales"]), fontsize=8, xytext=(5, 4), textcoords="offset points")
ax[1].axhline(100 * via["fatal"].mean(), color="#52514e", ls="--", lw=1, label="Promedio de la red estatal")
ax[1].legend(frameon=False, loc="upper right")
ax[1].set_xlabel("Siniestros en el corredor")
ax[1].set_ylabel("% de siniestros con fallecidos")
ax[1].set_title("Corredores viales (tamaño = fallecidos)")
guardar_fig(fig, "p05_zona_franja_corredores")

# 4) Heatmap corredor x franja (siniestros) para los 10 corredores principales
m = via[via["ubicacion_via"].isin(top.index[:10])].pivot_table(index="ubicacion_via", columns="franja", values="sid",
                                                              aggfunc="count", observed=False).reindex(top.index[:10])
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(m, annot=True, fmt="d", cmap=CMAP_SEC, ax=ax, cbar_kws={"label": "Siniestros"})
ax.set_xlabel("Franja horaria")
ax.set_ylabel("Corredor vial (código de la red estatal)")
ax.set_xticklabels([x.get_text().split(" ")[0] for x in ax.get_xticklabels()], rotation=0)
guardar_fig(fig, "p05_heatmap_corredor_franja")
