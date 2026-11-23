# Pregunta de negocio 9: a quién afecta cada tipo de siniestro y vehículo

> **Pregunta:** ¿Qué tipos de siniestro y qué vehículos afectan a quién? Es decir, qué rol (conductor, pasajero o peatón), sexo y edad tienen las víctimas según el tipo de siniestro y el vehículo involucrado.

**Script:** `pregunta_09.py` · **Técnicas:** unión de participantes y siniestros por `sid`, composición porcentual del perfil de las víctimas por grupo, fila de referencia con el total y heatmaps comparables · **Feature:** `rol`, `sexo`, `grupo_edad`, `tipo_siniestro` y `n_<vehículo>`.

## 1. Qué hace el código

- Toma las 16 410 víctimas (lesionados + fallecidos) y las une con el siniestro por `sid`.
- Para cada tipo de siniestro (100 o más víctimas) y cada vehículo (los 6 más frecuentes) calcula el % de víctimas que son conductor, pasajero o peatón, hombre, menor de 18 años o de 65 años o más. Cada % se calcula sobre las personas con ese dato conocido. Agrega una fila con el total como referencia.
- Dibuja dos heatmaps con la misma escala: filas = tipo de siniestro (ordenado por % de peatones) o vehículo (ordenado por % de conductores); columnas = quién.

## 2. Para la exposición (máx. 40 s)

> Cada fila es un tipo de siniestro o un vehículo, y cada columna, quién es la víctima; la primera fila es el total. En los atropellos, 84 % de las víctimas son peatones y casi una de cada cinco tiene 65 años o más, contra 6 % en general; en la caída de pasajero, 97 % son pasajeros. A la derecha, con una moto 61 % son conductores y 80 % hombres; con un bus, 65 % son pasajeros y 10 % tiene 65 años o más.

*Figura a mostrar:* `p09_a_quien_afecta.png`. 87 palabras, unos 39 s a ritmo normal.

## 3. Resultados

| Grupo | Víctimas | Peatón | Conductor | Pasajero | Hombres | 65+ |
|---|---|---|---|---|---|---|
| **Todos los siniestros** | 16 410 | 14 % | 44 % | 41 % | 73 % | 6 % |
| Atropellos | 2 209 | **84 %** | 12 % | 4 % | 68 % | **19 %** |
| Arrollamientos | 149 | 69 % | 20 % | 11 % | 73 % | 15 % |
| Caída de pasajero | 464 | 2 % | 2 % | **97 %** | 70 % | 9 % |
| Con moto | 6 927 | 6 % | **61 %** | 33 % | **80 %** | 3 % |
| Con bus | 1 244 | 9 % | 26 % | **65 %** | 62 % | **10 %** |

- En los choques entre vehículos (frontal, lateral, posterior, estrellamiento) conductores y pasajeros se reparten casi por mitades y los peatones son menos de 5 %.
- Entre los fallecidos, el 88 % de los de atropellos y el 66 % de los de arrollamientos son peatones; en siniestros con moto, el 76 % de los fallecidos son conductores.

## 4. Análisis

1. **Cada tipo de siniestro afecta a alguien distinto:** los atropellos y arrollamientos, a peatones (con más personas mayores de lo habitual); la caída de pasajero, a pasajeros; los choques entre vehículos, a quienes van dentro.
2. **Cada vehículo tiene su perfil:** las motos afectan sobre todo a sus conductores y a hombres jóvenes; los buses, a pasajeros, con más mujeres y más personas de 65 años o más que el promedio.
3. Complementa la pregunta 8: allí se ve quién es más vulnerable (letalidad); aquí, qué siniestro y qué vehículo se asocia a cada persona.

## 5. Limitaciones

- Las víctimas de «siniestros con moto» o «con bus» son todas las del siniestro, no solo quienes iban en ese vehículo (puede haber peatones u ocupantes de otro vehículo). Un siniestro con moto y bus cuenta en ambos grupos.
- El sexo se conoce en 99 % de las víctimas y la edad en 65 %; los porcentajes de edad se calculan solo con quienes la tienen.
- Los menores de 18 son 9 % de las víctimas y los de 65 o más 6 %; sus diferencias entre filas son pequeñas y los grupos con pocas víctimas (arrollamientos, 149) se interpretan con cautela.
- Describe a quién afecta cada siniestro, no cuán probable es que le ocurra a cada grupo: no se mide exposición.

## 6. Archivos

`p09_perfil_por_tipo_siniestro.csv`, `p09_perfil_por_vehiculo.csv` · `p09_a_quien_afecta.png`
