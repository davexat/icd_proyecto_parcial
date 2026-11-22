# PREGUNTA DE NEGOCIO 4
# ¿Dónde están los puntos críticos (zonas pequeñas con muchos siniestros) en el país y en las
# ciudades con más eventos, y coinciden con los lugares donde ocurren las muertes?
#
# Técnicas: cuadrícula de ~2 km (agrupar por coordenadas), concentración en pocas celdas,
# ranking de celdas, mapa de severidad y mapas de celdas facetados por cantón (mapas con Folium).
import folium
import numpy as np
import pandas as pd
from branca.colormap import LinearColormap

from limpieza_datos import cargar_datos
from utilidades import PALETA, etiqueta_mapa, guardar_facetas, guardar_mapa, guardar_tabla, mapa_base, mostrar, seccion

sin, _ = cargar_datos()

# 1) Concentración nacional en celdas de la cuadrícula (cada celda mide ~2 km)
seccion("1) Concentración de siniestros en celdas de ~2 km")
celdas = sin.groupby(["celda_lat", "celda_lon"]).agg(siniestros=("sid", "size"), fallecidos=("fallecidos", "sum"),
                                                      canton=("canton", lambda s: s.mode().iat[0])).sort_values("siniestros", ascending=False)
celdas["% acumulado"] = 100 * celdas["siniestros"].cumsum() / celdas["siniestros"].sum()
print(f"Celdas con al menos un siniestro: {len(celdas)}")
for pct in [1, 5, 10]:
    k = int(np.ceil(len(celdas) * pct / 100))
    print(f"El {pct}% de las celdas con más eventos ({k}) concentra {celdas['% acumulado'].iloc[k - 1]:.1f}% de los siniestros "
          f"y {100 * celdas['fallecidos'].iloc[:k].sum() / celdas['fallecidos'].sum():.1f}% de los fallecidos")
print("\nTop 10 celdas nacionales:")
mostrar(celdas.head(10))
guardar_tabla(celdas.head(50), "p04_top50_celdas")

# 2) Mapas de las celdas de ~2 km en los 3 cantones con más siniestros (una faceta por cantón, con Folium)
seccion("2) Los 3 cantones con más siniestros")
top = sin["canton"].value_counts().head(3).index.tolist()
RAD = 0.01                                    # media celda: cada celda mide 0.02 grados
AZULES = ["#cde2fb", "#6da7ec", "#256abf", "#0d366b"]
facetas = []
filas = []
for cant in top:
    d = sin[sin["canton"] == cant]
    lo, hi = d[["lat", "lon"]].quantile(0.003), d[["lat", "lon"]].quantile(0.997)   # quita coordenadas muy lejanas
    d = d[d["lat"].between(lo["lat"], hi["lat"]) & d["lon"].between(lo["lon"], hi["lon"])]
    c = d.groupby(["celda_lat", "celda_lon"]).size().sort_values(ascending=False)
    filas.append({"canton": cant, "siniestros": len(d), "celdas con eventos": len(c), "celda máxima": int(c.iloc[0]),
                  "% en las 5 celdas principales": round(100 * c.head(5).sum() / c.sum(), 1)})
    mapa = mapa_base(location=[d["lat"].mean(), d["lon"].mean()])
    escala = LinearColormap(AZULES, vmin=1, vmax=c.max(), caption="Siniestros por celda de ~2 km")
    for (la, lo_), n in c.items():            # cada celda se pinta según su número de siniestros
        folium.Rectangle([[la - RAD, lo_ - RAD], [la + RAD, lo_ + RAD]], color="white", weight=0.5, fill=True,
                         fill_color=escala(n), fill_opacity=0.8, tooltip=f"{n} siniestros").add_to(mapa)
    for _, r in d[d["fatal"]].iterrows():     # siniestros con fallecidos encima de las celdas
        folium.CircleMarker([r["lat"], r["lon"]], radius=3, color="white", weight=0.6, fill=True,
                            fill_color=PALETA[1], fill_opacity=1).add_to(mapa)
    escala.add_to(mapa)
    etiqueta_mapa(mapa, f'<b>{cant.title()}</b> ({len(d):,} siniestros)<br><span style="color:{PALETA[1]}">&#9679;</span> con fallecidos', abajo=True)
    mapa.fit_bounds([[d["lat"].min(), d["lon"].min()], [d["lat"].max(), d["lon"].max()]])
    facetas.append(mapa)
res = pd.DataFrame(filas).set_index("canton")
mostrar(res)
guardar_tabla(res, "p04_concentracion_por_canton")
guardar_facetas(facetas, "p04_densidad_facetado", ancho=1800, alto=620)

# 3) Mapa nacional por severidad (tres capas, los fatales más grandes y opacos)
seccion("3) Mapa nacional por severidad")
mapa = mapa_base(location=[-1.6, -78.5], zoom_start=7, prefer_canvas=True)
for sev, color, radio, op in [("SIN VÍCTIMAS", "#9a9992", 1.5, 0.5), ("CON LESIONADOS", PALETA[0], 2, 0.6), ("FATAL", PALETA[1], 2.2, 0.95)]:
    d = sin[sin["severidad"] == sev]
    puntos = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [round(lon, 5), round(lat, 5)]}, "properties": {}}
        for lat, lon in zip(d["lat"], d["lon"])]}
    folium.GeoJson(puntos, name=f"{sev.capitalize()} ({len(d):,})",
                   marker=folium.CircleMarker(radius=radio, weight=0, fill=True, fill_color=color, fill_opacity=op),
                   style_function=lambda f, c=color, o=op: {"fillColor": c, "fillOpacity": o, "color": c, "weight": 0}).add_to(mapa)
folium.LayerControl(collapsed=False).add_to(mapa)
etiqueta_mapa(mapa, "<b>Siniestros 2026 por severidad</b>")
cont = sin[sin["lon"] > -85]                  # encuadre del continente; Galápagos queda fuera de vista
mapa.fit_bounds([[cont["lat"].min(), cont["lon"].min()], [cont["lat"].max(), cont["lon"].max()]])
guardar_mapa(mapa, "p04_mapa_nacional_severidad", ancho=800, alto=950)
