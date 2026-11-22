# PREGUNTA DE NEGOCIO 15 (adicional)
# ¿Qué características tienen los siniestros de alta consecuencia (3 o más víctimas) y qué tan
# concentradas están las víctimas en pocos eventos?
#
# Técnicas: distribución de víctimas por siniestro, porcentaje de víctimas que concentran los
# siniestros de alta consecuencia, comparación del % de alta consecuencia con y sin cada
# característica, top 10 de siniestros y gráfico facetado por zona.
import pandas as pd
import matplotlib.pyplot as plt

from limpieza_datos import cargar_datos
from utilidades import PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, _ = cargar_datos()
UMBRAL = 3
sin["alta"] = sin["n_victimas"] >= UMBRAL

# 1) Distribución y concentración
seccion("1) Distribución de víctimas por siniestro")
v = sin["n_victimas"]
print(f"Promedio de víctimas por siniestro: {v.mean():.2f} | máximo: {v.max()} | percentil 99: {v.quantile(.99):.0f}")
print(f"Siniestros con {UMBRAL} o más víctimas: {int(sin['alta'].sum()):,} ({100 * sin['alta'].mean():.1f}%) "
      f"-> concentran {100 * v[sin['alta']].sum() / v.sum():.1f}% de las víctimas y "
      f"{100 * sin.loc[sin['alta'], 'fallecidos'].sum() / sin['fallecidos'].sum():.1f}% de los fallecidos")

# 2) Características asociadas: % de alta consecuencia con la característica vs sin ella
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
    con, sin_c = 100 * sin.loc[mask, "alta"].mean(), 100 * sin.loc[~mask, "alta"].mean()
    filas.append({"característica": k, "siniestros con ella": int(mask.sum()), "% alta consecuencia (con)": con,
                  "% alta consecuencia (sin)": sin_c, "veces más probable": con / sin_c})
res = pd.DataFrame(filas).set_index("característica").sort_values("veces más probable", ascending=False)
mostrar(res.round(2), 20)
guardar_tabla(res, "p15_caracteristicas_alta_consecuencia")

# 3) Los 10 siniestros con más víctimas
seccion("3) Los 10 siniestros con más víctimas")
t10 = sin.nlargest(10, "n_victimas")[["fecha", "canton", "provincia", "tipo_siniestro", "n_vehiculos", "lesionados", "fallecidos", "causa_grupo"]]
mostrar(t10)
guardar_tabla(t10, "p15_top10_siniestros", indice=False)

# 4) Gráficos
fig, ax = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [1, 1.3]})
cnt = v.clip(upper=12).value_counts().sort_index()
ax[0].bar(cnt.index, cnt.values, color=PALETA[0])
ax[0].set_yscale("log")
ax[0].set_xlabel("Víctimas por siniestro (12 = 12 o más)")
ax[0].set_ylabel("Número de siniestros (escala log)")
ax[0].set_title("Víctimas por siniestro")
r = res.sort_values("veces más probable")
ax[1].barh(r.index, r["veces más probable"], color=PALETA[0])
ax[1].axvline(1, color="#52514e", ls="--", lw=1)
ax[1].set_xlabel("Veces más probable que el siniestro sea de alta consecuencia (1 = igual)")
ax[1].set_title("Qué se asocia a la alta consecuencia")
guardar_fig(fig, "p15_distribucion_y_caracteristicas")

fig, ax = plt.subplots(1, 2, figsize=(13, 4.2), sharey=True)
for a, zona, c in zip(ax, ["URBANA", "RURAL"], PALETA):
    d = sin[sin["zona"] == zona]
    cnt = d["n_victimas"].clip(upper=12).value_counts(normalize=True).sort_index() * 100
    a.bar(cnt.index, cnt.values, color=c)
    a.set_yscale("log")
    a.set_title(f"Zona {zona.lower()} | {100 * d['alta'].mean():.1f}% con {UMBRAL} o más víctimas")
    a.set_xlabel("Víctimas por siniestro (12 = 12 o más)")
ax[0].set_ylabel("% de siniestros (escala log)")
guardar_fig(fig, "p15_victimas_por_zona")
