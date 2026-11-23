# PREGUNTA DE NEGOCIO 7
# ¿Qué tipos de siniestro y qué vehículos involucrados concentran la mayor gravedad, y esa
# gravedad cambia entre zona urbana y rural?
#
# Técnicas: tabla de gravedad por tipo de siniestro, comparación del % de siniestros fatales con y
# sin cada tipo de vehículo, barras agrupadas urbano vs rural y heatmap tipo de siniestro x vehículo.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import cargar_datos
from utilidades import CMAP_SEC, GRIS, PALETA, gravedad, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()

# 1) Gravedad por tipo de siniestro
seccion("1) Gravedad por tipo de siniestro")
t = gravedad(sin, "tipo_siniestro").sort_values("% fatales", ascending=False)
mostrar(t.round(2))
guardar_tabla(t, "p07_gravedad_por_tipo_siniestro")

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
guardar_tabla(rr, "p07_gravedad_por_vehiculo")
print("\n% fatales según número de vehículos (4 = 4 o más):")
nv = sin.assign(nveh=sin["n_vehiculos"].clip(upper=4)).groupby("nveh")["fatal"].agg(["size", "mean"])
nv["mean"] *= 100
mostrar(nv.rename(columns={"size": "siniestros", "mean": "% fatales"}).round(2))

# 3) Gráfico: % de siniestros con fallecidos por tipo de siniestro (urbana vs rural) y por vehículo (con vs sin él)
seccion("3) Gravedad urbana vs rural por tipo de siniestro")
z = gravedad(sin, ["tipo_siniestro", "zona"], minimo=30).reset_index()
orden = list(t.index[t["siniestros"] >= 100])               # ya viene ordenado de mayor a menor gravedad
media = 100 * sin["fatal"].mean()
fig, ax = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={"width_ratios": [1.15, 1]})
alto = 0.38
for desp, zona, c in [(-alto / 2, "URBANA", PALETA[0]), (alto / 2, "RURAL", PALETA[1])]:
    d = z[z["zona"] == zona].set_index("tipo_siniestro").reindex(orden)
    b = ax[0].barh([i + desp for i in range(len(orden))], d["% fatales"], alto, color=c, label=f"Zona {zona.lower()}")
    ax[0].bar_label(b, fmt="%.0f", fontsize=8, padding=2)
ax[0].set_yticks(range(len(orden)))
ax[0].set_yticklabels([f"{i.capitalize()} ({int(t.loc[i, 'siniestros']):,})" for i in orden])
ax[0].invert_yaxis()
ax[0].axvline(media, color="#52514e", ls="--", lw=1)
ax[0].text(media + 0.6, len(orden) - 0.6, f"Promedio nacional ({media:.1f} %)", fontsize=8, color="#52514e")
ax[0].set_xlabel("% de siniestros con fallecidos")
ax[0].set_title("Qué tipo de siniestro: urbana vs rural")
ax[0].legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2)
rv = rr.sort_values("veces más fatales")
b = ax[1].barh([i + alto / 2 for i in range(len(rv))], rv["% fatales (con el vehículo)"], alto, color=PALETA[0], label="Siniestros CON el vehículo")
ax[1].barh([i - alto / 2 for i in range(len(rv))], rv["% fatales (sin él)"], alto, color=GRIS, label="Siniestros SIN el vehículo")
for i, (_, r) in enumerate(rv.iterrows()):
    ax[1].text(r["% fatales (con el vehículo)"] + 0.3, i + alto / 2, f"{r['veces más fatales']:.2f}×", va="center", fontsize=8)
ax[1].set_yticks(range(len(rv)))
NOMBRES = {"camion": "Camión", "suv": "SUV", "automovil": "Automóvil"}
ax[1].set_yticklabels([f"{NOMBRES.get(i, i.capitalize())} ({int(n):,})" for i, n in rv["siniestros"].items()])
ax[1].axvline(media, color="#52514e", ls="--", lw=1)
ax[1].set_xlabel("% de siniestros con fallecidos (× = veces más fatales con el vehículo que sin él)")
ax[1].set_title("Qué vehículo: con vs sin él")
ax[1].legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2)
guardar_fig(fig, "p07_gravedad_tipo_y_vehiculo")

# 4) Heatmap tipo de siniestro x vehículo 1 (% fatales; celdas con menos de 30 siniestros omitidas)
sub = sin[sin["tipo_veh_1"].notna()]
m = sub.pivot_table(index="tipo_siniestro", columns="tipo_veh_1", values="fatal", aggfunc="mean") * 100
n = sub.pivot_table(index="tipo_siniestro", columns="tipo_veh_1", values="fatal", aggfunc="size")
m = m.astype(float).where(n >= 30).dropna(how="all").dropna(axis=1, how="all")
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(m, annot=True, fmt=".0f", cmap=CMAP_SEC, ax=ax, cbar_kws={"label": "% de siniestros con fallecidos"})
ax.set_xlabel("Tipo de vehículo 1 (celdas con n < 30 omitidas)")
ax.set_ylabel("Tipo de siniestro")
ax.set_xticklabels([x.get_text().title().replace("Vehículo Deportivo Utilitario", "Utilitario deportivo") for x in ax.get_xticklabels()], rotation=45, ha="right")
ax.set_yticklabels([x.get_text().capitalize() for x in ax.get_yticklabels()], rotation=0)
guardar_fig(fig, "p07_heatmap_tipo_vehiculo")
