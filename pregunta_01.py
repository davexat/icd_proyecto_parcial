# PREGUNTA DE NEGOCIO 1
# ¿Existen patrones temporales (mes, día de la semana y hora) en la siniestralidad, y cambian
# entre zona urbana y rural? ¿Cuáles son los momentos de temporada alta y de horas pico?
#
# Técnicas: índices de estacionalidad (valor / promedio), prueba chi-cuadrado de uniformidad,
# Kruskal-Wallis sobre conteos diarios, heatmap día x hora y gráfico facetado por zona.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from limpieza_datos import cargar_datos, MESES, DIAS
from utilidades import CMAP_SEC, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
dias_cal = pd.Series(pd.date_range(sin["fecha"].min(), sin["fecha"].max()))   # días del periodo observado

# 1) Índices de estacionalidad: tasa por día calendario / promedio (>1 = temporada alta)
seccion("1) Índices de estacionalidad")
por_mes = sin.groupby("mes").size() / dias_cal.dt.month.value_counts().sort_index()
idx_mes = (por_mes / por_mes.mean()).rename(index=lambda m: MESES[m - 1])
por_dia = sin.groupby("dia_semana").size() / dias_cal.dt.day_of_week.add(1).value_counts().sort_index()
idx_dia = (por_dia / por_dia.mean()).rename(index=lambda d: DIAS[d - 1])
por_hora = sin.groupby("hora_num").size()
idx_hora = por_hora / por_hora.mean()
for nombre, idx in [("mes", idx_mes), ("día de la semana", idx_dia), ("hora", idx_hora)]:
    print(f"\nÍndice por {nombre}:")
    mostrar(idx.round(3).to_frame("índice"), 24)
guardar_tabla(pd.concat({"mes": idx_mes, "dia": idx_dia, "hora": idx_hora}).rename("indice").to_frame(), "p01_indices")

# 2) Pruebas estadísticas de que el patrón no es azar
seccion("2) Pruebas de uniformidad y diferencia entre días")
esperado_dia = dias_cal.dt.day_of_week.add(1).value_counts().sort_index()
chi_d = stats.chisquare(sin["dia_semana"].value_counts().sort_index(), esperado_dia / esperado_dia.sum() * len(sin))
chi_h = stats.chisquare(por_hora)
print(f"Chi-cuadrado día de la semana (esperado proporcional a días calendario): chi2={chi_d.statistic:.1f}, p={chi_d.pvalue:.2e}")
print(f"Chi-cuadrado hora (esperado uniforme): chi2={chi_h.statistic:.1f}, p={chi_h.pvalue:.2e}")
diario = sin.groupby("fecha").size().reindex(dias_cal, fill_value=0)
kw = stats.kruskal(*[g.values for _, g in diario.groupby(diario.index.day_of_week)])
mw = stats.mannwhitneyu(diario[diario.index.day_of_week >= 5], diario[diario.index.day_of_week < 5])
print(f"Kruskal-Wallis de siniestros/día entre días de la semana: H={kw.statistic:.1f}, p={kw.pvalue:.2e}")
print(f"Fin de semana vs laborable (Mann-Whitney): mediana {diario[diario.index.day_of_week >= 5].median():.0f} vs "
      f"{diario[diario.index.day_of_week < 5].median():.0f} siniestros/día, p={mw.pvalue:.2e}")
print("Horas pico (índice > 1.3):", [int(h) for h in idx_hora[idx_hora > 1.3].index])

# 3) Gráfico de índices (barras; naranja = temporada alta)
fig, ax = plt.subplots(1, 3, figsize=(15, 4), gridspec_kw={"width_ratios": [9, 7, 24]})
for a, idx, t, xl in [(ax[0], idx_mes, "Mes", "Mes (2026)"), (ax[1], idx_dia, "Día de la semana", "Día"),
                      (ax[2], idx_hora, "Hora del día", "Hora de ocurrencia (0-23 h)")]:
    a.bar(range(len(idx)), idx.values, color=[PALETA[1] if v > 1 else PALETA[0] for v in idx.values], width=0.75)
    a.axhline(1, color="#52514e", lw=1)
    a.set_xticks(range(len(idx)))
    a.set_xticklabels([str(i)[:3].title() if not isinstance(i, (int, np.integer)) else str(i) for i in idx.index],
                      rotation=0 if t == "Hora del día" else 45)
    a.set_title(f"Índice por {t.lower()}")
    a.set_xlabel(xl)
    a.set_ylabel("Índice (1 = promedio)")
guardar_fig(fig, "p01_indices_estacionalidad")

# 4) Heatmaps facetados por zona: siniestros promedio por día x hora
mat = {}
fig, ax = plt.subplots(1, 2, figsize=(15, 4.5), sharey=True)
vmax = 0
for z in ["URBANA", "RURAL"]:
    d = sin[sin["zona"] == z]
    m = d.pivot_table(index="dia_semana", columns="hora_num", values="sid", aggfunc="count", fill_value=0)
    m = m.div(esperado_dia, axis=0).reindex(columns=range(24), fill_value=0)   # promedio por día calendario
    mat[z] = m
    vmax = max(vmax, m.values.max())
for a, z in zip(ax, mat):
    sns.heatmap(mat[z], ax=a, cmap=CMAP_SEC, vmin=0, vmax=vmax, yticklabels=[d.title()[:3] for d in DIAS],
                cbar_kws={"label": "Siniestros por día calendario"})
    a.set_title(f"Zona {z.lower()}")
    a.set_xlabel("Hora de ocurrencia (0-23 h)")
    a.set_ylabel("Día de la semana")
guardar_fig(fig, "p01_heatmap_dia_hora_por_zona")
for z, m in mat.items():
    pico = m.stack().idxmax()
    print(f"Zona {z}: pico en {DIAS[pico[0] - 1]} a las {pico[1]} h ({m.stack().max():.2f} siniestros por día)")
