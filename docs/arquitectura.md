# Arquitectura del Proyecto

## Descripción General

El proyecto integra información de tres fuentes distintas:

1. Archivo CSV de ventas Superstore.
2. API pública Nager.Date para obtener feriados de Estados Unidos.
3. Base de datos MySQL con metas corporativas.

Los datos son procesados mediante un pipeline ETL y posteriormente visualizados en un dashboard interactivo desarrollado con Streamlit.

## Arquitectura de Proyecto

C:.
│   .env
│   .gitignore
│   docker-compose.yml
│   Dockerfile
│   README.md
│   requirements.txt
│   
├───api
│   │   feriados.py
│   │   
│   └───__pycache__
│           feriados.cpython-313.pyc
│           openmeteo.cpython-313.pyc
│           
├───dashboard
│       app.py
│       
├───data
│   ├───database
│   │       init.sql
│   │       
│   ├───processed
│   │       clean_superstore_feriados.csv
│   │       
│   └───raw
│           Sample_ Superstore.csv
│           
├───docs
│       api_documentacion.md
│       arquitectura.md
│       guia_despliegue.md
│       manual_usuario.md
│       
├───etl
│   ├───extract
│   │   │   extract_api.py
│   │   │   extract_csv.py
│   │   │   extract_sql.py
│   │   │   
│   │   └───__pycache__
│   │           extract_api.cpython-313.pyc
│   │           extract_csv.cpython-313.pyc
│   │           extract_sql.cpython-313.pyc
│   │           
│   ├───load
│   │   │   load.py
│   │   │   
│   │   └───__pycache__
│   │           load.cpython-313.pyc
│   │           
│   ├───pipeline
│   │       pipeline.py
│   │       
│   └───transform
│       │   transform.py
│       │   
│       └───__pycache__
│               transform.cpython-313.pyc
│               
└───tests
        test_extract.py
        test_load.py
        test_transform.py
            

## Diagrama de Arquitectura

```text
                    +-------------------+
                    |   API Nager.Date  |
                    +---------+---------+
                              |
                              v
+----------------+     +-------------+
| CSV Superstore | --> |   ETL       |
+----------------+     | Extract     |
                       | Transform    |
+----------------+ --> | Load         |
| MySQL Metas    |     +------+-------+
+----------------+            |
                              v
                 +------------------------+
                 | Dataset Consolidado    |
                 | clean_superstore_      |
                 | feriados.csv           |
                 +------------+-----------+
                              |
                              v
                    +------------------+
                    | Dashboard        |
                    | Streamlit        |
                    +------------------+
```

## Componentes

### Extract

* extract_csv.py
* extract_api.py
* extract_sql.py

### Transform

* Limpieza de datos
* Integración de fuentes
* Creación de variables derivadas

### Load

* Carga de información consolidada
* Exportación de dataset final

### Visualización

Dashboard interactivo desarrollado con Streamlit.
