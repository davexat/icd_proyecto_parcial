# PREGUNTA DE NEGOCIO 15 (adicional)
# ¿Qué características distinguen a los siniestros de alta consecuencia (3 o más víctimas) y qué
# tan concentrada está la mortalidad en pocos eventos?
#
# Técnicas: distribución de víctimas por siniestro (escala log) y índice de sobredispersión frente a
# Poisson, curva de Lorenz de las víctimas, odds ratio con IC 95% de cada característica y gráfico
# facetado por zona.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

from limpieza_datos import cargar_datos
from utilidades import PALETA, gini, guardar_fig, guardar_tabla, lorenz, mostrar, odds_ratio, seccion

sin, _ = cargar_datos()
UMBRAL = 3
sin["alta"] = sin["n_victimas"] >= UMBRAL

# 1) Distribución y concentración
seccion("1) Distribución de víctimas por siniestro")
v = sin["n_victimas"]
print(f"Media = {v.mean():.2f}, varianza = {v.var():.2f}, índice de sobredispersión (var/media) = {v.var() / v.mean():.2f} "
      f"(Poisson = 1; valores > 1 indican eventos masivos más frecuentes que el azar)")
print(f"Siniestros con >= {UMBRAL} víctimas: {int(sin['alta'].sum()):,} ({100 * sin['alta'].mean():.1f}%) "
      f"-> concentran {100 * v[sin['alta']].sum() / v.sum():.1f}% de las víctimas y {100 * sin.loc[sin['alta'], 'fallecidos'].sum() / sin['fallecidos'].sum():.1f}% de los fallecidos")
print(f"Gini de las víctimas por siniestro = {gini(v):.2f} | percentil 99 = {v.quantile(.99):.0f} víctimas")

# 2) Características asociadas (odds ratio)
seccion("2) Características asociadas a la alta consecuencia")
car = {
    "Participa un bus": sin["n_bus"] > 0, "Transporte público": sin["transporte_publico"], "Participa un camión": sin["n_camion"] > 0,
    "Participa una motocicleta": sin["involucra_moto"], "3 o más vehículos": sin["n_vehiculos"] >= 3,
    "Zona rural": sin["zona"] == "RURAL", "Horario nocturno (18-05 h)": sin["nocturno"], "Fin de semana": sin["fin_semana"],
    "Feriado": sin["feriado"], "Red vial estatal": sin["via_estatal"],
    "Causa: exceso de velocidad": sin["causa_grupo"] == "Exceso de velocidad",
    "Causa: alcohol / sustancias": sin["causa_grupo"] == "Alcohol / sustancias",
    "Choque frontal": sin["tipo_siniestro"] == "CHOQUE FRONTAL", "Pérdida de pista": sin["tipo_siniestro"] == "PÉRDIDA DE PISTA",
}
filas = []
for k, mask in car.items():
    a = (mask & sin["alta"]).sum(); b = (mask & ~sin["alta"]).sum()
    c = (~mask & sin["alta"]).sum(); d = (~mask & ~sin["alta"]).sum()
    o, lo, hi, p = odds_ratio(a, b, c, d)
    filas.append({"característica": k, "siniestros con ella": int(mask.sum()), "% alta consecuencia (con)": 100 * a / max(a + b, 1),
                  "% alta consecuencia (sin)": 100 * c / max(c + d, 1), "OR": o, "IC_inf": lo, "IC_sup": hi, "p": p})
res = pd.DataFrame(filas).set_index("característica").sort_values("OR", ascending=False)
mostrar(res.round(3), 20)
guardar_tabla(res, "p15_odds_ratio_alta_consecuencia")

# 3) Los 10 siniestros con más víctimas
seccion("3) Los 10 siniestros con más víctimas")
t10 = sin.nlargest(10, "n_victimas")[["fecha", "canton", "provincia", "tipo_siniestro", "n_vehiculos", "lesionados", "fallecidos", "causa_grupo"]]
mostrar(t10)
guardar_tabla(t10, "p15_top10_siniestros", indice=False)

# 4) Gráficos
fig, ax = plt.subplots(1, 3, figsize=(17, 5), gridspec_kw={"width_ratios": [1, 1, 1.2]})
cnt = v.clip(upper=12).value_counts().sort_index()
ax[0].bar(cnt.index, cnt.values, color=PALETA[0])
ax[0].set_yscale("log")
ax[0].set_xlabel("Víctimas por siniestro (12 = 12 o más)")
ax[0].set_ylabel("Número de siniestros (escala log)")
ax[0].set_title("Víctimas por siniestro")
y, x = lorenz(v.values)
ax[1].plot(x, y, color=PALETA[1])
ax[1].plot([0, 1], [0, 1], color="#8a8a85", ls="--")
ax[1].set_xlabel("Proporción acumulada de siniestros (de menos a más víctimas)")
ax[1].set_ylabel("Proporción acumulada de víctimas")
ax[1].set_title(f"Lorenz de víctimas (Gini {gini(v):.2f})")
r = res.sort_values("OR")
ax[2].errorbar(r["OR"], range(len(r)), xerr=[r["OR"] - r["IC_inf"], r["IC_sup"] - r["OR"]], fmt="o", color=PALETA[0], capsize=3)
ax[2].axvline(1, color="#52514e", ls="--", lw=1)
ax[2].set_yticks(range(len(r)))
ax[2].set_yticklabels(r.index, fontsize=8)
ax[2].set_xscale("log")
ax[2].set_xlabel("Odds ratio de alta consecuencia (escala log, IC 95%)")
ax[2].set_title("Qué aumenta la probabilidad")
guardar_fig(fig, "p15_distribucion_lorenz_or")

fig, ax = plt.subplots(1, 2, figsize=(13, 4.2), sharey=True)
for a, zona, c in zip(ax, ["URBANA", "RURAL"], PALETA):
    d = sin[sin["zona"] == zona]
    cnt = d["n_victimas"].clip(upper=12).value_counts(normalize=True).sort_index() * 100
    a.bar(cnt.index, cnt.values, color=c)
    a.set_yscale("log")
    a.set_title(f"Zona {zona.lower()} | {100 * d['alta'].mean():.1f}% con ≥ {UMBRAL} víctimas")
    a.set_xlabel("Víctimas por siniestro (12 = 12 o más)")
ax[0].set_ylabel("% de siniestros (escala log)")
guardar_fig(fig, "p15_victimas_por_zona")
