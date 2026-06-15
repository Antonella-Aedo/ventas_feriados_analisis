from sqlalchemy import create_engine

# =====================================================
# REVISAR CARGA
# =====================================================

def revisar_carga(df):
    """
    Muestra información del DataFrame que será cargado.
    """

    print("\n===== DATASET A CARGAR =====")

    print("\nPrimeras filas:")
    print(df.head())

    print("\nCantidad de filas:")
    print(df.shape[0])

    print("\nCantidad de columnas:")
    print(df.shape[1])


# =====================================================
# CARGAR DATAFRAME EN MYSQL
# =====================================================

def cargar_mysql(df):
    """
    Guarda el DataFrame transformado en la tabla
    dw_superstore_climate de MySQL.
    """

    try:
        # Cadena de conexión
        ruta_conexion = (
            "mysql+mysqlconnector://"
            "root:root_password@localhost:3307/"
            "superstore_climate_db"
        )

        # Crear conexión
        engine = create_engine(ruta_conexion)

        # Insertar los datos en la tabla final
        df.to_sql(
            name="dw_superstore_climate",
            con=engine,
            if_exists="append",
            index=False
        )

        print("\nDatos cargados correctamente en MySQL.")
        print("Tabla destino: dw_superstore_climate")

    except Exception as e:
        print(f"\nError durante la carga: {e}")