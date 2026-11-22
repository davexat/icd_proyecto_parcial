# Propuesta de diapositivas: Siniestros de tránsito en Ecuador, enero-septiembre 2026

Los resultados de abajo salen de ejecutar los 10 scripts (`pregunta_01.py` a `pregunta_10.py`) con `08. BDD_Septiembre_2026_SM.xlsx`. Los gráficos y tablas se generan en `resultados/` (prefijo `pXX_`). Las cifras están redondeadas. Duración sugerida: unos 25 minutos, con una o dos diapositivas por pregunta. El guion de cada pregunta (máx. 40 s) está en `explicacion_preguntas/pregunta_NN.md`, sección "Para la exposición".

**Nivel de las técnicas:** las mismas que usan los ejemplos del curso: agrupaciones y promedios, porcentajes, índices de estacionalidad, Pareto ABC (80-15-5), correlación, z-score, heatmaps, gráficos facetados y mapas con latitud y longitud. No hay pruebas de hipótesis ni modelos.

## Estructura general

| # | Diapositiva | Contenido |
|---|---|---|
| 1 | Portada | Título, integrantes (presentan todos), paralelo |
| 2 | Contexto y objetivo | Por qué importa: 1.863 fallecidos y 14.547 lesionados en 9 meses; objetivo del EDA (sin modelos de ML) |
| 3 | El dataset | 17.236 siniestros, 374 columnas, 37.096 personas, 24 provincias, 210 cantones, 16 entes de control. Tabla con los 4 tipos de dato exigidos: **temporal** (fecha, hora), **categórico** (causa, tipo de siniestro, vehículo), **continuo** (edad, víctimas, hora decimal), **espacial** (provincia, cantón, latitud, longitud, vía) |
| 4 | Limpieza y transformación | Pasos de `limpieza_datos.py` (ver abajo) |
| 5 | Porcentaje de ruido | Gráfico de barras del % inutilizable por campo (`limpieza_ruido_por_campo.csv`) |
| 6 | Métricas nuevas y literatura | Tabla de features con su referencia (ver abajo) |
| 7-20 | Preguntas de negocio (10) | Una a dos diapositivas por pregunta, en el orden de la sección siguiente |
| 21 | Conclusiones | 5 mensajes clave |
| 22 | Recomendaciones | Acciones por actor (ANT, GAD, control) |
| 23 | Limitaciones | Calidad del registro, ausencia de población y exposición |
| 24 | Referencias | Las de abajo |

### Diapositivas 4-5: limpieza y ruido

- **Pasos:** lectura → esparsidad estructural → duplicados → fecha/hora → texto → coordenadas → vías → vehículos → validación cruzada → formato largo de participantes.
- **Ruido global en campos analíticos: 9,0 %** (siniestros 1,5 %; participantes 19,4 %). Se eliminaron 0 registros: los marcadores `ND`, `NO IDENTIFICADO` y `-1` pasan a nulo.
- Campos con más ruido: edad (43,9 % sin dato), tipo de ID (21,8 %), tipo de vehículo 1 (22,5 % "no identificado"), condición (18,4 %), sexo (12,8 %).
- Campos viales: 66,5 % es **"no aplica"** (siniestros fuera de la red vial estatal), no ruido.
- Hallazgos para 4-5 viñetas: 293 de 374 columnas con más del 95 % vacío (formato ancho de hasta 43 participantes); 5 horas guardadas como texto; 10 variantes de "colisión"; 0 coordenadas inválidas; las víctimas coinciden con las condiciones de los participantes en el 100 % de los registros.

### Diapositiva 6: métricas nuevas con referencia

| Métrica | Referencia |
|---|---|
| Víctimas, letalidad (fallecidos / víctimas) | WHO (2023); Elvik et al. (2009) |
| Severidad en 3 niveles (sin víctimas / con lesionados / fatal) | AASHTO (2010), *Highway Safety Manual* |
| Factor causal humano-vehículo-vía y 10 grupos de causa | Haddon (1968); Sabey y Taylor (1980) |
| Usuario vulnerable (moto, bici, scooter, peatón) | Peden et al. (2004); WHO (2023) |
| Celda de 2 km (puntos críticos) | Anderson (2009); Xie y Yan (2008) |
| Índice de estacionalidad | Hyndman y Athanasopoulos (2021) |

Franja horaria, fin de semana y feriado son convenciones del proyecto, sin referencia específica. El z-score de la pregunta 2 sigue el Ejemplo 1 del curso.

---

## Preguntas de negocio (en orden sugerido de exposición)

### P1. ¿En qué meses, días y horas ocurren más siniestros y cambia entre zona urbana y rural?
- **Técnicas:** conteos, índices de estacionalidad, heatmap.
- **Gráficos:** `p01_indices_estacionalidad.png` (3 paneles); `p01_heatmap_dia_hora_por_zona.png` (**heatmap facetado** urbana/rural).
- **Resultados:** domingo índice 1,38 y sábado 1,22; martes el más bajo (0,79). Horas pico 17-20 h (máximo a las 19 h, índice 1,59). Enero-abril bajo el promedio; mayo-septiembre sobre él (agosto 1,15). Pico urbano: domingo 20 h (3,4 siniestros/día); rural: domingo 19 h (2,8).
- **Conclusión:** la siniestralidad es de **tarde-noche y fin de semana**. Foco operativo: controles de viernes a domingo, 17-21 h.

### P2. ¿Qué días son críticos y qué tienen en común?
- **Técnicas:** z-score diario (como en el Ejemplo 1), correlación, calendario heatmap.
- **Gráficos:** `p02_serie_diaria_criticos.png`; `p02_calendario_heatmap.png` (**heatmap** semana × día).
- **Resultados:** 13 días críticos (4,8 %; z > 2 frente a su mismo día de la semana). El 1 de enero fue el peor (123 siniestros, 21 fallecidos, z = 4,2). Once de los 13 caen entre junio y septiembre. Entre los feriados, el 16,7 % fue crítico frente al 3,9 % del resto. Correlación diaria siniestros-fallecidos: 0,64. La distracción pesa 4 puntos más en días críticos.
- **Conclusión:** los días críticos son **eventos puntuales** (feriados y fines de semana largos) y se pueden anticipar con el calendario.

### P3. ¿Qué provincias y cantones concentran los siniestros y las muertes?
- **Técnicas:** Pareto ABC (80-15-5), Top 5, ranking por volumen y por gravedad.
- **Gráficos:** `p03_pareto_provincias.png` (**faceta** siniestros | fallecidos); `p03_mapa_burbujas_provincias.png`.
- **Resultados:** Guayas (32,7 %) y Pichincha (20,3 %) suman el 53 %; el Top 5 de provincias, el 70 %. Ocho de 24 provincias (clase A) reúnen el 80 %. En cantones, 35 de 210 (17 %) reúnen el 80 %. Las provincias pequeñas son las más graves: Esmeraldas 25 % de siniestros con fallecidos, Zamora Chinchipe 23 %, Cañar 20 %.
- **Conclusión:** hay **dos prioridades**: volumen (Guayas, Pichincha) y gravedad (provincias pequeñas, con menos casos pero más mortales).

### P4. ¿Dónde están los puntos críticos y coinciden con las muertes?
- **Técnicas:** cuadrícula de ~2 km, ranking de celdas, mapas de densidad.
- **Gráficos:** `p04_densidad_facetado.png` (**mapas facetados** por cantón, con los siniestros fatales encima); `p04_mapa_nacional_severidad.png`.
- **Resultados:** el 5 % de las celdas de 2 km concentra el 49 % de los siniestros y el 1 %, el 19 %. La celda más crítica está en Guayaquil (269 siniestros). Las 5 celdas principales reúnen el 25 % de los siniestros de Guayaquil, 17 % de Quito y 48 % de Santo Domingo.
- **Conclusión:** los siniestros se concentran en **pocas celdas**, pero esas celdas son más de volumen que de letalidad (4,5 fallecidos por cada 100 siniestros frente a 10,8 nacional); los fatales también aparecen fuera de los núcleos.

### P5. ¿Cómo influyen zona, tipo de vía y corredor?
- **Técnicas:** comparación urbano/rural, ranking de corredores, faceta por franja horaria, heatmap.
- **Gráficos:** `p05_zona_franja_corredores.png` (**faceta** urbano/rural + burbujas); `p05_heatmap_corredor_franja.png`.
- **Resultados:** rural 14,0 % de siniestros con fallecidos frente a urbano 7,1 %; red estatal 13,7 % frente a 7,5 % fuera de ella. En la madrugada rural llega al 20,2 % (urbana 10,7 %). Corredores: E40 tiene más siniestros (896) pero 10,5 % con fallecidos; E25 (645 siniestros, 125 fallecidos, 17 %) y E20 (22 %, 210 siniestros) son los más graves. Arterial (13,9 %) y colectora (13,5 %) son similares.
- **Conclusión:** la **carretera rural de madrugada** es el entorno más grave; priorizar E25 y E20.

### P6. ¿Qué causas explican los siniestros y cuáles son más graves?
- **Técnicas:** Pareto de causas, gravedad por grupo, heatmaps.
- **Gráficos:** `p06_pareto_y_burbujas.png`; `p06_heatmaps_causa_franja.png` (**heatmaps** causa × franja).
- **Resultados:** distracción 28,8 %, velocidad 19,3 %, irrespeto de señales 13,5 %; el factor humano explica el 94,5 % (vía 4,3 %, vehículo 1,2 %). Más graves (promedio nacional 9,6 % con fallecidos): vía y entorno 12,8 %, distracción 12,2 %, velocidad 12,0 %. Alcohol (5,8 %) e irrespeto de señales (4,8 %) quedan por debajo.
- **Conclusión:** distracción y velocidad son **frecuentes y graves** a la vez. El alcohol aparece como poco grave; puede deberse a subregistro de la causa, así que se presenta como limitación.

### P7. ¿Qué tipos de siniestro y vehículos concentran la gravedad?
- **Técnicas:** gravedad por tipo, comparación con y sin cada vehículo, heatmap.
- **Gráficos:** `p07_gravedad_tipo_por_zona.png` (**faceta** urbano/rural); `p07_heatmap_tipo_vehiculo.png`.
- **Resultados:** arrollamiento 46 % con fallecidos, pérdida de pista 22 %, choque frontal 19 %, atropello 14 %; el choque lateral es el más frecuente (4.858) pero solo 4,8 % con fallecidos. Con bus participando, 17,1 % de los siniestros son fatales (1,85 veces los que no tienen bus); motocicleta 13,4 % (1,72 veces); camión 13,3 % (1,44 veces). Con un solo vehículo, 12,3 %; con dos, 7,2 %. En zona rural, 12 de 13 tipos son más graves que en la urbana.
- **Conclusión:** frecuencia y gravedad **no coinciden**; las motos, el transporte pesado y el público son los de mayor riesgo.

### P8. ¿Qué perfil tienen las víctimas?
- **Técnicas:** letalidad por grupo, edad mediana, pirámide de población, heatmap.
- **Gráficos:** `p08_piramide_lesionados_fallecidos.png` (**faceta** lesionados | fallecidos); `p08_heatmap_rol_edad.png`.
- **Resultados:** hay 16.410 víctimas (edad conocida en el 65 %). Letalidad entre víctimas: peatón 16,0 %, conductor 13,8 %, pasajero 7,2 %. Hombres 12,7 % frente a mujeres 7,7 %; 2,8 hombres por cada mujer. Por edad: 65+ años 19,7 %, 30-64 13,9 %, 18-29 11,5 %, menores de 18 entre 8 y 9 %. Edad mediana: fallecidos 33 años, lesionados 30.
- **Conclusión:** el **peatón y el adulto mayor** son los más vulnerables; el volumen lo aportan hombres de 18 a 64 años.

### P9. ¿Cuándo, dónde y por qué ocurren los atropellos?
- **Técnicas:** comparación de porcentajes, heatmaps facetados, letalidad por edad, horario y zona.
- **Gráficos:** `p09_atropellos_heatmaps_y_edad.png` (**heatmaps facetados** urbano/rural + letalidad por edad).
- **Resultados:** 1.992 atropellos (11,6 % de los siniestros) causan el 15,5 % de los fallecidos; el 14,2 % es fatal frente al 9,0 % del resto (1,6 veces). Causas: distracción 33 %, velocidad 24 %. Letalidad del peatón: 65+ años 27 %, de noche 20 % (de día 12 %), en zona rural 24 % (urbana 13 %). El 72 % de los atropellos es urbano, pero en zona rural el 21 % es fatal frente al 11 % en la urbana. Guayas concentra 859 atropellos.
- **Conclusión:** el atropello es un problema **urbano en cantidad y rural en gravedad**; proteger cruces de 17 a 20 h y carreteras rurales de noche.

### P10. ¿Qué distingue a los siniestros de alta consecuencia (3 o más víctimas)?
- **Técnicas:** distribución de víctimas, concentración, comparación del % con y sin cada característica, top 10.
- **Gráficos:** `p10_distribucion_y_caracteristicas.png`; `p10_victimas_por_zona.png` (**faceta** urbano/rural).
- **Resultados:** 931 siniestros (5,4 %) concentran el 22,9 % de las víctimas y el 16,6 % de los fallecidos. Mayor probabilidad: choque frontal (2,4 veces), 3 o más vehículos (2,2), bus (2,0), transporte público (1,5), zona rural (1,4). Motocicleta y noche no la aumentan; el alcohol la reduce (0,8). El mayor evento: 41 lesionados en Santa Elena (19 de agosto).
- **Conclusión:** los eventos masivos están ligados al **transporte de pasajeros** y a las carreteras rurales.

---

## Conclusiones

1. La siniestralidad es de **tarde-noche y fin de semana**; los días verdaderamente críticos son puntuales y coinciden con feriados (el 1 de enero fue el peor).
2. Dos prioridades territoriales: **volumen** (Guayas, Pichincha y pocas celdas de 2 km en las ciudades) y **gravedad** (provincias pequeñas, carreteras rurales y madrugada).
3. **Distracción y velocidad** son las causas dominantes y graves; el peatón, el adulto mayor y el motociclista son los más vulnerables.
4. Los siniestros de alta consecuencia se asocian al **transporte de pasajeros**, al choque frontal y a las carreteras rurales.
5. La **calidad del registro** limita las conclusiones: 43,9 % de las personas sin edad y 22,5 % de los vehículos sin identificar, sobre todo en ATM y CTE.

## Limitaciones a mencionar

- El dataset cubre **9 meses**: no permite estacionalidad anual ni comparación con 2025.
- No hay **población ni kilómetros recorridos**, por lo que no se pueden calcular tasas per cápita.
- La severidad solo distingue fallecido/lesionado (sin lesión grave).
- Análisis exploratorio y descriptivo: **no causal** y sin pruebas de significancia.

## Referencias

- AASHTO (2010). *Highway Safety Manual* (1.ª ed.).
- Anderson, T. K. (2009). Kernel density estimation and K-means clustering to profile road accident hotspots. *Accident Analysis & Prevention*, 41(3), 359-364.
- Elvik, R., Høye, A., Vaa, T., Sørensen, M. (2009). *The Handbook of Road Safety Measures* (2.ª ed.). Emerald.
- Haddon, W. (1968). The changing approach to the epidemiology, prevention, and amelioration of trauma. *American Journal of Public Health*, 58(8).
- Hyndman, R. J., Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3.ª ed.). OTexts.
- Peden, M. et al. (2004). *World report on road traffic injury prevention*. WHO.
- Sabey, B. E., Taylor, H. (1980). The known risks we run: the highway. TRRL Supplementary Report 567.
- WHO (2023). *Global status report on road safety 2023*. ISBN 978-92-4-008651-7.
- Xie, Z., Yan, J. (2008). Kernel density estimation of traffic accidents in a network space. *Computers, Environment and Urban Systems*, 32(5), 396-406.
