# Pregunta de negocio 8: perfil de las víctimas

> **Pregunta:** ¿Qué perfil (edad, sexo y rol en la vía) tienen las personas lesionadas y fallecidas, y qué grupos son proporcionalmente más vulnerables?

**Script:** `pregunta_08.py` · **Técnicas:** tabla de participantes (una fila por persona), letalidad por perfil, edad mediana, pirámide facetada por condición y heatmap rol × edad.

## 1. Qué hace el código

- Usa la tabla de participantes (37 096 personas) y define víctimas = lesionados + fallecidos.
- Calcula la **letalidad = fallecidos / (fallecidos + lesionados)** por rol, sexo y grupo de edad, la edad mediana y la razón hombre : mujer. Compara también la letalidad con y sin edad registrada.
- Dibuja dos pirámides (lesionados y fallecidos) por edad y sexo, y un heatmap de letalidad rol × edad (celdas con 30 o más personas).

## 2. Para la exposición (máx. 40 s)

> Las pirámides separan lesionados y fallecidos por edad y sexo: ambas son sobre todo de hombres adultos entre 18 y 64 años. Pero el volumen no es lo mismo que la vulnerabilidad. El heatmap mide la letalidad por rol y edad: la fila del peatón se oscurece con los años, de 6 % en adolescentes a 27 % en mayores de 65, mientras la del conductor casi no cambia. Responde la pregunta: las víctimas son hombres adultos, pero los más vulnerables son los peatones adultos mayores.

*Figura a mostrar:* `p08_heatmap_rol_edad.png` (apoyo: `p08_piramide_lesionados_fallecidos.png`). 86 palabras, unos 34 s a ritmo normal.

## 3. Resultados

- **16 410 víctimas** (con edad el 65.2 %). Hombre : mujer = **2.8 : 1**.
- Letalidad: peatón **15.9 %**, conductor 13.8 %, pasajero 7.2 %; hombres 12.7 % y mujeres 7.7 %.
- Por edad: 0-11 años 9.4 %, 12-17 8.4 %, 18-29 11.5 %, 30-64 13.9 %, **65 o más 19.7 %**.
- Peatón por edad: 9, 6, 14, 21 y **27 %** (0-11 a 65+); la del conductor se mantiene en 13 a 16 %.
- Edad mediana: fallecidos 33 años, lesionados 30.

## 4. Análisis

1. **Las víctimas son sobre todo hombres adultos,** y ellos también mueren más.
2. **El adulto mayor es el más vulnerable,** pero es un fenómeno de peatones: la letalidad del conductor casi no cambia con la edad.

## 5. Limitaciones

- La edad falta en un tercio de las víctimas y las que no la tienen son menos letales (8.5 % frente a 12.9 %), así que los niveles por edad están algo sesgados.
- No se mide exposición. Ciclista y conductor ausente (10 víctimas cada uno) no se interpretan.

## 6. Archivos

`p08_letalidad_por_perfil.csv` · `p08_piramide_lesionados_fallecidos.png`, `p08_heatmap_rol_edad.png`
