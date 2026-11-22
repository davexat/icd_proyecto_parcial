# PREGUNTA DE NEGOCIO 2
# ¿Los feriados modifican el volumen, el horario y la gravedad de los siniestros respecto a días
# normales equivalentes (mismo día de la semana)?
#
# Técnicas: comparación contra línea base del mismo día de la semana, bootstrap del cociente,
# Mann-Whitney, chi-cuadrado / Kolmogorov-Smirnov sobre el perfil horario, intervalos de Wilson
# para la gravedad y gráfico facetado por tipo de día.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

from limpieza_datos import cargar_datos, DIAS
from utilidades import PALETA, cramers_v, guardar_fig, guardar_tabla, mostrar, seccion, wilson

sin, _ = cargar_datos()
rng = np.random.default_rng(42)
dias = pd.date_range(sin["fecha"].min(), sin["fecha"].max())
diario = pd.DataFrame({"siniestros": sin.groupby("fecha").size(), "fallecidos": sin.groupby("fecha")["fallecidos"].sum()}
                      ).reindex(dias, fill_value=0)
diario["feriado"] = diario.index.isin(sin.loc[sin["feriado"], "fecha"].unique())
diario["dow"] = diario.index.day_of_week

# 1) Bloques de feriado (fechas consecutivas) frente a la línea base del mismo día de la semana
seccion("1) Cada feriado frente a días no feriados del mismo día de la semana")
base = diario[~diario["feriado"]].groupby("dow")[["siniestros", "fallecidos"]].mean()
fer = diario[diario["feriado"]].copy()
fer["bloque"] = (fer.index.to_series().diff().dt.days.ne(1)).cumsum().values
fer["esperado"] = fer["dow"].map(base["siniestros"])
fer["razon"] = fer["siniestros"] / fer["esperado"]
bloques = fer.groupby("bloque").agg(inicio=("siniestros", lambda s: s.index.min().date()),
                                    fin=("siniestros", lambda s: s.index.max().date()), dias=("siniestros", "size"),
                                    siniestros_dia=("siniestros", "mean"), esperado_dia=("esperado", "mean"),
                                    razon=("razon", "mean"), fallecidos_dia=("fallecidos", "mean"))
mostrar(bloques.round(2))
guardar_tabla(bloques, "p02_bloques_feriado")

# 2) Efecto global con IC bootstrap y Wilcoxon sobre las razones
seccion("2) Efecto global del feriado")
razones = fer["razon"].values
boot = [rng.choice(razones, len(razones)).mean() for _ in range(5000)]
w = stats.wilcoxon(razones - 1)
print(f"Razón media observado/esperado = {razones.mean():.2f}  IC95% bootstrap [{np.percentile(boot, 2.5):.2f}, {np.percentile(boot, 97.5):.2f}]")
print(f"Wilcoxon (razón vs 1): p = {w.pvalue:.4f}")
mw = stats.mannwhitneyu(diario.loc[diario["feriado"], "siniestros"], diario.loc[~diario["feriado"], "siniestros"])
print(f"Mann-Whitney siniestros/día feriado vs no feriado (sin controlar día): p = {mw.pvalue:.4f}")

# 3) Perfil horario y gravedad por tipo de día
seccion("3) Perfil horario y gravedad por tipo de día")
orden = ["LABORABLE", "FIN DE SEMANA", "FERIADO"]
tab = pd.crosstab(sin["tipo_dia"], sin["franja"])
chi2, p, v = cramers_v(tab.loc[orden])
print(f"Chi-cuadrado tipo de día x franja horaria: chi2={chi2:.1f}, p={p:.2e}, V de Cramér={v:.3f}")
ks = stats.ks_2samp(sin.loc[sin["feriado"], "hora_decimal"], sin.loc[~sin["feriado"] & ~sin["fin_semana"], "hora_decimal"])
print(f"Kolmogorov-Smirnov hora feriado vs laborable: D={ks.statistic:.3f}, p={ks.pvalue:.4f}")
grav = sin.groupby("tipo_dia").agg(siniestros=("sid", "size"), fatales=("fatal", "sum"), fallecidos=("fallecidos", "sum"),
                                   lesionados=("lesionados", "sum")).loc[orden]
grav["% fatales"] = 100 * grav["fatales"] / grav["siniestros"]
grav["ic_inf"], grav["ic_sup"] = wilson(grav["fatales"], grav["siniestros"])
mostrar(grav.round(2))
guardar_tabla(grav, "p02_gravedad_por_tipo_dia")

# 4) Gráfico facetado: perfil horario (% del total del grupo) y gravedad con IC
fig, ax = plt.subplots(1, 4, figsize=(17, 3.8), gridspec_kw={"width_ratios": [1, 1, 1, 0.9]}, sharey=False)
hora = pd.crosstab(sin["tipo_dia"], sin["hora_num"], normalize="index").loc[orden] * 100
for a, t, c in zip(ax[:3], orden, PALETA):
    a.bar(hora.columns, hora.loc[t], color=c)
    a.set_title(t.capitalize())
    a.set_xlabel("Hora (0-23 h)")
    a.set_ylabel("% de siniestros del grupo")
    a.set_ylim(0, hora.values.max() * 1.1)
ax[3].errorbar(range(3), grav["% fatales"], yerr=[grav["% fatales"] - grav["ic_inf"], grav["ic_sup"] - grav["% fatales"]],
               fmt="o", color=PALETA[0], capsize=4)
ax[3].set_xticks(range(3))
ax[3].set_xticklabels([t.capitalize() for t in orden], rotation=20)
ax[3].set_ylabel("% de siniestros con fallecidos")
ax[3].set_title("Gravedad (IC 95%)")
ax[3].set_xlim(-0.5, 2.5)
guardar_fig(fig, "p02_perfil_horario_y_gravedad")

# 5) Serie diaria con feriados resaltados
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
