"""
utilidades.py
=============
Funciones auxiliares compartidas por las preguntas: estilo de gráficos, guardado de
resultados (figuras, tablas y mapas de Folium), tabla de gravedad por grupo y clasificación Pareto ABC.
"""
import html
import shutil
import subprocess
import tempfile
from pathlib import Path

import folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

from limpieza_datos import DIR_RES

# Paleta categórica (orden fijo) y rampas: azul secuencial; divergente azul-gris-naranja
PALETA = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
GRIS = "#8a8a85"
CMAP_SEC = LinearSegmentedColormap.from_list("sec", ["#cde2fb", "#6da7ec", "#256abf", "#0d366b"])
CMAP_DIV = LinearSegmentedColormap.from_list("div", ["#2a78d6", "#f1f0ec", "#eb6834"])


def estilo():
    sns.set_theme(style="whitegrid", context="notebook", palette=PALETA)
    plt.rcParams.update({"figure.dpi": 110, "axes.titlesize": 12, "axes.titleweight": "bold",
                         "axes.labelsize": 10, "grid.color": "#e6e5e0", "grid.linewidth": 0.7,
                         "axes.spines.top": False, "axes.spines.right": False})


estilo()


def guardar_fig(fig, nombre):
    DIR_RES.mkdir(exist_ok=True)
    fig.tight_layout()
    ruta = DIR_RES / f"{nombre}.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[figura] {ruta.name}")


# Mapa base gris claro de Esri (no requiere clave de API); las capas de datos se ven mejor sobre él
TILES_GRIS = "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
ATRIB_GRIS = "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ"


def mapa_base(**kw):
    """Mapa de Folium con el fondo gris de Esri (sin entrada en el control de capas)."""
    kw.setdefault("zoom_snap", 0.25)
    m = folium.Map(tiles=None, **kw)
    folium.TileLayer(TILES_GRIS, attr=ATRIB_GRIS, name="Mapa base", control=False).add_to(m)
    return m


def etiqueta_mapa(m, html, abajo=False):
    """Cuadro de título del mapa, arriba a la izquierda (o abajo si la parte de arriba lleva una escala de color)."""
    pos = "bottom:45px;left:10px" if abajo else "top:10px;left:55px"
    m.get_root().html.add_child(folium.Element(
        f'<div style="position:fixed;{pos};z-index:9999;background:white;padding:5px 9px;'
        f'border-radius:4px;font:13px Arial;box-shadow:0 0 4px #888">{html}</div>'))


def _navegador():
    """Ruta de Edge o Chrome (para capturar el mapa en PNG), o None si no hay ninguno."""
    candidatos = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                  r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                  r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                  r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    for c in candidatos + [shutil.which(x) for x in ("msedge", "chrome", "google-chrome", "chromium")]:
        if c and Path(c).exists():
            return c
    return None


def guardar_mapa(mapa, nombre, ancho=900, alto=900):
    """Guarda un mapa de Folium como HTML interactivo y, si hay Edge o Chrome, también como PNG.
    Necesita internet: el HTML carga Leaflet y las teselas del mapa base desde la red."""
    DIR_RES.mkdir(exist_ok=True)
    ruta_html = DIR_RES / f"{nombre}.html"
    if isinstance(mapa, str):                 # página HTML ya armada (facetas)
        ruta_html.write_text(mapa, encoding="utf-8")
    else:
        mapa.save(str(ruta_html))
    print(f"[mapa]   {ruta_html.name}")
    nav = _navegador()
    if nav is None:
        print(f"[aviso]  No se encontró Edge ni Chrome: no se creó {nombre}.png (abre el HTML y toma una captura).")
        return
    ruta_png = DIR_RES / f"{nombre}.png"
    ruta_png.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as perfil:
        try:
            subprocess.run([nav, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={perfil}",
                            f"--window-size={ancho},{alto}", "--force-device-scale-factor=2", "--virtual-time-budget=25000",
                            f"--screenshot={ruta_png}", ruta_html.as_uri()],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
        except subprocess.TimeoutExpired:
            pass
    print(f"[figura] {ruta_png.name}" if ruta_png.exists() else f"[aviso]  No se pudo crear {ruta_png.name}")


def guardar_facetas(mapas, nombre, ancho, alto):
    """Une varios mapas de Folium en una sola página (una faceta por mapa, lado a lado) y la guarda como HTML y PNG."""
    celdas = "".join(f'<iframe srcdoc="{html.escape(m.get_root().render(), quote=True)}"></iframe>' for m in mapas)
    pagina = ("<!DOCTYPE html><html><head><meta charset='utf-8'><style>html,body{margin:0;height:100%}"
              "body{display:flex;gap:6px;background:#fff}iframe{flex:1;border:0;height:100%}</style></head>"
              f"<body>{celdas}</body></html>")
    guardar_mapa(pagina, nombre, ancho, alto)


def guardar_tabla(df, nombre, indice=True):
    DIR_RES.mkdir(exist_ok=True)
    ruta = DIR_RES / f"{nombre}.csv"
    df.to_csv(ruta, index=indice, encoding="utf-8-sig")
    print(f"[tabla]  {ruta.name}")


def seccion(texto):
    print("\n" + "=" * 90 + f"\n{texto}\n" + "=" * 90)


def mostrar(df, n=15, **kw):
    with pd.option_context("display.width", 200, "display.max_columns", 30, "display.max_colwidth", 60,
                           "display.float_format", lambda x: f"{x:,.2f}"):
        print(df.head(n).to_string(**kw))


def gravedad(df, por, minimo=0):
    """Tabla de gravedad por grupo: siniestros, con fallecidos (% fatales), fallecidos, lesionados y víctimas por siniestro."""
    g = df.groupby(por, observed=True).agg(siniestros=("sid", "size"), fatales=("fatal", "sum"),
                                          fallecidos=("fallecidos", "sum"), lesionados=("lesionados", "sum"))
    g["% fatales"] = 100 * g["fatales"] / g["siniestros"]
    g["víctimas por siniestro"] = (g["fallecidos"] + g["lesionados"]) / g["siniestros"]
    return g[g["siniestros"] >= minimo]


def pareto_abc(serie, cortes=(0.80, 0.95)):
    """Clasificación ABC (80-15-5) de una serie de valores por categoría."""
    d = serie.sort_values(ascending=False).to_frame("valor")
    d["%"] = 100 * d["valor"] / d["valor"].sum()
    d["% acumulado"] = d["%"].cumsum()
    previo = d["% acumulado"] - d["%"]          # acumulado antes de sumar la categoría
    d["clase"] = np.where(previo < 100 * cortes[0], "A", np.where(previo < 100 * cortes[1], "B", "C"))
    return d
