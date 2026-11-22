# PREGUNTA DE NEGOCIO 10
# ¿Qué días presentan niveles anómalos de siniestros o de fallecidos y qué características
# (día de la semana, feriado, mes, causa dominante) comparten esos días críticos?
#
# Técnicas: valores estandarizados (z-score) y z robusto (mediana/MAD) de la serie diaria,
# autocorrelación semanal, correlación de Spearman siniestros-fallecidos, prueba exacta de Fisher
# para las características de los días críticos y calendario heatmap (semana x día).
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from limpieza_datos import DIAS, cargar_datos
from utilidades import CMAP_DIV, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
dias = pd.date_range(sin["fecha"].min(), sin["fecha"].max())
d = pd.DataFrame({"siniestros": sin.groupby("fecha").size(), "fallecidos": sin.groupby("fecha")["fallecidos"].sum(),
                  "lesionados": sin.groupby("fecha")["lesionados"].sum()}).reindex(dias, fill_value=0)
d["dow"] = d.index.day_of_week
d["fin_semana"] = d["dow"] >= 5
d["feriado"] = d.index.isin(sin.loc[sin["feriado"], "fecha"].unique())

# 1) Estandarización: la serie se compara contra el promedio de su mismo día de la semana,
#    para no marcar como "crítico" cada domingo solo por ser domingo.
seccion("1) Serie diaria estandarizada")
for c in ["siniestros", "fallecidos"]:
    mu, sd = d.groupby("dow")[c].transform("mean"), d.groupby("dow")[c].transform("std")
    d[f"z_{c}"] = (d[c] - mu) / sd
    med = d.groupby("dow")[c].transform("median")
    mad = d.groupby("dow")[c].transform(lambda s: stats.median_abs_deviation(s, scale="normal"))
    d[f"zr_{c}"] = (d[c] - med) / mad.replace(0, np.nan)
rho, p = stats.spearmanr(d["siniestros"], d["fallecidos"])
print(f"Correlación de Spearman siniestros-fallecidos por día: rho={rho:.2f}, p={p:.2e}")
ac7 = d["siniestros"].autocorr(7)
print(f"Autocorrelación de la serie a 7 días: {ac7:.2f} (ciclo semanal)")
print(f"Días con z (mismo día de la semana) > 2: siniestros {int((d['z_siniestros'] > 2).sum())} | fallecidos {int((d['z_fallecidos'] > 2).sum())}")

# 2) Días críticos y sus características
seccion("2) Días críticos (z > 2 en siniestros o fallecidos)")
d["critico"] = (d["z_siniestros"] > 2) | (d["z_fallecidos"] > 2)
cr = d[d["critico"]].copy()
causa = sin.groupby("fecha")["causa_grupo"].agg(lambda s: s.value_counts().index[0])
cr["causa_dominante"] = causa.reindex(cr.index)
cr["dia"] = [DIAS[i].title() for i in cr["dow"]]
mostrar(cr[["dia", "siniestros", "fallecidos", "z_siniestros", "z_fallecidos", "feriado", "causa_dominante"]].round(2), 40)
guardar_tabla(cr[["dia", "siniestros", "fallecidos", "z_siniestros", "z_fallecidos", "feriado", "causa_dominante"]], "p10_dias_criticos")
print(f"\n{len(cr)} días críticos de {len(d)} ({100 * len(cr) / len(d):.1f}%)")
for var in ["fin_semana", "feriado"]:
    t = pd.crosstab(d["critico"], d[var]).reindex(index=[False, True], columns=[False, True], fill_value=0)
    o, p = stats.fisher_exact(t.values)
    print(f"Fisher crítico x {var}: OR={o:.2f}, p={p:.3f}  (% críticos entre los {var}: {100 * t.loc[True, True] / t[True].sum():.1f}% vs {100 * t.loc[True, False] / t[False].sum():.1f}%)")
print("\nCríticos por mes:", cr.groupby(cr.index.month).size().to_dict())

# Composición de causas en días críticos frente al resto
comp = pd.concat([sin[sin["fecha"].isin(cr.index)]["causa_grupo"].value_counts(normalize=True).rename("críticos"),
                  sin[~sin["fecha"].isin(cr.index)]["causa_grupo"].value_counts(normalize=True).rename("resto")], axis=1) * 100
comp["diferencia (pp)"] = comp["críticos"] - comp["resto"]
mostrar(comp.sort_values("diferencia (pp)", ascending=False).round(1))

# 3) Gráficos: serie con críticos y calendario heatmap
fig, ax = plt.subplots(2, 1, figsize=(14, 7), sharex=True)
for a, c, col in zip(ax, ["siniestros", "fallecidos"], PALETA):
    a.plot(d.index, d[c], color=col, lw=1)
    a.plot(d.index, d[c].rolling(7, center=True).mean(), color="#52514e", lw=2, label="Promedio móvil 7 días")
    crit = d[d[f"z_{c}"] > 2]
    a.scatter(crit.index, crit[c], color="#e34948", s=30, zorder=3, label="Día crítico (z > 2)")
    a.set_ylabel(f"{c.capitalize()} por día")
    a.legend(frameon=False, ncol=2, loc="upper left")
ax[1].set_xlabel("Fecha (2026)")
guardar_fig(fig, "p10_serie_diaria_criticos")

d["semana"] = d.index.to_series().dt.strftime("%G-W%V")
fig, ax = plt.subplots(1, 2, figsize=(16, 5.5), sharey=True)
for a, c in zip(ax, ["z_siniestros", "z_fallecidos"]):
    cal = d.pivot_table(index="semana", columns="dow", values=c)
    sns.heatmap(cal, cmap=CMAP_DIV, center=0, vmin=-3, vmax=3, ax=a, cbar_kws={"label": "z (vs. mismo día de la semana)"},
                linewidths=0.4, linecolor="white")
    a.set_title(f"Calendario: {c[2:]} (rojo/naranja = por encima de lo habitual)")
    a.set_xticklabels([x[:3].title() for x in DIAS], rotation=0)
    a.set_xlabel("Día de la semana")
    a.set_ylabel("Semana ISO")
guardar_fig(fig, "p10_calendario_heatmap")
