import requests
import os
import time
import configparser

class WebScraper:
    fichier_configuration = '../config/ConfigBDD.ini'

    def __init__(self):
        self.config = self.ImportConfiguration(self.fichier_configuration)
        self.site_annonces = self.config['site_annonces']
        self.rep_sauvegarde_html = self.config['rep_sauvegarde_html']
        self.nb_page = int(self.config['nb_page'])
        self.delai_requete = int(self.config['delai_requete'])
        self.session = requests.Session()

    @staticmethod
    def ImportConfiguration(fichier_configuration):
        parser = configparser.ConfigParser()
        parser.read(fichier_configuration)
        db_config = {
            'site_annonces': parser.get('properties', 'site_annonces'),
            'rep_sauvegarde_html': parser.get('properties', 'rep_sauvegarde_html'),
            'nb_page': parser.get('properties', 'nb_page'),
            'delai_requete': parser.get('properties', 'delai_requete'),
        }
        return db_config

    def TelechargerPagesHtml(self, page_num):
        try:
            site_scrapper = f"{self.site_annonces}&page={page_num}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = self.session.get(site_scrapper, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f'Erreur => erreur lors de telechargement : {e}')
            return None

    def SauvegardePage(self, content, page_num):
        if not os.path.exists(self.rep_sauvegarde_html):
            os.makedirs(self.rep_sauvegarde_html)
        filename = os.path.join(self.rep_sauvegarde_html, f'pageHTML_{page_num}.html')
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Sauvegarde de la page HTML =>  {filename}')

    def ScrapperSiteAnnonces(self):
        for page_num in range(1, self.nb_page + 1):
            page_content = self.TelechargerPagesHtml(page_num)
            if page_content:
                self.SauvegardePage(page_content, page_num)
            else:
                break
            time.sleep(self.delai_requete)