import os  # Traiter des fichiers système
import pandas as pd  # Pour manipuler les fichiers JSON
import re  # Manipuler des regex
from src.FichiersDonneesObjects import FichierRepository  # Gestion table 'fichier'
from src.VoituresDonneesObjects import VoitureRepository  # Gestion table 'voiture'


class InsertionDonnees:
    def __init__(self, db_connection):
        self.db_connection = db_connection

        self.json_directory = db_connection.Config_Sup['rep_sauvegarde_json']

        # Création des repositories pour insérer fichiers et voitures
        self.fichier_repo = FichierRepository(self.db_connection.connection)
        self.voiture_repo = VoitureRepository(self.db_connection.connection)

    def InsererLesDonneesEnBase(self):
        # Vérifie si le répertoire JSON existe
        if not os.path.exists(self.json_directory):
            print("Erreur : le dossier JSON est introuvable.")
            return

        # Liste des fichiers .json dans le répertoire
        json_fichier = sorted([f for f in os.listdir(self.json_directory) if f.endswith('.json')])

        # Parcourir caque fichier json
        for fichier in json_fichier:
            file_path = os.path.join(self.json_directory, fichier)
            print(f"Traitement du fichier {fichier}")

            try:
                # Ajoute le fichier dans la base et récupère l'id
                id_fichier = self.fichier_repo.inserer_fichier(fichier)

                if id_fichier:
                    # json en DataFrame
                    data = pd.read_json(file_path)

                    # Filtre les données valides via regex
                    valid_data = self.ValiderLesDonneesViaRgex(data)

                    # Insère les données valides dans la base
                    self.voiture_repo.inserer_voitures(valid_data, id_fichier)

                self.db_connection.connection.commit()

            except Exception as e:
                print(f"Erreur lors du traitement du fichier {fichier} : {e}")
                self.db_connection.connection.rollback()

    def ValiderLesDonneesViaRgex(self, data):
        # Règles de validation p
        regex_patterns = {
            'marque': r'^[\w\sÀ-ÖØ-öø-ÿ]+$',
            'modele': r'^[\w\sÀ-ÖØ-öø-ÿ]+$',
            'kilometrage': r'^\d+$',
            'annee': r'^\d{4}$',
            'boite_vitesse': r'^[A-Za-z\s]+$',
            'prix': r'^\d+$',
            'carburant': r'^[\w\sÀ-ÖØ-öø-ÿ\s]+$',
        }

        valid_data = []  # Liste pour les lignes valides

        # Vérifie chaque ligne de données
        for _, row in data.iterrows():
            if all(re.match(regex_patterns[field], str(row.get(field, ""))) for field in regex_patterns):
                valid_data.append(row)

        return pd.DataFrame(valid_data)
