# PREGUNTA DE NEGOCIO 4
# ¿Dónde están los puntos calientes (hotspots) de siniestros dentro de las ciudades con más
# eventos, y coinciden con los puntos donde ocurren las muertes?
#
# Técnicas: cuadrícula de ~2 km, estadístico local Getis-Ord Gi* (z > 2.58 = hotspot al 99%),
# densidad kernel (KDE), índice de Jaccard entre hotspots de siniestros y de fallecidos,
# concentración de eventos en pocas celdas y mapas facetados por cantón.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.ndimage import uniform_filter

from limpieza_datos import cargar_datos
from utilidades import CMAP_SEC, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
PASO = 0.02                                   # grados (~2.2 km)

# 1) Concentración nacional en celdas de la cuadrícula
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


def gi_star(puntos, lat0, lat1, lon0, lon1):
    """Gi* con vecindad 3x3 (pesos 1) sobre la cuadrícula del cantón. Devuelve matriz de z-scores."""
    ny, nx = int(round((lat1 - lat0) / PASO)) + 3, int(round((lon1 - lon0) / PASO)) + 3
    iy = ((puntos["lat"] - lat0) / PASO).round().astype(int) + 1
    ix = ((puntos["lon"] - lon0) / PASO).round().astype(int) + 1
    x = np.zeros((ny, nx))
    np.add.at(x, (iy.values, ix.values), puntos["peso"].values)
    n, xb, s = x.size, x.mean(), x.std()
    suma_vec = uniform_filter(x, size=3, mode="constant") * 9           # suma 3x3
    w = 9
    z = (suma_vec - xb * w) / (s * np.sqrt((n * w - w ** 2) / (n - 1)))
    return z, (lat0 - PASO, lon0 - PASO)


# 2) Hotspots en los 3 cantones con más siniestros: siniestros (peso 1) y fallecidos (peso = fallecidos)
seccion("2) Hotspots Gi* en los 3 cantones con más siniestros")
top = sin["canton"].value_counts().head(3).index.tolist()
fig, ax = plt.subplots(2, 3, figsize=(17, 10))
filas = []
for j, cant in enumerate(top):
    d = sin[sin["canton"] == cant].copy()
    # recorta extremos (coordenadas lejanas del centro) para que el mapa sea legible
    lo, hi = d[["lat", "lon"]].quantile(0.003), d[["lat", "lon"]].quantile(0.997)
    d = d[d["lat"].between(lo["lat"], hi["lat"]) & d["lon"].between(lo["lon"], hi["lon"])]
    lat0, lat1, lon0, lon1 = d["lat"].min(), d["lat"].max(), d["lon"].min(), d["lon"].max()
    resultados = {}
    for medida in ["siniestros", "fallecidos"]:
        d["peso"] = 1 if medida == "siniestros" else d["fallecidos"]
        z, (la, lo_) = gi_star(d, lat0, lat1, lon0, lon1)
        resultados[medida] = (z, la, lo_)
    zs, zf = resultados["siniestros"][0], resultados["fallecidos"][0]
    hs, hf = zs > 2.58, zf > 2.58
    jac = (hs & hf).sum() / max((hs | hf).sum(), 1)
    filas.append({"canton": cant, "siniestros": len(d), "celdas_hotspot_siniestros": int(hs.sum()),
                  "celdas_hotspot_fallecidos": int(hf.sum()), "jaccard": round(jac, 2)})
    # panel superior: KDE + puntos; panel inferior: mapa Gi* de siniestros con fallecidos encima
    kde = stats.gaussian_kde(d[["lon", "lat"]].T.values)
    gx, gy = np.meshgrid(np.linspace(lon0, lon1, 120), np.linspace(lat0, lat1, 120))
    dens = kde(np.vstack([gx.ravel(), gy.ravel()])).reshape(gx.shape)
    ax[0, j].contourf(gx, gy, dens, levels=10, cmap=CMAP_SEC)
    ax[0, j].scatter(d["lon"], d["lat"], s=2, color="white", alpha=0.5)
    ax[0, j].set_title(f"{cant.title()}: densidad kernel ({len(d)} siniestros)")
    z, la, lo_ = resultados["siniestros"]
    ext = [lo_ - PASO / 2, lo_ + (z.shape[1] - 0.5) * PASO, la - PASO / 2, la + (z.shape[0] - 0.5) * PASO]
    im = ax[1, j].imshow(np.where(z > 2.58, z, np.nan), origin="lower", extent=ext, cmap="Oranges", vmin=2.58, aspect="auto")
    ax[1, j].scatter(d["lon"], d["lat"], s=2, color="#b8b7b0", alpha=0.6, label="Siniestros")
    f = d[d["fallecidos"] > 0]
    ax[1, j].scatter(f["lon"], f["lat"], s=18, color=PALETA[0], edgecolor="white", linewidth=0.5, label="Con fallecidos")
    ax[1, j].set_title(f"{cant.title()}: hotspots Gi* (Jaccard = {jac:.2f})")
    for a in (ax[0, j], ax[1, j]):
        a.set_xlabel("Longitud (°)")
        a.set_ylabel("Latitud (°)")
    ax[1, j].legend(frameon=False, loc="lower right")
    # % de siniestros del cantón que caen en celdas hotspot
    iy = ((d["lat"] - lat0) / PASO).round().astype(int) + 1
    ix = ((d["lon"] - lon0) / PASO).round().astype(int) + 1
    filas[-1]["%_siniestros_en_hotspots"] = round(100 * hs[iy.values, ix.values].mean(), 1)
res = pd.DataFrame(filas).set_index("canton")
mostrar(res)
guardar_tabla(res, "p04_hotspots_por_canton")
guardar_fig(fig, "p04_hotspots_facetado")

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
