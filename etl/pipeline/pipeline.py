import os
import sys
import pandas as pd

# Configurar ruta dinámica de ejecución
ruta_actual = os.path.dirname(os.path.abspath(__file__)) 
ruta_raiz = os.path.abspath(os.path.join(ruta_actual, "..", "..")) 

if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

# 1. IMPORTAR EXTRACTORES
from etl.extract.extract_api import leer_api
from etl.extract.extract_csv import leer_csv
from etl.extract.extract_sql import leer_mysql

# 2. IMPORTAR TRANSFORMACIONES
from etl.transform.transform import (
    transformar_csv,
    transformar_api,
    transformar_sql,
    unir_ventas_feriados,
    unir_metas,
    crear_variables,
    revisar_transformacion
)

# 3. IMPORTAR CARGADOR
from etl.load.load import cargar_mysql, revisar_carga


def ejecutar_pipeline():
    print("==================================================")
    print("   INICIANDO PIPELINE ETL: VENTAS Y FERIADOS     ")
    print("==================================================\n")

    # ----------------------------------------------------
    # FASE 1: EXTRACT (Extracción Multiaño)
    # ----------------------------------------------------
    print(">>> FASE 1: Extrayendo datos de las fuentes...")
    
    # Extraer rango completo según nuestro Dataset real (2014-2017)
    anios_dataset = [2014, 2015, 2016, 2017]
    listas_feriados = []
    
    print(f"Buscando feriados en la API para los años: {anios_dataset}...")
    for anio in anios_dataset:
        df_anio = leer_api(anio)
        if df_anio is not None and not df_anio.empty:
            listas_feriados.append(df_anio)
            
    df_api = pd.concat(listas_feriados, ignore_index=True) if listas_feriados else None
    
    ruta_csv = os.path.join(ruta_raiz, "data/raw/Sample_ Superstore.csv")
    df_csv = leer_csv(ruta_csv)
    df_sql = leer_mysql()

    if df_api is None or df_csv is None or df_sql is None:
        print("\n[ERROR] Una o más fuentes fallaron al extraerse. Pipeline abortado.")
        return

    print("\n[OK] Extracción completa de todas las fuentes.\n")

    # ----------------------------------------------------
    # FASE 2: TRANSFORM (Transformación y Cruce)
    # ----------------------------------------------------
    print(">>> FASE 2: Transformando y uniendo datasets...")
    
    df_csv_limpio = transformar_csv(df_csv)
    df_api_limpio = transformar_api(df_api)
    df_sql_limpio = transformar_sql(df_sql)

    print("\nUniendo Ventas con Feriados de la API...")
    df_unido = unir_ventas_feriados(df_csv_limpio, df_api_limpio)
    
    print("Uniendo Resultado con Metas de MySQL...")
    df_consolidado = unir_metas(df_unido, df_sql_limpio)

    print("Creating variables derivadas para análisis...")
    df_final = crear_variables(df_consolidado)

    revisar_transformacion(df_final)
    print("\n[OK] Transformación completada con éxito.\n")

    # ----------------------------------------------------
    # FASE 3: LOAD (Limpieza de nombres y carga final)
    # ----------------------------------------------------
    print(">>> FASE 3: Guardando en disco y cargando a MySQL...")
    
    # 3.1 Guardar copia física en data/processed
    ruta_procesado = os.path.join(ruta_raiz, "data/processed/clean_superstore_feriados.csv")
    try:
        os.makedirs(os.path.dirname(ruta_procesado), exist_ok=True)
        df_final.to_csv(ruta_procesado, index=False, encoding="utf-8")
        print(f"[OK] Dataset integrado guardado localmente en: {ruta_procesado}")
    except Exception as e:
        print(f"[ERROR] No se pudo escribir el archivo: {e}. Abortando carga.")
        return

    # 3.2 Volver a leer para asegurar consistencia
    try:
        df_desde_processed = pd.read_csv(ruta_procesado)
    except Exception as e:
        print(f"[ERROR] Falló la lectura del dataset procesado: {e}")
        return

    # ==============================================================================
    # SOLUCIÓN AL ERROR DE COLUMNAS: Normalizar nombres para MySQL superstore_feriados_db
    # ==============================================================================
    # Mapea columnas como 'Order ID' -> 'order_id', 'Product Name' -> 'product_name'
    df_desde_processed.columns = (
        df_desde_processed.columns
        .str.lower()
        .str.replace(' ', '_')
    )

    # Remover 'row_id' si existe, ya que la tabla final usa un ID Auto Incremental automático
    if 'row_id' in df_desde_processed.columns:
        df_desde_processed = df_desde_processed.drop(columns=['row_id'])

    # 3.3 Mostrar auditoría visual con las columnas corregidas y disparar la carga
    revisar_carga(df_desde_processed)
    
    try:
        cargar_mysql(df_desde_processed)
        print("\n==================================================")
        print("   ¡PIPELINE FINALIZADO COMPLETAMENTE EXITOSO!   ")
        print("==================================================")
    except Exception as e:
        print(f"\n[ERROR] Falló la inserción final en MySQL. Verifique los campos: {e}")


if __name__ == "__main__":
    ejecutar_pipeline()