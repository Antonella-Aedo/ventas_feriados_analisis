import os
import sys

# Configurar ruta dinámica apuntando a la raíz del proyecto (1 nivel arriba desde 'etl')
ruta_actual = os.path.dirname(os.path.abspath(__file__)) # Apunta a la carpeta etl/
ruta_raiz = os.path.abspath(os.path.join(ruta_actual, "..")) # Sube 1 nivel hasta superstore-climate-analysis

# Usamos insert(0, ...) en lugar de append para darle máxima prioridad a tu proyecto
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

# 1. IMPORTAR TUS EXTRACTORES
from etl.extract.extract_api import leer_api
from etl.extract.extract_csv import leer_csv
from etl.extract.extract_sql import leer_mysql

# 2. IMPORTAR TUS TRANSFORMACIONES
from etl.transform.transform import (
    transformar_csv,
    transformar_api,
    transformar_sql,
    unir_ventas_feriados,
    unir_metas,
    crear_variables,
    revisar_transformacion
)

# 3. IMPORTAR TU CARGADOR
from etl.load.load import cargar_mysql, revisar_carga


def ejecutar_pipeline():
    print("==================================================")
    print("   INICIANDO PIPELINE ETL: SUPERSTORE CLIMATE     ")
    print("==================================================\n")

    # ----------------------------------------------------
    # FASE 1: EXTRACT (Extracción)
    # ----------------------------------------------------
    print(">>> FASE 1: Extrayendo datos de las fuentes...")
    
    # Extraer de la API (Tomamos 2016 basándonos en tu script)
    df_api = leer_api(2016)
    
    # Extraer del CSV
    ruta_csv = "data/raw/Sample_ Superstore.csv"
    df_csv = leer_csv(ruta_csv)
    
    # Extraer de MySQL (Metas)
    df_sql = leer_mysql()

    # Validar que ninguna extracción haya fallado críticamente
    if df_api is None or df_csv is None or df_sql is None:
        print("\n[ERROR] Una o más fuentes fallaron al extraerse. Pipeline abortado.")
        return

    print("\n[OK] Extracción completada con éxito.\n")

    # ----------------------------------------------------
    # FASE 2: TRANSFORM (Transformación y Cruce)
    # ----------------------------------------------------
    print(">>> FASE 2: Transformando y uniendo datasets...")
    
    # Limpiezas individuales
    df_csv_limpio = transformar_csv(df_csv)
    df_api_limpio = transformar_api(df_api)
    df_sql_limpio = transformar_sql(df_sql)

    # Cruces (Uniones)
    print("\nUniendo Ventas con Feriados de la API...")
    df_unido = unir_ventas_feriados(df_csv_limpio, df_api_limpio)
    
    print("Uniendo Resultado con Metas de MySQL...")
    df_consolidado = unir_metas(df_unido, df_sql_limpio)

    # Feature Engineering (Nuevas variables)
    print("Creando variables derivadas para análisis...")
    df_final = crear_variables(df_consolidado)

    # Control de calidad opcional en pantalla
    revisar_transformacion(df_final)
    print("\n[OK] Transformación completada con éxito.\n")

    # ----------------------------------------------------
    # FASE 3: LOAD (Carga y Guardado)
    # ----------------------------------------------------
    print(">>> FASE 3: Guardando datos procesados y cargando a MySQL...")
    
    # 3.1 GUARDAR COPIA LOCAL EN DATA/PROCESSED
    ruta_procesado = "data/processed/clean_superstore_climate.csv"
    try:
        # Creamos la carpeta si por alguna razón no existiera
        os.makedirs(os.path.dirname(ruta_procesado), exist_ok=True)
        
        # Guardamos el DataFrame final
        df_final.to_csv(ruta_procesado, index=False, encoding="utf-8")
        print(f"[OK] Archivo final guardado localmente en: {ruta_procesado}")
    except Exception as e:
        print(f"[WARN] No se pudo guardar el CSV local en processed: {e}")

    # 3.2 MOSTRAR REVISIÓN DE CARGA
    revisar_carga(df_final)
    
    # 3.3 CARGA FINAL EN LA BASE DE DATOS
    cargar_mysql(df_final)
    
    print("\n==================================================")
    print("   PIPELINE FINALIZADO EXITOSAMENTE              ")
    print("==================================================")


if __name__ == "__main__":
    ejecutar_pipeline()