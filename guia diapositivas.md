# Guía de diapositivas: qué poner en cada una y qué parte del guion le corresponde

Acompaña al documento «Guion de exposición (13:33 min)» · 16 diapositivas + apéndice oculto · numeración igual a la del guion

## 1. Regla de oro: del guion a la pantalla

Cada parte del guion tiene un lugar fijo en la diapositiva. Así el público aprende dónde mirar y nadie lee la pantalla.

| Parte del guion | Dónde va en la diapositiva |
| --- | --- |
| **Pregunta** | El **título**, con su número: «P3 · ¿Qué provincias y cantones concentran más siniestros?» |
| **Cómo** | Una **franja de 2 o 3 etiquetas** bajo el título con las técnicas (ejemplo: «Pareto ABC» · «Ranking por gravedad»). Nunca código ni párrafos |
| **Resultado** | El **gráfico**, con una flecha o círculo naranja en lo que se menciona, y **2 o 3 cifras grandes** que son las mismas que se dicen en voz alta |
| Hallazgo principal | Una **banda al pie** con una sola oración (la «frase titular» de cada diapositiva, abajo) |
| Matiz o advertencia | **Nota pequeña en gris** al pie |
| **Puente** | No se escribe: solo se dice |

## 2. Plantilla repetible para las preguntas (diapositivas 6 a 15)

1. **Arriba:** título con la pregunta (28 pt o más). Debajo, la franja de etiquetas de «Cómo lo respondimos» (18 pt).
2. **Centro:** el gráfico, lo más grande posible y recortado al panel que importa.
3. **Derecha o sobre el gráfico:** 2 o 3 cifras grandes (40 pt o más), una por idea que se dice.
4. **Pie:** banda con la frase titular en una sola línea; nota gris debajo si hay matiz.
5. **Esquina:** nombre del expositor y número de diapositiva (así el cambio de persona es evidente).
6. **Colores:** los del proyecto, azul #2a78d6 y naranja #eb6834. Resalten en naranja lo que se está diciendo.
7. **Tope de texto:** 25 palabras en pantalla, sin contar el gráfico.

Si lo anterior se mantiene igual en las 10 preguntas, el público entiende cada diapositiva en 3 segundos.

## 3. Estado de los gráficos antes de armar las diapositivas

| Gráfico | Problema | Estado |
| --- | --- | --- |
| P3 mapa de burbujas | Galápagos aplastaba el continente y las etiquetas se montaban | Hecho: ahora es un mapa de Folium con encuadre del continente (`pregunta_03.py`); usar la captura `p03_mapa_burbujas_provincias.png` |
| P5 burbujas de corredores | La línea punteada no tenía rótulo | Hecho: lleva la leyenda «Promedio de la red estatal» (`pregunta_05.py`) |
| P6 burbujas | Etiquetas ambiguas entre Distracción, Velocidad y Vía | Hecho: etiquetas separadas con líneas guía (`pregunta_06.py`) |
| P7 facetas urbano / rural | Estaban en dos paneles con ejes distintos, y el efecto de cada vehículo no se veía | Hecho: ahora son barras agrupadas urbano vs rural con el mismo eje, y un segundo panel con y sin cada vehículo (`pregunta_07.py`) |
| P8 sexo y edad | La pirámide solo muestra cantidades; la vulnerabilidad por sexo no se veía | Hecho: se añaden barras de letalidad por sexo y edad junto al mapa de calor (`pregunta_08.py`) |
| P9 y P10 | P9 hablaba de cuándo y dónde; P10 mezclaba dos gráficos sin relación | Hecho: P9 pasó a «a quién afecta» y P10 muestra concentración y exposición en una sola figura |

## 4. Diapositivas, una por una

### Diapositiva 1: Portada (expositor 1)

- **Título:** Siniestros de tránsito en Ecuador, enero a septiembre de 2026
- **Subtítulo:** ¿Cuándo, dónde, por qué y a quién afectan?
- **En pantalla:** nombres de los tres integrantes, materia y fecha.
- **Visual:** fondo azul sobrio, sin gráfico.
- **Del guion:** el saludo y «Somos \[nombres\]…» se dicen con esta diapositiva. Cambien a la 2 al decir «Queremos responder…».

### Diapositiva 2: Contexto y las 10 preguntas

- **Título:** 10 preguntas, un solo hilo
- **En pantalla:** cinco bloques en fila unidos por flechas: **Cuándo** (P1, P2) → **Dónde** (P3, P4, P5) → **Por qué** (P6) → **Qué y a quién** (P7, P8, P9) → **Consecuencias** (P10). Bajo cada bloque, el nombre de quien lo presenta (un color por expositor).
- **Frase al pie:** Objetivo: describir qué variables explican mejor lo ocurrido (análisis retrospectivo).
- **Del guion:** «cuándo, dónde y por qué ocurrieron los siniestros y a quién afectaron» son los cinco bloques; «análisis retrospectivo» es la frase al pie; «diez preguntas» es el título; «varias técnicas» es una nota pequeña («Cada pregunta usa varias técnicas»).
- **No escribir:** el párrafo completo.

### Diapositiva 3: Los datos

- **Título:** Los datos
- **En pantalla:** cuatro cifras grandes en fila: **17 236** siniestros · **374** columnas · **1 863** fallecidos · **14 547** lesionados. Debajo, cuatro tarjetas: *Temporal* (fecha, hora) · *Categórico* (tipo, causa, vehículo) · *Continuo* (edad, víctimas) · *Espacial* (provincia, cantón, latitud, longitud).
- **Del guion:** la primera oración son las cifras; la última oración son las tarjetas. «Hasta 43 personas y 13 vehículos» solo se dice.

### Diapositiva 4: Limpieza y ruido

- **Título:** Limpieza: 0 registros eliminados y 8.96 % de ruido
- **Izquierda:** cuatro cuadros numerados: **1 Estructura** (ancho → largo, 37 096 personas) · **2 Fechas, horas y texto** · **3 Validación** (duplicados, coordenadas, víctimas) · **4 Marcadores → nulo**.
- **Derecha:** barras horizontales del ruido por campo, con los cinco campos que tienen ruido: edad 43.9 %, tipo de vehículo 1 22.5 %, tipo de ID 21.8 %, condición 18.4 %, sexo 12.8 % (salen de `limpieza_ruido_por_campo.csv`). Si falta tiempo para el gráfico, tres cifras: **8.96 %** global · **1.5 %** siniestros · **19 %** personas.
- **Nota gris al pie:** Campos de vía vacíos (66 %) = «no aplica» (fuera de la red estatal), no son ruido.
- **Del guion:** cada «Primero, Segundo, Tercero, Cuarto» es un cuadro; «Así medimos el ruido…» son las cifras; la última oración es la nota al pie.

### Diapositiva 5: Métricas nuevas

- **Título:** Métricas nuevas, con respaldo en la literatura
- **En pantalla:** una tabla de tres columnas, una fila por oración del guion:

| Métrica | Referencia | Se usa en |
| --- | --- | --- |
| Número de víctimas y letalidad | OMS (2023) | P8, P9, P10 |
| Factor causal y grupo de causa | Haddon (1968); Sabey y Taylor (1980) | P6 |
| Índice de estacionalidad | Hyndman y Athanasopoulos (2021) | P1 |

- **No incluir** `severidad`, `severidad_ponderada` ni `usuario_vulnerable`: están creadas en la limpieza pero ninguna pregunta las usa, y el jurado podría preguntar dónde se aplican. Las referencias completas van en el apéndice.

### Diapositiva 6: P1 · ¿Cuándo ocurren los siniestros?

- **Etiquetas:** Índice de estacionalidad · Mes, día y hora · Urbano vs rural
- **Visual:** arriba, `p01_indices_general.png` (los tres paneles nacionales). Abajo, en tres miniaturas, `p01_indices_mes_zona.png`, `p01_indices_dia_zona.png` y `p01_indices_hora_zona.png` (azul = urbano, naranja = rural). Círculo naranja en el domingo y en el pico de las 19 h.
- **Cifras grandes:** Domingo: índice **1.38** (rural **1.50**, urbano 1.31) · Pico a las **19 h** (rural **1.86**, urbano 1.43) · Enero → agosto: **0.82 → 1.15**
- **Frase titular:** Fin de semana y tarde-noche concentran los siniestros, y el campo es más extremo que la ciudad.
- **Nota gris:** Son nueve meses: el alza de enero a agosto no prueba estacionalidad anual.
- **Del guion:** «Calculamos un índice…» son las etiquetas; «El domingo es el día más cargado…» son las cifras; «Un matiz…» es la nota gris.

### Diapositiva 7: P2 · ¿Qué días fueron críticos?

- **Etiquetas:** z-score contra el mismo día de la semana · Comparación con todos los días
- **Visual en dos pasos (misma diapositiva):** al empezar, `p02_dias_criticos_z.png` a todo el ancho (los puntos rojos son los días críticos y ya llevan su fecha). Al decir «Si los comparamos con todos los días…», se reemplaza por `p02_que_tienen_en_comun.png` (naranja = días críticos, gris = todos los días).
- **Cifras grandes:** **13 de 273** días críticos · Feriado: **23 %** vs 7 % de todos los días · Distracción: **77 %** vs 58 %
- **Frase titular:** Pocos días concentran los excesos; el 1 de enero es el extremo y casi siempre caen entre junio y septiembre.
- **Nota gris:** El nivel diario sube durante el año, lo que refuerza el peso de los meses recientes.
- **Del guion:** «Calculamos…» son las etiquetas; «Cada punto es un día…» es el primer gráfico; «¿Qué tienen en común?…» es el segundo gráfico y las cifras.

### Diapositiva 8: P3 · ¿Qué provincias y cantones concentran más siniestros y muertes?

- **Etiquetas:** Pareto ABC (80-15-5) · Ranking por volumen vs gravedad
- **Visual:** `p03_mapa_burbujas_provincias.png` corregido, a la izquierda y grande. A la derecha, dos cajas: **Por volumen**: Guayas 32.7 %, Pichincha 20.3 %. **Por gravedad** (% con fallecidos): Esmeraldas 25.3 %, Zamora Chinchipe 23.3 %, Cañar 19.5 %.
- **Cifra grande:** **8 de 24** provincias = 80 % de los siniestros
- **Frase titular:** Volumen y gravedad apuntan a provincias distintas.
- **Nota gris:** Promedio nacional: 9.6 % de siniestros con fallecidos (provincias con 100 o más siniestros).
- **Respaldo:** `p03_pareto_provincias.png` en el apéndice.

### Diapositiva 9: P4 · ¿En qué provincias pesan más las motos, los camiones y los buses?

- **Etiquetas:** Porcentaje por provincia · Mapas de burbujas · Un mapa por vehículo
- **Visual:** `p04_vehiculos_por_provincia.png` a todo el ancho (tres mapas: motocicleta, camión y bus; tamaño = siniestros con ese vehículo, color = % de los siniestros de la provincia).
- **Cifras grandes:** Motos **50 %** en Santo Domingo vs **33 %** en el país · Camiones **17 %** en Cotopaxi vs **10 %** · Buses **8 %** en Chimborazo vs **5 %**
- **Frase titular:** Cada vehículo pesa más en provincias distintas.
- **Nota gris:** Muestra dónde participa cada vehículo, no cuál es más peligroso. La escala de color es distinta en cada mapa.

### Diapositiva 10: P5 · ¿Cómo influyen la zona y los corredores viales?

- **Etiquetas:** Urbano vs rural · Gravedad por franja · Burbujas por corredor
- **Visual:** `p05_zona_franja_corredores.png` completo (barras agrupadas a la izquierda, burbujas a la derecha). Círculo en la barra «Madrugada rural 20.2 %» y en los puntos E25 y E20.
- **Cifras grandes:** Rural **14 %** vs urbana **7 %** · E25 **17 %** · E20 **22 %**
- **Frase titular:** Rural y madrugada son lo más letal; E25 y E20, los corredores más letales.
- **No escribir:** la jerarquía de la vía (arterial 13.9 % y colectora 13.5 %); solo se dice.

### Diapositiva 11: P6 · ¿Qué causas explican los siniestros y cuáles son más graves?

- **Etiquetas:** Pareto de 26 causas · Factor humano / vehículo / vía · Burbujas frecuencia vs gravedad
- **Visual:** recortar la mitad derecha de `p06_pareto_y_burbujas.png` (burbujas, versión corregida), porque el Pareto de la izquierda tiene los nombres de causa cortados. A la izquierda, tres cifras en vez del Pareto.
- **Cifras grandes:** **94.5 %** factor humano · **28.8 %** distracción · **19.3 %** velocidad
- **Frase titular:** Distracción y velocidad: casi la mitad de los siniestros y de las más graves.
- **Nota gris:** Alcohol: 5.8 % de siniestros fatales. Probable sesgo de registro (hipótesis).
- **Respaldo:** `p06_heatmaps_causa_franja.png` en el apéndice.

### Diapositiva 12: P7 · ¿Qué tipos de siniestro y vehículos son más graves?

- **Etiquetas:** % de siniestros con fallecidos · Tipo, urbano vs rural · Vehículo, con vs sin él
- **Visual:** `p07_gravedad_tipo_y_vehiculo.png` completo (a la izquierda, barras por tipo con la zona urbana y la rural; a la derecha, barras con y sin cada vehículo y las veces más fatales).
- **Cifras grandes:** Arrollamientos **37 % → 59 %** (urbano → rural) · Atropellos **11 % → 21 %** · Bus **1.85×**, moto **1.72×**
- **Frase titular:** Arrollamientos, pérdidas de pista y choques frontales son lo más grave; el campo agrava casi todos los tipos.
- **Nota gris:** Son asociaciones, no causas. Entre paréntesis, el número de siniestros de cada tipo o vehículo.

### Diapositiva 13: P8 · ¿Quiénes son las víctimas y los más vulnerables?

- **Etiquetas:** Letalidad = fallecidos / víctimas · Pirámide por condición · Sexo y edad · Rol y edad
- **Visual:** dos imágenes: la pirámide `p08_piramide_lesionados_fallecidos.png` arriba o a la izquierda (40 % del ancho) y `p08_vulnerabilidad.png` (barras por sexo y edad, y mapa de calor rol × edad) con el resto. Círculo en la celda Peatón / 65+ (27).
- **Cifras grandes:** **2.8** hombres por cada mujer · Hombres 65+: **22 %** (mujeres **16 %**) · Peatón: **6 % → 27 %**
- **Frase titular:** El aumento de la letalidad con la edad viene de los peatones.
- **Nota gris:** La edad está registrada en el 65 % de las víctimas.

### Diapositiva 14: P9 · ¿Qué tipos de siniestro y vehículos afectan a quién?

- **Etiquetas:** % de las víctimas · Rol, sexo y edad · Tipo de siniestro y vehículo
- **Visual:** `p09_a_quien_afecta.png` completo (dos mapas de calor; la primera fila de cada uno es el total). Resaltar con un círculo Atropellos / Peatón (84), Caída de pasajero / Pasajero (97), Moto / Conductor (61) y Bus / Pasajero (65).
- **Cifras grandes:** Atropellos: **84 %** peatones, **19 %** de 65+ (general 6 %) · Moto: **61 %** conductores, **80 %** hombres · Bus: **65 %** pasajeros, **10 %** de 65+
- **Frase titular:** Cada siniestro golpea a alguien distinto: atropellos a peatones, motos a sus conductores y buses a sus pasajeros.
- **Nota gris:** Las víctimas son las de los siniestros donde participa el vehículo, no solo quienes iban en él.
- **No escribir:** el resto de filas; el gráfico las muestra.

### Diapositiva 15: P10 · ¿Qué caracteriza a los siniestros de alta consecuencia?

- **Etiquetas:** Alta consecuencia = 3 o más víctimas · Con vs sin cada característica · Personas por siniestro
- **Visual:** `p10_concentracion_y_exposicion.png` completo (a la izquierda, qué parte del total son los siniestros de 3+ víctimas; en el centro, el % con y sin cada característica; a la derecha, las personas por siniestro). Marcar con un recuadro las tres primeras filas (choque frontal, 3+ vehículos, bus) y las dos últimas (moto, alcohol).
- **Cifras grandes:** **5.4 %** de los siniestros → **23 %** de las víctimas · Choque frontal **2.4×** · 3+ vehículos **2.2×** · Bus **2.0×** · Personas por siniestro: **2.6**, **3.6** y **3.0** contra 2
- **Frase titular:** Pocos eventos concentran muchas víctimas, y lo define cuánta gente va expuesta.
- **No escribir:** moto 0.97 y alcohol 0.82; solo se dicen.

### Diapositiva 16: Conclusiones

- **Título:** Conclusiones
- **En pantalla:** cuatro columnas con un ícono, una cifra y máximo 10 palabras cada una:
  - **Cuándo:** fines de semana, 17 a 20 h, feriados
  - **Dónde:** cada vehículo, en provincias distintas; gravedad en zona rural y madrugada
  - **Por qué:** 94.5 % factor humano: distracción y velocidad
  - **A quién:** peatón mayor, nocturno y rural; choque frontal y buses
- **Banda «En conjunto»:** las diferencias más marcadas en gravedad aparecen según la zona, la hora, el tipo de siniestro y el rol de la víctima.
- **Pie gris:** Límites: análisis descriptivo y retrospectivo, no causal ni predictivo · ruido 8.96 % · cobertura del registro variable por ente.
- **Visual:** sin gráfico. Cada columna corresponde a una oración de las conclusiones del guion, en el mismo orden; la banda es la oración «En conjunto».

## 5. Apéndice oculto (para la ronda de preguntas)

- **Respaldos de las diapositivas:** Pareto de provincias de P3, heatmap causa × franja de P6, heatmap tipo × vehículo de P7 y heatmap corredor × franja de P5.
- **Limpieza:** tabla completa de pasos y ruido por campo.
- **Referencias completas** de las métricas nuevas (autores, año, revista o editorial).
