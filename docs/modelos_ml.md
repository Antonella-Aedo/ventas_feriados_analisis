# Modelos de Machine Learning

## Introducción

El proyecto incorpora modelos de aprendizaje automático desarrollados con Scikit-learn para complementar el análisis de ventas realizado sobre el dataset Superstore.

Los modelos fueron entrenados utilizando el dataset procesado generado por el pipeline ETL y posteriormente almacenados en formato `.pkl` para ser utilizados desde el dashboard.

---

# Decision Tree

## Objetivo

Clasificar registros según variables comerciales del conjunto de datos.

## Tipo de aprendizaje

Aprendizaje supervisado.

## Variables utilizadas

- Sales
- Quantity
- Discount
- Profit

## Archivo generado

```text
data/models/decision_tree.pkl
```

---

# Regresión Lineal

## Objetivo

Predecir el comportamiento de las ventas utilizando relaciones lineales entre las variables del dataset.

## Tipo de aprendizaje

Aprendizaje supervisado.

## Variables utilizadas

- Sales
- Quantity
- Discount
- Profit

## Archivo generado

```text
data/models/linear_regression.pkl
```

---

# K-Means

## Objetivo

Agrupar automáticamente registros similares mediante técnicas de aprendizaje no supervisado.

## Tipo de aprendizaje

Aprendizaje no supervisado.

## Variables utilizadas

- Sales
- Quantity
- Discount
- Profit

## Funcionamiento

El modelo realiza las siguientes etapas:

1. Carga del dataset procesado.
2. Selección de variables numéricas.
3. Estandarización mediante StandardScaler.
4. Entrenamiento del algoritmo K-Means.
5. Generación de clusters.
6. Almacenamiento del modelo entrenado.

## Archivo generado

```text
data/models/kmeans.pkl
```

---

# Librerías utilizadas

- pandas
- scikit-learn
- joblib

---

# Integración con el Dashboard

Los modelos entrenados son utilizados por el dashboard desarrollado en Streamlit para mostrar resultados predictivos y análisis de los datos sin necesidad de volver a entrenarlos en cada ejecución.