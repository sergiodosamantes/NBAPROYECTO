import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import random
from skimage import io
from graphics import Graphics

# Función para manejar el cambio de equipo
def on_team_change():
    # Actualizar el equipo seleccionado en el estado de sesión
    st.session_state.team_selected = st.session_state.team_selectbox

# Cargar datos
nt_data = pd.read_csv('./2024_nba_player_stats.csv')
t_data = pd.read_csv('./NuevoArchivo.csv')

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
if(st.session_state.df_selected == "nt_data"):
    teams = df["Team"].unique().tolist()
else:
    teams = df["Equipo"].unique().tolist()

# Inicializar el estado de sesión si no existe
if "team_selected" not in st.session_state:
    st.session_state.team_selected = teams[0]  # Equipo por defecto

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
if(st.session_state.df_selected == "nt_data"):
    filtered_data = df[df["Team"] == st.session_state.team_selected]
else:
    filtered_data = df[df["Equipo"] == st.session_state.team_selected]

# Crear instancia de Graphics
graphics = Graphics(df, st.session_state.team_selected, filtered_data)

df

# Generar gráficos solo una vez (con el equipo seleccionado o por defecto)
if(st.session_state.df_selected == "nt_data"):
    graphics.team_points_pie_chart_diagram()
    graphics.age_line_diagram()

    st.divider()
    st.title("Estadísticas de NBA por Equipo")
    col1, col2 = st.columns(2)
    with col1:
        graphics.pts_per_team_histogram_diagram()

    with col2:
        graphics.ast_per_team_histogram_diagram()

    graphics.pts_ast_scatter_diagram()
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