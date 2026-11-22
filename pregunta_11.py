# PREGUNTA DE NEGOCIO 11 (adicional)
# ¿Qué provincias tienen una siniestralidad estable y cuáles volátil, y cuáles crecieron o
# decrecieron a lo largo de 2026?
#
# Técnicas: coeficiente de variación diario (CV > 1 = volátil, criterio del Ejemplo 2),
# representatividad en el total, variación porcentual entre el primer y el último trimestre
# disponibles, heatmap provincia x mes y facetas de las provincias principales.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import MESES, cargar_datos
from utilidades import CMAP_DIV, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
dias = pd.date_range(sin["fecha"].min(), sin["fecha"].max())
diario = sin.groupby(["provincia", "fecha"]).size().unstack(0).reindex(dias, fill_value=0).fillna(0)

# 1) Volatilidad: CV = desviación estándar diaria / media diaria
seccion("1) Volatilidad por provincia")
v = pd.DataFrame({"siniestros": diario.sum(), "media_dia": diario.mean(), "desv": diario.std()})
v["CV"] = v["desv"] / v["media_dia"]
v["representatividad %"] = 100 * v["siniestros"] / v["siniestros"].sum()
v["clase"] = np.where(v["CV"] > 1, "Volátil", "Estable")
v = v.sort_values("siniestros", ascending=False)
mostrar(v.round(2), 24)
guardar_tabla(v, "p11_volatilidad_provincias")
print("\nProvincias volátiles (CV > 1):", int((v["CV"] > 1).sum()), "| representan",
      f"{v.loc[v['CV'] > 1, 'representatividad %'].sum():.1f}% de los siniestros")

# 2) Cambio a lo largo del año: siniestros por día calendario en cada mes y variación primer vs último trimestre
seccion("2) Variación entre el primer y el último trimestre (provincias con 150 o más siniestros)")
dias_mes = pd.Series(dias).dt.month.value_counts().sort_index()
mes = diario.groupby(diario.index.month).sum().div(dias_mes, axis=0)
primero, ultimo = mes.index[:3], mes.index[-3:]
var = pd.DataFrame({"promedio primeros 3 meses": mes.loc[primero].mean(), "promedio últimos 3 meses": mes.loc[ultimo].mean()})
var["variación %"] = 100 * (var["promedio últimos 3 meses"] / var["promedio primeros 3 meses"] - 1)
var["siniestros"] = v["siniestros"]
var = var[var["siniestros"] >= 150].sort_values("variación %", ascending=False)
mostrar(var.round(2), 20)
guardar_tabla(var, "p11_variacion_provincias")

# 3) Gráficos
fig, ax = plt.subplots(1, 2, figsize=(15, 5.2))
col = v["clase"].map({"Volátil": PALETA[1], "Estable": PALETA[0]})
ax[0].scatter(v["representatividad %"], v["CV"], s=45, c=col, edgecolor="white")
ax[0].axhline(1, color="#52514e", lw=1)
for n_, off in [("GUAYAS", (-8, 10)), ("PICHINCHA", (-30, 10)), ("GALAPAGOS", (6, -4))]:     # solo 3 etiquetas para que no se monten
    ax[0].annotate(n_.title(), (v.loc[n_, "representatividad %"], v.loc[n_, "CV"]), fontsize=8, xytext=off, textcoords="offset points")
ax[0].set_xscale("log")
ax[0].set_xlabel("Representatividad en siniestros (% del total, escala log)")
ax[0].set_ylabel("Coeficiente de variación diario")
ax[0].set_title("Volatilidad vs representatividad por provincia")
ax[0].scatter([], [], color=PALETA[1], label="Volátil (CV > 1)")
ax[0].scatter([], [], color=PALETA[0], label="Estable (CV ≤ 1)")
ax[0].legend(frameon=False)
idx = mes[var.index] / mes[var.index].mean()
sns.heatmap((idx.T - 1) * 100, cmap=CMAP_DIV, center=0, annot=True, fmt=".0f", ax=ax[1],
            xticklabels=[MESES[m - 1][:3].title() for m in mes.index], cbar_kws={"label": "% sobre el promedio de la provincia"})
ax[1].set_yticklabels([t.get_text().title()[:18] for t in ax[1].get_yticklabels()], rotation=0)
ax[1].set_xlabel("Mes (2026)")
ax[1].set_ylabel("")
ax[1].set_title("Siniestros por día respecto al promedio de cada provincia")
guardar_fig(fig, "p11_volatilidad_y_variacion")

top6 = v.index[:6]
fig, ax = plt.subplots(2, 3, figsize=(14, 6), sharex=True)
for a, prov, c in zip(ax.ravel(), top6, PALETA):
    a.plot(mes.index, mes[prov], marker="o", color=c)
    a.set_title(prov.title()[:22])
    a.set_xticks(mes.index)
    a.set_xticklabels([MESES[m - 1][:1] for m in mes.index])
    a.set_ylim(bottom=0)
for a in ax[:, 0]:
    a.set_ylabel("Siniestros por día")
for a in ax[1]:
    a.set_xlabel("Mes (2026)")
guardar_fig(fig, "p11_facetas_provincias_principales")
