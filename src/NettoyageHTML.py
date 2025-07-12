import os
import configparser
from bs4 import BeautifulSoup

class NettoyageHtml:

    fichier_configuration = '../config/ConfigBDD.ini'

    def __init__(self):
        self.config = self.ImportConfiguration(self.fichier_configuration)
        self.rep_sauvegarde_html = self.config['rep_sauvegarde_html']
        self.rep_sauvegarde_txt = self.config['rep_sauvegarde_txt']

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
        parcourir = BeautifulSoup(ContenueHtml, 'lxml')
        ContenueExtrait = parcourir.find_all('div', class_='vehicle-information-wrapper')
        ContenueText = [div.get_text(separator='\n', strip=True) for div in ContenueExtrait]
        return '\n\n'.join(ContenueText)

    def TraitementFichiersHTML(self):
        for fichiers in os.listdir(self.rep_sauvegarde_html):
            if fichiers.endswith('.html'):
                fichiersUrl = os.path.join(self.rep_sauvegarde_html, fichiers)
                with open(fichiersUrl, 'r', encoding='utf-8') as file:
                    ContenueHtml = file.read()
                    NetoyageContenue = self.ExtractionInformationVoiture(ContenueHtml)

                    NomFichierSortie = os.path.splitext(fichiers)[0] + '.txt'
                    RepertoireSortie = os.path.join(self.rep_sauvegarde_txt, NomFichierSortie)
                    self.SauvegardeFichiers(NetoyageContenue, RepertoireSortie)
                    os.remove(fichiersUrl)
                    print(f'La page HTML est bien nettoyé')

    @staticmethod
    def SauvegardeFichiers(Contenue, UrlSauvegarde):
        with open(UrlSauvegarde, 'w', encoding='utf-8') as file:
            file.write(Contenue )