# Equipo 4: Pi por Monte Carlo (`pi`)

Ejemplo de MapReduce que estima el valor de **$\pi$** simulando puntos en un cuadrado unitario. Esta guía permite reproducir el proceso paso a paso, en entornos **Linux** o **Windows**, asegurando una ejecución reproducible y determinista.

> 💻 = Comando ejecutado en el sistema anfitrión (**Host**).  
> 🐳 = Comando ejecutado dentro del contenedor (**Hadoop**).

---

## Integrantes

- Gustavo Adalid Catalan Carmen
- Valentín Almaraz Martínez
- Alberto Saúl Lopez Crespo

---

## Contenido del repositorio

```text
.
├── README.md              ← Guía técnica y pasos de reproducción
├── datos/                 ← Nota técnica sobre generación en memoria
├── scripts/
│   ├── ejecutar.sh        ← Script automatizado de MapReduce en el contenedor
│   └── simular_pi.py      ← Réplica matemática en Python sin Hadoop
├── resultados/            ← Resultados de referencia, concentrado y logs
├── ejercicio/
│   ├── ejercicio.md       ← Mini-ejercicio para evaluación cruzada
│   └── solucion.md        ← Análisis teórico y solución
├── imagenes/              ← Diagramas ilustrativos
├── presentacion.pdf       ← Diapositivas para exposición
└── presentacion.pptx      ← Diapositivas editables
```

---

## 1. ¿Qué hace el ejemplo `pi`?

Calcula una aproximación del número $\pi$ mediante simulación geométrica. Se toma un cuadrado de lado 1 con un cuadrante de círculo inscrito (o círculo centrado de radio $r = 0.5$). La probabilidad de que un punto aleatorio caiga dentro del círculo corresponde a la razón entre el área del círculo y la del cuadrado:

$$\frac{\text{Área del círculo}}{\text{Área del cuadrado}} = \frac{\pi r^2}{(2r)^2} = \frac{\pi}{4}$$

$$\pi \approx 4 \times \frac{\text{puntos dentro del círculo}}{\text{puntos totales simulados}}$$

![Puntos en el cuadrado unitario](imagenes/puntos_halton.png)

### Caso de uso real
El método de Monte Carlo se emplea en valuación de activos financieros, cálculo de riesgos actuariales, termodinámica estadística y simulaciones de transporte de radiación. Al tratarse de muestreos numéricamente independientes, permite una paralelización eficiente sobre clústeres distribuidos.

> **Determinismo:** La implementación en Hadoop utiliza secuencias **cuasi-Monte Carlo (Halton)** con bases 2 y 3. No son números pseudoaleatorios uniformes, sino una secuencia matemática determinista que garantiza cobertura homogénea. Por lo tanto, con parámetros idénticos de mapas y muestras, el resultado numérico siempre es exactamente el mismo.

---

## 2. Funcionamiento en MapReduce

El comando se invoca como: `hadoop jar hadoop-mapreduce-examples-*.jar pi <nMaps> <nSamples>`

![Diagrama Map y Reduce](imagenes/diagrama_mapreduce.png)

| Fase | Entrada | Proceso | Salida |
|---|---|---|---|
| **División** | Parámetros `nMaps` y `nSamples` | Genera $N$ tareas asignando desplazamientos (`offset = i × nSamples`) | Pares `(offset, size)` |
| **Map** | `(offset, size)` | Genera la secuencia de Halton y clasifica si cada $(x,y)$ cumple $x^2 + y^2 \le 1$ | Pares clave-valor: `(true, nDentro)` y `(false, nFuera)` |
| **Shuffle / Sort** | Salidas de los Mappers | Agrupa los conteos por clave booleana | Listas `true → [d₁, d₂, ...]` y `false → [f₁, f₂, ...]` |
| **Reduce** | Conteos agrupados | Suma todos los aciertos interiores y exteriores | Acumulados `(totalDentro, totalFuera)` |
| **Consolidación** | Valores finales | Aplica la fórmula $\pi = 4 \times \frac{\text{totalDentro}}{\text{totalPuntos}}$ | Impresión en consola del valor estimado |

---

## 3. Prerrequisitos

- Docker y motor de ejecución en ejecución (Docker Desktop en ejecución).
- Git configurado en el sistema anfitrión.

---

## 4. Guía paso a paso para reproducción

### Paso 1 💻: Clonar el repositorio
```bash
git clone https://github.com/valentinalmaraz401-dot/bda-equipo-4-pi.git
cd bda-equipo-4-pi
```

### Paso 2 💻: Asegurar que el contenedor esté activo
```bash
docker start hadoop
```

### Paso 3 💻: Transferir el script al contenedor
```bash
docker exec -u root hadoop mkdir -p /tmp/equipo4
docker cp scripts/ejecutar.sh hadoop:/tmp/equipo4/ejecutar.sh
docker exec -u root hadoop chown -R hadoop:hadoop /tmp/equipo4
docker exec -u root hadoop chmod +x /tmp/equipo4/ejecutar.sh
```

### Paso 4 💻: Ejecutar el cálculo automatizado
Para asegurar compatibilidad tanto si Hadoop se ubica en `/home/hadoop/hadoop-3.3.6` o en `/opt/hadoop`, ejecuta este comando directo:

```bash
docker exec -it -u hadoop hadoop bash -c "
if [ -d '/home/hadoop/hadoop-3.3.6' ]; then
    export HADOOP_HOME=/home/hadoop/hadoop-3.3.6
elif [ -d '/opt/hadoop' ]; then
    export HADOOP_HOME=/opt/hadoop
fi
export PATH=\$HADOOP_HOME/bin:\$PATH
bash /tmp/equipo4/ejecutar.sh
"
```

El script ejecutará las series de prueba (`pi 2 5`, `pi 10 10`, `pi 10 100`, `pi 10 1000`, `pi 10 10000`, `pi 10 100000`, `pi 16 1000`), generando los logs en `/tmp/equipo4/logs/` y el concentrado en `/tmp/equipo4/resumen.txt`.

### Paso 5 💻: Extraer resultados y verificar
Copia los resultados a tu máquina local:
```bash
docker cp hadoop:/tmp/equipo4/resumen.txt resultados/resumen_obtenido.txt
docker cp hadoop:/tmp/equipo4/logs resultados/
```

Valida la reproducibilidad contra los valores esperados:
```bash
diff resultados/resumen_esperado.txt resultados/resumen_obtenido.txt && echo "COMPROBACIÓN EXITOSA: LOS RESULTADOS SON IDÉNTICOS"
```

### Paso 6 💻: Verificación con Python (independiente de Hadoop)
```bash
python3 scripts/simular_pi.py 10 1000
```
*Salida esperada:* `Estimated value of Pi is 3.14080000000000000000`

---

## 5. Tabla de referencia de resultados

| Configuración | Puntos totales | $\pi$ estimado | Error absoluto |
|---|---:|---|---:|
| `pi 2 5` | 10 | 3.60000000000000000000 | 0.4584 |
| `pi 10 10` | 100 | 3.20000000000000000000 | 0.0584 |
| `pi 10 100` | 1,000 | 3.14800000000000000000 | 0.0064 |
| `pi 10 1000` | 10,000 | 3.14080000000000000000 | 0.0008 |
| `pi 10 10000` | 100,000 | 3.14120000000000000000 | 0.0004 |
| `pi 10 100000` | 1,000,000 | 3.14155200000000000000 | 0.00004 |
| `pi 16 1000` | 16,000 | 3.14250000000000000000 | 0.0009 |

---

## 6. Mini-ejercicio

El ejercicio práctico para evaluación cruzada se encuentra en [`ejercicio/`](ejercicio/):
- **`ejercicio/ejercicio.md`**: Instrucciones y preguntas de análisis sobre escalabilidad y precisión.
- **`ejercicio/solucion.md`**: Respuestas esperadas y justificación teórica.

---

## 7. Solución de problemas comunes

| Error | Causa | Solución |
|---|---|---|
| `failed to connect to the docker API` | Docker está apagado o no iniciado. | Iniciar Docker Desktop o correr `sudo systemctl start docker`. |
| `executable file not found in $PATH` | Sesión remota de Docker no cargó variables de entorno. | Ejecutar el comando del Paso 4 que define explícitamente `$HADOOP_HOME`. |
| `Cannot create input directory ... QuasiMonteCarlo_.../in` | Ejecución en la raíz `/` sin permisos de escritura. | Especificar siempre un directorio con permisos (como `-w /home/hadoop` o `/tmp/equipo4`). |
| `bash: ... bad interpreter: No such file or directory` | Saltos de línea estilo Windows (CRLF). | Ejecutar en el contenedor: `sed -i 's/\r$//' /tmp/equipo4/ejecutar.sh`. |
