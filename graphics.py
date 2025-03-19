import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class Graphics:
    def __init__(self, df_data, team_selected, filtered_data):
        """
        Constructor de la clase Graphips.
        :param df_data: DataFrame que contiene los datos a graficar.
        """
        self.df_data = df_data
        self.filtered_data = filtered_data
        self.team_selected = team_selected

    def set_team_selected(self, team_selected, filtered_data):
        """
        Método para actualizar el equipo seleccionado.
        :param team_selected: Nuevo equipo seleccionado.
        :param filtered_data: Nueva info por equipo.
        """
        self.filtered_data = filtered_data
        self.team_selected = team_selected

    def team_points_pie_chart_diagram(self, team_column = "Team", points_column = "PTS"):
        """
        Gráfico de pastel: Proporción de puntos por equipo.
        """
        st.subheader("Proporción de Puntos por Equipo")

        # Agrupar por equipo y sumar puntos
        total_points_by_team = self.df_data.groupby(team_column)[points_column].sum().reset_index()

        # Inicialización del gráfico
        fig, ax = plt.subplots(figsize=(8, 8))

        # Crear la gráfica de pastel
        ax.pie(
            total_points_by_team[points_column],
            labels=total_points_by_team[team_column],
            autopct='%1.1f%%',
            colors=sns.color_palette("coolwarm", len(total_points_by_team))
        )
        ax.set_title("Proporción de Puntos por Equipo")

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

    def pts_per_team_histogram_diagram(self, player_column = "PName", points_column = "PTS"):
        """
        Histograma de puntos por jugador para un equipo seleccionado.
        """
        # Inicialización del gráfico
        fig, ax = plt.subplots(figsize=(6, 3))

        # Generar el histograma
        sns.barplot(x=self.filtered_data[player_column], y=self.filtered_data[points_column], palette="coolwarm", ax=ax)
        ax.set_title(f"Histograma de Puntos por Jugador - {self.team_selected}")
        ax.set_xlabel("Jugador")
        ax.set_ylabel("Puntos")
        plt.xticks(rotation=45, ha="right")

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

    def ast_per_team_histogram_diagram(self, player_column = "PName", asistence_column = "AST"):
        """
        Histograma de asistencias por jugador para un equipo seleccionado.
        """
        # Inicialización del gráfico
        fig, ax = plt.subplots(figsize=(6, 3))

        # Generar el histograma
        sns.barplot(x=self.filtered_data[player_column], y=self.filtered_data[asistence_column], palette="coolwarm", ax=ax)
        ax.set_title(f"Histograma de Asistencias por Jugador - {self.team_selected}")
        ax.set_xlabel("Jugador")
        ax.set_ylabel("Asistencias")
        plt.xticks(rotation=45, ha="right")

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

    def pts_ast_scatter_diagram(self, points_column = "PTS", asistence_column = "AST", position_column = "POS"):
        """
        Gráfico de dispersión: Puntos vs. Asistencias.
        """
        st.subheader("Puntos vs. Asistencias")
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.scatterplot(data=self.filtered_data, x=points_column, y=asistence_column, hue=position_column, palette="coolwarm", ax=ax)
        ax.set_title(f"Puntos vs. Asistencias - {self.team_selected}")
        ax.set_xlabel("Puntos")
        ax.set_ylabel("Asistencias")
        st.pyplot(fig)

    def age_line_diagram(self, age_column = "Age", points_column = "PTS"):
        """
        Diagrama de línea: Evolución de puntos por edad.
        """
        st.subheader("Evolución de Puntos por Edad")

        # Crear rangos de edad
        ticks = list(range(int(self.df_data[age_column].min()), int(self.df_data[age_column].max()) + 1, 3))
        self.df_data["Age Group"] = pd.cut(
            self.df_data[age_column],
            bins=ticks,
            labels=[f"{ticks[i]}-{ticks[i+1]-1}" for i in range(len(ticks)-1)]
        )

        # Promediar puntos por edad
        avg_points_by_age = self.df_data.groupby(age_column)[points_column].mean().reset_index()

        # Inicialización del gráfico
        fig, ax = plt.subplots(figsize=(6, 3))

        # Crear el diagrama de línea
        sns.lineplot(data=avg_points_by_age, x=age_column, y=points_column, marker="o", color="blue", ax=ax)
        ax.set_title("Evolución de Puntos por Edad")
        ax.set_xlabel("Edad")
        ax.set_ylabel("Puntos Promedio")

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)