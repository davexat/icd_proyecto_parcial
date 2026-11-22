# Pregunta de negocio 14 (adicional): atropellos

> **Pregunta:** ¿Cuándo, dónde y por qué causas ocurren los atropellos, y qué peatones tienen mayor probabilidad de morir?

**Técnicas:** comparación del % de siniestros fatales (atropellos vs resto), heatmaps facetados día × hora por zona, ranking de provincias y causas, y letalidad del peatón por edad, horario y zona.
**Verificación:** el script corre sin errores y genera 2 tablas y 1 figura.

## 1. Qué hace el código

**Bloque 0: selección.** `at` son los siniestros de tipo "ATROPELLOS". `ped` son los peatones víctimas (lesionados o fallecidos) de la tabla de participantes.

**Bloque 1: dimensión del problema.** Peso de los atropellos en los siniestros y en los fallecidos, comparación de su % de fatales contra el resto y letalidad del peatón.

**Bloque 2: cuándo y dónde.** Peso del atropello por franja horaria y ranking de provincias (cantidad, % fatales y % que representan dentro de los siniestros de la provincia). Guarda `p14_atropellos_por_provincia.csv`.

**Bloque 3: causas.** Las 6 causas más frecuentes de los atropellos, con su % y su % fatal.

**Bloque 4: perfil del peatón.** Letalidad por grupo de edad, por horario (noche = 18 a 05 h) y por zona. Guarda `p14_letalidad_peaton_edad.csv`.

**Bloque 5: gráficos.** Dos heatmaps día × hora (zona urbana y rural, con escala común y normalizados por días calendario) y un gráfico de barras con la letalidad del peatón por edad.

## 2. Resultados

- Atropellos: **1 992 (11.6 % de los siniestros)** con **289 fallecidos (15.5 % de todos los fallecidos)**.
- % de siniestros fatales: atropellos **14.2 %** vs resto 9.0 % (**1.6 veces**).
- Peatones víctimas: 2 345, con letalidad de **15.9 %**.
- Peso del atropello por franja: madrugada 5.9 %, mañana 11.4 %, tarde 12.9 %, **noche 13.6 %**.

**Provincias:** Guayas 859 atropellos (15.2 % de sus siniestros), Pichincha 338 (9.6 %), Tungurahua 132, Santo Domingo 119, Manabí 77 (23.4 % fatales), Los Ríos 45 (22.2 %), El Oro 45 (20.0 %).

**Causas de los atropellos:**

| Causa | % | % fatales |
|---|---|---|
| Conducir desatento a las condiciones de tránsito | 33.1 | 16.1 |
| Superar los límites de velocidad | 23.8 | 13.1 |
| No ceder el paso al peatón | 14.0 | 8.3 |
| Peatón que cruza sin respetar la señalización | 10.8 | 12.0 |
| No transitar por las aceras o zonas de seguridad | 6.2 | **19.5** |

**Letalidad del peatón:** 0-11 años 9.3 %, 12-17 6.2 %, 18-29 13.7 %, 30-64 **20.9 %**, 65+ **27.1 %**; noche 20.1 % vs día 12.4 %; rural 24.3 % vs urbana 12.8 %.

**Heatmaps:** el pico urbano es el viernes entre las 20:00 y las 20:59 (25 atropellos sumando todos los viernes) y el rural el domingo entre las 19:00 y las 19:59 (22). Las horas 17 a 21 (de 17:00 a 21:59) reúnen cerca del 39 % de los atropellos en ambas zonas.

## 3. Análisis

1. **El atropello es un problema desproporcionado:** 1 de cada 9 siniestros pero 1 de cada 6.5 muertes, y es 1.6 veces más letal que el resto.
2. **Ocurre al anochecer.** Su peso crece del 5.9 % en la madrugada al 13.6 % en la noche, y las horas 17 a 21 (17:00 a 21:59) concentran casi el 40 % de los casos, un tramo que coincide con la salida del trabajo y con menor visibilidad.
3. **Las causas dominantes son del conductor** (desatención y velocidad suman 57 %), aunque en 1 de cada 10 atropellos el peatón cruza sin respetar la señalización.
4. **La probabilidad de morir sube con la edad, la noche y la zona rural**: el peatón de 65 años o más tiene 27.1 % de letalidad, y en zona rural la letalidad se duplica respecto a la urbana (24.3 % vs 12.8 %). Estos tres factores se pueden combinar para priorizar intervenciones (cruces rurales, iluminación, límites de velocidad).
5. **Provincias:** Guayas y Pichincha concentran el volumen, pero la letalidad es mayor en provincias como Manabí, Los Ríos y El Oro.

## 4. Limitaciones y advertencias

- La letalidad por edad usa solo peatones con edad registrada (ver sesgo en P13).
- La feature `usuario_vulnerable`, creada en la limpieza, no se usa en este script; aquí se filtra directamente por rol "PEATÓN". Si se presenta como feature, convendría aplicarla (por ejemplo, para ampliar el análisis a motociclistas y ciclistas).
- El pico urbano/rural de los heatmaps se refiere a una celda día × hora con pocos casos; es orientativo.

## 5. Archivos generados

- Tablas: `p14_atropellos_por_provincia.csv`, `p14_letalidad_peaton_edad.csv`
- Figura: `p14_atropellos_heatmaps_y_edad.png`

**Cumple de las instrucciones:** gráfico facetado (6.2), heatmap (6.3), datos temporales, espaciales y continuos.
