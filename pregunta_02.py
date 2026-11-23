# PREGUNTA DE NEGOCIO 2
# ¿Qué días tuvieron muchos más siniestros o fallecidos de lo habitual y qué tienen en común
# (día de la semana, feriado, mes, causa dominante)?
#
# Técnicas: valores estandarizados (z-score) de la serie diaria, como en el Ejemplo 1; correlación
# entre siniestros y fallecidos; comparación de los días críticos con el total de días (día de la
# semana, mes, feriado y causa dominante) en gráficos facetados.
import pandas as pd
import matplotlib.pyplot as plt

from limpieza_datos import DIAS, cargar_datos
from utilidades import GRIS, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
dias = pd.date_range(sin["fecha"].min(), sin["fecha"].max())
d = pd.DataFrame({"siniestros": sin.groupby("fecha").size(), "fallecidos": sin.groupby("fecha")["fallecidos"].sum()}
                 ).reindex(dias, fill_value=0)
d["dow"] = d.index.day_of_week
d["fin_semana"] = d["dow"] >= 5
d["feriado"] = d.index.isin(sin.loc[sin["feriado"], "fecha"].unique())

# 1) Estandarización: cada día se compara contra el promedio de su mismo día de la semana,
#    para no marcar como "crítico" cada domingo solo por ser domingo.
#    z = cuántas desviaciones estándar está un día por encima (o por debajo) de lo habitual; 0 = día normal.
seccion("1) Serie diaria estandarizada (z-score)")
for c in ["siniestros", "fallecidos"]:
    d[f"z_{c}"] = (d[c] - d.groupby("dow")[c].transform("mean")) / d.groupby("dow")[c].transform("std")
print(f"Correlación entre siniestros y fallecidos por día: {d['siniestros'].corr(d['fallecidos']):.2f}")
print(f"Días con z > 2: siniestros {int((d['z_siniestros'] > 2).sum())} | fallecidos {int((d['z_fallecidos'] > 2).sum())}")

# 2) Días críticos y sus características
seccion("2) Días críticos (z > 2 en siniestros o fallecidos)")
d["critico"] = (d["z_siniestros"] > 2) | (d["z_fallecidos"] > 2)
cr = d[d["critico"]].copy()
cr["causa_dominante"] = sin.groupby("fecha")["causa_grupo"].agg(lambda s: s.value_counts().index[0]).reindex(cr.index)
cr["dia"] = [DIAS[i].title() for i in cr["dow"]]
cols = ["dia", "siniestros", "fallecidos", "z_siniestros", "z_fallecidos", "feriado", "causa_dominante"]
mostrar(cr[cols].round(2), 40)
guardar_tabla(cr[cols], "p02_dias_criticos")
print(f"\n{len(cr)} días críticos de {len(d)} ({100 * len(cr) / len(d):.1f}%)")
for var in ["fin_semana", "feriado"]:
    print(f"% de días críticos entre los días '{var}': {100 * d.loc[d[var], 'critico'].mean():.1f}% | resto: {100 * d.loc[~d[var], 'critico'].mean():.1f}%")
print("Críticos por mes:", cr.groupby(cr.index.month).size().to_dict())

# Composición de causas en días críticos frente al resto
comp = pd.concat([sin[sin["fecha"].isin(cr.index)]["causa_grupo"].value_counts(normalize=True).rename("críticos"),
                  sin[~sin["fecha"].isin(cr.index)]["causa_grupo"].value_counts(normalize=True).rename("resto")], axis=1) * 100
comp["diferencia (pp)"] = comp["críticos"] - comp["resto"]
mostrar(comp.sort_values("diferencia (pp)", ascending=False).round(1))

# 3) Gráfico 1: cuántas desviaciones sobre lo habitual tuvo cada día (los críticos pasan de 2)
MESES_ABR = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep"]
fig, ax = plt.subplots(2, 1, figsize=(14, 7.5), sharex=True)
for a, c, titulo in zip(ax, ["siniestros", "fallecidos"], ["Siniestros por día", "Fallecidos por día"]):
    z = d[f"z_{c}"]
    crit = d[z > 2]
    a.scatter(d.index[z <= 2], z[z <= 2], color=GRIS, s=14, alpha=0.6, label="Día normal")
    a.scatter(crit.index, z[z > 2], color="#e34948", s=34, zorder=3, label=f"Día crítico ({len(crit)})")
    # Rótulos en una fila arriba, separados lo justo para no montarse, con una línea guía hacia cada punto
    fechas = list(crit.index)
    xs = [f.toordinal() for f in fechas]
    sep, tope = 12, d.index[-1].toordinal() + 2
    for i in range(1, len(xs)):
        xs[i] = max(xs[i], xs[i - 1] + sep)
    xs[-1] = min(xs[-1], tope)
    for i in range(len(xs) - 2, -1, -1):
        xs[i] = min(xs[i], xs[i + 1] - sep)
    for fecha, x in zip(fechas, xs):
        a.annotate(f"{fecha.day} {MESES_ABR[fecha.month - 1]}", (fecha, z[fecha]), xytext=(pd.Timestamp.fromordinal(x), 6.4),
                   textcoords="data", ha="center", va="bottom", fontsize=8,
                   arrowprops=dict(arrowstyle="-", color="#9a9994", lw=0.7, shrinkA=1, shrinkB=3))
    a.axhline(2, color="#52514e", ls="--", lw=1)
    a.text(d.index[10], 2.1, "Límite: 2 desviaciones", ha="left", va="bottom", fontsize=8, color="#52514e")
    a.axhline(0, color="#c9c8c3", lw=0.8)
    a.set_ylim(-3, 7.6)
    a.set_ylabel("Desviaciones sobre lo habitual\n(0 = día normal)")
    a.set_title(titulo, loc="left")
    a.legend(frameon=False, loc="lower right", bbox_to_anchor=(1, 1.0), ncol=2)
ax[1].set_xlabel("Fecha (2026)")
guardar_fig(fig, "p02_dias_criticos_z")

# 4) Gráfico 2: ¿en qué se parecen los días críticos? Cada grupo de barras compara los días críticos con TODOS los días.
seccion("3) Qué tienen en común los días críticos (% de los críticos vs % de todos los días)")
causa4 = {"Distracción al conducir": "Distracción", "Exceso de velocidad": "Velocidad",
          "Irrespeto de señales / prioridad": "Señales"}
d["causa_dominante"] = sin.groupby("fecha")["causa_grupo"].agg(lambda s: s.value_counts().index[0]).reindex(d.index)
d["causa4"] = d["causa_dominante"].map(causa4).fillna("Otras")
d["mes"] = d.index.month
d["tipo_dia"] = d["feriado"].map({True: "Feriado", False: "No feriado"})
paneles = [("Día de la semana", d["dow"].map(lambda i: DIAS[i][:3].title()), [x[:3].title() for x in DIAS]),
           ("Mes", d["mes"].map(lambda m: MESES_ABR[m - 1].title()), [m.title() for m in MESES_ABR]),
           ("Feriado", d["tipo_dia"], ["Feriado", "No feriado"]),
           ("Causa dominante del día", d["causa4"], ["Distracción", "Velocidad", "Señales", "Otras"])]
fig, ax = plt.subplots(2, 2, figsize=(14, 7.5))
for a, (titulo, serie, orden) in zip(ax.ravel(), paneles):
    todos = 100 * serie.value_counts(normalize=True).reindex(orden).fillna(0)
    crit_ = 100 * serie[d["critico"]].value_counts(normalize=True).reindex(orden).fillna(0)
    print(f"\n{titulo}:")
    mostrar(pd.DataFrame({"% críticos": crit_, "% todos los días": todos}).round(1))
    x = range(len(orden))
    a.bar([i - 0.2 for i in x], todos, 0.4, color=GRIS, label=f"Todos los días ({len(d)})")
    b = a.bar([i + 0.2 for i in x], crit_, 0.4, color=PALETA[1], label=f"Días críticos ({len(cr)})")
    a.bar_label(b, fmt="%.0f", fontsize=8, padding=2)
    a.set_xticks(list(x))
    a.set_xticklabels(orden)
    a.set_ylabel("% de los días del grupo")
    a.set_title(titulo)
ax[1, 0].legend(frameon=False, loc="upper left")
guardar_fig(fig, "p02_que_tienen_en_comun")
