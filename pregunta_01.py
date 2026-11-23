# PREGUNTA DE NEGOCIO 1
# ¿En qué meses, días de la semana y horas ocurren más siniestros, y ese patrón cambia entre
# zona urbana y rural?
#
# Técnicas: índices de estacionalidad (valor / promedio; mayor a 1 = temporada alta) y
# gráficos de barras y líneas: uno general y uno por categoría (mes, día, hora) urbana vs rural.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from limpieza_datos import cargar_datos, MESES, DIAS
from utilidades import PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
dias_cal = pd.Series(pd.date_range(sin["fecha"].min(), sin["fecha"].max()))   # días del periodo observado
dias_por_mes = dias_cal.dt.month.value_counts().sort_index()
dias_por_dow = dias_cal.dt.day_of_week.add(1).value_counts().sort_index()


def indices(df):
    """Índice = siniestros por día calendario / promedio de la categoría (1 = promedio)."""
    por_mes = df.groupby("mes").size() / dias_por_mes
    por_dia = df.groupby("dia_semana").size() / dias_por_dow
    por_hora = df.groupby("hora_num").size().reindex(range(24), fill_value=0)
    return {"mes": (por_mes / por_mes.mean()).rename(index=lambda m: MESES[m - 1]),
            "día": (por_dia / por_dia.mean()).rename(index=lambda d: DIAS[d - 1]),
            "hora": por_hora / por_hora.mean()}


# 1) Índices generales y por zona
seccion("1) Índices de estacionalidad")
gen = indices(sin)
zonas = {"Urbana": indices(sin[sin["zona"] == "URBANA"]), "Rural": indices(sin[sin["zona"] == "RURAL"])}
for cat in ["mes", "día", "hora"]:
    tabla = pd.DataFrame({"General": gen[cat], **{z: zonas[z][cat] for z in zonas}})
    print(f"\nÍndice por {cat}:")
    mostrar(tabla.round(2), 24)
tablas = {cat: pd.DataFrame({"General": gen[cat], **{z: zonas[z][cat] for z in zonas}}) for cat in gen}
guardar_tabla(pd.concat(tablas, names=["categoria", "valor"]), "p01_indices")
print("\nHoras pico generales (índice > 1.3):", [int(h) for h in gen["hora"][gen["hora"] > 1.3].index])
for cat in ["mes", "día", "hora"]:
    for z, ind in zonas.items():
        print(f"{cat} | {z}: máximo {ind[cat].idxmax()} ({ind[cat].max():.2f}), mínimo {ind[cat].idxmin()} ({ind[cat].min():.2f})")

# 2) Imagen general: las tres categorías (naranja = temporada alta)
fig, ax = plt.subplots(1, 3, figsize=(15, 4), gridspec_kw={"width_ratios": [9, 7, 24]})
for a, cat, xl in [(ax[0], "mes", "Mes (2026)"), (ax[1], "día", "Día de la semana"), (ax[2], "hora", "Hora de ocurrencia (0-23 h)")]:
    idx = gen[cat]
    a.bar(range(len(idx)), idx.values, color=[PALETA[1] if v > 1 else PALETA[0] for v in idx.values], width=0.75)
    a.axhline(1, color="#52514e", lw=1)
    a.set_xticks(range(len(idx)))
    a.set_xticklabels([str(i)[:3].title() if cat != "hora" else str(i) for i in idx.index], rotation=0 if cat == "hora" else 45)
    a.set_title(f"Índice por {cat if cat != 'hora' else 'hora del día'}")
    a.set_xlabel(xl)
    a.set_ylabel("Índice (1 = promedio)")
guardar_fig(fig, "p01_indices_general")

# 3) Una imagen por categoría: urbana vs rural (cada zona contra su propio promedio)
seccion("3) Urbana vs rural")
COL = {"Urbana": PALETA[0], "Rural": PALETA[1]}
for cat, xl, nombre in [("mes", "Mes (2026)", "p01_indices_mes_zona"), ("día", "Día de la semana", "p01_indices_dia_zona"),
                        ("hora", "Hora de ocurrencia (0-23 h)", "p01_indices_hora_zona")]:
    fig, a = plt.subplots(figsize=(11 if cat == "hora" else 8, 4.2))
    n = len(gen[cat])
    x = np.arange(n)
    for k, (z, ind) in enumerate(zonas.items()):
        if cat == "hora":
            a.plot(x, ind[cat].values, color=COL[z], lw=2, marker="o", ms=4, label=z)
        else:
            a.bar(x + (k - 0.5) * 0.38, ind[cat].values, width=0.36, color=COL[z], label=z)
    a.axhline(1, color="#52514e", lw=1, ls="--")
    a.set_xticks(x)
    a.set_xticklabels([str(i)[:3].title() if cat != "hora" else str(i) for i in gen[cat].index])
    a.set_title(f"Índice por {cat if cat != 'hora' else 'hora del día'}: zona urbana vs rural")
    a.set_xlabel(xl)
    a.set_ylabel("Índice (1 = promedio de su zona)")
    a.legend(frameon=False, ncol=2, loc="upper left")
    guardar_fig(fig, nombre)
