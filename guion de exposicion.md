# Guion de exposición: siniestros de tránsito en Ecuador, enero a septiembre de 2026

Duración estimada: **13:50** (rango de 12:50 a 14:45 según el ritmo de cada quien) · 1 801 palabras · 3 expositores · 16 diapositivas

## 1. Cómo usar este guion

- **Texto normal** = lo que se dice. Lo que está entre **\[corchetes\]** son nombres que deben completar. Las etiquetas en negrita (*Pregunta, Cómo, Resultado, Puente*) son guía y no se leen.
- *Las frases en cursiva se pueden saltar* si van tarde (ahorran unos 40 segundos en total).
- **Orden en cada pregunta: Pregunta → Cómo → Resultado → Puente.** Primero se explica cómo se respondió (una o dos frases, en lenguaje ejecutivo) porque eso le dice al público cómo leer el gráfico; el resultado se cuenta con el gráfico ya en pantalla, y el puente conecta con la pregunta siguiente.
- **Ritmo base:** 135 palabras por minuto más 2 segundos por cambio de diapositiva. Es una estimación: léanlo en voz alta con cronómetro una vez y ajusten. Si les da más de 13:45, usen los recortes de la sección 6.
- Las cifras están redondeadas igual que en la guía de diapositivas: digan lo mismo que muestra la pantalla.

## 2. Tiempos y relojes de control

| Diap. | Sección | Expositor | Palabras | Tiempo | Reloj al terminar |
| --- | --- | --- | --- | --- | --- |
| 1 a 2 | Contexto | 1 | 84 | 0:41 | 0:41 |
| 3 | Los datos | 1 | 62 | 0:29 | 1:10 |
| 4 | Limpieza y ruido | 1 | 172 | 1:18 | 2:29 |
| 5 | Métricas nuevas | 1 | 56 | 0:26 | 2:56 |
| 6 | P1 · Cuándo | 1 | 145 | 1:06 | 4:02 |
| 7 | P2 · Días críticos | 1 | 140 | 1:04 | **5:06** |
| 8 | P3 · Provincias y cantones | 2 | 132 | 1:00 | 6:07 |
| 9 | P4 · Vehículos por provincia | 2 | 115 | 0:53 | 7:00 |
| 10 | P5 · Zona y corredores | 2 | 129 | 0:59 | 8:00 |
| 11 | P6 · Causas | 2 | 138 | 1:03 | **9:03** |
| 12 | P7 · Tipo y vehículo | 3 | 121 | 0:55 | 9:58 |
| 13 | P8 · Perfil de víctimas | 3 | 125 | 0:57 | 10:55 |
| 14 | P9 · A quién afecta | 3 | 117 | 0:54 | 11:49 |
| 15 | P10 · Alta consecuencia | 3 | 118 | 0:54 | 12:43 |
| 16 | Conclusiones | 3 | 147 | 1:07 | **13:50** |

**Por expositor:** el 1 dura 5:06, el 2 dura 3:56 y el 3 dura 4:47. Los cambios de expositor suman unos 5 a 10 segundos extra, así que el total real ronda 14:00.

**Relojes de control:** el expositor 1 debe terminar cerca de 5:05 y el 2 cerca de 9:05. Si en el cambio al expositor 3 ya van pasados de 9:00, activen los recortes. El expositor 2 tiene menos texto, así que puede dejar 2 a 3 segundos de silencio sobre cada mapa para que se lean.

## 3. Expositor 1: introducción, P1 y P2 (0:00 a 5:06)

### &#91;Diap. 1 a 2\] Contexto (0:41)

Buenas tardes. Somos el grupo #9 conformado por Bruno Romero, Darwin Diaz y mi persona, David Sandoval y les presentamos un análisis de los siniestros de tránsito en Ecuador entre enero y septiembre de 2026. 

**\[→ Diap. 2\]** Queremos describir cuándo, dónde y por qué ocurrieron los siniestros y a quién afectaron, e identificar qué variables explican mejor lo sucedido. Es un análisis retrospectivo: buscamos caracterizar los datos ya registrados, no predecir dónde ocurrirá el próximo. Planteamos diez preguntas de negocio, ordenadas en el hilo que vemos en pantalla, y cada una la resolvemos combinando varias técnicas de análisis.

### &#91;Diap. 3\] Los datos (0:29)

Trabajamos con los 17 236 siniestros registrados, uno por fila, con 1 863 fallecidos y más de 14 000 lesionados. Cada registro describe hasta 43 personas y 13 vehículos, en 374 columnas. El dataset contiene diferentes tipos de datos tales como: 
- temporales, fecha y hora; 
- categóricos, como tipo y causa; 
- continuos, como la edad; 
- y espaciales, como provincia, cantón y sus coordenadas.

### &#91;Diap. 4\] Limpieza y ruido (1:18)

Antes de analizar, limpiamos los datos en cuatro pasos. 

Primero, estructura: el Excel tenía una fila por siniestro, con la edad y el sexo de cada persona repartidos en muchas columnas; lo reorganizamos con una fila por persona, lo que dio 37 096 filas en total. 

Segundo, fechas, horas y texto: corregimos horas escritas como texto y unificamos su formato. 

Tercero, validación: no encontramos filas repetidas, coordenadas fuera de Ecuador ni víctimas que no coincidieran con las personas. 

Cuarto, datos desconocidos: donde el dataset decía «no identificado» o «ND», o ponía −1 en la edad, dejamos el dato vacío para que no cuente como un valor real. No eliminamos ningún siniestro. 

**\[→ Ruido\]** Ruido son los datos que faltan y no se pueden usar: 9 % de los campos que analizamos. Los más afectados son la edad, que falta en 44 %, el tipo de vehículo, el tipo de identificación, la condición de la víctima y el sexo. Como el análisis es retrospectivo, no rellenamos esos vacíos: usamos solo lo que realmente se registró.

### &#91;Diap. 5\] Métricas nuevas (0:26)

A partir de lo registrado, creamos métricas nuevas apoyadas en literatura. La definición de víctima y letalidad, de la OMS. La agrupación de causas en factor humano, vehículo y vía, de Haddon y de Sabey y Taylor. Y el índice de estacionalidad, de Hyndman. Con esto, pasamos a las preguntas.

### &#91;Diap. 6\] P1 · Cuándo ocurren (1:06)

**Pregunta:** Pregunta uno: ¿cuándo ocurren los siniestros, y cambia entre ciudad y campo?

**Cómo:** Calculamos un índice de estacionalidad: los siniestros de cada mes, día u hora divididos entre su promedio; si pasa de uno, es temporada alta. Lo mostramos primero a nivel nacional y luego separado por zona urbana y rural.

**Resultado:** El domingo es el día más cargado, con índice de casi 1.4, y el pico está entre las 17 y las 20 horas, con máximo a las 19.
(sig) En ambas zonas es igual, pero el campo es más extremo: el domingo llega a 1.50 contra 1.31 en la ciudad, y a las 19 horas, a 1.86 contra 1.43. La ciudad es más pareja y tiene más actividad de madrugada. *Un matiz: son solo nueve meses, así que el alza de enero a agosto no prueba una estacionalidad anual.*

**Puente:** ¿Hay días que se salen incluso de este patrón?

### &#91;Diap. 7\] P2 · Días críticos (1:04)

**Pregunta:** Pregunta dos: ¿qué días fueron críticos y qué tienen en común?

**Cómo:** Medimos cuántas desviaciones se aparta cada día de lo habitual para su día de la semana: cero es normal y más de dos es crítico. Luego comparamos esos días con todos los demás.

**Resultado:** Cada punto es un día y los rojos son los críticos: 13 de 273. El más extremo es el 1 de enero, con 123 siniestros y 21 fallecidos. En común: 11 de los 13 caen entre junio y septiembre; casi uno de cada cuatro es feriado, frente a uno de cada quince en general; y la distracción domina en 77 %, contra 58 %. El día de la semana no los distingue. *Un matiz: el nivel diario sube de enero a agosto, lo que refuerza esos meses.*

**Puente:** Ya sabemos cuándo. Mi compañero \[nombre\] les cuenta dónde.

## 4. Expositor 2: P3, P4, P5 y P6 (5:06 a 9:03)

### &#91;Diap. 8\] P3 · Provincias y cantones (1:00)

**Pregunta:** Pregunta tres: ¿qué provincias y cantones concentran más siniestros y muertes?

**Cómo:** Aplicamos una clasificación Pareto ABC, que ordena las provincias y las suma hasta llegar al 80 %. Y comparamos dos rankings: por volumen y por gravedad, es decir, el porcentaje de siniestros con fallecidos.

**Resultado:** Ocho de las 24 provincias suman el 80 % de los siniestros, y solo Guayas y Pichincha son más de la mitad. *Por cantón, 35 de 210 bastan para el 80 %.* Pero al medir gravedad el orden cambia: Esmeraldas tiene fallecidos en el 25 % de sus siniestros, aunque es la número 16 en volumen, y le siguen Zamora Chinchipe y Cañar. El promedio nacional es 9.6 %. El ranking cambia según se mida por volumen o por gravedad.

**Puente:** ¿Y qué vehículos pesan en cada provincia?

### &#91;Diap. 9\] P4 · Vehículos por provincia (0:53)

**Pregunta:** Pregunta cuatro: ¿en qué provincias pesan más las motos, los camiones y los buses?

**Cómo:** Calculamos, para cada provincia, el porcentaje de sus siniestros que involucra cada vehículo, y lo dibujamos en tres mapas: el tamaño de la burbuja es la cantidad y el color, ese porcentaje.

**Resultado:** Las motos participan en un tercio de todos los siniestros del país, pero en Santo Domingo y Los Ríos llegan a cerca de la mitad. Los camiones destacan en Cotopaxi y Cañar, y los buses en Chimborazo e Imbabura. Por cantidad mandan Guayas y Pichincha, porque tienen más siniestros en total. *Esto muestra dónde participa cada vehículo, no cuál es más peligroso.*

**Puente:** ¿Y entre la ciudad y la carretera?

### &#91;Diap. 10\] P5 · Zona y corredores (0:59)

**Pregunta:** Pregunta cinco: ¿cómo influyen la zona y los corredores viales?

**Cómo:** Comparamos urbano contra rural con barras agrupadas por cada franja horaria del día, y ubicamos los corredores de la red estatal en burbujas, donde el tamaño es el número de fallecidos.

**Resultado:** La zona rural es el doble de grave: 14 % de siniestros con fallecidos, contra 7 % en la urbana. *La jerarquía de la vía casi no importa: arterial y colectora andan en 14 % y 13 %.* La madrugada es la franja más letal en ambas zonas, y en la rural llega a uno de cada cinco. Entre corredores, la E40 tiene más siniestros pero 10.5 % fatales; la E25, con 17 %, y la E20, con 22 %, fueron más letales.

**Puente:** Y ahora, ¿por qué ocurren?

### &#91;Diap. 11\] P6 · Causas (1:03)

**Pregunta:** Pregunta seis: ¿qué causas explican los siniestros y cuáles son más graves?

**Cómo:** Hicimos un Pareto de las 26 causas, agrupadas en factor humano, vehículo y vía, y un gráfico de burbujas que cruza frecuencia con gravedad.

**Resultado:** El 94.5 % es factor humano. La distracción, con 28.8 %, y el exceso de velocidad, con 19.3 %, explican casi la mitad, y además están entre las más graves: unos 12 % de sus siniestros tiene fallecidos, sobre el 9.6 % promedio. *Irrespetar señales es la tercera causa, pero de las menos letales.* De madrugada pesan más la velocidad, el alcohol y la fatiga. Un aviso: el alcohol sale poco letal, 5.8 %, pero creemos que es un sesgo del registro, no que sea inofensivo.

**Puente:** Con cuándo, dónde y por qué claros, \[nombre\] continúa con qué siniestros y a quiénes afectan.

## 5. Expositor 3: P7, P8, P9, P10 y conclusiones (9:03 a 13:50)

### &#91;Diap. 12\] P7 · Tipo de siniestro y vehículo (0:55)

**Pregunta:** Pregunta siete: ¿qué tipos de siniestro y qué vehículos son más graves?

**Cómo:** Calculamos el porcentaje de siniestros con fallecidos por tipo, en ciudad y campo, y por vehículo, con y sin él.

**Resultado:** Los arrollamientos son los más graves: 37 % de siniestros con fallecidos en la ciudad y 59 % en el campo; siguen pérdida de pista y choque frontal. El choque lateral es el más frecuente, pero de los menos graves. En casi todos los tipos el campo es peor: en atropellos, 11 % contra 21 %. Si participa un bus, el siniestro es 1.85 veces más fatal; con una moto, 1.72. *Son asociaciones, no prueba de que el vehículo cause la gravedad.*

**Puente:** Pasemos de los vehículos a las personas.

### &#91;Diap. 13\] P8 · Perfil de las víctimas (0:57)

**Pregunta:** Pregunta ocho: ¿qué perfil tienen las víctimas y quiénes son más vulnerables?

**Cómo:** Medimos la letalidad, que es fallecidos sobre fallecidos más lesionados, por sexo, edad y rol, con una pirámide, barras y un mapa de calor.

**Resultado:** Por cada mujer víctima hay 2.8 hombres, y desde los 12 años ellos mueren más: su letalidad llega a 22 % desde los 65 años, contra 16 % en ellas. El mapa de calor muestra de dónde viene el aumento: en el peatón sube de 6 % en adolescentes a 27 % desde los 65 años, y en el conductor casi no cambia. Un límite: falta la edad en más de un tercio de las víctimas.

**Puente:** Ahora cruzamos a estas personas con el tipo de siniestro y el vehículo.

### &#91;Diap. 14\] P9 · A quién afecta cada siniestro (0:54)

**Pregunta:** Pregunta nueve: ¿qué tipos de siniestro y qué vehículos afectan a quién?

**Cómo:** Vemos, entre las víctimas, qué porcentaje es conductor, pasajero, peatón, hombre, menor de 18 o de 65 años o más, por tipo de siniestro y por vehículo. La primera fila es el total.

**Resultado:** Cada siniestro golpea a alguien distinto. En los atropellos, 84 % son peatones y casi una de cada cinco víctimas tiene 65 años o más, contra 6 % en general. En la caída de pasajero, 97 % son pasajeros. Con una moto, 61 % son conductores y 80 % hombres; con un bus, 65 % son pasajeros y 10 % tiene 65 años o más.

**Puente:** Y por último, los eventos más graves.

### &#91;Diap. 15\] P10 · Alta consecuencia (0:54)

**Pregunta:** Pregunta diez: ¿qué características tienen los siniestros de alta consecuencia, con tres o más víctimas?

**Cómo:** Medimos cuánto concentran esos siniestros y comparamos, con y sin cada característica, su frecuencia y las personas por siniestro.

**Resultado:** Solo el 5.4 % de los siniestros tiene tres o más víctimas, pero reúne el 23 % de las víctimas. Son más frecuentes con choque frontal, 2.4 veces; tres o más vehículos, 2.2; y bus, 2. Y son los que involucran más gente: de 2.6 a 3.6 personas por siniestro, contra 2 en el resto. Moto y alcohol no la elevan ni tienen más gente: la alta consecuencia depende de cuántos van expuestos. El peor dejó 41 lesionados en Santa Elena.

**Puente:** Con esto, cerramos.

### &#91;Diap. 16\] Conclusiones (1:07)

Para cerrar. Cuándo: fines de semana, entre las 17 y las 20 horas, y feriados. Dónde: las motos, los camiones y los buses destacan cada uno en provincias distintas; el volumen está en Guayas y Pichincha, pero la gravedad en provincias pequeñas, zonas rurales y madrugadas. Por qué: 94.5 % es factor humano, sobre todo distracción y velocidad. A quién: los hombres, casi tres de cada cuatro víctimas, y los peatones mayores, los más vulnerables; cada siniestro golpea a alguien distinto. Choques frontales y buses producen los eventos con más víctimas. En conjunto, las diferencias más marcadas en la gravedad aparecen según la zona, la hora, el tipo de siniestro y el rol de la víctima. Como límites, el análisis es descriptivo y retrospectivo: caracteriza lo que ya ocurrió, no predice dónde ocurrirá, y la calidad del registro varía entre entes. Gracias, quedamos atentos a sus preguntas.

## 6. Si van tarde o si sobra tiempo

**Recortes, en este orden:**

1. Saltar las 7 frases en cursiva (matiz de P1, matiz de P2, cantones de P3, alcance de P4, jerarquía de P5, señales de P6 y asociaciones de P7): ahorra unos 40 segundos. El matiz de P1 (solo nueve meses) conviene tenerlo como respuesta preparada si preguntan por el aumento mensual.
2. En la diapositiva 4, nombrar solo los cuatro pasos sin el detalle de cada uno: ahorra unos 55 segundos.

**Si sobra tiempo:** no agreguen preguntas nuevas. Usen esos segundos para señalar con el puntero el punto del gráfico que mencionan (el domingo y las 19 h, el 1 de enero, Santo Domingo en el mapa de motos) y para dejar un silencio breve tras cada cambio de diapositiva.

**Consejos de ritmo:** no lean la diapositiva; digan las cifras redondeadas como están escritas; en el cambio de expositor, el que termina dice el nombre del siguiente y el que empieza retoma con la pregunta, sin agradecer ni resumir.
