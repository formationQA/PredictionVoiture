import os
import zipfile
import shutil
import configparser
from datetime import datetime


class JsonSauvegarde:
    fichier_configuration = '../config/ConfigBDD.ini'

    def __init__(self):
        self.config = self.ImportConfiguration(self.fichier_configuration)
        self.rep_sauvegarde_json = self.config['rep_sauvegarde_json']
        self.rep_sauve = self.config['rep_sauve']

    @staticmethod
    def ImportConfiguration(fichier_configuration):
        parser = configparser.ConfigParser()
        parser.read(fichier_configuration)
        configuration = {
            'rep_sauvegarde_json': parser.get('properties', 'rep_sauvegarde_json'),
            'rep_sauve': parser.get('properties', 'rep_sauve')
        }
        return configuration

    def CompresserJSon(self):
        # Condition si le fichier JSON n'existe pas
        if not os.path.exists(self.rep_sauvegarde_json):
            return

        if not os.path.exists(self.rep_sauve):
            os.makedirs(self.rep_sauve)

        # Nommage de fichier ZIP avec date et heure
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = os.path.join(self.rep_sauvegarde_json, f"JSON_Sauvegarde_{now}.zip")

        # Création du fichier ZIP et ajout des fichiers JSON
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(self.rep_sauvegarde_json):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.rep_sauvegarde_json, filename)
                    zipf.write(filepath, os.path.basename(filepath))

        # Copie du fichier ZIP dans le dossier de sauvegarde
        shutil.copy(zip_filename, self.rep_sauve)
        # Supprime tous les fichiers du dossier JSON
        shutil.rmtree(self.rep_sauvegarde_json)
        os.makedirs(self.rep_sauvegarde_json)
        # Message de confirmation
        print(f"Le répertoire de sauvegarde JSON a été compressé et vidé.")
