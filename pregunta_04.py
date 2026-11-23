# PREGUNTA DE NEGOCIO 4
# ¿En qué provincias pesan más las motocicletas, los camiones y los buses en los siniestros, y esas
# provincias son las mismas donde hay más siniestros?
#
# Técnicas: porcentaje de siniestros que involucran cada tipo de vehículo por provincia, ranking por
# porcentaje y por cantidad, y mapas de burbujas con latitud y longitud, uno por vehículo (Folium).
import folium
import numpy as np
import pandas as pd
from branca.colormap import LinearColormap

from limpieza_datos import cargar_datos
from utilidades import etiqueta_mapa, guardar_facetas, guardar_tabla, mapa_base, mostrar, seccion

sin, _ = cargar_datos()
MINIMO = 100                                   # provincias con menos siniestros se omiten: su porcentaje es inestable
VEHICULOS = {"Motocicleta": "n_motocicleta", "Camión": "n_camion", "Bus": "n_bus"}

# 1) Por provincia: siniestros totales y siniestros que involucran cada vehículo
seccion("1) Porcentaje de siniestros que involucran cada vehículo, por provincia")
prov = sin.groupby("provincia").agg(siniestros=("sid", "size"), lat=("lat", "mean"), lon=("lon", "mean"))
nacional = {}
for nombre, col in VEHICULOS.items():
    con = sin[sin[col] > 0]
    prov[f"{nombre} (n)"] = con.groupby("provincia").size()
    prov[f"{nombre} (n)"] = prov[f"{nombre} (n)"].fillna(0).astype(int)
    prov[f"{nombre} (%)"] = 100 * prov[f"{nombre} (n)"] / prov["siniestros"]
    nacional[nombre] = 100 * len(con) / len(sin)
    print(f"{nombre}: {len(con):,} siniestros ({nacional[nombre]:.1f}% del total)")
prov = prov[prov["siniestros"] >= MINIMO]
print(f"\nProvincias con {MINIMO} o más siniestros: {len(prov)} de 24")
guardar_tabla(prov, "p04_vehiculos_por_provincia")

for nombre in VEHICULOS:
    print(f"\n{nombre}: provincias con mayor porcentaje (promedio nacional {nacional[nombre]:.1f}%)")
    mostrar(prov.sort_values(f"{nombre} (%)", ascending=False)[["siniestros", f"{nombre} (n)", f"{nombre} (%)"]].round(1), 5)
    top2 = prov[f"{nombre} (n)"].nlargest(2)
    print(f"Mayor cantidad: {', '.join(top2.index.str.title())} "
          f"({100 * top2.sum() / sin[sin[VEHICULOS[nombre]] > 0].shape[0]:.1f}% de los siniestros con {nombre.lower()})")

# 2) Un mapa por vehículo (facetas): tamaño = siniestros con ese vehículo, color = % de los siniestros de la provincia
seccion("2) Mapas de burbujas por vehículo")
LADO = {"GUAYAS": "bottom", "SANTA ELENA": "left", "SANTO DOMINGO DE LOS TSACHILAS": "left", "PICHINCHA": "right",
        "CAÑAR": "right", "LOS RIOS": "left", "MANABI": "left", "EL ORO": "left", "LOJA": "left", "COTOPAXI": "right",
        "TUNGURAHUA": "right", "CHIMBORAZO": "right", "AZUAY": "right", "ZAMORA CHINCHIPE": "bottom"}
cont = sin[sin["lon"] > -85]                    # encuadre del continente; Galápagos queda fuera de vista
facetas = []
for nombre in VEHICULOS:
    pct, cant = f"{nombre} (%)", f"{nombre} (n)"
    mapa = mapa_base(location=[-1.4, -78.6], zoom_start=7, zoom_snap=1)   # zoom entero: sin líneas entre teselas
    escala = LinearColormap(["#cde2fb", "#6da7ec", "#256abf", "#0d366b"], vmin=prov[pct].min(), vmax=prov[pct].max(),
                            caption=f"% de siniestros de la provincia con {nombre.lower()}")
    rotular = set(prov[pct].nlargest(3).index) | set(prov[cant].nlargest(2).index)    # las 3 de mayor porcentaje y las 2 de mayor cantidad
    for n, r in prov.iterrows():
        etiqueta = "Santo Domingo" if n.startswith("SANTO DOMINGO") else n.title()
        radio = max(4.0, r[cant] ** 0.5 / 2.2)
        marca = folium.CircleMarker([r["lat"], r["lon"]], radius=radio, color="white", weight=1, fill=True,
                                    fill_color=escala(r[pct]), fill_opacity=0.85,
                                    popup=folium.Popup(f"<b>{etiqueta}</b><br>Siniestros: {int(r['siniestros']):,}<br>"
                                                       f"Con {nombre.lower()}: {int(r[cant]):,} ({r[pct]:.1f} %)", max_width=220))
        if n in rotular:
            lado = LADO.get(n, "top")
            dx, dy = {"right": (radio + 4, 0), "left": (-radio - 4, 0), "top": (0, -radio - 4), "bottom": (0, radio + 4)}[lado]
            marca.add_child(folium.Tooltip(etiqueta, permanent=True, direction=lado, offset=(dx, dy),
                                           style="font-size:11px;padding:1px 4px;"))
        marca.add_to(mapa)
    escala.add_to(mapa)
    etiqueta_mapa(mapa, f"<b>{nombre}</b> (promedio nacional {nacional[nombre]:.0f} %)<br>tamaño = siniestros con {nombre.lower()}", abajo=True)
    mapa.fit_bounds([[cont["lat"].min(), cont["lon"].min()], [cont["lat"].max(), cont["lon"].max()]])
    facetas.append(mapa)
guardar_facetas(facetas, "p04_vehiculos_por_provincia", ancho=1800, alto=900)
