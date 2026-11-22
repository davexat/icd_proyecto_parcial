# PREGUNTA DE NEGOCIO 13 (adicional)
# ¿Qué entes de control reportan información más incompleta y cuánto sesga eso las conclusiones
# sobre las víctimas (edad, sexo, gravedad)?
#
# Técnicas: porcentaje de datos faltantes por ente y campo (heatmap), chi-cuadrado de independencia
# entre ente y dato faltante, comparación de víctimas con y sin edad registrada y sensibilidad de la
# letalidad por grupo de edad al restringir el análisis a entes con registro completo.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from limpieza_datos import GRUPOS_EDAD, cargar_datos
from utilidades import CMAP_SEC, PALETA, cramers_v, guardar_fig, guardar_tabla, mostrar, seccion, wilson

sin, part = cargar_datos()

# 1) Porcentaje de campos sin información por ente de control
seccion("1) Datos faltantes por ente de control")
p = part.groupby("ente_control").agg(personas=("sid", "size"), edad=("edad", lambda s: 100 * s.isna().mean()),
                                    sexo=("sexo", lambda s: 100 * s.isna().mean()),
                                    condicion=("condicion", lambda s: 100 * s.isna().mean()),
                                    tipo_id=("tipo_id", lambda s: 100 * s.isna().mean()))
s_ = sin.groupby("ente_control").agg(siniestros=("sid", "size"), vehiculo_1=("tipo_veh_1", lambda s: 100 * (s.isna() | s.eq("NO IDENTIFICADO")).mean()))
q = s_.join(p).sort_values("siniestros", ascending=False)
q.columns = ["siniestros", "% tipo vehículo 1 sin dato", "personas", "% sin edad", "% sin sexo", "% sin condición", "% sin tipo de ID"]
mostrar(q.round(1), 20)
guardar_tabla(q, "p13_faltantes_por_ente")
tab = pd.crosstab(part["ente_control"], part["edad"].isna())
chi2, pv, v = cramers_v(tab)
print(f"\nEnte x 'edad faltante': chi2={chi2:.0f}, p={pv:.2e}, V de Cramér={v:.3f}  (el faltante NO es aleatorio entre entes)")
print("Entes con >50% de personas sin edad:", ", ".join(q.index[q["% sin edad"] > 50]))

# 2) ¿Las víctimas sin edad se parecen a las que sí la tienen?
seccion("2) Víctimas con y sin edad registrada")
vic = part[part["condicion"].isin(["LESIONADO", "FALLECIDO"])].copy()
vic["fallecido"] = vic["condicion"].eq("FALLECIDO")
vic["con_edad"] = vic["edad"].notna()
g = vic.groupby("con_edad").agg(victimas=("fallecido", "size"), fallecidos=("fallecido", "sum"))
g["letalidad %"] = 100 * g["fallecidos"] / g["victimas"]
g["ic_inf"], g["ic_sup"] = wilson(g["fallecidos"], g["victimas"])
mostrar(g.round(2))
chi2, pv, v = cramers_v(pd.crosstab(vic["con_edad"], vic["fallecido"]))
print(f"Chi-cuadrado con_edad x fallecido: chi2={chi2:.1f}, p={pv:.2e}, V={v:.3f}")
print("Zona de las víctimas sin edad (%):", (vic.loc[~vic["con_edad"], "zona"].value_counts(normalize=True) * 100).round(1).to_dict())

# 3) Sensibilidad: letalidad por grupo de edad con todos los entes vs solo entes con <40% sin edad
seccion("3) Sensibilidad de la letalidad por grupo de edad a la calidad del registro")
buenos = q.index[q["% sin edad"] < 40]
print("Entes con registro de edad razonable (<40% sin edad):", ", ".join(buenos))
def leta(df):
    t = df.dropna(subset=["grupo_edad"]).groupby("grupo_edad", observed=True)["fallecido"].agg(["size", "sum"])
    t["letalidad %"] = 100 * t["sum"] / t["size"]
    return t.reindex(GRUPOS_EDAD)
a, b = leta(vic), leta(vic[vic["ente_control"].isin(buenos)])
comp = pd.DataFrame({"todos los entes": a["letalidad %"], "solo entes con buen registro": b["letalidad %"],
                     "n todos": a["size"], "n buenos": b["size"]})
mostrar(comp.round(1))
guardar_tabla(comp, "p13_sensibilidad_letalidad_edad")

# 4) Gráficos: heatmap de faltantes y sensibilidad
fig, ax = plt.subplots(1, 2, figsize=(15, 5.5), gridspec_kw={"width_ratios": [1.3, 1]})
h = q[["% sin edad", "% sin sexo", "% sin condición", "% sin tipo de ID", "% tipo vehículo 1 sin dato"]].astype(float).astype(float)
sns.heatmap(h, annot=True, fmt=".0f", cmap=CMAP_SEC, ax=ax[0], cbar_kws={"label": "% de registros sin información"})
ax[0].set_xticklabels([t.get_text().replace("% ", "").replace("sin dato", "").replace("sin ", "") for t in ax[0].get_xticklabels()], rotation=30, ha="right")
ax[0].set_ylabel("Ente de control (ordenado por siniestros)")
ax[0].set_xlabel("Campo")
ax[0].set_title("Información faltante por ente y campo")
x = np.arange(len(GRUPOS_EDAD))
ax[1].bar(x - 0.2, comp["todos los entes"], 0.4, color=PALETA[0], label="Todos los entes")
ax[1].bar(x + 0.2, comp["solo entes con buen registro"], 0.4, color=PALETA[1], label="Solo entes con buen registro")
ax[1].set_xticks(x)
ax[1].set_xticklabels(GRUPOS_EDAD)
ax[1].set_xlabel("Grupo de edad (años)")
ax[1].set_ylabel("Letalidad entre víctimas (%)")
ax[1].set_title("¿Cambia la conclusión al filtrar por calidad?")
ax[1].legend(frameon=False)
guardar_fig(fig, "p13_faltantes_y_sensibilidad")
