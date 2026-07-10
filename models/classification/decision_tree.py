import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    cross_val_score
)

from sklearn.tree import DecisionTreeClassifier, plot_tree

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ======================================================
# CARGAR DATASET
# ======================================================

df = pd.read_csv("data/processed/clean_superstore_feriados.csv")

print("="*60)
print("DATASET")
print("="*60)
print(df.head())

# ======================================================
# VARIABLES DEL MODELO
# ======================================================

X = df[[
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
]].copy()

y = df["Cumple_Meta"]

# ======================================================
# CONVERTIR VARIABLES CATEGÓRICAS
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

print("\nCantidad de variables luego del encoding:", X.shape[1])

# ======================================================
# DIVIDIR ENTRENAMIENTO Y PRUEBA
# ======================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nEntrenamiento:", X_train.shape)
print("Prueba:", X_test.shape)

# ======================================================
# MODELO
# ======================================================

modelo = DecisionTreeClassifier(
    random_state=42
)

# ======================================================
# HIPERPARÁMETROS
# ======================================================

param_grid = {

    "criterion":[
        "gini",
        "entropy"
    ],

    "max_depth":[
        3,
        5,
        10,
        15,
        None
    ],

    "min_samples_split":[
        2,
        5,
        10
    ]

}

# ======================================================
# GRID SEARCH
# ======================================================

grid = GridSearchCV(

    estimator=modelo,

    param_grid=param_grid,

    cv=5,

    scoring="accuracy",

    n_jobs=-1

)

grid.fit(X_train, y_train)

print("\nMejores parámetros:")

print(grid.best_params_)

# ======================================================
# MEJOR MODELO
# ======================================================

modelo = grid.best_estimator_
# ======================================================
# GUARDAR MODELO
# ======================================================

joblib.dump(modelo, "data/models/decision_tree.pkl")
joblib.dump(list(X.columns), "data/models/decision_tree_columns.pkl")

print("\nModelo guardado correctamente en:")
print("data/models/decision_tree.pkl")
# ======================================================
# PREDICCIONES
# ======================================================

y_train_pred = modelo.predict(X_train)

y_test_pred = modelo.predict(X_test)

# ======================================================
# MÉTRICAS
# ======================================================

print("\n")

print("="*60)
print("ENTRENAMIENTO")
print("="*60)

acc_train = accuracy_score(y_train,y_train_pred)

print("Accuracy:",acc_train)

print("\n")

print("="*60)
print("PRUEBA")
print("="*60)

acc_test = accuracy_score(y_test,y_test_pred)

print("Accuracy :",accuracy_score(y_test,y_test_pred))

print("Precision:",precision_score(y_test,y_test_pred))

print("Recall:",recall_score(y_test,y_test_pred))

print("F1 Score:",f1_score(y_test,y_test_pred))

print("\n")

print(classification_report(y_test,y_test_pred))

# ======================================================
# MATRIZ DE CONFUSIÓN
# ======================================================

cm = confusion_matrix(y_test,y_test_pred)

disp = ConfusionMatrixDisplay(cm)

disp.plot()

plt.title("Matriz de Confusión")

plt.show()

# ======================================================
# VALIDACIÓN CRUZADA
# ======================================================

cv = cross_val_score(

    modelo,

    X,

    y,

    cv=5,

    scoring="accuracy"

)

print("\n")

print("="*60)
print("VALIDACIÓN CRUZADA")
print("="*60)

print("Accuracy por Fold")

print(cv)

print()

print("Accuracy promedio:",cv.mean())

# ======================================================
# IMPORTANCIA DE VARIABLES
# ======================================================

importancias = pd.Series(

    modelo.feature_importances_,

    index=X.columns

)

importancias = importancias.sort_values(ascending=False)

print("\n")

print("="*60)

print("IMPORTANCIA VARIABLES")

print("="*60)

print(importancias.head(15))

plt.figure(figsize=(10,6))

importancias.head(15).plot(kind="barh")

plt.title("Importancia de Variables")

plt.xlabel("Importancia")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.show()

# ======================================================
# ÁRBOL
# ======================================================

plt.figure(figsize=(20,10))

plot_tree(

    modelo,

    filled=True,

    feature_names=X.columns,

    class_names=["No Cumple","Cumple"],

    max_depth=3,

    fontsize=8

)

plt.show()

# ======================================================
# ANÁLISIS
# ======================================================

print("\n")

print("="*60)

print("ANÁLISIS")

print("="*60)

print("Accuracy entrenamiento:",round(acc_train,4))

print("Accuracy prueba:",round(acc_test,4))

diferencia = abs(acc_train-acc_test)

if diferencia < 0.05:

    print("\nEl modelo presenta buen equilibrio entre entrenamiento y prueba.")

    print("No se observan signos importantes de overfitting.")

elif acc_train > acc_test:

    print("\nExiste evidencia de OVERFITTING.")

    print("El modelo aprende muy bien entrenamiento pero pierde capacidad de generalización.")

else:

    print("\nExiste evidencia de UNDERFITTING.")

    print("El modelo no logra aprender correctamente los patrones del conjunto de entrenamiento.")

