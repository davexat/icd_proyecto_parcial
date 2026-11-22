# Pregunta de negocio 8: casco y cinturón

> **Pregunta:** ¿Las personas que usan casco (motociclistas) o cinturón (ocupantes de vehículos cerrados) mueren menos que las que no lo usan, y qué tan confiable es el registro de estas variables?

**Técnicas:** porcentaje de fallecidos con y sin protección (total y por zona), gráfico de barras facetado y comparación del registro entre entes de control.
**Referencia de contraste:** Liu et al. (2008), Cochrane.
**Verificación:** el script corre sin errores y genera 1 tabla y 2 figuras.

## 1. Qué hace el código

**Bloque 0: grupos de análisis.** Selecciona ocupantes (conductores presentes y pasajeros) con condición conocida y arma dos grupos: *casco*, solo en siniestros donde todos los vehículos son motocicletas; y *cinturón*, solo en siniestros con vehículos cerrados (sin motos, bicicletas, scooters ni triciclos). Así cada protección se evalúa donde corresponde.

**Bloque 1: fallecidos con y sin protección.** Para cada grupo se queda con quienes tienen el campo registrado como "SI" o "NO" y calcula el % de fallecidos (sobre ocupantes) con y sin protección, en total y por zona. Guarda `p08_fallecidos_con_y_sin_proteccion.csv`. Imprime además el contraste con la literatura.

**Bloque 2: gráfico facetado.** Un panel por tipo de protección; barras agrupadas con/sin, para "todos", "zona urbana" y "zona rural".

**Bloque 3: auditoría del registro.** Para los motociclistas calcula el % con casco "SI" por ente de control (entes con 100 o más casos).

## 2. Resultados

| Protección | Grupo | % fallecidos con | % fallecidos sin | Personas (con / sin) |
|---|---|---|---|---|
| Casco | Todos | 13.64 | 13.50 | 1 334 / 1 541 |
| Casco | Urbana | 10.85 | 11.76 | 802 / 944 |
| Casco | Rural | 17.86 | 16.25 | 532 / 597 |
| Cinturón | Todos | 3.50 | 3.80 | 4 176 / 8 365 |
| Cinturón | Urbana | 1.40 | 1.77 | 2 422 / 4 759 |
| Cinturón | Rural | 6.39 | 6.49 | 1 754 / 3 606 |

- Registro de uso como "SI": casco 46.4 %, cinturón 33.3 %.
- Por ente, el % de motociclistas con casco "SI" va de 37.3 % (DMQ) a 49.2 % (CTE), con PNE 46.5 %, MSD 47.6 % y ATM 48.6 %.

## 3. Análisis

1. **En los datos, casco y cinturón casi no cambian la mortalidad.** Con casco, 13.64 % de fallecidos; sin casco, 13.50 %. La diferencia es prácticamente nula y en zona rural incluso es inversa.
2. **Esto contradice la literatura.** Liu et al. (2008) estiman que el casco reduce alrededor de 42 % el riesgo de muerte. Que aquí no se vea no indica que el casco no funcione, sino que **el registro no permite medirlo**.
3. **Por qué probablemente falla el registro** (hipótesis): "NO" parece ser un valor por defecto cuando no se anotó nada; los ilesos están subregistrados (el denominador solo incluye personas con condición conocida, lo que favorece a los más graves); y la variable no distingue casco bien puesto de mal puesto.
4. **Hay baja fiabilidad.** Menos de la mitad de los motociclistas tiene casco "SI" y el porcentaje varía entre entes, lo que sugiere criterios de registro distintos.

## 4. Limitaciones y advertencias

- El análisis es **exploratorio y no causal**: no hay velocidad, tipo de siniestro ni gravedad de la lesión para controlar.
- Es la pregunta más delicada para presentar: un resultado "el casco no sirve" sería un error de interpretación. Por eso se recomienda ubicarla en el apéndice y, si se muestra, enfocarla como **auditoría de calidad del registro**.

## 5. Archivos generados

- Tabla: `p08_fallecidos_con_y_sin_proteccion.csv`
- Figuras: `p08_fallecidos_con_y_sin_proteccion.png`, `p08_auditoria_casco_por_ente.png`

**Cumple de las instrucciones:** referencia de literatura (punto 4), gráfico facetado (6.2).
