import datetime  # Import du module datetime

# Classe FichierRepository pour gérer les interactions avec la table 'fichier'
class FichierRepository:
    def __init__(self, db_connection):
        self.connection = db_connection  # Connexion à la base de données

    # Méthode pour obtenir id d'un fichier à partir de nom
    def obtenir_id_fichier(self, nom_fichier):
        cursor = self.connection.cursor()  # Création d'un curseur pour exécuter SQL
        cursor.execute(
            """
            SELECT id_fichier FROM dataproject.fichier WHERE nom_fichier = %s
            """,
            (nom_fichier,)  # Passage du paramètre sous forme de tuple
        )
        result = cursor.fetchone()
        cursor.close()  # Fermeture du curseur
        return result[0] if result else None  # Retourne l'ID du fichier

    # Méthode pour insérer un fichier s'il n'existe pas déjà
    def inserer_fichier(self, nom_fichier):
        id_fichier = self.obtenir_id_fichier(nom_fichier)
        if id_fichier:
            print(f"Le fichier '{nom_fichier}' existe déjà avec id_fichier={id_fichier}")
            return id_fichier

        try:
            cursor = self.connection.cursor()  # Création d'un curseur pour l'insertion
            date_integration = datetime.datetime.now()  # Récupération de la date et heure
            insert_query = """
                INSERT INTO dataproject.fichier (nom_fichier, date_integration)
                VALUES (%s, %s) RETURNING id_fichier;
            """  # Requête SQL pour insérertion
            cursor.execute(insert_query, (nom_fichier, date_integration))  # Exécution de la requête avec les paramètres
            id_fichier = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()  # Fermeture du curseur
            print(f"Le fichier '{nom_fichier}' a été inséré avec succès, id_fichier={id_fichier}")  # Message d'info
            return id_fichier  # Retourne l'identifiant généré

        except Exception as e:
            print(f"Erreur lors de l'intégration du fichier : {e}")
            return None