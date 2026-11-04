# Solución: ¿qué tan bueno es tu π?

> Los valores son **exactos y repetibles** porque el ejemplo `pi` usa una secuencia determinista
> (Halton). Si te sale otro valor con los mismos parámetros, revisa la versión de Hadoop y los
> números del comando.

## Parte 1

`pi 2 5` da **3.60000000000000000000**.

Se generaron 2 × 5 = **10 puntos** en total. El Map #0 contó 5 dentro y 0 fuera; el Map #1
contó 4 dentro y 1 fuera. En total 9 dentro de 10, así que π ≈ 4 · 9 / 10 = 3.6.

## Parte 2

| Comando | Puntos totales | π estimado | Error |
|---|---:|---|---:|
| `pi 10 10` | 100 | 3.20000000000000000000 | 0.058 |
| `pi 10 100` | 1 000 | 3.14800000000000000000 | 0.0064 |
| `pi 10 1000` | 10 000 | 3.14080000000000000000 | 0.00079 |
| `pi 10 10000` | 100 000 | 3.14120000000000000000 | 0.00039 |
| `pi 10 100000` | 1 000 000 | 3.14155200000000000000 | 0.000041 |

## Parte 3

Los tres dan **3.14800000000000000000** (787 puntos dentro de 1 000).

## Parte 4

Las dos ejecuciones dan **3.14080000000000000000**, idénticas.

## Preguntas para reflexionar

1. **¿Por qué × 4?** La fracción de puntos dentro del círculo se acerca al cociente entre el
   área del círculo y la del cuadrado: (π · 0.5²) / 1² = π/4. Para obtener π hay que multiplicar
   esa fracción por 4.

2. **¿Qué emite el Map y qué hace el Reduce?** Cada Map recibe `(offset, size)`, genera `size`
   puntos de la secuencia de Halton y emite dos pares: `(true, nDentro)` y `(false, nFuera)`.
   Hadoop agrupa por clave y el Reduce suma todos los "dentro" por un lado y todos los "fuera"
   por otro. Con esos totales, el programa calcula 4 · dentro / (nMaps · nSamples).

3. **Parte 3:** los tres resultados son iguales. Cada mapper trabaja con un tramo distinto de
   la misma secuencia (por eso se le da un `offset`), así que juntos cubren siempre los puntos
   del 1 al `nMaps × nSamples`. El resultado depende solo del **total** de puntos, no de cómo se
   repartan entre mappers. Repartir entre más mappers sirve para ir más rápido en un clúster, no
   para cambiar el resultado.

4. **Parte 4:** el ejemplo no usa números aleatorios sino la **secuencia de Halton**, una
   secuencia determinista que llena el cuadrado de forma muy uniforme. Por eso el método se
   llama *cuasi-Monte Carlo*. Misma entrada, mismo resultado. Tiene una ventaja: converge más
   rápido que usar puntos aleatorios, y otra: se puede comprobar que el resultado es correcto.

5. **Parte 2:** con 100 000 puntos el error es 0.00039 (menor que 0.0005), mientras que con
   10 000 puntos sigue en 0.00079. Hacen falta aproximadamente **100 000 puntos**. Ojo: el error
   no baja de forma perfectamente uniforme (por ejemplo, con 16 000 puntos el error es 0.00091),
   pero en general baja al aumentar los puntos.

6. **Bonus:** `pi 10 1000000` da **3.14158440000000000000** (error ≈ 0.0000083). Tarda más
   (el tiempo depende de la computadora, normalmente de unos segundos a algo más de un minuto).
   Comparado con 1 millón de puntos (error 0.000041), el error mejora unas 5 veces al usar 10
   veces más puntos. Para aprender o demostrar el método no vale la pena; para un valor de
   π con muchos decimales hay fórmulas mucho mejores (como la del ejemplo `bbp` de otro equipo).
