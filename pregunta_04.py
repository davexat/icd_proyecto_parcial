# PREGUNTA DE NEGOCIO 4
# ¿Dónde están los puntos críticos (zonas pequeñas con muchos siniestros) en el país y en las
# ciudades con más eventos, y coinciden con los lugares donde ocurren las muertes?
#
# Técnicas: cuadrícula de ~2 km (agrupar por coordenadas), concentración en pocas celdas,
# ranking de celdas, mapa de severidad y mapas de densidad (hexbin) facetados por cantón.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from limpieza_datos import cargar_datos
from utilidades import CMAP_SEC, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()

# 1) Concentración nacional en celdas de la cuadrícula (cada celda mide ~2 km)
seccion("1) Concentración de siniestros en celdas de ~2 km")
celdas = sin.groupby(["celda_lat", "celda_lon"]).agg(siniestros=("sid", "size"), fallecidos=("fallecidos", "sum"),
                                                      canton=("canton", lambda s: s.mode().iat[0])).sort_values("siniestros", ascending=False)
celdas["% acumulado"] = 100 * celdas["siniestros"].cumsum() / celdas["siniestros"].sum()
print(f"Celdas con al menos un siniestro: {len(celdas)}")
for pct in [1, 5, 10]:
    k = int(np.ceil(len(celdas) * pct / 100))
    print(f"El {pct}% de las celdas con más eventos ({k}) concentra {celdas['% acumulado'].iloc[k - 1]:.1f}% de los siniestros")
print("\nTop 10 celdas nacionales:")
mostrar(celdas.head(10))
guardar_tabla(celdas.head(50), "p04_top50_celdas")

# 2) Mapas de densidad en los 3 cantones con más siniestros (facetas)
seccion("2) Los 3 cantones con más siniestros")
top = sin["canton"].value_counts().head(3).index.tolist()
fig, ax = plt.subplots(1, 3, figsize=(17, 5.5))
filas = []
for a, cant in zip(ax, top):
    d = sin[sin["canton"] == cant]
    lo, hi = d[["lat", "lon"]].quantile(0.003), d[["lat", "lon"]].quantile(0.997)   # quita coordenadas muy lejanas
    d = d[d["lat"].between(lo["lat"], hi["lat"]) & d["lon"].between(lo["lon"], hi["lon"])]
    hb = a.hexbin(d["lon"], d["lat"], gridsize=25, cmap=CMAP_SEC, mincnt=1)
    f = d[d["fatal"]]
    a.scatter(f["lon"], f["lat"], s=16, color=PALETA[1], edgecolor="white", linewidth=0.5, label="Con fallecidos")
    a.set_title(f"{cant.title()} ({len(d)} siniestros)")
    a.set_xlabel("Longitud (°)")
    a.set_ylabel("Latitud (°)")
    a.legend(frameon=False, loc="lower right")
    plt.colorbar(hb, ax=a, label="Siniestros por celda")
    c = d.groupby(["celda_lat", "celda_lon"]).size().sort_values(ascending=False)
    filas.append({"canton": cant, "siniestros": len(d), "celdas con eventos": len(c),
                  "% en las 5 celdas principales": round(100 * c.head(5).sum() / c.sum(), 1)})
res = pd.DataFrame(filas).set_index("canton")
mostrar(res)
guardar_tabla(res, "p04_concentracion_por_canton")
guardar_fig(fig, "p04_densidad_facetado")

# 3) Mapa nacional por severidad
fig, ax = plt.subplots(figsize=(7, 8))
for sev, c, s_, a_ in [("SIN VÍCTIMAS", "#cfcec8", 2, 0.4), ("CON LESIONADOS", PALETA[0], 3, 0.5), ("FATAL", PALETA[1], 8, 0.9)]:
    d = sin[sin["severidad"] == sev]
    ax.scatter(d["lon"], d["lat"], s=s_, color=c, alpha=a_, label=f"{sev.capitalize()} ({len(d):,})")
ax.set_xlabel("Longitud (°)")
ax.set_ylabel("Latitud (°)")
ax.set_title("Siniestros 2026 por severidad")
ax.legend(frameon=False, markerscale=3)
ax.set_aspect("equal")
guardar_fig(fig, "p04_mapa_nacional_severidad")
