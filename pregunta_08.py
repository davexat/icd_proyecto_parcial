# PREGUNTA DE NEGOCIO 8
# ¿Las personas que usan casco (motociclistas) o cinturón (ocupantes de vehículos cerrados) mueren
# menos que las que no lo usan, y qué tan confiable es el registro de estas variables?
#
# Técnicas: porcentaje de fallecidos con y sin protección (total y por zona), gráfico de barras
# facetado y comparación del registro entre entes de control.
# Nota: es un análisis exploratorio, no causal (no hay datos de velocidad ni de gravedad de lesión).
import pandas as pd
import matplotlib.pyplot as plt

from limpieza_datos import cargar_datos
from utilidades import PALETA, guardar_fig, guardar_tabla, mostrar, seccion

_, part = cargar_datos()
ocupantes = part["rol"].isin(["CONDUCTOR PRESENTE", "PASAJERO"]) & part["condicion"].notna()
grupos = {
    "Casco (solo motocicletas)": (part[ocupantes & part["solo_moto"]], "casco"),
    "Cinturón (solo vehículos cerrados)": (part[ocupantes & part["solo_vehiculos_cerrados"]], "cinturon"),
}

filas = []
for nombre, (d, exp) in grupos.items():
    d = d[d[exp].isin(["SI", "NO"])].copy()
    d["fallecido"] = d["condicion"].eq("FALLECIDO")
    seccion(f"{nombre}: {len(d):,} ocupantes con condición y protección registradas")
    print(f"Uso de protección registrado como 'SI': {100 * (d[exp] == 'SI').mean():.1f}%")
    for etiqueta, sub in [("Todos", d), ("Zona urbana", d[d["zona"] == "URBANA"]), ("Zona rural", d[d["zona"] == "RURAL"])]:
        for uso, g in sub.groupby(exp):
            filas.append({"variable": nombre, "grupo": etiqueta, "protección": "Con" if uso == "SI" else "Sin",
                          "personas": len(g), "% fallecidos": 100 * g["fallecido"].mean()})
res = pd.DataFrame(filas)
mostrar(res.round(2), 30)
guardar_tabla(res, "p08_fallecidos_con_y_sin_proteccion", indice=False)
print("\nContraste con la literatura: Liu et al. (2008, Cochrane) estiman que el casco reduce ~42% el riesgo de muerte. "
      "Si aquí la diferencia es pequeña, sugiere limitaciones del registro (p. ej. 'NO' como valor por defecto, ilesos "
      "subregistrados), no ausencia de efecto.")

# Gráfico facetado: % de fallecidos con y sin protección, por zona
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
for a, nombre in zip(ax, grupos):
    r = res[res["variable"] == nombre].pivot(index="grupo", columns="protección", values="% fallecidos").reindex(["Todos", "Zona urbana", "Zona rural"])
    x = range(len(r))
    a.bar([i - 0.2 for i in x], r["Con"], 0.4, color=PALETA[0], label="Con protección")
    a.bar([i + 0.2 for i in x], r["Sin"], 0.4, color=PALETA[1], label="Sin protección")
    a.set_xticks(list(x))
    a.set_xticklabels(r.index)
    a.set_title(nombre)
    a.set_ylabel("% de ocupantes fallecidos")
    a.legend(frameon=False)
guardar_fig(fig, "p08_fallecidos_con_y_sin_proteccion")

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
