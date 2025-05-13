from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, classification_report

class LinearRegressionViewer:
    def __init__(self, df_data, team_selected, filtered_data, filtered_data_year_only):
        """
        Constructor de la clase LinearRegression.
        :param df_data: DataFrame que contiene los datos a graficar.
        """
       # Calcular promedios generales por equipo
        avg_home = df_data.groupby('home_team')[['home_avg_pts', 'home_avg_reb']].mean()
        avg_away = df_data.groupby('away_team')[['away_avg_pts', 'away_avg_reb']].mean()

        # Reemplazar valores por promedios para crear el dataset de entrenamiento
        self.df_option1 = df_data.copy()
        self.df_option1['home_avg_pts'] = df_option1['home_team'].map(avg_home['home_avg_pts'])
        self.df_option1['home_avg_reb'] = df_option1['home_team'].map(avg_home['home_avg_reb'])
        self.df_option1['away_avg_pts'] = df_option1['away_team'].map(avg_away['away_avg_pts'])
        self.df_option1['away_avg_reb'] = df_option1['away_team'].map(avg_away['away_avg_reb'])

    