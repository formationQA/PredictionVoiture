import os
import pandas as pd
import re
from src.FichiersDonneesObjects import FichierRepository
from src.VoituresDonneesObjects import VoitureRepository


class InsertionDonnees:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.json_directory = db_connection.Config_Sup['rep_sauvegarde_json']
        self.fichier_repo = FichierRepository(self.db_connection.connection)
        self.voiture_repo = VoitureRepository(self.db_connection.connection)

    def InsererLesDonneesEnBase(self):
        if not os.path.exists(self.json_directory):
            print(f"erreur ")
            return

        json_fichier = sorted([f for f in os.listdir(self.json_directory) if f.endswith('.json')])

        for fichier in json_fichier:
            file_path = os.path.join(self.json_directory, fichier)
            print(f"Traitement du fichier {fichier}")

            try:
                id_fichier = self.fichier_repo.inserer_fichier(fichier)
                if id_fichier:
                    data = pd.read_json(file_path)
                    valid_data = self.ValiderLesDonneesViaRgex(data)
                    self.voiture_repo.inserer_voitures(valid_data, id_fichier)
                self.db_connection.connection.commit()
            except Exception as e:
                print(f"Erreur {fichier}: {e}")
                self.db_connection.connection.rollback()

    def ValiderLesDonneesViaRgex(self, data):
        regex_patterns = {
            'marque': r'^[\w\sÀ-ÖØ-öø-ÿ]+$',
            'modele': r'^[\w\sÀ-ÖØ-öø-ÿ]+$',
            'kilometrage': r'^\d+$',
            'annee': r'^\d{4}$',
            'boite_vitesse': r'^[A-Za-z\s]+$',
            'prix': r'^\d+$',
            'carburant': r'^[\w\sÀ-ÖØ-öø-ÿ\s]+$',
        }
        valid_data = []
        for _, row in data.iterrows():
            if all(re.match(regex_patterns[field], str(row.get(field, ""))) for field in regex_patterns):
                valid_data.append(row)

        return pd.DataFrame(valid_data)
