# Pregunta de negocio 7: perfil de las víctimas

> **Pregunta:** ¿Qué perfil (edad, sexo y rol en la vía) tienen las personas lesionadas y fallecidas, y qué grupos son proporcionalmente más vulnerables?

**Técnicas:** tabla de participantes en formato largo, letalidad (fallecidos / víctimas) por perfil, edad mediana, pirámide de población facetada por condición y heatmap rol × grupo de edad.
**Verificación:** el script corre sin errores y genera 1 tabla y 2 figuras.

## 1. Qué hace el código

**Bloque 0: cobertura.** Usa la tabla `part` (una fila por persona, 37 096 en total) y mide cuántas personas tienen edad, sexo y condición válidos. Define las víctimas como los lesionados más los fallecidos.

**Bloque 1: letalidad por perfil.** Por rol, sexo y grupo de edad calcula víctimas, fallecidos y **letalidad = fallecidos / (fallecidos + lesionados)**. Añade la edad mediana de fallecidos y lesionados y la razón hombre : mujer. Guarda `p07_letalidad_por_perfil.csv`.

**Bloque 2: pirámide facetada.** Dos pirámides (lesionados y fallecidos) con hombres a la izquierda y mujeres a la derecha por grupo de edad, usando solo personas con edad y sexo conocidos. El eje X de cada pirámide es distinto porque las magnitudes también lo son (miles vs cientos).

**Bloque 3: heatmap rol × edad.** Letalidad entre víctimas por rol y grupo de edad, omitiendo celdas con menos de 30 personas.

## 2. Resultados

**Cobertura:** edad 56.1 %, sexo 87.2 %, condición 81.7 %. Entre las 16 410 víctimas, tienen edad el 65.2 % y sexo el 99.3 %.

| Perfil | Víctimas | Letalidad |
|---|---|---|
| Peatón | 2 345 | **15.9 %** |
| Conductor presente | 7 265 | 13.8 % |
| Pasajero | 6 780 | 7.2 % |
| Hombre | 11 952 | **12.7 %** |
| Mujer | 4 341 | 7.7 % |
| 0 a 11 años | 438 | 9.4 % |
| 12 a 17 | 500 | 8.4 % |
| 18 a 29 | 4 095 | 11.5 % |
| 30 a 64 | 5 024 | 13.9 % |
| 65 o más | 646 | **19.7 %** |

- Razón hombre : mujer entre víctimas con sexo conocido: **2.8 : 1**.
- Edad mediana: fallecidos 33 años; lesionados 30 años.

**Heatmap rol × edad (letalidad %):** peatón 9 (0-11), 6 (12-17), 14 (18-29), 21 (30-64), **27 (65+)**; conductor 16, 13, 15 y 16 (12-17 a 65+); pasajero 8 a 9 en todas las edades menos 12 en 65+.

## 3. Análisis

1. **Las víctimas son sobre todo hombres adultos.** Casi tres de cada cuatro víctimas son hombres, concentrados en los 18 a 64 años (pirámide).
2. **Los hombres también mueren más cuando se accidentan** (12.7 % vs 7.7 %).
3. **El adulto mayor es el grupo más vulnerable** (19.7 %, el doble de los menores de 18). Pero el heatmap muestra que esto es un fenómeno *de peatones*: la letalidad del peatón sube de 6 % a 27 % con la edad, mientras que la del conductor casi no cambia (13 a 16 %).
4. **El peatón es el rol más letal** (15.9 %), por encima del conductor; el pasajero es el más protegido (7.2 %).

## 4. Limitaciones y advertencias

- La edad falta en un tercio de las víctimas. En P13 se ve que las víctimas *sin* edad tienen letalidad menor (8.5 % vs 12.9 %), así que los niveles absolutos de letalidad por edad están algo sesgados; el patrón por grupos se mantiene (ver P13).
- Ciclista (10 víctimas) y conductor ausente (10) no se interpretan por su tamaño; el heatmap los omite.
- Los resultados son descriptivos: no se mide exposición (cuánta gente de cada grupo circula).

## 5. Archivos generados

- Tabla: `p07_letalidad_por_perfil.csv`
- Figuras: `p07_piramide_lesionados_fallecidos.png`, `p07_heatmap_rol_edad.png`

**Cumple de las instrucciones:** gráfico facetado (6.2), heatmap (6.3), datos continuos (edad) y categóricos.
