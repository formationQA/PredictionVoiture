from fastapi import APIRouter, HTTPException
from ConnexionBDD import DatabaseConnection

class FormulaireAPI:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_marques(self):
        # Requête SQL pour récupérer toutes les marques
        query = ("SELECT DISTINCT marque FROM dataproject.voiture "
                 "ORDER BY marque asc ")
        return self.db_connection.execute_query(query)

    def get_modeles(self, marque):
        # Requête SQL pour récupérer les modèles d'une marque donnée
        query = ("SELECT DISTINCT modele FROM dataproject.voiture WHERE marque = %s"
                 " ORDER BY modele ASC")
        return self.db_connection.execute_query(query, (marque,))


# Définir le routeur pour l'API
router = APIRouter()

# Instance de la connexion à la base de données
db = DatabaseConnection()
db.connect()
api = FormulaireAPI(db)

@router.get("/marques")
def get_marques():
    """
    Endpoint pour récupérer les marques.
    """
    try:
        marques = api.get_marques()
        return {"marques": [row[0] for row in marques]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/modeles")
def get_modeles(marque: str):
    """
    Endpoint pour récupérer les modèles pour une marque donnée.
    """
    try:
        modeles = api.get_modeles(marque)
        return {"modeles": [row[0] for row in modeles]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
