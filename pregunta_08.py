# PREGUNTA DE NEGOCIO 8
# ¿Qué asociación existe entre el uso de casco (motociclistas) y de cinturón (ocupantes de
# vehículos cerrados) y la gravedad del desenlace, y cuán confiable es el registro de estas variables?
#
# Técnicas: odds ratio con IC 95% (Woolf) y prueba de Fisher, odds ratio ajustado por estratos con
# Mantel-Haenszel (zona x horario), forest plot facetado y auditoría del registro por ente de control.
# Nota: es un análisis exploratorio, no causal (no hay datos de velocidad, tipo de casco ni gravedad de lesión).
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from limpieza_datos import cargar_datos
from utilidades import PALETA, guardar_fig, guardar_tabla, mostrar, odds_ratio, seccion

_, part = cargar_datos()
ocupantes = part["rol"].isin(["CONDUCTOR PRESENTE", "PASAJERO"]) & part["condicion"].notna()
grupos = {
    "Casco (solo motocicletas)": (part[ocupantes & part["solo_moto"]], "casco"),
    "Cinturón (solo vehículos cerrados)": (part[ocupantes & part["solo_vehiculos_cerrados"]], "cinturon"),
}


def or_tabla(d, exp, evento):
    """OR de 'evento' para quien NO usa protección (exp == 'NO') frente a quien sí."""
    a = ((d[exp] == "NO") & d[evento]).sum(); b = ((d[exp] == "NO") & ~d[evento]).sum()
    c = ((d[exp] == "SI") & d[evento]).sum(); dd = ((d[exp] == "SI") & ~d[evento]).sum()
    o, lo, hi, p = odds_ratio(a, b, c, dd)
    return {"n": len(d), "% sin protección": 100 * (d[exp] == "NO").mean(), "% evento sin prot.": 100 * a / max(a + b, 1),
            "% evento con prot.": 100 * c / max(c + dd, 1), "OR": o, "IC_inf": lo, "IC_sup": hi, "p": p}


def mantel_haenszel(d, exp, evento, estratos):
    num = den = 0
    for _, g in d.groupby(estratos, observed=True):
        a = ((g[exp] == "NO") & g[evento]).sum(); b = ((g[exp] == "NO") & ~g[evento]).sum()
        c = ((g[exp] == "SI") & g[evento]).sum(); dd = ((g[exp] == "SI") & ~g[evento]).sum()
        n = a + b + c + dd
        if n:
            num += a * dd / n
            den += b * c / n
    return num / den if den else np.nan


resultados = []
for nombre, (d, exp) in grupos.items():
    d = d.copy()
    d["fallecido"] = d["condicion"].eq("FALLECIDO")
    d["noche"] = d["nocturno"].map({True: "noche", False: "día"})
    seccion(f"{nombre}: {len(d):,} ocupantes con condición conocida")
    print(f"Uso de protección registrado: {100 * (d[exp] == 'SI').mean():.1f}%")
    for etiqueta, sub in [("Fallecido vs. lesionado (solo víctimas)", d[d["condicion"].isin(["FALLECIDO", "LESIONADO"])]),
                          ("Fallecido vs. el resto (incluye ilesos)", d)]:
        fila = or_tabla(sub, exp, "fallecido")
        fila["OR Mantel-Haenszel (zona x día/noche)"] = mantel_haenszel(sub, exp, "fallecido", ["zona", "noche"])
        resultados.append({"variable": nombre, "análisis": etiqueta, "estrato": "Todos", **fila})
        print(f"\n{etiqueta}: OR sin protección = {fila['OR']:.2f} [{fila['IC_inf']:.2f}-{fila['IC_sup']:.2f}], "
              f"p={fila['p']:.3g}; OR ajustado (M-H) = {fila['OR Mantel-Haenszel (zona x día/noche)']:.2f}")
        if etiqueta.startswith("Fallecido vs. el resto"):
            for var, valores in [("zona", ["URBANA", "RURAL"]), ("noche", ["día", "noche"]), ("sexo", ["HOMBRE", "MUJER"])]:
                for v in valores:
                    s = sub[sub[var] == v]
                    if len(s) > 100:
                        resultados.append({"variable": nombre, "análisis": etiqueta, "estrato": v.capitalize(), **or_tabla(s, exp, "fallecido")})
res = pd.DataFrame(resultados)
guardar_tabla(res, "p08_odds_ratio", indice=False)
print("\nContraste con la literatura: Liu et al. (2008, Cochrane) estiman que el casco reduce ~42% el riesgo de muerte. "
      "Un OR cercano a 1 aquí sugiere limitaciones del registro (p. ej. 'NO' como valor por defecto, ilesos subregistrados), "
      "no ausencia de efecto.")

# Forest plot facetado: OR de muerte (sin protección vs con protección) por estrato
fig, ax = plt.subplots(1, 2, figsize=(13, 4.8), sharex=True)
for a, (nombre, _) in zip(ax, grupos.items()):
    r = res[(res["variable"] == nombre) & res["análisis"].str.startswith("Fallecido vs. el resto")].reset_index(drop=True)
    y = np.arange(len(r))[::-1]
    a.errorbar(r["OR"], y, xerr=[r["OR"] - r["IC_inf"], r["IC_sup"] - r["OR"]], fmt="o", color=PALETA[0], capsize=3)
    a.axvline(1, color="#52514e", ls="--", lw=1)
    a.set_yticks(y)
    a.set_yticklabels(r["estrato"])
    a.set_xscale("log")
    a.set_xlabel("Odds ratio de morir: sin protección vs con protección (escala log, IC 95%)")
    a.set_title(nombre)
guardar_fig(fig, "p08_forest_plot")

# Auditoría del registro: % de motociclistas con casco 'SI' por ente de control
seccion("Auditoría del registro de casco por ente de control (motociclistas, n >= 100)")
m = grupos["Casco (solo motocicletas)"][0]
aud = m.groupby("ente_control").agg(n=("sid", "size"), con_casco=("casco", lambda s: 100 * (s == "SI").mean())).query("n >= 100")
aud = aud.sort_values("con_casco")
mostrar(aud.round(1))
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.barh(aud.index, aud["con_casco"], color=PALETA[0])
ax.set_xlabel("% de ocupantes de motocicleta con casco registrado como 'SI'")
ax.set_ylabel("Ente de control")
ax.set_title("Casco registrado como SI, por ente de control")
guardar_fig(fig, "p08_auditoria_casco_por_ente")
