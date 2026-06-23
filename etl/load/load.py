import os

from sqlalchemy import create_engine


def cargar_env_desde_archivo():
    """Carga variables de entorno desde el archivo .env de la raíz del proyecto."""
    ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    ruta_env = os.path.join(ruta_raiz, ".env")

    if not os.path.exists(ruta_env):
        return

    with open(ruta_env, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, valor = linea.split("=", 1)
            clave = clave.strip()
            valor = valor.strip().strip('"').strip("'")
            if clave and clave not in os.environ:
                os.environ[clave] = valor


cargar_env_desde_archivo()


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



def obtener_ruta_conexion_mysql(host=None, port=None):
    return (
        "mysql+mysqlconnector://"
        f"{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{host or os.getenv('MYSQL_HOST')}:{port or os.getenv('MYSQL_PORT')}/"
        f"{os.getenv('MYSQL_DATABASE')}"
    )


def cargar_mysql(df):
    try:
        ruta_conexion = obtener_ruta_conexion_mysql()
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
        if os.getenv("MYSQL_HOST") == "db":
            try:
                ruta_conexion = obtener_ruta_conexion_mysql(host="localhost", port="3307")
                engine = create_engine(ruta_conexion)
                df.to_sql(
                    name="dw_superstore_c",
                    con=engine,
                    if_exists="append",
                    index=False
                )
                print("\nDatos cargados correctamente en MySQL con localhost:3307.")
                print("Tabla destino:superstore_feriados_db")
                return
            except Exception as e2:
                print(f"\nError durante la carga en el reintento: {e2}")
                return

        print(f"\nError durante la carga: {e}")