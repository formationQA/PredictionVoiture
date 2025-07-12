from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
from ConnexionBDD import DatabaseConnection

class PredictionAPI:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.model_dir = self.db_connection.Config_Sup['rep_sauve_model']
        self.model_path = os.path.join(self.model_dir, "prix_voiture_model.pkl")
        self.scaler_path = os.path.join(self.model_dir, "scaler.pkl")
        self.features_path = os.path.join(self.model_dir, "features.pkl")

        # Charger le modèle, le scaler et les features
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        self.features = joblib.load(self.features_path)

    def predict(self, data):
        try:
            input_data = pd.DataFrame([data])
            input_encoded = pd.get_dummies(input_data)

            # Ajouter les colonnes manquantes
            for col in self.features:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0

            input_encoded = input_encoded[self.features]
            input_scaled = self.scaler.transform(input_encoded)

            predicted_log_price = self.model.predict(input_scaled)
            predicted_price = np.expm1(predicted_log_price)

            return round(predicted_price[0], 2)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Définir le routeur pour l'API
router = APIRouter()

# Schéma des données pour la prédiction
class CarData(BaseModel):
    marque: str
    modele: str
    annee: int
    kilometrage: int
    boite_vitesse: str
    carburant: str

# Instance de la connexion à la base de données
db = DatabaseConnection()
db.connect()
api = PredictionAPI(db)

@router.post("/predict")
def predict_price(car: CarData):
    """
    Endpoint pour prédire le prix d'une voiture.
    """
    predicted_price = api.predict(car.dict())
    return {"predicted_price": predicted_price}
