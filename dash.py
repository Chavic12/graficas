import streamlit as st
import pandas as pd
import plotly.express as px

# Crear el encabezado del dashboard
st.title("Dashboard de Indicadores Bancarios")

# Cargar tus datos directamente (reemplaza 'indicadores.csv' con tu propio archivo)
archivo_csv = 'indicadores.csv'
datos = pd.read_csv(archivo_csv)

# Calcular ROA (Return on Assets)
datos['ROA'] = datos['Ingresos_Netos_millones'] / datos['Activos_Finales_millones_promedio']

# Calcular Eficiencia en Gasto Operativo
datos['Eficiencia_Gasto_Operativo'] = (datos['Ingresos_Netos_millones'] - datos['Gastos_Operativos_millones']) / datos['Ingresos_Netos_millones']

# Calcular Gasto de Personal/Ingresos multiplicado por 100
datos['Gasto_Personal_Ingresos'] = (datos['Gasto_personal'] / datos['Ingresos_Netos_millones']) * 100

# Calcular columnas adicionales para el cálculo del Grado Absorción
datos['Grado_Absorción'] = datos['Gastos_Operativos_millones'] / datos['Margen_Financiero_Neto_millones']

# Selección de indicador
indicador_seleccionado = st.sidebar.selectbox("Seleccionar Indicador", [
    'ROA',
    'Eficiencia_Gasto_Operativo',
    'Gasto_Personal_Ingresos',
    'Grado_Absorción'
])

# Selección de cliente
cliente_seleccionado = st.selectbox("Seleccionar Cliente", datos['Cliente'].unique())

# Filtrar datos para el cliente seleccionado
datos_cliente = datos[datos['Cliente'] == cliente_seleccionado]

# Mostrar datos seleccionados
st.subheader(f"Datos para {cliente_seleccionado}")
st.write(datos_cliente[indicador_seleccionado])

# Gráficos interactivos para el cliente seleccionado
st.subheader(f"Gráficos para {indicador_seleccionado} - Cliente {cliente_seleccionado}")

# Gráfico de línea para el indicador seleccionado a lo largo de los años
st.subheader(f"Tendencia a lo largo de los años - {indicador_seleccionado}")
fig_linea_cliente = px.line(
    datos_cliente,
    x='Año',
    y=indicador_seleccionado,
    labels={indicador_seleccionado: indicador_seleccionado},
    title=f"Tendencia de {indicador_seleccionado} para {cliente_seleccionado}"
)
st.plotly_chart(fig_linea_cliente)

# Gráfico de dispersión
st.subheader(f"Relación con Activos Iniciales y Depósitos - {indicador_seleccionado}")
fig_dispersion_cliente = px.scatter(
    datos_cliente,
    x='Activos_Iniciales_millones',
    y=indicador_seleccionado,
    size='Depositos_Corto_Plazo_millones',
    labels={indicador_seleccionado: indicador_seleccionado},
    title=f"Relación de {indicador_seleccionado} con Activos Iniciales y Depósitos para {cliente_seleccionado}"
)
st.plotly_chart(fig_dispersion_cliente)

# Gráfico de barras
st.subheader(f"Comparación Anual - {indicador_seleccionado}")
fig_barras_cliente = px.bar(
    datos_cliente,
    x='Año',
    y=indicador_seleccionado,
    labels={indicador_seleccionado: indicador_seleccionado},
    title=f"Comparación Anual de {indicador_seleccionado} para {cliente_seleccionado}"
)
st.plotly_chart(fig_barras_cliente)
# Gráfico radial mejorado
st.subheader(f"Comparación Radial Mejorada - {indicador_seleccionado}")
fig_radial_mejorado = px.scatter_polar(
    datos_cliente,
    r=indicador_seleccionado,
    theta='Año',
    range_r=[0, datos_cliente[indicador_seleccionado].max()],
    color='Año',  # Asignar el color según el año
    color_discrete_sequence=px.colors.qualitative.Set1,  # Personalizar la paleta de colores
    labels={indicador_seleccionado: f"{indicador_seleccionado} - Año"},
    title=f"Comparación Radial Mejorada para {cliente_seleccionado}"
)
st.plotly_chart(fig_radial_mejorado)





# Estadísticas resumidas
st.subheader(f"Estadísticas Resumidas para {cliente_seleccionado}")
st.write(datos_cliente[indicador_seleccionado].describe())
