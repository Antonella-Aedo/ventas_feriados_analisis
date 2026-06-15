import pandas as pd

# =====================================================
# TRANSFORMACIONES DEL CSV (VENTAS)
# =====================================================

def transformar_csv(ventas):
    """
    Limpia y transforma el dataset de ventas.
    """

    # Convertir fechas
    ventas["Order Date"] = pd.to_datetime(
        ventas["Order Date"],
        errors="coerce"
    )

    ventas["Ship Date"] = pd.to_datetime(
        ventas["Ship Date"],
        errors="coerce"
    )

    # Revisar nulos
    print("\n===== NULOS CSV =====")
    print(ventas.isnull().sum())

    # Eliminar duplicados
    duplicados = ventas.duplicated().sum()

    print(f"\nDuplicados CSV: {duplicados}")

    ventas = ventas.drop_duplicates()

    return ventas

# =====================================================
# TRANSFORMACIONES DE LA API (FERIADOS)
# =====================================================

def transformar_api(feriados):
    """
    Limpia y transforma los datos obtenidos desde la API.
    """

    # Convertir fecha
    feriados["Fecha"] = pd.to_datetime(
        feriados["Fecha"],
        errors="coerce"
    )

    # Revisar nulos
    print("\n===== NULOS API =====")
    print(feriados.isnull().sum())

    # Eliminar duplicados
    feriados = feriados.drop_duplicates()

    return feriados

# =====================================================
# TRANSFORMACIONES MYSQL (METAS)
# =====================================================

def transformar_sql(metas):
    """
    Limpia el dataset proveniente de MySQL.
    """

    # Eliminar espacios
    metas["region"] = metas["region"].str.strip()

    # Revisar nulos
    print("\n===== NULOS MYSQL =====")
    print(metas.isnull().sum())

    # Eliminar duplicados
    metas = metas.drop_duplicates()

    return metas

# =====================================================
# UNIR CSV + API
# =====================================================

def unir_ventas_feriados(ventas, feriados):
    """
    Une las ventas con los feriados.
    """

    df = ventas.merge(
        feriados,
        left_on="Order Date",
        right_on="Fecha",
        how="left"
    )

    return df

# =====================================================
# UNIR RESULTADO + MYSQL
# =====================================================

def unir_metas(df, metas):
    """
    Une el dataset anterior con las metas de ventas.
    """

    df = df.merge(
        metas,
        left_on="Region",
        right_on="region",
        how="left"
    )

    return df

# =====================================================
# CREAR VARIABLES NUEVAS
# =====================================================

def crear_variables(df):
    """
    Crea nuevas variables para el análisis.
    """

    # Indica si la venta fue realizada en un feriado
    df["Es_Feriado"] = (
        df["Nombre_Feriado"].notnull()
    )

    # Año de la venta
    df["Año"] = (
        df["Order Date"].dt.year
    )

    # Mes de la venta
    df["Mes"] = (
        df["Order Date"].dt.month
    )

    # Día de la semana
    df["Dia_Semana"] = (
        df["Order Date"].dt.day_name()
    )

    # Indica si la venta supera la meta regional
    df["Cumple_Meta"] = (
        df["Sales"] >= df["meta_ventas"]
    )

    return df

# =====================================================
# REVISIÓN DEL DATASET FINAL
# =====================================================

def revisar_transformacion(df):
    """
    Muestra información del dataset transformado.
    """

    print("\n===== DATASET TRANSFORMADO =====")

    print("\nPrimeras filas:")
    print(df.head())

    print("\nDimensiones:")
    print(df.shape)

    print("\nValores nulos:")
    print(df.isnull().sum())

    print("\nDuplicados:")
    print(df.duplicated().sum())