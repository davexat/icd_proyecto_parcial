# PREGUNTA DE NEGOCIO 10
# ¿Qué características tienen los siniestros de alta consecuencia (3 o más víctimas), cuánto
# concentran de las víctimas y se explican por la cantidad de personas expuestas?
#
# Técnicas: concentración de víctimas y fallecidos, comparación del % de alta consecuencia con y sin
# cada característica, personas involucradas por siniestro con y sin cada característica
# (exposición), barras agrupadas con filas compartidas y top 10 de siniestros.
import pandas as pd
import matplotlib.pyplot as plt

from limpieza_datos import cargar_datos
from utilidades import GRIS, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, part = cargar_datos()
UMBRAL = 3
sin["alta"] = sin["n_victimas"] >= UMBRAL
sin["n_personas"] = sin["sid"].map(part.groupby("sid").size()).fillna(0)       # personas registradas (víctimas + ilesos)

# 1) Concentración
seccion("1) Concentración de víctimas")
v = sin["n_victimas"]
pct_sin = 100 * sin["alta"].mean()
pct_vic = 100 * v[sin["alta"]].sum() / v.sum()
pct_fal = 100 * sin.loc[sin["alta"], "fallecidos"].sum() / sin["fallecidos"].sum()
print(f"Promedio de víctimas por siniestro: {v.mean():.2f} | máximo: {v.max()}")
print(f"Siniestros con {UMBRAL} o más víctimas: {int(sin['alta'].sum()):,} ({pct_sin:.1f}%) "
      f"-> concentran {pct_vic:.1f}% de las víctimas y {pct_fal:.1f}% de los fallecidos")
print(f"Personas por siniestro: alta consecuencia {sin.loc[sin['alta'], 'n_personas'].mean():.2f} vs resto {sin.loc[~sin['alta'], 'n_personas'].mean():.2f}")

# 2) Características: % de alta consecuencia y personas por siniestro, con y sin la característica
seccion("2) Características asociadas a la alta consecuencia")
car = {
    "Choque frontal": sin["tipo_siniestro"] == "CHOQUE FRONTAL", "3 o más vehículos": sin["n_vehiculos"] >= 3,
    "Participa un bus": sin["n_bus"] > 0, "Transporte público": sin["transporte_publico"], "Red vial estatal": sin["via_estatal"],
    "Zona rural": sin["zona"] == "RURAL", "Pérdida de pista": sin["tipo_siniestro"] == "PÉRDIDA DE PISTA",
    "Participa un camión": sin["n_camion"] > 0, "Fin de semana": sin["fin_semana"], "Feriado": sin["feriado"],
    "Causa: exceso de velocidad": sin["causa_grupo"] == "Exceso de velocidad", "Horario nocturno (18-05 h)": sin["nocturno"],
    "Participa una motocicleta": sin["involucra_moto"], "Causa: alcohol / sustancias": sin["causa_grupo"] == "Alcohol / sustancias",
}
filas = []
for k, m in car.items():
    con, sn = 100 * sin.loc[m, "alta"].mean(), 100 * sin.loc[~m, "alta"].mean()
    filas.append({"característica": k, "siniestros con ella": int(m.sum()), "% alta consecuencia (con)": con,
                  "% alta consecuencia (sin)": sn, "veces más frecuente": con / sn,
                  "personas por siniestro (con)": sin.loc[m, "n_personas"].mean(),
                  "personas por siniestro (sin)": sin.loc[~m, "n_personas"].mean()})
res = pd.DataFrame(filas).set_index("característica").sort_values("veces más frecuente", ascending=False)
mostrar(res.round(2), 20)
guardar_tabla(res, "p10_caracteristicas_alta_consecuencia")

# 3) Los 10 siniestros con más víctimas
seccion("3) Los 10 siniestros con más víctimas")
t10 = sin.nlargest(10, "n_victimas")[["fecha", "canton", "provincia", "tipo_siniestro", "n_vehiculos", "lesionados", "fallecidos", "causa_grupo"]]
mostrar(t10)
guardar_tabla(t10, "p10_top10_siniestros", indice=False)

# 4) Gráfico: concentración | % de alta consecuencia con y sin | personas por siniestro con y sin
fig, ax = plt.subplots(1, 3, figsize=(18, 6.2), gridspec_kw={"width_ratios": [0.55, 1.25, 1.05]})
for i, (lab, p) in enumerate([("Siniestros", pct_sin), ("Víctimas", pct_vic), ("Fallecidos", pct_fal)]):
    ax[0].bar(i, p, color=PALETA[1], width=0.6)
    ax[0].bar(i, 100 - p, bottom=p, color=GRIS, width=0.6)
    ax[0].text(i, p / 2 if p > 12 else p + 3, f"{p:.0f} %" if p >= 10 else f"{p:.1f} %", ha="center", va="center", fontsize=10,
               color="white" if p > 12 else "#242421", fontweight="bold")
ax[0].set_xticks(range(3))
ax[0].set_xticklabels(["Siniestros", "Víctimas", "Fallecidos"])
ax[0].set_ylabel("% del total")
ax[0].set_title(f"Qué parte son los de\n{UMBRAL}+ víctimas")
ax[0].text(1, 55, "Resto", ha="center", color="white", fontsize=9)
r = res.iloc[::-1]
y = range(len(r))
h = 0.38
b = ax[1].barh([i + h / 2 for i in y], r["% alta consecuencia (con)"], h, color=PALETA[0], label="CON la característica")
ax[1].barh([i - h / 2 for i in y], r["% alta consecuencia (sin)"], h, color=GRIS, label="SIN la característica")
for i, (_, f) in zip(y, r.iterrows()):
    ax[1].text(f["% alta consecuencia (con)"] + 0.2, i + h / 2, f"{f['veces más frecuente']:.2f}×", va="center", fontsize=8)
ax[1].set_yticks(list(y))
ax[1].set_yticklabels(r.index)
ax[1].axvline(pct_sin, color="#52514e", ls="--", lw=1)
ax[1].set_xlabel(f"% de siniestros con {UMBRAL} o más víctimas (× = veces más frecuente con que sin)")
ax[1].set_title("¿Qué los hace más frecuentes?")
ax[1].legend(frameon=False, loc="lower right")
ax[2].barh([i + h / 2 for i in y], r["personas por siniestro (con)"], h, color=PALETA[0])
ax[2].barh([i - h / 2 for i in y], r["personas por siniestro (sin)"], h, color=GRIS)
for i, (_, f) in zip(y, r.iterrows()):
    ax[2].text(f["personas por siniestro (con)"] + 0.04, i + h / 2, f"{f['personas por siniestro (con)']:.1f}", va="center", fontsize=8)
ax[2].set_yticks(list(y))
ax[2].set_yticklabels([])
ax[2].set_xlabel("Personas involucradas por siniestro (promedio)")
ax[2].set_title("¿Cuánta gente van expuesta?")
guardar_fig(fig, "p10_concentracion_y_exposicion")
