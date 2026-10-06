"""Resumen de temperaturas y exportación de lecturas con alerta."""
import csv
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

COLUMNA_OBLIGATORIA = {'id_registro', 'fecha_hora', 'id_sensor', 'planta',
                       'temperatura_c', 'vibracion_mm_s'}
LIMITE = Decimal('85')


def leer_datos(ruta):
    with ruta.open(encoding='utf-8-sig', newline='') as archivo:
        lector = csv.DictReader(archivo)
        encabezados = lector.fieldnames
        if not encabezados or not COLUMNA_OBLIGATORIA.issubset(encabezados):
            raise ValueError('Faltan columnas en el archivo de entrada.')
        datos = list(lector)
    for numero, dato in enumerate(datos, start=1):
        if None in dato or any(not dato.get(c) or not dato[c].strip()
                               for c in COLUMNA_OBLIGATORIA):
            raise ValueError(f'La lectura {numero} tiene campos incompletos.')
        try:
            valor = Decimal(dato['temperatura_c'])
        except InvalidOperation as error:
            raise ValueError(f'Temperatura inválida en la lectura {numero}.') from error
        if not valor.is_finite():
            raise ValueError(f'Temperatura no finita en la lectura {numero}.')
    return encabezados, datos


def resumir(datos):
    temperaturas = [Decimal(d['temperatura_c']) for d in datos]
    plantas = sorted({d['planta'] for d in datos})
    promedios = {}
    for planta in plantas:
        valores = [t for d, t in zip(datos, temperaturas) if d['planta'] == planta]
        promedios[planta] = sum(valores, Decimal('0')) / len(valores)
    alertas = [d for d, t in zip(datos, temperaturas) if t > LIMITE]
    conteos = Counter(d['planta'] for d in alertas)
    maxima = max(temperaturas, default=None)
    empates = [d for d, t in zip(datos, temperaturas) if t == maxima]
    mayor_conteo = max((conteos[p] for p in plantas), default=0)
    lideres = [p for p in plantas if conteos[p] == mayor_conteo]
    return promedios, alertas, conteos, maxima, empates, lideres


def ejecutar():
    carpeta = Path(__file__).resolve().parent
    columnas, datos = leer_datos(carpeta / 'data' / 'sensores_industriales.csv')
    promedios, alertas, conteos, maxima, empates, lideres = resumir(datos)
    destino = carpeta / 'resultados' / 'alertas.csv'
    destino.parent.mkdir(exist_ok=True)
    with destino.open('w', encoding='utf-8', newline='') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(alertas)

    print('RESUMEN DE LAS MEDICIONES')
    print(f'Total de registros: {len(datos):,}')
    print(f'Sensores diferentes: {len({d["id_sensor"] for d in datos})}')
    print('\nPromedios de temperatura:')
    for planta, promedio in promedios.items():
        print(f'{planta}: {promedio:.4f} °C')
    print('\nLecturas con la temperatura más alta:')
    if maxima is None:
        print('El archivo no tiene mediciones.')
    else:
        print(f'Máxima: {maxima} °C')
        for dato in empates:
            print(f"{dato['id_sensor']} — {dato['fecha_hora']} — {dato['planta']} "
                  f"— registro {dato['id_registro']}")
    print(f'\nAlertas por encima de 85 °C: {len(alertas):,}')
    for planta in promedios:
        print(f'{planta}: {conteos[planta]}')
    if lideres:
        print('Planta(s) con más alertas: ' + ', '.join(lideres))
        if not alertas:
            print('Todas las plantas tienen cero alertas.')
    print('\nExportación lista: resultados/alertas.csv')


if __name__ == '__main__':
    try:
        ejecutar()
    except (OSError, ValueError, csv.Error) as error:
        raise SystemExit(f'No se pudo completar el análisis: {error}')
