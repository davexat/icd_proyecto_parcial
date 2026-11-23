# PREGUNTA DE NEGOCIO 3
# ¿Qué provincias y cantones concentran la mayor parte de los siniestros y de las muertes, y el
# ranking cambia si se mide por volumen o por gravedad?
#
# Técnicas: clasificación Pareto ABC (80-15-5), concentración del Top 5, ranking por volumen y por
# gravedad, gráfico Pareto facetado y mapa de burbujas con latitud y longitud (Folium).
import folium
import pandas as pd
import matplotlib.pyplot as plt
from branca.colormap import LinearColormap

from limpieza_datos import cargar_datos
from utilidades import (PALETA, etiqueta_mapa, gravedad, guardar_fig, guardar_mapa, guardar_tabla, mapa_base, mostrar,
                        pareto_abc, seccion)

sin, _ = cargar_datos()

# 1) Pareto ABC por provincia y cantón, midiendo siniestros y fallecidos
seccion("1) Clasificación ABC (80-15-5)")
res = {}
for nivel in ["provincia", "canton"]:
    for medida, serie in [("siniestros", sin.groupby(nivel).size()), ("fallecidos", sin.groupby(nivel)["fallecidos"].sum())]:
        abc = pareto_abc(serie)
        res[(nivel, medida)] = abc
        n_a = (abc["clase"] == "A").sum()
        print(f"{nivel:9s} | {medida:10s} | {len(abc)} unidades | clase A: {n_a} ({100 * n_a / len(abc):.0f}% de las unidades) "
              f"= 80% | Top 5 = {abc['%'].head(5).sum():.1f}%")
    guardar_tabla(res[(nivel, "siniestros")], f"p03_abc_{nivel}_siniestros")
print("\nTop 10 provincias por siniestros:")
mostrar(res[("provincia", "siniestros")].round(1), 10)

# 2) Volumen vs gravedad por provincia (% de siniestros con fallecidos)
seccion("2) Volumen vs gravedad por provincia (provincias con 100 o más siniestros)")
prov = gravedad(sin, "provincia")
prov[["lat", "lon"]] = sin.groupby("provincia")[["lat", "lon"]].mean()
prov["rango por volumen"] = prov["siniestros"].rank(ascending=False)
prov["rango por gravedad"] = prov["% fatales"].rank(ascending=False)
mostrar(prov[prov["siniestros"] >= 100].sort_values("% fatales", ascending=False)[
    ["siniestros", "fallecidos", "% fatales", "rango por volumen", "rango por gravedad"]].round(1), 12)
guardar_tabla(prov, "p03_provincias")

# 3) Gráficos: Pareto facetado (siniestros | fallecidos) y mapa de burbujas
fig, ax = plt.subplots(1, 2, figsize=(14, 4.8))
for a, medida, c in zip(ax, ["siniestros", "fallecidos"], PALETA):
    abc = res[("provincia", medida)].head(12)
    a.bar(range(len(abc)), abc["%"], color=c)
    a.plot(range(len(abc)), abc["% acumulado"], color="#52514e", marker="o", ms=4)
    a.axhline(80, color=PALETA[3], ls="--", lw=1)
    a.set_ylim(0, 105)
    a.set_xticks(range(len(abc)))
    a.set_xticklabels([("Santo Domingo" if i.startswith("SANTO DOMINGO") else i.title()[:14]) for i in abc.index],
                      rotation=60, ha="right")
    a.set_ylabel(f"% del total de {medida} (barras) y acumulado (línea)")
    a.set_title(f"Pareto de provincias: {medida}")
guardar_fig(fig, "p03_pareto_provincias")

# Mapa de burbujas con Folium: una burbuja por provincia en su coordenada promedio
mapa = mapa_base(location=[-1.4, -78.6], zoom_start=7, control_scale=True)
escala = LinearColormap(["#cde2fb", "#6da7ec", "#256abf", "#0d366b"], vmin=prov["% fatales"].min(),
                        vmax=prov["% fatales"].max(), caption="% de siniestros con fallecidos")
# Rótulos permanentes: las 8 provincias con más siniestros y las 3 más graves que cita el guion
rotular = set(prov.nlargest(8, "siniestros").index) | {"ESMERALDAS", "ZAMORA CHINCHIPE", "CAÑAR"}
LADO = {"GUAYAS": "bottom", "SANTA ELENA": "left", "SANTO DOMINGO DE LOS TSACHILAS": "left", "PICHINCHA": "right",
        "CAÑAR": "left", "ZAMORA CHINCHIPE": "bottom", "LOJA": "left", "AZUAY": "right"}
for n, r in prov.iterrows():
    nombre = "Santo Domingo" if n.startswith("SANTO DOMINGO") else n.title()
    radio = max(3.0, r["siniestros"] ** 0.5 / 3.5)
    marca = folium.CircleMarker([r["lat"], r["lon"]], radius=radio, color="white", weight=1,
                                fill=True, fill_color=escala(r["% fatales"]), fill_opacity=0.85,
                                popup=folium.Popup(f"<b>{nombre}</b><br>Siniestros: {int(r['siniestros']):,}<br>"
                                                   f"Fallecidos: {int(r['fallecidos']):,}<br>"
                                                   f"% con fallecidos: {r['% fatales']:.1f}", max_width=220))
    if n in rotular:
        lado = LADO.get(n, "top")                  # el rótulo se corre un radio para no tapar la burbuja
        dx, dy = {"right": (radio + 4, 0), "left": (-radio - 4, 0), "top": (0, -radio - 4), "bottom": (0, radio + 4)}[lado]
        marca.add_child(folium.Tooltip(nombre, permanent=True, direction=lado, offset=(dx, dy),
                                       style="font-size:11px;padding:1px 4px;"))
    marca.add_to(mapa)
escala.add_to(mapa)
etiqueta_mapa(mapa, "<b>Siniestros por provincia</b><br>tamaño = volumen, color = % con fallecidos", abajo=True)
cont = sin[sin["lon"] > -85]                       # el encuadre es el continente; Galápagos (5 siniestros) queda fuera de vista
mapa.fit_bounds([[cont["lat"].min(), cont["lon"].min()], [cont["lat"].max(), cont["lon"].max()]])
guardar_mapa(mapa, "p03_mapa_burbujas_provincias", ancho=800, alto=900)
