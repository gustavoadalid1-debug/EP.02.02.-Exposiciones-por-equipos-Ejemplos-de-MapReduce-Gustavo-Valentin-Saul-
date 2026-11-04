# resultados/

| Archivo | Qué es |
|---|---|
| `resumen_esperado.txt` | Salida esperada de `scripts/ejecutar.sh` (una línea por corrida). Se compara con `resumen_obtenido.txt` en el paso 7 del README |
| `resumen_obtenido.txt` | (lo genera quien reproduce) copia del `resumen.txt` del contenedor |
| `logs/` | (lo genera quien reproduce) salida completa de cada corrida |
| `capturas/` | Capturas de pantalla de nuestra ejecución en el contenedor |

## Valores esperados

| Comando | Puntos totales | π estimado |
|---|---:|---|
| `pi 2 5` | 10 | 3.60000000000000000000 |
| `pi 10 10` | 100 | 3.20000000000000000000 |
| `pi 10 100` | 1 000 | 3.14800000000000000000 |
| `pi 10 1000` | 10 000 | 3.14080000000000000000 |
| `pi 10 10000` | 100 000 | 3.14120000000000000000 |
| `pi 10 100000` | 1 000 000 | 3.14155200000000000000 |
| `pi 16 1000` | 16 000 | 3.14250000000000000000 |
| `pi 16 1000000` (opcional, `ejecutar.sh grande`) | 16 000 000 | 3.14159125000000000000 |
| `pi 10 1000000` (bonus del ejercicio) | 10 000 000 | 3.14158440000000000000 |

## Capturas sugeridas (carpeta `capturas/`)

- `01_docker_ps.png`: `docker ps -a` con el contenedor `hadoop` en `Up`.
- `02_hadoop_version.png`: `hadoop version` mostrando 3.3.6.
- `03_pi_10_1000.png`: ejecución de `pi 10 1000` con la línea `Estimated value of Pi is 3.14080000000000000000`.
- `04_ejecutar_sh.png`: resumen final de `ejecutar.sh`.
- `05_comparacion.png`: comparación con `resumen_esperado.txt` sin diferencias.
