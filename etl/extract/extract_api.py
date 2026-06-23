import os
import sys
import pandas as pd

# Configurar rutas dinámicas
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_raiz = os.path.abspath(os.path.join(ruta_actual, "..", ".."))

if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

from api.feriados import consultar_feriados


def leer_api(anio):
    """
    Obtiene los feriados desde la API
    y los transforma en DataFrame.
    """

    try:
        datos_json = consultar_feriados(anio)

        if datos_json is None:
            print("No se recibieron datos desde la API.")
            return None

        df = pd.DataFrame(datos_json)

        df = df[["date", "localName", "name"]]

        df = df.rename(columns={
            "date": "Fecha",
            "localName": "Nombre_Local",
            "name": "Nombre_Feriado"
        })
        print("Dataset de feriados cargado correctamente.")

        return df

    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        return None


def revisar_datos(df):

    print("\n===== REVISION DEL DATASET DE LA API =====")

    print("\nPrimeras filas:")
    print(df.head())

    print("\nDimensiones:")
    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")

    print("\nInformacion general:")
    df.info()

    print("\nTipos de datos:")
    print(df.dtypes)

    print("\nValores nulos:")
    print(df.isnull().sum())

    print("\nRegistros duplicados:")
    print(df.duplicated().sum())

    print("\nEstadisticas descriptivas:")
    print(df.describe(include="all"))


if __name__ == "__main__":

    feriados = leer_api(2016)

    if feriados is not None:
        revisar_datos(feriados)