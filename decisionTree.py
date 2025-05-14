import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
import seaborn as sns
import streamlit as st

class DecisionTreeViewer:
    def __init__(self, df_data):
        df_data['DobleDoble'] = df_data['Doble_Dobles'].apply(lambda x: 'Sí' if x >= 10 else 'No')

        self.features = [
            'Minutos_Jugados', 'Tiros_Campo_Encestados', 
            'Tiros_Campo_Intentados', 
            'Tiros_Libres_Intentados', 
            'Robos', 'Bloqueos', 'Triple_Dobles'
        ]

        X = df_data[self.features]
        y = df_data['DobleDoble']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        self.X = X
        self.y = y

        self.modelo = DecisionTreeClassifier(max_depth=4, random_state=42, class_weight='balanced')
        self.modelo.fit(self.X_train, self.y_train)
        self.y_pred = self.modelo.predict(self.X_test)

    def get_decision_tree(self):
        # Mostrar métricas en Streamlit
        st.write("Accuracy:", accuracy_score(self.y_test, self.y_pred))
        st.write("\nReporte de Clasificación:\n", classification_report(self.y_test, self.y_pred))

        # Visualizar el árbol en Streamlit
        fig, ax = plt.subplots(figsize=(20, 10))
        plot_tree(self.modelo, feature_names=self.features, class_names=['No', 'Sí'], filled=True, ax=ax)
        st.pyplot(fig)

    def cross_matrix(self):
        scores = cross_val_score(self.modelo, self.X, self.y, cv=5)
        st.write("Accuracy por fold:", scores)
        st.write("Promedio:", scores.mean())
        
        # Matriz de confusión con strings
        fig, ax = plt.subplots()
        cm = confusion_matrix(self.y_test, self.y_pred, labels=['No', 'Sí'])  # Usar strings
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=["No", "Sí"], yticklabels=["No", "Sí"], ax=ax)
        ax.set_xlabel("Predicción")
        ax.set_ylabel("Real")
        ax.set_title("Matriz de Confusión")
        st.pyplot(fig)
    
    def predict(self, new_data: pd.DataFrame):
        """
        Recibe un DataFrame con las mismas columnas que `self.features`
        y devuelve la predicción del modelo entrenado.
        """
        # Verificar que las columnas necesarias estén presentes
        missing_cols = [col for col in self.features if col not in new_data.columns]
        if missing_cols:
            raise ValueError(f"Faltan las siguientes columnas en los datos de entrada: {missing_cols}")

        predictions = self.modelo.predict(new_data[self.features])
        return predictions
    
    def predict_with_proba(self, input_df):
        pred = self.modelo.predict(input_df)[0]
        proba = self.modelo.predict_proba(input_df)[0]
        # Índice 1 es la probabilidad de que sea "Sí", porque los labels son ['No', 'Sí']
        return pred, proba[1]