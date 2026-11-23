# Pregunta de negocio 9: atropellos

> **Pregunta:** ¿Cuándo, dónde y por qué causas ocurren los atropellos, y qué peatones tienen mayor probabilidad de morir?

**Script:** `pregunta_09.py` · **Técnicas:** % de siniestros fatales (atropellos vs resto), heatmaps día × hora por zona, ranking de provincias y causas, letalidad del peatón por edad, horario y zona.

## 1. Qué hace el código

- Selecciona los siniestros de tipo "ATROPELLOS" y los peatones víctimas de la tabla de participantes.
- Mide el peso de los atropellos en siniestros y fallecidos, su % de fatales frente al resto, el peso por franja horaria, las provincias principales y las 6 causas más frecuentes.
- Calcula la letalidad del peatón por edad, horario (noche = 18 a 05 h) y zona. Dibuja dos heatmaps día × hora (urbana y rural, misma escala) y barras de letalidad por edad.

## 2. Para la exposición (máx. 40 s)

> Los dos heatmaps cruzan día y hora para atropellos, en zona urbana y rural. Lo oscuro se concentra entre las 17 y las 21 h: cerca del 40 % de los atropellos ocurre al anochecer. En las barras, la letalidad del peatón sube con la edad hasta 27 % en mayores de 65 años. Además es mayor de noche y en zona rural, donde se duplica. Respuesta: los atropellos son pocos en volumen pero graves, y pasan sobre todo al anochecer, en zona rural y con peatones mayores.

*Figura a mostrar:* `p09_atropellos_heatmaps_y_edad.png`. 88 palabras, unos 35 s a ritmo normal.

## 3. Resultados

- **1 992 atropellos (11.6 % de los siniestros)** causan **289 fallecidos (15.5 % del total)**; son fatales el **14.2 %** frente al 9.0 % del resto (1.6 veces).
- Peso por franja: madrugada 5.9 %, mañana 11.4 %, tarde 12.9 %, **noche 13.6 %**. Las horas 17 a 21 reúnen cerca del 39 %.
- Causas: desatención **33.1 %** (16.1 % fatales), velocidad **23.8 %**, no ceder el paso 14.0 %, peatón que cruza sin respetar la señalización 10.8 %.
- Letalidad del peatón (15.9 % en total): 65+ **27.1 %**, 30-64 20.9 %; noche **20.1 %** frente a 12.4 % de día; rural **24.3 %** frente a 12.8 % urbana.
- Provincias: Guayas 859 y Pichincha 338; mayor letalidad en Manabí, Los Ríos y El Oro.

## 4. Análisis

1. **Es un problema desproporcionado:** 1 de cada 9 siniestros y 1 de cada 6.5 muertes.
2. **La letalidad sube con la edad, la noche y la zona rural:** los tres factores describen al peatón con mayor letalidad en los datos (mayor, de noche y en zona rural).

## 5. Limitaciones

- La letalidad por edad usa solo peatones con edad registrada (sesgo explicado en la pregunta 8).
- Los picos de los heatmaps salen de celdas día × hora con pocos casos; son orientativos.

## 6. Archivos

`p09_atropellos_por_provincia.csv`, `p09_letalidad_peaton_edad.csv` · `p09_atropellos_heatmaps_y_edad.png`
