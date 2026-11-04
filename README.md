# Equipo 4: Pi por Monte Carlo (`pi`)

Ejemplo de MapReduce que estima el valor de **π** con puntos en un cuadrado. Esta guía permite reproducir todo paso a paso, en **Windows** o **Linux**, usando solo este README.

> 💻 = comando que se escribe **en tu computadora** · 🐳 = comando que se escribe **dentro del contenedor** `hadoop`

## Integrantes

- Gustavo Adalid Catalan Carmen
- Valentín Almaraz Martínez
- Alberto Saúl Lopez Crespo

## Contenido del repositorio

```
.
├── README.md              ← esta guía
├── datos/                 ← (pi no usa archivos de entrada, ver datos/README.md)
├── scripts/
│   ├── ejecutar.sh        ← 🐳 todos los comandos de Hadoop, en orden
│   └── simular_pi.py      ← 💻 (opcional) réplica en Python para verificar los resultados sin Hadoop
├── resultados/            ← salida esperada y capturas
├── ejercicio/
│   ├── ejercicio.md       ← mini ejercicio para compañeros
│   └── solucion.md        ← solución
├── imagenes/              ← diagramas usados en este README
├── presentacion.pdf       ← diapositivas
└── presentacion.pptx      ← diapositivas editables
```

---

## 1. ¿Qué hace el ejemplo `pi`?

Calcula una **aproximación de π**. Se imagina un cuadrado de lado 1 con un círculo inscrito (radio 0.5). El área del círculo es π · 0.5² = **π/4**, así que la fracción de puntos que cae dentro del círculo se acerca a π/4:

```
π ≈ 4 × (puntos dentro del círculo) / (puntos totales)
```

![Puntos en el cuadrado unitario](imagenes/puntos_halton.png)

**Caso real donde serviría:** la misma idea, estimar un valor lanzando muchísimas muestras independientes, se usa en simulaciones de Monte Carlo para valuar opciones financieras, calcular riesgos, simular el transporte de partículas en física o estimar probabilidades complejas. Como cada muestra es independiente, el trabajo se reparte muy bien entre muchas máquinas, y por eso es un ejemplo clásico para MapReduce.

> **Aclaración importante:** el `pi` de Hadoop no usa números aleatorios. Usa un método **cuasi-Monte Carlo**: los puntos vienen de la **secuencia de Halton** (bases 2 y 3), que cubre el cuadrado de forma muy uniforme y es **determinista**. Por eso, con los mismos parámetros **siempre da exactamente el mismo resultado**, algo que usaremos para comprobar la reproducibilidad.

## 2. ¿Cómo funciona? (Map y Reduce)

El programa se ejecuta así: `pi <nMaps> <nSamples>` (cuántos mappers y cuántos puntos genera cada uno).

![Diagrama Map y Reduce](imagenes/diagrama_mapreduce.png)

| Fase | Qué entra | Qué hace | Qué sale |
|---|---|---|---|
| **Entrada** | Hadoop crea `nMaps` archivos pequeños | Cada uno guarda un par `(offset, size)` con `offset = i · nSamples` y `size = nSamples` | `(offset, size)` por mapper |
| **Map** | `(offset, size)` | Genera los puntos de la secuencia de Halton desde el número `offset+1` hasta `offset+size` y cuenta cuántos caen dentro y fuera del círculo | `(true, nDentro)` y `(false, nFuera)` |
| **Shuffle** | Los pares de todos los mappers | Agrupa por clave (`true` / `false`) | `true → [n₀, n₁, …]`, `false → [m₀, m₁, …]` |
| **Reduce** | Las listas de cada clave | Suma todos los "dentro" y todos los "fuera" y guarda los totales en un archivo temporal | `(totalDentro, totalFuera)` |
| **Final** | Los totales | El programa principal calcula `4 · totalDentro / (nMaps · nSamples)` y lo imprime | `Estimated value of Pi is …` |

**Mini ejemplo con `pi 2 5`** (10 puntos en total):

- Map #0 procesa los puntos 1 a 5 de la secuencia: los 5 caen dentro → emite `(true, 5)` y `(false, 0)`.
- Map #1 procesa los puntos 6 a 10: 4 caen dentro y 1 fuera → emite `(true, 4)` y `(false, 1)`.
- Reduce suma: dentro = 5 + 4 = **9**, fuera = 0 + 1 = 1.
- π ≈ 4 · 9 / 10 = **3.6**. Con tan pocos puntos la estimación es mala, pero con más puntos mejora.

Notas:

- Como el reparto usa `offset`, cada mapper trabaja con un tramo distinto de la misma secuencia. Por eso el resultado solo depende del **total** de puntos (`nMaps × nSamples`), no de cómo se reparten.
- `pi` **no deja una carpeta de salida con `part-r-00000`**: imprime el resultado en pantalla y borra su carpeta temporal `QuasiMonteCarlo_*` al terminar (igual que `sudoku` en la práctica).
- En modo standalone (nuestro contenedor) los maps se ejecutan en una sola máquina, normalmente uno tras otro. En un clúster real correrían en paralelo en varios nodos.

![Convergencia](imagenes/convergencia_pi.png)

---

## 3. Requisitos

- El **contenedor `hadoop`** con **Hadoop 3.3.6** funcionando (si no lo tienes creado, el paso 2 incluye los comandos para levantarlo desde cero).
- **Docker** instalado y encendido en tu computadora.
- **Git** para clonar este repositorio.

| | 🪟 Windows 10/11 | 🐧 Linux (Debian/Ubuntu) |
|---|---|---|
| Terminal a usar | PowerShell (o la terminal de VS Code) | Terminal |
| Instalar Docker | `winget install -e --id Docker.DockerDesktop` (reinicia si lo pide y abre **Docker Desktop** hasta que diga *Engine running*) | `sudo apt update && sudo apt install -y docker.io` y luego `sudo usermod -aG docker $USER` (cierra sesión y vuelve a entrar) |
| Instalar Git | `winget install -e --id Git.Git` (cierra y abre la terminal) | `sudo apt install -y git` |
| Comprobar | `docker --version` y `git --version` | `docker --version` y `git --version` |

> Si en Linux no quieres agregar tu usuario al grupo `docker`, escribe `sudo` antes de cada comando `docker`.

---

## 4. Paso a paso

Los pasos 1 a 3 y 6 a 7 son **idénticos** en Windows y Linux. Cambian solo la instalación (tabla anterior) y la comparación de resultados (paso 7).

### Paso 1 💻: clonar el repositorio

```bash
git clone https://github.com/gustavoadalid1-debug/EP.02.02.-Exposiciones-por-equipos-Ejemplos-de-MapReduce-Gustavo-Valentin-Saul-.git bda-equipo-4-pi
cd bda-equipo-4-pi
```

Esto crea la carpeta `bda-equipo-4-pi` y entra a ella. **Todos los comandos 💻 siguientes se escriben desde esta carpeta.**

### Paso 2 💻: encender o crear el contenedor

Primero comprueba si ya tienes el contenedor en tu máquina:

```bash
docker ps -a
```

#### Opción 1: Si ya tienes el contenedor creado de la práctica anterior
Si en la columna `NAMES` aparece `hadoop`, simplemente enciéndelo si está en estado `Exited`:

```bash
docker start hadoop
```

#### Opción 2: Si estás en una computadora limpia (crear el contenedor desde cero)
Si el contenedor `hadoop` no existe en tu lista, créalo e instálalo ejecutando estos tres comandos en orden:

```bash
# 1. Crear el contenedor base Debian Bullseye
docker run -dit --name hadoop debian:bullseye bash

# 2. Configurar repositorios de archivo e instalar dependencias
docker exec -u root hadoop bash -c 'echo "Acquire::Check-Valid-Until \"false\";" > /etc/apt/apt.conf.d/99no-check-valid-until && echo -e "deb [http://archive.debian.org/debian](http://archive.debian.org/debian) bullseye main contrib non-free\ndeb [http://archive.debian.org/debian-security](http://archive.debian.org/debian-security) bullseye-security main contrib non-free" > /etc/apt/sources.list && apt-get update && apt-get install -y --no-install-recommends openjdk-11-jdk-headless wget procps ca-certificates'

# 3. Crear usuario hadoop, descargar Hadoop 3.3.6 y configurar variables de entorno
docker exec -u root hadoop bash -c 'useradd -m -s /bin/bash hadoop && cd /opt && wget [https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz](https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz) && tar -xzf hadoop-3.3.6.tar.gz && mv hadoop-3.3.6 hadoop && rm hadoop-3.3.6.tar.gz && chown -R hadoop:hadoop /opt/hadoop'
docker exec -u hadoop hadoop bash -c 'cat << "EOF" >> ~/.bashrc
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/opt/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
EOF'
```

> 🪟 En Windows, si sale `failed to connect to the docker API`, **Docker Desktop está apagado**: ábrelo y espera a que diga *Engine running*.

### Paso 3 💻 → 🐳: comprobar la versión de Hadoop

```bash
docker exec -u hadoop hadoop hadoop version
```

Debe empezar con `Hadoop 3.3.6`.

### Paso 4 💻: copiar el script al contenedor

Crea la carpeta de trabajo, copia el script y dale al usuario `hadoop` la propiedad:

```bash
docker exec -u root hadoop mkdir -p /tmp/equipo4
docker cp scripts/ejecutar.sh hadoop:/tmp/equipo4/ejecutar.sh
docker exec -u root hadoop chown -R hadoop:hadoop /tmp/equipo4
```

> `pi` **no necesita archivos de datos**: genera sus propios puntos. Por eso solo se copia el script.

### Paso 5 🐳: ejecutar el ejemplo dentro del contenedor

Abre una terminal dentro del contenedor **como usuario `hadoop`**:

```bash
docker exec -it -u hadoop hadoop bash
```

El prompt cambiará a `hadoop@...:~$`. Ahora ejecuta:

**Opción A: ejecutar todo con el script** (recomendada para reproducir la práctica completa):

```bash
bash /tmp/equipo4/ejecutar.sh
```

El script corre `pi` con 7 combinaciones de parámetros y guarda los resultados en `/tmp/equipo4/resumen.txt` y los registros completos en `/tmp/equipo4/logs/`.

**Opción B: ejecutar una sola vez a mano** (para demostraciones rápidas):

```bash
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 10 1000
```

Qué significa cada parte:
- `hadoop jar` ejecuta un programa empaquetado en un `.jar`.
- `…/hadoop-mapreduce-examples-3.3.6.jar` es el paquete de ejemplos de Hadoop.
- `pi` es el ejemplo que queremos.
- `10` = número de mappers. `1000` = puntos que genera cada mapper (10 000 en total).

Para salir del contenedor cuando termines: escribe `exit` (el contenedor continuará existiendo).

### Resultado esperado

Al final de la salida debe verse:

```
Number of Maps  = 10
Samples per Map = 1000
Wrote input for Map #0
Wrote input for Map #1
...
Wrote input for Map #9
Starting Job
... (mensajes INFO) ...
Job Finished in N seconds
Estimated value of Pi is 3.14080000000000000000
```

La línea que debe coincidir **exactamente** es la última: con `pi 10 1000` siempre sale `3.14080000000000000000`. Tabla completa de valores esperados:

| Comando | Total de puntos | π estimado | Error absoluto |
|---|---:|---|---:|
| `pi 2 5` | 10 | 3.60000000000000000000 | 0.458 |
| `pi 10 10` | 100 | 3.20000000000000000000 | 0.058 |
| `pi 10 100` | 1 000 | 3.14800000000000000000 | 0.0064 |
| `pi 10 1000` | 10 000 | 3.14080000000000000000 | 0.00079 |
| `pi 10 10000` | 100 000 | 3.14120000000000000000 | 0.00039 |
| `pi 10 100000` | 1 000 000 | 3.14155200000000000000 | 0.000041 |
| `pi 16 1000` | 16 000 | 3.14250000000000000000 | 0.00091 |
| `pi 16 1000000` (opcional, ver abajo) | 16 000 000 | 3.14159125000000000000 | 0.0000014 |

### Paso 6 💻: copiar los resultados a tu computadora

Si seguías dentro del contenedor, escribe `exit`. Luego, en tu computadora, desde la carpeta del repositorio:

```bash
docker cp hadoop:/tmp/equipo4/resumen.txt resultados/resumen_obtenido.txt
docker cp hadoop:/tmp/equipo4/logs resultados/
```

### Paso 7 💻: comparar con lo esperado

Si todo salió bien, no debe haber ninguna diferencia.

🪟 **Windows (PowerShell):**

```powershell
Compare-Object (Get-Content resultados/resumen_esperado.txt) (Get-Content resultados/resumen_obtenido.txt)
```

Si **no imprime nada**, los resultados son idénticos. Para verlos: `Get-Content resultados/resumen_obtenido.txt`.

🐧 **Linux:**

```bash
diff resultados/resumen_esperado.txt resultados/resumen_obtenido.txt && echo "IGUALES"
```

Debe imprimir `IGUALES`.

### Opcional A 🐳: ejecución grande (16 millones de puntos)

Dentro del contenedor, el script acepta el argumento `grande` para agregar `pi 16 1000000`:

```bash
bash /tmp/equipo4/ejecutar.sh grande
```

### Opcional B 💻: verificar sin Hadoop

`scripts/simular_pi.py` replica el algoritmo en Python (solo necesita Python 3, sin librerías externas):

🪟 **Windows:** `py scripts/simular_pi.py 10 1000` *(o `python scripts/simular_pi.py 10 1000`)*  
🐧 **Linux:** `python3 scripts/simular_pi.py 10 1000`

Debe imprimir el mismo valor que Hadoop (`3.14080000000000000000`).

### Ver qué otros ejemplos trae Hadoop 🐳

```bash
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar
```

---

## 5. Mini ejercicio

En la carpeta [`ejercicio/`](ejercicio/): `ejercicio.md` (para resolver) y `solucion.md` (solución).

## 6. Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `No such container: hadoop` al ejecutar `docker start hadoop` | El contenedor no ha sido creado en esa máquina | Sigue la **Opción 2 del Paso 2** para crear el contenedor base desde cero con `docker run` y configurar Hadoop. |
| `E: Failed to fetch ... 404 Not Found` al hacer `apt-get install` | Debian Bullseye pasó al archivo histórico oficial | Los repositorios deben apuntar a `http://archive.debian.org/debian` (ya incluido en el comando de creación del Paso 2). |
| En Windows `python` abre la Microsoft Store o dice `Python was not found` | Los "Alias de ejecución de aplicaciones" de Windows interceptan la llamada | Usa `py scripts/simular_pi.py 10 1000` o desactiva los alias en Configuración > Aplicaciones > Alias de ejecución de aplicaciones. |
| `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine` (Windows) | Docker Desktop está cerrado | Abre Docker Desktop y espera a *Engine running*. Repite el comando. |
| La terminal se cierra o se congela al presionar `Ctrl + Z` | En PowerShell `Ctrl + Z` no suspende programas, cierra la sesión | Usa `Ctrl + C` para detener un comando y `exit` para salir del contenedor. Para volver: `docker exec -it -u hadoop hadoop bash`. |
| Se borró el contenedor | Se ejecutó `docker rm hadoop` | **Nunca lo ejecutes**: borra Hadoop, Java y todos los archivos. Habría que crearlo de nuevo con el Paso 2. |
| `bash: /tmp/equipo4/ejecutar.sh: /bin/bash^M: bad interpreter` o `$'\r': command not found` | El script se guardó con saltos de línea de Windows (CRLF) | Este repositorio incluye un `.gitattributes` que lo previene. Si ocurre: `docker exec -u hadoop hadoop sed -i 's/\r$//' /tmp/equipo4/ejecutar.sh`. |
| `Permission denied` al escribir en `/tmp/equipo4` | Faltó el `chown` del paso 4 | Ejecuta `docker exec -u root hadoop chown -R hadoop:hadoop /tmp/equipo4`. |
| `docker cp` falla con `Could not find the file /tmp/equipo4` | Faltó crear la carpeta de destino | Ejecuta el comando `mkdir -p` del Paso 4 antes de transferir archivos. |
| 🪟 En Git Bash, las rutas como `/tmp/equipo4` se convierten en `C:/Program Files/Git/...` | Git Bash reescribe las rutas de Linux | Usa PowerShell o añade `MSYS_NO_PATHCONV=1` al comando de docker. |
| `Tmp directory … already exists` o quedó una carpeta `QuasiMonteCarlo_*` | Se interrumpió una ejecución previa de forma forzada | Ejecuta `rm -rf /tmp/equipo4/QuasiMonteCarlo_*` dentro del contenedor. |
| `ERROR: JAVA_HOME … does not exist` | Variables de entorno no cargadas en el shell | Ejecuta `source ~/.bashrc` o revisa que `echo $JAVA_HOME` apunte a `/usr/lib/jvm/java-11-openjdk-amd64`. |
| El resultado de `pi` no coincide con la tabla | Versión de Hadoop distinta o parámetros cambiados | Revisa `hadoop version` y los números pasados al comando. |

---

## 7. Presentación

Las diapositivas están en [`presentacion.pdf`](presentacion.pdf) (y la versión editable en [`presentacion.pptx`](presentacion.pptx)).
