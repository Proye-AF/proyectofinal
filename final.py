import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
@st.cache_data
def cargar_datos():
    try:
        # Cargar el archivo omitiendo las líneas mal formateadas
        df = pd.read_csv('dataset/aerolinea_muestra1.csv', delimiter=';', on_bad_lines='skip')
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        df = pd.DataFrame()  # Usa un DataFrame vacío en caso de error
    return df

df = cargar_datos()

# Procesar y filtrar las columnas necesarias
def procesar_datos(df):
    if df.empty:
        return df
    
    # Identificar y seleccionar las columnas relevantes
    columnas_relevantes = ['Fecha', 'Aeropuerto', 'Pasajeros', 'Aeronave']  # Ajustar según las columnas disponibles en el nuevo archivo
    
    # Verificar si las columnas relevantes están en el DataFrame
    columnas_presentes = [col for col in columnas_relevantes if col in df.columns]
    
    if len(columnas_presentes) != len(columnas_relevantes):
        st.error(f"Las columnas relevantes esperadas no están presentes. Columnas encontradas: {columnas_presentes}")
        return pd.DataFrame()
    
    # Seleccionar solo las columnas relevantes
    df = df[columnas_relevantes]
    
    # Convertir tipos de datos adecuados
    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
    df['Pasajeros'] = pd.to_numeric(df['Pasajeros'], errors='coerce')
    
    return df

df = procesar_datos(df)

# Sidebar para opciones de visualización
st.sidebar.title("Análisis de Datos de Aerolínea")
analysis_type = st.sidebar.selectbox(
    "Seleccione el tipo de análisis:",
    ['Vuelos Diarios', 'Actividad de Aeropuertos', 'Tipo de Aviones', 'Comparativa Anual', 'Resumen de Datos']
)

# Funciones para visualización de datos
def vuelos_diarios():
    st.title("Vuelos Diarios")
    fecha_columna = 'Fecha'

    if fecha_columna in df.columns:
        # Selección de rango de fechas
        min_date = df[fecha_columna].min()
        max_date = df[fecha_columna].max()
        start_date, end_date = st.date_input("Seleccione el rango de fechas:", [min_date, max_date], min_value=min_date, max_value=max_date)

        if start_date and end_date:
            df_filtered = df[(df[fecha_columna] >= pd.to_datetime(start_date)) & (df[fecha_columna] <= pd.to_datetime(end_date))]
        
            if not df_filtered.empty:
                # Gráfico de líneas para vuelos diarios
                fig_line = px.line(df_filtered, x=fecha_columna, y='Pasajeros', title='Vuelos Diarios')
                st.plotly_chart(fig_line)

                # Mostrar uno a uno los gráficos con botones
                if st.button('Mostrar Histograma'):
                    fig_hist = px.histogram(df_filtered, x=fecha_columna, y='Pasajeros', nbins=30, title='Distribución de Vuelos Diarios')
                    st.plotly_chart(fig_hist)

                if st.button('Mostrar Gráfico de Barras por Mes'):
                    df_filtered['Mes'] = df_filtered[fecha_columna].dt.month
                    df_monthly = df_filtered.groupby('Mes')['Pasajeros'].sum().reset_index()
                    fig_bar = px.bar(df_monthly, x='Mes', y='Pasajeros', title='Vuelos Diarios por Mes')
                    st.plotly_chart(fig_bar)

                if st.button('Mostrar Gráfico de Dispersión'):
                    fig_scatter = px.scatter(df_filtered, x=fecha_columna, y='Pasajeros', title='Dispersión de Vuelos Diarios')
                    st.plotly_chart(fig_scatter)
            else:
                st.write("No hay datos disponibles para el rango de fechas seleccionado.")
    else:
        st.error("No se encontró una columna de fecha adecuada.")

def actividad_aeropuertos():
    st.title("Actividad de Aeropuertos")
    if 'Aeropuerto' in df.columns:
        df_aggregated = df.groupby('Aeropuerto').size().reset_index(name='cantidad_vuelos')
        fig = px.bar(df_aggregated, x='Aeropuerto', y='cantidad_vuelos', title='Actividad por Aeropuerto')
        st.plotly_chart(fig)
    else:
        st.error("No se encontró una columna de Aeropuerto.")

def tipo_aviones():
    st.title("Tipo de Aviones")
    if 'Aeronave' in df.columns:
        fig = px.pie(df, names='Aeronave', title='Distribución de Tipos de Avión')
        st.plotly_chart(fig)
    else:
        st.error("No se encontró una columna de Aeronave.")

def comparativa_anual():
    st.title("Comparativa Anual de Vuelos")
    fecha_columna = 'Fecha'

    if fecha_columna in df.columns:
        df['año'] = df[fecha_columna].dt.year
        # Asegurarse de sumar solo las columnas numéricas
        df_aggregated = df.groupby('año').sum(numeric_only=True).reset_index()
        fig = px.bar(df_aggregated, x='año', y='Pasajeros', title='Comparativa Anual de Vuelos')
        st.plotly_chart(fig)
    else:
        st.error("No se encontró una columna de fecha adecuada.")

def resumen_datos():
    st.title("Resumen de Datos")
    st.write(f"Total de registros: {len(df)}")
    st.write(f"Total de columnas: {len(df.columns)}")

# Ejecución de la funcionalidad basada en la selección del usuario
if analysis_type == 'Vuelos Diarios':
    vuelos_diarios()
elif analysis_type == 'Actividad de Aeropuertos':
    actividad_aeropuertos()
elif analysis_type == 'Tipo de Aviones':
    tipo_aviones()
elif analysis_type == 'Comparativa Anual':
    comparativa_anual()
elif analysis_type == 'Resumen de Datos':
    resumen_datos()
