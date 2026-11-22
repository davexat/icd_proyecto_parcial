# PREGUNTA DE NEGOCIO 14 (adicional)
# ¿Cuándo, dónde y por qué causas ocurren los atropellos, y qué peatones tienen mayor probabilidad
# de morir?
#
# Técnicas: comparación del % de siniestros fatales (atropellos vs resto), heatmaps facetados día x
# hora por zona, ranking de provincias y causas, y letalidad del peatón por edad, horario y zona.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import DIAS, GRUPOS_EDAD, cargar_datos
from utilidades import CMAP_SEC, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

sin, part = cargar_datos()
es_at = sin["tipo_siniestro"] == "ATROPELLOS"
at = sin[es_at]
ped = part[(part["rol"] == "PEATÓN") & part["condicion"].isin(["LESIONADO", "FALLECIDO"])].copy()
ped["fallecido"] = ped["condicion"].eq("FALLECIDO")

# 1) Dimensión del problema
seccion("1) Atropellos frente al resto de siniestros")
print(f"Atropellos: {len(at):,} ({100 * len(at) / len(sin):.1f}% de los siniestros) | {at['fallecidos'].sum()} fallecidos "
      f"({100 * at['fallecidos'].sum() / sin['fallecidos'].sum():.1f}% de todos los fallecidos)")
print(f"% de siniestros fatales: atropellos {100 * at['fatal'].mean():.1f}% vs resto {100 * sin.loc[~es_at, 'fatal'].mean():.1f}% "
      f"-> {at['fatal'].mean() / sin.loc[~es_at, 'fatal'].mean():.1f} veces")
print(f"Peatones víctimas: {len(ped):,} | letalidad {100 * ped['fallecido'].mean():.1f}%")

# 2) Cuándo y dónde
seccion("2) Cuándo y dónde")
print("Peso del atropello entre todos los siniestros, por franja (%):")
print((100 * es_at.groupby(sin["franja"], observed=True).mean()).round(1).to_string())
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
c = c.sort_values("n", ascending=False).head(6)
c.index = [i.split("(")[0].strip().rstrip(".").capitalize()[:60] for i in c.index]
mostrar(c.round(1))

# 4) Perfil del peatón: letalidad por edad, horario y zona
seccion("4) Perfil del peatón víctima")
pe = ped.dropna(subset=["grupo_edad"]).groupby("grupo_edad", observed=True)["fallecido"].agg(["size", "sum"]).reindex(GRUPOS_EDAD)
pe["letalidad %"] = 100 * pe["sum"] / pe["size"]
mostrar(pe.round(1))
for var, nom in [("nocturno", "Horario (noche = 18-05 h)"), ("zona", "Zona")]:
    print(f"\nLetalidad del peatón por {nom.lower()}:")
    print((100 * ped.groupby(var)["fallecido"].mean()).round(1).to_string())
guardar_tabla(pe, "p14_letalidad_peaton_edad")

# 5) Gráficos: heatmaps facetados por zona + letalidad por edad
dias_cal = pd.Series(pd.date_range(sin["fecha"].min(), sin["fecha"].max())).dt.day_of_week.add(1).value_counts().sort_index()
fig, ax = plt.subplots(1, 3, figsize=(19, 4.8), gridspec_kw={"width_ratios": [1.3, 1.3, 0.9]})
vmax, mats = 0, {}
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
ax[2].bar(range(len(pe)), pe["letalidad %"], color=PALETA[1])
ax[2].set_xticks(range(len(pe)))
ax[2].set_xticklabels(pe.index)
ax[2].set_xlabel("Grupo de edad del peatón (años)")
ax[2].set_ylabel("Letalidad entre peatones víctimas (%)")
ax[2].set_title("Letalidad del peatón por edad")
guardar_fig(fig, "p14_atropellos_heatmaps_y_edad")
