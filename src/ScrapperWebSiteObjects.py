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

    # Télécharge le contenu HTML d'une page spécifique du site d'annonces
    def TelechargerPagesHtml(self, page_num):
        try:
            # Construit l’URL complète avec le numéro de page
            site_scrapper = f"{self.site_annonces}&page={page_num}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            # Envoie la requête HTTP GET
            response = self.session.get(site_scrapper, headers=headers)
            response.raise_for_status()
            return response.text  # Retourne le contenu HTML
        except requests.exceptions.RequestException as e:
            print(f'Erreur => erreur lors de telechargement : {e}')
            return None

    def SauvegardePage(self, content, page_num):
        # Sauvegarde le contenu HTML dans un fichier
        if not os.path.exists(self.rep_sauvegarde_html):
            os.makedirs(self.rep_sauvegarde_html)

        filename = os.path.join(self.rep_sauvegarde_html, f'pageHTML_{page_num}.html')

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f'Sauvegarde de la page HTML =>  {filename}')

    def ScrapperSiteAnnonces(self):
        # Boucle sur toutes les pages à scraper
        for page_num in range(1, self.nb_page + 1):
            page_content = self.TelechargerPagesHtml(page_num)

            if page_content:
                # Sauvegarde la page si elle a bien été récupérée
                self.SauvegardePage(page_content, page_num)
            else:
                break
            #délai entre deux requêtes
            time.sleep(self.delai_requete)
