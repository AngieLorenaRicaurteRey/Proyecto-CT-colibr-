import os
import shutil
import re
from datetime import datetime

def mes_a_numero(mes_str):
    meses = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    return meses.get(mes_str[:3], 0) 

def extraer_timestamp(nombre_archivo):
  
    patron = r"Image\[(\d{4}) (\w+) (\d{1,2}) (\d{2})-(\d{2})-(\d{2})\]"
    coincidencia = re.search(patron, nombre_archivo)
    if coincidencia:
        anio = int(coincidencia.group(1))
        mes = mes_a_numero(coincidencia.group(2))
        dia = int(coincidencia.group(3))
        hora = int(coincidencia.group(4))
        minuto = int(coincidencia.group(5))
        segundo = int(coincidencia.group(6))
        return datetime(anio, mes, dia, hora, minuto, segundo)
    return None

def procesar_imagenes(carpeta_origen):
    carpeta_destino = os.path.join(os.path.dirname(carpeta_origen), "repuesto")
    os.makedirs(carpeta_destino, exist_ok=True)

    archivos_tif = [
        f for f in os.listdir(carpeta_origen)
        if f.lower().endswith(".tif") and extraer_timestamp(f) is not None
    ]

  
    archivos_ordenados = sorted(archivos_tif, key=lambda f: extraer_timestamp(f))

    for i, nombre_original in enumerate(archivos_ordenados):
        nuevo_nombre = f"colibri_{i:04d}.tif"
        ruta_origen = os.path.join(carpeta_origen, nombre_original)
        ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)
        shutil.copy2(ruta_origen, ruta_destino)

    print(f"{len(archivos_ordenados)} archivos copiados a '{carpeta_destino}' en orden cronológico.")


procesar_imagenes(r"C:\Users\a.ricaurte\Desktop\2005proj")

