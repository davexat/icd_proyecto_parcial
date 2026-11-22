# Pregunta de negocio 2: feriados y fines de semana

> **Pregunta:** ¿Los feriados y los fines de semana cambian cuántos siniestros ocurren, a qué hora ocurren y qué tan graves son, frente a un día laborable?

**Técnicas:** promedio diario por tipo de día, razón contra el día laborable, porcentaje de siniestros con fallecidos, perfil horario facetado y serie diaria con media móvil.
**Verificación:** el script corre sin errores y genera 2 tablas y 2 figuras.

## 1. Qué hace el código

**Bloque 0: serie diaria.** Cuenta siniestros y fallecidos por fecha y los reindexa para incluir los días sin siniestros (se rellenan con 0). Luego clasifica cada día como `FERIADO`, `FIN DE SEMANA` o `LABORABLE`; el feriado tiene prioridad, así que un feriado en sábado cuenta como feriado.

**Bloque 1: volumen.** Promedio de siniestros y fallecidos por día según el tipo de día y la razón frente al laborable. Guarda `p02_volumen_por_tipo_dia.csv`.

**Bloque 2: gravedad.** Usa la función `gravedad()` de `utilidades.py` para obtener el porcentaje de siniestros con fallecidos por tipo de día. Guarda `p02_gravedad_por_tipo_dia.csv`.

**Bloque 3: gráfico facetado.** Tres paneles con el perfil horario (porcentaje de los siniestros del grupo en cada hora, para comparar la forma sin que influya el tamaño del grupo) y un cuarto con el porcentaje de siniestros fatales.

**Bloque 4: serie diaria.** Siniestros por día con media móvil de 7 días y los feriados sombreados.

## 2. Resultados

| Tipo de día | Días | Siniestros por día | Fallecidos por día | Razón vs laborable | % con fallecidos |
|---|---|---|---|---|---|
| Laborable | 185 | 54.7 | 5.2 | 1.00 | 8.5 % |
| Fin de semana | 70 | 82.9 | 10.3 | **1.52** | 11.0 % |
| Feriado | 18 | 72.7 | 9.8 | **1.33** | **12.0 %** |

Las víctimas por siniestro son casi iguales en los tres grupos (0.95 a 0.96).

## 3. Análisis

1. **Más siniestros.** Un día de fin de semana tiene un 52 % más de siniestros que uno laborable, y un feriado un 33 % más.
2. **Más muertes, por dos efectos.** Los fallecidos por día se duplican (5.2 a 10.3). Aumenta el número de siniestros y también la probabilidad de que sean mortales (8.5 % a 11.0 % y 12.0 %).
3. **No hay más víctimas por evento.** El promedio es de 0.95 víctimas por siniestro en cualquier tipo de día: la diferencia está en la probabilidad de muerte, no en el tamaño del evento.
4. **Cambia el horario.** En fin de semana el 24.6 % de los siniestros ocurre de 0 a 5 h, frente al 12.9 % entre semana (dato calculado aparte para sábado y domingo).

## 4. Limitaciones y advertencias

- Los feriados son solo 18 días, así que su promedio es más inestable.
- No se hizo prueba de hipótesis; con 1 308 siniestros en feriado y 10 123 en laborables la diferencia de 12.0 % contra 8.5 % es grande, pero conviene respaldarla con una prueba chi-cuadrado si el docente lo pide.
- Esta pregunta se solapa con P1 (fin de semana) y P10 (feriados críticos). Por eso se recomienda dejarla en el apéndice de la exposición.

## 5. Archivos generados

- Tablas: `p02_volumen_por_tipo_dia.csv`, `p02_gravedad_por_tipo_dia.csv`
- Figuras: `p02_perfil_horario_y_gravedad.png`, `p02_serie_diaria_feriados.png`

**Cumple de las instrucciones:** gráfico facetado (6.2), temporal (2.1) y categórico (2.2).
