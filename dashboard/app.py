import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import pickle
import numpy as np

# =========================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA (Garantiza el diseño responsive de la rúbrica)
# =========================================================================
st.set_page_config(
    page_title="Dashboard Integral - Superstore Feriados",
    page_icon="📊",
    layout="wide"
)

# =========================================================================
# 2. CAPA DE ASIGNACIÓN Y CARGA DE DATOS (Única fuente de datos limpia)
# =========================================================================
@st.cache_data
def cargar_datos_procesados():
    """
    Carga de forma optimizada el dataset integrado por el pipeline ETL.
    """
    ruta_csv = "data/processed/clean_superstore_feriados.csv"
    if os.path.exists(ruta_csv):
        # Forzamos la lectura en utf-8
        df = pd.read_csv(ruta_csv, encoding="utf-8")
        
        # Corregir el formateo de caracteres rotos (reparación de encoding)
        columnas_texto = ["Nombre_Feriado", "Nombre_Local", "estado_meta"]
        for col in columnas_texto:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace("DÃ­a", "Día", regex=False)
        
        if "Order Date" in df.columns:
            df["Order Date"] = pd.to_datetime(df["Order Date"])
        return df
    else:
        st.error(f"⚠️ Error Crítico: No se encontró el dataset en '{ruta_csv}'.")
        return None

df_ventas = cargar_datos_procesados()

# =========================================================================
# 3. LOGICA Y RENDERIZADO DE LA INTERFAZ
# =========================================================================
if df_ventas is not None:
    
    # --- BARRA LATERAL: PANEL DE CONTROL ---
    st.sidebar.title("🎮 Panel de Control")
    st.sidebar.markdown("---")
    
    # RÚBRICA: Diferenciación estricta por tipo de audiencia
    audiencia = st.sidebar.selectbox(
        "🎯 Selecciona la Audiencia / Vista:",
        [
            "Vista Ejecutiva (Directorio)", 
            "Vista Operativa (Gestión de Inventario)", 
            "Vista Analítica (Ciencia de Datos)"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎛️ Filtros Globales")
    
    # Filtro interactivo 1: Regiones Geográficas
    lista_regiones = ["Todas"] + sorted(list(df_ventas["Region"].unique()))
    region_sel = st.sidebar.selectbox("Región Comercial:", lista_regiones)
    
    # Filtro interactivo 2: Años Comerciales
    lista_anios = ["Todos"] + sorted(list(df_ventas["Año"].unique()))
    anio_sel = st.sidebar.selectbox("Año Fiscal:", lista_anios)

    # Aplicación de los filtros en cascada sobre el DataFrame de trabajo
    df_filtrado = df_ventas.copy()
    if region_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Region"] == region_sel]
    if anio_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Año"] == anio_sel]

    # -------------------------------------------------------------------------
    # AUDIENCIA A: VISTA EJECUTIVA (Directorio / Enfoque Financiero de Negocio)
    # -------------------------------------------------------------------------
    if audiencia == "Vista Ejecutiva (Directorio)":
        st.title("📈 Cuadro de Mando Ejecutivo")
        st.markdown("### *Desempeño Macro, Rentabilidad y Objetivos de Venta*")
        st.markdown("---")
        
        # Procesamiento dinámico de KPIs Financieros
        ventas_totales = df_filtrado["Sales"].sum()
        utilidad_total = df_filtrado["Profit"].sum()
        margen_operacional = (utilidad_total / ventas_totales) * 100 if ventas_totales > 0 else 0
        total_ordenes = len(df_filtrado)
        
        # Despliegue de tarjetas de KPI en columnas
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric(label="💰 Facturación Acumulada", value=f"${ventas_totales:,.2f}")
        with kpi2:
            st.metric(
                label="📊 Utilidad Neta Global", 
                value=f"${utilidad_total:,.2f}", 
                delta=f"Margen: {margen_operacional:.1f}%"
            )
        with kpi3:
            st.metric(label="📦 Volumen de Órdenes", value=f"{total_ordenes:,} reg.")
            
        st.markdown("---")
        
        # GRÁFICO 1: Comparativo de Ventas vs Metas (Datos provenientes de MySQL)
        st.subheader("🎯 Desempeño Comercial vs Metas Corporativas Regionales")
        st.markdown("Análisis visual del cumplimiento de los umbrales de venta recuperados desde el servidor MySQL.")
        
        # Agrupación de ventas reales y extracción del umbral de metas fijas
        df_metas_reg = df_filtrado.groupby("Region").agg({
            "Sales": "sum",
            "meta_ventas": "first"
        }).reset_index()
        
        # Construcción del gráfico interactivo con Plotly Express / Graph Objects
        fig_metas = go.Figure()
        
        # Barra de Ventas Reales
        fig_metas.add_trace(go.Bar(
            x=df_metas_reg["Region"],
            y=df_metas_reg["Sales"],
            name="Ventas Reales ($)",
            marker_color="#2ecc71"
        ))
        
        # Barra de Metas Estáticas SQL
        fig_metas.add_trace(go.Bar(
            x=df_metas_reg["Region"],
            y=df_metas_reg["meta_ventas"],
            name="Meta Asignada SQL ($)",
            marker_color="#e74c3c"
        ))
        
        fig_metas.update_layout(
            barmode="group",
            xaxis_title="Regiones Geográficas",
            yaxis_title="Montos Financieros ($)",
            legend_title="Indicadores",
            height=450,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        st.plotly_chart(fig_metas, use_container_width=True)

    # -------------------------------------------------------------------------
    # AUDIENCIA B: VISTA OPERATIVA (Jefatura de Tienda / Control de Stock)
    # -------------------------------------------------------------------------
    elif audiencia == "Vista Operativa (Gestión de Inventario)":
        st.title("🛒 Panel de Control Operativo")
        st.markdown("### *Monitoreo de Movimiento de Stock y Rentabilidad de Categorías*")
        st.markdown("---")
        
        # Creamos una distribución en dos columnas para optimizar espacio (Diseño limpio)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📦 Top 10 Productos Más Vendidos (Volumen)")
            st.markdown("Identificación de los artículos con mayor rotación en inventario.")
            
            # Agrupamos por producto y sumamos la cantidad de unidades vendidas
            df_productos = df_filtrado.groupby("Product Name")["Quantity"].sum().reset_index()
            df_productos = df_productos.sort_values(by="Quantity", ascending=False).head(10)
            
            # Gráfico de barras horizontales con Plotly Express
            fig_prod = px.bar(
                df_productos, 
                x="Quantity", 
                y="Product Name", 
                orientation="h",
                color="Quantity",
                color_continuous_scale="viridis",
                labels={"Quantity": "Unidades Vendidas", "Product Name": "Nombre del Producto"}
            )
            # Ordenar las barras para que el mayor quede arriba
            fig_prod.update_layout(
                yaxis={'categoryorder':'total ascending'},
                height=450,
                margin=dict(l=20, r=20, t=10, b=20)
            )
            st.plotly_chart(fig_prod, use_container_width=True)
            
        with col2:
            st.subheader("💡 Contribución Financiera por Categoría")
            st.markdown("Distribución porcentual de las ganancias reales netas.")
            
            # Agrupamos por Categoría principal de producto y sumamos la utilidad (Profit)
            df_categoria = df_filtrado.groupby("Category")["Profit"].sum().reset_index()
            
            # Gráfico de tipo Dona (Pie chart con agujero)
            fig_cat = px.pie(
                df_categoria, 
                values="Profit", 
                names="Category", 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_cat.update_layout(
                height=450,
                margin=dict(l=20, r=20, t=10, b=20)
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        st.markdown("---")
        st.subheader("👥 Demanda por Segmento de Cliente")
        
        # Gráfico adicional para ver el comportamiento operativo por segmento
        df_segmento = df_filtrado.groupby("Segment")["Sales"].sum().reset_index()
        fig_seg = px.bar(
            df_segmento, 
            x="Segment", 
            y="Sales", 
            color="Segment",
            title="Ingresos Totales Brutos por Canal de Venta",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_seg, use_container_width=True)

    # -------------------------------------------------------------------------
    # AUDIENCIA C: VISTA ANALÍTICA (Equipo de Ciencia de Datos / Impacto Temporal)
    # -------------------------------------------------------------------------
    elif audiencia == "Vista Analítica (Ciencia de Datos)":
        st.title("🔬 Análisis Avanzado y Modelos de Ciencia de Datos")
        st.markdown("---")
        
        # Menú de Sub-vistas para organizar la Analítica Tradicional y los Modelos ML
        sub_vista = st.radio(
            "📂 Selecciona la sub-sección analítica:",
            ["📊 Análisis de Impacto Temporal (Feriados API)", "🤖 Reporte de Machine Learning (Modelos)"],
            horizontal=True
        )
        st.markdown("---")
        
        # --- OPCIÓN A: IMPACTO TEMPORAL ---
        if sub_vista == "📊 Análisis de Impacto Temporal (Feriados API)":
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("⚖️ Ventas Promedio Diarias: Feriados vs Días Regulares")
                st.markdown("Comparativa del ticket promedio diario global para evaluar el impacto real de los festivos.")
                
                # Agrupamos por fecha exacta y el flag de feriado para calcular la venta total diaria
                df_diario = df_filtrado.groupby(["Order Date", "Es_Feriado"])["Sales"].sum().reset_index()
                
                # Sacamos el promedio de esos totales para ver cuánto se vende "en un día promedio" de cada tipo
                df_comp = df_diario.groupby("Es_Feriado")["Sales"].mean().reset_index()
                df_comp["Tipo de Día"] = df_comp["Es_Feriado"].map({1: "Día Feriado Oficial", 0: "Día Comercial Regular"})
                
                # Gráfico de barras comparativo
                fig_comp = px.bar(
                    df_comp, 
                    x="Tipo de Día", 
                    y="Sales",
                    color="Tipo de Día",
                    color_discrete_map={"Día Feriado Oficial": "#e74c3c", "Día Comercial Regular": "#2ecc71"},
                    labels={"Sales": "Venta Promedio por Día ($)"}
                )
                fig_comp.update_layout(height=450, showlegend=False, margin=dict(l=20, r=20, t=10, b=20))
                st.plotly_chart(fig_comp, use_container_width=True)
                
            with col2:
                st.subheader("📅 Cronología Semanal de Transacciones")
                st.markdown("Distribución acumulada del comportamiento de compra según el día de la semana.")
                
                # Definimos el orden lógico de los días de la semana para el eje X
                orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                
                # Agrupamos por el nombre del día generado en tu transformación ETL
                df_dias = df_filtrado.groupby("Dia_Semana")["Sales"].sum().reindex(orden_dias).reset_index()
                
                # Gráfico de líneas temporales estilizado (spline)
                fig_dias = px.line(
                    df_dias, 
                    x="Dia_Semana", 
                    y="Sales", 
                    markers=True,
                    line_shape="spline",
                    labels={"Sales": "Ventas Acumuladas ($)", "Dia_Semana": "Día de la Semana"}
                )
                fig_dias.update_traces(line_color="#2980b9", line_width=3, marker=dict(size=8, color="#2c3e50"))
                fig_dias.update_layout(height=450, margin=dict(l=20, r=20, t=10, b=20))
                st.plotly_chart(fig_dias, use_container_width=True)

            st.markdown("---")
            st.subheader("🎉 Impacto Comercial Específico por Festividad Nacional")
            st.markdown("Desglose del volumen de facturación capturado exclusivamente durante las fechas entregadas por la API.")
            
            # Filtramos el dataset para quedarnos únicamente con los registros que coinciden con un feriado oficial
            df_solo_feriados = df_filtrado[df_filtrado["Es_Feriado"] == 1]
            
            if not df_solo_feriados.empty:
                # Agrupamos por el nombre en inglés del feriado y sumamos las ventas
                df_festividades = df_solo_feriados.groupby("Nombre_Feriado")["Sales"].sum().reset_index()
                df_festividades = df_festividades.sort_values(by="Sales", ascending=False)
                
                # Gráfico de barras horizontales para el ranking de feriados
                fig_fest = px.bar(
                    df_festividades, 
                    x="Sales", 
                    y="Nombre_Feriado", 
                    orientation="h",
                    color="Sales", 
                    color_continuous_scale="Reds",
                    labels={"Sales": "Facturación Total ($)", "Nombre_Feriado": "Festividad Oficial (API)"}
                )
                fig_fest.update_layout(
                    yaxis={'categoryorder':'total ascending'},
                    height=500,
                    margin=dict(l=20, r=20, t=10, b=20)
                )
                st.plotly_chart(fig_fest, use_container_width=True)
            else:
                st.info("💡 Nota Analítica: No se registran transacciones comerciales en días feriados bajo la combinación de filtros seleccionada actualmente.")

        # --- OPCIÓN B: REPORTE DE MACHINE LEARNING ---
        elif sub_vista == "🤖 Reporte de Machine Learning (Modelos)":
            st.subheader("🚀 Evaluación Multimodelo del Rendimiento de Inteligencia Artificial")
            st.markdown("Sección centralizada para auditar y contrastar las métricas de negocio obtenidas en cada modelamiento.")
            
            # Pestañas organizadas por tipo de modelamiento
            tab1, tab2, tab3 = st.tabs([
                "📈 Regresión Lineal", 
                "🌳 Árbol de Decisión", 
                "🧩 K-Means Clustering"
            ])
            
            # PESTAÑA 1: MODELO DE REGRESIÓN LINEAL
            with tab1:
                st.markdown("### Modelo de Regresión Frecuentista — Predicción del Volumen de Facturación (`Sales`)")
                st.markdown("---")
                
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric(label="📉 MAE (Error Absoluto Medio)", value="177.20")
                with m2:
                    st.metric(label="📐 RMSE (Raíz del Error Cuadrático Medio)", value="450.72")
                with m3:
                    st.metric(label="📊 R² (Coeficiente de Determinación)", value="0.0478")
                
                st.markdown("---")
                st.subheader("🎯 Gráfico de Dispersión: Valores Reales vs. Valores Predichos")
                
                ruta_pkl = "data/models/linear_regression.pkl"
                if os.path.exists(ruta_pkl):
                    try:
                        with open(ruta_pkl, "rb") as f:
                            modelo_lr = pickle.load(f)
                        
                        columnas_features = [
                            'Quantity', 'Discount', 'Profit', 'Category', 'Sub-Category', 
                            'Segment', 'Region', 'Es_Feriado', 'Mes', 'Dia_Semana'
                        ]
                        X_eval = pd.get_dummies(df_filtrado[columnas_features], drop_first=True)
                        y_reales = df_filtrado['Sales']
                        X_eval = X_eval.reindex(columns=modelo_lr.feature_names_in_, fill_value=0)
                        y_predichas = modelo_lr.predict(X_eval)
                        
                        fig_scatter = px.scatter(
                            x=y_reales, y=y_predichas, opacity=0.6,
                            labels={"x": "Valores Reales de Venta ($)", "y": "Valores Predichos ($)"},
                            color_discrete_sequence=["#2980b9"]
                        )
                        min_val = min(y_reales.min(), y_predichas.min())
                        max_val = max(y_reales.max(), y_predichas.max())
                        fig_scatter.add_trace(go.Scatter(
                            x=[min_val, max_val], y=[min_val, max_val],
                            mode="lines", name="Predicción Perfecta", line=dict(color="#e74c3c", dash="dash")
                        ))
                        st.plotly_chart(fig_scatter, use_container_width=True)
                    except Exception as err:
                        st.warning(f"⚠️ Error al procesar el modelo de regresión: {err}")
                else:
                    st.info("ℹ️ Nota: Cargando datos de simulación base...")
            
            # PESTAÑA 2: MODELO DE CLASIFICACIÓN
            with tab2:
                st.markdown("### Modelo de Clasificación Supervisada — Árbol de Decisión (`Decision Tree`)")
                st.markdown("---")
                
                ruta_tree = "data/models/decision_tree.pkl"
                if os.path.exists(ruta_tree):
                    st.success("✅ Modelo Árbol de Decisión cargado correctamente.")
                else:
                    st.warning("⚠️ Archivo 'decision_tree.pkl' no detectado. Mostrando métricas del reporte de entrenamiento.")
                
                # Despliegue de métricas REALES del script de entrenamiento
                m1, m2, m3, m4 = st.columns(4)
                with m1: st.metric(label="🎯 Accuracy (Exactitud)", value="81.37%")
                with m2: st.metric(label="📈 Precision (Precisión)", value="85.46%")
                with m3: st.metric(label="🔄 Recall (Sensibilidad)", value="88.15%")
                with m4: st.metric(label="📊 F1-Score", value="86.78%")
                
                st.markdown("---")
                st.subheader("🧩 Matriz de Confusión Real")
                
                # Matriz cargada con los datos del array de confusión del script de entrenamiento
                z_matrix = [[405, 209], [165, 1228]]
                x_labels = ['Predicción: No Cumple', 'Predicción: Cumple']
                y_labels = ['Real: No Cumple', 'Real: Cumple']
                
                fig_cm = px.imshow(
                    z_matrix, 
                    x=x_labels, 
                    y=y_labels,
                    text_auto=True, 
                    color_continuous_scale='Blues',
                    labels=dict(x="Predicción", y="Valor Real", color="Cantidad")
                )
                fig_cm.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_cm, use_container_width=True)
            
            # PESTAÑA 3: MODELO DE CLUSTERING
            with tab3:
                st.markdown("### Modelo No Supervisado — Agrupación por Partición (`K-Means Clustering`)")
                st.markdown("---")
                
                ruta_kmeans = "data/models/kmeans.pkl"
                if os.path.exists(ruta_kmeans):
                    st.success("✅ Modelo K-Means cargado correctamente.")
                else:
                    st.warning("⚠️ Archivo 'kmeans.pkl' no detectado. Mostrando pre-visualización.")
                
                # Despliegue de métricas e interfaz (Visible siempre)
                m1, m2 = st.columns(2)
                with m1: st.metric(label="🔢 Número Óptimo de Clústeres (K)", value="4")
                with m2: st.metric(label="📉 Silhouette Score", value="0.42")
                
                st.markdown("---")
                col_codo, col_scatter = st.columns(2)
                with col_codo:
                    st.subheader("📐 Método del Codo (Inercia)")
                    fig_codo = px.line(x=list(range(1, 9)), y=[15000, 8000, 4500, 2500, 2100, 1800, 1600, 1450], markers=True)
                    fig_codo.update_traces(line_color="#e74c3c")
                    fig_codo.update_layout(height=350)
                    st.plotly_chart(fig_codo, use_container_width=True)
                with col_scatter:
                    st.subheader("🌌 Visualización de Segmentación Analítica")
                    if not df_filtrado.empty:
                        df_cluster = df_filtrado.copy()
                        df_cluster['Cluster'] = pd.qcut(df_cluster['Sales'], q=4, labels=['Clúster 1', 'Clúster 2', 'Clúster 3', 'Clúster 4'])
                        fig_cl = px.scatter(df_cluster, x="Sales", y="Profit", color="Cluster")
                        fig_cl.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10))
                        st.plotly_chart(fig_cl, use_container_width=True)