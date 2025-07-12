from fastapi import APIRouter, HTTPException
from ConnexionBDD import DatabaseConnection

router = APIRouter()
db = DatabaseConnection()
db.connect()  # Ensure connection is attempted when the module is loaded


@router.get("/voiture")
def get_voitures_stats(marque: str):
    try:
        result = db.execute_query("""
                                  SELECT annee, COUNT(*) as nombre
                                  FROM dataproject.voiture
                                  WHERE marque = %s
                                  GROUP BY annee
                                  ORDER BY annee ASC
                                  """, (marque,))

        if result is None or not result:
            return {
                "annees": [],
                "quantite": []
            }

        # Access elements by index since RealDictCursor is not used
        return {
            "annees": [r[0] for r in result],  # r[0] is 'annee'
            "quantite": [r[1] for r in result]  # r[1] is 'nombre'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/carburant")
def get_carburant_stats(marque: str):
    try:
        result = db.execute_query("""
                                  SELECT carburant, COUNT(*) as nombre
                                  FROM dataproject.voiture
                                  WHERE marque = %s
                                  GROUP BY carburant
                                  """, (marque,))
        if result is None or not result:
            return {}
        # Access elements by index
        return {r[0]: r[1] for r in result}  # r[0] is 'carburant', r[1] is 'nombre'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/boite")
def get_boite_stats(marque: str):
    try:
        result = db.execute_query("""
                                  SELECT boite_vitesse, COUNT(*) as nombre
                                  FROM dataproject.voiture
                                  WHERE marque = %s
                                  GROUP BY boite_vitesse
                                  """, (marque,))
        if result is None or not result:
            return {}
        # Access elements by index
        return {r[0]: r[1] for r in result}  # r[0] is 'boite_vitesse', r[1] is 'nombre'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kilometrage")
def get_kilometrage_stats(marque: str):
    try:
        result = db.execute_query("""
                                  SELECT annee, AVG(kilometrage) as km_moyen
                                  FROM dataproject.voiture
                                  WHERE marque = %s
                                  GROUP BY annee
                                  ORDER BY annee ASC
                                  """, (marque,))
        if result is None or not result:
            return {
                "annees": [],
                "kilometrage_moyen": []
            }
        # Access elements by index
        return {
            "annees": [r[0] for r in result],  # r[0] is 'annee'
            "kilometrage_moyen": [round(r[1], 2) for r in result]  # r[1] is 'km_moyen'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/modeles")
def get_modeles_par_marque():
    try:
        result = db.execute_query("""
                                  SELECT marque, COUNT(DISTINCT modele) as nb_modeles
                                  FROM dataproject.voiture
                                  GROUP BY marque
                                  """)
        if result is None or not result:
            return {}
        # Access elements by index
        return {r[0]: r[1] for r in result}  # r[0] is 'marque', r[1] is 'nb_modeles'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))