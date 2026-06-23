from sqlalchemy import create_engine

import os


# =====================================================
# REVISAR CARGA
# =====================================================

def revisar_carga(df):
    """
    Muestra información del DataFrame que será cargado.
    """


    print("\n===== DATASET A CARGAR =====")

    print("\nPrimeras filas:")
    print(df.head())

    print("\nCantidad de filas:")
    print(df.shape[0])

    print("\nCantidad de columnas:")
    print(df.shape[1])



def cargar_mysql(df):
    try:
        ruta_conexion = (
            "mysql+mysqlconnector://"
            f"{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
            f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/"
            f"{os.getenv('MYSQL_DATABASE')}"
        )

        engine = create_engine(ruta_conexion)

        df.to_sql(
            name="dw_superstore_c",
            con=engine,
            if_exists="append",
            index=False
        )

        print("\nDatos cargados correctamente en MySQL.")

        print("Tabla destino:superstore_feriados_db")


    except Exception as e:
        print(f"\nError durante la carga: {e}")