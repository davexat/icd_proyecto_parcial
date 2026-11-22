# PREGUNTA DE NEGOCIO 2
# ¿Los feriados y los fines de semana cambian cuántos siniestros ocurren, a qué hora ocurren y
# qué tan graves son, frente a un día laborable?
#
# Técnicas: promedio diario por tipo de día, razón contra el día laborable, porcentaje de
# siniestros con fallecidos, perfil horario facetado por tipo de día y serie diaria con media móvil.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from limpieza_datos import cargar_datos
from utilidades import PALETA, gravedad, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
orden = ["LABORABLE", "FIN DE SEMANA", "FERIADO"]
dias = pd.date_range(sin["fecha"].min(), sin["fecha"].max())
diario = pd.DataFrame({"siniestros": sin.groupby("fecha").size(), "fallecidos": sin.groupby("fecha")["fallecidos"].sum()}
                      ).reindex(dias, fill_value=0)
diario["feriado"] = diario.index.isin(sin.loc[sin["feriado"], "fecha"].unique())
diario["tipo_dia"] = np.select([diario["feriado"], diario.index.day_of_week >= 5], ["FERIADO", "FIN DE SEMANA"], "LABORABLE")

# 1) Volumen: promedio de siniestros y fallecidos por día según tipo de día
seccion("1) Promedio diario por tipo de día")
vol = diario.groupby("tipo_dia").agg(dias=("siniestros", "size"), siniestros_dia=("siniestros", "mean"),
                                     fallecidos_dia=("fallecidos", "mean")).loc[orden]
vol["razón vs laborable"] = vol["siniestros_dia"] / vol.loc["LABORABLE", "siniestros_dia"]
mostrar(vol.round(2))
guardar_tabla(vol, "p02_volumen_por_tipo_dia")

# 2) Gravedad: % de siniestros con fallecidos
seccion("2) Gravedad por tipo de día")
grav = gravedad(sin, "tipo_dia").loc[orden]
mostrar(grav.round(2))
guardar_tabla(grav, "p02_gravedad_por_tipo_dia")

# 3) Gráfico facetado: perfil horario (% del total de cada tipo de día) y % de siniestros fatales
fig, ax = plt.subplots(1, 4, figsize=(17, 3.8), gridspec_kw={"width_ratios": [1, 1, 1, 0.9]})
hora = pd.crosstab(sin["tipo_dia"], sin["hora_num"], normalize="index").loc[orden] * 100
for a, t, c in zip(ax[:3], orden, PALETA):
    a.bar(hora.columns, hora.loc[t], color=c)
    a.set_title(t.capitalize())
    a.set_xlabel("Hora (0-23 h)")
    a.set_ylabel("% de siniestros del grupo")
    a.set_ylim(0, hora.values.max() * 1.1)
ax[3].bar(range(3), grav["% fatales"], color=PALETA[:3])
ax[3].set_xticks(range(3))
ax[3].set_xticklabels([t.capitalize() for t in orden], rotation=20)
ax[3].set_ylabel("% de siniestros con fallecidos")
ax[3].set_title("Gravedad")
guardar_fig(fig, "p02_perfil_horario_y_gravedad")

# 4) Serie diaria con feriados resaltados
fig, ax = plt.subplots(figsize=(14, 3.8))
ax.plot(diario.index, diario["siniestros"], color=PALETA[0], lw=1.2, label="Siniestros por día")
ax.plot(diario.index, diario["siniestros"].rolling(7, center=True).mean(), color="#52514e", lw=2, label="Promedio móvil 7 días")
for d in diario.index[diario["feriado"]]:
    ax.axvspan(d - pd.Timedelta(hours=12), d + pd.Timedelta(hours=12), color=PALETA[1], alpha=0.35, lw=0)
ax.plot([], [], color=PALETA[1], lw=6, alpha=0.5, label="Feriado")
ax.set_xlabel("Fecha (2026)")
ax.set_ylabel("Siniestros por día")
ax.legend(frameon=False, ncol=3)
guardar_fig(fig, "p02_serie_diaria_feriados")
