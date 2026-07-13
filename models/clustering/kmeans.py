"""
Modelo no supervisado K-Means para el proyecto Superstore.

Este archivo:
1. Carga el dataset procesado.
2. Selecciona las variables Sales, Quantity, Discount y Profit.
3. Estandariza las variables.
4. Busca una cantidad adecuada de clusters.
5. Entrena el modelo K-Means.
6. Evalúa el modelo con Silhouette Score.
7. Guarda el modelo entrenado en formato .pkl.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS
# ---------------------------------------------------------

# Obtiene automáticamente la carpeta principal del proyecto.
BASE_DIR = Path(__file__).resolve().parents[2]

# Ruta del dataset limpio.
DATASET_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "clean_superstore_feriados.csv"
)

# Ruta donde se guardará el modelo entrenado.
MODEL_PATH = (
    BASE_DIR
    / "data"
    / "models"
    / "kmeans.pkl"
)

# Ruta donde se guardarán las columnas utilizadas.
COLUMNS_PATH = (
    BASE_DIR
    / "data"
    / "models"
    / "kmeans_columns.pkl"
)


# ---------------------------------------------------------
# 2. COLUMNAS PARA EL MODELO
# ---------------------------------------------------------

# Variables numéricas utilizadas para agrupar los registros.
COLUMNAS_MODELO = [
    "Sales",
    "Quantity",
    "Discount",
    "Profit",
]

# ---------------------------------------------------------
# 3. CARGA DEL DATASET
# ---------------------------------------------------------

def cargar_datos() -> pd.DataFrame:
    """
    Carga el dataset procesado desde la carpeta data/processed.

    Returns:
        DataFrame con los datos procesados.
    """

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el dataset en la ruta: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    if df.empty:
        raise ValueError("El dataset está vacío.")

    print("Dataset cargado correctamente.")
    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")

    return df


# ---------------------------------------------------------
# 4. PREPARACIÓN DE LOS DATOS
# ---------------------------------------------------------

def preparar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Selecciona las columnas necesarias y elimina valores inválidos.

    Args:
        df: Dataset completo.

    Returns:
        DataFrame con las variables utilizadas por K-Means.
    """

    # Comprueba que todas las columnas necesarias existan.
    columnas_faltantes = [
        columna
        for columna in COLUMNAS_MODELO
        if columna not in df.columns
    ]

    if columnas_faltantes:
        print("\nColumnas disponibles en el dataset:")
        print(df.columns.tolist())

        raise ValueError(
            "No se encontraron estas columnas necesarias: "
            f"{columnas_faltantes}"
        )

    # Crea una copia solo con las columnas utilizadas.
    datos = df[COLUMNAS_MODELO].copy()

    # Convierte los valores a formato numérico.
    for columna in COLUMNAS_MODELO:
        datos[columna] = pd.to_numeric(
            datos[columna],
            errors="coerce"
        )

    # Elimina filas que tengan valores nulos.
    filas_antes = len(datos)

    datos = datos.dropna()

    filas_despues = len(datos)

    print(
        f"Filas eliminadas por valores nulos: "
        f"{filas_antes - filas_despues}"
    )

    if datos.empty:
        raise ValueError(
            "No quedaron datos válidos para entrenar el modelo."
        )

    return datos


# ---------------------------------------------------------
# 5. BÚSQUEDA DE LA CANTIDAD DE CLUSTERS
# ---------------------------------------------------------

def buscar_mejor_k(datos: pd.DataFrame) -> tuple[int, float]:
    """
    Prueba diferentes cantidades de clusters entre 2 y 6.

    Para evitar tiempos de ejecución demasiado largos, utiliza una
    muestra representativa del dataset para seleccionar el mejor k.

    Args:
        datos: Variables numéricas preparadas.

    Returns:
        Tupla con el mejor número de clusters y su puntuación.
    """

    # Se utiliza una muestra para acelerar la búsqueda del mejor k.
    # El modelo final se entrenará posteriormente con todos los registros.
    cantidad_muestra = min(2000, len(datos))

    datos_muestra = datos.sample(
        n=cantidad_muestra,
        random_state=42
    )

    scaler = StandardScaler()

    datos_escalados = scaler.fit_transform(datos_muestra)

    mejor_k = 2
    mejor_puntuacion = -1.0

    print(
        f"\nBuscando el mejor k con una muestra de "
        f"{cantidad_muestra} registros."
    )

    print("\nEvaluación de diferentes cantidades de clusters:")

    for k in range(2, 7):

        modelo = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        etiquetas = modelo.fit_predict(datos_escalados)

        puntuacion = silhouette_score(
            datos_escalados,
            etiquetas,
            sample_size=min(500, cantidad_muestra),
            random_state=42
        )

        print(
            f"k = {k} | "
            f"Silhouette Score = {puntuacion:.4f}"
        )

        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_k = k

    print(f"\nMejor cantidad de clusters: {mejor_k}")

    print(
        f"Mejor Silhouette Score: "
        f"{mejor_puntuacion:.4f}"
    )

    return mejor_k, mejor_puntuacion


# ---------------------------------------------------------
# 6. ENTRENAMIENTO DEL MODELO
# ---------------------------------------------------------

def entrenar_modelo(
    datos: pd.DataFrame,
    numero_clusters: int
) -> Pipeline:
    """
    Crea un pipeline con StandardScaler y K-Means.

    Args:
        datos: Variables del modelo.
        numero_clusters: Cantidad de grupos seleccionada.

    Returns:
        Pipeline entrenado.
    """

    pipeline = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler()
            ),
            (
                "kmeans",
                KMeans(
                    n_clusters=numero_clusters,
                    random_state=42,
                    n_init=10
                )
            )
        ]
    )

    pipeline.fit(datos)

    print("\nModelo K-Means entrenado correctamente.")

    return pipeline


# ---------------------------------------------------------
# 7. RESUMEN DE LOS CLUSTERS
# ---------------------------------------------------------

def mostrar_resumen(
    modelo: Pipeline,
    datos: pd.DataFrame
) -> None:
    """
    Muestra cuántos registros quedaron en cada cluster.

    Args:
        modelo: Pipeline entrenado.
        datos: Datos utilizados para el entrenamiento.
    """

    etiquetas = modelo.predict(datos)

    resumen = (
        pd.Series(etiquetas, name="Cluster")
        .value_counts()
        .sort_index()
    )

    print("\nCantidad de registros por cluster:")
    print(resumen)


# ---------------------------------------------------------
# 8. GUARDADO DEL MODELO
# ---------------------------------------------------------

def guardar_modelo(modelo: Pipeline) -> None:
    """
    Guarda el modelo y las columnas utilizadas.

    Args:
        modelo: Pipeline K-Means entrenado.
    """

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Guarda el pipeline completo.
    joblib.dump(
        modelo,
        MODEL_PATH
    )

    # Guarda las columnas necesarias para usar el modelo.
    joblib.dump(
        COLUMNAS_MODELO,
        COLUMNS_PATH
    )

    print(
        f"\nModelo guardado correctamente en:\n{MODEL_PATH}"
    )

    print(
        f"\nColumnas guardadas correctamente en:\n{COLUMNS_PATH}"
    )


# ---------------------------------------------------------
# 9. EJECUCIÓN PRINCIPAL
# ---------------------------------------------------------

def main() -> None:
    """
    Ejecuta el proceso completo de entrenamiento.
    """

    print("=" * 60)
    print("ENTRENAMIENTO DEL MODELO K-MEANS")
    print("=" * 60)

    df = cargar_datos()

    datos = preparar_datos(df)

    print("\nColumnas utilizadas:")
    print(COLUMNAS_MODELO)

    print(
        f"\nRegistros utilizados para entrenar: "
        f"{len(datos)}"
    )

    mejor_k, mejor_puntuacion = buscar_mejor_k(datos)

    modelo = entrenar_modelo(
        datos=datos,
        numero_clusters=mejor_k
    )

    mostrar_resumen(
        modelo=modelo,
        datos=datos
    )

    guardar_modelo(modelo)

    print("\nResumen final:")

    print(
        f"- Número de clusters: {mejor_k}"
    )

    print(
        f"- Silhouette Score: {mejor_puntuacion:.4f}"
    )

    print(
        "- Modelo generado correctamente para "
        "su integración en el dashboard."
    )

    print("=" * 60)


if __name__ == "__main__":
    main()