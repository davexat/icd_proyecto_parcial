# Guion de exposición: siniestros de tránsito en Ecuador, enero a septiembre de 2026

Duración estimada: **13:25** (rango de 12:25 a 14:20 según el ritmo de cada quien) · 1 740 palabras · 3 expositores · 16 diapositivas

## 1. Cómo usar este guion

- **Texto normal** = lo que se dice. Lo que está entre **\[corchetes\]** son nombres que deben completar. Las etiquetas en negrita (*Pregunta, Cómo, Resultado, Puente*) son guía y no se leen.
- *Las frases en cursiva se pueden saltar* si van tarde (ahorran unos 30 segundos en total).
- **Orden en cada pregunta: Pregunta → Cómo → Resultado → Puente.** Primero se explica cómo se respondió (una o dos frases, en lenguaje ejecutivo) porque eso le dice al público cómo leer el gráfico; el resultado se cuenta con el gráfico ya en pantalla, y el puente conecta con la pregunta siguiente.
- **Ritmo base:** 135 palabras por minuto más 2 segundos por cambio de diapositiva. Es una estimación: léanlo en voz alta con cronómetro una vez y ajusten. Si les da más de 13:45, usen los recortes de la sección 6.
- Las cifras están redondeadas igual que en la guía de diapositivas: digan lo mismo que muestra la pantalla.

## 2. Tiempos y relojes de control

| Diap. | Sección | Expositor | Palabras | Tiempo | Reloj al terminar |
| --- | --- | --- | --- | --- | --- |
| 1 a 2 | Contexto | 1 | 84 | 0:41 | 0:41 |
| 3 | Los datos | 1 | 60 | 0:28 | 1:10 |
| 4 | Limpieza y ruido | 1 | 126 | 0:58 | 2:08 |
| 5 | Métricas nuevas | 1 | 71 | 0:33 | 2:41 |
| 6 | P1 · Cuándo | 1 | 145 | 1:06 | 3:48 |
| 7 | P2 · Días críticos | 1 | 102 | 0:47 | **4:35** |
| 8 | P3 · Provincias y cantones | 2 | 132 | 1:00 | 5:36 |
| 9 | P4 · Puntos críticos | 2 | 115 | 0:53 | 6:29 |
| 10 | P5 · Zona y corredores | 2 | 129 | 0:59 | 7:28 |
| 11 | P6 · Causas | 2 | 138 | 1:03 | **8:31** |
| 12 | P7 · Tipo y vehículo | 3 | 124 | 0:57 | 9:28 |
| 13 | P8 · Perfil de víctimas | 3 | 134 | 1:01 | 10:30 |
| 14 | P9 · Atropellos | 3 | 130 | 0:59 | 11:30 |
| 15 | P10 · Alta consecuencia | 3 | 115 | 0:53 | 12:23 |
| 16 | Conclusiones | 3 | 135 | 1:02 | **13:25** |

**Por expositor:** el 1 dura 4:35, el 2 dura 3:56 y el 3 dura 4:53. Los cambios de expositor suman unos 5 a 10 segundos extra, así que el total real ronda 13:35.

**Relojes de control:** el expositor 1 debe terminar cerca de 4:35 y el 2 cerca de 8:30. Si en el cambio al expositor 3 ya van pasados de 9:00, activen los recortes. El expositor 2 tiene menos texto, así que puede dejar 2 a 3 segundos de silencio sobre cada mapa para que se lean.

## 3. Expositor 1: introducción, P1 y P2 (0:00 a 4:35)

### &#91;Diap. 1 a 2\] Contexto (0:41)

Buenas tardes. Somos \[nombres\] y les presentamos un análisis de los siniestros de tránsito en Ecuador entre enero y septiembre de 2026. **\[→ Diap. 2\]** Queremos describir cuándo, dónde y por qué ocurrieron los siniestros y a quién afectaron, e identificar qué variables explican mejor lo sucedido. Es un análisis retrospectivo: caracteriza los datos ya registrados, no predice dónde ocurrirá el próximo. Planteamos diez preguntas de negocio, ordenadas en ese mismo hilo, y cada una la resolvemos combinando varias técnicas de análisis, no con un solo número.

### &#91;Diap. 3\] Los datos (0:28)

Trabajamos con 17 236 siniestros, con 1 863 fallecidos y más de 14 000 lesionados. Cada registro describe hasta 43 personas y 13 vehículos, en 374 columnas. El dataset tiene los cuatro tipos de datos que pide el proyecto: temporales, como fecha y hora; categóricos, como tipo y causa; continuos, como la edad; y espaciales, como provincia, cantón y coordenadas.

### &#91;Diap. 4\] Limpieza y ruido (0:58)

La limpieza tuvo cuatro pasos. Primero, estructura: pasamos la tabla de formato ancho a largo, con una fila por persona, 37 096 en total. Segundo, fechas, horas y texto: convertimos horas guardadas como texto y unificamos mayúsculas. Tercero, validación: no hay filas duplicadas, ninguna coordenada cae fuera de Ecuador y las víctimas coinciden con los participantes. Cuarto, los marcadores como «ND» o «no identificado» pasaron a datos nulos; no eliminamos ningún registro. Así medimos el ruido: el 8.96 % de los campos analíticos no sirve. Es solo 1.5 % en siniestros, pero 19 % en personas, sobre todo porque falta la edad en el 44 %. Y los campos de vía vacíos no son ruido: significan que el siniestro ocurrió fuera de la red vial estatal.

### &#91;Diap. 5\] Métricas nuevas (0:33)

Creamos métricas nuevas apoyadas en la literatura. El número de víctimas y la letalidad, de la Organización Mundial de la Salud. La severidad en tres niveles, del Highway Safety Manual. La agrupación de causas en factor humano, vehículo y vía, de Haddon y de Sabey y Taylor. Una cuadrícula de dos kilómetros para detectar puntos críticos, de Anderson. Y un índice de estacionalidad, de Hyndman. Con esto, pasamos a las preguntas.

### &#91;Diap. 6\] P1 · Cuándo ocurren (1:06)

**Pregunta:** Pregunta uno: ¿cuándo ocurren los siniestros, y cambia entre ciudad y campo?

**Cómo:** Calculamos un índice de estacionalidad: los siniestros de cada mes, día u hora divididos entre su promedio; si pasa de uno, es temporada alta. Lo mostramos primero a nivel nacional y luego separado por zona urbana y rural.

**Resultado:** El domingo es el día más cargado, con índice 1.38, y el pico está entre las 17 y las 20 horas, con máximo a las 19. En ambas zonas es igual, pero el campo es más extremo: el domingo llega a 1.50 contra 1.31 en la ciudad, y a las 19 horas, a 1.86 contra 1.43. La ciudad es más pareja y tiene más actividad de madrugada. *Un matiz: son solo nueve meses, así que el alza de enero a agosto no prueba una estacionalidad anual.*

**Puente:** ¿Hay días que se salen incluso de este patrón?

### &#91;Diap. 7\] P2 · Días críticos (0:47)

**Pregunta:** Pregunta dos: ¿qué días fueron críticos?

**Cómo:** Estandarizamos la serie diaria con un z-score, comparando cada día contra el promedio de su mismo día de la semana, para no marcar cada domingo como crítico solo por ser domingo.

**Resultado:** De 273 días, 13 son críticos. El caso extremo es el 1 de enero, con 123 siniestros y 21 fallecidos. Uno de cada seis feriados es crítico, frente a uno de cada 26 de los demás días. Casi todos caen entre junio y septiembre, y en 10 de los 13 la causa dominante es la distracción.

**Puente:** Ya sabemos cuándo. Mi compañero \[nombre\] les cuenta dónde.

## 4. Expositor 2: P3, P4, P5 y P6 (4:35 a 8:31)

### &#91;Diap. 8\] P3 · Provincias y cantones (1:00)

**Pregunta:** Pregunta tres: ¿qué provincias y cantones concentran más siniestros y muertes?

**Cómo:** Aplicamos una clasificación Pareto ABC, que ordena las provincias y las suma hasta llegar al 80 %. Y comparamos dos rankings: por volumen y por gravedad, es decir, el porcentaje de siniestros con fallecidos.

**Resultado:** Ocho de las 24 provincias suman el 80 % de los siniestros, y solo Guayas y Pichincha son más de la mitad. *Por cantón, 35 de 210 bastan para el 80 %.* Pero al medir gravedad el orden cambia: Esmeraldas tiene fallecidos en el 25 % de sus siniestros, aunque es la número 16 en volumen, y le siguen Zamora Chinchipe y Cañar. El promedio nacional es 9.6 %. El ranking cambia según se mida por volumen o por gravedad.

**Puente:** Y dentro de las ciudades, ¿dónde exactamente?

### &#91;Diap. 9\] P4 · Puntos críticos (0:53)

**Pregunta:** Pregunta cuatro: ¿dónde están los puntos críticos?

**Cómo:** Dividimos el país en una cuadrícula de dos por dos kilómetros, contamos siniestros por celda y dibujamos mapas de densidad de Guayaquil, Quito y Santo Domingo, con los siniestros con fallecidos en naranja.

**Resultado:** De 2 860 celdas, el 5 % más activo concentra casi la mitad de los siniestros, y siete de las diez principales están en Guayaquil. Guayaquil tiene un núcleo muy denso, Santo Domingo es la más concentrada y Quito la más dispersa, en una franja norte-sur. Un detalle clave: esas diez celdas tienen 4.5 fallecidos por cada 100 siniestros, frente a 10.8 en el país. Los puntos críticos concentran volumen, no letalidad.

**Puente:** ¿Y en carretera?

### &#91;Diap. 10\] P5 · Zona y corredores (0:59)

**Pregunta:** Pregunta cinco: ¿cómo influyen la zona y los corredores viales?

**Cómo:** Comparamos urbano contra rural, separamos la gravedad por franja horaria en gráficos facetados, y ubicamos los corredores de la red estatal en burbujas, donde el tamaño es el número de fallecidos.

**Resultado:** La zona rural es el doble de grave: 14 % de siniestros con fallecidos, contra 7 % en la urbana. *La jerarquía de la vía casi no importa: arterial y colectora andan en 14 % y 13 %.* La madrugada es la franja más letal en ambas zonas, y en la rural llega a uno de cada cinco. Entre corredores, la E40 tiene más siniestros pero 10.5 % fatales; la E25, con 17 %, y la E20, con 22 %, fueron más letales.

**Puente:** Y ahora, ¿por qué ocurren?

### &#91;Diap. 11\] P6 · Causas (1:03)

**Pregunta:** Pregunta seis: ¿qué causas explican los siniestros y cuáles son más graves?

**Cómo:** Hicimos un Pareto de las 26 causas, agrupadas en factor humano, vehículo y vía, y un gráfico de burbujas que cruza frecuencia con gravedad.

**Resultado:** El 94.5 % es factor humano. La distracción, con 28.8 %, y el exceso de velocidad, con 19.3 %, explican casi la mitad, y además están entre las más graves: unos 12 % de sus siniestros tiene fallecidos, sobre el 9.6 % promedio. *Irrespetar señales es la tercera causa, pero de las menos letales.* De madrugada pesan más la velocidad, el alcohol y la fatiga. Un aviso: el alcohol sale poco letal, 5.8 %, pero creemos que es un sesgo del registro, no que sea inofensivo.

**Puente:** Con cuándo, dónde y por qué claros, \[nombre\] continúa con qué siniestros y a quiénes afectan.

## 5. Expositor 3: P7, P8, P9, P10 y conclusiones (8:31 a 13:25)

### &#91;Diap. 12\] P7 · Tipo de siniestro y vehículo (0:57)

**Pregunta:** Pregunta siete: ¿qué tipos de siniestro y qué vehículos son más graves?

**Cómo:** Calculamos el porcentaje de siniestros con fallecidos por tipo, comparamos los siniestros con y sin cada vehículo, y separamos urbano y rural en gráficos facetados.

**Resultado:** Los arrollamientos son los más graves, con 46 % de siniestros fatales; siguen pérdida de pista y choque frontal, cerca de 20 %. El choque lateral es el más frecuente, pero de los menos graves. Si participa un bus, el siniestro es 1.85 veces más fatal; con una moto, 1.72. Y en la zona rural la letalidad casi se duplica: en atropellos pasa de 11 % a 21 %. *Son asociaciones, no prueba de que el vehículo cause la gravedad.*

**Puente:** Pasemos de los vehículos a las personas.

### &#91;Diap. 13\] P8 · Perfil de las víctimas (1:01)

**Pregunta:** Pregunta ocho: ¿qué perfil tienen las víctimas y quiénes son más vulnerables?

**Cómo:** Pasamos los datos a una fila por persona y medimos la letalidad, que es fallecidos sobre fallecidos más lesionados, por sexo, edad y rol, con una pirámide y un mapa de calor de rol por edad.

**Resultado:** Hay 2.8 hombres víctimas por cada mujer, y ellos mueren más: 12.7 % contra 7.7 %. Los de 65 años o más tienen 19.7 % de letalidad, el doble que los menores de 18. Pero el mapa de calor muestra que es un fenómeno de peatones: su letalidad sube de 6 % a 27 % con la edad, mientras que la del conductor casi no cambia. Un límite: la edad falta en un tercio de las víctimas.

**Puente:** Y el peatón nos lleva a la siguiente pregunta.

### &#91;Diap. 14\] P9 · Atropellos (0:59)

**Pregunta:** Pregunta nueve: ¿cuándo, dónde y por qué ocurren los atropellos?

**Cómo:** Comparamos los atropellos con el resto de siniestros, hicimos mapas de calor de día por hora para zona urbana y rural, y medimos la letalidad del peatón por edad, horario y zona.

**Resultado:** Los atropellos son el 11.6 % de los siniestros, pero el 15.5 % de las muertes. Ocurren al anochecer: entre las 17 y las 21 horas se concentra cerca del 40 %. La causa principal es conducir desatento, 33 %, y luego la velocidad, 24 %. El peatón de 65 años o más muere en 27 % de los casos; de noche, 20 % contra 12 % de día; y en zona rural, 24 % contra 13 % en la urbana.

**Puente:** Y por último, los eventos más graves.

### &#91;Diap. 15\] P10 · Alta consecuencia (0:53)

**Pregunta:** Pregunta diez: ¿qué características tienen los siniestros de alta consecuencia, con tres o más víctimas?

**Cómo:** Comparamos el porcentaje de alta consecuencia con y sin cada característica, y calculamos cuántas veces más probable es.

**Resultado:** Solo el 5.4 % de los siniestros tiene tres o más víctimas, pero reúne casi el 23 % de todas las víctimas. Los más probables son el choque frontal, 2.4 veces; los de tres o más vehículos, 2.2; y los que involucran un bus, 2. Moto y alcohol no la elevan, porque sus siniestros afectan a pocas personas por evento: la alta consecuencia depende de cuánta gente va expuesta. El peor dejó 41 lesionados en Santa Elena, en agosto.

**Puente:** Con esto, cerramos.

### &#91;Diap. 16\] Conclusiones (1:02)

Para cerrar. Cuándo: fines de semana, entre las 17 y las 20 horas, y feriados. Dónde: el 5 % de las celdas concentra casi la mitad de los siniestros; el volumen está en Guayas y Pichincha, pero la gravedad en provincias pequeñas, zonas rurales y madrugadas. Por qué: 94.5 % es factor humano, sobre todo distracción y velocidad. A quién: peatones mayores, de noche y en zona rural; y choques frontales y buses producen los eventos con más víctimas. En conjunto, las diferencias más marcadas en la gravedad aparecen según la zona, la hora, el tipo de siniestro y el rol de la víctima. Como límites, el análisis es descriptivo y retrospectivo: caracteriza lo que ya ocurrió, no predice dónde ocurrirá, y la calidad del registro varía entre entes. Gracias, quedamos atentos a sus preguntas.

## 6. Si van tarde o si sobra tiempo

**Recortes, en este orden:**

1. Saltar las 5 frases en cursiva (matiz de P1, cantones de P3, jerarquía de P5, señales de P6 y asociaciones de P7): ahorra unos 30 segundos. El matiz de P1 (solo nueve meses) conviene tenerlo como respuesta preparada si preguntan por el aumento mensual.
2. En la diapositiva 4, nombrar solo los cuatro pasos sin el detalle de cada uno: ahorra unos 15 segundos.

**Si sobra tiempo:** no agreguen preguntas nuevas. Usen esos segundos para señalar con el puntero el punto del gráfico que mencionan (el domingo y las 19 h, el 1 de enero, la celda de Guayaquil) y para dejar un silencio breve tras cada cambio de diapositiva.

**Consejos de ritmo:** no lean la diapositiva; digan las cifras redondeadas como están escritas; en el cambio de expositor, el que termina dice el nombre del siguiente y el que empieza retoma con la pregunta, sin agradecer ni resumir.
