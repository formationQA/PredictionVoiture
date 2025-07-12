import psycopg2
import configparser


class DatabaseConnection:
    fichier_configuration = '../config/ConfigBDD.ini'

    def __init__(self):
        self.db_config, self.Config_Sup = self.ImportConfiguration(self.fichier_configuration)
        self.connection = None

    @staticmethod
    def ImportConfiguration(fichier_configuration):
        parser = configparser.ConfigParser()
        parser.read(fichier_configuration)

        # Options de connexion pour PostgreSQL
        db_config = {
            'dbname': parser.get('postgresql', 'database'),
            'user': parser.get('postgresql', 'user'),
            'password': parser.get('postgresql', 'password'),
            'host': parser.get('postgresql', 'host'),
            'port': parser.get('postgresql', 'port')
        }

        Config_Sup = {
            'rep_sauvegarde_json': parser.get('properties', 'rep_sauvegarde_json'),
            'rep_sauve_model': parser.get('properties', 'rep_sauve_model')  # Ajouter cette clé
        }

        return db_config, Config_Sup

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print("Connexion à la base de données réussie")
        except psycopg2.OperationalError as e:
            print(f"Erreur lors de la connexion : {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Déconnexion réussie")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return None