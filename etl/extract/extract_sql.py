import os
import pandas as pd

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


def obtener_ruta_conexion_mysql(host=None, port=None):
    return (
        "mysql+mysqlconnector://"
        f"{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{host or os.getenv('MYSQL_HOST')}:{port or os.getenv('MYSQL_PORT')}/"
        f"{os.getenv('MYSQL_DATABASE')}"
    )


def leer_mysql():
    """
    Lee la tabla metas_ventas desde MySQL
    y devuelve un DataFrame.
    """

    ruta_conexion = obtener_ruta_conexion_mysql()

    try:
        engine = create_engine(ruta_conexion)

        query = """
        SELECT *
        FROM metas_ventas;
        """

        df = pd.read_sql(query, engine)

        print("Dataset MySQL cargado correctamente.")

        return df

    except Exception as e:
        if os.getenv("MYSQL_HOST") == "db":
            ruta_conexion = obtener_ruta_conexion_mysql(host="localhost", port="3307")
            try:
                engine = create_engine(ruta_conexion)
                query = """
                SELECT *
                FROM metas_ventas;
                """
                df = pd.read_sql(query, engine)
                print("Dataset MySQL cargado correctamente con localhost:3307.")
                return df
            except Exception as e2:
                print(f"Error al leer MySQL en el reintento: {e2}")
                return None

        print(f"Error al leer MySQL: {e}")
        return None
def revisar_datos(df):

    print("\n===== REVISION DEL DATASET MYSQL =====")

    print("\nPrimeras filas:")
    print(df.head())

    print("\nDimensiones:")
    print(df.shape)

    print("\nInformación general:")
    df.info()

    print("\nTipos de datos:")
    print(df.dtypes)

    print("\nValores nulos:")
    print(df.isnull().sum())

    print("\nDuplicados:")
    print(df.duplicated().sum())

    print("\nEstadísticas:")
    print(df.describe())
if __name__ == "__main__":

    metas = leer_mysql()

    if metas is not None:
        revisar_datos(metas)