# PREGUNTA DE NEGOCIO 6
# ¿Qué tipos de siniestro y qué vehículos involucrados concentran la mayor gravedad, y esa
# gravedad cambia entre zona urbana y rural?
#
# Técnicas: tabla de gravedad por tipo de siniestro, comparación del % de siniestros fatales con y
# sin cada tipo de vehículo, gráfico facetado urbano vs rural y heatmap tipo de siniestro x vehículo.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import cargar_datos
from utilidades import CMAP_SEC, PALETA, gravedad, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()

# 1) Gravedad por tipo de siniestro
seccion("1) Gravedad por tipo de siniestro")
t = gravedad(sin, "tipo_siniestro").sort_values("% fatales", ascending=False)
mostrar(t.round(2))
guardar_tabla(t, "p06_gravedad_por_tipo_siniestro")

# 2) % de siniestros fatales cuando participa cada vehículo frente a cuando no participa
seccion("2) Gravedad según el vehículo involucrado")
veh = ["automovil", "motocicleta", "camioneta", "suv", "camion", "bus", "bicicleta", "scooter", "furgoneta"]
filas = []
for v in veh:
    con, sin_v = sin[sin[f"n_{v}"] > 0], sin[sin[f"n_{v}"] == 0]
    if len(con) < 30:
        continue
    filas.append({"vehiculo": v, "siniestros": len(con), "% fatales (con el vehículo)": 100 * con["fatal"].mean(),
                  "% fatales (sin él)": 100 * sin_v["fatal"].mean()})
rr = pd.DataFrame(filas).set_index("vehiculo")
rr["veces más fatales"] = rr["% fatales (con el vehículo)"] / rr["% fatales (sin él)"]
rr = rr.sort_values("veces más fatales", ascending=False)
mostrar(rr.round(2))
guardar_tabla(rr, "p06_gravedad_por_vehiculo")
print("\n% fatales según número de vehículos (4 = 4 o más):")
nv = sin.assign(nveh=sin["n_vehiculos"].clip(upper=4)).groupby("nveh")["fatal"].agg(["size", "mean"])
nv["mean"] *= 100
mostrar(nv.rename(columns={"size": "siniestros", "mean": "% fatales"}).round(2))

# 3) Facetas urbano vs rural por tipo de siniestro
seccion("3) Gravedad urbana vs rural por tipo de siniestro")
z = gravedad(sin, ["tipo_siniestro", "zona"], minimo=30).reset_index()
orden = t.index[t["siniestros"] >= 100]
fig, ax = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)
for a, zona, c in zip(ax, ["URBANA", "RURAL"], PALETA):
    d = z[z["zona"] == zona].set_index("tipo_siniestro").reindex(orden).dropna(subset=["siniestros"])
    a.barh(range(len(d)), d["% fatales"], color=c)
    a.set_yticks(range(len(d)))
    a.set_yticklabels([i.capitalize() for i in d.index])
    a.invert_yaxis()
    a.set_title(f"Zona {zona.lower()}")
    a.set_xlabel("% de siniestros con fallecidos")
guardar_fig(fig, "p06_gravedad_tipo_por_zona")

# 4) Heatmap tipo de siniestro x vehículo 1 (% fatales; celdas con menos de 30 siniestros omitidas)
sub = sin[sin["tipo_veh_1"].notna()]
m = sub.pivot_table(index="tipo_siniestro", columns="tipo_veh_1", values="fatal", aggfunc="mean") * 100
n = sub.pivot_table(index="tipo_siniestro", columns="tipo_veh_1", values="fatal", aggfunc="size")
m = m.astype(float).where(n >= 30).dropna(how="all").dropna(axis=1, how="all")
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(m, annot=True, fmt=".0f", cmap=CMAP_SEC, ax=ax, cbar_kws={"label": "% de siniestros con fallecidos"})
ax.set_xlabel("Tipo de vehículo 1 (celdas con n < 30 omitidas)")
ax.set_ylabel("Tipo de siniestro")
ax.set_xticklabels([x.get_text().title()[:14] for x in ax.get_xticklabels()], rotation=45, ha="right")
ax.set_yticklabels([x.get_text().capitalize() for x in ax.get_yticklabels()], rotation=0)
guardar_fig(fig, "p06_heatmap_tipo_vehiculo")
