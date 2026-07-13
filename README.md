# 📊 Análisis de Ventas y Feriados mediante Pipeline ETL

## Descripción del Proyecto

Este proyecto implementa un proceso ETL (Extract, Transform, Load) para integrar información proveniente de múltiples fuentes de datos y generar un conjunto de datos consolidado para análisis de ventas.

Las fuentes utilizadas son:

* Dataset de ventas Superstore (CSV).
* API pública de feriados (Nager.Date).
* Base de datos MySQL con metas corporativas.

Los datos son procesados, limpiados e integrados para posteriormente ser visualizados mediante un dashboard interactivo desarrollado con Streamlit.

---

## Objetivo

Analizar el comportamiento de las ventas durante períodos de feriados y comparar los resultados obtenidos con las metas comerciales definidas por la organización.

---

## Arquitectura General

```text
                    +------------------+
                    | API Nager.Date   |
                    +---------+--------+
                              |
                              v

+----------------+     +-------------+     +----------------+
| CSV Superstore | --> | ETL         | <-- | MySQL Metas    |
+----------------+     | Extract     |     +----------------+
                       | Transform   |
                       | Load        |
                       +------+------+
                              |
                              v

                +--------------------------+
                | Dataset Consolidado       |
                | clean_superstore_         |
                | feriados.csv              |
                +------------+-------------+
                             |
                             v

                    +------------------+
                    | Dashboard        |
                    | Streamlit        |
                    +------------------+
```

---

## Estructura del Proyecto

```text
ventas_feriados_analisis-develop
│
├── api/
│   └── feriados.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── database/
│
├── docs/
│   ├── arquitectura.md
│   ├── api_documentacion.md
│   ├── manual_usuario.md
│   └── guia_despliegue.md
│
├── etl/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   └── pipeline/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

## Tecnologías Utilizadas

* Python 3.13
* Pandas
* NumPy
* Scikit-learn
* Joblib
* SQLAlchemy
* MySQL 8
* Streamlit
* Requests
* Docker
* Docker Compose

---

## Pipeline ETL

### Extract

Obtención de datos desde:

* Archivo CSV de ventas.
* API de feriados.
* Base de datos MySQL.

### Transform

Procesos realizados:

* Limpieza de datos.
* Eliminación de duplicados.
* Tratamiento de valores nulos.
* Conversión de tipos de datos.
* Integración de fuentes.

### Load

Carga de los datos transformados en la tabla:

```sql
dw_superstore_c
```

de la base de datos MySQL.

---

## Containerización con Docker

El proyecto se encuentra containerizado mediante Docker.

### Servicios

#### MySQL

Contenedor encargado de almacenar:

* Metas de ventas.
* Dataset consolidado.

#### Dashboard Streamlit

Contenedor encargado de:

* Ejecutar la aplicación web.
* Visualizar indicadores y análisis.

---

## Variables de Entorno

Archivo `.env`

```env
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_DATABASE=superstore_feriados_db
MYSQL_USER=root
MYSQL_PASSWORD=root_password
```

---

## Instalación

### Clonar repositorio

```bash
git clone <url-del-repositorio>
```

### Acceder al proyecto

```bash
cd ventas_feriados_analisis-develop
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecución con Docker

### Construir imágenes

```bash
docker compose build
```

### Levantar servicios

```bash
docker compose up -d
```

### Verificar contenedores

```bash
docker ps
```

---

## Ejecución del Pipeline

```bash
python etl/pipeline/pipeline.py
```

---

## Ejecutar Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard disponible en:

```text
http://localhost:8501
```

---

## Pruebas

Las pruebas unitarias se encuentran en:

```text
tests/
```

Para ejecutarlas:

```bash
pytest
```

---

## Modelos de Machine Learning

El proyecto incorpora tres modelos desarrollados con Scikit-learn para complementar el análisis de datos.

### Decision Tree

Modelo supervisado utilizado para clasificar registros según variables comerciales del dataset.

### Regresión Lineal

Modelo supervisado utilizado para estimar el comportamiento de las ventas y apoyar el análisis de tendencias.

### K-Means

Modelo de aprendizaje no supervisado utilizado para agrupar registros con características similares utilizando las variables:

- Sales
- Quantity
- Discount
- Profit

Los modelos entrenados se almacenan en:

```text
data/models/
```

y posteriormente son utilizados por el dashboard para realizar análisis y visualizaciones.

---

## Documentación

La documentación técnica se encuentra en:

* docs/arquitectura.md
* docs/api_documentacion.md
* docs/manual_usuario.md
* docs/guia_despliegue.md

---

## Autores

Antonella Aedo
Benjamin Diaz
Manuel Pizarro 

Proyecto académico desarrollado para la asignatura de Ingeniería de Datos y Analítica.
===

---

## Valor de negocio

Este proyecto permite analizar si las ventas del dataset Superstore presentan variaciones durante los días feriados en Estados Unidos.

Al integrar información histórica de ventas, metas comerciales y feriados oficiales, la organización puede identificar patrones de consumo, anticipar incrementos o disminuciones en la demanda y apoyar la toma de decisiones relacionadas con promociones, planificación de inventario y definición de metas de ventas.

Los feriados suelen modificar el comportamiento de compra de los clientes. Este análisis permite identificar cómo se comportan las ventas durante estos períodos y comparar su desempeño con las metas establecidas por la organización.

---

## Automatización

El archivo:

```text
etl/pipeline/pipeline.py
```

ejecuta automáticamente las etapas de extracción, transformación y carga de datos.

Este proceso puede programarse mediante el Programador de tareas de Windows u otras herramientas de automatización para ejecutarse periódicamente sin intervención del usuario.

