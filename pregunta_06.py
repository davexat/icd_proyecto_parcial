# PREGUNTA DE NEGOCIO 6
# ¿Qué tipos de siniestro y qué vehículos involucrados concentran la mayor gravedad, y esa
# gravedad cambia entre zona urbana y rural?
#
# Técnicas: tabla cruzada tipo x severidad, intervalos de Wilson, riesgo relativo (con IC 95%) de
# que el siniestro sea fatal cuando participa cada tipo de vehículo, chi-cuadrado / V de Cramér,
# gráfico facetado urbano vs rural y heatmap tipo de siniestro x tipo de vehículo.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import cargar_datos
from utilidades import CMAP_SEC, PALETA, cramers_v, guardar_fig, guardar_tabla, mostrar, riesgo_relativo, seccion, wilson

sin, _ = cargar_datos()

# 1) Gravedad por tipo de siniestro
seccion("1) Gravedad por tipo de siniestro")
t = sin.groupby("tipo_siniestro").agg(siniestros=("sid", "size"), fatales=("fatal", "sum"), fallecidos=("fallecidos", "sum"),
                                      lesionados=("lesionados", "sum"))
t["% fatales"] = 100 * t["fatales"] / t["siniestros"]
t["ic_inf"], t["ic_sup"] = wilson(t["fatales"], t["siniestros"])
t["fallecidos_x100"] = 100 * t["fallecidos"] / t["siniestros"]
t["victimas_x_siniestro"] = (t["fallecidos"] + t["lesionados"]) / t["siniestros"]
t = t.sort_values("% fatales", ascending=False)
mostrar(t.round(2))
guardar_tabla(t, "p06_gravedad_por_tipo_siniestro")
chi2, p, v = cramers_v(pd.crosstab(sin["tipo_siniestro"], sin["severidad"]))
print(f"\nChi-cuadrado tipo x severidad: chi2={chi2:.0f}, p={p:.2e}, V de Cramér={v:.3f}")

# 2) Riesgo relativo de siniestro fatal según vehículo involucrado
seccion("2) Riesgo relativo de siniestro fatal según el vehículo involucrado")
veh = ["automovil", "motocicleta", "camioneta", "suv", "camion", "bus", "bicicleta", "scooter", "furgoneta"]
filas = []
for vname in veh:
    e = sin[sin[f"n_{vname}"] > 0]
    ne = sin[sin[f"n_{vname}"] == 0]
    if len(e) < 30:
        continue
    rr, lo, hi = riesgo_relativo(e["fatal"].sum(), len(e), ne["fatal"].sum(), len(ne))
    filas.append({"vehiculo": vname, "siniestros": len(e), "% fatales (con el vehículo)": 100 * e["fatal"].mean(),
                  "% fatales (sin él)": 100 * ne["fatal"].mean(), "RR": rr, "IC_inf": lo, "IC_sup": hi})
rr = pd.DataFrame(filas).set_index("vehiculo").sort_values("RR", ascending=False)
mostrar(rr.round(2))
guardar_tabla(rr, "p06_riesgo_relativo_vehiculo")
print("\n% fatales según número de vehículos:")
nv = sin.assign(nveh=sin["n_vehiculos"].clip(upper=4)).groupby("nveh")["fatal"].agg(["size", "mean"])
nv["mean"] *= 100
mostrar(nv.rename(columns={"size": "siniestros", "mean": "% fatales"}).round(2))

# 3) Facetas urbano vs rural por tipo de siniestro
seccion("3) Gravedad urbana vs rural por tipo de siniestro")
z = sin.groupby(["tipo_siniestro", "zona"]).agg(n=("sid", "size"), fat=("fatal", "sum")).reset_index()
z["% fatales"] = 100 * z["fat"] / z["n"]
z["ic_inf"], z["ic_sup"] = wilson(z["fat"], z["n"])
z = z[z["n"] >= 30]
orden = t.index[t["siniestros"] >= 100]
fig, ax = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)
for a, zona, c in zip(ax, ["URBANA", "RURAL"], PALETA):
    d = z[z["zona"] == zona].set_index("tipo_siniestro").reindex(orden).dropna()
    a.barh(range(len(d)), d["% fatales"], xerr=[d["% fatales"] - d["ic_inf"], d["ic_sup"] - d["% fatales"]],
           color=c, error_kw={"ecolor": "#52514e", "capsize": 2})
    a.set_yticks(range(len(d)))
    a.set_yticklabels([i.capitalize() for i in d.index])
    a.invert_yaxis()
    a.set_title(f"Zona {zona.lower()}")
    a.set_xlabel("% de siniestros con fallecidos (IC 95%)")
guardar_fig(fig, "p06_gravedad_tipo_por_zona")

# 4) Heatmap tipo de siniestro x vehículo 1 (% fatales; n >= 30)
sub = sin[sin["tipo_veh_1"].notna()]
m = sub.pivot_table(index="tipo_siniestro", columns="tipo_veh_1", values="fatal", aggfunc="mean") * 100
n = sub.pivot_table(index="tipo_siniestro", columns="tipo_veh_1", values="fatal", aggfunc="size")
m = m.where(n >= 30).dropna(how="all").dropna(axis=1, how="all")
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(m, annot=True, fmt=".0f", cmap=CMAP_SEC, ax=ax, cbar_kws={"label": "% de siniestros con fallecidos"})
ax.set_xlabel("Tipo de vehículo 1 (celdas con n < 30 omitidas)")
ax.set_ylabel("Tipo de siniestro")
ax.set_xticklabels([x.get_text().title()[:14] for x in ax.get_xticklabels()], rotation=45, ha="right")
ax.set_yticklabels([x.get_text().capitalize() for x in ax.get_yticklabels()], rotation=0)
guardar_fig(fig, "p06_heatmap_tipo_vehiculo")
