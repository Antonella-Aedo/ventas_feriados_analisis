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
