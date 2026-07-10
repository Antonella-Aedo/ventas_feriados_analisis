CREATE DATABASE IF NOT EXISTS superstore_feriados_db;

USE superstore_feriados_db;

-- 1. TABLA: METAS DE VENTAS (Tabla Maestra / Configuración de Negocio)
-- DESCRIPCIÓN: 
-- Esta tabla actúa como una fuente maestra de parámetros de negocio. Contiene los 
-- objetivos financieros (metas de ventas) mínimos exigidos para cada región geográfica.
--
-- FUNCIÓN EN EL ETL:
-- Sirve como punto de referencia estático. Durante la fase de transformación, el pipeline 
-- lee estos valores para compararlos contra las ventas reales acumuladas de cada región 
-- y así determinar si se cumplieron o no los objetivos comerciales establecidos.

CREATE TABLE IF NOT EXISTS metas_ventas (
    id_meta INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(50) NOT NULL,
    meta_ventas DECIMAL(12,2) NOT NULL
);

DELETE FROM metas_ventas;

INSERT INTO metas_ventas (region, meta_ventas)
VALUES
('Central', 8883.71),
('East', 9847.34),
('South', 6850.16),
('West', 14007.73);


-- 2. TABLA: DATA WAREHOUSE FINAL (dw_superstore_climate)
-- DESCRIPCIÓN:
-- Es el repositorio central consolidado e integrado (Data Warehouse) del proyecto. 
-- No contiene datos sueltos, sino la información completamente unificada, limpia 
-- y enriquecida tras la ejecución del proceso ETL.
--
-- FUNCIÓN EN EL ETL / NEGOCIO:
-- Es el destino final de la Fase de Carga (Load). Almacena el historial completo de 
-- transacciones cruzando tres dimensiones críticas: el detalle de las ventas físicas, 
-- el calendario de feriados nacionales y el estatus de cumplimiento de metas corporativas.
-- Está optimizada para alimentar directamente las métricas y gráficos del Dashboard final.

CREATE TABLE IF NOT EXISTS dw_superstore_feriados (

    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Información Operativa de la Venta (Origen: CSV)
    order_id VARCHAR(50),
    order_date DATE,
    ship_date DATE,
    customer_id VARCHAR(50),
    region VARCHAR(50),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    product_name VARCHAR(255),
    sales DECIMAL(12,2),
    quantity INT,
    discount DECIMAL(5,2),
    profit DECIMAL(12,2),

    -- Información de Metas Corporativas (Origen: Cruce con MySQL `metas_ventas`)
    meta_ventas DECIMAL(12,2),

    -- Información de Contexto Comercial (Origen: API de Feriados)
    nombre_feriado VARCHAR(150),
    es_feriado BOOLEAN,

    -- Variable Derivada / Feature Engineering (Calculada en Python)
    estado_meta VARCHAR(30),

    -- Auditoría de Datos (Fecha y hora exacta en la que el ETL insertó el registro)
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);