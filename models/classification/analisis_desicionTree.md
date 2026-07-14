# Análisis del Modelo - Árbol de Decisión (Decision Tree)


## Variable objetivo

La variable objetivo del modelo es Cumple_Meta, una variable binaria que indica si una región alcanzó o no la meta de ventas establecida para un determinado mes. Esta variable toma el valor 1 cuando las ventas mensuales de la región son iguales o superiores a la meta definida, y 0 cuando no se alcanza dicho objetivo.

## Objetivo de la predicción

El propósito del modelo es predecir si una región cumplirá o no su meta mensual de ventas, utilizando variables relacionadas con las ventas y las características de cada pedido. Esta predicción puede servir como apoyo para la planificación comercial y la toma de decisiones orientadas a mejorar el cumplimiento de las metas de ventas.
## 1. Desempeño General del Modelo

El árbol de decisión obtuvo un **Accuracy de 81,37%** sobre el conjunto de prueba, lo que indica que clasificó correctamente aproximadamente **8 de cada 10 registros**. Además, el accuracy de entrenamiento fue de **86,33%**, una diferencia cercana a **5 puntos porcentuales**, lo que demuestra que el modelo mantiene un comportamiento similar entre entrenamiento y prueba y no presenta un sobreajuste importante.

| Métrica | Valor |
|---------|-------:|
| Accuracy Entrenamiento | **86,33%** |
| Accuracy Prueba | **81,37%** |
| Accuracy Validación Cruzada | **79,58%** |

La validación cruzada obtuvo un promedio cercano al accuracy de prueba, lo que confirma que el modelo es relativamente estable y generaliza adecuadamente sobre datos no vistos.

---

## 2. Precision

La **Precision** obtenida fue de **85,46%**.

Esto significa que cuando el modelo predice que una región **cumplirá la meta de ventas**, aproximadamente **85 de cada 100 predicciones son correctas**.

Este resultado indica que el modelo genera una baja cantidad de falsos positivos.

---

## 3. Recall

El **Recall** fue de **88,15%**.

Esto significa que el modelo logra identificar correctamente aproximadamente el **88% de los registros que realmente cumplen la meta de ventas**.

Esta métrica es importante porque refleja la capacidad del modelo para detectar la mayor cantidad posible de casos positivos.

---

## 4. F1 Score

El modelo obtuvo un **F1 Score de 86,78%**.

El F1 Score combina Precision y Recall en una única métrica.

Al obtener valores altos en ambas métricas, el modelo presenta un buen equilibrio entre identificar correctamente los casos positivos y reducir las clasificaciones incorrectas.

---

## 5. Matriz de Confusión

La matriz de confusión obtenida fue:

| Clase Real | Predijo No Cumple | Predijo Cumple |
|------------|------------------:|---------------:|
| **No Cumple** | **405** | **209** |
| **Cumple** | **165** | **1228** |

### Interpretación

- **Verdaderos Positivos (TP): 1228**

  Son los registros que realmente cumplían la meta y el modelo los clasificó correctamente.

- **Verdaderos Negativos (TN): 405**

  Son los registros que realmente no cumplían la meta y fueron clasificados correctamente.

- **Falsos Positivos (FP): 209**

  El modelo predijo que sí cumplirían la meta, pero en realidad no la alcanzaron. Representan casos donde el modelo fue demasiado optimista.

- **Falsos Negativos (FN): 165**

  El modelo indicó que no cumplirían la meta cuando realmente sí la cumplieron.

En total, el modelo cometió **374 errores** sobre **2007 observaciones**, equivalente aproximadamente al **18,6%** del conjunto de prueba, resultado consistente con el accuracy obtenido.

---

## 6. Importancia de las Variables

Las variables con mayor influencia en las decisiones del modelo fueron:

| Variable | Importancia |
|----------|------------:|
| Mes | **57,45%** |
| Region_South | **8,65%** |
| Region_East | **5,68%** |
| Region_West | **4,84%** |
| Profit | **4,61%** |
| Sales | **3,47%** |

El árbol identifica claramente que **Mes** es la variable más importante para determinar si una región cumplirá la meta de ventas, representando más de la mitad de toda la importancia del modelo.

Las variables relacionadas con la región también aportan información relevante, mientras que variables como **Profit** y **Sales** complementan la toma de decisiones.

### ¿Por qué "Mes" es la variable más importante?

Al analizar el porcentaje de cumplimiento por mes se obtuvo:

| Mes | % Cumple Meta |
|-----|--------------:|
| Enero | 24% |
| Febrero | 9% |
| Marzo | 58% |
| Abril | 39% |
| Mayo | 50% |
| Junio | 72% |
| Julio | 53% |
| Agosto | 35% |
| Septiembre | 91% |
| Octubre | 68% |
| Noviembre | 100% |
| Diciembre | 97% |

Estos resultados muestran una **marcada estacionalidad** en las ventas:

- Enero y febrero presentan bajos niveles de cumplimiento.
- A partir de junio aumenta considerablemente el porcentaje de cumplimiento.
- Noviembre y diciembre prácticamente siempre cumplen la meta establecida.

Por este motivo, el árbol utiliza **Mes** como el primer criterio de división en la construcción del modelo.

---

## 7. Evaluación del Overfitting

No se observan señales importantes de **overfitting**.

El accuracy obtenido en entrenamiento (**86,33%**) y en prueba (**81,37%**) presenta una diferencia pequeña, mientras que la validación cruzada obtuvo un promedio de **79,58%**.

Estos resultados indican que el modelo mantiene un comportamiento consistente sobre datos no utilizados durante el entrenamiento y posee una adecuada capacidad de generalización.

---

# Conclusión

El modelo de **Árbol de Decisión (Decision Tree)** presenta un desempeño satisfactorio para predecir el cumplimiento de las metas regionales de ventas.

Obtuvo un **Accuracy de 81,37%**, una **Precision de 85,46%**, un **Recall de 88,15%** y un **F1 Score de 86,78%**, evidenciando un buen equilibrio entre identificar correctamente los casos positivos y minimizar los errores de clasificación.

La matriz de confusión mostró que el modelo clasificó correctamente **1228 registros positivos** y **405 registros negativos**, mientras que los errores correspondieron a **209 falsos positivos** y **165 falsos negativos**.

El análisis de importancia de variables permitió identificar que **Mes** es el principal factor predictivo, debido a la fuerte estacionalidad observada en las ventas, seguido por la región geográfica y variables comerciales como **Profit** y **Sales**.

En conjunto, los resultados demuestran que el modelo es **estable**, **generaliza adecuadamente** y constituye una herramienta útil para apoyar la predicción del cumplimiento de metas de ventas regionales y la toma de decisiones comerciales.