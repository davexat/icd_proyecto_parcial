"""
utilidades.py
=============
Funciones auxiliares compartidas por las preguntas: estilo de gráficos, guardado de
resultados, tabla de gravedad por grupo y clasificación Pareto ABC.
"""
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
