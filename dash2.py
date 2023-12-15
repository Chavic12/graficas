import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

# Función para obtener el nombre del mes en español
def obtener_nombre_mes(numero_mes):
    nombres_meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    return nombres_meses[numero_mes - 1]

# Título principal con estilo
st.title("Dashboard de Indicadores Bancarios")
st.markdown("---")  # Línea divisoria

# Cargar datos
archivo_csv = 'datosPrueba5.csv'
datos = pd.read_csv(archivo_csv)

# Listas de indicadores
indicadores_financieros = ["IND_ROA", "IND_Gastos_Operativos"]
indicadores_negocios = ['Porcentaje_Crecimiento_Clientes', 'Porcentaje_Crecimiento_Canales']

# Sidebar para selección de perspectiva e indicador
perspectiva_seleccionada = st.sidebar.radio("Seleccionar Perspectiva", ['Financiera', 'Negocios'])

if perspectiva_seleccionada == 'Financiera':
    st.sidebar.subheader("Seleccionar Indicador Financiero")
    selected_indicator = st.sidebar.selectbox("Indicador Financiero", indicadores_financieros)
else:
    st.sidebar.subheader("Seleccionar Indicador de Negocios")
    selected_indicator = st.sidebar.selectbox("Indicador de Negocios", indicadores_negocios)

if perspectiva_seleccionada == 'Financiera':
    indicadores_seleccionados = indicadores_financieros
else:
    indicadores_seleccionados = indicadores_negocios

# Preprocesamiento de datos
datos['Fecha'] = pd.to_datetime(datos['Fecha'], format="%d-%m-%Y")
datos['Año'] = datos['Fecha'].dt.year
datos['Mes'] = datos['Fecha'].dt.month

# Mapear los nombres de los meses en español
datos['Mes'] = datos['Mes'].apply(obtener_nombre_mes)

datos_indicadores = datos[indicadores_seleccionados + ['Año', 'Mes']]

# Gráfico de línea
st.subheader("Tendencia de los Indicadores Bancarios a lo Largo del Tiempo")
st.markdown("Este gráfico muestra cómo han evolucionado los indicadores bancarios a lo largo de los meses y años. "
            "Cada línea representa la tendencia de un indicador específico, con animación para visualizar cambios en el tiempo.")
fig_linea_todos = px.line(
    datos_indicadores,
    x='Mes',
    y=indicadores_seleccionados,
    range_y=[-0.5, 2],
    animation_frame='Año',
    title="Tendencia de los Indicadores Bancarios",
    markers=True
)
st.plotly_chart(fig_linea_todos, use_container_width=True)

# Selector de año
selected_data = st.slider("Seleccionar Año", min_value=datos['Año'].min(), max_value=datos['Año'].max())

# Gráficos adicionales para el año seleccionado
if selected_data:
    datos_indicador_seleccionado = datos[datos['Año'] == selected_data][['Mes', 'Año', selected_indicator]]

    # Crear gráfico de barras para el rango seleccionado
    st.subheader(f"Tendencia Mensual de {selected_indicator} para el Año {selected_data}")
    st.markdown(f"Este gráfico de barras muestra la variación mensual del indicador {selected_indicator} "
                f"para el año {selected_data}. Cada barra representa el valor del indicador para un mes específico.")
    fig_barras = px.bar(
        datos_indicador_seleccionado,
        x='Mes',
        y=selected_indicator,
        title=f'Tendencia de {selected_indicator} para el año {selected_data}',
        labels={'Mes': 'Mes', selected_indicator: 'Valor'},
    )
    st.plotly_chart(fig_barras)

    # Crear gráfico de dispersión para el rango seleccionado
    st.subheader(f'Dispersión Mensual de {selected_indicator} para el Año {selected_data}')
    st.markdown(f"Este gráfico de dispersión muestra la dispersión del indicador {selected_indicator} "
                f"para el año {selected_data}. Cada punto representa el valor del indicador para un mes específico.")
    fig_dispersion = px.scatter(
        datos_indicador_seleccionado,
        x='Mes',
        y=selected_indicator,
        title=f'Dispersión de {selected_indicator} para el año {selected_data}',
        labels={'Mes': 'Mes', selected_indicator: 'Valor'},
    )
    st.plotly_chart(fig_dispersion)

    # Crear gráfico de área para el rango seleccionado
    st.subheader(f'Área Mensual de {selected_indicator} para el Año {selected_data}')
    st.markdown(f"Este gráfico de área muestra la distribución del indicador {selected_indicator} "
                f"para el año {selected_data}. La sombra debajo de la curva representa el área de variación del indicador.")
    fig_area = px.area(
        datos_indicador_seleccionado,
        x='Mes',
        y=selected_indicator,
        title=f'Área de {selected_indicator} para el año {selected_data}',
        labels={'Mes': 'Mes', selected_indicator: 'Valor'},
    )
    st.plotly_chart(fig_area)

    # Crear gráfico de violín para el rango seleccionado
    st.subheader(f'Gráfico de Violín de {selected_indicator} por Año')
    st.markdown(f"Este gráfico de violín muestra la distribución del indicador {selected_indicator} a lo largo de los años. "
                f"La forma del violín revela la densidad y variabilidad del indicador.")
    fig_violin = px.violin(datos, x='Año', y=selected_indicator, box=True,
                           title=f'Gráfico de Violín de {selected_indicator} por Año',
                           labels={'Año': 'Año', selected_indicator: 'Valor'})
    st.plotly_chart(fig_violin)

    # Crear gráfico de torta para el rango seleccionado
    st.subheader(f'Gráfico de Torta para mostrar la Proporción de {selected_indicator} por Mes')
    st.markdown(f"Este gráfico de torta muestra la proporción del indicador {selected_indicator} "
                f"para cada mes del año {selected_data}. Cada porción representa la proporción del indicador en un mes específico.")
    fig_torta = px.pie(datos, names='Mes', values=selected_indicator,
                       title=f'Gráfico de Torta para mostrar la proporción de {selected_indicator} por Mes',
                       labels={'Mes': 'Mes', selected_indicator: 'Valor'})
    st.plotly_chart(fig_torta)
