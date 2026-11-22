# Pregunta de negocio 1: ¿cuándo ocurren los siniestros?

> **Pregunta:** ¿En qué meses, días de la semana y horas ocurren más siniestros, y ese patrón cambia entre zona urbana y rural?

**Script:** `pregunta_01.py`
**Técnicas:** conteos normalizados por días de calendario, índices de estacionalidad (valor / promedio), gráfico de barras y heatmap día × hora facetado por zona.
**Feature nueva usada:** índice de estacionalidad (Hyndman y Athanasopoulos, 2021).

## 1. Qué hace el código

**Bloque 0: carga y calendario.** Carga los siniestros limpios y construye `dias_cal`, una serie con *todos* los días del periodo (1 ene a 30 sep, 273 días). Sirve para dividir los conteos entre el número de días que tiene cada mes o cada día de la semana, de modo que un mes de 31 días no "gane" a uno de 28 solo por tener más días.

**Bloque 1: índices de estacionalidad.** Para cada mes y día de la semana calcula siniestros por día calendario y lo divide entre el promedio de todos los meses (o días). Un índice mayor a 1 indica temporada alta; menor a 1, baja. Para la hora no se normaliza, porque todas las horas aparecen el mismo número de veces. Imprime las horas con índice mayor a 1.3 y guarda `p01_indices.csv`.

**Bloque 2: gráfico de índices.** Tres paneles de barras (mes, día, hora). Las barras con índice mayor a 1 van en naranja y se dibuja una línea en 1.

**Bloque 3: heatmaps por zona.** Para urbana y rural arma una matriz día de la semana × hora con los siniestros por día calendario, dividiendo cada fila entre el número de ese día en el periodo. Ambos heatmaps comparten la misma escala (`vmax` común) para que los colores sean comparables. Al final imprime el pico de cada zona.

## 2. Para la exposición (máx. 40 s)

> Este heatmap cruza el día de la semana con la hora; cada celda es el promedio de siniestros por día calendario y las dos zonas comparten escala. Lo más oscuro está en el domingo entre las 19 y las 20 h, tanto en la zona urbana como en la rural. Las barras de índices lo confirman: el domingo está 38 % sobre el promedio y martes y miércoles, 20 % por debajo. Así se responde la pregunta: los siniestros se concentran en fin de semana y al anochecer, y el patrón es parecido en ambas zonas.

*Figura a mostrar:* `p01_heatmap_dia_hora_por_zona.png` (apoyo: `p01_indices_estacionalidad.png`). Unas 85 palabras, cerca de 35 s a ritmo normal.

## 3. Resultados

| Dimensión | Valores destacados |
|---|---|
| Mes | enero 0.82 · febrero 0.86 · marzo 0.86 · abril 0.96 · mayo 1.08 · junio 1.08 · julio 1.12 · **agosto 1.15** · septiembre 1.09 |
| Día | martes 0.79 · miércoles 0.80 · lunes 0.88 · jueves 0.90 · viernes 1.02 · **sábado 1.22** · **domingo 1.38** |
| Hora | pico entre las **17 y 20 h** (índices 1.37, 1.36, **1.59**, 1.36); mínimo de madrugada (3 h: 0.63) |

- Pico urbano: **domingo a las 20 h** (3.41 siniestros por día calendario). Pico rural: **domingo a las 19 h** (2.79).
- Sábado y domingo concentran el **37.2 %** de los siniestros (serían 28.6 % si se repartieran parejo).
- En la zona urbana, la madrugada (0 a 5 h) del domingo promedia 2.65 siniestros por hora y por día; de lunes a jueves, 0.69.
- Entre sábado y domingo, el 24.6 % de los siniestros ocurre de 0 a 5 h; entre semana, el 12.9 %.

## 4. Análisis

1. **El fin de semana pesa más que cualquier mes.** El domingo es el día con más siniestros (38 % sobre el promedio) y martes y miércoles son los más bajos (cerca de 20 % bajo el promedio).
2. **Hay dos picos horarios.** Uno en la tarde-noche (17 a 20 h, con máximo a las 19 h) y otro menor a las 7 h, que probablemente coincide con la entrada al trabajo y a clases.
3. **Urbano y rural comparten el patrón** (picos el domingo entre 19 y 20 h), pero la zona urbana tiene más siniestros por hora y una madrugada de fin de semana más intensa.
4. **Tendencia creciente en el año.** El índice sube de 0.82 en enero a 1.15 en agosto.

## 5. Limitaciones y advertencias

- **Nueve meses no alcanzan para hablar de estacionalidad anual.** No hay octubre a diciembre ni un segundo año, así que el patrón mensual mezcla estacionalidad y tendencia.
- **El alza de mayo a agosto viene casi toda de dos entes.** Al revisar los siniestros por mes y ente, PNE pasa de ~280 a ~650 al mes y CTE de ~285 a ~450, mientras ATM y DMQ se mantienen estables. Puede ser temporada alta real o mayor cobertura del registro; conviene decirlo como "posible" en la exposición.
- El análisis es descriptivo: no se hace una prueba de significancia entre días u horas.

## 6. Archivos generados

- Tabla: `p01_indices.csv`
- Figuras: `p01_indices_estacionalidad.png`, `p01_heatmap_dia_hora_por_zona.png`
