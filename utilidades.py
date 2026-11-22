"""
utilidades.py
=============
Funciones auxiliares compartidas por las preguntas: estilo de gráficos, guardado de
resultados y pequeñas utilidades estadísticas (intervalos, odds ratio, Pareto, Gini).
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

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


# ------------------------------ estadística ------------------------------
def wilson(k, n, z=1.96):
    """Intervalo de Wilson (%) para una proporción k/n."""
    k, n = np.asarray(k, float), np.asarray(n, float)
    p = np.divide(k, n, out=np.zeros_like(k), where=n > 0)
    den = 1 + z ** 2 / np.where(n > 0, n, 1)
    centro = (p + z ** 2 / (2 * np.where(n > 0, n, 1))) / den
    mitad = z * np.sqrt(p * (1 - p) / np.where(n > 0, n, 1) + z ** 2 / (4 * np.where(n > 0, n, 1) ** 2)) / den
    return 100 * (centro - mitad), 100 * (centro + mitad)


def odds_ratio(a, b, c, d):
    """OR de la tabla [[a, b], [c, d]] (a/b = expuestos con/sin evento; c/d = no expuestos). IC 95% de Woolf y p de Fisher."""
    a, b, c, d = [x + 0.5 if min(a, b, c, d) == 0 else x for x in (a, b, c, d)]
    orr = (a * d) / (b * c)
    se = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    p = stats.fisher_exact([[a, b], [c, d]])[1] if max(a, b, c, d) < 5e4 else stats.chi2_contingency([[a, b], [c, d]])[1]
    return orr, np.exp(np.log(orr) - 1.96 * se), np.exp(np.log(orr) + 1.96 * se), p


def riesgo_relativo(a, n1, c, n0):
    """RR de a/n1 (expuestos) frente a c/n0 (no expuestos) con IC 95% (log)."""
    rr = (a / n1) / (c / n0)
    se = np.sqrt(1 / a - 1 / n1 + 1 / c - 1 / n0)
    return rr, np.exp(np.log(rr) - 1.96 * se), np.exp(np.log(rr) + 1.96 * se)


def cramers_v(tabla):
    chi2, p, _, _ = stats.chi2_contingency(tabla)
    n = np.asarray(tabla).sum()
    k = min(np.asarray(tabla).shape) - 1
    return chi2, p, float(np.sqrt(chi2 / (n * k)))


def pareto_abc(serie, cortes=(0.80, 0.95)):
    """Clasificación ABC (80-15-5) de una serie de valores por categoría."""
    d = serie.sort_values(ascending=False).to_frame("valor")
    d["%"] = 100 * d["valor"] / d["valor"].sum()
    d["% acumulado"] = d["%"].cumsum()
    previo = d["% acumulado"] - d["%"]          # acumulado antes de sumar la categoría
    d["clase"] = np.where(previo < 100 * cortes[0], "A", np.where(previo < 100 * cortes[1], "B", "C"))
    return d


def gini(x):
    x = np.sort(np.asarray(x, float))
    n = len(x)
    return float((2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum()))


def lorenz(x):
    x = np.sort(np.asarray(x, float))
    return np.insert(np.cumsum(x) / x.sum(), 0, 0), np.linspace(0, 1, len(x) + 1)
