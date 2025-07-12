import datetime


class FichierRepository:
    def __init__(self, db_connection):
        self.connection = db_connection

    def obtenir_id_fichier(self, nom_fichier):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT id_fichier FROM dataproject.fichier WHERE nom_fichier = %s
            """,
            (nom_fichier,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def inserer_fichier(self, nom_fichier):
        id_fichier = self.obtenir_id_fichier(nom_fichier)
        if id_fichier:
            print(f"Le fichier '{nom_fichier}' existe déjà avec id_fichier={id_fichier}")
            return id_fichier

        try:
            cursor = self.connection.cursor()
            date_integration = datetime.datetime.now()
            insert_query = """
                INSERT INTO dataproject.fichier (nom_fichier, date_integration)
                VALUES (%s, %s) RETURNING id_fichier;
            """
            cursor.execute(insert_query, (nom_fichier, date_integration))
            id_fichier = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            print(f"Le fichier '{nom_fichier}' a été inséré avec succès, id_fichier={id_fichier}")
            return id_fichier
        except Exception as e:
            print(f"Erreur lors de l'intégration du fichier : {e}")
            return None
