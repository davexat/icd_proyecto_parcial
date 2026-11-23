# PREGUNTA DE NEGOCIO 8
# ¿Qué perfil (edad, sexo y rol en la vía) tienen las personas lesionadas y fallecidas, y qué
# grupos son proporcionalmente más vulnerables?
#
# Técnicas: tabla de participantes en formato largo, letalidad (fallecidos / víctimas) por perfil,
# edad mediana, pirámide de población facetada por condición, barras agrupadas sexo x edad y
# heatmap rol x grupo de edad.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import GRUPOS_EDAD, cargar_datos
from utilidades import CMAP_SEC, PALETA, guardar_fig, guardar_tabla, mostrar, seccion

_, part = cargar_datos()

# 0) Cobertura de datos: cuántas personas tienen edad / sexo / condición válidos
seccion("0) Cobertura de datos de las personas involucradas")
print(f"Personas registradas: {len(part):,}")
for c in ["edad", "sexo", "condicion"]:
    print(f"  {c}: {100 * part[c].notna().mean():.1f}% con dato válido")
vic = part[part["condicion"].isin(["LESIONADO", "FALLECIDO"])].copy()       # víctimas
vic["fallecido"] = vic["condicion"].eq("FALLECIDO")
print(f"Víctimas (lesionados + fallecidos): {len(vic):,} | con edad: {100 * vic['edad'].notna().mean():.1f}% "
      f"| con sexo: {100 * vic['sexo'].notna().mean():.1f}%")

# 1) Letalidad entre víctimas por rol, sexo y grupo de edad
seccion("1) Letalidad entre víctimas (fallecidos / (fallecidos + lesionados))")
tablas = {}
for var in ["rol", "sexo", "grupo_edad"]:
    d = vic.dropna(subset=[var]).groupby(var, observed=True).agg(victimas=("fallecido", "size"), fallecidos=("fallecido", "sum"))
    d["letalidad %"] = 100 * d["fallecidos"] / d["victimas"]
    tablas[var] = d
    print(f"\nPor {var}:")
    mostrar(d.round(2))
guardar_tabla(pd.concat(tablas), "p08_letalidad_por_perfil")
e = vic.dropna(subset=["edad"])
print(f"\nEdad mediana: fallecidos {e.loc[e['fallecido'], 'edad'].median():.0f} años | lesionados {e.loc[~e['fallecido'], 'edad'].median():.0f} años")
con_e, sin_e = vic[vic["edad"].notna()], vic[vic["edad"].isna()]
print(f"Letalidad entre víctimas con edad registrada: {100 * con_e['fallecido'].mean():.1f}% | sin edad: {100 * sin_e['fallecido'].mean():.1f}%")
hm = vic[vic["sexo"].isin(["HOMBRE", "MUJER"])]["sexo"].value_counts()
print(f"Razón hombre : mujer entre víctimas con sexo conocido = {hm['HOMBRE'] / hm['MUJER']:.1f} : 1")

# 2) Pirámide de población facetada: lesionados | fallecidos
fig, ax = plt.subplots(1, 2, figsize=(13, 4.8), sharey=True)
for a, cond in zip(ax, ["LESIONADO", "FALLECIDO"]):
    d = vic[(vic["condicion"] == cond) & vic["grupo_edad"].notna() & vic["sexo"].isin(["HOMBRE", "MUJER"])]
    c = pd.crosstab(d["grupo_edad"], d["sexo"]).reindex(GRUPOS_EDAD, fill_value=0)
    a.barh(range(len(c)), -c["HOMBRE"], color=PALETA[0], label="Hombres")
    a.barh(range(len(c)), c["MUJER"], color=PALETA[1], label="Mujeres")
    a.set_yticks(range(len(c)))
    a.set_yticklabels(c.index)
    mx = c.values.max() * 1.1
    a.set_xlim(-mx, mx)
    a.set_xticks(a.get_xticks())
    a.set_xticklabels([f"{abs(int(x)):,}" for x in a.get_xticks()])
    a.set_title(f"{cond.capitalize()}s")
    a.set_xlabel("Personas (con edad y sexo conocidos)")
    a.axvline(0, color="#52514e", lw=0.8)
ax[0].set_ylabel("Grupo de edad (años)")
ax[0].legend(frameon=False)
guardar_fig(fig, "p08_piramide_lesionados_fallecidos")

# 3) Vulnerabilidad: letalidad por edad y sexo (barras agrupadas) y por rol y edad (heatmap).
#    Se omiten las celdas con menos de 30 personas.
seccion("2) Letalidad por sexo y grupo de edad")
ls = vic[vic["sexo"].isin(["HOMBRE", "MUJER"])].dropna(subset=["grupo_edad"])
let_se = ls.pivot_table(index="sexo", columns="grupo_edad", values="fallecido", aggfunc="mean", observed=False)[GRUPOS_EDAD] * 100
n_se = ls.pivot_table(index="sexo", columns="grupo_edad", values="fallecido", aggfunc="size", observed=False)[GRUPOS_EDAD]
mostrar(pd.concat({"letalidad %": let_se, "víctimas": n_se}, axis=1).round(1))
guardar_tabla(pd.concat({"letalidad %": let_se, "víctimas": n_se}, axis=1), "p08_letalidad_sexo_edad")
d = vic.dropna(subset=["grupo_edad"])
let = d.pivot_table(index="rol", columns="grupo_edad", values="fallecido", aggfunc="mean", observed=False) * 100
n = d.pivot_table(index="rol", columns="grupo_edad", values="fallecido", aggfunc="size", observed=False)
let = let.astype(float).where(n >= 30).dropna(how="all")
fig, ax = plt.subplots(1, 2, figsize=(14, 4.8), gridspec_kw={"width_ratios": [1, 1.15]})
for desp, sexo, c, lab in [(-0.2, "HOMBRE", PALETA[0], "Hombres"), (0.2, "MUJER", PALETA[1], "Mujeres")]:
    b = ax[0].bar([i + desp for i in range(len(GRUPOS_EDAD))], let_se.loc[sexo], 0.4, color=c, label=lab)
    ax[0].bar_label(b, fmt="%.0f", fontsize=8, padding=2)
ax[0].set_xticks(range(len(GRUPOS_EDAD)))
ax[0].set_xticklabels(GRUPOS_EDAD)
ax[0].set_xlabel("Grupo de edad (años)")
ax[0].set_ylabel("Letalidad entre víctimas (%)")
ax[0].set_title("Por sexo y edad")
ax[0].legend(frameon=False, loc="upper left")
sns.heatmap(let, annot=True, fmt=".0f", cmap=CMAP_SEC, ax=ax[1], cbar_kws={"label": "Letalidad entre víctimas (%)"})
ax[1].set_xlabel("Grupo de edad (años; celdas con n < 30 omitidas)")
ax[1].set_ylabel("Rol en el siniestro")
ax[1].set_yticklabels([t.get_text().capitalize() for t in ax[1].get_yticklabels()], rotation=0)
ax[1].set_title("Por rol y edad")
guardar_fig(fig, "p08_vulnerabilidad")
