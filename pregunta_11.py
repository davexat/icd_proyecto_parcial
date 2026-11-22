# PREGUNTA DE NEGOCIO 11 (adicional)
# ¿Qué provincias tienen una siniestralidad estable y cuáles volátil, y cuáles muestran una
# tendencia creciente o decreciente a lo largo de 2026?
#
# Técnicas: coeficiente de variación diario (CV > 1 = volátil, criterio del Ejemplo 2) frente al CV
# esperado de un proceso de Poisson, índice de sobredispersión, tau de Kendall sobre la serie
# mensual y heatmap provincia x mes con facetas de las provincias principales.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from limpieza_datos import MESES, cargar_datos
from utilidades import CMAP_DIV, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
dias = pd.date_range(sin["fecha"].min(), sin["fecha"].max())
diario = sin.groupby(["provincia", "fecha"]).size().unstack(0).reindex(dias, fill_value=0).fillna(0)

# 1) Volatilidad: CV observado, CV esperado bajo Poisson e índice de sobredispersión (varianza / media)
seccion("1) Volatilidad por provincia")
v = pd.DataFrame({"siniestros": diario.sum(), "media_dia": diario.mean(), "desv": diario.std()})
v["CV"] = v["desv"] / v["media_dia"]
v["CV_poisson"] = 1 / np.sqrt(v["media_dia"])
v["sobredispersion"] = diario.var() / diario.mean()
v["representatividad %"] = 100 * v["siniestros"] / v["siniestros"].sum()
v["clase"] = np.where(v["CV"] > 1, "Volátil", "Estable")
v = v.sort_values("siniestros", ascending=False)
mostrar(v.round(2), 24)
guardar_tabla(v, "p11_volatilidad_provincias")
print("\nProvincias volátiles (CV>1):", int((v["CV"] > 1).sum()), "| con representatividad conjunta de",
      f"{v.loc[v['CV'] > 1, 'representatividad %'].sum():.1f}% de los siniestros")

# 2) Tendencia mensual: siniestros por día calendario y tau de Kendall (enero-septiembre)
seccion("2) Tendencia mensual (siniestros por día)")
dias_mes = pd.Series(dias).dt.month.value_counts().sort_index()
mes = diario.groupby(diario.index.month).sum().div(dias_mes, axis=0)
tend = []
for prov in mes.columns:
    if v.loc[prov, "siniestros"] >= 150:
        tau, p = stats.kendalltau(mes.index, mes[prov])
        pend = np.polyfit(mes.index, mes[prov] / mes[prov].mean(), 1)[0] * 100
        tend.append({"provincia": prov, "siniestros": v.loc[prov, "siniestros"], "tau": tau, "p": p, "variación % por mes": pend})
tend = pd.DataFrame(tend).set_index("provincia").sort_values("tau", ascending=False)
tend["tendencia"] = np.where(tend["p"] < 0.05, np.where(tend["tau"] > 0, "Creciente", "Decreciente"), "Sin tendencia clara")
mostrar(tend.round(3), 20)
guardar_tabla(tend, "p11_tendencia_provincias")

# 3) Gráficos
fig, ax = plt.subplots(1, 2, figsize=(15, 5.2))
col = v["clase"].map({"Volátil": PALETA[1], "Estable": PALETA[0]})
ax[0].scatter(v["representatividad %"], v["CV"], s=45, c=col, edgecolor="white")
xs = np.linspace(v["media_dia"].min(), v["media_dia"].max(), 100)
rep = xs / v["media_dia"].sum() * 100
ax[0].plot(rep, 1 / np.sqrt(xs), color="#8a8a85", ls="--", label="CV esperado si fuera Poisson")
ax[0].axhline(1, color="#52514e", lw=1)
for n_, r in v.head(6).iterrows():
    ax[0].annotate(n_.title()[:12], (r["representatividad %"], r["CV"]), fontsize=8, xytext=(5, 4), textcoords="offset points")
ax[0].set_xscale("log")
ax[0].set_xlabel("Representatividad en siniestros (% del total, escala log)")
ax[0].set_ylabel("Coeficiente de variación diario")
ax[0].set_title("Volatilidad vs representatividad por provincia")
ax[0].scatter([], [], color=PALETA[1], label="Volátil (CV > 1)")
ax[0].scatter([], [], color=PALETA[0], label="Estable (CV ≤ 1)")
ax[0].legend(frameon=False)
idx = mes[tend.index] / mes[tend.index].mean()
sns.heatmap((idx.T - 1) * 100, cmap=CMAP_DIV, center=0, annot=True, fmt=".0f", ax=ax[1],
            xticklabels=[m[:3].title() for m in MESES], cbar_kws={"label": "% sobre el promedio de la provincia"})
ax[1].set_yticklabels([t.get_text().title()[:18] for t in ax[1].get_yticklabels()], rotation=0)
ax[1].set_xlabel("Mes (2026)")
ax[1].set_ylabel("")
ax[1].set_title("Siniestros por día respecto al promedio de cada provincia")
guardar_fig(fig, "p11_volatilidad_y_tendencia")

top6 = v.index[:6]
fig, ax = plt.subplots(2, 3, figsize=(14, 6), sharex=True)
for a, prov, c in zip(ax.ravel(), top6, PALETA):
    a.plot(mes.index, mes[prov], marker="o", color=c)
    a.set_title(prov.title()[:22])
    a.set_xticks(mes.index)
    a.set_xticklabels([m[:1] for m in MESES])
    a.set_ylim(bottom=0)
for a in ax[:, 0]:
    a.set_ylabel("Siniestros por día")
for a in ax[1]:
    a.set_xlabel("Mes (2026)")
guardar_fig(fig, "p11_facetas_provincias_principales")
