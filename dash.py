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


print(datos['ROA'])

# Calcular Eficiencia en Gasto Operativo
datos['Eficiencia_Gasto_Operativo'] = (datos['Ingresos_Netos_millones'] - datos['Gastos_Operativos_millones']) / datos['Ingresos_Netos_millones']

# Calcular Gasto de Personal/Ingresos multiplicado por 100
datos['Gasto_Personal_Ingresos'] = (datos['Gasto_personal'] / datos['Ingresos_Netos_millones']) * 100

# Calcular columnas adicionales para el cálculo del Grado Absorción
datos['Grado_Absorción'] = datos['Gastos_Operativos_millones'] / datos['Margen_Financiero_Neto_millones']

# Calcular los indicadores solicitados
datos['Solvencia_Patrimonial'] = datos['Patrimonio_millones'] / datos['Activos_Finales_millones']
datos['Porcentaje_Crecimiento_Captaciones'] = ((datos['Captaciones_Finales_millones'] - datos['Captaciones_Iniciales_millones']) / datos['Captaciones_Iniciales_millones']) * 100
datos['Porcentaje_Crecimiento_Cartera'] = ((datos['Cartera_Final_millones'] - datos['Cartera_Inicial_millones']) / datos['Cartera_Inicial_millones']) * 100
datos['Porcentaje_Crecimiento_Provisiones'] = ((datos['Provisiones_Finales_millones'] - datos['Provisiones_Iniciales_millones']) / datos['Provisiones_Iniciales_millones']) * 100

# Perspectiva financiera
indicadores_financieros = [
    'ROA', 'Eficiencia_Gasto_Operativo', 'Gasto_Personal_Ingresos', 'Grado_Absorción',
    'Solvencia_Patrimonial', 'Porcentaje_Crecimiento_Captaciones',
    'Porcentaje_Crecimiento_Cartera', 'Porcentaje_Crecimiento_Provisiones'
]

# Perspectiva de negocios
indicadores_negocios = [
    'Porcentaje_Crecimiento_Clientes', 'Porcentaje_Crecimiento_Canales'
]

# Selección de perspectiva
perspectiva_seleccionada = st.sidebar.radio("Seleccionar Perspectiva", ['Financiera', 'Negocios'])

# Selección de indicador
if perspectiva_seleccionada == 'Financiera':
    st.sidebar.subheader("Seleccionar Indicador Financiero")
    indicador_seleccionado = st.sidebar.selectbox("Indicador Financiero", indicadores_financieros)
else:
    st.sidebar.subheader("Seleccionar Indicador de Negocios")
    indicador_seleccionado = st.sidebar.selectbox("Indicador de Negocios", indicadores_negocios)

# Filtrar los datos según la perspectiva seleccionada
if perspectiva_seleccionada == 'Financiera':
    indicadores_seleccionados = indicadores_financieros
else:
    indicadores_seleccionados = indicadores_negocios

# Crear un DataFrame con los indicadores seleccionados
datos_indicadores = datos[indicadores_seleccionados + ['Año']]
# Reorganizar los datos para que estén listos para el gráfico polar
datos_polar = pd.melt(datos_indicadores, id_vars=['Año'], value_vars=indicadores_seleccionados, var_name='Indicador', value_name='Valor')

# Crear gráfico polar con color por indicador
fig_radial_todos = px.line_polar(
    datos_polar,
    r='Valor',
    theta='Indicador',
    line_close=True,
    animation_frame='Año',
    color='Indicador',  # Cambiar a 'Indicador' para que el color sea por indicador
    color_discrete_sequence=px.colors.qualitative.Set1
)
st.plotly_chart(fig_radial_todos)




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


# Gráfico de dispersión con línea de tendencia
st.subheader(f"Relación entre {indicador_seleccionado} y Activos Iniciales - Cliente {cliente_seleccionado}")
fig_dispersion_tendencia = px.scatter(
    datos_cliente,
    x='Activos_Iniciales_millones',
    y=indicador_seleccionado,
    trendline="ols",  # Línea de tendencia de mínimos cuadrados ordinarios
    labels={indicador_seleccionado: indicador_seleccionado},
    title=f"Relación entre {indicador_seleccionado} y Activos Iniciales para {cliente_seleccionado}"
)
st.plotly_chart(fig_dispersion_tendencia)

# Gráfico de barras (Cliente)
st.subheader(f"Comparación Anual - {indicador_seleccionado}")
fig_barras_cliente = px.bar(
    datos_cliente,
    x='Año',
    y=indicador_seleccionado,
    labels={indicador_seleccionado: indicador_seleccionado},
    title=f"Comparación Anual de {indicador_seleccionado} para {cliente_seleccionado}"
)
st.plotly_chart(fig_barras_cliente)
