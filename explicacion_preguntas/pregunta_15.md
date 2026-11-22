# Pregunta de negocio 15 (adicional): siniestros de alta consecuencia

> **Pregunta:** ¿Qué características tienen los siniestros de alta consecuencia (3 o más víctimas) y qué tan concentradas están las víctimas en pocos eventos?

**Técnicas:** distribución de víctimas por siniestro, porcentaje de víctimas que concentran los siniestros de alta consecuencia, comparación del % de alta consecuencia con y sin cada característica, top 10 de siniestros y gráfico facetado por zona.
**Feature nueva usada:** `n_victimas` (lesionados + fallecidos; WHO, 2023).
**Verificación:** el script corre sin errores y genera 2 tablas y 2 figuras.

## 1. Qué hace el código

**Bloque 0: definición.** Un siniestro es de "alta consecuencia" si `n_victimas >= 3` (la constante `UMBRAL`).

**Bloque 1: distribución y concentración.** Promedio, máximo y percentil 99 de víctimas por siniestro, y qué parte de las víctimas y de los fallecidos concentran los siniestros de alta consecuencia.

**Bloque 2: características asociadas.** Para 14 características (bus, camión, moto, 3 o más vehículos, zona rural, noche, fin de semana, causa, tipo de siniestro, etc.) compara el % de siniestros de alta consecuencia *con* la característica frente a *sin* ella y calcula la razón ("veces más probable"). Guarda `p15_caracteristicas_alta_consecuencia.csv`.

**Bloque 3: Top 10.** Los 10 siniestros con más víctimas. Guarda `p15_top10_siniestros.csv`.

**Bloque 4: gráficos.** Histograma de víctimas por siniestro (escala logarítmica, 12 = 12 o más), barras horizontales con la razón de probabilidad y una figura facetada urbano / rural con la distribución en porcentaje.

## 2. Resultados

- Promedio: **0.95 víctimas por siniestro**; máximo 41; percentil 99 = 5.
- **931 siniestros (5.4 %) tienen 3 o más víctimas** y concentran el **22.9 % de las víctimas** y el **16.6 % de los fallecidos**.

| Característica | % alta consecuencia (con) | (sin) | Veces más probable |
|---|---|---|---|
| Choque frontal | 11.9 | 4.9 | **2.41** |
| 3 o más vehículos | 11.3 | 5.1 | **2.23** |
| Participa un bus | 10.3 | 5.1 | **2.01** |
| Transporte público | 7.7 | 5.1 | 1.53 |
| Red vial estatal | 6.8 | 4.7 | 1.44 |
| Zona rural | 6.7 | 4.7 | 1.43 |
| Participa un camión | 7.0 | 5.2 | 1.33 |
| Exceso de velocidad | 5.7 | 5.3 | 1.07 |
| Horario nocturno | 5.4 | 5.4 | 1.01 |
| Participa una motocicleta | 5.3 | 5.5 | 0.97 |
| Causa: alcohol / sustancias | 4.5 | 5.5 | 0.82 |

- Siniestro más grave: **41 lesionados** en un estrellamiento en Santa Elena (19 de agosto). Le siguen un choque frontal en Santa Elena (34 lesionados y 4 fallecidos, 12 de abril) y una pérdida de carril en Cuenca (27 lesionados y 2 fallecidos).
- La proporción de alta consecuencia es de 6.7 % en la zona rural y 4.7 % en la urbana.

## 3. Análisis

1. **Las víctimas están concentradas.** Algo más de 1 de cada 20 siniestros explica casi 1 de cada 4 víctimas.
2. **La clave es la cantidad de personas expuestas por evento.** Lo que más aumenta la probabilidad de alta consecuencia es lo que implica *muchos ocupantes*: el bus (2.0 veces), el transporte público (1.5), los siniestros con 3 o más vehículos (2.2) y el choque frontal (2.4), que suele implicar un impacto de gran energía (interpretación: el dataset no mide velocidad).
3. **Variables que no aparecen como se esperaría.** Moto (0.97) y alcohol (0.82) no elevan la probabilidad de alta consecuencia: sus siniestros afectan a pocas personas cada vez (el motociclista y su acompañante), aunque sean letales (ver P5 y P6). Alta consecuencia y alta letalidad son conceptos distintos.
4. **Rural y vía estatal** aumentan la probabilidad en torno a 1.4 veces, en línea con lo visto en P9.

## 4. Limitaciones y advertencias

- El umbral de 3 víctimas es una decisión del equipo; con otro umbral las razones cambiarían.
- Las razones comparan con y sin cada característica de forma aislada; no controlan que varias se solapen (por ejemplo, bus y transporte público, o choque frontal y rural).
- Los 18 siniestros con más de 10 lesionados son atípicos reales y se conservaron; influyen en la cola de la distribución.

## 5. Archivos generados

- Tablas: `p15_caracteristicas_alta_consecuencia.csv`, `p15_top10_siniestros.csv`
- Figuras: `p15_distribucion_y_caracteristicas.png`, `p15_victimas_por_zona.png`

**Cumple de las instrucciones:** feature con referencia (punto 4), gráfico facetado (6.2), escalas logarítmicas rotuladas (6.4).
