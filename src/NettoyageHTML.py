import os
import configparser
from bs4 import BeautifulSoup  # Pour parser et extraire le contenu HTML


class NettoyageHtml:
    fichier_configuration = '../config/ConfigBDD.ini'

    def __init__(self):
        self.config = self.ImportConfiguration(self.fichier_configuration)
        self.rep_sauvegarde_html = self.config['rep_sauvegarde_html']  # Dossier source des fichiers HTML
        self.rep_sauvegarde_txt = self.config['rep_sauvegarde_txt']    # Dossier de sortie pour les fichiers TXT

    #Méthode pour importer la configuration de fichier .ini
    @staticmethod
    def ImportConfiguration(fichier_configuration):
        parser = configparser.ConfigParser()
        parser.read(fichier_configuration)

        configuration = {
            'rep_sauvegarde_html': parser.get('properties', 'rep_sauvegarde_html'),
            'rep_sauvegarde_txt': parser.get('properties', 'rep_sauvegarde_txt')
        }
        return configuration

    def ExtractionInformationVoiture(self, ContenueHtml):
        # Parse le contenu HTML et extrait les informations
        parcourir = BeautifulSoup(ContenueHtml, 'lxml')
        # Recherche les div contenant les infos du véhicule
        ContenueExtrait = parcourir.find_all('div', class_='vehicle-information-wrapper')
        # Nettoie le texte et le formate
        ContenueText = [div.get_text(separator='\n', strip=True) for div in ContenueExtrait]
        return '\n\n'.join(ContenueText)  # Retourne le texte extrait et formaté

    def TraitementFichiersHTML(self):
        # Parcourt tous les fichiers dans le dossier HTML
        for fichiers in os.listdir(self.rep_sauvegarde_html):
            if fichiers.endswith('.html'):
                fichiersUrl = os.path.join(self.rep_sauvegarde_html, fichiers)

                with open(fichiersUrl, 'r', encoding='utf-8') as file:
                    ContenueHtml = file.read()
                    # Extrait et nettoie les données
                    NetoyageContenue = self.ExtractionInformationVoiture(ContenueHtml)

                    # Nommage le fichier de sortie
                    NomFichierSortie = os.path.splitext(fichiers)[0] + '.txt'
                    RepertoireSortie = os.path.join(self.rep_sauvegarde_txt, NomFichierSortie)

                    # Sauvegarde le fichier en .txt
                    self.SauvegardeFichiers(NetoyageContenue, RepertoireSortie)

                    # Supprime le fichier HTML utilisé
                    os.remove(fichiersUrl)

                    print(f'La page HTML "{fichiers}" a été nettoyée et sauvegardée.')

    @staticmethod
    def SauvegardeFichiers(Contenue, UrlSauvegarde):
        with open(UrlSauvegarde, 'w', encoding='utf-8') as file:
            file.write(Contenue)
