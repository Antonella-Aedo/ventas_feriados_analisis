CREATE DATABASE IF NOT EXISTS superstore_climate_db;

USE superstore_climate_db;

-- ========================================
-- TABLA DE METAS DE VENTAS
-- ========================================

CREATE TABLE IF NOT EXISTS metas_ventas (
    id_meta INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(50) NOT NULL,
    meta_ventas DECIMAL(12,2) NOT NULL
);

INSERT INTO metas_ventas (region, meta_ventas)
VALUES
('West', 50000),
('East', 45000),
('South', 30000),
('Central', 40000);

-- ========================================
-- DATA WAREHOUSE FINAL
-- ========================================

CREATE TABLE IF NOT EXISTS dw_superstore_climate (

    id INT AUTO_INCREMENT PRIMARY KEY,

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

    meta_ventas DECIMAL(12,2),

    nombre_feriado VARCHAR(150),

    es_feriado BOOLEAN,

    estado_meta VARCHAR(30),

    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);