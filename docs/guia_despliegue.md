# Guía de Despliegue

## Requisitos

* Docker Desktop
* Python 3.13
* Git

## Clonar Proyecto

```bash
git clone <repositorio>
cd ventas_feriados_analisis
```

## Crear Entorno Virtual

```bash
python -m venv venv
```

Activar:

```bash
venv\Scripts\activate
```

## Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Levantar Base de Datos

```bash
docker-compose up -d
```

## Ejecutar ETL

```bash
python etl/pipeline/pipeline.py
```

## Ejecutar Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard disponible en:

http://localhost:8501
