import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos desde el archivo CSV
archivo_csv = "indicadores_bancarios.csv"  # Reemplaza con la ruta correcta
df = pd.read_csv(archivo_csv)

# Crear aplicación Streamlit
st.title('Visualización de Datos Financieros')


# Crear menú para seleccionar indicador
indicadores = ['Rentabilidad sobre el activo (ROA)', 'Eficiencia en gasto operativo', 'Gasto Personal', 'Grado de absorción', 'Morosidad de cartera total', 'Liquidez de corto plazo', 'Rentabilidad sobre el patrimonio (ROE)',
               'Cobertura de cartera improductiva', 'Porcentaje de crecimiento en activos', 'Solvencia Patrimonial', 'Porcentaje de crecimiento en captaciones', 'Porcentaje de crecimiento de cartera', 'Porcentaje de crecimiento de provisiones de cartera']
indicador = st.selectbox('Seleccionar Indicador:', indicadores)

# Agregar menús desplegables para la selección del usuario
clientes = st.selectbox('Seleccionar Cliente:', df['Cliente'].unique())

# Convertir el valor seleccionado a entero para manejar posibles discrepancias en el tipo

# Filtrar datos según la selección del usuario
filtered_data = df[df['Cliente'] == clientes]


# Verificar si hay datos filtrados antes de crear el gráfico
if not filtered_data.empty:
    # Mostrar datos en una tabla
    st.dataframe(filtered_data)

    # Crear gráfico con Plotly Express
    variables = st.multiselect('Seleccionar Variables:', df.columns)

    fig = px.line(filtered_data, x='Año', y=variables,
                  labels={'value': 'Monto', 'variable': 'Categoría'},
                  title=f'{clientes} - {variables}',
                  line_shape='linear')

    # Mostrar gráfico
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error('No hay datos disponibles para el cliente seleccionado.')
