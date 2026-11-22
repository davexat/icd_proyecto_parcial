# PREGUNTA DE NEGOCIO 1
# ¿En qué meses, días de la semana y horas ocurren más siniestros, y ese patrón cambia entre
# zona urbana y rural?
#
# Técnicas: conteos, índices de estacionalidad (valor / promedio; mayor a 1 = temporada alta),
# gráfico de barras y heatmap día x hora facetado por zona.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import cargar_datos, MESES, DIAS
from utilidades import CMAP_SEC, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
dias_cal = pd.Series(pd.date_range(sin["fecha"].min(), sin["fecha"].max()))   # días del periodo observado

# 1) Índices de estacionalidad: siniestros por día calendario / promedio (> 1 = temporada alta)
seccion("1) Índices de estacionalidad")
por_mes = sin.groupby("mes").size() / dias_cal.dt.month.value_counts().sort_index()
idx_mes = (por_mes / por_mes.mean()).rename(index=lambda m: MESES[m - 1])
por_dia = sin.groupby("dia_semana").size() / dias_cal.dt.day_of_week.add(1).value_counts().sort_index()
idx_dia = (por_dia / por_dia.mean()).rename(index=lambda d: DIAS[d - 1])
por_hora = sin.groupby("hora_num").size()
idx_hora = por_hora / por_hora.mean()
for nombre, idx in [("mes", idx_mes), ("día de la semana", idx_dia), ("hora", idx_hora)]:
    print(f"\nÍndice por {nombre}:")
    mostrar(idx.round(2).to_frame("índice"), 24)
guardar_tabla(pd.concat({"mes": idx_mes, "dia": idx_dia, "hora": idx_hora}).rename("indice").to_frame(), "p01_indices")
print("\nHoras pico (índice > 1.3):", [int(h) for h in idx_hora[idx_hora > 1.3].index])

# 2) Gráfico de índices (naranja = temporada alta)
fig, ax = plt.subplots(1, 3, figsize=(15, 4), gridspec_kw={"width_ratios": [9, 7, 24]})
for a, idx, t, xl in [(ax[0], idx_mes, "mes", "Mes (2026)"), (ax[1], idx_dia, "día de la semana", "Día"),
                      (ax[2], idx_hora, "hora del día", "Hora de ocurrencia (0-23 h)")]:
    a.bar(range(len(idx)), idx.values, color=[PALETA[1] if v > 1 else PALETA[0] for v in idx.values], width=0.75)
    a.axhline(1, color="#52514e", lw=1)
    a.set_xticks(range(len(idx)))
    a.set_xticklabels([str(i)[:3].title() if not isinstance(i, (int, np.integer)) else str(i) for i in idx.index],
                      rotation=0 if t == "hora del día" else 45)
    a.set_title(f"Índice por {t}")
    a.set_xlabel(xl)
    a.set_ylabel("Índice (1 = promedio)")
guardar_fig(fig, "p01_indices_estacionalidad")

# 3) Heatmaps facetados por zona: siniestros promedio por día calendario, día x hora
seccion("3) Día x hora por zona")
dias_por_dow = dias_cal.dt.day_of_week.add(1).value_counts().sort_index()
mat = {}
for z in ["URBANA", "RURAL"]:
    m = sin[sin["zona"] == z].pivot_table(index="dia_semana", columns="hora_num", values="sid", aggfunc="count", fill_value=0)
    mat[z] = m.div(dias_por_dow, axis=0).reindex(columns=range(24), fill_value=0)
vmax = max(m.values.max() for m in mat.values())
fig, ax = plt.subplots(1, 2, figsize=(15, 4.5), sharey=True)
for a, z in zip(ax, mat):
    sns.heatmap(mat[z], ax=a, cmap=CMAP_SEC, vmin=0, vmax=vmax, yticklabels=[d.title()[:3] for d in DIAS],
                cbar_kws={"label": "Siniestros por día calendario"})
    a.set_title(f"Zona {z.lower()}")
    a.set_xlabel("Hora de ocurrencia (0-23 h)")
    a.set_ylabel("Día de la semana")
guardar_fig(fig, "p01_heatmap_dia_hora_por_zona")
for z, m in mat.items():
    pico = m.stack().idxmax()
    print(f"Zona {z}: pico el {DIAS[pico[0] - 1].lower()} a las {pico[1]} h ({m.stack().max():.2f} siniestros por día)")
