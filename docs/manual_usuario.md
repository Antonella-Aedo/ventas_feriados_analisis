# Manual de Usuario

## Objetivo

Permitir el análisis de ventas durante feriados mediante un dashboard interactivo.

## Inicio del Sistema

1. Levantar MySQL mediante Docker.
2. Ejecutar el pipeline ETL.
3. Ejecutar Streamlit.

## Ejecutar Pipeline

```bash
python etl/pipeline/pipeline.py
```

## Ejecutar Dashboard

```bash
streamlit run dashboard/app.py
```

## Funcionalidades

### Vista Ejecutiva

Permite visualizar:

* Ventas totales
* Cumplimiento de metas
* Comparación por año

### Vista Operativa

Permite visualizar:

* Comportamiento por región
* Inventario y categorías

### Vista Analítica

Permite visualizar:

* Tendencias históricas
* Impacto de feriados
* Variables derivadas

## Filtros Disponibles

* Región
* Año

Los filtros se encuentran en la barra lateral izquierda.

---

# Uso de los modelos de Machine Learning

El dashboard incorpora modelos de Machine Learning previamente entrenados.

Estos modelos permiten:

- Clasificar registros mediante Decision Tree.
- Estimar tendencias utilizando Regresión Lineal.
- Agrupar registros similares mediante K-Means.

Los modelos son cargados automáticamente desde:

```text
data/models/
```

Por lo tanto, el usuario no necesita volver a entrenarlos para utilizar el sistema.
