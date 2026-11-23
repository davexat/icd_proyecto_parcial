# PREGUNTA DE NEGOCIO 9
# ¿Qué tipos de siniestro y qué vehículos afectan a quién? Es decir, qué rol (conductor, pasajero o
# peatón), sexo y edad tienen las víctimas según el tipo de siniestro y el vehículo involucrado.
#
# Técnicas: tabla participantes x siniestros (join por sid), composición porcentual del perfil de las
# víctimas por grupo, fila de referencia con el total y heatmaps comparables lado a lado.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza_datos import cargar_datos
from utilidades import CMAP_SEC, guardar_fig, guardar_tabla, mostrar, seccion

sin, part = cargar_datos()
vic = part[part["condicion"].isin(["LESIONADO", "FALLECIDO"])].copy()                  # víctimas
vic["rol3"] = vic["rol"].map({"CONDUCTOR PRESENTE": "Conductor", "PASAJERO": "Pasajero", "PEATÓN": "Peatón"})
VEH = {"Motocicleta": "n_motocicleta", "Automóvil": "n_automovil", "Camioneta": "n_camioneta",
       "SUV": "n_suv", "Camión": "n_camion", "Bus": "n_bus"}
vic = vic.merge(sin[["sid"] + list(VEH.values())], on="sid", how="left")
COLS = ["Conductor", "Pasajero", "Peatón", "Hombres", "Menores de 18", "65 años o más"]


def perfil(d):
    """% de víctimas por rol, sexo y edad (cada % se calcula sobre las personas con ese dato conocido)."""
    r = d["rol3"].dropna()
    s = d["sexo"][d["sexo"].isin(["HOMBRE", "MUJER"])]
    e = d["grupo_edad"].dropna()
    return pd.Series({"Conductor": 100 * (r == "Conductor").mean(), "Pasajero": 100 * (r == "Pasajero").mean(),
                      "Peatón": 100 * (r == "Peatón").mean(), "Hombres": 100 * (s == "HOMBRE").mean(),
                      "Menores de 18": 100 * e.isin(["0-11", "12-17"]).mean(), "65 años o más": 100 * (e == "65+").mean(),
                      "víctimas": len(d)})


# 1) Perfil de las víctimas según el tipo de siniestro
seccion("1) A quién afecta cada tipo de siniestro (% de las víctimas)")
base = perfil(vic).rename("Todos los siniestros")
tipo = vic.groupby("tipo_siniestro").apply(perfil, include_groups=False)
tipo = tipo[tipo["víctimas"] >= 100].sort_values("Peatón", ascending=False)
tipo.index = [t.capitalize() for t in tipo.index]
mostrar(pd.concat([base.to_frame().T, tipo]).round(1), 20)
guardar_tabla(pd.concat([base.to_frame().T, tipo]), "p09_perfil_por_tipo_siniestro")

# 2) Perfil de las víctimas según el vehículo involucrado en el siniestro
seccion("2) A quién afecta cada vehículo (víctimas de siniestros en que participa ese vehículo)")
veh = pd.DataFrame({k: perfil(vic[vic[c] > 0]) for k, c in VEH.items()}).T
veh = veh[veh["víctimas"] >= 100].sort_values("Conductor", ascending=False)
mostrar(pd.concat([base.to_frame().T, veh]).round(1), 20)
guardar_tabla(pd.concat([base.to_frame().T, veh]), "p09_perfil_por_vehiculo")
fall = vic[vic["condicion"] == "FALLECIDO"]
f = fall.groupby("tipo_siniestro").apply(perfil, include_groups=False)
print("\nSolo fallecidos en atropellos y arrollamientos (% peatón):")
print(f.loc[["ATROPELLOS", "ARROLLAMIENTOS"], ["Peatón", "víctimas"]].round(1).to_string())
print("Solo fallecidos en siniestros con moto (% conductor):", round(perfil(fall[fall["n_motocicleta"] > 0])["Conductor"], 1))

# 3) Heatmaps comparables: filas = tipo de siniestro / vehículo, columnas = quién; primera fila = total
fig, ax = plt.subplots(1, 2, figsize=(17, 6.8), gridspec_kw={"width_ratios": [1, 1], "wspace": 0.45})
for a, tabla, titulo in [(ax[0], tipo, "Según el tipo de siniestro"), (ax[1], veh, "Según el vehículo involucrado")]:
    m = pd.concat([base.to_frame().T, tabla])[COLS]
    etiquetas = [f"{i} ({int(n):,})" for i, n in zip(m.index, pd.concat([base.to_frame().T, tabla])["víctimas"])]
    sns.heatmap(m, annot=True, fmt=".0f", cmap=CMAP_SEC, vmin=0, vmax=100, ax=a, cbar=False, linewidths=0.6, linecolor="white")
    a.set_yticklabels(etiquetas, rotation=0)
    a.set_xticklabels(COLS, rotation=30, ha="right")
    a.axhline(1, color="white", lw=5)                       # separa la referencia (todos los siniestros)
    a.axvline(3, color="white", lw=5)                       # separa rol | sexo y edad
    a.set_title(titulo)
    a.set_ylabel("")
    a.set_xlabel("% de las víctimas (entre paréntesis, nº de víctimas)")
guardar_fig(fig, "p09_a_quien_afecta")
