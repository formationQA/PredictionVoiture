import streamlit as st
import requests
import plotly.express as px

# Configuration de la page Streamlit
st.set_page_config(page_title="Statistiques Voitures", page_icon="📊")
st.title("📊 Statistiques détaillées des voitures")


# Fonction pour récupérer des données depuis une API avec gestion d'erreur
def get_data(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None


# Récupération des marques disponibles
marques_data = get_data("http://127.0.0.1:8002/api/formulaire/marques")
marques = marques_data.get("marques", []) if marques_data else []

if not marques:
    st.warning("Aucune marque disponible. Vérifiez la base de données et que le backend FastAPI est lancé.")
else:
    # Sélection de la marque par l'utilisateur
    marque = st.selectbox("Choisissez une marque :", marques)

    if marque:
        st.subheader(f"Statistiques pour {marque}")

        # 1. Histogramme du nombre de voitures par année
        stats = get_data("http://127.0.0.1:8002/api/stats/voiture", params={"marque": marque})
        if stats and stats.get('annees') and stats.get('quantite'):
            fig = px.bar(x=stats['annees'], y=stats['quantite'],
                         labels={'x': 'Année', 'y': 'Nombre'},
                         title=f"Nombre de voitures par année pour {marque}")
            st.plotly_chart(fig)
        else:
            st.info(f"Aucune statistique par année disponible pour {marque}.")

        # 2. Camembert répartition carburant
        carburant = get_data("http://127.0.0.1:8002/api/stats/carburant", params={"marque": marque})
        if carburant:
            fig = px.pie(values=list(carburant.values()), names=list(carburant.keys()),
                         title=f"Répartition carburant pour {marque}")
            st.plotly_chart(fig)
        else:
            st.info(f"Aucune statistique de carburant disponible pour {marque}.")

        # 3. Camembert répartition transmission
        boite = get_data("http://127.0.0.1:8002/api/stats/boite", params={"marque": marque})
        if boite:
            fig = px.pie(values=list(boite.values()), names=list(boite.keys()),
                         title=f"Répartition transmission pour {marque}")
            st.plotly_chart(fig)
        else:
            st.info(f"Aucune statistique de transmission disponible pour {marque}.")

        # 4. Courbe du kilométrage moyen par année
        km_stats = get_data("http://127.0.0.1:8002/api/stats/kilometrage", params={"marque": marque})
        if km_stats and km_stats.get('annees') and km_stats.get('kilometrage_moyen'):
            fig = px.line(x=km_stats['annees'], y=km_stats['kilometrage_moyen'],
                          labels={'x': 'Année', 'y': 'Kilométrage moyen'},
                          title=f"Kilométrage moyen des {marque}")
            st.plotly_chart(fig)
        else:
            st.info(f"Aucune statistique de kilométrage disponible pour {marque}.")

# Statistiques globales : nombre de modèles par marque
st.subheader("Nombre de modèles par marque")
modeles = get_data("http://127.0.0.1:8002/api/stats/modeles")
if modeles:
    fig = px.bar(x=list(modeles.keys()), y=list(modeles.values()),
                 labels={'x': 'Marque', 'y': 'Nombre de modèles'},
                 color=list(modeles.values()),
                 title="Nombre de modèles par marque")
    st.plotly_chart(fig)
else:
    st.info("Aucune statistique de modèles disponible.")
