import pandas as pd
from sqlalchemy import create_engine


def leer_mysql():
    """
    Lee la tabla metas_ventas desde MySQL
    y devuelve un DataFrame.
    """

    try:
        ruta_conexion = (
            "mysql+mysqlconnector://"
            "root:root_password@localhost:3307/"
            "superstore_climate_db"
        )

        engine = create_engine(ruta_conexion)

        query = """
        SELECT *
        FROM metas_ventas;
        """

        df = pd.read_sql(query, engine)

        print("Dataset MySQL cargado correctamente.")

        return df

    except Exception as e:
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