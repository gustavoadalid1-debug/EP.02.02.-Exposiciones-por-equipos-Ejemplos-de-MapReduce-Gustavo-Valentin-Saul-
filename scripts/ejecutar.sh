#!/bin/bash
# =====================================================================
# ejecutar.sh  -  Equipo 4: Pi por Monte Carlo (ejemplo "pi" de Hadoop)
#
# 🐳 Ejecutar DENTRO del contenedor, como usuario hadoop:
#       bash /tmp/equipo4/ejecutar.sh            (corridas normales)
#       bash /tmp/equipo4/ejecutar.sh grande     (agrega pi 16 1000000)
#
# Deja:  /tmp/equipo4/resumen.txt   (una línea por corrida)
#        /tmp/equipo4/logs/         (salida completa de cada corrida)
# =====================================================================

if [ -z "${HADOOP_HOME:-}" ]; then
  echo "ERROR: HADOOP_HOME no está definido."
  echo "       ¿Entraste como usuario hadoop?  ->  su - hadoop"
  exit 1
fi

# Busca el .jar de ejemplos (así funciona con cualquier versión de Hadoop)
JAR=$(ls "$HADOOP_HOME"/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar 2>/dev/null | head -n 1)
if [ -z "$JAR" ]; then
  echo "ERROR: no encontré hadoop-mapreduce-examples-*.jar en $HADOOP_HOME"
  exit 1
fi

TRABAJO=/tmp/equipo4
LOGS="$TRABAJO/logs"
RESUMEN="$TRABAJO/resumen.txt"

mkdir -p "$LOGS"
# pi crea una carpeta temporal QuasiMonteCarlo_* en el directorio actual
cd "$TRABAJO" || exit 1
: > "$RESUMEN"          # vacía el resumen de una ejecución anterior

echo "Versión: $(hadoop version | head -n 1)"
echo "Jar:     $JAR"
echo

correr() {
  local maps=$1 samples=$2
  local log="$LOGS/pi_${maps}x${samples}.log"
  echo "==> pi $maps $samples   ($((maps * samples)) puntos en total)"
  hadoop jar "$JAR" pi "$maps" "$samples" > "$log" 2>&1
  local linea
  linea=$(grep "Estimated value of Pi" "$log")
  if [ -z "$linea" ]; then
    echo "    FALLÓ. Revisa el registro: $log"
    return 1
  fi
  echo "    $linea"
  echo "pi $maps $samples -> $linea" >> "$RESUMEN"
}

correr 2 5
correr 10 10
correr 10 100
correr 10 1000
correr 10 10000
correr 10 100000
correr 16 1000

if [ "${1:-}" = "grande" ]; then
  correr 16 1000000
fi

echo
echo "Resumen guardado en $RESUMEN:"
cat "$RESUMEN"
echo
echo "Siguiente paso (en TU computadora, no aquí):"
echo "  docker cp hadoop:/tmp/equipo4/resumen.txt resultados/resumen_obtenido.txt"
echo "  docker cp hadoop:/tmp/equipo4/logs resultados/"
