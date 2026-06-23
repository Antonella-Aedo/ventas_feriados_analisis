import pandas as pd
# Archivo 
# Lee el archivo CSV y devuelve un DataFrame.
def leer_csv(ruta_csv):
    try:
        df = pd.read_csv(ruta_csv)
        print(" Dataset cargado correctamente.")
        return df

    except FileNotFoundError:
        print(" No se encontró el archivo.")
        return None

    except Exception as e:
        print(f" Error al leer el CSV: {e}")
        return None
# Muestra información básica del dataset.
def revisar_datos(df):
    """
    Revisa información general del dataset.
    """

    print("\n===== REVISIÓN DEL DATASET =====")

    print("\nPrimeras filas:")
    print(df.head())

    print("\nDimensiones:")
    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")

    print("\nInformación general:")
    df.info()

    print("\nTipos de datos:")
    print(df.dtypes)

    print("\nValores nulos:")
    print(df.isnull().sum())

    print("\nRegistros duplicados:")
    print(df.duplicated().sum())

    print("\nEstadísticas descriptivas:")
    print(df.describe())

if __name__ == "__main__":

    ruta = "data/raw/Sample_ Superstore.csv"

    ventas = leer_csv(ruta)

    revisar_datos(ventas)