import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import random
from skimage import io
from graphics import Graphics
from linearRegresion import LinearRegressionViewer
from decisionTree import DecisionTreeViewer

# Función para manejar el cambio de equipo
def on_team_change():
    # Actualizar el equipo seleccionado en el estado de sesión
    st.session_state.team_selected = st.session_state.team_selectbox

# Función para manejar el cambio de año
def on_year_change():
    # Actualizar el año seleccionado en el estado de sesión
    st.session_state.year_selected = st.session_state.year_selectbox

# Cargar datos
t_data = pd.read_csv('./Archivo_Unido.csv')
nt_data = pd.read_csv('./2024_nba_player_stats.csv')

# Cargar logo
logo = io.imread(r"./images/nba_logo.png")

# Título de la aplicación
st.title("Estadísticas de NBA General")

# Inicializar el estado de sesión si no existe
if "df_selected" not in st.session_state:
    st.session_state.df_selected = None  # Inicializar sin DataFrame seleccionado

# Mostrar un modal para seleccionar el DataFrame
if st.session_state.df_selected is None:
    st.write("Selecciona el DataFrame que deseas usar:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Usar No Transformados"):
            st.session_state.df_selected = "nt_data"
    with col2:
        if st.button("Usar Transformados"):
            st.session_state.df_selected = "t_data"
    st.stop()  # Detener la ejecución hasta que se seleccione un DataFrame

# Obtener el DataFrame seleccionado
if st.session_state.df_selected == "nt_data":
    df = nt_data
else:
    df = t_data

# Barra lateral
st.sidebar.markdown("## MENÚ DE CONFIGURACIÓN")
st.sidebar.divider()

# Lista de equipos disponibles
if st.session_state.df_selected == "nt_data":
    teams = df["Team"].unique().tolist()
    years = df["Year"].unique().tolist()
else:
    teams = df["Equipo"].unique().tolist()
    years = df["Año"].unique().tolist()

# Inicializar el estado de sesión si no existe
if "team_selected" not in st.session_state:
    st.session_state.team_selected = teams[0]  # Equipo por defecto

if "year_selected" not in st.session_state:
    st.session_state.year_selected = years[0]  # Año por defecto

# Selector de año en la barra lateral (uno a la vez)
team_selected = st.sidebar.selectbox(
    "Selecciona un Año:", 
    years, 
    index=years.index(st.session_state.year_selected),  # Año seleccionado o por defecto
    key="year_selectbox",  # Clave para identificar el selectbox en el estado de sesión
    on_change=on_year_change  # Llamar a on_year_change cuando cambiar el año
)
st.sidebar.divider()

# Selector de equipo en la barra lateral (uno a la vez)
team_selected = st.sidebar.selectbox(
    "Selecciona un Equipo:", 
    teams, 
    index=teams.index(st.session_state.team_selected),  # Equipo seleccionado o por defecto
    key="team_selectbox",  # Clave para identificar el selectbox en el estado de sesión
    on_change=on_team_change  # Llamar a on_team_change cuando cambia el equipo
)
st.sidebar.divider()

st.sidebar.image(logo)

# Filtrar datos del equipo seleccionado (o por defecto)
if st.session_state.df_selected == "nt_data":
    filtered_data = df[(df["Team"] == st.session_state.team_selected) & (df["Year"] == st.session_state.year_selected)]
    filtered_data_year_only = df[(df["Year"] == st.session_state.year_selected)]
else:
    filtered_data = df[(df["Equipo"] == st.session_state.team_selected) & (df["Año"] == st.session_state.year_selected)]
    filtered_data_year_only = df[(df["Año"] == st.session_state.year_selected)]

# Crear instancia de Graphics
graphics = Graphics(df, st.session_state.team_selected, filtered_data, filtered_data_year_only)
linearRegression = LinearRegressionViewer(t_data)
decisionTree = DecisionTreeViewer(t_data)

df

# Generar gráficos solo una vez (con el equipo seleccionado o por defecto)
if st.session_state.df_selected == "nt_data":
    graphics.team_points_pie_chart_diagram("Team", "PTS")
    graphics.age_line_diagram("Age", "PTS")

    st.divider()
    st.title("Estadísticas de NBA por Equipo")
    col1, col2 = st.columns(2)
    with col1:
        graphics.pts_per_team_histogram_diagram("PName", "PTS")

    with col2:
        graphics.ast_per_team_histogram_diagram("PName", "AST")

    graphics.pts_ast_scatter_diagram("PTS", "AST", "POS")
else:
    graphics.team_points_pie_chart_diagram("Equipo", "Puntos_Totales")
    graphics.age_line_diagram("Edad", "Puntos_Totales")

    st.divider()
    st.title("Estadísticas de NBA por Equipo")
    col1, col2 = st.columns(2)
    with col1:
        graphics.pts_per_team_histogram_diagram("Nombre_Jugador", "Puntos_Totales")

    with col2:
        graphics.ast_per_team_histogram_diagram("Nombre_Jugador", "Asistencias")

    graphics.pts_ast_scatter_diagram("Puntos_Totales", "Asistencias", "Posición")

st.divider()
st.title("Modelo Regresion Linear")
st.text("Predice el número de asistencias según los parámetros los robos, bloqueos y tiros libres hechos por un jugador")
linearRegression.prediction_interface()
st.divider()
st.text("Criterios de evaluación")
linearRegression.get_mean_square_error_graph()
linearRegression.get_scatter_plot_with_metrics()

st.divider()
st.title("Modelo Arbol de Decision")

input_data = {
    'Minutos_Jugados': st.slider("Minutos Jugados", min_value=0, max_value=5000, value=2500),
    'Tiros_Campo_Encestados': st.slider("Tiros de Campo Encestados", min_value=0, max_value=1000, value=500),
    'Tiros_Campo_Intentados': st.slider("Tiros de Campo Intentados", min_value=0, max_value=2000, value=1000),
    'Tiros_Libres_Intentados': st.slider("Tiros Libres Intentados", min_value=0, max_value=600, value=300),
    'Robos': st.slider("Robos", min_value=0, max_value=100, value=50),
    'Bloqueos': st.slider("Bloqueos", min_value=0, max_value=100, value=50),
    'Triple_Dobles': st.slider("Triple-Dobles", min_value=0, max_value=100, value=50),
}
nuevo_df = pd.DataFrame([input_data])

prediccion, probabilidad = decisionTree.predict_with_proba(nuevo_df)
st.subheader("Predicción en tiempo real")
st.write(f"¿Doble-Doble?: {prediccion} ({probabilidad*100:.2f}%)")

st.divider()
decisionTree.get_decision_tree()
decisionTree.cross_matrix()