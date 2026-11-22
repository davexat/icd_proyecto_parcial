# PREGUNTA DE NEGOCIO 14 (adicional)
# ¿Cuándo, dónde y bajo qué causas ocurren los atropellos, y qué hace que un peatón tenga mayor
# probabilidad de morir?
#
# Técnicas: riesgo relativo de siniestro fatal en atropellos vs. resto, heatmaps facetados día x hora
# por zona, causas con intervalos de Wilson, perfil de edad y sexo de peatones y odds ratio por
# franja nocturna y por zona.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import DIAS, GRUPOS_EDAD, cargar_datos
from utilidades import CMAP_SEC, PALETA, guardar_fig, guardar_tabla, mostrar, odds_ratio, riesgo_relativo, seccion, wilson

sin, part = cargar_datos()
at = sin[sin["tipo_siniestro"] == "ATROPELLOS"]
ped = part[(part["rol"] == "PEATÓN") & part["condicion"].isin(["LESIONADO", "FALLECIDO"])].copy()
ped["fallecido"] = ped["condicion"].eq("FALLECIDO")

# 1) Dimensión del problema
seccion("1) Atropellos frente al resto de siniestros")
rr, lo, hi = riesgo_relativo(at["fatal"].sum(), len(at), sin.loc[sin["tipo_siniestro"] != "ATROPELLOS", "fatal"].sum(),
                             (sin["tipo_siniestro"] != "ATROPELLOS").sum())
print(f"Atropellos: {len(at):,} ({100 * len(at) / len(sin):.1f}% de los siniestros) | {at['fallecidos'].sum()} fallecidos "
      f"({100 * at['fallecidos'].sum() / sin['fallecidos'].sum():.1f}% de todos los fallecidos)")
print(f"% de siniestros fatales: atropellos {100 * at['fatal'].mean():.1f}% vs resto "
      f"{100 * sin.loc[sin['tipo_siniestro'] != 'ATROPELLOS', 'fatal'].mean():.1f}% -> RR = {rr:.2f} [{lo:.2f}-{hi:.2f}]")
print(f"Peatones víctimas: {len(ped):,} | letalidad {100 * ped['fallecido'].mean():.1f}%")

# 2) Cuándo y dónde
seccion("2) Cuándo y dónde")
print("Peso del atropello entre todos los siniestros, por franja:")
w = sin.groupby("franja", observed=True).apply(lambda g: 100 * (g["tipo_siniestro"] == "ATROPELLOS").mean(), include_groups=False)
print(w.round(1).to_string())
prov = at.groupby("provincia").agg(atropellos=("sid", "size"), fatales=("fatal", "sum"))
prov["% fatales"] = 100 * prov["fatales"] / prov["atropellos"]
prov["% de todos los siniestros de la provincia"] = 100 * prov["atropellos"] / sin.groupby("provincia").size().reindex(prov.index)
prov = prov.sort_values("atropellos", ascending=False)
mostrar(prov.round(1), 10)
guardar_tabla(prov, "p14_atropellos_por_provincia")

# 3) Causas
seccion("3) Causas de los atropellos")
c = at.groupby("causa_probable").agg(n=("sid", "size"), fatales=("fatal", "sum"))
c["%"] = 100 * c["n"] / c["n"].sum()
c["% fatales"] = 100 * c["fatales"] / c["n"]
c["ic_inf"], c["ic_sup"] = wilson(c["fatales"], c["n"])
c = c.sort_values("n", ascending=False).head(6)
c.index = [i.split("(")[0].strip().rstrip(".").capitalize()[:60] for i in c.index]
mostrar(c.round(1))

# 4) Perfil del peatón: letalidad por edad, sexo y horario
seccion("4) Perfil del peatón víctima")
pe = ped.dropna(subset=["grupo_edad"]).groupby("grupo_edad", observed=True)["fallecido"].agg(["size", "sum"]).reindex(GRUPOS_EDAD)
pe["letalidad %"] = 100 * pe["sum"] / pe["size"]
pe["ic_inf"], pe["ic_sup"] = wilson(pe["sum"], pe["size"])
mostrar(pe.round(1))
for var, ref, nom in [("nocturno", True, "noche (18-05 h)"), ("zona", "RURAL", "zona rural")]:
    a = ped[ped[var] == ref]; b = ped[ped[var] != ref]
    o, l, h, pv = odds_ratio(a["fallecido"].sum(), (~a["fallecido"]).sum(), b["fallecido"].sum(), (~b["fallecido"]).sum())
    print(f"OR de morir como peatón en {nom} vs. el resto: {o:.2f} [{l:.2f}-{h:.2f}], p={pv:.3g}")
guardar_tabla(pe, "p14_letalidad_peaton_edad")

# 5) Gráficos: heatmaps facetados por zona + perfil
dias_cal = pd.Series(pd.date_range(sin["fecha"].min(), sin["fecha"].max())).dt.day_of_week.add(1).value_counts().sort_index()
fig, ax = plt.subplots(1, 3, figsize=(19, 4.8), gridspec_kw={"width_ratios": [1.3, 1.3, 0.9]})
vmax = 0
mats = {}
for z in ["URBANA", "RURAL"]:
    m = at[at["zona"] == z].pivot_table(index="dia_semana", columns="hora_num", values="sid", aggfunc="count", fill_value=0)
    mats[z] = m.reindex(index=range(1, 8), columns=range(24), fill_value=0).div(dias_cal, axis=0)
    vmax = max(vmax, mats[z].values.max())
for a, z in zip(ax[:2], mats):
    sns.heatmap(mats[z], cmap=CMAP_SEC, vmin=0, vmax=vmax, ax=a, yticklabels=[d[:3].title() for d in DIAS],
                cbar_kws={"label": "Atropellos por día calendario"})
    a.set_title(f"Atropellos en zona {z.lower()}")
    a.set_xlabel("Hora (0-23 h)")
    a.set_ylabel("Día de la semana")
ax[2].bar(range(len(pe)), pe["letalidad %"], yerr=[pe["letalidad %"] - pe["ic_inf"], pe["ic_sup"] - pe["letalidad %"]],
          color=PALETA[1], error_kw={"ecolor": "#52514e", "capsize": 3})
ax[2].set_xticks(range(len(pe)))
ax[2].set_xticklabels(pe.index)
ax[2].set_xlabel("Grupo de edad del peatón (años)")
ax[2].set_ylabel("Letalidad entre peatones víctimas (%)")
ax[2].set_title("Letalidad del peatón por edad (IC 95%)")
guardar_fig(fig, "p14_atropellos_heatmaps_y_edad")
