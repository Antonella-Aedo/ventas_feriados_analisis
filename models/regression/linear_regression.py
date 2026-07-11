import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. CARGAR LOS DATOS
# Ajusta la ruta si tus datos procesados están en otro archivo dentro de data/processed/
data_path = os.path.join("data", "processed", "clean_superstore_feriados.csv") 

if not os.path.exists(data_path):
    # Si no encuentra el procesado, intentamos buscar en la raíz de data por si acaso
    data_path = os.path.join("data", "data.csv")

df = pd.read_csv(data_path)

# 2. SELECCIÓN DE VARIABLES (Según tu plan de trabajo)
# Variables predictoras asignadas a Benjamín
features = [
    'Quantity', 'Discount', 'Profit', 'Category', 'Sub-Category', 
    'Segment', 'Region', 'Es_Feriado', 'Mes', 'Dia_Semana'
]
# Variable objetivo asignada a Benjamín
target = 'Sales'

# Convertir variables categóricas a numéricas (One-Hot Encoding) automáticamente
X = pd.get_dummies(df[features], drop_first=True)
y = df[target]

# 3. DIVISIÓN DE DATOS (80% Entrenamiento, 20% Prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# 4. ENTRENAMIENTO DEL MODELO (Hiperparámetro: fit_intercept)
model = LinearRegression(fit_intercept=True)
model.fit(X_train, y_train)

# 5. VALIDACIÓN CRUZADA (Cross Validation)
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
print(f"Validación Cruzada (R2 promedio en 5 folds): {np.mean(cv_scores):.4f}")

# 6. EVALUACIÓN CON MÉTRICAS REQUERIDAS
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n--- Métricas de Evaluación ---")
print(f"MAE (Error Absoluto Medio): {mae:.2f}")
print(f"RMSE (Raíz del Error Cuadrático Medio): {rmse:.2f}")
print(f"R² (Coeficiente de Determinación): {r2:.4f}")

# 7. GUARDAR EL MODELO EN FORMATO PKL
# Asegurar que exista la carpeta donde se guardará
output_dir = os.path.join("data", "models")
os.makedirs(output_dir, exist_ok=True)

pkl_path = os.path.join(output_dir, "linear_regression.pkl")

with open(pkl_path, "wb") as f:
    pickle.dump(model, f)

print(f"\n¡Éxito! Modelo guardado correctamente en: {pkl_path}")