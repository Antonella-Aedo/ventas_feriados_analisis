import pandas as pd

# =====================================================
# TRANSFORMACIONES DEL CSV (VENTAS)
# =====================================================

def transformar_csv(ventas):
    """
    Limpia y transforma el dataset de ventas manejando formatos híbridos de fecha.
    """
    # Clonamos para evitar advertencias de memoria
    ventas = ventas.copy()

    # SOLUCIÓN MAESTRA: 'format="mixed"' procesa barras (1/29/14) y guiones (09-09-2015) a la vez
    print("Digeriendo formatos mixtos de fechas (barras, guiones y años cortos)...")
    
    ventas["Order Date"] = pd.to_datetime(
        ventas["Order Date"],
        format="mixed",
        dayfirst=False, # Mantiene la prioridad de mes primero para el formato de EE.UU. (1/29/14)
        errors="coerce"
    )

    ventas["Ship Date"] = pd.to_datetime(
        ventas["Ship Date"],
        format="mixed",
        dayfirst=False,
        errors="coerce"
    )

    # Revisar nulos (¡Verás cómo este contador ahora baja a 0!)
    print("\n===== NULOS CSV (POST-PROCESAMIENTO DE FECHAS) =====")
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
    if feriados is None or feriados.empty:
        return pd.DataFrame(columns=["Fecha", "Nombre_Local", "Nombre_Feriado"])

    feriados = feriados.copy()
    
    feriados["Fecha"] = pd.to_datetime(
        feriados["Fecha"],
        errors="coerce"
    )

    print("\n===== NULOS API =====")
    print(feriados.isnull().sum())

    feriados = feriados.drop_duplicates()

    return feriados

# =====================================================
# TRANSFORMACIONES MYSQL (METAS)
# =====================================================

def transformar_sql(metas):
    """
    Limpia el dataset proveniente de MySQL.
    """
    if metas is None or metas.empty:
        return pd.DataFrame(columns=["id_meta", "region", "meta_ventas"])

    metas = metas.copy()
    metas["region"] = metas["region"].str.strip()

    print("\n===== NULOS MYSQL =====")
    print(metas.isnull().sum())

    metas = metas.drop_duplicates()

    return metas

# =====================================================
# UNIR CSV + API
# =====================================================

def unir_ventas_feriados(ventas, feriados):
    """
    Une las ventas con los feriados utilizando la fecha como llave.
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
    Une el dataset anterior con las metas regionales.
    """

    metas = metas.rename(columns={
        "region": "Region"
    })

    df = df.merge(
        metas,
        on="Region",
        how="left"
    )

    return df

# =====================================================
# CREAR VARIABLES NUEVAS
# =====================================================

def crear_variables(df):
    """
    Crea nuevas variables temporales y de cumplimiento para el análisis.
    Reemplaza los valores nulos de la API por etiquetas descriptivas.
    """
    df = df.copy()

    # 1. REEMPLAZAR NULOS DE LA API CON UN TEXTO IDENTIFICADOR
    # Cambiamos los vacíos (NaN) por un texto claro para tus reportes
    df["Nombre_Feriado"] = df["Nombre_Feriado"].fillna("Día Regular / No Feriado")
    df["Nombre_Local"] = df["Nombre_Local"].fillna("Día Regular / No Feriado")
    
    # Para la columna 'Fecha' de la API, si estaba vacía, le copiamos la misma fecha de la venta
    df["Fecha"] = df["Fecha"].fillna(df["Order Date"])

    # 2. CALCULAR VARIABLES (Ahora basadas en las etiquetas anteriores)
    # 1 si es un feriado real (es decir, si el texto NO es "Día Regular / No Feriado"), 0 si es un día normal.
    df["Es_Feriado"] = (df["Nombre_Feriado"] != "Día Regular / No Feriado").astype(int)

    # Variables temporales extraídas de la fecha corregida
    df["Año"] = df["Order Date"].dt.year
    df["Mes"] = df["Order Date"].dt.month
    df["Dia_Semana"] = df["Order Date"].dt.day_name()

    # Define el estado de la meta que espera tu Data Warehouse final en MySQL
    df["estado_meta"] = df.apply(
        lambda row: "Cumple Meta Regional" if row["Sales"] >= row["meta_ventas"] else "Venta Regular", 
        axis=1
    )
    
    # Campo auxiliar booleano de control interno
    df["Cumple_Meta"] = (df["Sales"] >= df["meta_ventas"]).astype(int)

    return df

# =====================================================
# REVISIÓN DEL DATASET FINAL
# =====================================================

def revisar_transformacion(df):
    """
    Muestra información del dataset transformado en la consola.
    """
    print("\n===== DATASET TRANSFORMADO =====")
    print("\nPrimeras filas:")
    print(df.head(2))

    print("\nDimensiones:")
    print(df.shape)

    print("\nValores nulos:")
    print(df.isnull().sum())

    print("\nDuplicados:")
    print(df.duplicated().sum())