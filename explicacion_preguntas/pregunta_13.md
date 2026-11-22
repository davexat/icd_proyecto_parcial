# Pregunta de negocio 13 (adicional): calidad del registro por ente de control

> **Pregunta:** ¿Qué entes de control reportan información más incompleta y cuánto cambia eso las conclusiones sobre las víctimas (edad, sexo, gravedad)?

**Técnicas:** porcentaje de datos faltantes por ente y campo (heatmap), comparación de víctimas con y sin edad registrada y sensibilidad de la letalidad por grupo de edad al usar solo entes con buen registro.
**Verificación:** el script corre sin errores y genera 2 tablas y 1 figura.

## 1. Qué hace el código

**Bloque 1: faltantes por ente.** A partir de la tabla de participantes calcula, por ente de control, el % de personas sin edad, sin sexo, sin condición y sin tipo de identificación; de la tabla de siniestros toma el % con el tipo del vehículo 1 sin dato. Une todo en una tabla ordenada por número de siniestros y la guarda en `p13_faltantes_por_ente.csv`.

**Bloque 2: víctimas con y sin edad.** Compara la letalidad de las víctimas que tienen edad registrada con la de las que no, y su zona. Sirve para saber si los datos faltan "al azar".

**Bloque 3: sensibilidad.** Define "entes con buen registro" como los que tienen menos de 40 % de personas sin edad (10 entes) y repite la letalidad por grupo de edad solo con ellos, para compararla con la de todos los entes.

**Bloque 4: gráficos.** Heatmap de % faltante por ente y campo, y barras agrupadas con la letalidad por edad en las dos versiones.

## 2. Resultados

| Ente | Siniestros | % sin edad | % sin sexo | % sin condición | % vehículo 1 sin dato |
|---|---|---|---|---|---|
| PNE | 3 951 | 11.7 | 3.0 | 19.7 | 17.2 |
| CTE | 3 596 | **73.4** | 2.3 | 9.7 | 26.8 |
| ATM | 3 253 | **75.1** | 24.0 | 24.5 | **41.8** |
| DMQ | 2 874 | 19.3 | 19.2 | 19.2 | 8.0 |
| MSD | 854 | **51.2** | 26.9 | 30.3 | 28.6 |
| MRI | 196 | **50.6** | 31.2 | 23.4 | 15.3 |

Entes con más del 50 % de personas sin edad: **CTE, ATM, MSD y MRI**. CTE y ATM reúnen el 40 % de los siniestros del país.

**Víctimas con y sin edad:**

| | Víctimas | Letalidad |
|---|---|---|
| Con edad | 10 703 | **12.9 %** |
| Sin edad | 5 707 | 8.5 % |

**Letalidad por grupo de edad, todos los entes vs entes con buen registro:**

| Grupo | Todos | Buen registro |
|---|---|---|
| 0-11 | 9.4 | 12.9 |
| 12-17 | 8.4 | 9.4 |
| 18-29 | 11.5 | 13.6 |
| 30-64 | 13.9 | 16.4 |
| 65+ | 19.7 | 24.0 |

## 3. Análisis

1. **La calidad del registro depende mucho del ente.** PNE registra la edad casi siempre (11.7 % sin dato); CTE y ATM la omiten en tres de cada cuatro personas.
2. **Los datos no faltan al azar.** Las víctimas sin edad tienen una letalidad más baja (8.5 % vs 12.9 %), y una posible explicación es que la edad se anota más cuando la persona falleció o el caso fue grave (hipótesis; el dataset no lo confirma). Si es así, la letalidad calculada solo con víctimas con edad está algo inflada.
3. **El patrón, en cambio, es robusto.** Al filtrar a los entes con buen registro, los niveles suben unos 1 a 4 puntos, pero la forma es la misma: mínimo en 12 a 17 años y máximo en 65 o más. Las conclusiones de P7 y P14 sobre la edad se sostienen; lo que no es confiable es el valor exacto.
4. **Hay problemas más allá de la edad:** ATM no tiene el tipo de vehículo 1 en el 41.8 % de sus siniestros, lo que aporta más de un tercio de los ~3 870 registros sin ese dato (el ruido de 22 % de ese campo).

## 4. Limitaciones y advertencias

- Es una pregunta sobre *calidad de datos* más que sobre seguridad vial. Por eso se recomienda reutilizar su heatmap en la diapositiva de limpieza (punto 3 de las instrucciones) y no presentarla como pregunta aparte.
- El umbral de 40 % para "buen registro" es una decisión del equipo; con otro umbral los números cambian un poco.
- Los entes pequeños (MQE, MDU, MMI) tienen pocos registros y porcentajes inestables.

## 5. Archivos generados

- Tablas: `p13_faltantes_por_ente.csv`, `p13_sensibilidad_letalidad_edad.csv`
- Figura: `p13_faltantes_y_sensibilidad.png`

**Cumple de las instrucciones:** respalda el análisis de ruido (3.1 y 3.2), heatmap (6.3).
