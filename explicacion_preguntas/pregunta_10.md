# Pregunta de negocio 10: siniestros de alta consecuencia

> **Pregunta:** ¿Qué características tienen los siniestros de alta consecuencia (3 o más víctimas), cuánto concentran de las víctimas y se explican por la cantidad de personas expuestas?

**Script:** `pregunta_10.py` · **Técnicas:** concentración de víctimas y fallecidos, % de alta consecuencia con y sin cada característica, personas por siniestro con y sin cada característica, top 10 · **Feature:** `n_victimas` (lesionados + fallecidos; WHO, 2023) y personas registradas por siniestro.

## 1. Qué hace el código

- Define alta consecuencia como `n_victimas >= 3` y mide cuánto concentran esos siniestros de las víctimas y fallecidos.
- Para 14 características (bus, camión, moto, 3 o más vehículos, zona rural, noche, causa, tipo de siniestro, etc.) compara el % de alta consecuencia *con* y *sin* ella ("veces más frecuente") y el promedio de personas registradas por siniestro con y sin ella. Lista el top 10 de siniestros.
- Dibuja una figura de tres paneles que comparten el orden de filas: qué parte del total son los siniestros de alta consecuencia, el % con y sin cada característica y las personas por siniestro con y sin ella.

## 2. Para la exposición (máx. 40 s)

> A la izquierda, los siniestros con tres o más víctimas son solo el 5.4 % pero reúnen el 23 % de las víctimas. En el centro, el porcentaje de alta consecuencia con y sin cada característica: choque frontal, tres o más vehículos y bus lo duplican o más. A la derecha, esos mismos casos son los que involucran más gente, de 2.6 a 3.6 personas por siniestro contra 2 en el resto; moto y alcohol no suben ni una ni otra. Lo que cuenta es cuánta gente va expuesta.

*Figura a mostrar:* `p10_concentracion_y_exposicion.png`. 89 palabras, unos 40 s a ritmo normal.

## 3. Resultados

- Promedio 0.95 víctimas por siniestro; máximo 41. **931 siniestros (5.4 %)** tienen 3 o más y concentran el **22.9 % de las víctimas** y el 16.6 % de los fallecidos.
- Veces más frecuente: choque frontal **2.41**, 3 o más vehículos **2.23**, bus **2.01**, transporte público 1.53, red estatal 1.44, zona rural 1.43. Velocidad 1.07, noche 1.01, moto 0.97, alcohol 0.82.
- Personas por siniestro con la característica: 3 o más vehículos **3.6**, bus **3.0**, choque frontal **2.6**, transporte público 2.5; moto 2.15 y alcohol 2.2, igual que el resto (2.15). Los de alta consecuencia tienen 4.85 personas en promedio contra 2.0 en los demás.
- El más grave: 41 lesionados en un estrellamiento en Santa Elena (19 de agosto).

## 4. Análisis

1. **Las víctimas están concentradas:** 1 de cada 20 siniestros explica casi 1 de cada 4 víctimas.
2. **Lo define cuánta gente va expuesta:** las tres características que más aumentan la frecuencia (choque frontal, varios vehículos, bus) son las que más personas reúnen por siniestro; moto y alcohol no aumentan ninguna de las dos. Moto y bus son más fatales (pregunta 7), pero solo el bus reúne a mucha gente.

## 5. Limitaciones

- El umbral de 3 víctimas es una decisión del equipo.
- Las razones comparan cada característica por separado, aunque varias se solapan (bus y transporte público, choque frontal y rural).
- La relación con las personas por siniestro no es universal: la pérdida de pista tiene más alta consecuencia (1.37 veces) con solo 1.6 personas por siniestro. Además, las víctimas forman parte de las personas registradas, así que los siniestros con muchas personas tienen más posibilidad de llegar a 3 víctimas por definición.

## 6. Archivos

`p10_caracteristicas_alta_consecuencia.csv`, `p10_top10_siniestros.csv` · `p10_concentracion_y_exposicion.png`
