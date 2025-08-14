import re
import os
import json
import configparser
import subprocess
from datetime import datetime
from threading import Lock


class JsonConvert:
    fichier_configuration = '../config/ConfigBDD.ini'

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
        return {
            'rep_sauvegarde_txt': parser.get('properties', 'rep_sauvegarde_txt'),
            'rep_sauvegarde_json': parser.get('properties', 'rep_sauvegarde_json')
        }

    @staticmethod
    def NettoyerNum(number_str):
        return re.sub(r'[^\d]', '', number_str)

    @staticmethod
    def NettoyerLignes(lines):
        ligne = [line for line in lines if line.strip() and line.strip() != "•"]
        ligne = [line for line in ligne if not line.startswith("Dès")]
        ligne = [line for line in ligne if not line.startswith("+")]
        return ligne

    @staticmethod
    def ExtraireSections(text):
        sections = text.strip().split('\n\n')
        return [section.strip() for section in sections if section.strip()]

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

    @staticmethod
    def ValiderJSON(fichier):
        """
        Utilise le binaire json_validator compilé avec Bison/Flex pour valider.
        """
        try:
            result = subprocess.run(
                ["../parser/json_validator", fichier],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return result.returncode == 0
        except FileNotFoundError:
            print("⚠️ Erreur : json_validator introuvable. Compile-le avec `make`.")
            return False

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
                print(f"📄 Traitement du fichier: {filename}")

                fichier = os.path.join(self.rep_sauvegarde_txt, filename)
                text = self.LectureFichier(fichier)
                data = self.PreparerDonneesJson(text)

                json_filename = self.GenererNomFichier()
                fichier_sortie = os.path.join(self.rep_sauvegarde_json, json_filename)

                self.InsertionDansJSON(data, fichier_sortie)

                # Validation avec json_validator
                if not self.ValiderJSON(fichier_sortie):
                    print(f"❌ JSON invalide, suppression : {fichier_sortie}")
                    os.remove(fichier_sortie)
                else:
                    print(f"✅ JSON valide sauvegardé : {fichier_sortie}")

                os.remove(fichier)
