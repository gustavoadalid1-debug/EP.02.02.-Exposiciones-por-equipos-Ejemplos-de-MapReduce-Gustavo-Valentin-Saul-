# Mini ejercicio: ¿qué tan bueno es tu π?

## ¿De qué se trata este ejercicio?

Vas a usar el ejemplo `pi` de Hadoop, que estima el valor de π con puntos en un cuadrado. Es
casi igual al ejemplo de `grep` de la práctica, pero aquí **no hay archivos de entrada ni
carpeta de salida**: solo le dices cuántos mappers usar y cuántos puntos genera cada uno.

La idea es que observes tres cosas: cómo mejora la estimación con más puntos, si importa cómo
se reparten los puntos entre mappers y si el resultado cambia al repetir la ejecución.

> 🐳 Todo se escribe **dentro del contenedor** `hadoop`, como usuario `hadoop`
> (`docker exec -it -u hadoop hadoop bash` desde tu computadora).

Para escribir menos, guarda la ruta del `.jar` en una variable:

```bash
export EJEMPLOS=$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar
cd /tmp
```

Cada ejecución tiene esta forma (la línea que importa es la última de la salida,
`Estimated value of Pi is …`):

```bash
hadoop jar $EJEMPLOS pi <nMaps> <nSamples>
```

Usa π = 3.14159265 para calcular errores (`error = |π − tu estimación|`).

## Parte 1: tu primera estimación

Ejecuta `pi 2 5`.

1. ¿Qué valor de π obtienes?
2. ¿Cuántos puntos se generaron en total?

## Parte 2: más puntos, mejor estimación

Ejecuta cada comando y completa la tabla:

| Comando | Puntos totales | π estimado | Error |
|---|---:|---|---|
| `pi 10 10` | | | |
| `pi 10 100` | | | |
| `pi 10 1000` | | | |
| `pi 10 10000` | | | |
| `pi 10 100000` | | | |

## Parte 3: ¿importa cómo se reparten los puntos?

Los tres comandos generan **1 000 puntos en total**, pero con reparto distinto:

```bash
hadoop jar $EJEMPLOS pi 1 1000
hadoop jar $EJEMPLOS pi 10 100
hadoop jar $EJEMPLOS pi 20 50
```

Anota el valor que da cada uno.

## Parte 4: ¿es de verdad aleatorio?

Ejecuta **dos veces seguidas** el mismo comando:

```bash
hadoop jar $EJEMPLOS pi 10 1000
hadoop jar $EJEMPLOS pi 10 1000
```

Compara los dos resultados.

## Preguntas para reflexionar

1. ¿Por qué el resultado final se multiplica por 4?
2. ¿Qué pares emite cada Map y qué hace el Reduce con ellos?
3. En la Parte 3, ¿qué pasó con los tres resultados? ¿Qué te dice eso sobre cómo reparte Hadoop los puntos entre los mappers?
4. En la Parte 4, con números aleatorios de verdad esperarías dos valores distintos. ¿Por qué aquí salió igual? (Pista: busca "secuencia de Halton".)
5. Observando la tabla de la Parte 2, ¿aproximadamente cuántos puntos hacen falta para que el error sea menor que 0.0005?
6. **Bonus:** ejecuta `pi 10 1000000` (10 millones de puntos). ¿Cuánto tarda y cuánto mejora el error? ¿Vale la pena?
