import joblib
import pandas as pd

"""
Prueba de funcionamiento de los modelos de Machine Learning.

Este script verifica que los modelos almacenados en formato .pkl
pueden cargarse correctamente y realizar predicciones sobre nuevos
registros sin necesidad de volver a entrenarlos.
"""

# ======================================================
# CARGAR Y PREPARAR DATOS
# ======================================================

def preparar_datos(columnas_modelo):
    """
    Carga el dataset y aplica el mismo preprocesamiento
    utilizado durante el entrenamiento.
    """

    df = pd.read_csv("data/processed/clean_superstore_feriados.csv")

    nuevo = df.iloc[[0]]

    X = nuevo[columnas_modelo].copy()

    columnas_categoricas = [
        c for c in [
            "Region",
            "Category",
            "Sub-Category",
            "Segment",
            "Ship Mode",
            "Dia_Semana"
        ] if c in X.columns
    ]

    if columnas_categoricas:
        X = pd.get_dummies(
            X,
            columns=columnas_categoricas,
            drop_first=True
        )

    return X


# ======================================================
# TEST ÁRBOL DE DECISIÓN
# ======================================================

def test_decision_tree():

    print("\n==============================")
    print("TEST DECISION TREE")
    print("==============================")

    modelo = joblib.load("data/models/decision_tree.pkl")
    columnas = joblib.load("data/models/decision_tree_columns.pkl")

    X = preparar_datos([
        "Sales",
        "Profit",
        "Discount",
        "Quantity",
        "Region",
        "Category",
        "Sub-Category",
        "Segment",
        "Ship Mode",
        "Es_Feriado",
        "Mes",
        "Dia_Semana"
    ])

    X = X.reindex(columns=columnas, fill_value=0)

    pred = modelo.predict(X)

    print("Predicción:", pred[0])

    if pred[0] == 1:
        print("Resultado: Cumple Meta Regional")
    else:
        print("Resultado: Venta Regular")


# ======================================================
# TEST K-MEANS
# ======================================================

def test_kmeans():

    print("\n==============================")
    print("TEST K-MEANS")
    print("==============================")

    modelo = joblib.load("data/models/kmeans.pkl")

    X = preparar_datos([
        "Sales",
        "Quantity",
        "Discount",
        "Profit"
    ])

    # El Pipeline ya contiene StandardScaler + KMeans
    cluster = modelo.predict(X)

    print(f"Cluster asignado: {cluster[0]}")

    assert len(cluster) == 1

    print("Modelo funcionando correctamente.")


# ======================================================
# EJECUCIÓN
# ======================================================

if __name__ == "__main__":

    test_decision_tree()
    test_kmeans()