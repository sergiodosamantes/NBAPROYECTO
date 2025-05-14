from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import streamlit as st

class LinearRegressionViewer:
    def __init__(self, df_data):
        features = [
            'Minutos_Jugados',
            'Tiros_Campo_Intentados',
            'Triples_Intentados',
            'Tiros_Libres_Intentados',
            'Rebotes_Totales',
            'Asistencias',
            'Robos',
            'Bloqueos',
            'Pérdidas',
            'Faltas_Personales'
        ]

        X = df_data[features]

        # Normaliza
        scaler = StandardScaler()
        X_normalizado = scaler.fit_transform(X)

        # Si quieres convertirlo a DataFrame con los mismos nombres:
        X_normalizado = pd.DataFrame(X_normalizado, columns=features)

        # Variables corregidas para evitar multicolinealidad
        X = df_data[['Minutos_Jugados', 'Tiros_Campo_Intentados', 'Triples_Intentados',
                'Tiros_Libres_Intentados', 'Rebotes_Totales', 'Asistencias', 
                'Robos', 'Bloqueos', 'Pérdidas', 'Faltas_Personales']]

        X_with_const = add_constant(X)

        # Calcula VIF para cada variable
        self.vif_data = pd.DataFrame()
        self.vif_data["Variable"] = X_with_const.columns
        self.vif_data["VIF"] = [variance_inflation_factor(X_with_const.values, i) 
                        for i in range(X_with_const.shape[1])]
        
        X = df_data[["Robos" ,"Bloqueos", "Tiros_Libres_Intentados"]] 
        y = df_data["Asistencias"]# Dividir en datos de entrenamiento y prueba
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X,y, test_size=0.2, random_state=23)

        self.X = X
        self.y = y

        # Crear el modelo de regresión lineal
        self.modelo = LinearRegression()

        # Entrenar el modelo
        self.modelo.fit(self.X_train, self.y_train)

        # Hacer predicciones
        self.y_predict = self.modelo.predict(self.X_test.values)

    def get_mean_square_error_graph(self):
        mse = mean_squared_error(self.y_test, self.y_predict)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, self.y_predict)

        # Mostrar métricas en Streamlit
        st.metric("RMSE", f"{rmse:.2f}")
        st.metric("R² Score", f"{r2:.2f}")

        # Mostrar tabla comparativa
        comparacion = pd.DataFrame({"Real": self.y_test, "Predicho": self.y_predict})
        st.write("Comparación entre valores reales y predichos:")
        st.dataframe(comparacion.head(10))

    def get_scatter_plot_with_metrics(self):
        # Mostrar métricas
        st.write(f"R² Score: {r2_score(self.y_test, self.y_predict):.2f}")
        st.write(f"MSE: {mean_squared_error(self.y_test, self.y_predict):.2f}")

        # Crear y mostrar gráfico
        fig, ax = plt.subplots()
        ax.scatter(self.y_test, self.y_predict)
        ax.set_xlabel("Valores Reales")
        ax.set_ylabel("Predicciones")
        ax.set_title("Reales vs Predichos")
        st.pyplot(fig)

        # Validación cruzada
        scores = cross_val_score(self.modelo, self.X, self.y, cv=5, scoring='r2')
        st.write(f"Promedio R² (validación cruzada): {scores.mean():.2f}")

    def prediction_interface(self):
        """Interfaz de Streamlit para realizar predicciones con el modelo"""
        
        # Crear columnas para organizar los inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            robos = st.number_input(
                "Robos", 
                min_value=0, 
                max_value=100, 
                value=1, 
                step=1,
                key="robos_input"
            )
        
        with col2:
            bloqueos = st.number_input(
                "Bloqueos", 
                min_value=0, 
                max_value=100, 
                value=1, 
                step=1,
                key="bloqueos_input"
            )
        
        with col3:
            tiros_libres = st.number_input(
                "Tiros Libres Intentados", 
                min_value=0, 
                max_value=100, 
                value=1, 
                step=1,
                key="tiros_libres_input"
            )
        
        # Botón para realizar la predicción
        if st.button("Predecir Asistencias", key="predict_button"):
            try:
                # Realizar la predicción
                prediccion = round(self.make_prediction(robos, bloqueos, tiros_libres))
                
                # Mostrar el resultado con estilo
                st.success(f"**Predicción de Asistencias:** {prediccion:.2f}")
                
                # Mostrar también los valores usados
                st.write("Valores utilizados para la predicción:")
                st.json({
                    "Robos": robos,
                    "Bloqueos": bloqueos,
                    "Tiros Libres Intentados": tiros_libres
                })
                
            except Exception as e:
                st.error(f"Error al realizar la predicción: {str(e)}")

    def make_prediction(self, robos: int, bloqueos: int, tiros_libres_intentados: int):
        """
        Realiza una predicción de asistencias basada en los parámetros de entrada.
        
        Args:
            robos: Número de robos
            bloqueos: Número de bloqueos
            tiros_libres_intentados: Número de tiros libres intentados
            
        Returns:
            Predicción de asistencias
        """
        # Crear array de entrada con las características en el orden correcto
        input_data = np.array([[robos, bloqueos, tiros_libres_intentados]])
        
        # Realizar predicción
        prediction = self.modelo.predict(input_data)
        
        return prediction[0]