class VoitureRepository:
    def __init__(self, db_connection):
        self.connection = db_connection

#Verifié si une voiture existe en base avec la meme marque et model et année
#si non on passe à l'insertion sinon on vérifié les autre caract
    def voiture_existe_et_differe(self, row):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT kilometrage, boite_vitesse, prix, carburant
            FROM dataproject.voiture
            WHERE marque = %s AND modele = %s AND annee = %s
            """,
            (row['marque'], row['modele'], row['annee'])
        )
        result = cursor.fetchone()
        cursor.close()
        if not result:
            return False

        existing_kilometrage, existing_boite_vitesse, existing_prix, existing_carburant = result
        return not (
            row.get('kilometrage') == existing_kilometrage and
            row.get('boite_vitesse') == existing_boite_vitesse and
            row.get('prix') == existing_prix and
            row.get('carburant') == existing_carburant
        )

    # data est un DataFrame pandas contenant plusieurs voitures.
    # insérer les données de datFrame si n'existe pas
    def inserer_voitures(self, data, id_fichier):
        try:
            cursor = self.connection.cursor()
            for _, row in data.iterrows():
                if 'marque' in row and 'modele' in row and 'annee' in row:
                    if not self.voiture_existe_et_differe(row):
                        cleaned_row = [
                            row.get('marque', "").upper(),
                            row.get('modele', ""),
                            row.get('kilometrage', 0),
                            row.get('annee', 0),
                            row.get('boite_vitesse', ""),
                            row.get('prix', 0),
                            row.get('carburant', ""),
                            id_fichier
                        ]
                        insert_query = """
                            INSERT INTO dataproject.voiture (marque, modele, kilometrage, annee, boite_vitesse, prix, carburant, id_fichier)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(insert_query, cleaned_row)
                    else:
                        print(f"Une voiture avec les mêmes caractristiques existe déjàa en base: {row['marque']} {row['modele']} {row['annee']}")
                else:
                    print(f"Ligne manquante : {row}")

            self.connection.commit()
            cursor.close()
            print("Données insérées.")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données de voiture : {e}")
