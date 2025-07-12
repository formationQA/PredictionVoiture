import re   #Traiter les regexs
import os   #traiter le system fichier
import json #manipuler les fichiers JSON
import configparser #manipuler le fichier de config (ini)
from datetime import datetime, timedelta
from threading import Lock


class JsonConvert:
    fichier_configuration = '../config/ConfigBDD.ini'

    #COnstructeur
    def __init__(self):
        self.config = self.ImportConfiguration(self.fichier_configuration)
        self.rep_sauvegarde_txt = self.config['rep_sauvegarde_txt']
        self.rep_sauvegarde_json = self.config['rep_sauvegarde_json']
        self.last_generated_time = None
        self.counter = 0
        self.lock = Lock()

    @staticmethod
    def ImportConfiguration(fichier_configuration):
        parser = configparser.ConfigParser()
        parser.read(fichier_configuration)
        configuration = {
            'rep_sauvegarde_txt': parser.get('properties', 'rep_sauvegarde_txt'),
            'rep_sauvegarde_json': parser.get('properties', 'rep_sauvegarde_json')
        }
        return configuration

#Nettoyage de chaînes de caractères (ne garde que les chiffres)
    @staticmethod
    def NettoyerNum(number_str):
        return re.sub(r'[^\d]', '', number_str)

#Filtrer les lignes spéciales
    @staticmethod
    def NettoyerLignes(lines):
        ligne = [line for line in lines if line.strip() and line.strip() != "•"]
        ligne = [line for line in ligne if not line.startswith("Dès")]
        ligne = [line for line in ligne if not line.startswith("+")]
        return ligne

#Découper un texte en sections
    @staticmethod
    def ExtraireSections(text):
        sections = text.strip().split('\n\n')
        return [section.strip() for section in sections if section.strip()]

#Préparer les données JSON pour chaque voiture
    @staticmethod
    def PreparerDonneesJson(info_voitures):
        sections = JsonConvert.ExtraireSections(info_voitures)
        voitures = []
        for section in sections:
            lines = section.split('\n')
            lines = JsonConvert.NettoyerLignes(lines)

            Voiture = {
                "marque": lines[0].split()[0] if len(lines) > 0 and len(lines[0].split()) > 0 else "",
                "modele": " ".join(lines[0].split()[1:]) if len(lines) > 0 and len(lines[0].split()) > 1 else "",
                "prix": lines[8].replace(' €', '').replace(' ', '') if len(lines) > 8 else "",
                "kilometrage": lines[6].replace(' km', '').replace(' ', '') if len(lines) > 6 else "",
                "boite_vitesse": lines[4] if len(lines) > 4 else "",
                "carburant": lines[3] if len(lines) > 3 else "",
                "annee": lines[5] if len(lines) > 5 else ""
            }
            voitures.append(Voiture)

        return voitures

    @staticmethod
    def LectureFichier(fichier):
        with open(fichier, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def InsertionDansJSON(data, fichier_sortie):
        with open(fichier_sortie, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def GenererNomFichier(self):
        with self.lock:
            now = datetime.now()
            date_str = now.strftime("%Y%m%d_%H%M%S")
            milliseconds = f"{now.microsecond // 1000:03}"
            if self.last_generated_time == (date_str, milliseconds):
                self.counter += 1
            else:
                self.last_generated_time = (date_str, milliseconds)
                self.counter = 0
            return f"DSW_{date_str}{milliseconds}_{self.counter}.json"

    def SauvegardeJSON(self):
        if not os.path.exists(self.rep_sauvegarde_json):
            os.makedirs(self.rep_sauvegarde_json)

        for filename in sorted(os.listdir(self.rep_sauvegarde_txt)):
            if filename.endswith('.txt'):
                print(f"Traitement du fichier: {filename}")

                fichier = os.path.join(self.rep_sauvegarde_txt, filename)
                text = self.LectureFichier(fichier)
                data = self.PreparerDonneesJson(text)
                print(f"Données extraites: {data}")

                json_filename = self.GenererNomFichier()
                fichier_sortie = os.path.join(self.rep_sauvegarde_json, json_filename)

                self.InsertionDansJSON(data, fichier_sortie)
                os.remove(fichier)
                print(f"Fichier JSON sauvegardé : {fichier_sortie}")
