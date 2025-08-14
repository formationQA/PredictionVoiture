import os
import joblib
import configparser
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

class ModelDePrediction:
    def __init__(self, config_path='../config/ConfigBDD.ini'):
        # Charger la configuration
        config = configparser.ConfigParser()
        config.read(config_path)

        self.db_url = f"postgresql://{config['postgresql']['user']}:{config['postgresql']['password']}@{config['postgresql']['host']}:{config['postgresql']['port']}/{config['postgresql']['database']}"
        self.model_dir = config['properties']['rep_sauve_model']

        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
    #Méthode pour entrainer le modele et le sauvegarder pour une utilisation
    def train_and_save_model(self):
        print("Chargement des données depuis la base de données...")
        engine = create_engine(self.db_url)
        query = """
            SELECT marque, modele, annee, kilometrage, boite_vitesse, carburant, prix
            FROM dataproject.voiture
        """
        data = pd.read_sql_query(query, engine)

        print("Préparation des données...")
        #Séparation des données
        X = pd.get_dummies(data[['marque', 'modele', 'annee', 'kilometrage', 'boite_vitesse', 'carburant']])
        data['prix_log'] = np.log1p(data['prix'])
        y = data['prix_log']

        # Standardisation
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Division des données
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Entraîner le modèle
        model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
        model.fit(X_train, y_train)

        # Évaluer le modèle
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(np.expm1(y_test), np.expm1(y_pred))
        r2 = r2_score(np.expm1(y_test), np.expm1(y_pred))
        print(f"MAE : {mae:.2f}")
        print(f"R² : {r2:.2f}")

        # Sauvegarder le modèle
        model_path = os.path.join(self.model_dir, "prix_voiture_model.pkl")
        scaler_path = os.path.join(self.model_dir, "scaler.pkl")
        features_path = os.path.join(self.model_dir, "features.pkl")

        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        joblib.dump(list(X.columns), features_path)

        print(f"Modèl et objets sauvegardés dans {self.model_dir}.")


