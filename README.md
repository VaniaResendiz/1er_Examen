# 1er_Examen
# Temperatura y vibración de sensores industriales

**Vania Yoel Reséndiz Ávila**

El proyecto resume las temperaturas de cuatro plantas y separa las lecturas que superan 85 °C. El informe relaciona esos resultados con los temas de Big Data del parcial.

## Archivo de entrada

`data/sensores_industriales.csv` contiene **mediciones simuladas**. Son 100,000 filas y 40 sensores. Cada planta tiene 25,000 registros. Las fechas del archivo usan día/mes/año.

| Campo | Contenido |
|---|---|
| id_registro | Número de la lectura |
| fecha_hora | Momento de la medición |
| id_sensor | Código del sensor |
| planta | Planta asignada |
| temperatura_c | Temperatura en °C |
| vibracion_mm_s | Vibración en mm/s |

Una temperatura mayor que 85 °C cuenta como alerta. Exactamente 85 °C queda fuera. Esta regla pertenece al ejercicio y no es un diagnóstico de falla.

## Preparar el proyecto

Se necesitan Git y Python 3.10 o una versión posterior. El programa usa solo la biblioteca estándar de Python, así que no necesita paquetes externos. Por eso `requirements.txt` contiene una aclaración y no una lista de paquetes con versiones.

Primero se crea un repositorio en GitHub. En los ejemplos se usa `URL_DEL_REPOSITORIO`: hay que sustituirla por su URL real y actualizar este README antes de entregar.

En Windows, abrir PowerShell y ejecutar:

```powershell
git clone URL_DEL_REPOSITORIO sensores-industriales
cd sensores-industriales
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python analisis.py
```

Si la activación está bloqueada, ejecutar `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y repetir el comando de activación. Si Python se ejecuta con `python` en lugar de `py`, usar `python -m venv .venv`.

En Linux o macOS:

```bash
git clone URL_DEL_REPOSITORIO sensores-industriales
cd sensores-industriales
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python analisis.py
```

## Qué entrega el programa

En la terminal aparecen el total de registros, los sensores distintos, los promedios por planta, las lecturas con temperatura máxima y el conteo de alertas. Se muestran todos los empates. Los resultados se calculan a partir del archivo, no están escritos como respuestas fijas en el programa.

La salida se guarda en `resultados/alertas.csv`, con las columnas y valores originales. Cada ejecución actualiza ese archivo. Las rutas se construyen desde la carpeta del programa, por lo que no dependen del nombre del usuario de la computadora.

## Archivos

- `analisis.py`: lectura, cálculos y exportación.
- `data/sensores_industriales.csv`: datos originales.
- `resultados/alertas.csv`: lecturas mayores que 85 °C.
- `informe.md`: apartados 5 a 9 y diagramas.
- `requirements.txt`: información sobre dependencias.
- `.gitignore`: exclusiones del entorno y caché.
- `evidencias/`: captura de la segunda ejecución y revisión del proyecto.

## Comprobarlo en otra carpeta

Desde la primera copia, en PowerShell:

```powershell
deactivate
cd ..
git clone URL_DEL_REPOSITORIO sensores-segunda-copia
cd sensores-segunda-copia
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python analisis.py
git diff --exit-code -- resultados/alertas.csv
```

Para Linux o macOS, reemplazar la creación del entorno por `python3 -m venv .venv` y la activación por `source .venv/bin/activate`.

Si la comparación termina con código 0 y sin diferencias, la exportación coincide. Guardar una captura real de esta segunda copia, con su ruta, el comando y los resultados visibles, en `evidencias/reproducibilidad.png`.

## Cambios en Git

Durante el desarrollo deben guardarse al menos cuatro cambios significativos y enviarse al repositorio. Se pueden separar por preparación del proyecto, programa, informe y verificación final. Para consultar el historial:

```bash
git log --oneline
```

La captura y el historial de otro proyecto no sustituyen los de este repositorio.
