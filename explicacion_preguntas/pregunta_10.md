# Pregunta de negocio 10: siniestros de alta consecuencia

> **Pregunta:** ¿Qué características tienen los siniestros de alta consecuencia (3 o más víctimas) y qué tan concentradas están las víctimas en pocos eventos?

**Script:** `pregunta_10.py` · **Técnicas:** distribución de víctimas por siniestro, concentración, % de alta consecuencia con y sin cada característica, top 10 · **Feature:** `n_victimas` (lesionados + fallecidos; WHO, 2023).

## 1. Qué hace el código

- Define alta consecuencia como `n_victimas >= 3` y mide cuánto concentran esos siniestros de las víctimas y fallecidos.
- Para 14 características (bus, camión, moto, 3 o más vehículos, zona rural, noche, causa, tipo de siniestro, etc.) compara el % de alta consecuencia *con* y *sin* ella y calcula las "veces más probable". Lista el top 10 de siniestros.
- Grafica un histograma de víctimas (escala log), las razones de probabilidad en barras y la distribución por zona.

## 2. Para la exposición (máx. 40 s)

> A la izquierda, el histograma con escala logarítmica: casi todos los siniestros tienen cero o una víctima, pero hay una cola larga. Ese 5 % de siniestros con tres o más víctimas concentra casi una cuarta parte de todas las víctimas. A la derecha, las barras muestran cuánto más probable es la alta consecuencia con cada característica: choque frontal, tres o más vehículos y bus duplican o más la probabilidad. Moto y alcohol no suben. Lo que cuenta es cuánta gente hay en el evento.

*Figura a mostrar:* `p10_distribucion_y_caracteristicas.png` (apoyo: `p10_victimas_por_zona.png`). 85 palabras, unos 34 s a ritmo normal.

## 3. Resultados

- Promedio 0.95 víctimas por siniestro; máximo 41. **931 siniestros (5.4 %)** tienen 3 o más y concentran el **22.9 % de las víctimas** y el 16.6 % de los fallecidos.
- Veces más probable: choque frontal **2.41**, 3 o más vehículos **2.23**, bus **2.01**, transporte público 1.53, red estatal 1.44, zona rural 1.43. Velocidad 1.07, noche 1.01, moto 0.97, alcohol 0.82.
- El más grave: 41 lesionados en un estrellamiento en Santa Elena (19 de agosto).

## 4. Análisis

1. **Las víctimas están concentradas:** 1 de cada 20 siniestros explica casi 1 de cada 4 víctimas.
2. **Lo define cuánta gente va expuesta** (bus, transporte público, varios vehículos). Moto y alcohol son letales (preguntas 6 y 7) pero afectan a pocas personas por evento.

## 5. Limitaciones

- El umbral de 3 víctimas es una decisión del equipo.
- Las razones comparan cada característica por separado, aunque varias se solapan (bus y transporte público, choque frontal y rural).

## 6. Archivos

`p10_caracteristicas_alta_consecuencia.csv`, `p10_top10_siniestros.csv` · `p10_distribucion_y_caracteristicas.png`, `p10_victimas_por_zona.png`
