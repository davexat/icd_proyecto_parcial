"""
limpieza_datos.py
=================
Modulo compartido por pregunta_01.py ... pregunta_15.py.

Dataset: siniestros de transito en Ecuador, enero-septiembre 2026
(archivo "08. BDD_Septiembre_2026_SM.xlsx", hoja BDD_2026, 17.236 filas x 374 columnas).
Cada fila es un siniestro; las columnas *_1 ... *_43 describen hasta 43 participantes
(formato ancho) y TIPO_DE_VEHICULO_1 ... _13 hasta 13 vehiculos.

Que hace este modulo
--------------------
1. Lee el Excel y mide el RUIDO (datos que no sirven para el analisis).
2. Limpia y transforma: texto, fechas/horas, marcadores "ND"/"NO IDENTIFICADO"/-1, etc.
3. Pasa los participantes de formato ancho a formato largo (una fila por persona).
4. Crea metricas nuevas (features) basadas en literatura (ver REFERENCIAS).
5. Guarda el resultado en ./datos (cache parquet) para que cada pregunta cargue en segundos.

Uso
---
    python limpieza_datos.py        -> reconstruye todo e imprime el reporte de ruido y los pasos
    from limpieza_datos import cargar_datos
    sin, part = cargar_datos()      -> siniestros (1 fila = 1 siniestro) y participantes (1 fila = 1 persona)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):          # evita errores de acentos en consolas de Windows
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent
DIR_DATOS = RAIZ / "datos"
DIR_RES = RAIZ / "resultados"
N_PARTICIPANTES = 43
N_VEHICULOS = 13

# Pesos de la severidad ponderada (estilo EPDO). Son un SUPUESTO ajustable, no un estandar oficial.
PESO_FALLECIDO = 10
PESO_LESIONADO = 1

MESES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE"]
DIAS = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
FRANJAS = ["Madrugada (00-05)", "Mañana (06-11)", "Tarde (12-17)", "Noche (18-23)"]
GRUPOS_EDAD = ["0-11", "12-17", "18-29", "30-64", "65+"]

# Agrupacion de las 26 causas probables (CODIGO_CAUSA) por factor contribuyente.
# Idea del modelo humano - vehiculo - via/entorno (Haddon 1968; Sabey y Taylor 1980).
CAUSA_GRUPO = {
    "C09": "Exceso de velocidad",
    "C14": "Distracción al conducir",
    "C06": "Alcohol / sustancias", "C07": "Alcohol / sustancias",
    "C03": "Fatiga / somnolencia",
    "C23": "Irrespeto de señales / prioridad", "C24": "Irrespeto de señales / prioridad",
    "C25": "Irrespeto de señales / prioridad", "C26": "Irrespeto de señales / prioridad",
    "C11": "Maniobras y distancia", "C12": "Maniobras y distancia", "C18": "Maniobras y distancia",
    "C19": "Maniobras y distancia", "C22": "Maniobras y distancia",
    "C16": "Conducta del peatón / pasajero", "C17": "Conducta del peatón / pasajero",
    "C27": "Conducta del peatón / pasajero",
    "C04": "Vehículo / carga", "C05": "Vehículo / carga", "C08": "Vehículo / carga",
    "C01": "Vía y entorno", "C02": "Vía y entorno", "C10": "Vía y entorno", "C21": "Vía y entorno",
    "C15": "Otras infracciones", "C20": "Otras infracciones",
}
CAUSA_FACTOR = {c: ("Vehículo" if g == "Vehículo / carga" else "Vía y entorno" if g == "Vía y entorno" else "Humano")
                for c, g in CAUSA_GRUPO.items()}

REFERENCIAS = {
    "n_victimas, letalidad": "WHO (2023). Global status report on road safety 2023. Geneva: World Health Organization. "
                             "ISBN 978-92-4-008651-7. | Elvik, R., Hoye, A., Vaa, T., Sorensen, M. (2009). "
                             "The Handbook of Road Safety Measures (2a ed.). Emerald.",
    "severidad (FATAL / CON LESIONADOS / SIN VICTIMAS)": "AASHTO (2010). Highway Safety Manual (1a ed.). Escala de severidad "
                             "tipo KABCO, simplificada a 3 niveles porque el dataset no distingue lesiones graves.",
    "severidad_ponderada": "AASHTO (2010). Highway Safety Manual: idea de 'accidentes equivalentes' (EPDO) que pondera "
                           "mas a las victimas graves. Los pesos 10:1 usados aqui son un supuesto del proyecto.",
    "causa_grupo, factor_causal": "Haddon, W. (1968). The changing approach to the epidemiology, prevention, and amelioration "
                                  "of trauma. Am. J. Public Health, 58(8). | Sabey, B. E., Taylor, H. (1980). The known risks "
                                  "we run: the highway. TRRL Supplementary Report 567.",
    "usuario_vulnerable": "Peden, M. et al. (2004). World report on road traffic injury prevention. WHO. | WHO (2023).",
    "celda de cuadricula, densidad kernel": "Xie, Z., Yan, J. (2008). Kernel density estimation of traffic accidents in a network "
                                            "space. Computers, Environment and Urban Systems, 32(5), 396-406. | Anderson, T. K. "
                                            "(2009). Kernel density estimation and K-means clustering to profile road accident "
                                            "hotspots. Accident Analysis & Prevention, 41(3), 359-364.",
    "hotspots (Gi*)": "Getis, A., Ord, J. K. (1992). The analysis of spatial association by use of distance statistics. "
                      "Geographical Analysis, 24(3), 189-206.",
    "indice de estacionalidad": "Hyndman, R. J., Athanasopoulos, G. (2021). Forecasting: Principles and Practice (3a ed.). OTexts.",
    "indice de sobredispersion": "Lord, D., Mannering, F. (2010). The statistical analysis of crash-frequency data: a review and "
                                 "assessment of methodological alternatives. Transportation Research Part A, 44(5), 291-305.",
    "uso de casco (OR)": "Liu, B. C. et al. (2008). Helmets for preventing injury in motorcycle riders. Cochrane Database of "
                         "Systematic Reviews, 2008(1), CD004333.",
}

# Columnas de analisis (para medir ruido). 'ND' en campos viales = no aplica (el dataset solo tiene
# datos de vias de la red estatal); se reporta aparte y no cuenta como ruido.
CAMPOS_SIN_RUIDO = ["fecha", "hora_num", "provincia", "canton", "parroquia", "zona", "lat", "lon", "causa_probable",
                    "tipo_siniestro", "tipo_veh_1", "servicio_1", "lesionados", "fallecidos", "ente_control"]
CAMPOS_VIALES = ["id_via", "nombre_via", "ubicacion_via", "jerarquia_via"]
CAMPOS_PART = ["edad", "sexo", "condicion", "rol", "tipo_id"]


# --------------------------------------------------------------------------------------
# Lectura
# --------------------------------------------------------------------------------------
def _ruta_excel():
    archivos = [p for p in RAIZ.glob("*.xlsx") if not p.name.startswith("~$")]
    if not archivos:
        raise FileNotFoundError("No se encontro el .xlsx en la carpeta del proyecto: " + str(RAIZ))
    return archivos[0]


def _leer_crudo():
    return pd.read_excel(_ruta_excel(), engine="openpyxl")


# --------------------------------------------------------------------------------------
# Limpieza + transformacion
# --------------------------------------------------------------------------------------
def _texto(s):
    """Quita espacios sobrantes y pasa a mayusculas (corrige 'colisión' vs 'COLISIÓN')."""
    return s.astype("string").str.strip().str.upper()


def _construir(raw):
    pasos = []   # (paso, descripcion, registros_o_celdas_afectados, porcentaje)

    def anotar(paso, descr, n, total):
        pasos.append({"paso": paso, "descripcion": descr, "afectados": int(n),
                      "base": int(total), "porcentaje": round(100 * n / total, 2) if total else 0.0})

    n = len(raw)
    anotar("0. Lectura", f"Filas x columnas leídas: {n} x {raw.shape[1]}", 0, n)

    # Paso 1 - estructura: columnas casi vacias (slots de participantes/vehiculos poco usados)
    vacias = raw.isna().mean()
    anotar("1. Estructura", "Columnas con >95% de celdas vacías (slots de participantes/vehículos poco usados); "
                            "no son ruido: se reorganizan en formato largo", (vacias > 0.95).sum(), raw.shape[1])
    anotar("1. Estructura", "Celdas vacías sobre el total de la tabla ancha (esparsidad estructural)",
           raw.isna().sum().sum(), raw.size)

    # Paso 2 - duplicados
    anotar("2. Duplicados", "Filas completamente duplicadas", raw.duplicated().sum(), n)
    ids_rep = raw["SINIESTROS"].duplicated(keep=False)
    anotar("2. Duplicados", "Registros con código SINIESTROS repetido (son hechos distintos: otra provincia/ente/"
                            "coordenadas; se conservan y se usa un identificador interno 'sid')", ids_rep.sum(), n)

    # Paso 3 - renombrar y seleccionar columnas
    s = pd.DataFrame({"sid": np.arange(n)})
    s["id_siniestro"] = raw["SINIESTROS"].astype("string")
    s["fecha"] = pd.to_datetime(raw["FECHA"])

    # Paso 4 - hora: objetos time y 5 textos 'HH:MM'
    hs = raw["HORA"].map(lambda x: x.strftime("%H:%M") if hasattr(x, "strftime") else str(x)[:5])
    n_txt = raw["HORA"].map(lambda x: isinstance(x, str)).sum()
    anotar("4. Fecha/hora", "Horas guardadas como texto 'HH:MM' en lugar de hora; se convierten", n_txt, n)
    s["hora_num"] = hs.str[:2].astype(int)
    s["minuto"] = hs.str[3:5].astype(int)
    s["hora_decimal"] = s["hora_num"] + s["minuto"] / 60
    incons = (s["hora_num"] != raw["PERIODO_2"]).sum()
    anotar("4. Fecha/hora", "Hora inconsistente con la franja PERIODO_2 tras la conversión", incons, n)
    anotar("4. Fecha/hora", "Día de la semana (DIA_2) inconsistente con FECHA",
           ((s["fecha"].dt.day_of_week + 1) != raw["DIA_2"]).sum(), n)

    s["mes"] = s["fecha"].dt.month
    s["dia_semana"] = s["fecha"].dt.day_of_week + 1        # 1 = lunes ... 7 = domingo
    s["feriado"] = _texto(raw["FERIADO"]).eq("SI")

    # Paso 5 - texto
    for nuevo, viejo in [("ente_control", "ENTE_DE_CONTROL"), ("provincia", "PROVINCIA"), ("canton", "CANTON"),
                         ("parroquia", "PARROQUIA"), ("zona_planificacion", "ZONA_PLANIFICACION"), ("zona", "ZONA"),
                         ("tipo_siniestro", "TIPO_DE_SINIESTRO"), ("causa_probable", "CAUSA_PROBABLE"),
                         ("tipo_veh_1", "TIPO_DE_VEHICULO_1"), ("servicio_1", "SERVICIO_1"),
                         ("tipo_veh_2", "TIPO_DE_VEHICULO_2")]:
        s[nuevo] = _texto(raw[viejo])
    anotar("5. Texto", "Categorías de tipo de siniestro con variantes de mayúsculas/espacios unificadas",
           (raw["TIPO_DE_SINIESTRO"].astype("string") != s["tipo_siniestro"]).sum(), n)
    s["cod_causa"] = _texto(raw["CODIGO_CAUSA"])
    s["direccion"] = _texto(raw["DIRECCION"])
    s["lat"] = raw["LATITUD_Y"].astype(float)
    s["lon"] = raw["LONGITUD_X"].astype(float)

    # Paso 6 - coordenadas: dentro de Ecuador (continente + Galapagos)
    fuera = ~(s["lat"].between(-5.1, 1.6) & s["lon"].between(-92.2, -75.0)) | s["lat"].isna() | s["lon"].isna()
    anotar("6. Coordenadas", "Coordenadas fuera de Ecuador (continental + Galápagos) o nulas", fuera.sum(), n)
    s.loc[fuera, ["lat", "lon"]] = np.nan

    # Paso 7 - campos viales: ND = no aplica
    for nuevo, viejo in [("id_via", "ID_DE_LA_VIA"), ("nombre_via", "NOMBRE_DE_LA_VIA"),
                         ("ubicacion_via", "UBICACION_DE_LA_VIA"), ("jerarquia_via", "JERARQUIA_DE_LA_VIA")]:
        s[nuevo] = _texto(raw[viejo].astype("string")).replace({"ND": pd.NA, "0": pd.NA})
    s["via_estatal"] = s["ubicacion_via"].notna()
    anotar("7. Vías", "Registros sin datos de vía ('ND' o 0): ocurren fuera de la red vial estatal (no aplica)",
           (~s["via_estatal"]).sum(), n)

    # Paso 8 - vehiculos
    mapa_veh = {"AUTOMOVIL": "automovil", "BICICLETA": "bicicleta", "BUS": "bus", "CAMION": "camion",
                "CAMIONETA": "camioneta", "EMERGENCIAS": "emergencias", "ESPECIAL": "especial",
                "FURGONETA": "furgoneta", "MOTOCICLETA": "motocicleta", "NO_IDENTIFICADO": "no_identificado",
                "SCOOTER_ELECTRICO": "scooter", "TRICIMOTO": "tricimoto", "VEHICULO_DEPORTIVO_UTILITARIO": "suv"}
    for viejo, nuevo in mapa_veh.items():
        s["n_" + nuevo] = raw[viejo].astype(int)
    s["n_vehiculos"] = raw["SUMA_DE_VEHICULOS"].astype(int)
    anotar("8. Vehículos", "Registros donde SUMA_DE_VEHICULOS != suma de columnas por tipo",
           (s[["n_" + v for v in mapa_veh.values()]].sum(axis=1) != s["n_vehiculos"]).sum(), n)
    serv = pd.concat([_texto(raw[f"SERVICIO_{i}"]) for i in range(1, N_VEHICULOS + 1)], axis=1)
    s["transporte_publico"] = serv.eq("PÚBLICO").any(axis=1)

    # Paso 9 - victimas y validacion cruzada con participantes
    s["lesionados"] = raw["LESIONADOS"].astype(int)
    s["fallecidos"] = raw["FALLECIDOS"].astype(int)
    cond = pd.concat([_texto(raw[f"CONDICION_{i}"]) for i in range(1, N_PARTICIPANTES + 1)], axis=1)
    ok = ((cond.eq("FALLECIDO").sum(axis=1) == s["fallecidos"]) &
          (cond.eq("LESIONADO").sum(axis=1) == s["lesionados"]))
    anotar("9. Validación", "Siniestros cuyas víctimas (FALLECIDOS/LESIONADOS) NO coinciden con las condiciones "
                            "de los participantes", (~ok).sum(), n)
    anotar("9. Validación", "Siniestros con >10 lesionados (atípicos reales; se conservan y se marcan)",
           (s["lesionados"] > 10).sum(), n)

    # ---------------- Features (metricas nuevas) ----------------
    s["n_victimas"] = s["fallecidos"] + s["lesionados"]
    s["severidad"] = np.select([s["fallecidos"] > 0, s["lesionados"] > 0], ["FATAL", "CON LESIONADOS"], "SIN VÍCTIMAS")
    s["severidad"] = pd.Categorical(s["severidad"], ["SIN VÍCTIMAS", "CON LESIONADOS", "FATAL"], ordered=True)
    s["fatal"] = s["fallecidos"] > 0
    s["letalidad"] = np.where(s["n_victimas"] > 0, s["fallecidos"] / s["n_victimas"].replace(0, np.nan), np.nan)
    s["severidad_ponderada"] = PESO_FALLECIDO * s["fallecidos"] + PESO_LESIONADO * s["lesionados"]
    s["franja"] = pd.cut(s["hora_num"], [-1, 5, 11, 17, 23], labels=FRANJAS).astype("object")
    s["franja"] = pd.Categorical(s["franja"], FRANJAS, ordered=True)
    s["nocturno"] = (s["hora_num"] < 6) | (s["hora_num"] >= 18)
    s["fin_semana"] = s["dia_semana"] >= 6
    s["tipo_dia"] = np.select([s["feriado"], s["fin_semana"]], ["FERIADO", "FIN DE SEMANA"], "LABORABLE")
    s["mes_nombre"] = pd.Categorical(s["mes"].map(lambda m: MESES[m - 1]), MESES, ordered=True)
    s["dia_nombre"] = pd.Categorical(s["dia_semana"].map(lambda d: DIAS[d - 1]), DIAS, ordered=True)
    s["causa_grupo"] = s["cod_causa"].map(CAUSA_GRUPO).fillna("Otras infracciones")
    s["factor_causal"] = s["cod_causa"].map(CAUSA_FACTOR).fillna("Humano")
    s["involucra_moto"] = s["n_motocicleta"] > 0
    s["solo_moto"] = s["n_motocicleta"] == s["n_vehiculos"]
    vru = s[["n_motocicleta", "n_bicicleta", "n_scooter", "n_tricimoto"]].sum(axis=1) > 0
    s["usuario_vulnerable"] = vru | s["tipo_siniestro"].eq("ATROPELLOS")
    s["solo_vehiculos_cerrados"] = s[["n_motocicleta", "n_bicicleta", "n_scooter", "n_tricimoto",
                                      "n_no_identificado"]].sum(axis=1) == 0
    s["celda_lat"] = (s["lat"] / 0.02).round() * 0.02     # cuadricula ~2 km (0.02 grados)
    s["celda_lon"] = (s["lon"] / 0.02).round() * 0.02

    # ---------------- Participantes: formato ancho -> largo ----------------
    partes = []
    for i in range(1, N_PARTICIPANTES + 1):
        t = pd.DataFrame({"sid": s["sid"], "orden": i,
                          "tipo_id": _texto(raw[f"TIPO_ID_{i}"]), "edad": raw[f"EDAD_{i}"].astype(float),
                          "sexo": _texto(raw[f"SEXO_{i}"]), "condicion": _texto(raw[f"CONDICION_{i}"]),
                          "rol": _texto(raw[f"PARTICIPANTE_{i}"]), "casco": _texto(raw[f"CASCO_{i}"]),
                          "cinturon": _texto(raw[f"CINTURON_{i}"])})
        partes.append(t[t["rol"].notna()])
    p = pd.concat(partes, ignore_index=True)
    anotar("10. Participantes", "Participantes (filas) tras pasar a formato largo", len(p), len(p))

    p["edad"] = p["edad"].where(p["edad"] >= 0)                 # -1 = sin dato
    for c in ["sexo", "condicion", "tipo_id"]:
        p[c] = p[c].replace({"NO IDENTIFICADO": pd.NA})
    p["grupo_edad"] = pd.cut(p["edad"], [-1, 11, 17, 29, 64, 200], labels=GRUPOS_EDAD).astype("object")
    p["grupo_edad"] = pd.Categorical(p["grupo_edad"], GRUPOS_EDAD, ordered=True)
    p["victima"] = p["condicion"].isin(["FALLECIDO", "LESIONADO"])
    cols = ["sid", "fecha", "hora_num", "franja", "nocturno", "mes", "dia_semana", "tipo_dia", "provincia", "canton",
            "zona", "ente_control", "tipo_siniestro", "causa_grupo", "n_vehiculos", "solo_moto",
            "solo_vehiculos_cerrados", "usuario_vulnerable"]
    p = p.merge(s[cols], on="sid", how="left")

    # ---------------- Ruido ----------------
    filas = []
    for c in CAMPOS_SIN_RUIDO:
        base = s[c]
        malos = base.isna()
        if not pd.api.types.is_numeric_dtype(base) and not pd.api.types.is_datetime64_any_dtype(base):
            malos = malos | base.astype("string").isin(["ND", "NO IDENTIFICADO"])
        filas.append({"tabla": "siniestros", "campo": c, "inutilizables": int(malos.sum()), "base": n,
                      "tipo": "ruido"})
    for c in CAMPOS_VIALES:
        filas.append({"tabla": "siniestros", "campo": c, "inutilizables": int(s[c].isna().sum()), "base": n,
                      "tipo": "no aplica"})
    for c in CAMPOS_PART:
        malos = p[c].isna()
        filas.append({"tabla": "participantes", "campo": c, "inutilizables": int(malos.sum()), "base": len(p),
                      "tipo": "ruido"})
    ruido = pd.DataFrame(filas)
    ruido["porcentaje"] = (100 * ruido["inutilizables"] / ruido["base"]).round(2)
    return s, p, pd.DataFrame(pasos), ruido


def _resumen_ruido(ruido):
    r = ruido[ruido["tipo"] == "ruido"]
    total = {}
    for tabla, g in r.groupby("tabla"):
        total[tabla] = float(round(100 * g["inutilizables"].sum() / g["base"].sum(), 2))
    tot = float(round(100 * r["inutilizables"].sum() / r["base"].sum(), 2))
    return total, tot


def reconstruir():
    raw = _leer_crudo()
    s, p, pasos, ruido = _construir(raw)
    DIR_DATOS.mkdir(exist_ok=True)
    DIR_RES.mkdir(exist_ok=True)
    s.to_parquet(DIR_DATOS / "siniestros_limpio.parquet", index=False)
    p.to_parquet(DIR_DATOS / "participantes_limpio.parquet", index=False)
    pasos.to_csv(DIR_RES / "limpieza_pasos.csv", index=False, encoding="utf-8-sig")
    ruido.to_csv(DIR_RES / "limpieza_ruido_por_campo.csv", index=False, encoding="utf-8-sig")
    return s, p, pasos, ruido


def cargar_datos():
    """Devuelve (siniestros, participantes) limpios. Usa la cache si esta al dia."""
    fs, fp = DIR_DATOS / "siniestros_limpio.parquet", DIR_DATOS / "participantes_limpio.parquet"
    vigente = fs.exists() and fp.exists() and min(fs.stat().st_mtime, fp.stat().st_mtime) > max(
        _ruta_excel().stat().st_mtime, Path(__file__).stat().st_mtime)
    if not vigente:
        print("Construyendo datos limpios (solo la primera vez, ~1 min)...")
        s, p, _, _ = reconstruir()
    else:
        s, p = pd.read_parquet(fs), pd.read_parquet(fp)
    DIR_RES.mkdir(exist_ok=True)
    return s, p


if __name__ == "__main__":
    s, p, pasos, ruido = reconstruir()
    pd.set_option("display.width", 220, "display.max_colwidth", 110, "display.max_rows", 200)
    print("\n=== PASOS DE LIMPIEZA Y TRANSFORMACIÓN ===")
    print(pasos.to_string(index=False))
    print("\n=== RUIDO POR CAMPO (celdas inutilizables) ===")
    print(ruido.to_string(index=False))
    por_tabla, total = _resumen_ruido(ruido)
    print("\nRuido por tabla (% de celdas analíticas inutilizables):", por_tabla)
    print(f"Ruido global en campos analíticos: {total} %")
    print("Registros eliminados: 0 (los marcadores se convierten a nulo y se documentan; no se descartan siniestros)")
    print(f"\nSiniestros: {s.shape} | Participantes: {p.shape}")
    print("\n=== REFERENCIAS DE LAS MÉTRICAS NUEVAS ===")
    for k, v in REFERENCIAS.items():
        print(f"- {k}: {v}")
