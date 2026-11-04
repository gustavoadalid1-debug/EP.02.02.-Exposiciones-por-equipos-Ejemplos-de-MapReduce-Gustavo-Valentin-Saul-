# datos/

El ejemplo `pi` **no usa archivos de entrada**: Hadoop genera por sí mismo los archivos
mínimos con los pares `(offset, size)` que reciben los mappers, y los borra al terminar.

Por eso esta carpeta no tiene datos. Lo único que hay que indicarle al programa son los
dos parámetros de la línea de comandos:

```
pi <nMaps> <nSamples>
```
