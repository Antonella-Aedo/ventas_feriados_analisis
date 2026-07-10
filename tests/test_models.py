import joblib
import pandas as pd
'''
Se desarrolló un script para cargar el modelo almacenado en formato .pkl y realizar predicciones sobre nuevos registros. Esto permitió verificar que el modelo entrenado puede reutilizarse sin necesidad de volver a entrenarlo, facilitando su integración con el dashboard desarrollado en Streamlit.

'''
# ======================================================
# CARGAR MODELO
# ======================================================

modelo = joblib.load("data/models/decision_tree.pkl")
columnas = joblib.load("data/models/decision_tree_columns.pkl")

print("Modelo cargado correctamente.")

# ======================================================
# CARGAR DATOS
# ======================================================

df = pd.read_csv("data/processed/clean_superstore_feriados.csv")

# Tomar un registro como ejemplo
nuevo = df.iloc[[0]]

X = nuevo[[
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
]]

# ======================================================
# MISMO PREPROCESAMIENTO DEL ENTRENAMIENTO
# ======================================================

X = pd.get_dummies(
    X,
    columns=[
        "Region",
        "Category",
        "Sub-Category",
        "Segment",
        "Ship Mode",
        "Dia_Semana"
    ],
    drop_first=True
)

# Agregar columnas faltantes
X = X.reindex(columns=columnas, fill_value=0)

# ======================================================
# PREDICCIÓN
# ======================================================

pred = modelo.predict(X)

print("Predicción:", pred[0])

if pred[0] == 1:
    print("Resultado: Cumple Meta Regional")
else:
    print("Resultado: Venta Regular")