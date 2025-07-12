from fastapi import FastAPI
from WebApiModel import router as prediction_router
from ApiFormulaireWeb import router as formulaire_router
from fastapi.middleware.cors import CORSMiddleware
from ApiStats import router as stats_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorisez toutes les origines. Remplacez par ["http://localhost:63342"] pour restreindre.
    allow_credentials=True,
    allow_methods=["*"],  # Autorisez toutes les méthodes HTTP.
    allow_headers=["*"],  # Autorisez tous les headers.
)


# Inclure les deux routeurs
app.include_router(prediction_router, prefix="/api/prediction", tags=["Prediction"])
app.include_router(formulaire_router, prefix="/api/formulaire", tags=["Formulaire"])
app.include_router(stats_router, prefix="/api/stats", tags=["Stats"])

# Point de test de l'API
@app.get("/")
def read_root():
    return {"message": "API pour prédiction et formulaire de voitures"}
